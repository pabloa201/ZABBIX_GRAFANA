DHCP BAD_ADDRESS Monitor: Prevenção de Conflitos de Rede
Este projeto nasceu de uma necessidade real: detetar de forma proativa falhas silenciosas no servidor DHCP do Windows causadas por dispositivos de rede defeituosos que "queimam" endereços de IP, gerando a entrada BAD_ADDRESS e paralisando a autenticação de novos dispositivos na rede.

O Problema
Em ambientes corporativos, adaptadores USB/Ethernet, switchs de entrada e de baixa qualidade podem tentar capturar IPs incessantemente, forçando o DHCP a marcar esses endereços como conflitantes (BAD_ADDRESS). Sem uma notificação nativa do Windows, a equipa de TI só percebe o problema quando o pool de IPs se esgota, causando paragens na operação.

A Solução
Desenvolvi uma solução híbrida que utiliza um script Python customizado e o Zabbix Agent 2 para monitorizar os logs do DHCP em tempo real, disparando alertas imediatos sempre que um novo conflito é registado.

Deteta automaticamente se os logs do Windows estão em Português ou Inglês.

Uma memoria simples para salvar o denreço que queimou: Utiliza hashing (MD5) para garantir que um alerta só seja disparado uma vez por cada evento, evitando alarmes repetitivos sempre que ele rodar.

Por exemplo, se a renovação do pool do dhcp for 5 dias, enquanto ele nao encontrar um novo endereço que ficou como BAD_ADDRES, ele nao vai gerar alerta, se aparecer somente 1, ficara aquele 1 unico com um alerta somente, caso renovar o dhcp e outro endereço ficar queimado, dai sim, ele vai alertar, pois como o pool reiniciou, ele será visto como novo.

Possui um contador interno que evita o crescimento infinito dos ficheiros de log locais.

Baixo Footprint: Executado como um .exe compilado, sem necessidade de instalar o Python no servidor de produção.

Configuração do Ambiente:

1. No Servidor Zabbix
Crie um item no Host do Servidor DHCP:

Nome: ALERTA! BAD_ADDRESS

Tipo: Zabbix Agent (Active)

Chave: dhcp.badaddress

Tipo de Informação: Numeric (Unsigned)

Intervalo: 2m

*Trigger de Incidente:

last(/NOME_DO_HOST/dhcp.badaddress)=1

Trigger de Recuperação:

last(/NOME_DO_HOST/dhcp.badaddress)=0

2. No Servidor DHCP (Windows)
No ficheiro zabbix_agent2.conf, adicione o parâmetro de utilizador:

UserParameter=dhcp.badaddress, "C:\Scripts\CheckBAD_ADDRESS\CheckBAD_ADDRESS.exe"

O Script Python (Lógica Core) SCRIPT DISPONIVEL NO ARQUIVO "main.py"
O script realiza o parsing do log oficial do Windows (C:\Windows\System32\dhcp\DhcpSrvLog-*.log).

Fluxo de Execução:

Identifica o dia da semana atual.

Abre o log com codificação latin-1 (padrão Windows).

Procura pelo código de evento 13 (Conflict/BAD_ADDRESS).

Gera um Hash da linha; se for diferente do último Hash guardado, retorna 1 (Alerta), caso contrário retorna 0.

Compilação:

pip install pyinstaller
pyinstaller --onefile --console main.py

Estrutura de Ficheiros local

Após a primeira execução, o script gere automaticamente na pasta C:\Scripts\CheckBAD_ADDRESS\:

CheckBAD_ADDRESS.exe: executavel principal

conflitos_dhcp.txt: log de IPs que sofreram conflito.

last_check.txt: Memória do último Hash processado.

contador.txt: Controlo de rotação de logs.