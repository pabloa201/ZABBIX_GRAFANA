Oracle Database Monitoring via ODBC (Zabbix + Ubuntu 24.04)
Este projeto detalha o complexo processo de configuração do Oracle Instant Client em sistemas Linux modernos para habilitar o monitoramento de disponibilidade de instâncias Oracle via ODBC.

O Desafio Técnico
Monitorar Oracle via Zabbix Server (sem agente no banco) exige que o sistema operacional tenha drivers perfeitamente alinhados. No Ubuntu 24.04, a mudança nas bibliotecas base (libaio) geralmente impede o funcionamento dos drivers legados da Oracle. Este guia documenta o workaround de engenharia necessário para superar essas limitações.


1. REQUISITOS DO SISTEMA (UBUNTU 24.04)
--------------------------------------
O Ubuntu 24.04 alterou pacotes base. É necessário instalar a libaio1t64 e 
gerenciar o link simbólico para compatibilidade com o Driver Oracle.

# Instalação dos pacotes
sudo apt update
sudo apt install libaio1t64 unixodbc odbcinst -y

# Correção do link simbólico (Dangling Symlink fix)
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1


2. CONFIGURAÇÃO DO ORACLE INSTANT CLIENT
---------------------------------------

baixar o site do oracle a instancia do stantclient basiclite e o stantclient odbc
e descompactar na apsta em questão com unzip

unzip instantclient-odbc-linux.x64-19.29.0.0.0dbru.zip -d /opt/oracle



Local da Instalação: /opt/oracle/instantclient_19_29

# Ajuste de links internos do Driver
cd /opt/oracle/instantclient_19_29
sudo rm libocci_gcc53.so libclntsh.so
sudo ln -s libocci_gcc53.so.19.1 libocci_gcc53.so
sudo ln -s libclntsh.so.19.1 libclntsh.so

# Permissões de leitura para o usuário do Zabbix
sudo chmod -R 755 /opt/oracle/

checar se ta certo apos os comandos acima:

 ldd /opt/oracle/instantclient_19_29/libsqora.so.19.1
        linux-vdso.so.1 (0x00007ffcd99f9000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x000078c44369c000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x000078c4435b3000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x000078c4435ae000)
        libnsl.so.1 => /lib/x86_64-linux-gnu/libnsl.so.1 (0x000078c443592000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x000078c44358d000)
        libaio.so.1 => not found
        libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x000078c443578000)
        libclntsh.so.19.1 => not found
        libclntshcore.so.19.1 => not found
        libodbcinst.so.2 => /lib/x86_64-linux-gnu/libodbcinst.so.2 (0x000078c443564000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x000078c442e00000)
        /lib64/ld-linux-x86-64.so.2 (0x000078c4436b5000)
        libltdl.so.7 => /lib/x86_64-linux-gnu/libltdl.so.7 (0x000078c443557000)
não pode aparecer not found


se tiver... correção:
sudo apt install libaio1t64 -y
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1
cd /opt/oracle/instantclient_19_29
sudo chmod +x *.so*
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1
deve aparecer:

ln: failed to create symbolic link '/usr/lib/x86_64-linux-gnu/libaio.so.1': File exists
sudo rm libocci_gcc53.so
sudo ln -s libocci_gcc53.so.19.1 libocci_gcc53.so
sudo rm libclntsh.so
sudo ln -s libclntsh.so.19.1 libclntsh.so
sudo chmod -R 755 /opt/oracle/instantclient_19_29
sudo ldconfig

