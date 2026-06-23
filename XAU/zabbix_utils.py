#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import socket
import struct
import json
import os
import sys
from dotenv import load_dotenv

# Load env variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def send_to_zabbix(key, value, host_name="xau-app"):
    """
    Sends a metric value to Zabbix Server using raw TCP Zabbix Sender Protocol.
    """
    # Check if network mode is local
    network_mode = os.getenv("NETWORK_MODE", "server")
    if network_mode.lower() == "local":
        sys.stdout.write(f"NETWORK_MODE is local. Bypassing Zabbix notification for {key}: {value}\n")
        return None

    # Read configuration from environment or use defaults
    zabbix_server = os.getenv("ZBX_SERVER_HOST") or os.getenv("ZABBIX_SERVER") or "zabbix-server"
    zabbix_port = 10051
    
    try:
        # Construct Zabbix Sender JSON data
        payload_data = {
            "request": "sender data",
            "data": [
                {
                    "host": host_name,
                    "key": key,
                    "value": str(value)
                }
            ]
        }
        payload = json.dumps(payload_data).encode('utf-8')
        
        # Build packet: header + length + payload
        header = b'ZBXD\x01'
        data_len = struct.pack('<Q', len(payload))
        packet = header + data_len + payload
        
        # Connect and send
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0)
        s.connect((zabbix_server, zabbix_port))
        s.sendall(packet)
        response = s.recv(1024)
        s.close()
        return response
    except Exception as e:
        sys.stderr.write(f"Zabbix notification failed: {e}\n")
        return None
