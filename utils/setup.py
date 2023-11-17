import subprocess
import random
import os


def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)
        subprocess.run(['sudo', 'smbpasswd', '-a', '-p', password, username], check=True)
        print(f'Utente "{username}" creato con successo.')
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione dell\'utente: {e}')


def makeFS(type):
    # questo è stato messo qui per creare la cartella della base path perché deve esistere, non è detto che serva, ma
    # dipende da dove condivide SAMBA
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
    if type == "home":
        # Create the full path by joining the base path with the nested folders
        full_path = os.path.join(base_path, *user_folders)

        # Use os.makedirs() to create the nested folder structure
        os.makedirs(full_path)

        print(f"Folder structure '{full_path}' created successfully.")


def generate_random_sentence(num_words):
    words = [
        'apple', 'banana', 'orange', 'grape', 'kiwi', 'python', 'programming',
        'random', 'file', 'dimension', 'dog', 'cat', 'house', 'car', 'beach',
        'computer', 'cloud', 'flower', 'mountain', 'ocean', 'sun', 'moon',
        'rainbow', 'coffee', 'book', 'music', 'dance', 'happy', 'friend',
        'journey', 'adventure', 'love', 'peace', 'smile', 'laughter', 'family',
        'holiday', 'vacation', 'explore', 'discover', 'treasure', 'magic',
        'wonder', 'secret', 'fantasy', 'imagination', 'create', 'inspire',
        'dream', 'believe', 'achieve', 'success', 'victory', 'celebrate',
        'challenge', 'effort', 'energy', 'focus', 'persevere', 'progress',
        'mindful', 'grateful', 'kindness', 'forgive', 'compassion', 'courage',
        'strength', 'patience', 'wisdom', 'knowledge', 'learn', 'teach', 'grow',
        'expansion', 'innovation', 'evolve', 'change', 'transform', 'balance',
        'harmony', 'connect', 'communicate', 'collaborate', 'community', 'together',
        'support', 'embrace', 'kindred', 'soul', 'heart', 'spirit', 'nature',
        'semicolon', 'colon'
    ]
    sentence = ' '.join(random.choice(words) + random.choice(['', ',', ';', ':']) for _ in range(num_words))
    return sentence.capitalize() + '.'


def create_files(dimMin, dimMax, numFile):
    for _ in range(numFile):
        dimA = str(random.uniform(dimMin, dimMax))
        nomeFile = f"file{dimA}.txt"  # TODO acpire come arrotorndare il nome

        with open(nomeFile, "w") as file:
            dim = random.uniform(dimMin, dimMax)
            numWords = random.randint(5, 15)  # Random number of words per sentence
            numSentences = int((dim * 1000000) / (numWords * 5))  # Assuming average word length of 5 characters

            for _ in range(numSentences):
                sentence = generate_random_sentence(numWords) + '\\n'
                file.write(sentence)

    def convert_file(input_file, output_file):
        subprocess.run(['pandoc', input_file, '-o', output_file])
        print(f'File "{input_file}" converted to "{output_file}" successfully.')

# Sostituisci 'nuovo_utente' e 'nuova_password' con i valori desiderati
# new_username = 'nuovo_utente'
# new_password = 'nuova_password'

# create_user(new_username, new_password)
