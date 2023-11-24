# Samba-deception-component-generator
This repository is dedicated to a powerful tool designed to enhance network security through deception techniques. By leveraging the Samba protocol, the Samba Deception Component Generator provides an efficient way to create and deploy deceptive components within your network infrastructure
## Goal
The goal of this project is to create a fake resource generator for one specific type of resource.

    • The final output of the generator must be a OCI compatible image ready to be instantiated
    • The container image must include all the relevant "fake" data for its correct operation
    • The container must function out of the box, eventual configuration has to be provided during the generation to build the final working image
        ◦ support both public and private shares
        ◦ automatically generated and realistic fs hierarchy
        ◦ populated with generated word/pdf files (https://pandoc.org/)
        ◦ support for ldap for authentication

## Usage


