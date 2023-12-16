import subprocess
import random
import os
import time
from datetime import datetime, timedelta

users = [] 
group_members=[]

def setup_ldap(domain, adminpasswd):
    config_content = f"""[libdefaults]
    default_realm = {domain.upper()}
    dns_lookup_kdc = true
    dns_lookup_realm = false
    """
    with open("/etc/krb5.conf", "w") as krb5_conf:
            krb5_conf.write(config_content)
    subprocess.run("rm -f /etc/samba/smb.conf", shell=True, check=True)
    realm = domain.split(".")[0]
    subprocess.run(f"samba-tool domain provision --realm={domain.upper()} --domain {realm.upper()} --server-role=dc", shell=True, check=True)
    subprocess.run(f'samba-tool user setpassword administrator --newpassword={adminpasswd}', shell=True, check=True)
    subprocess.run('echo "search mydomain.lan\nnameserver 127.0.0.1\n" > /etc/resolv.conf', shell=True, check=True)
    subprocess.run('rm -f /var/lib/samba/private/krb5.conf && ln -s /etc/krb5.conf /var/lib/samba/private/krb5.conf', shell=True, check=True)


def kinit_user(username,password):
    subprocess.run('service winbind stop', shell=True, check=True)
    subprocess.run('service smbd stop', shell=True, check=True)
    subprocess.run('service nmbd stop', shell=True, check=True)
    subprocess.run(f'service samba-ad-dc start', shell=True, check=True)
    time.sleep(2)
    subprocess.run(f'echo {password} | kinit {username}', shell=True, check=True)
    subprocess.run('service samba-ad-dc stop', shell=True, check=True)

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

def add_member(member):
    try:
        group_members.append(member)
    except subprocess.CalledProcessError as e:
        print(f'Errore funzione add_member: {e}')

# create user in the system and add it to samba users
def create_user(username, password,ldap=False):
    try:
        # Creare un nuovo utente
        subprocess.run(['useradd', username], check=True)
        command = f'(echo "{password}";echo "{password}") | passwd "{username}"'
        subprocess.run(command, shell=True, check=True)
        if not ldap:
            command = f'(echo "{password}"; echo "{password}")  | smbpasswd -s -a "{username}"'
            subprocess.run(command, shell=True, check=True)
        else:
            subprocess.run(f'samba-tool user create {username} {password}', shell=True, check=True)
        print(f'Utente "{username}" created.')
        users.append(username)
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione dell\'utente: {e}')

def create_group(group_name, group_members,ldap=False):
    try:
        base_path='/sambashare/'
        path='/sambashare/'+group_name
        create_and_populate_folder(base_path,group_name)
        if not ldap:
            subprocess.run(['groupadd', group_name], check=True)
            subprocess.run(['chgrp', group_name,path], check=True)
            subprocess.run(f"chmod -R 770 {path}",shell=True,check=True)
            for m in group_members:
                subprocess.run(f'usermod -a -G {group_name} {m}',shell=True, check=True)
        else:
            subprocess.run(f'samba-tool group add {group_name}',shell=True, check=True)
            for m in group_members:
                subprocess.run(f'samba-tool group addmembers {group_name} {m}',shell=True, check=True)
        print(f'Gruppo "{group_name}" created.')
        group_members.clear()
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione del gruppo: {e}')




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

def make_fs(type, ldap=False):
    base_path = '/sambashare'
    os.mkdir(base_path)
    if type == "public" or type == "both":
        public_folders = ['Public', 'Public/Shared_Documents', 'Public/Shared_Pictures']
        for folder in public_folders:
            create_and_populate_folder(base_path, folder)
            subprocess.run(f"chmod -R 777 {base_path}/{folder}", shell=True, check=True)
    if type == "private" or type == "both":
        for user in users:
            base_user_path = os.path.join(base_path, user)
            # Specify the user folders
            user_folders = ['Documents', 'Documents/personal/', 'Documents/personal/lawyer',
                            'Documents/personal/family',
                            'Documents/work/', 'Documents/work/projects', 'Pictures', 'Downloads',
                            'Downloads/important_documents', 'Desktop', 'Desktop/trash', 'Desktop/work']
            for folder in user_folders:
                create_and_populate_folder(base_user_path, folder)
                if not ldap:
                    subprocess.run(f"chown -R {user} {base_user_path}", shell=True, check=True)
                    subprocess.run(f"chgrp -R {user} {base_user_path}", shell=True, check=True)
                    subprocess.run(f"chmod -R 770 {base_user_path}", shell=True, check=True)
                else:
                    subprocess.run(f"chmod -R 777 {base_user_path}", shell=True, check=True)

def modify_samba_conf(mode,user):
    with open("/etc/samba/smb.conf", 'a') as file:
        if mode=="Public":
            file.write("[Public]\ncomment = Public sharing folder\npath = /sambashare/Public\npublic=yes\nwritable = yes\ncreate mask= 0666\n directory mask = 0777")
        elif mode=="Private":
            file.write("\n[" +user + "]" + "\ncomment = private folder\npath = /sambashare/" + user + "\npublic=no\nguest ok=no\nread only = no\ncreate mask= 0660\n directory mask = 0770\nvalid users = " + user)
        elif mode=="Group":
            file.write("\n[" + user + "]" + "\npath=/sambashare/" + user + "\npublic=no\nguest ok=no\nread only=no\nvalid users=@" + user)

setup_ldap("mydomain.lan","Passw0rd")
modify_samba_conf("Public","")
create_user("a","Passw0rd",True)
kinit_user("a","Passw0rd")
modify_samba_conf("Private","a")
create_user("l","Passw0rd",True)
kinit_user("l","Passw0rd")
modify_samba_conf("Private","l")
create_user("c","Passw0rd",True)
kinit_user("c","Passw0rd")
modify_samba_conf("Private","c")
make_fs("both",True)

add_member("a")

add_member("l")

add_member("c")

create_group("cyber",group_members,True)
modify_samba_conf("Group","cyber")
kinit_user("administrator","Passw0rd")
