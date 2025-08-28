#!/usr/bin/env python3
"""
Simple OAuth callback server for Open Banking authorization.
Runs on port 8765 to catch the OAuth callback and display the authorization code.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests to the callback URL."""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        auth_code = query_params.get("code", [None])[0]
        state = query_params.get("state", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if auth_code:
            html_content = self.generate_success_page(auth_code, state)
        else:
            html_content = self.generate_error_page()

        self.wfile.write(html_content.encode("utf-8"))

    def generate_success_page(self, auth_code, state):
        """Generate HTML page showing the authorization code."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OAuth Authorization Success</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .success-icon {{
            color: #28a745;
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #28a745;
            text-align: center;
            margin-bottom: 30px;
        }}
        .code-box {{
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            word-break: break-all;
            position: relative;
        }}
        .copy-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }}
        .copy-btn:hover {{
            background: #0056b3;
        }}
        .info {{
            background: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .timestamp {{
            color: #6c757d;
            font-size: 12px;
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✅</div>
        <h1>OAuth Authorization Successful!</h1>
        
        <div class="info">
            <strong>Authorization completed successfully!</strong><br>
            You can now copy the authorization code below and use it in your application.
        </div>
        
        <h3>Authorization Code:</h3>
        <div class="code-box" id="authCode">
            {auth_code}
        </div>
        
        <button class="copy-btn" onclick="copyToClipboard()">Copy Code</button>
        
        <div class="info">
            <strong>State:</strong> {state or "None"}<br>
            <strong>Timestamp:</strong> {timestamp}
        </div>
        
        <div class="timestamp">
            This page will remain open. You can close it after copying the code.
        </div>
    </div>

    <script>
        function copyToClipboard() {{
            const codeElement = document.getElementById('authCode');
            const text = codeElement.textContent;
            
            navigator.clipboard.writeText(text).then(function() {{
                const btn = document.querySelector('.copy-btn');
                btn.textContent = 'Copied!';
                btn.style.background = '#28a745';
                
                setTimeout(function() {{
                    btn.textContent = 'Copy Code';
                    btn.style.background = '#007bff';
                }}, 2000);
            }}).catch(function(err) {{
                console.error('Could not copy text: ', err);
                alert('Failed to copy code. Please copy it manually.');
            }});
        }}
    </script>
</body>
</html>
        """

    def generate_error_page(self):
        """Generate HTML page for errors."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OAuth Authorization Error</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .error-icon {
            color: #dc3545;
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
        }
        h1 {
            color: #dc3545;
            text-align: center;
        }
        .error-box {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">❌</div>
        <h1>OAuth Authorization Error</h1>
        
        <div class="error-box">
            <strong>Error:</strong> No authorization code received.<br>
            Please try the authorization process again.
        </div>
        
        <p>If you continue to have issues, please check:</p>
        <ul>
            <li>That you completed the authorization on the bank's website</li>
            <li>That you were redirected back to this callback URL</li>
            <li>That the authorization process completed successfully</li>
        </ul>
    </div>
</body>
</html>
        """

    def log_message(self, format, *args):
        """Custom logging to show callback details."""
        if "code=" in self.path:
            print(f"🔐 OAuth callback received: {self.path}")
        else:
            print(f"📡 Request received: {self.path}")


def run_server(port=8765):
    """Run the OAuth callback server."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)

    print(f"🚀 OAuth callback server starting on port {port}")
    print(f"📍 Callback URL: http://127.0.0.1:{port}/callback")
    print("⏳ Waiting for OAuth callback...")
    print(
        "💡 Complete the authorization in your browser, then return here to get the code"
    )
    print("🛑 Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()


if __name__ == "__main__":
    run_server()

# http://127.0.0.1:8765/callback?state=demo-state&code=eaafacf6-efb5-483d-a073-3743b8ac606b
