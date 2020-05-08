#!/bin/sh
cd ~ &&
sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bak && 
sudo wget https://HLOverflow.github.io/RPIDHCPCH.conf -O /etc/dhcpcd.conf &&
sudo sed -i s/WLANIP/$1/g /etc/dhcpcd.conf &&
sudo sed -i s/ETHIP/$2/g /etc/dhcpcd.conf &&
sudo sed -i s/ROUTERIP/$3/g /etc/dhcpcd.conf &&
sudo apt-get install git wiringpi ntp ntpdate -y &&
sudo sed -i s/debian/sg/g /etc/ntp.conf
sudo service ntp restart &&
cd ~ &&
wget http://www.cooking-hacks.com/media/cooking/images/documentation/raspberry_arduino_shield/raspberrypi2.zip  &&
unzip raspberrypi2.zip &&
cd cooking/arduPi/ &&
chmod +x install_arduPi &&
./install_arduPi &&
cd ~ &&
wget http://www.cooking-hacks.com/media/cooking/images/documentation/tutorial_kit_lorawan/arduPi_api_LoRaWAN_v1_2.zip && 
unzip -u arduPi_api_LoRaWAN_v1_2.zip && 
cd cooking/examples/LoRaWAN && 
chmod +x cook.sh && 
./cook.sh LoRaWAN_01a_configure_module_868.cpp &&
./cook.sh LoRaWAN_01b_configure_module_900.cpp &&
./cook.sh LoRaWAN_02_send_unconfirmed.cpp &&
./cook.sh LoRaWAN_03_send_confirmed.cpp &&
./cook.sh LoRaWAN_04_power_level.cpp &&
./cook.sh LoRaWAN_05_data_rate.cpp &&
./cook.sh LoRaWAN_06_adaptive_data_rate.cpp &&
./cook.sh LoRaWAN_07_channels_frequency.cpp &&
./cook.sh LoRaWAN_P2P_01_configure_module.cpp &&
./cook.sh LoRaWAN_P2P_02_send_packets.cpp &&
./cook.sh LoRaWAN_P2P_03_receive_packets.cpp &&
./cook.sh LoRaWAN_P2P_04_hybrid_p2p_to_lorawan.cpp &&
./cook.sh LoRaWAN_Template.cpp &&
echo "[*] done"
