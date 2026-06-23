#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
import os
from dotenv import load_dotenv

# --- 1. DATABASE UTILITIES ---

def get_db_config():
    """Reads database credentials from environment variables / .env"""
    # Load env variables from root workspace and local directory
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    
    config = {
        'host': os.getenv("XAU_DB_HOST") or os.getenv("DATABASE_HOST") or "localhost",
        'user': os.getenv("XAU_DB_USER") or os.getenv("DB_USER") or "xau",
        'password': os.getenv("XAU_DB_PASSWORD") or os.getenv("DB_PASSWORD") or "lanfr144",
        'database': os.getenv("XAU_DB_NAME") or os.getenv("DB_NAME") or "xau",
        'port': os.getenv("MYSQL_PORT") or "3306"
    }
    return config

def get_connection():
    config = get_db_config()
    if config:
        try:
            host = config['host'].strip('"')
            # Use host port (MYSQL_PORT) if connecting to localhost, otherwise use default internal container port
            port = int(config['port']) if host in ["localhost", "127.0.0.1"] else 3306
            return mysql.connector.connect(
                user=config['user'].strip('"'),
                password=config['password'].strip('"'),
                host=host,
                port=port,
                database=config['database'].strip('"')
            )
        except mysql.connector.Error as err:
            st.error(f"MySQL Connection Error: {err}")
    return None

def run_query(query, params=None, is_select=True):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            if is_select:
                result = cursor.fetchall()
                return pd.DataFrame(result)
            else:
                conn.commit()
                return cursor.rowcount
        except mysql.connector.Error as err:
            st.error(f"Database Error {err.errno}: {err.msg}")
        finally:
            conn.close()
    return None

# --- 2. FORMATTING HELPERS ---

def format_weight_str(val):
    """Format for static display: 1000,000 Grammes"""
    if val is None: return "0,000 Grammes"
    return f"{float(val):.3f}".replace('.', ',') + " Grammes"

# --- 3. DOMAIN SYNC LOGIC ---

DOMAIN_MAP = {
    "uid": ("Uid", "uid"),
    "codeBcee": ("CodeBcee", "codeBcee"),
    "name": ("Name", "name"),
    "form": ("Form", "form"),
    "purity": ("Purity", "purity"),
    "weightNet": ("Weight", "weight"),
    "image": ("Image", "image")
}

def sync_domains_from_df(df):
    for col, (table, db_col) in DOMAIN_MAP.items():
        if col in df.columns:
            unique_vals = df[col].dropna().unique()
            for val in unique_vals:
                check = run_query(f"SELECT `{db_col}` FROM `{table}` WHERE `{db_col}` = %s", (val,))
                if check is not None and check.empty:
                    run_query(f"INSERT INTO `{table}` (`{db_col}`) VALUES (%s)", (val,), is_select=False)

# --- 4. SCREEN FUNCTIONS ---

def screen_dashboard():
    st.title("📈 Gold Price Dashboard")
    
    col1, col2 = st.columns(2)
    start_dt = col1.date_input("Start Date", value=date(2024, 1, 1), key="dash_start")
    end_dt = col2.date_input("End Date", value=date.today(), key="dash_end")

    query = """
    SELECT r.pk_dt, r.priceBceeBuy, r.priceBceeSell, x.name, x.uid 
    FROM Rate r JOIN Xau x ON r.pkfk_uid = x.uid
    WHERE r.pk_dt BETWEEN %s AND %s
    """
    df = run_query(query, (start_dt, end_dt))
    
    if df is not None and not df.empty:
        df['pk_dt'] = pd.to_datetime(df['pk_dt'])
        assets = st.multiselect("Filter Assets", options=df['name'].unique(), default=df['name'].unique()[:1])
        
        if assets:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            for asset in assets:
                sub_df = df[df['name'] == asset].sort_values('pk_dt')
                fig.add_trace(go.Scatter(x=sub_df['pk_dt'], y=sub_df['priceBceeBuy'], name=f"{asset} Buy (€)"), secondary_y=False)
                fig.add_trace(go.Scatter(x=sub_df['pk_dt'], y=sub_df['priceBceeSell'], name=f"{asset} Sell (€)", line=dict(dash='dot')), secondary_y=True)
            
            fig.update_layout(title="Historical Price Trends", hovermode="x unified", legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, width='stretch', config={'displaylogo': False})
    else:
        st.info("No data found for the selected date range.")

