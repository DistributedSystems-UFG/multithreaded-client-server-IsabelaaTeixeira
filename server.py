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
s.bind((HOST, PORT))
s.listen(1)

print("Servidor de Análise aguardando conexões...")
(conn, addr) = s.accept()

while True:
    data = conn.recv(4096)
    if not data: break
    
    requisicoes = json.loads(bytes.decode(data))
    respostas = []
    
    for req in requisicoes:
        comando = req.get('comando')
        
        if comando == 'analise_entropia':
            texto = req.get('texto', '')
            respostas.append({'comando': comando, 'resultado_entropia': calcular_entropia(texto)})
            
        elif comando == 'extrair_ips':
            log = req.get('texto', '')
            # regex para encontrar padroes de IPv4
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log)
            respostas.append({'comando': comando, 'ips_encontrados': ips})
            
        elif comando == 'cifra_xor':
            texto = req.get('texto', '')
            chave = req.get('chave', 0)
            # ofuscacao usando operacao bit a bit XOR
            ofuscado = "".join(chr(ord(c) ^ chave) for c in texto)
            respostas.append({'comando': comando, 'resultado_xor': ofuscado})
            
        else:
            respostas.append({'comando': comando, 'erro': 'Ferramenta não reconhecida'})
    
    conn.send(str.encode(json.dumps(respostas)))

conn.close()
