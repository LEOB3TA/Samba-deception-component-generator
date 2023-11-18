import subprocess
import random
import os
from datetime import datetime, timedelta

users = []

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
        'semicolon', 'colon', 'create', 'inspire', 'imagine', 'explore', 'discover',
        'treasure', 'dream', 'believe', 'achieve', 'celebrate', 'challenge', 'effort',
        'focus', 'persevere', 'progress', 'mindfully', 'gratefully', 'kindly', 'forgive',
        'compassionately', 'courageously', 'strength', 'patiently', 'wisdom', 'knowledge',
        'learn', 'teach', 'grow', 'expand', 'innovate', 'evolve', 'change', 'transform',
        'balance', 'harmony', 'connect', 'communicate', 'collaborate', 'community', 'together',
        'support', 'embrace', 'kindred', 'soul', 'heart', 'spirit', 'nature', 'semicolon',
        'colon', 'create', 'inspire', 'imagine', 'explore', 'discover', 'treasure', 'dream',
        'believe', 'achieve', 'celebrate', 'challenge', 'effort', 'focus', 'persevere',
        'progress', 'mindfully', 'gratefully', 'kindly', 'forgive', 'compassionately',
        'courageously', 'strength', 'patiently', 'wisdom', 'knowledge', 'learn', 'teach',
        'grow', 'expand', 'innovate', 'evolve', 'change', 'transform', 'balance', 'harmony',
        'connect', 'communicate', 'collaborate', 'community', 'together', 'support', 'embrace',
        'kindred', 'soul', 'heart', 'spirit', 'nature', 'semicolon', 'colon'
    ]
    sentence = ' '.join(random.choice(words) + random.choice(['', ',', ';', ':']) for _ in range(num_words))
    return sentence.capitalize() + '.'

# Creates num_file files with a random dimension beetween dim_min and dim_max using generate_random_sentence with a random name
def create_files(dim_min, dim_max, num_file):
    wordlist = ['pwd', 'password', 'Password', 'myFile', 'my_file', 'note', 'file', 'File', 'secret',
                'document', 'confidential', 'private', 'backup', 'important', 'data', 'access', 'admin',
                'login', 'username', 'security', 'top_secret', 'classified', 'sensitive', 'confidential_info',
                'john', 'mary', 'bob', 'alice', 'steve', 'jane', 'mark', 'sara', 'david', 'emily', 'chiara',
                'project', 'report', 'draft', 'memo', 'info', 'key', 'code', 'account', 'profile', 'log',
                'archive', 'client_list', 'employee_info', 'finance', 'budget', 'meeting_notes', 'agenda',
                'presentation', 'proposal', 'contract', 'invoice', 'receipt', 'schedule', 'calendar', 'task_list',
                'reminder', 'reminder_list', 'team_notes', 'survey', 'feedback', 'survey_results', 'analysis',
                'research', 'survey_data', 'survey_responses', 'policy', 'procedure', 'manual', 'guide', 'instructions',
                'training_material', 'tutorial', 'user_guide', 'setup_guide', 'config', 'configuration', 'settings',
                'setup_info', 'install_guide', 'release_notes', 'version_info', 'update', 'patch', 'bug_report',
                'issue_log', 'error_log', 'debug_info', 'test_data', 'test_cases', 'test_results', 'bug_fixes',
                'improvements', 'enhancements', 'feature_request', 'wishlist', 'roadmap', 'milestones']
    for _ in range(num_file):
        file_dim = random.uniform(dim_min, dim_max)
        current_datetime = datetime.now()
        random_offset = random.randint(0, 1825)  # 5 years
        formatted_datetime = (current_datetime - timedelta(days=random_offset)).strftime("%Y%m%d")
        nome = random.choice(wordlist)
        nome_file = f"{nome}_{formatted_datetime}.txt"
        with open(nome_file, "w") as file:
            num_words = random.randint(5, 15)  # Random number of words per sentence
            num_sentences = int((file_dim * 1000000) / (num_words * 5))  # Assuming average word length of 5 characters

            for _ in range(num_sentences):
                sentence = generate_random_sentence(num_words) + '\n'
                file.write(sentence)
    return

# create user in the system and add it to samba users
def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['useradd', '-m', '-p', password, username], check=True)
        command = f'(echo "{password}"; echo "{password}")  | smbpasswd -s -a "{username}"'
        subprocess.run(command, shell=True, check=True)
        print(f'Utente "{username}" created.')
        users.append(username)
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione dell\'utente: {e}')


def convert_to_word(input_file, output_file):
    subprocess.run(["pandoc", input_file, "-o", output_file])


def convert_to_pdf(input_file, output_file):
    subprocess.run(["pandoc", input_file, "-o", output_file])


def create_and_populate_folder(base_path,folder):
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
    os.chdir(folder_path)
    random_files_number = random.randint(0, 10)
    create_files(0.0001, 0.1, random_files_number)  # DON'T CHANGE THE DIMENSIONS
    txt_files = [file for file in os.listdir(folder_path)]
    random_number = random.randint(0, len(txt_files))
    txt_files_word = txt_files[:random_number]
    txt_files_pdf = txt_files[random_number:]

    for input_file in txt_files_word:
        output_file = os.path.splitext(input_file)[0] + ".docx"
        convert_to_word(input_file, output_file)

    for input_file in txt_files_pdf:
        output_file = os.path.splitext(input_file)[0] + ".pdf"
        convert_to_pdf(input_file, output_file)
    for file in txt_files:
        os.remove(file)
    print(f"{folder_path} populated with files")
    os.chdir(base_path)

def make_fs(type):
    base_path = '/sambashare'
    os.mkdir(base_path)

    if type == "public" or "both":
        public_folders = ['Public', 'Public/Shared_Documents', 'Public/Shared_Pictures']
        for folder in public_folders:
            create_and_populate_folder(base_path,folder)
    if type == "private" or "both":
        for user in users:
            base_user_path = os.path.join(base_path, user)
            # Specify the user folders
            user_folders = ['Documents', 'Documents/personal/', 'Documents/personal/lawyer',
                            'Documents/personal/family',
                            'Documents/work/', 'Documents/work/projects', 'Pictures', 'Downloads',
                            'Downloads/important_documents', 'Desktop', 'Desktop/trash', 'Desktop/work']
            for folder in user_folders:
                create_and_populate_folder(base_user_path,folder)
