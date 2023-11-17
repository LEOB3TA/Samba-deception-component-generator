import subprocess
import random
import os
from datetime import datetime


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


def create_files(dim_min, dim_max, num_file):
    for _ in range(num_file):
        file_dim = random.uniform(dim_min, dim_max)
        file_dim_str = str(file_dim)
        file_round_dim_str = file_dim_str
        if file_dim_str.find('.') != -1:
            file_round_dim_str = file_dim_str[:file_dim_str.find('.')]
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d_%S")
        nome_file = f"{formatted_datetime}_{file_round_dim_str}MB.txt"
        print(nome_file)

        with open(nome_file, "w") as file:
            num_words = random.randint(5, 15)  # Random number of words per sentence
            num_sentences = int((file_dim * 1000000) / (num_words * 5))  # Assuming average word length of 5 characters

            for _ in range(num_sentences):
                sentence = generate_random_sentence(num_words) + '\n'
                file.write(sentence)
    return

def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)
        subprocess.run(['sudo', 'smbpasswd', '-a', '-p', password, username], check=True)
        print(f'Utente "{username}" creato con successo.')
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione dell\'utente: {e}')




def convert_to_word(input_file, output_file):
    subprocess.run(["pandoc", input_file, "-o", output_file, "--to=docx"])

def convert_to_pdf(input_file, output_file):
    subprocess.run(["pandoc", input_file, "-o", output_file, "--to=pdf"])


def makeFS():
    # questp è stato messo qui per creare la cartella della base path perchèà deve esistere, non è detto che serva dipende da dove condivide samba
    # Specify the path for the new folder
    base_path = '/Users/leo/try/prova'

    # Use the os.makedirs() function to create the folder along with any necessary parent folders
    os.makedirs(base_path)

    print(f"Folder '{base_path}' created successfully.")
    # TODO capire quel è la cartella dove samba condivide

    # Specify the user folders
    user_folders = ['Documents', 'Pictures', 'Downloads', 'Desktop', 'Public']
    for folder in user_folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
        os.chdir(folder_path)
        create_files(0.1, 10, 20)
        txt_files = [file for file in folder_path if file.endswith(".txt")]
        # Divide la lista di file a metà
        half_count = len(txt_files) // 2
        txt_files_word = txt_files[:half_count]
        txt_files_pdf = txt_files[half_count:]

        for input_file in txt_files_word:
            output_file = os.path.splitext(input_file)[0] + ".docx"
            convert_to_word(input_file, output_file)
            print(f"Convertito {input_file} in {output_file}")

        for input_file in txt_files_pdf:
            output_file = os.path.splitext(input_file)[0] + ".pdf"
            convert_to_pdf(input_file, output_file)
            print(f"Convertito {input_file} in {output_file}")
        os.chdir(base_path)


# Sostituisci 'nuovo_utente' e 'nuova_password' con i valori desiderati
# new_username = 'nuovo_utente'
# new_password = 'nuova_password'

# create_user(new_username, new_password)
