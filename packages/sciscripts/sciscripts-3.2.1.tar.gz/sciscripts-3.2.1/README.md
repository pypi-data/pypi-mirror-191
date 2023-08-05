# SciScripts  

Scripts for controlling devices/running experiments/analyzing data.


## Background

The package is strongly focused on auditory neuroscience, and consists in three modules: `Analysis`, `Exps` and `IO`. In combination with a hardware setup (documentation comming soon), it allows stimulus delivery, recording control and analysis of several behavioral and electrophysiological techniques, including:  
- Auditory Brainstem Responses (ABRs);  
- Auditory Pre-pulse inhibition (PPI);  
- Gap Pre-pulse Inhibition of Acoustic Startle (GPIAS);  
- Auditory Evoked Response Potentials (aERPs);  
- Extracellular Unit recordings;  
- Local field potentials;  
- General optogenetic and/or sound stimulation.

SciScripts can use a sound card to provide sound stimulation (d'oh!), but also to provide digital triggers (with a simple addition of a diode at the device's input). This allows for, as example, providing combined sound and laser stimulation (see `Examples/SoundAndLaserStimulation.py`). Combined with a real-time kernel and a well setup sound system (documentation comming soon), you can achieve a very precise stimulation, at high sampling rates (192kHz in our system; see [Malfatti et al., 2021, Figure 1](https://www.eneuro.org/content/eneuro/8/1/ENEURO.0413-20.2020/F2.large.jpg)).


### sciscripts.Analysis
Module for calculations, signal processing and plotting. Very useful for analyzing experiments recorded with the `sciscripts.Exps` module. 

Submodules are higher-level functions implementing the lower-level functions at `sciscripts.Analysis.Analysis`.


### sciscripts.Exps  
Module for preparing and running stimulation paradigms for several experiments. Depends on `sciscripts.IO` for generating signals and writing stimulus to data acquisition boards.


### sciscripts.IO
Module for generating signals, interface with input-output cards and reading/writing of several different file types. 

Submodules are higher-level functions implementing the lower-level functions at `sciscripts.IO.IO`.



## Dependencies


### Software
1. OS:  
    - Linux  
    - xdpyinfo [optional]  
    - xrandr [optional]  
2. Python:  
    - asdf  
    - h5py  
    - matplotlib  
    - numpy  
    - pandas  
    - pyserial  
    - scipy  
    - sounddevice  
    - cv2 [optional, needed for video analysis]  
    - rpy2 [optional, needed for statistics]  
    - Klusta [optional, needed for spike clustering analysis]  
    - SpyKING Circus [optional, needed for spike clustering analysis]  


### Hardware
1. Analysis:  
    - [None]  
2. Exps:  
    - Sound card  
    - Arduino Uno [optional, needed for syncing devices and timestamps]  
    - a Data Acquisition card [optional, needed for recordings, tested with Open-ephys DAQ]  
3. IO:  
    - Sound card [for sciscripts.IO.SoundCard]  
    - Arduino Uno [for sciscripts.IO.Arduino]  



## Installation


### Simple

```bash
$ pip install --user sciscripts
```

### Advanced

If you:
- Plan to contribute to the code;  
- Want to change the code and see the results on the fly;  
- Want the most up-to-date version;  

Then run these commands:
```bash
$ git clone https://gitlab.com/malfatti/SciScripts/ -b Dev
$ cd SciScripts/
$ pip install --user -e .
```

This will:
1. Clone the development branch of this repository;  
2. Enter the cloned repository;  
3. Install software dependencies using pip and install SciScripts as a link to the cloned repository.

If you fix/improve something, pull your changes back here! PRs are always welcome.



## Configuration

### Environment variables

For saving experiment info and running analysis, SciScripts expect the variables `DATAPATH` and `ANALYSISPATH` to be set. You can set them by adding the following to `~/.bashrc`, or `~/.profile`, or wherever your desktop environment searches for exported variables:
```bash
export DATAPATH=~/Data
export ANALYSISPATH=~/Analysis
```
changing the path to where you find appropriate.


### Triggering recordings

For running experiments, SciScripts sends TTLs to signal start/stop of recordings through serial to an Arduino Uno. For this to work, the arduino should be programmed using the `SciScripts.ino` file. If no arduino is connected, the experiment will still run, but you will see a console warning, and recordings will have to be triggered manually on your recording system. 

    ############################################################
    ############################################################
    ##                                                        ##
    ##                        DANGER!                         ##
    ##                                                        ##
    ##  If your system has an arduino connected that is NOT   ##
    ##  running `SciScripts.ino`, SciScripts will NOT be      ##
    ##  able to know, so it will send serial commands to the  ##
    ##  connected arduino and it will respond as per its      ##
    ##  programming!                                          ##
    ##                                                        ##
    ##  I am NOT responsible for any damage or injury that    ##
    ##  may happen because you ran SciScripts and your        ##
    ##  arduino triggered a laser and burned your retina; or  ##
    ##  triggered a step motor and crashed a $600 probe, or   ##
    ##  your priceless fingers.                               ##
    ##                                                        ##
    ############################################################
    ############################################################



### Calibrating sound card

For running experiments, SciScripts uses your computer's sound card as a DAQ. To achieve precise input/output, the sound card must be calibrated. Follow the instructions at the `Examples/CalibratingAudioSetup.py` script.



## Examples

The `Examples/` folder contains example scripts (!) of how SciScripts can be used for experiments and analysis. Here is a walkthrough for the `Examples/FilteringAndPlotting.py` script.

Load data from an open-ephys recording folder:
```python
In [1]: import numpy as np

In [2]: from sciscripts.IO import IO

In [3]: from sciscripts.Analysis import Analysis

In [4]: from sciscripts.Analysis.Plot import Plot

In [5]: Folder = 'DataSet/2018-08-13_13-25-45_1416'

In [6]: Data, Rate = IO.DataLoader(Folder)

Loading recording1 ...
Loading recording2 ...
Loading recording3 ...
Loading recording4 ...
Loading recording5 ...
Loading recording6 ...
Loading recording7 ...
Loading recording8 ...
Converting to uV...
```

Select a recording and filter it:
```python
In [7]: Proc = list(Data.keys())[0]             # Select 1st rec processor

In [8]: DataExp = list(Data[Proc].keys())[0]    # Select 1st experiment

In [9]: Rec0 = Data[Proc][DataExp]['0'][:,:8]   # Select the 1st 8 channels

In [10]: Rate0 = Rate[Proc][DataExp]

In [11]: Time0 = np.arange(Rec0.shape[0])/Rate0
```

Plot 50ms of raw channels
```python
In [12]: Plot.AllCh(Rec0[:int(Rate0*0.05),:], Save=True, File='Plot1', Ext=['png'])
```
![](Plot1.png)

Filtering in theta and gamma bands
```python
In [13]: Rec0Theta = Analysis.FilterSignal(Rec0, Rate0, Frequency=[4,12], Order=2)
Filtering channel 1 ...
Filtering channel 2 ...
Filtering channel 3 ...
Filtering channel 4 ...
Filtering channel 5 ...
Filtering channel 6 ...
Filtering channel 7 ...
Filtering channel 8 ...
Filtering channel 9 ...
Filtering channel 10 ...
Filtering channel 11 ...
Filtering channel 12 ...
Filtering channel 13 ...
Filtering channel 14 ...
Filtering channel 15 ...
Filtering channel 16 ...

In [14]: Rec0Gamma = Analysis.FilterSignal(Rec0, Rate0, Frequency=[30,100], Order=3)
Filtering channel 1 ...
Filtering channel 2 ...
Filtering channel 3 ...
Filtering channel 4 ...
Filtering channel 5 ...
Filtering channel 6 ...
Filtering channel 7 ...
Filtering channel 8 ...
Filtering channel 9 ...
Filtering channel 10 ...
Filtering channel 11 ...
Filtering channel 12 ...
Filtering channel 13 ...
Filtering channel 14 ...
Filtering channel 15 ...
Filtering channel 16 ...
```

Plot raw, theta and gamma
```python
In [15]: Window = int(Rate0/2)
    ...: plt = Plot.Return('plt')
    ...: Fig, Axes = plt.subplots(1,3)
    ...: Axes[0] = Plot.AllCh(Rec0[:Window,:], Time0[:Window], Ax=Axes[0], lw=0.7)
    ...: Axes[1] = Plot.AllCh(Rec0Theta[:Window,:], Time0[:Window], Ax=Axes[1], lw=0.7)
    ...: Axes[2] = Plot.AllCh(Rec0Gamma[:Window,:], Time0[:Window], Ax=Axes[2], lw=0.7)
    ...: 
    ...: AxArgs = {'xlabel': 'Time [s]'}
    ...: for Ax in Axes: Plot.Set(Ax=Ax, AxArgs=AxArgs)
    ...: 
    ...: Axes[0].set_ylabel('Voltage [µv]')
    ...: Axes[0].set_title('Raw signal')
    ...: Axes[1].set_title('Theta [4-12Hz]')
    ...: Axes[2].set_title('Gamma [30-100Hz]')
    ...:
    ...: Plot.Set(Fig=Fig)
    ...: Fig.savefig('Plot2.png')
    ...: plt.show()
```
![](Plot2.png)

Scripts using this package for real experiments and analysis can be found at `Examples/`, and at the LabScripts repository, specifically the [Python3/Exps/](https://gitlab.com/malfatti/LabScripts/-/tree/master/Python3/Exps) and [Python3/Analysis/](https://gitlab.com/malfatti/LabScripts/-/tree/master/Python3/Analysis) folders.

