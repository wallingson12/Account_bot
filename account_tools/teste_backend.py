import requests
import sqlite3
import pandas as pd

# TES_GET_IP
def test_get_ip_user():
    resp = requests.post("http://127.0.0.1:8000/api/token/", json={
        "username": "wallingson",
        "password": "lisagawski"
    })

    data = resp.json()
    token_access = data.get("access")
    client_ip = data.get("client_ip")

    print("Token de acesso:", token_access)
    print("IP do cliente:", client_ip)

#test_get_ip_user()
