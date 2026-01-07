import requests
import json

# ========== CONFIGURE AQUI ==========
BASE_URL = "http://localhost:8000"
USERNAME = "wallingson"  # ALTERE AQUI
PASSWORD = "lisagawski"  # ALTERE AQUI


# ====================================

def test_single_session():
    print("=" * 60)
    print("TESTE: SESSÃO ÚNICA - REVOGAÇÃO DE TOKENS")
    print("=" * 60)

    # ========== PASSO 1: PRIMEIRO LOGIN ==========
    print("\n[PASSO 1] Fazendo primeiro login...")
    try:
        response1 = requests.post(
            f"{BASE_URL}/api/token/",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=10
        )
    except Exception as e:
        print(f"❌ ERRO de conexão: {e}")
        return

    if response1.status_code != 200:
        print(f"❌ ERRO no login: Status {response1.status_code}")
        print(f"Resposta: {response1.text}")
        return

    data1 = response1.json()
    token1_access = data1.get('access', '')
    token1_refresh = data1.get('refresh', '')
    ip1 = data1.get('client_ip', 'N/A')

    print(f"✅ Login 1 realizado com sucesso!")
    print(f"   IP: {ip1}")
    print(f"   Access Token: {token1_access[:40]}...")
    print(f"   Refresh Token: {token1_refresh[:40]}...")

    # ========== PASSO 2: SEGUNDO LOGIN (MESMA CONTA) ==========
    print("\n[PASSO 2] Fazendo SEGUNDO login com a mesma conta...")
    print("   (Isso deve revogar o token 1)")

    import time
    time.sleep(1)  # Pequena pausa para garantir timestamps diferentes

    try:
        response2 = requests.post(
            f"{BASE_URL}/api/token/",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=10
        )
    except Exception as e:
        print(f"❌ ERRO de conexão: {e}")
        return

    if response2.status_code != 200:
        print(f"❌ ERRO no segundo login: Status {response2.status_code}")
        return

    data2 = response2.json()
    token2_access = data2.get('access', '')
    token2_refresh = data2.get('refresh', '')
    ip2 = data2.get('client_ip', 'N/A')

    print(f"✅ Login 2 realizado com sucesso!")
    print(f"   IP: {ip2}")
    print(f"   Access Token: {token2_access[:40]}...")
    print(f"   Refresh Token: {token2_refresh[:40]}...")

    # ========== PASSO 3: TENTAR USAR REFRESH TOKEN 1 ==========
    print("\n[PASSO 3] Tentando usar o REFRESH TOKEN 1...")
    print("   Resultado esperado: FALHA (401) - token revogado")

    try:
        response_refresh1 = requests.post(
            f"{BASE_URL}/api/token/refresh/",
            json={"refresh": token1_refresh},
            timeout=10
        )
    except Exception as e:
        print(f"❌ ERRO de conexão: {e}")
        return

    print(f"   Status: {response_refresh1.status_code}")

    if response_refresh1.status_code == 401:
        print("   ✅ CORRETO! Token 1 foi revogado com sucesso!")
        try:
            error_data = response_refresh1.json()
            print(f"   Mensagem: {error_data}")
        except:
            print(f"   Resposta: {response_refresh1.text}")
    else:
        print("   ❌ ERRO! Token 1 ainda está válido (não deveria!)")
        try:
            print(f"   Resposta: {response_refresh1.json()}")
        except:
            print(f"   Resposta: {response_refresh1.text}")

    # ========== PASSO 4: TENTAR USAR REFRESH TOKEN 2 ==========
    print("\n[PASSO 4] Tentando usar o REFRESH TOKEN 2...")
    print("   Resultado esperado: SUCESSO (200)")

    try:
        response_refresh2 = requests.post(
            f"{BASE_URL}/api/token/refresh/",
            json={"refresh": token2_refresh},
            timeout=10
        )
    except Exception as e:
        print(f"❌ ERRO de conexão: {e}")
        return

    print(f"   Status: {response_refresh2.status_code}")

    if response_refresh2.status_code == 200:
        print("   ✅ CORRETO! Token 2 está funcionando!")
        data = response_refresh2.json()
        new_access = data.get('access', '')
        print(f"   Novo Access Token: {new_access[:40]}...")
    else:
        print("   ❌ ERRO! Token 2 não está funcionando (deveria!)")
        try:
            print(f"   Resposta: {response_refresh2.json()}")
        except:
            print(f"   Resposta: {response_refresh2.text}")

    # ========== RESUMO ==========
    print("\n" + "=" * 60)
    print("RESUMO DO TESTE")
    print("=" * 60)

    test_passed = True

    print("✅ Login 1: Sucesso")
    print("✅ Login 2: Sucesso")

    if response_refresh1.status_code == 401:
        print("✅ Token 1 REVOGADO: Correto!")
    else:
        print("❌ Token 1 AINDA VÁLIDO: Erro na implementação!")
        test_passed = False

    if response_refresh2.status_code == 200:
        print("✅ Token 2 VÁLIDO: Correto!")
    else:
        print("❌ Token 2 INVÁLIDO: Erro na implementação!")
        test_passed = False

    print("=" * 60)

    if test_passed:
        print("\n🎉 TESTE PASSOU! Sistema de sessão única funcionando!")
    else:
        print("\n⚠️  TESTE FALHOU! Verifique a implementação.")

    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️  Certifique-se de que:")
    print("   1. O servidor Django está rodando")
    print("   2. Você alterou USERNAME e PASSWORD no código")
    print("   3. A URL está correta\n")

    input("Pressione ENTER para iniciar o teste...")

    test_single_session()