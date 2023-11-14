import subprocess

def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)
        print(f'Utente "{username}" creato con successo.')
    except subprocess.CalledProcessError as e:
       print(f'Errore durante la creazione dell\'utente: {e}')

# Sostituisci 'nuovo_utente' e 'nuova_password' con i valori desiderati
new_username = 'nuovo_utente'
new_password = 'nuova_password'

create_user(new_username, new_password)