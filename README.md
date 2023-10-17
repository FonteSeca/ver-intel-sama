# Organizador de Gravações da Câmera Intelbras DVR

O script `organiza.py` automatiza a organização de gravações provenientes da câmera Intelbras DVR. Ele cria uma estrutura de pastas intuitiva e fácil de navegar para as gravações.

## Como Funciona

1. A variável `caminho_base` deve ser configurada para o caminho onde a estrutura das pastas será criada.
2. A variável `pasta_arquivos` deve ser configurada para o caminho onde estão todas as gravações.

**Nota:** Este script funciona apenas para gravações que seguem o formato de nomeação: `MHDX_ch12_main_YYYYMMDDHHMMSS_YYYYMMDDHHMMSS`.

## Estrutura de Pastas

A estrutura de pastas criada pelo script é a seguinte:

- `ANO`
  - `MÊS - ANO`
    - `DIA - MÊS - ANO`
      - `CÂMERA`

Esta organização facilita a busca e o acesso às gravações conforme necessário.

## Como Usar

1. Configure os caminhos das variáveis `caminho_base` e `pasta_arquivos`.
2. Execute o script.

# Verificador de Gravações da Câmera Intelbras DVR

O script `verifica_cameras.py` percorre cada pasta e subpasta do diretório de gravações, identificando as câmeras e os dias em que foram feitas as gravações. Ele fornece informações sobre o horário de início e término das gravações, e também identifica e registra quaisquer arquivos corrompidos.

## Como Funciona

1. O script percorre recursivamente cada pasta e subpasta.
2. Identifica as câmeras e os dias em que foram feitas as gravações.
3. Registra o horário de início e término das gravações.
4. Identifica e registra arquivos corrompidos.

## Variáveis para Alterar

- `caminhos_bases`: Lista de caminhos que o script irá percorrer.
- `caminho_arquivo_csv`: Caminho onde o arquivo CSV será gerado.

## Formato do CSV

O script gera um arquivo CSV que inclui as seguintes informações:

- Nome da Câmera
- Data da Gravação
- Horário de Início
- Horário de Término
- Status (Normal ou Corrompido)

## Como Usar

1. Certifique-se de ter executado o script `organiza.py` previamente.
2. Configure as variáveis `caminhos_bases` e `caminho_arquivo_csv`.
3. Execute o script `verifica_cameras.py`.
