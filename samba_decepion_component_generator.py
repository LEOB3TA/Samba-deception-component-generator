import lib_platform
import subprocess
import os
import shutil
import sys
import time
import inquirer
import socket
import re

base_start_content = """
#!/bin/bash

# Riavvia il servizio smbd
service smbd restart &

# Avvia smbd in foreground senza creare un nuovo gruppo di processi
smbd --foreground --no-process-group
"""

base_dockerfile_content = """# Usa l'immagine di Ubuntu 20.04 come base
FROM ubuntu:20.04

# Aggiorna il repository degli apt e installa Samba
RUN apt-get update && \\
 apt-get install -y samba winbind libnss-winbind krb5-user smbclient ldb-tools python3-cryptography && \\
            apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra && \\
            apt-get clean 

#Copia il file setup.py e lo esegue
COPY setup.py /
RUN python3 /setup.py && rm /setup.py

RUN apt-get remove -y pandoc texlive-latex-base texlive-fonts-recommended texlive-fonts-extra

COPY start.sh /start.sh
RUN chmod +x start.sh



# Esponi le porte necessarie per Samba
EXPOSE 139 445


# Avvia il servizio Samba quando il contenitore viene avviato
CMD /start.sh"""

base_setup_content = """import subprocess
import random
import os
import time
from datetime import datetime, timedelta

users = [] 
group_members=[]

def setup_ldap(domain, adminpasswd):
    config_content = f\"""[libdefaults]
    default_realm = {domain.upper()}
    dns_lookup_kdc = true
    dns_lookup_realm = false
    \"""
    with open("/etc/krb5.conf", "w") as krb5_conf:
            krb5_conf.write(config_content)
    subprocess.run("rm -f /etc/samba/smb.conf", shell=True, check=True)
    realm = domain.split(".")[0]
    subprocess.run(f"samba-tool domain provision --realm={domain.upper()} --domain {realm.upper()} --server-role=dc", shell=True, check=True)
    subprocess.run(f'samba-tool user setpassword administrator --newpassword={adminpasswd}', shell=True, check=True)
    subprocess.run('echo "search mydomain.lan\\nnameserver 127.0.0.1\\n" > /etc/resolv.conf', shell=True, check=True)
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
                sentence = generate_random_sentence(num_words) + '\\n'
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
        print(f'Errore durante la creazione dell\\'utente: {e}')

def create_group(group_name, group_members):
    try:
        base_path='/sambashare/'
        path='/sambashare/'+group_name
        create_and_populate_folder(base_path,group_name)
        subprocess.run(['groupadd', group_name], check=True)
        subprocess.run(['chgrp', group_name,path], check=True)
        subprocess.run(f"chmod -R 660 {path}",shell=True,check=True)
        for m in group_members:
            subprocess.run(['usermod', '-a', '-G', group_name, m], check=True)
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
            file.write("[Public]\\ncomment = Public sharing folder\\npath = /sambashare/Public\\npublic=yes\\nwritable = yes\\ncreate mask= 0666\\n directory mask = 0777")
        elif mode=="Private":
            file.write("\\n[" +user + "]" + "\\ncomment = private folder\\npath = /sambashare/" + user + "\\npublic=no\\nguest ok=no\\nread only = no\\ncreate mask= 0660\\n directory mask = 0770\\nvalid users = " + user)
        elif mode=="Group":
            file.write("\\n[" + user + "]" + "\\npath=/sambashare/" + user + "\\npublic=no\\nguest ok=no\\nread only=no\\nvalid users=@" + user)

"""

def get_local_ip_address():
    try:
        # Get the machine's hostname
        host_name = socket.gethostname()

        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(host_name)

        return ip_address
    except socket.error as e:
        print(f"Error in obtaining the local IP address: {e}")
        return None


