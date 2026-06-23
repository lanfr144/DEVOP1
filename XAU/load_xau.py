#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import json
import mysql.connector
import sys
import re
import os
import glob
from datetime import datetime
import pandas as pd
from io import StringIO
import inspect
from dotenv import load_dotenv

# Try to load env variables from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import Zabbix utility
try:
    from zabbix_utils import send_to_zabbix
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from zabbix_utils import send_to_zabbix

# What is the biggest variation for the price which is realistic ?
VARIATION_MAXIMAL = .12

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def load_data(filename):
    # Filename validation: "metaux-precieux_" + yyyymmdd + "_" + hh24miss + ".json"
    pattern = r"^metaux-precieux_(\d{8})_\d{6}\.json$"
    base_name = os.path.basename(filename)
    match = re.match(pattern, base_name)
    
    if not match:
        error_msg = f"{filename}:{lineno()}: Error: Filename {base_name} does not match format metaux-precieux_yyyymmdd_hh24miss.json"
        sys.stderr.write(error_msg + "\n")
        send_to_zabbix("xau.error", error_msg)
        return 1

    extracted_date = match.group(1) # Extracts yyyymmdd

    # Load database credentials from env variables
    host = os.getenv("DATABASE_HOST") or os.getenv("XAU_DB_HOST") or "localhost"
    port = int(os.getenv("MYSQL_PORT") or 3306) if host in ["localhost", "127.0.0.1"] else 3306
    user = os.getenv("XAU_DB_USER") or os.getenv("DB_USER") or "xau"
    password = os.getenv("XAU_DB_PASSWORD") or os.getenv("DB_PASSWORD") or "your_windows_user_here"
    database = os.getenv("XAU_DB_NAME") or os.getenv("DB_NAME") or "xau"

    conn = None
    try:
        # Load and Parse JSON Data
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
            # Extract precious metal datasets
            datasets = content['data']['datasets']
            
            # Keep a human readable trace.
            df = pd.read_json(StringIO(json.dumps(datasets, indent=4)))
            
            # Remove unused information.
            df = df.drop(columns=['issuer','sys_language_uid','l10n_parent','additional_info','deliverable'], errors='ignore')
            df.to_csv(filename.replace(".json", ".csv"), encoding='utf-8', index=False)
            
            # Check data price and weight ratios
            df['ratioPrice'] = df['price_bcee_buy'] / df['price_bcee_sell']
            df['ratioWeight'] = df['weight_brut'] / df['weight_net']
            
            # Validation rules:
            # Check if ratio between price buy and price sell is between (1.01, 1.20)
            # Check if ratio between weight brut and net is between (1.00, 1.091)
            invalid_mask = (~df['ratioPrice'].between(1.01, 1.20)) | (~df['ratioWeight'].between(1.00, 1.091))
            invalid_rows = df[invalid_mask]
            
            if not invalid_rows.empty:
                error_msg = f"{filename}:{lineno()}: Error: {invalid_rows.shape[0]} invalid variation rows found during validation rules."
                sys.stderr.write(error_msg + "\n")
                invalid_rows.to_csv(filename.replace(".json", ".err"), encoding='utf-8', index=True)
                send_to_zabbix("xau.error", error_msg)
                return 1

        # Connect to MySQL
        conn = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            autocommit=False  # Ensure manual control over transactions
        )
        
        cursor = conn.cursor()
        nbr_errors = 0 
        
        for item in datasets:
            # Insert Data
            query = """
insert into Rate(pkfk_uid,pk_dt,priceBceeBuy,priceBceeSell)
select uid, %s, %s, %s
from Xau
where uid = %s and
codeBcee = %s and
name = %s and
form = %s and
purity = %s and
weightNet = %s and
weightBrut = %s
and ( image = %s or image is null )
and not exists ( select 1
from Rate
where pkfk_uid = Xau.uid
and pk_dt = %s )"""
            
            data_tuple = (
                extracted_date,
                float(item.get('price_bcee_buy', 0)),
                float(item.get('price_bcee_sell', 0)),
                item.get('uid'),
                item.get('code_bcee'),
                item.get('name'),
                item.get('form'),
                item.get('purity'),
                float(item.get('weight_net', 0)),
                float(item.get('weight_brut', 0)),
                str(item.get('image')) if item.get('image') != 0 else None,
                extracted_date
            )
                        
            cursor.execute(query, data_tuple)
            count = cursor.rowcount
            
            # Update if price changed!
            query = """
update Rate 
set priceBceeBuy = %s ,priceBceeSell = %s
where pkfk_uid = %s
and pk_dt = %s
and ( priceBceeBuy != %s or priceBceeSell != %s )
"""
            
            data_tuple = (
                float(item.get('price_bcee_buy', 0)),
                float(item.get('price_bcee_sell', 0)),
                item.get('uid'),
                extracted_date,
                float(item.get('price_bcee_buy', 0)),
                float(item.get('price_bcee_sell', 0))
            )

            cursor.execute(query, data_tuple)
            count += cursor.rowcount
            if count != 1 :
                nbr_errors += 1 
                sys.stderr.write(f"{filename}:{lineno()}: Row mismatch count={count} for pkfk_uid={item.get('uid')}\n")

        # Verify values loaded
        for item in datasets:
            query = """
select count(1) nb
from Rate
where pkfk_uid = %s
and pk_dt = %s
and priceBceeBuy = %s
and priceBceeSell = %s
"""
            
            data_tuple = (
                item.get('uid'),
                extracted_date,
                float(item.get('price_bcee_buy', 0)),
                float(item.get('price_bcee_sell', 0))
            )

            cursor.execute(query, data_tuple)
            result = cursor.fetchone()

            if result[0] != 1 :
                nbr_errors += 1 
                sys.stderr.write(f"{filename}:{lineno()}: Verification row not found or duplicate: {result[0]} rows for pkfk_uid={item.get('uid')}\n")

        # Check variation limit compared to previous day
        query = f"""
select count(1) nb
from Rate e, Rate i
where e.pk_dt = %s
and i.pkfk_uid = e.pkfk_uid
and i.pk_dt = DATE_ADD(e.pk_dt, INTERVAL -1 DAY)
and ((i.priceBceeBuy  not between e.priceBceeBuy  * (1-{VARIATION_MAXIMAL}) and e.priceBceeBuy  * (1+{VARIATION_MAXIMAL}))
 or ( i.priceBceeSell not between e.priceBceeSell * (1-{VARIATION_MAXIMAL}) and e.priceBceeSell * (1+{VARIATION_MAXIMAL})))"""

        cursor.execute(query, (extracted_date,))
        result = cursor.fetchone()

        if result[0] > 0:
            nbr_errors += result[0]
            sys.stderr.write(f"{filename}:{lineno()}: Error: {result[0]} rows exceeded the maximum variation of {VARIATION_MAXIMAL*100}%\n")
            
        if nbr_errors > 0 :
            conn.rollback()
            error_msg = f"load_xau failed: {nbr_errors} errors occurred during loading/validation of {base_name}."
            send_to_zabbix("xau.error", error_msg)
            return 1
        else :
            conn.commit()
            print(f"Data successfully loaded from {base_name} to database.")
            send_to_zabbix("xau.trace", f"load_xau succeeded: {base_name} loaded into database.")
            return 0

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = exc_tb.tb_frame.f_code.co_filename
        if conn:
            conn.rollback()
        error_msg = f"load_xau exception for {base_name}: {str(e)} in {fname} at line {exc_tb.tb_lineno}"
        sys.stderr.write(error_msg + "\n")
        send_to_zabbix("xau.error", error_msg)
        return 1
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Auto-detect latest JSON file in XAU folder
        dir_path = os.path.dirname(os.path.abspath(__file__))
        files = glob.glob(os.path.join(dir_path, "metaux-precieux_*.json"))
        if not files:
            sys.stderr.write("Usage: python load_xau.py <filename>\nOr place metaux-precieux_*.json files in the script directory.\n")
            send_to_zabbix("xau.error", "load_xau failed: No metaux-precieux_*.json files found.")
            sys.exit(1)
        files.sort()
        target_file = files[-1]
        print(f"Auto-detected latest JSON file: {os.path.basename(target_file)}")
    else:
        target_file = sys.argv[1]
    
    exit_code = load_data(target_file)
    sys.exit(exit_code)