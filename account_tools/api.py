import requests

def autenticar_api(usuario: str, senha: str, url_token="http://127.0.0.1:8000/api/token/"):
    try:
        resp = requests.post(url_token, json={"username": usuario, "password": senha})
        print(resp.json())
        if resp.status_code == 200:
            json_resp = resp.json()
            token = json_resp.get("access")
            ip = json_resp.get("client_ip")  # IP vindo do backend
            if token:
                return {"token": token, "ip": ip}
            else:
                raise Exception("Token não recebido da API.")
        else:
            raise Exception("Credenciais inválidas.")
    except Exception as e:
        raise e
