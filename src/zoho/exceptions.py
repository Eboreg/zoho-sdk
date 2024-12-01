import requests


class ZohoHTTPError(Exception):
    code: str | None = None
    message: str | None = None

    def __init__(self, response: requests.Response):
        self.response = response
        super().__init__(f"[{response.status_code}]: {response.text.strip()} (url: {response.url})")
        try:
            self.code = response.json()["data"][0]["code"]
        except Exception:
            self.code = None
        try:
            self.message = response.json()["data"][0]["message"]
        except Exception:
            self.message = None

    def json(self):
        try:
            return self.response.json()
        except Exception:
            return None

    @classmethod
    def raise_for_status(cls, response: requests.Response):
        """
        A little more helpful error messages than the ones we get from
        requests.Response.raise_for_status(), plus a never-failing json()
        method on the exception.
        """
        if response.status_code >= 400:
            raise cls(response=response)
