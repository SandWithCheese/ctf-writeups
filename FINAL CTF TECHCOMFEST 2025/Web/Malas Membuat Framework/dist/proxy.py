import os
from mitmproxy import http
from urllib.parse import unquote
import socket

def request(flow: http.HTTPFlow) -> None:
    ...
def strict_csp(flow: http.HTTPFlow):
    flow.response.headers["Content-Security-Policy"] = "default-src 'none';"
    flow.response.headers["X-Content-Type-Options"] = "nosniff"
    flow.response.headers["X-Frame-Options"] = "DENY"
    flow.response.headers["X-XSS-Protection"] = "1; mode=block"
    flow.response.headers["Referrer-Policy"] = "no-referrer"
    flow.response.headers["Feature-Policy"] = "geolocation 'none'; microphone 'none'; camera 'none';"
    flow.response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    flow.response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    flow.response.headers["Cross-Origin-Resource-Policy"] = "same-site"

def response(flow: http.HTTPFlow) -> None:
    # 1 solusi tiupkan ke probset, probset gelisah ingin segera ngasih hint... https://web.facebook.com/share/p/18q6UNLLEP/
    if len(flow.request.pretty_url) > 1500:
        flow.kill()
        return
    if 'admin' in unquote(flow.request.pretty_url):
        bot_domain = "bot"
        try:
            bot_ip = socket.gethostbyname(bot_domain)
        except socket.gaierror:
            print(f"Failed to resolve domain: {bot_domain}")
            flow.kill()
            return

        print(f"Bot IP: {bot_ip}")

        if flow.client_conn.address[0] != bot_ip:
            flow.kill()
            return
        if flow.request.cookies.get("secret") != os.environ['SECRET']:
            flow.kill()
            return

    if flow.response.status_code > 200:
        flow.response.text = "Blocked by mitmproxy"
        flow.response.status_code = 403
        strict_csp(flow)
    else:
        strict_csp(flow)
        flow.response.headers["Content-Security-Policy"] = "default-src 'none'; style-src 'self' 'unsafe-inline'; script-src 'unsafe-inline';"
