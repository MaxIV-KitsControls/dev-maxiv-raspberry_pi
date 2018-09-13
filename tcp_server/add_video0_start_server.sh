#!/bin/sh
sudo modprobe bcm2835-v4l2
cd ~/tcp_server/
bash keep_eth0_alive.sh

