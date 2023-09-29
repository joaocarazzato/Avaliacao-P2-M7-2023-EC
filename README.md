# Prova 2 - Modulo 7

O objetivo desse repositório, é a entrega da prova prática 2 do módulo 7, onde era preciso realizar o deploy de uma aplicação em prod na Cloud, nesse caso, na AWS.

https://github.com/joaocarazzato/Avaliacao-P2-M7-2023-EC/assets/99187756/32f77222-4a77-452c-847c-566943e5c25f

## Como realizei o deploy?

Primeiro, eu baixei os arquivos disponibilizados pelo professor em seu repositório e analisei eles, o que eu precisava mudar? O que eu tinha que fazer com esses arquivos?

Após isso, considerei que a primeira etapa seria criar um banco de dados RDS dentro da AWS, e tentar enviar e receber dados localmente pelo frontend. Então, além de adaptar os códigos para a minha própria database, realizei mais algumas mudanças para que fosse necessário utilizar somente um arquivo python e que a mudança de IP no frontend não fosse feita de forma manual, exemplo:

```
var server_ip = "ip_do_servidor"

function addTask() {
  const taskInput = document.getElementById("taskInput");
  const taskText = taskInput.value.trim();

  if (taskText !== "") {
    //Realizar um POST com fetch para enviar os dados para o backend
    fetch(`http://${server_ip}/create_note`, {
    
    [...]
```

Com isso, consegui realizar testes locais mais facilmente para então passar para a Cloud.

Então, adicionei uma seção de código a aplicação de backend(backend/main.py), para que quando ele recebesse o parâmetro "create_db", ele criasse a tabela e não tivesse que realizar o procedimento através da execução de outro arquivo:

```
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    print('Criando tabela...\n')
    # cria o banco de dados
    create_table()

    print('Tabela criada.')
    sys.exit(0)
```

Então, para executá-lo agora, ficaria assim: ```python main.py create_db```

Assim, a tabela já seria criada e já poderia ser utilizada.
Porém, percebi que meu código não estava funcionando, acabou que faltou uma linha de código para realmente enviar/commitar as mudanças que queriamos na db, então adicionei-a dentro da função ```create_table()```:

```
[...]

    # Commita as mudanças para o banco
    con.commit()
    # Fecha a conexão
    con.close()

[...]
```

Após isso, tive que subir duas EC2s, tanto para o frontend quanto o backend, ao fazer isso, tive que permitir as conexões de HTTP e HTTPS. Então, configurei primeiramente o backend, utilizando também um IP Elástico, para que eu pudesse alterar o ip utilizado no frontend com mais facilidade. Para o backend, eu criei um dockerfile para facilitar o meu processo, e digitei os seguintes comandos:

```
sudo apt update
sudo apt upgrade -y
git clone https://github.com/joaocarazzato/Avaliacao-P2-M7-2023-EC.git
sudo apt install docker.io
sudo apt install docker-compose
cd Avaliacao-P2-M7-2023-EC/backend
sudo docker build . -t backend
sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
sudo docker run -p 8000:8000 backend
```

Após isso, meu backend estava rodando na nuvem e pronto para receber conexões em seu ip direto, sem utilizar a porta 8000 por ter sido criado um redirecionamento.

E então, tive que criar a EC2 do meu frontend, também abrindo as conexões HTTP e HTTPS, após isso, executei os seguintes comandos:

```
sudo apt update
sudo apt upgrade -y
sudo apt install apache2
git clone https://github.com/joaocarazzato/Avaliacao-P2-M7-2023-EC.git
sudo cp ./Avaliacao-P2-M7-2023-EC/frontend/* /var/www/html
```

Após isso, pelo Apache já redirecionar nossas portas para a porta 80, eu já conseguia acessar o meu frontend e fazer requisições para meu backend como demonstrado no primeiro vídeo.