def build_docker_image(image_name, dockerfile_path='.', build_args=None):
    """
     Build a Docker image from a specified Dockerfile using subprocess.

     :param image_name: Name for the Docker image.
     :param dockerfile_path: Path to the directory containing the Dockerfile.
     :param build_args: Dictionary of build arguments (optional).
     """
    build_command = ['docker', 'build', '-t', image_name]

    if build_args:
        for key, value in build_args.items():
            build_command.extend(['--build-arg', f'{key}={value}'])

    build_command.append(dockerfile_path)

    try:
        print(f"Building Docker image {image_name}...")
        build_process = subprocess.Popen(
            build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for output in build_process.stdout:
            print(output.strip())

        build_process.wait()

        if build_process.returncode == 0:
            print(f"Docker image {image_name} built successfully.")
        else:
            print(f"Failed to build Docker image {image_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")

print(""" _____                    _                  _                          _    _                                                                          _                                           _               
/  ___|                  | |                | |                        | |  (_)                                                                        | |                                         | |              
\ `--.   __ _  _ __ ___  | |__    __ _    __| |  ___   ___  ___  _ __  | |_  _   ___   _ __     ___  ___   _ __ ___   _ __    ___   _ __    ___  _ __  | |_    __ _   ___  _ __    ___  _ __  __ _ | |_  ___   _ __ 
 `--. \ / _` || '_ ` _ \ | '_ \  / _` |  / _` | / _ \ / __|/ _ \| '_ \ | __|| | / _ \ | '_ \   / __|/ _ \ | '_ ` _ \ | '_ \  / _ \ | '_ \  / _ \| '_ \ | __|  / _` | / _ \| '_ \  / _ \| '__|/ _` || __|/ _ \ | '__|
/\__/ /| (_| || | | | | || |_) || (_| | | (_| ||  __/| (__|  __/| |_) || |_ | || (_) || | | | | (__| (_) || | | | | || |_) || (_) || | | ||  __/| | | || |_  | (_| ||  __/| | | ||  __/| |  | (_| || |_| (_) || |   
\____/  \__,_||_| |_| |_||_.__/  \__,_|  \__,_| \___| \___|\___|| .__/  \__||_| \___/ |_| |_|  \___|\___/ |_| |_| |_|| .__/  \___/ |_| |_| \___||_| |_| \__|  \__, | \___||_| |_| \___||_|   \__,_| \__|\___/ |_|   
                                                                | |                                                  | |                                       __/ |                                                
                                                                |_|                                                  |_|                                      |___/                                                 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n

""")
print("This script allows you to create an OCI image for a deception component with a SAMBA server.")
time.sleep(0.5)
######LDAP SECTION
questions = [inquirer.List("y_n",
                           message="Do you want LDAP authentication",
                           choices=["Yes", "No"]), ]
ldap_y_n = inquirer.prompt(questions)
if "Yes" in ldap_y_n["y_n"]:
    while True:
        questions = [
            inquirer.Text(
                "domain",
                message="Insert the domain [mydomain.lan]:",
                default= "mydomain.lan"
            ), inquirer.Password(
                "password",
                message="insert the administrator password: "
            ), inquirer.Password(
                "password_confirm",
                message="Confirm password"
            )
        ]
        ldap = inquirer.prompt(questions)
        domain_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$')
        if domain_pattern.match(ldap["domain"]):
            password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')
            if password_pattern.match(ldap["password"]) and ldap["password"] == ldap["password_confirm"]:
                break
            else:
                print("The password must have one number, one uppercase letter and must be longer than 7 characters, or the passwords doesn't match")
        else:
            print("The domain is not in the correct format")
    base_setup_content += f'setup_ldap("{ldap["domain"]}","{ldap["password"]}")\n'
    base_start_content=f"""#!/bin/bash
# Riavvia il servizio smbd
echo "search {ldap["domain"]}\nnameserver 127.0.0.1\n" > /etc/resolv.conf
service samba-ad-dc start
/bin/bash"""
    questions = [
        inquirer.List(
            "type",
            message="Choose what type of sharing do you prefer",
            choices=["Public", "Private", "Both"],
        ),
    ]
    chosen_type = inquirer.prompt(questions)

    if "Public" in chosen_type["type"]:
        ##TODO anto roba che ha fatto stamattina
        base_setup_content += ('make_fs("public",True)\n')
        base_setup_content += ('modify_samba_conf("Public","")\n')

    elif "Private" in chosen_type["type"]:
        users = []
        try:
            number_of_user = int(input("how many user do you want create? "))
        except:
            print("you have to insert a integer number")
        for _ in range(number_of_user):
            while True:
                questions = [
                    inquirer.Text(
                        "username",
                        message="Insert username",
                    ), inquirer.Password(
                        "password",
                        message="Insert password"
                    ), inquirer.Password(
                        "password_confirm",
                        message="Confirm password"
                    )
                ]
                user = inquirer.prompt(questions)
                password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')
                if password_pattern.match(ldap["password"]) and ldap["password"] == ldap["password_confirm"]:
                    break
                else:
                    print("The password must have one number, one uppercase letter and must be longer than 7 characters, or the passwords doesn't match")
            users.append(user["username"])
            base_setup_content += f'create_user("{user["username"]}","{user["password"]}",True)\nkinit_user("{user["username"]}","{user["password"]}")\n'
            ##TODO roba che ha fatto anto stamattina
            base_setup_content += (f'modify_samba_conf("Private","{user["username"]}")\n')
        base_setup_content += 'make_fs("private",True)\n'
    elif "Both" in chosen_type["type"]:
        users = []
       ##TODO PUBLIC FOR ANTO
        base_setup_content += ('modify_samba_conf("Public","")\n')
        number_of_user = int(input("how many user do you want create? "))
        for _ in range(number_of_user):
            while True:
                questions = [
                    inquirer.Text(
                        "username",
                        message="Insert username",
                    ), inquirer.Password(
                        "password",
                        message="Insert password"
                    ), inquirer.Password(
                        "password_confirm",
                        message="Confirm password"
                    )
                ]
                user = inquirer.prompt(questions)
                if password_pattern.match(ldap["password"]) and ldap["password"] == ldap["password_confirm"]:
                    break
                else:
                    print("The password must have one number, one uppercase letter and must be longer than 7 characters, or the passwords doesn't match")
            users.append(user["username"])
            base_setup_content += f'create_user("{user["username"]}","{user["password"]}",True)\nkinit_user("{user["username"]}","{user["password"]}")'
            ## TODO anto roba stamattina per condivisione privata
            base_setup_content += (f'modify_samba_conf("Private","{user["username"]}")\n')
        base_setup_content += 'make_fs("both",True)\n'
    if "Both" in chosen_type["type"] or "Private" in chosen_type["type"]:
        questions=[inquirer.List("y_n",
                                 message="Do you want create groups",
                                 choices=["Yes", "No"]),]
        group_y_n = inquirer.prompt(questions)

        if "Yes" in group_y_n["y_n"]: ##TODO verificare il funzionamento in LDAP
            try:
                number_of_groups = int(input("how many groups do you want create? "))
            except:
                print("you have to insert a integer number")
            for _ in range(number_of_groups):
                group_name = input("insert name of the group (same name as the folder): ")
                question = [
                    inquirer.Checkbox(
                        "users",
                        message="Choose group's members (use right arrow to select and left to deselect)",
                        choices=users,
                    ),
                ]
                chosen_users = inquirer.prompt(question)
                for u in chosen_users["users"]:
                    base_setup_content += f'\nadd_member("{u}")\n'
                base_setup_content += f'\ncreate_group("{group_name}","group_members")\n'
                ##TODO roba di anto per i gruppi
                base_setup_content += (f'modify_samba_conf("Group","{group_name}")\n')
    base_setup_content += f'kinit_user("administrator","{ldap["password"]}")'
##### END OF LDAP SECTION


if "No" in ldap_y_n["y_n"]:
    questions = [
        inquirer.List(
            "type",
            message="Choose what type of sharing do you prefer",
            choices=["Public", "Private", "Both"],
        ),
    ]
    chosen_type = inquirer.prompt(questions)

    if "Public" in chosen_type["type"]:
        ##TODO roba anto public
        base_setup_content += (f'modify_samba_conf("Public","")\n')
        base_setup_content += ('make_fs("public")')

    elif "Private" in chosen_type["type"]:
        users = []
        try:
            number_of_user = int(input("how many user do you want create? "))
        except:
            print("you have to insert a integer number")
        for _ in range(number_of_user):
            while True:
                questions = [
                    inquirer.Text(
                        "username",
                        message="Insert username",
                    ), inquirer.Password(
                        "password",
                        message="Insert password"
                    ), inquirer.Password(
                        "password_confirm",
                        message="Confirm password"
                    )
                ]
                user = inquirer.prompt(questions)
                if user["password"] == user["password_confirm"]:
                    break
                else:
                    print("PASSWORD DO NOT MATCH")
            users.append(user["username"])
            base_setup_content += f'\ncreate_user("{user["username"]}","{user["password"]}")\n'
            ## TODO roba anto private
            base_setup_content += 'make_fs("private")'
            base_setup_content += (f'modify_samba_conf("Private","{user["username"]}")\n')

    elif "Both" in chosen_type["type"]:
        users = []
        ##TODO roba anto public
        base_setup_content += (f'modify_samba_conf("Public","")\n')
        number_of_user = int(input("how many user do you want create? "))
        for _ in range(number_of_user):
            while True:
                questions = [
                    inquirer.Text(
                        "username",
                        message="Insert username",
                    ), inquirer.Password(
                        "password",
                        message="Insert password"
                    ), inquirer.Password(
                        "password_confirm",
                        message="Confirm password"
                    )
                ]
                user = inquirer.prompt(questions)
                if user["password"] == user["password_confirm"]:
                    break
                else:
                    print("PASSWORD DO NOT MATCH")
            users.append(user["username"])
            base_setup_content += f'\ncreate_user("{user["username"]}","{user["password"]}")\n'
           ##TODO roba anto private
            base_setup_content += (f'modify_samba_conf("Private","{user["username"]}")\n')
        base_setup_content += 'make_fs("both")'
    if "Both" in chosen_type["type"] or "Private" in chosen_type["type"]:
        questions=[inquirer.List("y_n",
                message="Do you want create groups",
                choices=["Yes", "No"]),]
        group_y_n = inquirer.prompt(questions)

        if "Yes" in group_y_n["y_n"]:
            try:
                number_of_groups = int(input("how many groups do you want create? "))
            except:
                print("you have to insert a integer number")
            for _ in range(number_of_groups):
                group_name = input("insert name of the group (same name as the folder): ")
                question = [
                    inquirer.Checkbox(
                        "users",
                        message="Choose group's members (use right arrow to select and left to deselect)",
                        choices=users,
                    ),
                ]
                chosen_users = inquirer.prompt(question)
                for u in chosen_users["users"]:
                    base_setup_content += f'\nadd_member("{u}")\n'
                base_setup_content += f'\ncreate_group("{group_name}","group_members")\n'
                base_setup_content += (f'modify_samba_conf("Group","{group_name}")\n')
                #base_smb_config_content = base_smb_config_content + "\n" + "[" + group_name + "]" + "\npath=/sambashare/" + group_name + "\npublic=no\nguest ok=no\nread only=no\nvalid users=@" + group_name
if os.path.exists("./image"):
    shutil.rmtree("./image")

os.mkdir("./image")

#write start.sh
with open("image/start.sh", 'w') as file:
    file.write(base_start_content)

# write the setup file
with open("image/setup.py", 'w') as file:
    file.write(base_setup_content)

# write the Dockerfile file
with open("image/Dockerfile", 'w') as file:
    file.write(base_dockerfile_content)

questions=[inquirer.List("y_n",
            message="If you have docker do you want build the image?",
            choices=["Yes", "No"]),]
build_y_n = inquirer.prompt(questions)

if "Yes" in build_y_n["y_n"]:
    image_name = input("insert the name of the image: ")
    docker_build_command = f"docker build -t {image_name} ./image/"
    # Run the build command using subprocess
    try:
        subprocess.run(docker_build_command, shell=True, check=True)
        print("Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")
        sys.exit(1)
    questions = [inquirer.List("y_n",
                               message="Do you want run the image?",
                               choices=["Yes", "No"]), ]
    run_y_n = inquirer.prompt(questions)
    if "Yes" in run_y_n["y_n"]:
        port1 = int(input("Choose the actual port to which you want to map the port 139 of the image. "))
        port2 = int(input("Choose the actual port to which you want to map the port 445 of the image. "))
        ip_address=get_local_ip_address()
        if lib_platform.is_platform_windows:
            docker_run_command = f"START /B docker run -p {ip_address}:{port1}:139 -p {ip_address}:{port2}:445 {image_name}"
        else:
            docker_run_command = f"docker run -p {ip_address}:{port1}:139 -p {ip_address}:{port2}:445 {image_name} &"
        try:
            subprocess.run(docker_run_command, shell=True, check=True)
            print("Docker image run successfully.")
            print(f"\n\nPORT MAPPING: {ip_address}:{port1}-->139\t{ip_address}:{port2}-->445\n\n")
        except subprocess.CalledProcessError as e:
            print(f"Error running Docker image: {e}")
            sys.exit(1)

questions=[inquirer.List("y_n",
            message="Do you want delete all the created files?",
            choices=["Yes", "No"]),]
delete_y_n = inquirer.prompt(questions)
if "Yes" in delete_y_n["y_n"]:
    os.sync()
    shutil.rmtree("image")

print("""
----------------------------------------------------------------------------------
Thanks for using this script.
Author: Antonio Cassanelli, Leonardo Focardi, Christian Galeone
----------------------------------------------------------------------------------
""")
