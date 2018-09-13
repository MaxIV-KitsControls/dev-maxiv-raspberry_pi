#!/bin/bash
while [ True ]; do
	ping -c1 your-gateway-etc 
	sleep 1
	ps -aux | grep -v grep | grep rpi_gpio_server > /dev/null
	if [ $? -eq 0 ]; then
		echo "Process is running."
	else
		python rpi_gpio_server.py -camera y &	
	fi
done
