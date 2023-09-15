import os
import csv
from datetime import datetime

def extrair_camera_e_datas_do_nome_arquivo(nome_arquivo, delimitador='_'):
    partes = nome_arquivo.split(delimitador)

    if len(partes) == 5 and partes[1].startswith('ch'):
        camera = partes[1][2:]
        camera = int(camera.zfill(2))
        ano, mes, dia = partes[3][:4], partes[3][4:6], partes[3][6:8]
        hora, minutos, segundos = partes[4][8:10], partes[4][10:12], partes[4][12:14]
        return camera, int(dia), int(mes), int(ano), hora, minutos, segundos
    else:
        return None, None, None, None, None, None, None

# Lista de caminhos para verificar
caminhos_bases = [r'F:\2023', r'H:\2023', r'D:\2023', r'E:\2023']

# Caminho completo para o arquivo CSV
caminho_arquivo_csv = r'C:\CAMERAS\arquivos_camera_2.csv'

# Dicionário para armazenar as informações de status de gravação por câmera, dia e caminho
status_gravacao_por_camera_dia_caminho = {}


# Inicializa o dicionário com as chaves de todas as câmeras
for camera in range(1, 32):
    chave_camera = f"Camera {camera:02d}"
    status_gravacao_por_camera_dia_caminho[chave_camera] = {}

# Percorre os caminhos base
for caminho_base in caminhos_bases:
    for diretorio_raiz, _, arquivos in os.walk(caminho_base):
        for nome_arquivo in arquivos:
            camera, dia, mes, ano, hora, minutos, segundos = extrair_camera_e_datas_do_nome_arquivo(nome_arquivo)
            if camera is not None and 1 <= camera <= 31:
                chave_camera = f"Camera {camera:02d}"
                chave_dia = f"{dia}/{mes:02d}"
                chave_caminho = caminho_base

                if chave_dia not in status_gravacao_por_camera_dia_caminho[chave_camera]:
                    status_gravacao_por_camera_dia_caminho[chave_camera][chave_dia] = {}

                if chave_caminho not in status_gravacao_por_camera_dia_caminho[chave_camera][chave_dia]:
                    status_gravacao_por_camera_dia_caminho[chave_camera][chave_dia][chave_caminho] = "OK"
                    


                tamanho_arquivo = os.path.getsize(os.path.join(diretorio_raiz, nome_arquivo))

                if tamanho_arquivo == 0:
                    status_gravacao_por_camera_dia_caminho[chave_camera][chave_dia][chave_caminho] = "ERRO"


# Cria uma lista com todas as datas únicas
dias_unicos = sorted({chave_dia for chave_camera, dias in status_gravacao_por_camera_dia_caminho.items() for chave_dia in dias.keys()})
# Ordena as datas na lista dias_unicos
dias_unicos.sort(key=lambda data: datetime.strptime(data, "%d/%m"))

# Abre o arquivo CSV em modo de escrita com a codificação correta
with open(caminho_arquivo_csv, 'w', newline='', encoding='utf-8-sig') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)

    # Escreve o cabeçalho
    escritor_csv.writerow(['CAMERAS'] + dias_unicos)

    # Inicializa um dicionário para armazenar os valores encontrados
    valores_por_camera = {}

    # Percorre os caminhos e verifica se o valor para cada chave já foi encontrado
    for caminho_base in caminhos_bases:

        for camera in range(1, 32):
            chave_camera = f"Camera {camera:02d}"

            linha = [chave_camera] + [status_gravacao_por_camera_dia_caminho[chave_camera].get(dia, {}).get(caminho_base, "") for dia in dias_unicos]

            if chave_camera not in valores_por_camera:
                valores_por_camera[chave_camera] = {}

            for idx, valor in enumerate(linha[1:]):
                if valor:
                    if idx not in valores_por_camera[chave_camera]:
                        valores_por_camera[chave_camera][idx] = valor

    # Escreve os valores mesclados no CSV
    for camera, valores in valores_por_camera.items():
        valores_mesclados = [valores.get(idx, "") for idx in range(len(dias_unicos))]
        escritor_csv.writerow([camera] + valores_mesclados)









print("Processo concluído.")
