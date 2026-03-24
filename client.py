import json
from socket import *
from constCS import *

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

# client manda um lote de tarefas de analise para o servidor
tarefas = [
    {
        "comando": "analise_entropia", 
        "texto": "z5A!9kP@qL2#vM8*xW1$" #   (alta entropia)
    },
    {
        "comando": "extrair_ips", 
        "texto": "Acesso negado no log. Origem: 192.168.1.45. Tentativa de brute force a partir de 10.0.0.7 na porta 22."
    },
    {
        "comando": "cifra_xor", 
        "texto": "senha_banco_dados", 
        "chave": 42 #  chave numerica para ofuscar o texto
    }
]

dados = json.dumps(tarefas)
s.send(str.encode(dados))

resposta = s.recv(4096)
resultados = json.loads(bytes.decode(resposta))

print("=== Relatório de Processamento do Servidor ===")
for res in resultados:
    print(res)

s.close()
