import lib_platform
import subprocess
import os
import shutil
import sys
import time
import inquirer


base_dockerfile_content = """# Usa l'immagine di Ubuntu 20.04 come base
FROM ubuntu:20.04

# Aggiorna il repository degli apt e installa Samba
RUN apt-get update && \\
 apt-get install -y samba && \\
            apt-get install -y pandoc && \\
            apt-get install -y texlive-latex-base && \\
            apt-get install -y texlive-fonts-recommended && \\
            apt-get install -y texlive-fonts-extra && \\
          #  apt-get install -y texlive-latex-extra && \\
            apt-get clean && \\
            rm -rf /var/lib/apt/lists/*

#Copia il file setup.py e lo esegue
COPY setup.py /
RUN python3 /setup.py && rm /setup.py

RUN apt-get remove -y pandoc && \\
    apt-get remove -y texlive-latex-base && \\
    apt-get remove -y texlive-fonts-recommended && \\
    apt-get remove -y texlive-fonts-extra

# Copia il file di configurazione di Samba nella posizione corretta
COPY smb.conf /etc/samba/smb.conf


# Esponi le porte necessarie per Samba
EXPOSE 139 445


# Avvia il servizio Samba quando il contenitore viene avviato
RUN service smbd restart
CMD ["smbd", "--foreground", "--no-process-group"]
CMD tail -f /dev/null"""