digite novamente:  ldd /opt/oracle/instantclient_19_29/libsqora.so.19.1
deve aparecer assim agora:        
        linux-vdso.so.1 (0x00007ffe4dc62000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x000071c3560d8000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x000071c355d17000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x000071c3560d3000)
        libnsl.so.1 => /lib/x86_64-linux-gnu/libnsl.so.1 (0x000071c355cfb000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x000071c3560ce000)
        libaio.so.1 => /lib/x86_64-linux-gnu/libaio.so.1 (0x000071c3560c7000)
        libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x000071c355ce8000)
        libclntsh.so.19.1 => /opt/oracle/instantclient_19_29/libclntsh.so.19.1 (0x000071c351a00000)
        libclntshcore.so.19.1 => /opt/oracle/instantclient_19_29/libclntshcore.so.19.1 (0x000071c351400000)
        libodbcinst.so.2 => /lib/x86_64-linux-gnu/libodbcinst.so.2 (0x000071c355cd4000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x000071c351000000)
        /lib64/ld-linux-x86-64.so.2 (0x000071c3560f1000)
        libnnz19.so => /opt/oracle/instantclient_19_29/libnnz19.so (0x000071c350800000)
        libltdl.so.7 => /lib/x86_64-linux-gnu/libltdl.so.7 (0x000071c3560ba000)



3. REGISTRO DO DRIVER E BIBLIOTECAS
----------------------------------
Registrar o caminho das bibliotecas no sistema e definir o driver ODBC.

# Registro no Cache do Linux
sudo sh -c "echo /opt/oracle/instantclient_19_29 > /etc/ld.so.conf.d/oracle.conf"
sudo ldconfig

# Definição do Driver (odbcinst.ini)
# Arquivo: /etc/odbcinst.ini
[Oracle]
Description = Oracle ODBC driver
Driver      = /opt/oracle/instantclient_19_29/libsqora.so.19.1


4. CONFIGURAÇÃO DOS BANCOS DE DADOS (DSN)
----------------------------------------
Configurar o arquivo /etc/odbc.ini. 
As credenciais são mantidas aqui para segurança e centralização.

[BASE_PROD]
Driver = Oracle
ServerName = //IP_PROD:1521/SID_PROD
UserID = SEU_USUARIO
Password = SUA_SENHA

[BASE_HML]
Driver = Oracle
ServerName = //IP_HML:1521/SID_HML
UserID = SEU_USUARIO
Password = SUA_SENHA

Feito isso e salvo, para testar a conexão:

isql -v nome_do_serviço user senha
por exemeplo

isql -v BASE_HML consultor c0nsu1t0r

se aparecer:
+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| echo [string]                         |
| quit                                  |
|                                       |
+---------------------------------------+

deu certo.

5. VARIÁVEIS DE AMBIENTE (ZABBIX SERVICE)
----------------------------------------
Necessário para que o serviço 'zabbix-server' enxergue o Instant Client.

Comando: sudo systemctl edit zabbix-server

[Service]
Environment="LD_LIBRARY_PATH=/opt/oracle/instantclient_19_29"
Environment="ORACLE_HOME=/opt/oracle/instantclient_19_29"
Environment="TNS_ADMIN=/opt/oracle/instantclient_19_29"

# Aplicar alterações
sudo systemctl daemon-reload
sudo systemctl restart zabbix-server


6. VALIDAÇÃO E TROUBLESHOOTING
-----------------------------
Teste de conexão via terminal (fingindo ser o usuário zabbix):

sudo -u zabbix isql -v BASE_PROD

# Erros comuns:
# ORA-01017: Usuário/Senha incorretos no odbc.ini ou Case Sensitivity.
# File Not Found: Link simbólico da libaio.so.1 ausente.


7. PADRÃO ZABBIX WEB (GRAFANA)
-----------------------------
- Tipo de Item: Database monitor
- Chave: db.odbc.select[oracle_up,{$ORACLE.DSN}]
- SQL: SELECT 1 FROM DUAL
- User/Pass: Deixar campos vazios no Zabbix (lê do .ini)
- Refresh: 30s (PROD) / 60s (HML)
- Grafana: Value Mapping (1 = Online / 0 = Offline)

==========================================================================

📊 Configuração no Front-end (Zabbix/Grafana)
Item Type: Database monitor

Key: db.odbc.select[oracle_up,{$ORACLE.DSN}]

Query: SELECT 1 FROM DUAL

Visualização: Dashboards no Grafana com Value Mapping (1: Online / 0: Offline).