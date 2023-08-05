#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[IO.IO] Loading dependencies...')
import numpy as np, subprocess
from glob import glob
from multiprocessing import Process

from sciscripts.IO import Asdf, Bin, Hdf5, Intan, OpenEphys, Txt
print('[IO.IO] Done.')


def DataLoader(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Processor=None, Experiment=None, Recording=None, Verbose=False):
    FilesExt = [F.split('.')[-1] for F in glob(Folder+'/*.*')]

    if 'kwd' in FilesExt: Data, Rate = OpenEphys.OpenEphys.KwikLoad(Folder, Unit, ChannelMap, ImpedanceFile, Processor, Experiment, Recording, Verbose)
    elif 'dat' in FilesExt: Data, Rate = OpenEphys.Binary.LoadOld(Folder, Unit, ChannelMap, ImpedanceFile, Processor, Experiment, Recording, Verbose)
    elif 'continuous' in FilesExt: Data, Rate = OpenEphys.OpenEphys.OELoad(Folder, Unit, ChannelMap, ImpedanceFile, Processor, Recording, Verbose)
    elif np.unique(FilesExt).tolist() == ['int']: Data, Rate = Intan.FolderLoad(Folder, ChannelMap, Verbose)
    elif Folder[-4:] == '.int': Data, Rate = Intan.Load(Folder, ChannelMap, Verbose)
    elif FilesExt == ['xml']: Data, Rate = OpenEphys.Binary.Load(Folder, Processor, Experiment, Recording, Unit, ChannelMap, ImpedanceFile, Verbose)
    elif Folder[-4:] == '.dat': Data = np.memmap(Folder, Unit); Rate = None
    elif Folder[-5:] == '.asdf' and Asdf.Avail: Data = Asdf.Read(Folder); Rate = None

    elif FilesExt == []:
        SubFolder = sorted(glob(Folder+'/*'))
        if len(SubFolder) == 1:
            Data, Rate = DataLoader(SubFolder[0], Unit, ChannelMap, ImpedanceFile, Processor, Experiment, Recording, Verbose)

    else:
        raise TypeError('Data format not supported.')

    return(Data, Rate)


def DataWriter(Data, Path, Ext):
    if Ext == 'hdf5' and Hdf5.Avail:
        File = Path.split('/')[0] + '.hdf5'
        Hdf5.Write(Data, Path, File)
    elif Ext == 'asdf' and Asdf.Avail:
        File = Path.split('/')[0] + '/' + '_'.join(Path.split('/')[1:]) + '.asdf'
        Asdf.Write(Data, File)
    elif Ext == 'dat':
        Bin.Write(Data, Path)
    elif Ext == 'txt':
        File = Path.split('/')[0] + '/' + '_'.join(Path.split('/')[1:]) + '.txt'
        Txt.Write(Data, Path)
    else:
        raise TypeError('Output format not supported.')

    return(Data, Rate)


def RunProcess(Cmd, LogFile=''):
    if LogFile == '': print('Logging disabled, outputting to STDOUT.')
    else: print('Check progress in file', LogFile)

    try:
        if LogFile == '': Log = subprocess.PIPE
        else:  Log = open(LogFile, 'w')

        P = subprocess.Popen(Cmd,
                             stdout=Log,
                             stderr=subprocess.STDOUT)

        print('Process id:', P.pid )
        P.communicate()[0]; ReturnCode = P.returncode
        if LogFile != '': Log.close()

    except Exception as e:
        ReturnCode = 1; print(e)

    return(ReturnCode)


def MultiProcess(Function, Args, Procs=8, Verbose=False):
    TotalNo = len(Args)
    ProcLists = [[] for _ in range(0, TotalNo, Procs)]

    for A, Arg in enumerate(Args):
        ProcLists[A//Procs].append(Process(target=Function, args=Arg))

    for ProcList in ProcLists:
        for Proc in ProcList:
            Proc.start()
            if Verbose: print('PID =', Proc.pid)
        Proc.join()

    return(None)

