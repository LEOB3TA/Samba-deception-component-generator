# Samba-deception-component-generator
This repository is dedicated to a powerful tool designed to enhance network security through deception techniques. By leveraging the Samba protocol, the Samba Deception Component Generator provides an efficient way to create and deploy deceptive components within your network infrastructure

# Index
- [Usage](#usage)
- [Features](#features)
- [Examples](#examples)
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

## Features
The goal of this project is to create a fake samba component, in particular:
- The created container contains all the fake data for correct operation
- The configuration is provided during the generation of the container
- The generation:
  - supports **both** **public** and **private** shared
  - automatically generates and populates with **fake files a realistic fs hierarchy**
  - supports **LDAP** authentication


