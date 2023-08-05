#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20210614
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Functions for reading and writing video files.

Under heavy development, highly unstable.
"""

print('[IO.Video] Loading dependencies...')
try:
    import cv2
except ModuleNotFoundError:
    raise ModuleNotFoundError('This module requires the cv2 module to be installed.')

import os
print('[IO.Video] Done.')

DefaultCodecs = {
    'avi': 'mjpg',
    'mp4': 'h265',
}


# Level 0

def GetFourCC(Str):
    fcc = {f'c{e+1}': el for e,el in enumerate(Codec)}
    FourCC = cv.VideoWriter_fourcc(**fcc)
    return(FourCC)


def Read(File):
    Video = cv2.VideoCapture(File)
    Info = {
        'FPS': int(Video.get(cv2.CAP_PROP_FPS)),
        'Width': int(Video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'Height': int(Video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'FrameNo': int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
    }
    return(Video, Info)


# Level 1

def GetInfo(File):
    Video, Info = Read(File)
    Video.release()
    return(Info)


def Write(Data, FPS, File, Codec='auto'):
    if len(Data.shape) != 4 or 'uint8' not in str(Data.dtype).lower():
        raise TypeError('`Data` must be a 4d array (width, height, RGB, frames) of type `uint8`.')

    if str(Codec).lower() == 'auto':
        Ext = File.split('.')[-1].lower()
        FourCC = GetFourCC(DefaultFourCC[Ext])
    else:
        FourCC = GetFourCC(Codec)

    Dimensions = Data.shape[:2]

    Output = cv2.VideoWriter(
        filename=File,
        fourcc=FourCC,
        fps=FPS,
        frameSize=tuple(Dimensions)
    )

    for Frame in range(Data.shape[3]): Output.write(Data[:,:,:,Frame])
    Output.release()

    return(None)


