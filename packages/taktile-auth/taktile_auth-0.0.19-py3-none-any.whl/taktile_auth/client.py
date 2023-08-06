import datetime
import json
import typing as t

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from pydantic import BaseModel, ValidationError

from taktile_auth.exceptions import InvalidAuthException, TaktileAuthException
from taktile_auth.schemas.session import SessionState
from taktile_auth.schemas.token import TaktileIdToken
from taktile_auth.settings import settings
from taktile_auth.utils.cache import Cache

ALGORITHM = "RS256"


def _get_auth_server_url(env: str) -> str:
    if env == "local":
        return "http://taktile-api.local.taktile.com:8000"
    if env == "prod":
        return "https://taktile-api.taktile.com"
    return f"https://taktile-api.{env}.taktile.com"


class AuthClient:
    class JWTResponseSuccess(BaseModel):
        token: str

    class JWTResponseAllowedFailure(BaseModel):
        """A failure which allows us to use the cache"""

        exception: t.Any

    class JWTResponseForbiddenFailure(BaseModel):
        """A failure which doesn't allow us to use the cache"""

        exception: t.Any

    class CacheResponse(BaseModel):
        """Response from the cache"""

        token: str
        is_in_speedup_window: bool

    def __init__(
        self,
        url: str = _get_auth_server_url(settings.ENV),
        cache: t.Optional[Cache] = None,
        cache_speedup_time: datetime.timedelta = datetime.timedelta(
            minutes=settings.CACHE_SPEEDUP_TIME_MINUTES
        ),
        cache_fallback_time: datetime.timedelta = datetime.timedelta(
            minutes=settings.CACHE_FALLBACK_TIME_MINUTES
        ),
    ) -> None:
        self.public_key_url = f"{url}/.well-known/jwks.json"
        self.access_token_url = f"{url}/api/v1/login/access-token"
        self._cache = cache
        self._cache_speedup_time = cache_speedup_time
        self._cache_fallback_time = cache_fallback_time

    def get_public_key(
        self,
        *,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Any:
        jwk: t.Any = None
        if key:
            jwk = json.loads(key)
        else:
            try:
                response = requests.get(self.public_key_url, timeout=5)
                response.raise_for_status()
            except requests.exceptions.RequestException:
                if self._cache is not None:
                    jwk = self._cache.get("jwk")
            else:
                jwk = response.json()
                if self._cache is not None:
                    self._cache.put("jwk", jwk)

        if jwk is None:
            raise TaktileAuthException("No public key found")

        for k in jwk["keys"]:
            if k["kid"] == kid:
                return RSAAlgorithm.from_jwk(k)  # type: ignore
        raise InvalidAuthException("invalid-public-key")

    def decode_id_token(
        self,
        *,
        token: t.Optional[str] = None,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> TaktileIdToken:
        if not token:
            raise InvalidAuthException("no-auth-provided")
        try:
            public_key = self.get_public_key(key=key, kid=kid)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=[ALGORITHM],
                audience=settings.ENV,
            )
            return TaktileIdToken(**payload)
        except jwt.ExpiredSignatureError as exc:
            raise InvalidAuthException("signature-expired") from exc
        except (jwt.PyJWTError, ValidationError) as exc:
            raise InvalidAuthException("could-not-validate") from exc

    def get_access(
        self,
        *,
        session_state: SessionState,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Tuple[TaktileIdToken, SessionState]:
        if not session_state.api_key and not session_state.jwt:
            raise InvalidAuthException("no-auth-proved")

        if session_state.jwt:
            return (
                self.decode_id_token(
                    token=session_state.jwt, key=key, kid=kid
                ),
                session_state,
            )

        if cache_response := self._get_from_cache(
            session_state=session_state, key=key
        ):
            session_state.jwt = cache_response.token
            should_refresh = not cache_response.is_in_speedup_window
        else:
            should_refresh = False

        if not session_state.jwt or should_refresh:
            tapi_response = self._refresh_jwt(session_state=session_state)

            if isinstance(tapi_response, AuthClient.JWTResponseSuccess):
                session_state.jwt = tapi_response.token
                if self._cache:
                    self._cache.put(
                        str(session_state.api_key), tapi_response.token
                    )
            elif isinstance(
                tapi_response, AuthClient.JWTResponseAllowedFailure
            ):
                if session_state.jwt:
                    return (
                        self.decode_id_token(
                            token=session_state.jwt, key=key, kid=kid
                        ),
                        session_state,
                    )
                else:
                    raise InvalidAuthException(
                        "Auth server unreachable; no cached token"
                    ) from tapi_response.exception
            elif isinstance(
                tapi_response, AuthClient.JWTResponseForbiddenFailure
            ):
                raise InvalidAuthException(
                    "Auth server unreachable;"
                    " cache usage not allowed due to exception type"
                ) from tapi_response.exception

        return (
            self.decode_id_token(token=session_state.jwt, key=key, kid=kid),
            session_state,
        )

    def _get_from_cache(
        self, *, session_state: SessionState, key: t.Optional[str]
    ) -> t.Optional[CacheResponse]:
        """
        Take a look at PEP 76: Auth Cache Router for details on this logic
        """

        if self._cache is None or session_state.api_key is None:
            return None

        cached_jwt = self._cache.get(str(session_state.api_key))

        if not cached_jwt:
            return None

        try:
            token = self.decode_id_token(token=cached_jwt, key=key)
        except InvalidAuthException:
            self._cache.delete(str(session_state.api_key))
            return None

        issue_time = datetime.datetime.fromtimestamp(float(token.iat))

        is_in_speedup_window = (
            datetime.datetime.utcnow() < issue_time + self._cache_speedup_time
        )

        return AuthClient.CacheResponse(
            token=cached_jwt, is_in_speedup_window=is_in_speedup_window
        )

    def _refresh_jwt(
        self, *, session_state: SessionState
    ) -> t.Union[
        JWTResponseSuccess,
        JWTResponseAllowedFailure,
        JWTResponseForbiddenFailure,
    ]:
        """
        Take a look at PEP 76: Auth Cache Router for details on this logic
        """
        try:
            res = requests.post(
                self.access_token_url,
                headers=session_state.to_auth_headers(),
                timeout=2,
                params={
                    "expires_seconds": int(
                        self._cache_fallback_time.total_seconds()
                    )
                },
            )
            res.raise_for_status()
            id_token = res.json()["id_token"]
            return AuthClient.JWTResponseSuccess(token=id_token)

        except requests.exceptions.Timeout as exc:
            return AuthClient.JWTResponseAllowedFailure(exception=exc)
        except requests.exceptions.HTTPError as exc:
            if (
                exc.response.status_code in (404, 499)
                or exc.response.status_code >= 500
            ):
                return AuthClient.JWTResponseAllowedFailure(exception=exc)
            return AuthClient.JWTResponseForbiddenFailure(exception=exc)
        except Exception as exc:
            return AuthClient.JWTResponseForbiddenFailure(exception=exc)
