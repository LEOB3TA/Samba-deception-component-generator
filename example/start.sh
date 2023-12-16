#!/bin/bash
# Riavvia il servizio smbd
echo "search mydomain.lan
nameserver 127.0.0.1
" > /etc/resolv.conf
service samba-ad-dc start
/bin/bash