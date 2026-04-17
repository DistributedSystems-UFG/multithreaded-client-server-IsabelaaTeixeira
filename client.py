import json
import random
import string
import threading
import time
from socket import *
from constCS import *

# VARIÁVEL DE CONTROLE: Quantas requisições vamos fazer no teste?
NUM_REQUISICOES = 1000 

def gerar_tarefa_aleatoria():
    comandos = ['analise_entropia', 'extrair_ips', 'cifra_xor']
    comando = random.choice(comandos)
    
    if comando == 'analise_entropia':
        # Gera uma string aleatória de 30 caracteres
        texto = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        return [{"comando": comando, "texto": texto}]
        
    elif comando == 'extrair_ips':
        # Gera um IP aleatório falso para colocar num log
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        return [{"comando": comando, "texto": f"Log de acesso suspeito. Origem: {ip} detectada no firewall."}]
        
    elif comando == 'cifra_xor':
        # Gera um texto aleatório para ofuscar
        texto = ''.join(random.choices(string.ascii_letters, k=15))
        return [{"comando": comando, "texto": texto, "chave": random.randint(1, 50)}]

# FUNÇÃO DA THREAD: Cria a conexão, gera os dados, envia, recebe e fecha
def disparar_requisicao():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        
        tarefa = gerar_tarefa_aleatoria()
        s.send(str.encode(json.dumps(tarefa)))
        
        resposta = s.recv(4096)
        # Ocultamos o "print" da resposta aqui para não poluir o terminal durante o teste de mil requisições
        
        s.close()
    except Exception as e:
        print(f"Erro na conexão da thread: {e}")

print(f"Preparando envio de {NUM_REQUISICOES} requisições em paralelo...")
threads = []

# Inicia o cronômetro
start_time = time.time()

# Cria e dispara as mil threads simultaneamente
for _ in range(NUM_REQUISICOES):
    t = threading.Thread(target=disparar_requisicao)
    threads.append(t)
    t.start()

# O comando .join() faz o programa esperar todas as threads terminarem antes de continuar
for t in threads:
    t.join()

# Para o cronômetro
end_time = time.time()
tempo_total = end_time - start_time

print("=== EXPERIMENTO 1 CONCLUÍDO ===")
print("Arquitetura: Cliente Multithread vs Servidor Multithread")
print(f"Total de requisições: {NUM_REQUISICOES}")
print(f"Tempo total de processamento: {tempo_total:.4f} segundos.")