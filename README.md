# Embedded Systems

The current project is designed to visualize the battery voltage of an electric vehicle. A dsPIC microcontroller is used to read voltage and send infomation onto a web page. 


## dsPIC
The dsPIC used is the dsPIC33EV256GM102. Analog voltage is read through pin 2 and UART transmission is performed on pin 11. 
### Hardware required
* PicKit 3
### Software required
* MPLAB X IDE
* MPLAB X IPE

1. Create a project on MPLAB X IDE and use [dsPIC.c](https://github.com/IvanMendoza1616/SistemasEmbebidos/blob/master/dsPIC.c)
2. COmpile it and load it to the dsPIC with MPLAB X IPE

## Web service

``` bash
sudo apt install python3-pip
pip3 install virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install flask
```
1. Create directory `plots` in `static/`
2. Run the flask server on local ip address
3. Be sure to have sudo privileges for listening to serial port

``` bash
python ./flaskt.py
```

## Author
IvanMendoza1616

