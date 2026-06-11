--ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

-- =============================================================================
-- MySQL Initialization Script: Database Provisioning & Security Setup
-- =============================================================================
-- This script runs automatically during the database container's initial startup.
-- It creates core databases and assigns permission privileges to dedicated users.
-- =============================================================================

-- 1. Create the databases
-- devop1_db: The main backend application database
CREATE DATABASE IF NOT EXISTS devop1_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- airflow_db: Metadata storage for the Apache Airflow orchestrator stack
CREATE DATABASE IF NOT EXISTS airflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- zabbix: Database used by the Zabbix telemetry server
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- 2. Create dev_user and grant full access to devop1_db and airflow_db
-- 'dev_user'@'%' can connect from any network host (IP wildcard '%')
CREATE USER IF NOT EXISTS 'dev_user'@'%' IDENTIFIED BY 'your_db_password_here';
GRANT ALL PRIVILEGES ON devop1_db.* TO 'dev_user'@'%';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'dev_user'@'%';

-- 3. Create dedicated airflow user and grant privileges to airflow_db
CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow'@'%';

-- 4. Create dedicated zabbix user and grant privileges to zabbix database
CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY 'your_db_password_here';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%';

-- 5. Reload privileges table in MySQL to apply the new access permissions immediately
FLUSH PRIVILEGES;