base_dockerfile_content = """# Usa l'immagine di Ubuntu 20.04 come base
FROM ubuntu:20.04

# Aggiorna il repository degli apt e installa Samba
RUN apt-get update && \
            apt-get install -y samba && \
            apt-get install -y python3 && \
            apt-get install pandoc && \
            apt-get install texlive-latex-base && \
            apt-get install texlive-fonts-recommended && \
            apt-get install texlive-fonts-extra && \
            apt-get install texlive-latex-extra
##  apt-get clean && \
##   rm -rf /var/lib/apt/lists/*

#Copia il file setup.py e lo esegue
COPY setup.py /home/
RUN python3 /home/setup.py && rm /home/setup.py

# Copia il file di configurazione di Samba nella posizione corretta
COPY smb.conf /etc/samba/smb.conf

# Esponi le porte necessarie per Samba
EXPOSE 137/udp 138/udp 139 445

# Avvia il servizio Samba quando il contenitore viene avviato
CMD ["smbd", "--foreground", "--no-process-group"]"""

base_smb_config_content = """#======================= Global Settings =======================

[global]

## Browsing/Identification ###

# Change this to the workgroup/NT-domain name your Samba server will part of
   workgroup = WORKGROUP

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

def create_user(username, password):
    try:
        # Creare un nuovo utente
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)
        subprocess.run(['sudo', 'smbpasswd','-a', '-p', password, username], check=True)
        print(f'Utente "{username}" creato con successo.')
    except subprocess.CalledProcessError as e:
       print(f'Errore durante la creazione dell\\'utente: {e}')
       
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

def create_files(dimMin,dimMax,numFile):
    for _ in range(numFile):
        dimA = str(random.uniform(dimMin,dimMax))
        nomeFile = f"file{dimA}.txt" #TODO acpire come arrotorndare il nome

        with open(nomeFile, "w") as file:
            dim = random.uniform(dimMin, dimMax)
            numWords = random.randint(5, 15)  # Random number of words per sentence
            numSentences = int((dim * 1000000) / (numWords * 5))  # Assuming average word length of 5 characters

            for _ in range(numSentences):
                sentence = generate_random_sentence(numWords) + '\\n'
                file.write(sentence)
                
    def convert_file(input_file,output_file):
        subprocess.run(['pandoc', input_file, '-o', output_file])
        print(f'File "{input_file}" converted to "{output_file}" successfully.')


# Sostituisci 'nuovo_utente' e 'nuova_password' con i valori desiderati
#new_username = 'nuovo_utente'
#new_password = 'nuova_password'

#create_user(new_username, new_password)

#create_files(1,50,10) crea 10 file di dimensione variabile 1 a 50 MB
"""

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
while True:
    choice = int(input("""
----------------------------------------------------------------------------------
Choose what type of sharing do you prefer: 0 --> public, 1 --> private, 2 --> both
----------------------------------------------------------------------------------
    """))
    if choice == 0: #change [folder] if you change the folder in samba, other options: guest ok = yes create mask =0775
        base_smb_config_content=base_smb_config_content + "\n"+ "[Public]\ncomment = Public sharing folder\npath = /sambashare/Public\npublic=yes\nbrowsable = yes\nwritable = yes\nread only = no"
        break
    elif choice == 1:
        base_setup_content.replace(f"public_share = True", f"public_share = False")
        number_of_user = int(input("how many user do you want create?"))
        for _ in range(number_of_user):
            username = input("insert username: ")
            password = input("insert password for user " + username+": ")
            base_setup_content = base_setup_content + f"\ncreate_user(" + '"' + username + '"' + "," + '"' + password + '"' ")"
            base_smb_config_content=base_smb_config_content + "\n"+ "["+username+"]"+"\ncomment = private folder\npath = /sambashare/"+username+"\npublic=no\nguest ok=no"
        break
    elif choice == 2:
        base_smb_config_content=base_smb_config_content + "\n"+ "[Public]\ncomment = Public sharing folder\npath = /sambashare/Public\npublic=yes\nbrowsable = yes\nwritable = yes\nread only = no"
        number_of_user = int(input("how many user do you want create? "))
        for _ in range(number_of_user):
            username = input("insert username: ")
            password = input("insert password for user " + username+": ")
            base_setup_content = base_setup_content + "\ncreate_user(" + username + "," + password + ")"
            base_smb_config_content=base_smb_config_content + "\n"+ "["+username+"]"+"\ncomment = private folder\npath = /sambashare/"+username+"\npublic=no\nguest ok=no"
        break
    else:
        print("Invalid choice")
while (True):  ##Ci piace??
    choice = int(input("""
----------------------------------------------------------------------------------
Do you want LDAP authentication: 0 --> yes, 1 --> no
----------------------------------------------------------------------------------
    """))
    if choice == 0:
        print("yes\n")  # creare implementzioni corrette
        serverLdap = input("insert LDAP server: ")
        dn = input("insert distinguished name (DN): ")
        break
    elif choice == 1:
        print("no")  # creare implementzioni corrette
        break
    else:
        print("Invalid choice")

# write the setup file
with open("setup.py", 'w') as file:
    file.write(base_setup_content)

# write smb.conf file
with open("smb.conf", 'w') as file:
    file.write(base_smb_config_content)

# write the Dockerfile file
with open("Dockerfile", 'w') as file:
    file.write(base_dockerfile_content)
