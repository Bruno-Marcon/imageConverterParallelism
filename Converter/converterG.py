import os
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image

def selecionar_pasta_origem():
    global pasta_origem
    pasta_origem = filedialog.askdirectory()
    label_pasta_origem.config(text=f'Pasta de Origem: {pasta_origem}')

def selecionar_pasta_destino():
    global pasta_destino_principal
    pasta_destino_principal = filedialog.askdirectory()
    label_pasta_destino.config(text=f'Pasta de Destino: {pasta_destino_principal}')

def converter_imagens():
    if not os.path.exists(pasta_destino_principal):
        status_label.config(text=f"A pasta de destino principal '{pasta_destino_principal}' não existe ou não é acessível.")
        return

    data_hora_atual = datetime.datetime.now()
    nome_pasta_destino = data_hora_atual.strftime("%Y-%m-%d_%H-%M-%S")
    pasta_destino = os.path.join(pasta_destino_principal, nome_pasta_destino)

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    start_time = datetime.datetime.now()
    formato_origem = formato_origem_combobox.get()
    formato_destino = formato_destino_combobox.get()
    for arquivo in os.listdir(pasta_origem):
        if arquivo.endswith(f'.{formato_origem}'):
            caminho_completo_origem = os.path.join(pasta_origem, arquivo)
            nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
            caminho_completo_destino = os.path.join(pasta_destino, f'{nome_arquivo_sem_extensao}.{formato_destino}')
            imagem = Image.open(caminho_completo_origem)
            imagem = imagem.convert('RGB')
            imagem.save(caminho_completo_destino, formato_destino)

            status_label.config(text=f'Convertendo: {arquivo} para {nome_arquivo_sem_extensao}.{formato_destino}')

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    status_label.config(text=f'Conversão concluída em {elapsed_time.total_seconds():.2f} segundos.')

# Configuração da janela principal
root = tk.Tk()
root.title('Conversor de Imagens')
root.geometry('500x400')

# Crie um estilo com uma aparência mais limpa
style = ttk.Style()
style.theme_use('clam')

# Labels para exibir informações
label_pasta_origem = tk.Label(root, text='Pasta de Origem: Nenhuma pasta selecionada')
label_pasta_destino = tk.Label(root, text='Pasta de Destino: Nenhuma pasta selecionada')
status_label = tk.Label(root, text='Aguardando conversão...')

label_pasta_origem.pack(pady=10)
label_pasta_destino.pack(pady=10)
status_label.pack(pady=10)

# Comboboxes para escolher os formatos de origem e destino
formatos_disponiveis = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'CR2']  # Adicione outros formatos, se necessário
formato_origem_combobox = ttk.Combobox(root, values=formatos_disponiveis)
formato_destino_combobox = ttk.Combobox(root, values=formatos_disponiveis)

formato_origem_combobox.set('png')  # Formato de origem padrão
formato_destino_combobox.set('jpg')  # Formato de destino padrão

formato_origem_combobox.pack(pady=10)
formato_destino_combobox.pack(pady=10)

# Botões para seleção de pastas e início da conversão
btn_selecionar_origem = ttk.Button(root, text='Selecionar Pasta de Origem', command=selecionar_pasta_origem)
btn_selecionar_destino = ttk.Button(root, text='Selecionar Pasta de Destino', command=selecionar_pasta_destino)
btn_converter = ttk.Button(root, text='Converter Imagens', command=converter_imagens)

btn_selecionar_origem.pack(pady=10)
btn_selecionar_destino.pack(pady=10)
btn_converter.pack(pady=10)

root.mainloop()
