#/bin/bash
gennum=`shuf -i 1-3 -n 1`

if [ "$gennum" = "1" ]
then
        /root/vpn1.sh
elif [ "$gennum" = "2" ]
then
        /root/vpn2.sh
elif [ "$gennum" = "3" ]
then
        /root/vpn3.sh
fi