base_smb_config_content = """#======================= Global Settings =======================

[global]

## Browsing/Identification ###

# Change this to the workgroup/NT-domain name your Samba server will part of
   workgroup = WORKGROUP
   client min protocol = NT1
   client max protocol = SMB3 
   security = user
#### Networking ####

# The specific set of interfaces / networks to bind to
# This can be either the interface name or an IP address/netmask;
# interface names are normally preferred
;   interfaces = 127.0.0.0/8 eth0

# Only bind to the named interfaces and/or networks; you must use the
# 'interfaces' option above to use this.
# It is recommended that you enable this feature if your Samba machine is
# not protected by a firewall or is a firewall itself.  However, this
# option cannot handle dynamic or non-broadcast interfaces correctly.
;   bind interfaces only = yes



#### Debugging/Accounting ####

# This tells Samba to use a separate log file for each machine
# that connects
   log file = /var/log/samba/log.%m

# Cap the size of the individual log files (in KiB).
   max log size = 1000

# We want Samba to only log to /var/log/samba/log.{smbd,nmbd}.
# Append syslog@1 if you want important messages to be sent to syslog too.
   logging = file

# Do something sensible when Samba crashes: mail the admin a backtrace
   panic action = /usr/share/samba/panic-action %d


####### Authentication #######

# Server role. Defines in which mode Samba will operate. Possible
# values are "standalone server", "member server", "classic primary
# domain controller", "classic backup domain controller", "active
# directory domain controller". 
#
# Most people will want "standalone server" or "member server".
# Running as "active directory domain controller" will require first
# running "samba-tool domain provision" to wipe databases and create a
# new domain.
   server role = standalone server

   obey pam restrictions = yes

# This boolean parameter controls whether Samba attempts to sync the Unix
# password with the SMB password when the encrypted SMB password in the
# passdb is changed.
   unix password sync = yes

# For Unix password sync to work on a Debian GNU/Linux system, the following
# parameters must be set (thanks to Ian Kahan <<kahan@informatik.tu-muenchen.de> for
# sending the correct chat script for the passwd program in Debian Sarge).
   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .

# This boolean controls whether PAM will be used for password changes
# when requested by an SMB client instead of the program listed in
# 'passwd program'. The default is 'no'.
   pam password change = yes

# This option controls how unsuccessful authentication attempts are mapped
# to anonymous connections
   map to guest = bad user

########## Domains ###########

#
# The following settings only takes effect if 'server role = classic
# primary domain controller', 'server role = classic backup domain controller'
# or 'domain logons' is set 
#

# It specifies the location of the user's
# profile directory from the client point of view) The following
# required a [profiles] share to be setup on the samba server (see
# below)
;   logon path = \\%N\profiles\%U
# Another common choice is storing the profile in the user's home directory
# (this is Samba's default)
#   logon path = \\%N\%U\profile

# The following setting only takes effect if 'domain logons' is set
# It specifies the location of a user's home directory (from the client
# point of view)
;   logon drive = H:
#   logon home = \\%N\%U

# The following setting only takes effect if 'domain logons' is set
# It specifies the script to run during logon. The script must be stored
# in the [netlogon] share
# NOTE: Must be store in 'DOS' file format convention
;   logon script = logon.cmd

# This allows Unix users to be created on the domain controller via the SAMR
# RPC pipe.  The example command creates a user account with a disabled Unix
# password; please adapt to your needs
; add user script = /usr/sbin/useradd --create-home %u

# This allows machine accounts to be created on the domain controller via the 
# SAMR RPC pipe.  
# The following assumes a "machines" group exists on the system
; add machine script  = /usr/sbin/useradd -g machines -c "%u machine account" -d /var/lib/samba -s /bin/false %u

# This allows Unix groups to be created on the domain controller via the SAMR
# RPC pipe.  
; add group script = /usr/sbin/addgroup --force-badname %g

############ Misc ############

# Using the following line enables you to customise your configuration
# on a per machine basis. The %m gets replaced with the netbios name
# of the machine that is connecting
;   include = /home/samba/etc/smb.conf.%m

# Some defaults for winbind (make sure you're not using the ranges
# for something else.)
;   idmap config * :              backend = tdb
;   idmap config * :              range   = 3000-7999
;   idmap config YOURDOMAINHERE : backend = tdb
;   idmap config YOURDOMAINHERE : range   = 100000-999999
;   template shell = /bin/bash

# Setup usershare options to enable non-root users to share folders
# with the net usershare command.

# Maximum number of usershare. 0 means that usershare is disabled.
#   usershare max shares = 100

# Allow users who've been granted usershare privileges to create
# public shares, not just authenticated ones
   usershare allow guests = yes

#======================= Share Definitions =======================

[homes]
   comment = Home Directories
   browseable = no

# By default, the home directories are exported read-only. Change the
# next parameter to 'no' if you want to be able to write to them.
   read only = yes

# File creation mask is set to 0700 for security reasons. If you want to
# create files with group=rw permissions, set next parameter to 0775.
   create mask = 0700

# Directory creation mask is set to 0700 for security reasons. If you want to
# create dirs. with group=rw permissions, set next parameter to 0775.
   directory mask = 0700

# By default, \\server\\username shares can be connected to by anyone
# with access to the samba server.
# The following parameter makes sure that only "username" can connect
# to \\server\\username
# This might need tweaking when using external authentication schemes
   valid users = %S

# Un-comment the following and create the netlogon directory for Domain Logons
# (you need to configure Samba to act as a domain controller too.)
;[netlogon]
;   comment = Network Logon Service
;   path = /home/samba/netlogon
;   guest ok = yes
;   read only = yes

# Un-comment the following and create the profiles directory to store
# users profiles (see the "logon path" option above)
# (you need to configure Samba to act as a domain controller too.)
# The path below should be writable by all users so that their
# profile directory may be created the first time they log on
;[profiles]
;   comment = Users profiles
;   path = /home/samba/profiles
;   guest ok = no
;   browseable = no
;   create mask = 0600
;   directory mask = 0700

[printers]
   comment = All Printers
   browseable = no
   path = /var/tmp
   printable = yes
   guest ok = no
   read only = yes
   create mask = 0700

# Windows clients look for this share name as a source of downloadable
# printer drivers
[print$]
   comment = Printer Drivers
   path = /var/lib/samba/printers
   browseable = yes
   read only = yes
   guest ok = no
# Uncomment to allow remote administration of Windows print drivers.
# You may need to replace 'lpadmin' with the name of the group your
# admin users are members of.
# Please note that you also need to set appropriate Unix permissions
# to the drivers directory for these users to have write rights in it
;   write l"""

