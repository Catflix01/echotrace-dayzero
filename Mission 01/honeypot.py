import datetime
import socket
import logging
import json

# Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 2222       # Fake SSH port
LOGFILE = 'honeypot.log'

# Setup logging
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log_echo_trace(addr, username, password):
    echo_data = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        "source_ip": addr[0],
        "username": username.decode(),
        "password": password.decode(),
        "confidence": "LOW",
        "protocol": "HONEYPOT_PORT22"
    }
    with open("honeypot_logs.json", "a") as json_file:
        json.dump(echo_data, json_file)
        json_file.write("\n")

def send_to_webhook(addr, username, password):
    # This function can be implemented to send logs to Discord, Notion, etc.
    pass

def start_honeypot():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[EchoTrace Honeypot] Listening on port {PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[!] Connection from {addr}")
                # logging.info(f"[ECHO DETECTED]")
                # logging.info(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
                # logging.info(f"Source IP: {addr[0]}")
                # EchoTrace-themed welcome banner
                conn.sendall(b'EchoTrace | Port22_ShellBait\n')
                conn.sendall(b'Username: ')
                username = conn.recv(1024).strip()
                conn.sendall(b'Password: ')
                password = conn.recv(1024).strip()
                # logging.info(f"Username: {username.decode()}")
                # logging.info(f"Password: {password.decode()}")
                # logging.info("Confidence: LOW")
                # logging.info("Protocol: HONEYPOT_PORT22")
                log_echo_trace(addr, username, password)
                conn.sendall(b'Access denied.\n')
                conn.close()

if __name__ == "__main__":
    try:
        start_honeypot()
    except KeyboardInterrupt:
        print("\n[!] Shutting down honeypot.")