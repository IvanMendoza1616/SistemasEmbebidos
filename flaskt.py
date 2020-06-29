from flask import Flask, Response, render_template, request, url_for, redirect
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import serial
import os
import time

app = Flask(__name__)

@app.route("/",methods = ["POST","GET"])
@app.route("/home",methods = ["POST","GET"])
def home():
    if request.method == "POST":
        if request.form["submit_button"] == "Plot":
            seconds = request.form["secs"]
            return redirect(url_for("plot",value = int(seconds)))
        else:
            dsPIC = serial.Serial('/dev/ttyS3',115200)
            dsPIC.flushInput()
            dsPIC.flushOutput()
    
            voltage = open('voltage.txt', 'w+b')
            initial_time = time.time()
            while time.time() - initial_time < 1:
                bytesToRead = dsPIC.inWaiting()
                datos = dsPIC.read(bytesToRead)
                voltage.write(datos)
            voltage.close()
            return render_template("actual.html",vf = round(lastvoltage()*5/1024,2))
    else:
        return render_template("home.html")

@app.route('/plot/<value>')
def plot(value = None):
    dsPIC = serial.Serial('/dev/ttyS3',115200)
    dsPIC.flushInput()
    dsPIC.flushOutput()
    
    voltage = open('voltage.txt', 'w+b')
    initial_time = time.time()
    while time.time() - initial_time < int(value):
        bytesToRead = dsPIC.inWaiting()
        datos = dsPIC.read(bytesToRead)
        voltage.write(datos)
    voltage.close()

    fig = create_figure(int(value))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    nname = "plots/temp" + str(time.time()) +  ".png"    
    fig.savefig('static/' +  nname,dpi = 300)

    return render_template("plot.html",vf = round(lastvoltage()*5/1024,2),plotimg = nname,secs = value)

def lastvoltage():
    with open('voltage.txt','r',errors = 'ignore') as file:
        file_data = file.readlines()
    return int(file_data[-2])

def create_figure(s):
    with open('voltage.txt','r',errors = 'ignore') as file:
        file_data = file.readlines()
    x = []
    y = []
    for i in range (len(file_data) - ((s)*2424),len(file_data)-1):
        try:
            y.append(int(file_data[i])*5/1024)
        except:pass
    for i in range(len(y)):
        x.append(int(i)/2424)
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.plot(x,y,linewidth = 0.5)
    axis.grid()
    axis.axis([0,s,0,5])
    return fig

if __name__ == "__main__":
    app.run(host = "192.168.1.72", port = 5000, debug = True)

    

