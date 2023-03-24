import tkinter as tk
from tkinter import *
from tkinter import filedialog
import customtkinter as cTK
import shutil
from send2trash import send2trash
from PIL import ImageTk, Image
import os


def check_dir(one):
    global img_numb
    global img_list
    global location
    global folders_list

    img_numb = 0
    img_list = []

    # Depois da primeira vez que checa, atualiza a barra de status.
    if one == 1:
        status = Label(root, text='Checando arquivos novamente...  ',
                       bd=1, relief=SUNKEN, anchor=E, bg='#282424', fg='white')
        status.grid(row=6, column=0, columnspan=3, sticky=W+E)

        create_folders(1)

        status = Label(root, text='Arquivos checados!  ', bd=1,
                       relief=SUNKEN, anchor=E, fg='green', bg='#282424')
        status.grid(row=6, column=0, columnspan=3, sticky=W+E)

    pasta = os.listdir(location)

    # create a list of dir with just archives, but in chronological order
    dir_list = os.chdir(location)
    dir_list = sorted(filter(os.path.isfile, os.listdir('.')),
                      key=os.path.getmtime)

    # Monta o caminho delas
    folders_list = []

    for folder_path in pasta:
        if os.path.isdir(os.path.join(location, folder_path)):
            folders_list.append(folder_path)

    # imagens
    img_count = 0

    for item in dir_list:
        # Checa se o aqruivo termina em mp4, png ou jpeg
        if item.endswith('.jpg') or item.endswith('.png') or item.endswith('.jpeg'):
            # Se tem, cria o caminho pro item
            img_path = os.path.join(location + '\\' + item)
            img_count += 1

            # append the path to a list of paths
            img_list.append(img_path)


def lugar(path):
    global location
    welcome_root.destroy()
    location = path
    check_dir(0)


# proxima imagem
def proxima(self):
    global exibir
    global img_numb

    # deleta a imagem antiga
    exibir.grid_forget()

    # adiciona um ao contador de imagens
    global img_numb
    img_numb = img_numb + 1

    # para na última imagem
    if img_numb == len(img_list):
        img_numb = len(img_list) - 1

    # mostra a próxima imagem
    exibir_path = img_list[img_numb]

    im = Image.open(exibir_path).resize((550, 450))
    ph = ImageTk.PhotoImage(im)
    exibir = Label(root, image=ph, bg='black')
    exibir.image = ph
    exibir.grid(row=0, column=0, columnspan=3)

    if img_numb + 1 == 69:
        status = Label(root, text='hahah imagem 69 sexo haha ',
                       bd=1, relief=SUNKEN, anchor=E, bg='#282424', fg='pink')
        status.grid(row=6, column=0, columnspan=3, sticky=W+E)

    else:
        status = Label(root, text='Imagem número ' + str(img_numb+1),
                       bd=1, relief=SUNKEN, anchor=E, bg='#282424', fg='white')
        status.grid(row=6, column=0, columnspan=3, sticky=W+E)

# Imagem Anterior


def anterior(self):
    global exibir
    global img_numb

    # deleta a imagem antiga
    exibir.grid_forget()

    # adiciona um ao contador de imagens
    global img_numb
    img_numb = img_numb - 1

    # se a imagem chegar na primeira, ela para lá
    if img_numb <= 0:
        img_numb = 0

    # mostra a próxima imagem
    exibir_path = img_list[img_numb]

    im = Image.open(exibir_path).resize((550, 450))
    ph = ImageTk.PhotoImage(im)
    exibir = Label(root, image=ph, bg='black')
    exibir.image = ph
    exibir.grid(row=0, column=0, columnspan=3)

    # Altera o status
    status = Label(root, text='Imagem número ' + str(img_numb+1),
                   bd=1, relief=SUNKEN, anchor=E, bg='#282424', fg='white')
    status.grid(row=6, column=0, columnspan=3, sticky=W+E)

    if img_numb + 1 == 69:
        status = Label(root, text='hahah imagem 69 sexo haha ',
                       bd=1, relief=SUNKEN, anchor=E, bg='#282424', fg='pink')
        status.grid(row=6, column=0, columnspan=3, sticky=W+E)

