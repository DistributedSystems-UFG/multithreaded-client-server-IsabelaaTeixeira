[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7EVNAYx2)
# ClientServerBasics (2.0)
Starter code for the basic client-server assignment


Este template corresponde ao exemplo da Fig. 2.3 do livro. O exercício consiste em acrescentar funcionalidade ao servidor para torná-lo mais útil. Essa funcionalidade deve ser acessível aos clientes. Por exemplo, o servidor pode ser uma espécie de calculadora remota. O cliente passa dois valores numéricos, juntamente com o nome de uma operação (ex.: add, subtract, multiply, divide) e o servidor executa a operação respectiva e retorna seu resultado para o cliente. Você pode implementar um servidor com outras funcionalidades (diferente da calculadora). O imporante é que ele ofereça pelo menos três operações diferentes que os clientes podem utilizar remotamente, passando dados para serem processados e recebendo o resultado desse processamento como resposta.

Tarefa individual.

## PASSO A PASSO 

O primeiro passo dessa atividade foi acessar e configurar as instâncias no AWS Academy. Seguindo o passo a passo da aula e do vídeo disponibilizado pelo professor na plataforma turing, lancei 6 instâncias peer (na região N. Virginia), 1 instância server (também na região N. Virginia) e outras 2 instâncias peer (na região Oregon). Além disso, estabelecemos um Elastic IP para o server.

![[Pasted image 20260323200001.png]]


### Acessando as instâncias

Após isso, o objetivo foi acessar essas instâncias para testar a comunicação entre elas, para isso abrimos dois terminais locais para acessar as máquinas virtuais criadas na AWS Academy, utilizando o usuário correto para a imagem do sistema (`ec2-user`):

- **Terminal 1 (Server):**
```
ssh -i 2026-1-east.pem ec2-user@52.3.203.46
```
 ![[Pasted image 20260323200634.png]]


- **Terminal 2 (Client / `peer1`):**
```    
ssh -i 2026-1-east.pem ec2-user@100.54.202.135
```
![[Pasted image 20260323200658.png]]
```No caso do client, esse IP varia a cada vez que o AWS é aberto.```


### Git

Após os terminais serem acessados, realizei o git clone do repositório do github em cada uma das máquinas, com o comando:
```    
git clone https://github.com/DistributedSystems-UFG/basic-client-server-with-sockets-IsabelaaTeixeira.git
```

Com o repositório clonado, foi preciso ajustar o ip do HOST, que é o "Private IPv4 addresses" mostrado na imagem. 

![[Pasted image 20260323201031.png]]

Assim, acessei o arquivo constCS.py nos dois terminais e alterei o conteúdo para o valor correto do host, fazendo um ```nano constCS.py``` e assim ficando:

```    
HOST = '172.31.23.228'
PORT = 5678
```

### Verificando a comunicação

Para verificar se as máquinas estão conseguindo se comunicar, primeiro realizamos um ```python3 server.py``` (para isso é necessário estar no diretório que contém o arquivo server.py) na máquina server. Inicialmente a máquina vai ficar carregando e esperando a confirmação do outro lado:
![[Pasted image 20260323202107.png]]

Com isso, realiza-se um ```python3 client.py``` (para isso é necessário estar no diretório que contém o arquivo client.py) na máquina client. Ao fazer isso, o cliente envia um ```Hello, world``` para o servidor. Após isso conseguimos ver a mensagem sendo enviada e chegando do outro lado:
![[Pasted image 20260323202657.png]]
![[Pasted image 20260323202715.png]]


## Aplicando as alterações pedidas

Com base no exemplo fornecido em aula (slide 5), faça o seguinte:
- acrescente complexidade no processamento da requisição no servidor;
- permita que o cliente chame mais de uma funcionalidade diferente no servidor a cada requisição.

A minha ideia foi transformar o servidor em um **Mini Kit de Forense Digital e Segurança**, de forma que teremos 3 funcionalidades: 
- **`analise_entropia`**: Calcula a entropia de Shannon de um texto (muito usado em forense para descobrir se um dado está criptografado ou compactado).
- **`extrair_ips`**: Vasculha um texto de log e extrai todos os endereços de IP suspeitos usando Regex.
- **`cifra_xor`**: Aplica uma operação bit a bit (XOR) com uma chave para ofuscar ou desofuscar uma string.