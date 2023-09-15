import os
import shutil
import sys
from datetime import datetime


def extrair_camera_e_datas_do_nome_arquivo(nome_arquivo, delimitador='_'):
    partes = nome_arquivo.split(delimitador)

    if len(partes) == 5 and partes[1].startswith('ch'):
        camera = partes[1][2:]
        camera = camera.zfill(2)
        ano_inicio, mes_inicio, dia_inicio = partes[3][:4], partes[3][4:6], partes[3][6:8]
        ano_fim, mes_fim, dia_fim = partes[4][:4], partes[4][4:6], partes[4][6:8]
        return camera, ano_inicio, mes_inicio, dia_inicio, ano_fim, mes_fim, dia_fim
    else:
        return None, None, None, None, None, None, None

def obter_nome_mes_em_portugues(numero_mes):
    meses_em_portugues = {
        '01': 'JANEIRO',
        '02': 'FEVEREIRO',
        '03': 'MARÇO',
        '04': 'ABRIL',
        '05': 'MAIO',
        '06': 'JUNHO',
        '07': 'JULHO',
        '08': 'AGOSTO',
        '09': 'SETEMBRO',
        '10': 'OUTUBRO',
        '11': 'NOVEMBRO',
        '12': 'DEZEMBRO'
    }
    return meses_em_portugues.get(numero_mes, numero_mes)

def criar_estrutura_de_pastas(caminho_base, nome_arquivo, origem):
    camera, ano_inicio, mes_inicio, dia_inicio, ano_fim, mes_fim, dia_fim = extrair_camera_e_datas_do_nome_arquivo(nome_arquivo)

    if camera:
        nome_mes_inicio = obter_nome_mes_em_portugues(mes_inicio)
        nome_mes_inicio = nome_mes_inicio.upper()
        nome_mes_fim = obter_nome_mes_em_portugues(mes_fim)
        nome_mes_fim = nome_mes_fim.upper()

        pasta_ano = os.path.join(caminho_base, ano_inicio)
        os.makedirs(pasta_ano, exist_ok=True)

        pasta_mes_inicio = os.path.join(pasta_ano, f'{nome_mes_inicio} - {ano_inicio}')
        os.makedirs(pasta_mes_inicio, exist_ok=True)

        pasta_dia_inicio = os.path.join(pasta_mes_inicio, f'{dia_inicio}-{mes_inicio}-{ano_inicio}')
        os.makedirs(pasta_dia_inicio, exist_ok=True)

        pasta_camera = os.path.join(pasta_dia_inicio, f'CAMERA {camera}')
        os.makedirs(pasta_camera, exist_ok=True)

        destino = os.path.join(pasta_camera, nome_arquivo)
        
        if os.path.exists(destino):
            print(f"Arquivo '{nome_arquivo}' enviado para a pasta de revisão.")
            destino_revisar = os.path.join(caminho_base, 'REVISAR', nome_arquivo)
            os.makedirs(os.path.dirname(destino_revisar), exist_ok=True)
            shutil.move(origem, destino_revisar)
            return
        
        shutil.move(origem, destino)
        print(f"Arquivo {nome_arquivo} movido para a pasta correspondente.")
    else:
        print(f"Nome de arquivo {nome_arquivo} não corresponde ao padrão esperado. Movendo para a pasta 'REVISAR'.")
        destino_revisar = os.path.join(caminho_base, 'REVISAR', nome_arquivo)
        os.makedirs(os.path.dirname(destino_revisar), exist_ok=True)
        shutil.move(origem, destino_revisar)

# Especifique o caminho da pasta base onde a estrutura será criada
caminho_base = r'F:'

# Pasta onde os arquivos estão localizados
pasta_arquivos = r'F:\20233'

total_arquivos_por_mes = {}
total_arquivos_por_dia = {}
total_arquivos_por_camera = {}

# Abre o arquivo de log para escrita
with open('log.txt', 'w') as log_file:
    # Redireciona a saída padrão para o arquivo de log
    original_stdout = sys.stdout
    sys.stdout = log_file

    for diretorio_raiz, _, arquivos in os.walk(pasta_arquivos):
        for nome_arquivo in arquivos:
            print(f"Nome do arquivo: {nome_arquivo}")
            origem = os.path.join(diretorio_raiz, nome_arquivo)  # Caminho absoluto do arquivo de origem
            criar_estrutura_de_pastas(caminho_base, nome_arquivo, origem)

            camera, _, mes, dia, _, _, _ = extrair_camera_e_datas_do_nome_arquivo(nome_arquivo)
            if camera:
                total_arquivos_por_mes[mes] = total_arquivos_por_mes.get(mes, 0) + 1
                total_arquivos_por_dia[dia] = total_arquivos_por_dia.get(dia, 0) + 1
                total_arquivos_por_camera[camera] = total_arquivos_por_camera.get(camera, 0) + 1
# ...

# O restante do código permanece o mesmo para a geração de logs


    # Redireciona a saída padrão de volta ao console
    sys.stdout = original_stdout

# Abre novamente o arquivo de log para leitura e exibe seu conteúdo no console
with open('log.txt', 'r') as log_file:
    print(log_file.read())

# Gera o log de quantidade de arquivos por mês, dia e câmera no arquivo de log
with open('log.txt', 'a') as log_file:
    log_file.write("\nQuantidade de arquivos por mês:\n")
    for mes, total in total_arquivos_por_mes.items():
        log_file.write(f"{mes}: {total} arquivos\n")

    log_file.write("\nQuantidade de arquivos por dia:\n")
    for dia, total in total_arquivos_por_dia.items():
        log_file.write(f"{dia}: {total} arquivos\n")

    log_file.write("\nQuantidade de arquivos por câmera:\n")
    for camera, total in total_arquivos_por_camera.items():
        log_file.write(f"Câmera {camera}: {total} arquivos\n")
