![desktop](https://user-images.githubusercontent.com/113215575/190463642-8867eb49-7cee-41e2-9248-703e4179cf9e.png)
![mobile1](https://user-images.githubusercontent.com/113215575/190463649-fabb3692-3d82-4e6b-81f3-b1a106ab6807.png)
# Hash Kit
### Free, Open-Source, Bitcoin Mining Farm Management Software
From, Hash Frontier, Twitter: @HashFrontier

No more black boxes, no more management software fees, and improved miner uptime and insights. Works well on a mobile browser too.

This software assumes that your miners have static addresses assigned to them. It is generally a good practice to assign static IP addresses to your miners or use a switch that assigns static addresses to each ethernet port.

### Currently only supports cgminer based firmwares (Verified: Bitmain, Vnish)

## Setup

1) Install Ubuntu Server on your machine, keeping the "ubuntu" default username. Any ol' computer will do, really. 

    If you're using a Raspberry Pi, only use a quality brand of Micro SD card. Cheaper brands (*cough* PATRIOT..) are verified unreliable. Image the Micro SD card using the Raspberry Pi Imager tool. You can find Ubuntu Server listed in the "Other General Purpose OS" section of the tool.

2) SSH into your machine from another computer or use the terminal directly on the machine to complete the following steps.

3) Run the following command: 

    git clone https://github.com/HashFrontier/Hash-Kit.git

4) Run the following command:

    cd Hash-Kit/
    
5) Run the following command:

    sudo sh system_resources/init.sh
    
6) Wait. The machine will reboot itself and automatically start the Hash Kit services.
   
7) Locate the machine's IP address on your network and navigate to it in your browser. (Ex: 192.168.1.169)
