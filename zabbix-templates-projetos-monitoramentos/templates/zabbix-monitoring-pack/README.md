Zabbix Monitoring Pack: Infraestrutura Completa
Este repositório contém uma coleção de templates e configurações do Zabbix (versão 7.2) desenvolvidos para o monitoramento proativo de infraestruturas críticas. O foco é garantir a alta disponibilidade de serviços essenciais, desde bancos de dados Oracle até o parque de impressão e links de internet.

Conteúdo do Repositório
1. Bancos de Dados (Oracle)
Arquivo: DATABASES_ORACLE.yaml

Destaque: Monitoramento de conectividade via ODBC (DSN) com triggers de nodata para alertas de indisponibilidade (Priority: Disaster). Ideal para ambientes que dependem de ERPs e sistemas legados.

2. Conectividade e Telecom
Arquivos: LINKS_INTERNET_MPLS.yaml e PABXS.yaml

Destaque: Monitoramento de latência e perda de pacotes (ICMP Ping) com gráficos empilhados (Stacked) para análise visual rápida de oscilações em links de diferentes operadoras (Vivo, Embratel, Copel, etc).

3. Servidores e Automação
Arquivo: SERVIDORES.yaml

Destaque: Inclui monitoramento avançado de disco e uma trigger personalizada para BAD_ADDRESS via logs do DHCP (logrt), demonstrando capacidade de automação em nível de sistema operacional (Windows/Active Directory).

4. Periféricos e UPS (Nobreaks/Impressoras)
Arquivos: NOBREAK.yaml e IMPRESSORAS.yaml

Destaque: Uso de SNMPv3 com autenticação para monitoramento seguro de Nobreaks APC (Voltagem de fase, carga de bateria) e monitoramento de status de impressoras em rede.

5. Notificações Inteligentes (Telegram Bot)
Arquivo: TemplateTelegramBotAlert.json

Destaque: Configuração de Webhook para integração do Zabbix com o Telegram. Permite o envio de alertas formatados em Markdown diretamente para grupos de suporte, agilizando o tempo de resposta (MTTR).

Como Utilizar
Realize o import dos arquivos .yaml ou .json na interface do seu Zabbix em Data Collection > Templates > Import.

Para o bot do Telegram, configure as macros {$TOKEN} e {$ID_DO_GRUPO} conforme as instruções no script do Webhook.

Associe os hosts aos respectivos templates e ajuste as interfaces (IP/SNMP).