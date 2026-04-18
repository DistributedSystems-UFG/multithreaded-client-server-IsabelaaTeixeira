import json
import random
import string
import threading
import time
from socket import *
from constCS import *

# variavel de controle
NUM_REQUISICOES = 1000 

def gerar_tarefa_aleatoria():
    comandos = ['analise_entropia', 'extrair_ips', 'cifra_xor']
    comando = random.choice(comandos)
    
    if comando == 'analise_entropia':
        # uma string de 30 caracteres é gerada
        texto = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        return [{"comando": comando, "texto": texto}]
        
    elif comando == 'extrair_ips':
        # ip aleatorio falso
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        return [{"comando": comando, "texto": f"Log de acesso suspeito. Origem: {ip} detectada no firewall."}]
        
    elif comando == 'cifra_xor':
        # texto falso para ofuscar
        texto = ''.join(random.choices(string.ascii_letters, k=15))
        return [{"comando": comando, "texto": texto, "chave": random.randint(1, 50)}]

# a thread cria a conexão, gera os dados, envia, recebe e fecha
def disparar_requisicao():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        
        tarefa = gerar_tarefa_aleatoria()
        s.send(str.encode(json.dumps(tarefa)))
        
        resposta = s.recv(4096)
        
        s.close()
    except Exception as e:
        print(f"Erro na conexão da thread: {e}")

print(f"Preparando envio de {NUM_REQUISICOES} requisições em paralelo...")
threads = []

start_time = time.time()

for _ in range(NUM_REQUISICOES):
    t = threading.Thread(target=disparar_requisicao)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
tempo_total = end_time - start_time

print("=== EXPERIMENTO 1 CONCLUÍDO ===")
print("Arquitetura: Cliente Multithread vs Servidor Multithread")
print(f"Total de requisições: {NUM_REQUISICOES}")
print(f"Tempo total de processamento: {tempo_total:.4f} segundos.")