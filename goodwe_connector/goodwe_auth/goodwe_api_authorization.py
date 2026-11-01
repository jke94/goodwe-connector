import base64
import hashlib
import json
import time
from json import JSONDecodeError

from requests.exceptions import RequestException

from goodwe_connector.goodwe_constants import (
    GOODWE_SEMS_PLUS_API_URL,
    GOODWE_SEMS_PLUS_LOGIN_URL,
    GOODWE_SEMS_PLUS_USER_AGENT,
)
from goodwe_connector.goodwe_logger.goodwe_api_logger import GoodweApiLogger
from goodwe_connector.http import RequestsHttpClient


class GoodweApiAuth:
    def __init__(
        self,
        system_id: str,
        account: str,
        password: str,
        logging: bool = False,
        http_client=None,
    ) -> None:
        self.system_id = system_id
        self.account = account
        self.password = password
        self.base_url = GOODWE_SEMS_PLUS_API_URL
        self._credentials = ""

        self._logger = GoodweApiLogger(isLogging=logging)
        self._http_client = http_client or RequestsHttpClient()

    @staticmethod
    def _signature(token: dict) -> str:
        timestamp = round(time.time() * 1000)
        digest = hashlib.sha256(
            f"{timestamp}@{token.get('uid', '')}@{token.get('token', '')}".encode()
        ).hexdigest()
        return base64.b64encode(f"{digest}@{timestamp}".encode()).decode()

    @staticmethod
    def _encode_password(password: str) -> str:
        password_hash = hashlib.md5(
            password.encode(), usedforsecurity=False
        ).hexdigest()
        return base64.b64encode(password_hash.encode()).decode()

    def _request_headers(self, token: dict) -> dict:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://semsplus.goodwe.com",
            "Referer": "https://semsplus.goodwe.com/",
            "User-Agent": GOODWE_SEMS_PLUS_USER_AGENT,
            "Token": json.dumps(token, separators=(",", ":")),
            "X-Signature": self._signature(token),
        }

    def _authorization(self) -> bool:
        login_token = {
            "uid": "",
            "timestamp": 0,
            "token": "",
            "client": "semsPlusWeb",
            "version": "",
            "language": "en",
        }
        login_payload = {
            "account": self.account,
            "pwd": self._encode_password(self.password),
            "agreement": 1,
            "isChinese": False,
            "isLocal": False,
        }

        try:
            response = self._http_client.post(
                GOODWE_SEMS_PLUS_LOGIN_URL,
                payload=login_payload,
                headers=self._request_headers(login_token),
                timeout=10,
                json_body=True,
            )
            try:
                response.raise_for_status()
                self._logger.info(
                    f"Login request elapsed seconds: {response.elapsed}"
                )
                body = response.json()
            finally:
                response.close()
        except RequestException as error:
            self._logger.warning(f"{error}")
            return False
        except JSONDecodeError as error:
            self._logger.warning(f"{error}")
            return False

        if not isinstance(body, dict):
            self._logger.warning("SEMS+ login returned an unexpected response.")
            return False

        if str(body.get("code")) not in {"0", "00000"}:
            self._logger.warning(
                "SEMS+ login rejected (code=%s): %s",
                body.get("code"),
                body.get("msg"),
            )
            return False

        credentials = body.get("data")
        if not isinstance(credentials, dict) or not credentials.get("token"):
            self._logger.warning("SEMS+ login response did not contain a token.")
            return False

        api_url = body.get("api") or credentials.get("api")
        self.base_url = (
            api_url.rstrip("/")
            if isinstance(api_url, str) and api_url.startswith("https://")
            else GOODWE_SEMS_PLUS_API_URL
        )
        self._credentials = json.dumps(credentials, separators=(",", ":"))
        return True
