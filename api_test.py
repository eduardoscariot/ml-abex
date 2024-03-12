import requests

# Arquivo projetado para a realização de testes da API via código

# Teste 1
response = requests.get("http://127.0.0.1:8000/")

# Apresenta mensagem com o retorno do teste.
if response.status_code == 200:
    response_data = response.json()
    print(f"Teste 01 - OK. Response: {response_data}")
else:
    print(f"Falha na requisição do Teste 01: {response.status_code}")