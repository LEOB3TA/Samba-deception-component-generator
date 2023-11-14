base_dockerfile_content = """# Usa l'immagine di Ubuntu 20.04 come base
FROM ubuntu:20.04

# Aggiorna il repository degli apt e installa Samba
RUN apt-get update && \
            apt-get install -y samba && \
                               apt-get install -y python3
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
while(True):
    choice = int(input("""
----------------------------------------------------------------------------------
Choose what type of sharing do you prefer: 0 --> public, 1 --> privale, 2 --> both
----------------------------------------------------------------------------------
    """))
    if choice == 0:
        print("public")  # creare implementzioni corrette
        break
    elif choice == 1:
        print("private")  # creare implementzioni corrette
        break
    elif choice == 2:
        print("both")  # creare implementzioni corrette
        break
    else:
        print("Invalid choice")
while(True): ##Ci piace??
    choice = int(input("""
----------------------------------------------------------------------------------
Choose what type of file system do you prefer: 0 --> home, 1 --> work
----------------------------------------------------------------------------------
    """))
    if choice == 0:
        print("home")  # creare implementzioni corrette
        break
    elif choice == 1:
        print("work")  # creare implementzioni corrette
        break
    else:
        print("Invalid choice")
