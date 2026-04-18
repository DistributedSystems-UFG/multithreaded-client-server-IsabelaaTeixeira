import json
import math
import re
import threading
from socket import *
from constCS import *

def calcular_entropia(texto):
    if not texto: return 0
    entropia = 0
    for x in set(texto):
        p_x = float(texto.count(x)) / len(texto)
        entropia += - p_x * math.log2(p_x)
    return round(entropia, 4)

# a thread atende um cliente de forma independente
def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        if not data: return
        
        requisicoes = json.loads(bytes.decode(data))
        respostas = []
        
        for req in requisicoes:
            comando = req.get('comando')
            
            if comando == 'analise_entropia':
                texto = req.get('texto', '')
                respostas.append({'comando': comando, 'resultado_entropia': calcular_entropia(texto)})
                
            elif comando == 'extrair_ips':
                log = req.get('texto', '')
                ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log)
                respostas.append({'comando': comando, 'ips_encontrados': ips})
                
            elif comando == 'cifra_xor':
                texto = req.get('texto', '')
                chave = req.get('chave', 0)
                ofuscado = "".join(chr(ord(c) ^ chave) for c in texto)
                respostas.append({'comando': comando, 'resultado_xor': ofuscado})
                
        conn.send(str.encode(json.dumps(respostas)))
    except Exception as e:
        print(f"Erro com o cliente {addr}: {e}")
    finally:
        conn.close()

s = socket(AF_INET, SOCK_STREAM) 

s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
s.bind((HOST, PORT))

s.listen(100)

print("Servidor Multithread aguardando conexões...")

while True:
    (conn, addr) = s.accept()
    thread_cliente = threading.Thread(target=handle_client, args=(conn, addr))
    thread_cliente.start()