base_setup_content = """import subprocess
import random
import os
from datetime import datetime, timedelta

users = []
group_members=[]

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
def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['useradd', '-m', '-p', password, username], check=True)
        command = f'(echo "{password}"; echo "{password}")  | smbpasswd -s -a "{username}"'
        subprocess.run(command, shell=True, check=True)
        print(f'Utente "{username}" created.')
        users.append(username)
    except subprocess.CalledProcessError as e:
        print(f'Errore durante la creazione dell\\'utente: {e}')

def create_group(group_name, list):
    try:
        base_path='/sambashare/'
        path='/sambashare/'+group_name
        create_and_populate_folder(base_path,group_name)
        subprocess.run(['groupadd', group_name], check=True)
        subprocess.run(['chgrp', group_name,path], check=True)
        subprocess.run(f"chmod -R 770 {path}",shell=True,check=True)
        for m in group_members:
            subprocess.run(['usermod', '-a', '-G', group_name, m], check=True)
        print(f'Gruppo "{group_name}" created.')
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
    
def make_fs(type):
    base_path = '/sambashare'
    os.mkdir(base_path)
    if type == "public" or "both":
        public_folders = ['Public', 'Public/Shared_Documents', 'Public/Shared_Pictures']
        for folder in public_folders:
           create_and_populate_folder(base_path,folder)
           subprocess.run(f"chmod -R 777 {base_path}/{folder}",shell=True,check=True)
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
            subprocess.run(f"chown -R {user} {base_user_path}",shell=True,check=True)
            subprocess.run(f"chgrp -R {user} {base_user_path}",shell=True,check=True)
            subprocess.run(f"chmod -R 770 {base_user_path}",shell=True,check=True)
"""


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
questions = [
    inquirer.List(
        "type",
        message="Choose what type of sharing do you prefer",
        choices=["Public", "Private", "Both"],
    ),
]
chosen_type = inquirer.prompt(questions)

if "Public" in chosen_type["type"]:
    base_smb_config_content = base_smb_config_content + "\n" + "[Public]\ncomment = Public sharing folder\npath = /sambashare/Public\npublic=yes\nwritable = yes\ncreate mask= 0666\n directory mask = 0777"
    base_setup_content += 'make_fs("public")'

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
        base_smb_config_content = base_smb_config_content + "\n" + "[" + user["username"] + "]" + "\ncomment = private folder\npath = /sambashare/" + user["username"] + "\npublic=no\nguest ok=no\nread only = no\ncreate mask= 0660\n directory mask = 0770\nvalid users = " + user["username"]
    base_setup_content += 'make_fs("private")'

elif "Both" in chosen_type["type"]:
    users = []
    base_smb_config_content = base_smb_config_content + "\n" + "[Public]\ncomment = Public sharing folder\npath = /sambashare/Public\npublic=yes\nbrowsable = yes\nwritable = yes\nread only = no"
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
        base_smb_config_content = base_smb_config_content + "\n" + "[" + user[
            "username"] + "]" + "\ncomment = private folder\npath = /sambashare/" + user[
                                      "username"] + "\npublic=no\nguest ok=no\nread only = no\ncreate mask= 0660\n directory mask = 0770\nvalid users = " + \
                                  user["username"]
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
            base_smb_config_content = base_smb_config_content + "\n" + "[" + group_name + "]" + "\npath=/sambashare/" + group_name + "\npublic=no\nguest ok=no\nread only=no\nvalid users=@" + group_name

questions=[inquirer.List("y_n",
            message="Do you want LDAP authentication",
            choices=["Yes", "No"]),]
ldap_y_n = inquirer.prompt(questions)

if "Yes" in ldap_y_n["y_n"]:
    IPserverLdap = input("insert IP of LDAP server: ")
    base_smb_config_content = base_smb_config_content[
                              :74] + "\n" + "passdb backend = ldapsam:ldap://" + IPserverLdap + "\nldap suffix = dc=example,dc=org\nldap user suffix = cn=users,cn=accounts\n" + base_smb_config_content[                                                                                                                                                74:]
    # dn = input("insert distinguished name (DN): ")

if os.path.exists("image"):
    shutil.rmtree("image")

os.mkdir("image")

# write the setup file
with open("./image/setup.py", 'w') as file:
    file.write(base_setup_content)

# write smb.conf file
with open("./image/smb.conf", 'w') as file:
    file.write(base_smb_config_content)

# write the Dockerfile file
with open("./image/Dockerfile", 'w') as file:
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
        if lib_platform.is_platform_windows == True:
            docker_run_command = f"START /B docker run -p 127.0.0.1:{port1}:139 -p 127.0.0.1:{port2}:445 {image_name}"
        else:
            docker_run_command = f"docker run -p 127.0.0.1:{port1}:139 -p 127.0.0.1:{port2}:445 {image_name} &"
        try:
            subprocess.run(docker_run_command, shell=True, check=True)
            print("Docker image run successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running Docker image: {e}")
            sys.exit(1)

questions=[inquirer.List("y_n",
            message="Do you want delete all the created files?",
            choices=["Yes", "No"]),]
delete_y_n = inquirer.prompt(questions)
if "Yes" in build_y_n["y_n"]:
    os.sync()
    shutil.rmtree("image")

print("""
----------------------------------------------------------------------------------
Thanks for using this script.
Author: Antonio Cassanelli, Leonardo Focardi, Christian Galeone
----------------------------------------------------------------------------------
""")