def screen_xau_management():
    st.title("🟡 Xau Assets Catalog")
    
    df = run_query("SELECT * FROM Xau")
    if df is not None:
        df['preview'] = df['image']
        
        edited_df = st.data_editor(
            df, 
            num_rows="dynamic", 
            width='stretch', 
            hide_index=True,
            column_config={
                "preview": st.column_config.ImageColumn("Preview"),
                "image": st.column_config.TextColumn("Image URL"),
                "weightNet": st.column_config.NumberColumn("Weight Net (Grammes)", format="%.3f"),
                "weightBrut": st.column_config.NumberColumn("Weight Brut (Grammes)", format="%.3f"),
                "uid": st.column_config.NumberColumn("UID", format="%d", step=1, required=True)
            },
            key="xau_editor_v4"
        )

        if st.button("💾 Save All Changes (Xau)"):
            sync_domains_from_df(edited_df)
            run_query("DELETE FROM Xau", is_select=False)
            for _, row in edited_df.iterrows():
                run_query("""INSERT INTO Xau (uid, codeBcee, name, form, purity, weightNet, weightBrut, image) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                          (int(row['uid']), row['codeBcee'], row['name'], row['form'], row['purity'], row['weightNet'], row['weightBrut'], row['image']), 
                          is_select=False)
            st.success("Xau database updated.")
            st.rerun()

def screen_rate_management():
    st.title("📊 Rate History Management")
    
    xau_data = run_query("SELECT uid, name FROM Xau")
    if xau_data is None or xau_data.empty:
        st.error("Please populate the Xau table first.")
        return

    name_to_uid = {row['name']: row['uid'] for _, row in xau_data.iterrows()}
    uid_to_name = {row['uid']: row['name'] for _, row in xau_data.iterrows()}

    df = run_query("SELECT pk_dt, priceBceeBuy, priceBceeSell, pkfk_uid FROM Rate")
    
    if df is not None:
        df['asset_name'] = df['pkfk_uid'].map(uid_to_name)

        edited_df = st.data_editor(
            df, 
            num_rows="dynamic", 
            width='stretch',
            hide_index=True,
            column_config={
                "asset_name": st.column_config.SelectboxColumn(
                    "Asset Name",
                    options=list(name_to_uid.keys()),
                    required=True
                ),
                "priceBceeBuy": st.column_config.NumberColumn("Buy Price", format="%.2f €"),
                "priceBceeSell": st.column_config.NumberColumn("Sell Price", format="%.2f €"),
                "pk_dt": st.column_config.DateColumn("Date", required=True),
                "pkfk_uid": None 
            },
            key="rate_editor_v4"
        )
        
        if st.button("💾 Save Changes (Rates)"):
            run_query("DELETE FROM Rate", is_select=False)
            for _, row in edited_df.iterrows():
                target_uid = name_to_uid.get(row['asset_name'])
                if target_uid:
                    run_query("INSERT INTO Rate (pk_dt, priceBceeBuy, priceBceeSell, pkfk_uid) VALUES (%s, %s, %s, %s)",
                              (row['pk_dt'], row['priceBceeBuy'], row['priceBceeSell'], int(target_uid)), is_select=False)
            st.success("Rate history updated.")
            st.rerun()

def screen_domain_tables():
    st.title("🗂️ Domain Values Editor")
    tables = {"CodeBcee": "codeBcee", "Form": "form", "Image": "image", "Name": "name", "Purity": "purity", "Uid": "uid", "Weight": "weight"}
    target = st.selectbox("Select Domain Table", list(tables.keys()))
    db_col = tables[target]
    
    df = run_query(f"SELECT * FROM `{target}`")
    if df is not None:
        if target == "Uid":
            col_cfg = {db_col: st.column_config.NumberColumn("UID", format="%d", step=1, required=True)}
        elif target == "Weight":
            col_cfg = {db_col: st.column_config.NumberColumn("Weight", format="%.3f")}
        else:
            col_cfg = {db_col: st.column_config.TextColumn(target, required=True)}

        edited_df = st.data_editor(df, num_rows="dynamic", width='stretch', hide_index=True, column_config=col_cfg, key=f"dom_edit_v4_{target}")
        
        if st.button(f"💾 Update {target}"):
            run_query(f"DELETE FROM `{target}`", is_select=False)
            for _, row in edited_df.iterrows():
                val = int(row[db_col]) if target == "Uid" else row[db_col]
                run_query(f"INSERT INTO `{target}` (`{db_col}`) VALUES (%s)", (val,), is_select=False)
            st.success(f"Domain table {target} updated.")
            st.rerun()

        if target == "Image":
            st.divider()
            st.subheader("🖼️ Preview Gallery")
            cols = st.columns(3)
            for i, url in enumerate(df[db_col]):
                if url: cols[i % 3].image(url, caption=f"URL {i+1}", width=200)

# --- 5. MAIN NAVIGATION ---

def main():
    st.set_page_config(page_title="XAU Database Pro", layout="wide")
    st.sidebar.title("💎 Gold Manager")
    choice = st.sidebar.radio("Navigation", ["Dashboard", "Xau Assets", "Rate Management", "Domain Tables"], key="main_nav_v4")

    try:
        if choice == "Dashboard": screen_dashboard()
        elif choice == "Xau Assets": screen_xau_management()
        elif choice == "Rate Management": screen_rate_management()
        elif choice == "Domain Tables": screen_domain_tables()
    except Exception as e:
        st.error(f"Application Error: {e}")

if __name__ == "__main__":
    main()
