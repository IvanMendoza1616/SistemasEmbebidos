from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from datetime import datetime
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import serial

app = Flask(__name__)


@app.route("/")
def root():
    return "dsPIC"


@app.route('/plot/<value>')
def plot(value=None):
    dsPIC = serial.Serial('/dev/ttyS3',115200)
    dsPIC.flushInput()
    dsPIC.flushOutput()
    
    voltaje=open('voltaje.txt', 'w+b')
    vtemp = voltaje.readlines()
    while len(vtemp)<int(value)*2424: #2424 valores p/seg dsPIC
        bytesToRead = dsPIC.inWaiting()
        datos=dsPIC.read(bytesToRead)
        print(datos)
        voltaje.write(datos)
        with open('voltaje.txt') as v1:
            vtemp = v1.readlines()

    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    fig.savefig('temp.png', dpi=1000)
    print(len(vtemp))
    
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/read/')
def read():
    dsPIC = serial.Serial('COM4',115200)
    dsPIC.flushInput()
    dsPIC.flushOutput()
    voltaje=open('voltaje.txt', 'w+b')
    while True:
        bytesToRead = dsPIC.inWaiting()
        datos=dsPIC.read(bytesToRead)
        print(datos)
        voltaje.write(datos)
    return ("Nunca")


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    with open('voltaje.txt') as file:
        file_data = file.readlines()
    x = []
    y = []
    for i in range(1,len(file_data)):
        try:
            y.append(int(file_data[i])*5/1024)
        except:pass
    for i in range(len(y)):
        x.append(int(i))
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y, linewidth = 0.5)
    axis.grid()
    return fig


if __name__ == "__main__":
    app.run()

