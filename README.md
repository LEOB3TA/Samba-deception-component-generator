# Samba-deception-component-generator
This repository is dedicated to a powerful tool designed to enhance network security through deception techniques. By leveraging the Samba protocol, the Samba Deception Component Generator provides an efficient way to create and deploy deceptive components within your network infrastructure

# Index
- [Usage](#usage)
- [Features](#features)
- [Example](#example)
- [Contribute](#contribute)

## Usage

- Clone repository from Github <!--Forse meglio fare una release-->
```shell
git clone https://github.com/LEOB3TA/Samba-deception-component-generator
cd Samba-deception-component-generator
```
- Install the requirements
```shell
pip install -r requirements.txt
```
- Run samba_deception_component_generator.py
```shell
python3 samba_deception_component_generator.py
```
- The generated files will be created inside **image** folder

 If you didn't build and run docker image via our script:

- build docker image
```shell
cd image
docker build -t image-name .
```
- run docker image
```shell
docker run -d -p host-ip:host-port:445 -p host-ip:host-port:139 --name container-name image-name
```

## Features
The goal of this project is to create a fake samba component, in particular:
- The created container contains all the fake data for correct operation
- The configuration is provided during the generation of the container
- The generation:
  - supports **both** **public** and **private** shared
  - automatically generates and populates with **fake files a realistic fs hierarchy**
  - supports **LDAP** authentication
  - creations of **local users and groups**
  - build and run **docker image** (**only for standard authentication, not for LDAP**)
  - delete of the created files

## Example

https://github.com/LEOB3TA/Samba-deception-component-generator/assets/100613275/fd494663-d697-44e6-a6b9-f31eabcdea5e

This is an example of usage; all generated files are placed within the "example" folder.
The users are:
- *a*, password = *Passw0rd*
- *l*, password = *Passw0rd*
- *c*, password = *Passw0rd*
  
The group is *cyber*
## Contribute

We appreciate contributions to enhance this project! Here's how you can get involved:
- Bug Reports and Features: Open an issue to report bugs or suggest features.
- Code Contributions:
        Fork the repo.
        Create a branch, make changes, and commit.
        Push to your fork and open a pull request.

