import json
import random
import string
import time
from socket import *
from constCS import *

NUM_REQUISICOES = 1000 

def gerar_tarefa_aleatoria():
    comandos = ['analise_entropia', 'extrair_ips', 'cifra_xor']
    comando = random.choice(comandos)
    
    if comando == 'analise_entropia':
        texto = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        return [{"comando": comando, "texto": texto}]
    elif comando == 'extrair_ips':
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        return [{"comando": comando, "texto": f"Log suspeito: {ip}"}]
    else:
        texto = ''.join(random.choices(string.ascii_letters, k=15))
        return [{"comando": comando, "texto": texto, "chave": random.randint(1, 50)}]

print(f"Preparando envio de {NUM_REQUISICOES} requisições SEQUENCIAIS (uma por vez)...")

start_time = time.time()

# dispara uma por vez no laço FOR tradicional (sem threads)
for i in range(NUM_REQUISICOES):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        
        tarefa = gerar_tarefa_aleatoria()
        s.send(str.encode(json.dumps(tarefa)))
        
        resposta = s.recv(4096)
        s.close()
    except Exception as e:
        print(f"Erro na requisição {i}: {e}")

end_time = time.time()
tempo_total = end_time - start_time

print("=== EXPERIMENTO 2 CONCLUÍDO ===")
print("Arquitetura: Cliente Single vs Servidor Single")
print(f"Total de requisições: {NUM_REQUISICOES}")
print(f"Tempo total de processamento: {tempo_total:.4f} segundos.")