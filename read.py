import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

dsPIC = serial.Serial('/dev/ttyS3',115200)
dsPIC.flushInput()
dsPIC.flushOutput()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = [] 
i=1

voltaje = open('voltaje.txt', 'w+b')
vtemp=voltaje.readlines()
while len(vtemp)<10000:
    bytesToRead = dsPIC.inWaiting()
    datos = dsPIC.read(bytesToRead)
    print(datos)
    voltaje.write(datos)
    with open('voltaje.txt')as v1:
        vtemp = v1.readlines()
print(len(vtemp))
