import os
from typing import Self

import dotenv


class Settings:
    _instance: Self
    _initialized: bool = False

    auth_code: str | None
    auth_url: str
    client_id: str | None
    client_secret: str | None
    list_limit: int
    # Only used for the callback URL on interactive authentication:
    local_webserver_host: str
    local_webserver_port: int
    refresh_token: str | None
    scope: list[str]
    timezone: str
    token_url: str

    def __new__(cls):
        # Forced singleton:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.auth_code = os.environ.get("ZOHO_AUTH_CODE", None)
            self.auth_url = os.environ.get("ZOHO_AUTH_URL", "https://accounts.zoho.com/oauth/v2/auth")
            self.client_id = os.environ.get("ZOHO_CLIENT_ID", None)
            self.client_secret = os.environ.get("ZOHO_CLIENT_SECRET", None)
            self.list_limit = 200
            self.local_webserver_host = os.environ.get("ZOHO_LOCAL_WEBSERVER_HOST", "127.0.0.1")
            self.local_webserver_port = int(os.environ.get("ZOHO_LOCAL_WEBSERVER_PORT", "8888"))
            self.refresh_token = os.environ.get("ZOHO_REFRESH_TOKEN", None)
            self.scope = [
                "ZohoCRM.modules.ALL",
                "ZohoCRM.settings.ALL",
                "ZohoCRM.coql.READ",
                "ZohoCRM.users.ALL",
                "ZohoCRM.org.ALL",
            ]
            self.timezone = os.environ.get("ZOHO_TIMEZONE", "UTC")
            self.token_url = os.environ.get("ZOHO_TOKEN_URL", "https://accounts.zoho.eu/oauth/v2/token")
            self._initialized = True


def find_dotenv():
    # pylint: disable=protected-access
    for dirname in dotenv.main._walk_to_root(__file__):
        check_path = os.path.join(dirname, ".env")
        if os.path.isfile(check_path):
            return check_path
    return None


# Very important to do them in this order:
dotenv.load_dotenv(find_dotenv())
settings = Settings()
