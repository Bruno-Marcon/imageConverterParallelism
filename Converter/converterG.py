import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
import datetime
import concurrent.futures

def converter_arquivo(caminho_origem, caminho_destino, largura_alvo):
    imagem = Image.open(caminho_origem)
    largura_original, altura_original = imagem.size

    nova_altura = int(largura_alvo * (altura_original / largura_original))

    imagem = imagem.resize((largura_alvo, nova_altura), Image.ANTIALIAS)
    imagem.save(caminho_destino, 'JPEG')

def iniciar_conversao():
    pasta_origem = pasta_origem_var.get()
    pasta_destino_principal = pasta_destino_var.get()

    if not os.path.exists(pasta_origem):
        resultado_label.config(text=f"A pasta de origem '{pasta_origem}' não existe ou não é acessível.")
    elif not os.path.exists(pasta_destino_principal):
        resultado_label.config(text=f"A pasta de destino principal '{pasta_destino_principal}' não existe ou não é acessível.")
    else:
        tempo_inicio = datetime.datetime.now()

        data_hora_atual = tempo_inicio.strftime("%Y-%m-%d_%H-%M-%S")
        pasta_destino = os.path.join(pasta_destino_principal, data_hora_atual)

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        arquivos_a_converter = [arquivo for arquivo in os.listdir(pasta_origem) if arquivo.endswith('.CR2')]
        
        num_threads = min(4, len(arquivos_a_converter))

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            for arquivo in arquivos_a_converter:
                caminho_completo_origem = os.path.join(pasta_origem, arquivo)
                nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
                caminho_completo_destino = os.path.join(pasta_destino, f'{nome_arquivo_sem_extensao}.jpg')

                largura_alvo = 1280
                executor.submit(converter_arquivo, caminho_completo_origem, caminho_completo_destino, largura_alvo)

        tempo_fim = datetime.datetime.now()
        tempo_total = tempo_fim - tempo_inicio

        resultado_label.config(text=f'Conversão concluída em {tempo_total}.')
        resultado_label.update()

root = tk.Tk()
root.title("Conversor de Imagens")
root.geometry("400x250")

pasta_origem_var = tk.StringVar()
pasta_destino_var = tk.StringVar()

tk.Label(root, text="Pasta de origem:").pack()
tk.Entry(root, textvariable=pasta_origem_var).pack()
tk.Button(root, text="Selecionar pasta", command=lambda: pasta_origem_var.set(filedialog.askdirectory())).pack()

tk.Label(root, text="Pasta de destino:").pack()
tk.Entry(root, textvariable=pasta_destino_var).pack()
tk.Button(root, text="Selecionar pasta", command=lambda: pasta_destino_var.set(filedialog.askdirectory())).pack()

tk.Button(root, text="Iniciar Conversão", command=iniciar_conversao).pack()

resultado_label = tk.Label(root, text="")
resultado_label.pack()

root.mainloop()
