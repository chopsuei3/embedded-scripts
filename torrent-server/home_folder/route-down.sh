#!/bin/sh
sudo iptables -t nat -D POSTROUTING -o tun0 -j MASQUERADE
gpio write 28 0
gpio write 27 1

