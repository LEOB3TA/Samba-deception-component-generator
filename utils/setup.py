import subprocess
import os

def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)
        print(f'Utente "{username}" creato con successo.')
    except subprocess.CalledProcessError as e:
       print(f'Errore durante la creazione dell\'utente: {e}')

def makeFS(type):
    # questp è stato messo qui per creare la cartella della base path perchèà deve esistere, non è detto che serva dipende da dove condivide samba
    # Specify the path for the new folder
    base_path = '/path/to/your/base_folder'

    # Use the os.makedirs() function to create the folder along with any necessary parent folders
    os.makedirs(base_path)

    print(f"Folder '{base_path}' created successfully.")
    # TODO capire quel è la cartella dove samba condivide

    # Specify the user folders
    user_folders = ['Documents', 'Pictures', 'Downloads', 'Desktop']
    for folder in user_folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    if type=="home":

        # Create the full path by joining the base path with the nested folders
        full_path = os.path.join(base_path, *user_folders)

        # Use os.makedirs() to create the nested folder structure
        os.makedirs(full_path)

        print(f"Folder structure '{full_path}' created successfully.")



# Sostituisci 'nuovo_utente' e 'nuova_password' con i valori desiderati
new_username = 'nuovo_utente'
new_password = 'nuova_password'

create_user(new_username, new_password)