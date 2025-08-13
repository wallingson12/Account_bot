import random
import re
import hashlib
import os
import pandas as pd

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email)

def gerar_codigo():
    return f"{random.randint(0, 999999):06d}"

def gerar_hash_codigo(codigo):
    return hashlib.sha256(codigo.encode()).hexdigest()

def save_to_excel(df, excel_path, sheet_name='Dados'):
    if os.path.exists(excel_path):
        try:
            with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception:
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)