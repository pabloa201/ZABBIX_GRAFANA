Automação de Instalação: Zabbix 7.2 + Grafana
Este diretório contém soluções para automatizar o deployment da stack de monitoramento em ambientes Linux (Ubuntu 22.04+).

1. Script da Comunidade (AUTOMZG)
Localizado na pasta AUTOMZG-main, este é um projeto encontrado na comunidade (LinkedIn) que realiza a instalação completa e automatizada das aplicações.

Como utilizar:

git clone https://github.com/bug-it/automzg.git
cd automzg
chmod +x automzg.sh
sudo ./automzg.sh

2. Minha Versão Otimizada (Com Foco em Segurança)
O arquivo install-zabbix-grafana.ufw-linux.sh é uma versão personalizada por mim. A diferença aplicada é do Firewall (UFW).

Ao executar este script, o sistema configura automaticamente as regras de segurança, permitindo o tráfego apenas nas portas essenciais:

10050-10051: Comunicação Zabbix (Agent/Server)

80 / 443: Interface Web (HTTP/HTTPS)

3000: Dashboards Grafana

Como executar minha versão:

Crie o arquivo: sudo nano install-zabbix-grafana-ufw-linux.sh

Cole o conteúdo do script e salve.

Rode os comandos:

Bash
chmod +x install-zabbix-grafana-ufw-linux.sh
sudo ./install-zabbix-grafana-ufw-linux.sh
