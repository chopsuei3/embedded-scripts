#!/bin/sh
#gpio mode 27 out
#gpio mode 28 out
sudo iptables -t nat -I POSTROUTING -o tun0 -j MASQUERADE
#gpio write 27 0
#gpio write 28 1

