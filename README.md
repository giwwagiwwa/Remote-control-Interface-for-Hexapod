# Remote-control-Interface-for-Hexapod
Deployment of a Flask webserver in a Raspberry Pi for controlling the servos offset of an Hexapod robot with 18 dof. Based on Capers II, a Hexapod Robot

## Attribution:
This project uses source code for controlling the Hexapod from https://github.com/Toglefritz/Capers_II.

## File description:
This repo includes:
* The flask webserver interface for controlling the servos offset by communicating the RPI with the Botboarduino by an HC-06 Bluetooth dongle.
* The source code for controlling the Hexapod modified to control the serial commands by the webserver.