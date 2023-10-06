from PIL import Image
import os
import datetime
import concurrent.futures
import numpy as np
import time

def converter_arquivo(caminho_origem, caminho_destino):
    imagem = Image.open(caminho_origem)
    imagem.save(caminho_destino, 'JPEG')

pasta_origem = os.path.expanduser('~/Desktop/imagenscr2')
pasta_destino_principal = 'I:\\Hospital Salvatoriano Divino Salvador\\Crachás\\Convertidas'


if not os.path.exists(pasta_destino_principal):
    print(f"A pasta de destino principal '{pasta_destino_principal}' não existe ou não é acessível.")
else:
    tempo_inicio = time.time()

    data_hora_atual = datetime.datetime.now()
    nome_pasta_destino = data_hora_atual.strftime("%Y-%m-%d_%H-%M-%S")
    pasta_destino = os.path.join(pasta_destino_principal, nome_pasta_destino)
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    arquivos_a_converter = [arquivo for arquivo in os.listdir(pasta_origem) if arquivo.endswith('.CR2')]
    num_processos = min(4, len(arquivos_a_converter))
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processos) as executor:
        for arquivo in arquivos_a_converter:
            caminho_completo_origem = os.path.join(pasta_origem, arquivo)
            nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
            caminho_completo_destino = os.path.join(pasta_destino, f'{nome_arquivo_sem_extensao}.jpg')
            executor.submit(converter_arquivo, caminho_completo_origem, caminho_completo_destino)
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio

    print(f'Conversão concluída em {tempo_total:.2f} segundos.')
