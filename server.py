import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}/index.html")

if __name__ == "__main__":
    # Run server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        # Open web browser automatically in a separate thread
        threading.Thread(target=open_browser, daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.server_close()
