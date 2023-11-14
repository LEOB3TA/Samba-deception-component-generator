# Usa l'immagine di Ubuntu 20.04 come base
FROM ubuntu:20.04

# Aggiorna il repository degli apt e installa Samba
RUN apt-get update && \
    apt-get install -y samba && \
  ##  apt-get clean && \
 ##   rm -rf /var/lib/apt/lists/*

# Copia il file di configurazione di Samba nella posizione corretta
COPY smb.conf /etc/samba/smb.conf

# Esponi le porte necessarie per Samba
EXPOSE 137/udp 138/udp 139 445

# Avvia il servizio Samba quando il contenitore viene avviato
CMD ["smbd", "--foreground", "--no-process-group"]
