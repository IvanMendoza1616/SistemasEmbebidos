from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import serial
import os
import time

app = Flask(__name__)

@app.route("/")
def root():
    return 0

@app.route("/home",methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        seconds = request.form["secs"]
        return redirect(url_for("plot",value = int(seconds)))
    else:
        return render_template("home.html")

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
    voltaje = open('voltaje.txt', 'w+b')
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

    nname = "temp" + str(time.time()) +  ".png"
    
    fig.savefig('static/' +  nname,dpi = 100)
    #print(len(vtemp))
    return render_template("plot.html",vf = lastvoltage()*5/1024,plotimg = nname,secs = value)

def lastvoltage():
    with open('voltaje.txt') as file:
        file_data = file.readlines()
    return int(file_data[-2])


def create_figure():
    with open('voltaje.txt') as file:
        file_data = file.readlines()
    x = []
    y = []
    for i in range (1,len(file_data)-1):
        try:
            y.append(int(file_data[i])*5/1024)
        except:pass
    for i in range(len(y)):
        x.append(int(i)/2424)
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.plot(x,y,linewidth = 0.5)
    axis.grid()
    return fig

if __name__ == "__main__":
    app.run(host = "192.168.1.72", port = 5000, debug = True)

    

