#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import re

download_dir = r"C:\Users\lanfr144\Documents\DEVOP1\COURS\download"
keywords = ["kubernetes", "k8s", "swarm", "airflow", "zabbix", "grafana", "prometheus", "influxdb", "uptime kuma", "jenkins", "mysql", "postgresql", "flask", "django"]

def search_files():
    results = {kw: [] for kw in keywords}
    for file in os.listdir(download_dir):
        if not file.endswith((".pdf", ".docx", ".pptx")):
            continue
        file_path = os.path.join(download_dir, file)
        try:
            with open(file_path, 'rb') as f:
                data = f.read().lower()
                for kw in keywords:
                    # Search using simple byte matching
                    kw_bytes = kw.encode('utf-8')
                    if kw_bytes in data:
                        results[kw].append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            
    print("Search results:")
    for kw, files in results.items():
        print(f"{kw.upper()}: found in {len(files)} files: {files}")

if __name__ == "__main__":
    search_files()
