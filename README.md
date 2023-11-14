# Samba-deception-component-generator
This repository is dedicated to a powerful tool designed to enhance network security through deception techniques. By leveraging the Samba protocol, the Samba Deception Component Generator provides an efficient way to create and deploy deceptive components within your network infrastructure

## TODO
<ul>
<li>Scrivere nel smb.conf la configurazione desiderata</li>
<li>Controllare che il comando COPY effettivamente copi il nostro file desiderato</li>
<li>Capire come generare i file e inserirli nel filesystem fake</li>
<li>Controllare che le porte siano corrette</li>


## Come creare un immagine OCI
- Creare un Dockerfile
- docker build -t <nome> -f Dockerfile .
- docker image save -o <nome>.tar <nome>
- skopeo copy docker-archive:<nome>.tar oci:<nome>:latest

Viene creata una cartella con tutto ciò che serve.
#### NB skopeo deve essere installato