# Cria um novo diretório


def create_dir():

    new_dir_name = dir_name.get()

    os.mkdir(new_dir_name)

    status = Label(root, text='Pasta "' + new_dir_name + '" Criada!  ', bd=1,
                   relief=SUNKEN, anchor=E, fg='Green', bg='#282424')
    status.grid(row=6, column=0, columnspan=3, sticky=W+E)


# Re nomeia a foto
def rename_file():

    file_name = dir_name.get()
    os.rename(img_list[img_numb], file_name + '.png')
    img_list[img_numb] = file_name + '.png'

    status = Label(root, text='Imagem renomeada!  ', bd=1,
                   relief=SUNKEN, anchor=E, fg='Green', bg='#282424')
    status.grid(row=6, column=0, columnspan=3, sticky=W+E)


# Move a imagem ( o principal lol )
def move_image(path):

    # img_list = list of paths of the images, move path is passed by the folder button, it just tells the moving path
    move_path = path + '/' + os.path.basename(img_list[img_numb])
    shutil.move(img_list[img_numb], move_path)

    status = Label(root, text='Imagem Movida!  ', bd=1,
                   relief=SUNKEN, anchor=E, fg='Green', bg='#282424')
    status.grid(row=6, column=0, columnspan=3, sticky=W+E)

    proxima('')


# Apaga um arquivo
def delete():
    def confirm():
        global delete_button
        send2trash(img_list[img_numb])

        status = Label(root, text='Imagem Apagada.  ', bd=1,
                       relief=SUNKEN, anchor=E, fg='Red', bg='#282424')
        status.grid(row=6, column=0, columnspan=3, sticky=W+E)

        delete_button.grid_forget()
        delete_button = cTK.CTkButton(root, text='Apagar',
                                      fg_color='#0E8388', command=delete, text_color='Black', width=10)
        delete_button.grid(row=2, column=2)
        check_dir(1)
        proxima('')

    global delete_button
    delete_button.grid_forget()

    delete_button = cTK.CTkButton(root, text='Certeza?',
                                  fg_color='Red', command=confirm, text_color='Black', width=10)
    delete_button.grid(row=2, column=2)


def fechar(ss):
    root.quit()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  WELCOME ROOT
saved_paths = []
welcome_root = cTK.CTk()
welcome_root.title('File Organizer, Bem Vindo!')

# Mensagem Bem Vindo
welcome_msg = cTK.CTkLabel(
    master=welcome_root, text="Bem Vindo! \n Escolha um dos caminhos para começar, ou crie um novo!", font=('Comic Sans MS', 15))
welcome_msg.grid(row=0, column=0)


def delete_folders():
    try:
        os.remove('save.txt')
        welcome_root.quit()

    except:
        raise Exception('Arquivo nao existe!')


def folder_buttons():

    if len(saved_paths) > 0:
        folder_button1 = cTK.CTkButton(
            master=welcome_root, text=saved_paths[0], command=lambda: lugar(saved_paths[0]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))

        folder_button1.grid(row=2, column=0, pady=5)

    if len(saved_paths) > 1:
        folder_button2 = cTK.CTkButton(
            master=welcome_root, text=saved_paths[1], command=lambda: lugar(saved_paths[1]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))

        folder_button2.grid(row=3, column=0, pady=5)

    if len(saved_paths) > 2:
        folder_button3 = cTK.CTkButton(
            master=welcome_root, text=saved_paths[2], command=lambda: lugar(saved_paths[2]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))

        folder_button3.grid(row=4, column=0, pady=5)

    if len(saved_paths) > 3:
        folder_button4 = cTK.CTkButton(
            master=welcome_root, text=saved_paths[3], command=lambda: lugar(saved_paths[3]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))

        folder_button4.grid(row=5, column=0, pady=5)

    if len(saved_paths) > 4:
        folder_button5 = cTK.CTkButton(
            master=welcome_root, text=saved_paths[4], command=lambda: lugar(saved_paths[4]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))

        folder_button5.grid(row=6, column=0, pady=5)

    if len(saved_paths) > 5:
        folder_button6 = cTK.CTkButton(
            master=welcome_root, text=saved_paths[5], command=lambda: lugar(saved_paths[5]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))

        folder_button6.grid(row=7, column=0, pady=5)

