# Usa l'immagine di Ubuntu 20.04 come base
FROM ubuntu:20.04

# Aggiorna il repository degli apt e installa Samba
RUN apt-get update && \
 apt-get install -y samba winbind libnss-winbind krb5-user smbclient ldb-tools python3-cryptography && \
            apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra && \
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
CMD /start.sh