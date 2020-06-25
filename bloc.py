import serial

dsPIC = serial.Serial('/dev/ttyS3',115200)
dsPIC.flushInput()
dsPIC.flushOutput()
voltaje=open('voltaje.txt', 'w+b')
while True:
    bytesToRead = dsPIC.inWaiting()
    datos=dsPIC.read(bytesToRead)
    print(datos)
    voltaje.write(datos)