# Apagar botões


delete_button = cTK.CTkButton(master=welcome_root, text="Apagar Pastas (reinicia o programa)",
                              command=delete_folders, fg_color='#2E4F4F', text_color='Black')
delete_button.grid(row=8, column=0, pady=5)

# CHECA SE O ARQUIVO SAVE.TXT EXISTE NO CAMINHO, SE SIM, ELE ABRE ELE
if os.path.isfile('save.txt'):

    with open('save.txt', 'r') as f:

        save_file = f.read()
        save_file = save_file.split(',')
        saved_paths = [x for x in save_file if x.strip()]
        folder_buttons()

# ADICIONAR O BOTAO PRA ACESSAR A PASTA PRIMÁRIA NO WELCOME ROOT


def add_folder():
    global saved_paths

    add = tk.filedialog.askdirectory(
        initialdir='/', title='Escolha uma pasta principal')

    saved_paths.append(add)

    with open('save.txt', 'w') as f:
        for path in saved_paths:
            f.write(path + ',')

    folder_buttons()


# Botão pra adicionar a pasta
add_path = cTK.CTkButton(welcome_root, text='Adicionar Caminho',
                         fg_color='#0E8388', command=add_folder, text_color='Black', width=10)
add_path.grid(row=1, column=0, pady=10)

welcome_root.mainloop()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ROOT PRINCIPAL
root = cTK.CTk()
root.title('File Organizer 2023 100%% atualizado')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure((0, 1, 2), weight=1)


# Botões

# Recarrega a lista de imagens
refresh = cTK.CTkButton(master=root, text='Refresh',
                        command=lambda: check_dir(1), fg_color='#0E8388', text_color='Black', width=10)
refresh.grid(row=2, column=1)

# Fechar

delete_button = cTK.CTkButton(root, text='Apagar',
                              fg_color='#0E8388', command=delete, text_color='Black', width=10)
delete_button.grid(row=2, column=2)

# proximo
next = cTK.CTkButton(master=root, text='Proxima >>', command=lambda: proxima(
    ''), fg_color='#bad1cd', text_color='Black', width=10)
next.grid(row=1, column=2)

# Anterior
previous = cTK.CTkButton(master=root, text='<< Anterior',
                         command=lambda: anterior('s'), fg_color='#bad1cd', text_color='Black', width=10)
previous.grid(row=1, column=1)

# Entrada que escreve o nome da nova pasta
dir_name = cTK.CTkEntry(master=root, placeholder_text="Nome da nova pasta... ",
                        width=180, corner_radius=10)
dir_name.grid(row=1, column=0, padx=10, pady=5)

# Criar nova pasta
new_dir = cTK.CTkButton(master=root, text='Nova Pasta',
                        command=create_dir, fg_color='#bad1cd', text_color='Black', width=10)
new_dir.grid(row=3, column=0, pady=8)

# Renomear o arquivo
rename_button = cTK.CTkButton(master=root, text='Re nomear Arquivo',
                              command=rename_file, fg_color='#bad1cd', text_color='Black', width=10)
rename_button.grid(row=2, column=0, pady=5)

# Status
status = Label(root, text='Nada...  ', bd=1, relief=SUNKEN,
               anchor=E, bg='#282424', fg='white')
status.grid(row=6, column=0, columnspan=3, sticky=W+E)

