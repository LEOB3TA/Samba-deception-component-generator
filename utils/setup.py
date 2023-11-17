import subprocess
import random


def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)
        subprocess.run(['sudo', 'smbpasswd', '-a', '-p', password, username], check=True)
        print(f'Utente "{username}" creato con successo.')
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione dell\'utente: {e}')


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