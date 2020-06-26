from flask import Flask
from flask import Response
from flask import render_template
from flask import request
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import serial

app = Flask(__name__)

@app.route("/")
def root():
    test = 1
    return render_template("index.html",vf = test)

@app.route('/plot/<value>')
def plot(value = None):
    dsPIC = serial.Serial('/dev/ttyS3',115200)
    dsPIC.flushInput()
    dsPIC.flushOutput()
    voltaje = open('voltaje.txt', 'w+b')
    vtemp=voltaje.readlines()

    bytesToRead = dsPIC.inWaiting()
    datos = dsPIC.read(bytesToRead)
    dsPIC.flushInput()
    dsPIC.flushOutput()
    dsPIC.read_all()

    while len(vtemp)<int(value)*2424:
        bytesToRead = dsPIC.inWaiting()
        datos = dsPIC.read(bytesToRead)
        #print(datos)
        voltaje.write(datos)
        with open('voltaje.txt')as v1:
            vtemp = v1.readlines()
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    fig.savefig('templates/temp.png',dpi = 100)
    #print(len(vtemp))

    return render_template("index.html",vf = lastvoltage()*5/1024)

def lastvoltage():
    with open('voltaje.txt') as file:
        file_data = file.readlines()
    return int(file_data[-2])


def create_figure():
    with open('voltaje.txt') as file:
        file_data = file.readlines()
    x = []
    y = []
    for i in range (1,len(file_data)):
        try:
            y.append(int(file_data[i])*5/1024)
        except:pass
    for i in range(len(y)):
        x.append(int(i))
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.plot(x,y,linewidth = 0.5)
    axis.grid()
    return fig

if __name__ == "__main__":
    app.run(host = "192.168.1.72", port = 5000, debug = True)

    

