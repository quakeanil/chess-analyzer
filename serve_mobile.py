"""
Lightweight Mobile Server for Chess Analyzer Dashboard
Run this script to access your dashboard from your Xiaomi 17 Ultra or any smartphone on your local WiFi!
"""
import http.server
import socket
import socketserver
import os
import sys

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def run_server(port=8080):
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}/dashboard.html"
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 65)
    print("📱 CHESS ANALYZER - MOBILE ACCESS FOR XIAOMI 17 ULTRA")
    print("=" * 65)
    print(f"\n[+] Server running on your local Wi-Fi network!")
    print(f"[+] Open this link in Chrome/Browser on your Xiaomi phone:\n")
    print(f"    👉  \033[1;32m{url}\033[0m\n")
    print("=" * 65)
    print("[*] Note: Make sure your phone is connected to the same Wi-Fi network.")
    print("[*] Press Ctrl+C in this window anytime to stop the server.")
    print("=" * 65)
    
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[+] Mobile server stopped.")

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
