import argparse
import datetime
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import requests

from zoho.exceptions import ZohoHTTPError
from zoho.settings import settings
from zoho.utils import now


class OAuth2Token:
    access_token: str
    expires: datetime.datetime
    token_type: str

    def __init__(self, token: dict):
        self.access_token = token["access_token"]
        self.token_type = token["token_type"]
        self.expires = now() + datetime.timedelta(seconds=token["expires_in"])


class ZohoOAuth2Token(OAuth2Token):
    api_domain: str
    refresh_token: str

    def __init__(self, token: dict, refresh_token: str | None = None):
        super().__init__(token=token)
        self.api_domain = token["api_domain"]
        self.refresh_token = refresh_token or token["refresh_token"]


class AuthCallbackHandler(BaseHTTPRequestHandler):
    def write_response(self, encoding: str, content: str):
        encoded = content.encode(encoding, "surrogateescape")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", f"text/html; charset={encoding}")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def html_template(self, encoding: str, content: str):
        return f"""
<!DOCTYPE HTML>
<html lang="en">
<head>
    <meta charset="{encoding}">
</head>
<body style="font-size:20px;line-height:1.5em">
    <div style="max-width:1024px;margin:auto;">
        {content}
    </div>
</body>
</html>
"""

    def on_success(self, encoding: str, refresh_token: str):
        settings.refresh_token = refresh_token
        print(f"Your refresh token: {refresh_token}")
        print(
            "Make sure zoho.settings.refresh_token is set to this value, e.g. by defining the ZOHO_REFRESH_TOKEN "
            "environment variable."
        )
        content = f"""
            <p>Your refresh token:</p>
            <pre>{refresh_token}</pre>
            <p>
                Make sure <code>zoho.settings.refresh_token</code> is set to this value, e.g. by defining the
                <code>ZOHO_REFRESH_TOKEN</code> environment variable.
            </p>
            <p>You may close the browser tab.</p>
        """
        response = self.html_template(encoding=encoding, content=content)
        self.write_response(encoding, response)

    def on_error(self, encoding: str, error: str):
        content = (
            f"<p>Auth server returned error: <strong>{error}</strong>.</p>"
            "<p>You may close the browser tab.</p>"
        )
        response = self.html_template(encoding, content)
        self.write_response(encoding, response)

    def do_GET(self):
        encoding = sys.getfilesystemencoding()
        parsed_url = urlparse(self.path)
        qs = parse_qs(parsed_url.query)
        if "code" in qs:
            auth_code = qs["code"][0]
            token = get_oauth2_token_from_auth_code(auth_code)
            self.on_success(encoding, token.refresh_token)
        elif "error" in qs:
            self.on_error(encoding, qs["error"][0])


def get_oauth2_token_interactive():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", help="(optional) Will be used to set zoho.settings.client_id")
    parser.add_argument("--client-secret", help="(optional) Will be used to set zoho.settings.client_secret")
    args = parser.parse_args()

    if args.client_id is not None:
        settings.client_id = args.client_id
    if args.client_secret is not None:
        settings.client_secret = args.client_secret

    if not settings.client_id or not settings.client_secret:
        print("zoho.settings.client_id and zoho.settings.client_secret must both be set to non-empty strings.")
        sys.exit(1)

    webserver_address = f"http://{settings.local_webserver_host}:{settings.local_webserver_port}/"

    params = {
        "scope": ",".join(settings.scope),
        "client_id": settings.client_id,
        "response_type": "code",
        "access_type": "offline",
        "redirect_uri": webserver_address,
    }
    webbrowser.open_new_tab(f"{settings.auth_url}?{urlencode(params)}")

    print(f"Booting up a local web server on {webserver_address}. Press Ctrl+C to cancel.")
    with HTTPServer((settings.local_webserver_host, settings.local_webserver_port), AuthCallbackHandler) as httpd:
        httpd.timeout = 600
        httpd.handle_request()


def get_oauth2_token_from_refresh_token(refresh_token: str):
    params = {
        "refresh_token": refresh_token,
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "grant_type": "refresh_token",
    }
    response = requests.post(url=f"{settings.token_url}?{urlencode(params)}", timeout=10)
    ZohoHTTPError.raise_for_status(response)
    return ZohoOAuth2Token(response.json(), refresh_token=refresh_token)


def get_oauth2_token_from_auth_code(auth_code: str):
    response = requests.post(
        url=settings.token_url,
        data={
            "grant_type": "authorization_code",
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "redirect_uri": f"http://{settings.local_webserver_host}:{settings.local_webserver_port}/",
            "code": auth_code,
        },
        timeout=10,
    )
    ZohoHTTPError.raise_for_status(response)
    token = ZohoOAuth2Token(response.json())
    settings.refresh_token = token.refresh_token
    return token
