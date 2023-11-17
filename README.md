# Samba-deception-component-generator
This repository is dedicated to a powerful tool designed to enhance network security through deception techniques. By leveraging the Samba protocol, the Samba Deception Component Generator provides an efficient way to create and deploy deceptive components within your network infrastructure
## Obiettivo
The goal of this project is to create a fake resource generator for one specific type of resource.

    • The final output of the generator must be a OCI compatible image ready to be instantiated
    • The container image must include all the relevant "fake" data for its correct operation
    • The container must function out of the box, eventual configuration has to be provided during the generation to build the final working image
        ◦ support both public and private shares
        ◦ automatically generated and realistic fs hierarchy
        ◦ populated with generated word/pdf files (https://pandoc.org/)
        ◦ support for ldap for authentication
## TODO
<ul>
<li>Scrivere nel smb.conf la configurazione desiderata</li>
<li>Controllare che il comando COPY effettivamente copi il nostro file desiderato</li>
<li>Capire come generare i file e inserirli nel filesystem fake</li>
<li>Controllare che le porte siano corrette</li>
<li>Inserire alcune catture alle eccezioni</li>
<li>Controllare i todo nello script</li>
<li>È necessaria la funzione __main__ in python??</li>
</ul>


## Come creare un immagine OCI
- Creare un Dockerfile
- docker build -t <nome> -f Dockerfile .
- docker image save -o <nome>.tar <nome>
- skopeo copy docker-archive:<nome>.tar oci:<nome>:latest

Viene creata una cartella con tutto ciò che serve.
#### NB skopeo deve essere installato
