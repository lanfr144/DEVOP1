--ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
CREATE DATABASE IF NOT EXISTS devop1_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS airflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

CREATE USER IF NOT EXISTS 'dev_user'@'%' IDENTIFIED BY 'your_db_password_here';
GRANT ALL PRIVILEGES ON devop1_db.* TO 'dev_user'@'%';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'dev_user'@'%';

CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow'@'%';

CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY 'your_db_password_here';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%';

FLUSH PRIVILEGES;