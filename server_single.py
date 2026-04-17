import json
import math
import re
from socket import *
from constCS import *

def calcular_entropia(texto):
    if not texto: return 0
    entropia = 0
    for x in set(texto):
        p_x = float(texto.count(x)) / len(texto)
        entropia += - p_x * math.log2(p_x)
    return round(entropia, 4)

s = socket(AF_INET, SOCK_STREAM) 
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
s.bind((HOST, PORT))
s.listen(100)

print("Servidor Single-Thread (1 por vez) aguardando conexões...")

while True:
    # Ele aceita a conexão e trava o laço aqui até terminar tudo
    (conn, addr) = s.accept()
    try:
        data = conn.recv(4096)
        if data:
            requisicoes = json.loads(bytes.decode(data))
            respostas = []
            
            for req in requisicoes:
                comando = req.get('comando')
                if comando == 'analise_entropia':
                    respostas.append({'comando': comando, 'resultado_entropia': calcular_entropia(req.get('texto', ''))})
                elif comando == 'extrair_ips':
                    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', req.get('texto', ''))
                    respostas.append({'comando': comando, 'ips_encontrados': ips})
                elif comando == 'cifra_xor':
                    ofuscado = "".join(chr(ord(c) ^ req.get('chave', 0)) for c in req.get('texto', ''))
                    respostas.append({'comando': comando, 'resultado_xor': ofuscado})
                    
            conn.send(str.encode(json.dumps(respostas)))
    except Exception as e:
        print(f"Erro com o cliente {addr}: {e}")
    finally:
        conn.close()