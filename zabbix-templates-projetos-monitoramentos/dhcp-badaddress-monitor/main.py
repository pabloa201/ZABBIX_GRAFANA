import os
import sys
import hashlib
import datetime


def check_new_bad_address():
    # 1. Definir caminhos absolutos de forma segura
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    arquivo_controle = os.path.join(base_path, "last_check.txt")
    arquivo_historico = os.path.join(base_path, "conflitos_dhcp.txt")
    arquivo_contador = os.path.join(base_path, "contador.txt")

    # 2. Identificar o log do Windows (Português/Inglês)
    dias_pt = {'Mon': 'Seg', 'Tue': 'Ter', 'Wed': 'Qua', 'Thu': 'Qui', 'Fri': 'Sex', 'Sat': 'Sab', 'Sun': 'Dom'}
    now = datetime.datetime.now()
    dia_en = now.strftime('%a')
    dia_pt = dias_pt.get(dia_en, dia_en)

    caminho_log = f"C:\\Windows\\System32\\dhcp\\DhcpSrvLog-{dia_pt}.log"
    if not os.path.exists(caminho_log):
        caminho_log = f"C:\\Windows\\System32\\dhcp\\DhcpSrvLog-{dia_en}.log"

    if not os.path.exists(caminho_log):
        return "0"

    # 3. Ler o Hash anterior
    last_hash = ""
    if os.path.exists(arquivo_controle):
        try:
            with open(arquivo_controle, 'r') as f:
                last_hash = f.read().strip()
        except:
            pass

    # 4. Processar o log
    try:
        with open(caminho_log, 'r', encoding='latin-1', errors='ignore') as f:
            lines = f.readlines()

        for line in reversed(lines):
            line_strip = line.strip()
            if line_strip.startswith('13') or "BAD_ADDRESS" in line_strip:
                current_hash = hashlib.md5(line_strip.encode('utf-8')).hexdigest()

                if current_hash != last_hash:
                    # Tenta salvar os arquivos de log/controle
                    try:
                        # Gerenciar contador
                        count = 0
                        if os.path.exists(arquivo_contador):
                            with open(arquivo_contador, 'r') as c:
                                content = c.read().strip()
                                count = int(content) if content.isdigit() else 0

                        novo_count = 1 if count >= 3 else count + 1
                        modo = 'w' if count >= 3 else 'a'

                        # Salvar histórico
                        with open(arquivo_historico, modo) as h:
                            ts = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                            h.write(f"[{ts}] {line_strip}\n")

                        # Salvar novo contador e novo hash
                        with open(arquivo_contador, 'w') as c:
                            c.write(str(novo_count))
                        with open(arquivo_controle, 'w') as ctrl:
                            ctrl.write(current_hash)
                    except:
                        pass  # Se falhar a escrita, ainda assim retornamos 1

                    return "1"
                else:
                    return "0"
        return "0"
    except:
        return "0"


if __name__ == "__main__":
    try:
        resultado = check_new_bad_address()
        # Garante que o resultado seja string e limpa espaços
        saida = str(resultado).strip()
        # Usa o print comum que é mais seguro para o console do PyCharm
        print(saida, end='')
    except Exception:
        # Caso ocorra um erro catastrófico, retorna 0 para não quebrar o Zabbix
        print("0", end='')