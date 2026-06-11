#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import socket
import sys

# -----------------------------------------------------------------------------
# STEP 1: CONFIGURATION OF DEFAULT SERVICES PORTS
# -----------------------------------------------------------------------------
# These are the default base port numbers for all system services.
# When a port offset is applied, it will be added to these base values.
DEFAULT_PORTS = {
    "BACKEND_PORT": 5000,
    "MYSQL_PORT": 3306,
    "AIRFLOW_PORT": 8080,
    "ZABBIX_PORT": 8081,
    "JENKINS_PORT": 8088
}

# -----------------------------------------------------------------------------
# STEP 2: PORT AVAILABILITY CHECKER
# -----------------------------------------------------------------------------
def is_port_in_use(port):
    """Attempts to bind to a port on localhost to check if it's currently occupied."""
    # socket.AF_INET specifies IPv4 address family.
    # socket.SOCK_STREAM specifies TCP protocol.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0) # Set a 1-second timeout for the connection attempt
        # connect_ex returns 0 if the connection succeeded (port is occupied/in use).
        # It returns an error code if the connection failed (meaning port is free).
        return s.connect_ex(('127.0.0.1', port)) == 0

# -----------------------------------------------------------------------------
# STEP 3: ENV FILE PARSING UTILITY
# -----------------------------------------------------------------------------
def load_env(env_path):
    """Reads a .env file and loads its key-value pairs into a Python dictionary."""
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignore comment lines and lines without assignments
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

# -----------------------------------------------------------------------------
# STEP 4: ENV FILE WRITER / IN-PLACE UPDATER
# -----------------------------------------------------------------------------
def write_env(env_path, updates):
    """Idempotently updates or appends environment variables inside the .env file."""
    # If the file does not exist, create it and write the updates
    if not os.path.exists(env_path):
        with open(env_path, 'w', encoding='utf-8') as f:
            for k, v in updates.items():
                f.write(f"{k}={v}\n")
        return

    # Read existing lines from the .env file to preserve structure and comments
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_keys = set()
    new_lines = []
    
    # Process existing lines, replacing variables when matched
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            key, _ = stripped.split('=', 1)
            key = key.strip()
            if key in updates:
                # Replace the old value with the new update
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    # Append any new keys that were not originally in the .env file
    for k, v in updates.items():
        if k not in updated_keys:
            new_lines.append(f"{k}={updates[k]}\n")

    # Write the updated content back to the .env file
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# -----------------------------------------------------------------------------
# STEP 5: MAIN EXECUTION LOGIC
# -----------------------------------------------------------------------------
def main():
    # Resolve the repository root directory relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    
    if not os.path.exists(env_path):
        print(f"[ERROR] .env file not found at {env_path}")
        sys.exit(1)
        
    # Load environment configuration variables
    env_vars = load_env(env_path)
    
    # Fetch the port offset number (default to 0 if not present)
    offset_str = env_vars.get("PORT_OFFSET", "0")
    try:
        offset = int(offset_str)
    except ValueError:
        print(f"[ERROR] PORT_OFFSET in .env is not a valid integer: '{offset_str}'")
        sys.exit(1)
        
    print(f"[INFO] Using PORT_OFFSET={offset} loaded from .env")
    
    # Calculate target ports and verify they are free
    calculated_ports = {}
    in_use_ports = []
    
    for name, default_port in DEFAULT_PORTS.items():
        # Add the offset to calculate the final port
        target_port = default_port + offset
        calculated_ports[name] = target_port
        
        print(f"Checking target port {name}: {target_port} ... ", end="")
        sys.stdout.flush()
        
        # Verify port availability
        if is_port_in_use(target_port):
            print("IN USE")
            in_use_ports.append((name, target_port))
        else:
            print("FREE")
            
    # Exit if any port conflicts were found
    if in_use_ports:
        print("\n[ERROR] The following calculated ports are already in use on the host:")
        for name, port in in_use_ports:
            print(f"  - {name}: {port}")
        print("Please resolve the conflict or change PORT_OFFSET in .env before proceeding.")
        sys.exit(1)
        
    # Persist the calculated ports in the .env file
    updates = {name: str(port) for name, port in calculated_ports.items()}
    write_env(env_path, updates)
    print("\n[SUCCESS] Successfully verified and updated .env with offsetted ports:")
    for name, port in calculated_ports.items():
        print(f"  - {name}: {port}")

if __name__ == "__main__":
    main()