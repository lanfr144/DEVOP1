#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# WSL Setup & Installation Guide - Project Antigravity (DEVOP1)

This guide provides step-by-step instructions for deploying the containerized development infrastructure inside a brand-new WSL (Windows Subsystem for Linux) distribution.

---

## 🛠️ Step 1: Install and Initialize a New WSL Distribution

1. **Open PowerShell as Administrator** on your Windows host.
2. **Install a new Ubuntu distribution** (Ubuntu 22.04 LTS is highly recommended):
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```
3. **Initialize the OS**:
   - Set up your username and password when prompted by the new terminal.
4. **Update System Packages**:
   Inside the WSL environment, execute:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3 python3-pip git curl
   ```

---

## 🐳 Step 2: Install Docker Engine on WSL

We install Docker Engine directly on the WSL distribution to manage containers without Docker Desktop constraints.

1. **Remove old versions (if any)**:
   ```bash
   sudo apt remove docker docker-engine docker.io containerd runc -y
   ```
2. **Install prerequisite libraries**:
   ```bash
   sudo apt install -y apt-transport-https ca-certificates gnupg lsb-release
   ```
3. **Add Docker’s official GPG key**:
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```
4. **Set up the stable repository**:
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
5. **Install Docker Engine and Docker Compose Plugin**:
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```
6. **Configure non-root user permissions**:
   To run docker commands without prefixing `sudo`, add your user to the `docker` group:
   ```bash
   sudo usermod -aG docker $USER
   ```
   *Note: Close and reopen your WSL terminal to apply the group membership changes.*
7. **Start the Docker daemon**:
   ```bash
   sudo service docker start
   ```

---

## 🔀 Step 3: Clone Repository and Configure Git Filters

1. **Clone the repository** into your home folder inside WSL:
   ```bash
   git clone https://github.com/lanfr144/DEVOP1.git ~/DEVOP1
   cd ~/DEVOP1
   ```
2. **Run the Git Filter Setup Script**:
   WSL uses the Unix setup script. Mark it executable and run it to set up the clean/smudge metadata expansion rules:
   ```bash
   chmod +x local_tools/setup_filters.sh
   ./local_tools/setup_filters.sh
   ```
   This registers the `ident-dynamic` clean and smudge filters using the absolute path script.

---

## ⚙️ Step 4: Environment and Port Configuration

1. **Generate the Environment File**:
   Copy the example template to create your active `.env`:
   ```bash
   cp .env.example .env
   ```
2. **Run Port Offset Verification**:
   To ensure that default ports do not conflict with active services on your Windows host, run the validation tool:
   ```bash
   python3 local_tools/apply_port_offset.py
   ```
   This reads your `PORT_OFFSET` (configured in `.env`), calculates the mapped port offsets, tests if they are free on your loopback network, and updates the `.env` dynamically.

---

## 🚀 Step 5: Launch the Application Stack

1. **Build and start all containerized services** (MySQL, Flask Backend, Apache Airflow, Zabbix Server/Web):
   ```bash
   docker compose up -d --build
   ```
2. **Verify container execution status**:
   ```bash
   docker compose ps
   ```

---

## 📊 Step 6: Verify Accessible Services

Once the stack is running, you can access the applications on the host Windows browser (since WSL maps ports directly to the local host):

* **Web Backend API**: `http://localhost:6000` (Version & Git ID meta info)
* **Apache Airflow Dashboard**: `http://localhost:9080` (Credentials: `admin`/`admin`)
* **Zabbix Web UI**: `http://localhost:9081` (Credentials: `Admin`/`zabbix`)
* **MySQL Database Service**: Host `127.0.0.1`, Port `4306` (Credentials from `.env`)