# Atalho desses botões
root.bind('<Right>', proxima)
root.bind('<Left>', anterior)
root.bind('<Escape>', fechar)

# Exibe as imagens
try:
    # Exibe a primeira imagem
    exibir_path = img_list[img_numb]

    im = Image.open(exibir_path).resize((550, 450))
    ph = ImageTk.PhotoImage(im)
    exibir = Label(root, image=ph, bg='black')
    exibir.image = ph
    exibir.grid(row=0, column=0, columnspan=3)

except:
    status = Label(root, text='Nenhuma Imagem encontrada! Reinicie o programa.  ', bd=1, relief=SUNKEN,
                   anchor=E, bg='#282424', fg='Red')
    status.grid(row=6, column=0, columnspan=3, sticky=W+E)

# Pastas "geradas automaticamente"


def create_folders(one):

    if len(folders_list) > 0:
        if len(folders_list[0]) >= 16:
            title1 = folders_list[0][:15] + "..."
        else:
            title1 = folders_list[0]

        pasta1 = cTK.CTkButton(master=root, text=title1, command=lambda: move_image(
            folders_list[0]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta1.grid(row=3, column=1, pady=5)

    if len(folders_list) > 1:
        if len(folders_list[1]) >= 16:
            title2 = folders_list[1][:15] + "..."
        else:
            title2 = folders_list[1]

        pasta2 = cTK.CTkButton(master=root, text=title2, command=lambda: move_image(
            folders_list[1]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta2.grid(row=3, column=2)

    if len(folders_list) > 2:
        if len(folders_list[2]) >= 16:
            title3 = folders_list[2][:15] + "..."
        else:
            title3 = folders_list[2]

        pasta3 = cTK.CTkButton(master=root, text=title3, command=lambda: move_image(
            folders_list[2]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta3.grid(row=4, column=0)

    if len(folders_list) > 3:
        if len(folders_list[3]) >= 16:
            title4 = folders_list[3][:15] + "..."
        else:
            title4 = folders_list[3]

        pasta4 = cTK.CTkButton(master=root, text=title4, command=lambda: move_image(
            folders_list[3]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta4.grid(row=4, column=1, pady=5)

    if len(folders_list) > 4:
        if len(folders_list[4]) >= 16:
            title5 = folders_list[4][:15] + "..."
        else:
            title5 = folders_list[4]

        pasta5 = cTK.CTkButton(master=root, text=title5, command=lambda: move_image(
            folders_list[4]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta5.grid(row=4, column=2)

    if len(folders_list) > 5:
        if len(folders_list[5]) >= 16:
            title6 = folders_list[5][:15] + "..."
        else:
            title6 = folders_list[5]

        pasta6 = cTK.CTkButton(master=root, text=title6, command=lambda: move_image(
            folders_list[5]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta6.grid(row=5, column=0)

    if len(folders_list) > 6:
        if len(folders_list[6]) >= 16:
            title7 = folders_list[6][:15] + "..."
        else:
            title7 = folders_list[6]

        pasta7 = cTK.CTkButton(master=root, text=title7, command=lambda: move_image(
            folders_list[6]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta7.grid(row=5, column=1, pady=5)

    if len(folders_list) > 7:
        if len(folders_list[7]) >= 16:
            title8 = folders_list[7][:15] + "..."
        else:
            title8 = folders_list[7]

        pasta8 = cTK.CTkButton(master=root, text=title8, command=lambda: move_image(
            folders_list[7]), fg_color='#2E4F4F', text_color='Black', width=120, height=40, font=('', 18))
        pasta8.grid(row=5, column=2)

    if one == 1:
        global delete_button

        delete_button.grid_forget()

        delete_button = cTK.CTkButton(root, text='Apagar',
                                      fg_color='#0E8388', command=delete, text_color='Black', width=10)

        delete_button.grid(row=2, column=2)


create_folders(0)
root.mainloop()
