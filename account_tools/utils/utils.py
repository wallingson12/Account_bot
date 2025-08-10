import random
import re
import hashlib

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email)

def gerar_codigo():
    return f"{random.randint(0, 999999):06d}"

def gerar_hash_codigo(codigo):
    return hashlib.sha256(codigo.encode()).hexdigest()