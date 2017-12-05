count=0
while :
do
        if ! ping -c 1 $1
        then
                sudo echo "network down" >> /home/pi/log.txt
                sudo date >> /home/pi/log.txt
                sudo ifdown wlan0
                sudo ifup wlan0
                count=$(expr $count + 1)
        fi

        if ping -c 1 $1
        then
                count=0
                echo "network connect" >> /home/pi/log.txt
                sudo date >> /home/pi/log.txt
        fi

        if [ $count -eq 2 ];
        then
                sudo reboot
        fi
        sleep 10s
done

