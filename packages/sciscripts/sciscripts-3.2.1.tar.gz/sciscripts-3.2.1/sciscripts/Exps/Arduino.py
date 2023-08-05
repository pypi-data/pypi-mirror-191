#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20210410
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'Exps.Arduino'
print(f'[{ScriptName}] Loading dependencies...')
import inspect, os
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from datetime import datetime

from sciscripts.IO import Arduino, Txt
print(f'[{ScriptName}] Done.')


def CheckPiezoAndTTL(XLim=(0, 192), YLim=(-5, 1028), FramesPerBuf=192, BaudRate=115200):
    ArduinoObj = Arduino.CreateObj(BaudRate)

    Fig = plt.figure()
    Ax = plt.axes(xlim=XLim, ylim=YLim)

    Plots = [[], []]
    Plots[0] = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]
    Plots[1] = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]

    def AnimInit():
        for Plot in Plots:
            Plot.set_ydata([])
        return Plots

    def PltUp(n):
        Data = [[0]*FramesPerBuf, [0]*FramesPerBuf]
        for Frame in range(FramesPerBuf):
            Temp = ArduinoObj.readline().decode(); Temp = Temp.split()
            if len(Temp) is not 2:
                Temp = [0, 0]
            Data[0][Frame] = Temp[0]; Data[1][Frame] = Temp[1]

        for Index, Plot in enumerate(Plots):
            Plot.set_ydata(Data[Index])

        return tuple(Plots)

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


def Oscilloscope(XLim=(0, 192), YLim=(-5, 1028), FramesPerBuf=192, BaudRate=115200):

    ArduinoObj = Arduino.CreateObj(BaudRate)

    Fig = plt.figure()
    Ax = plt.axes(xlim=XLim, ylim=YLim)
    Plot = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]

    def AnimInit():
        Data = []
        Plot.set_ydata(Data)
        return Plot,

    def PltUp(n):
        Data = []
        for Frame in range(FramesPerBuf):
            Data.append(ArduinoObj.readline())
        Plot.set_ydata(Data)
        return Plot,

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


def ReadAnalogIn(Channels, Rate, Interp=True, FramesPerBuf=128, AnimalName='Animal', FileName='', **Kws):
    """
    Grab serial data and continuously write to a .dat file.

    The shape will be in the filename.
    """
    FunctionName = inspect.stack()[0][3]

    ArduinoObj = Arduino.CreateObj(115200)

    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    if not len(FileName):
        FileName = '-'.join([Date, AnimalName, 'ArduinoRec'])
    InfoFile = f'{FileName}.dict'

    Kws = {**locals()}
    DataInfo = Txt.InfoWrite(**Kws)

    DataLen = 0
    try:
        print(f'[{ScriptName}.{FunctionName}] [00:00:00] Recording..')
        # ThisSec = 1; TimeStart = 0
        while True:
            Data, Time = Arduino.GetSerialData(Channels, Rate, ArduinoObj, FramesPerBuf, Interp)
            # if TimeStart == 0: TimeStart = Time[0]
            # if (Time[-1]-TimeStart)//10 >= ThisSec:
                # ThisTime = datetime.strptime(str(ThisSec*10), '%S').strftime('%H:%M:%S')
                # print(f'[{ScriptName}.{FunctionName}] [{ThisTime}] Recording..')
                # ThisSec += 1
            with open(Date+'.dat', 'ab') as File: File.write(Data.tobytes())
            with open(Date+'_Time.dat', 'ab') as File: File.write(Time.tobytes())
            DataLen += Data.shape[0]

    except KeyboardInterrupt:
        print('Done.')
        pass

    Out = f'{FileName}_{DataLen}x{len(Channels)}.dat'
    os.rename(Date+'.dat', Out)
    Out = f'{FileName}_Time_{DataLen}x1.dat'
    os.rename(Date+'_Time.dat', Out)
    print(f'Recorded to {FileName}*.dat .')


