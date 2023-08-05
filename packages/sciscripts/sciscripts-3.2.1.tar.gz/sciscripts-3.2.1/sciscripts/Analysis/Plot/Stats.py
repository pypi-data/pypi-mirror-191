#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 2022-07-18
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np

from sciscripts.Analysis import Analysis
from sciscripts.Analysis import Stats
from sciscripts.Analysis.Plot import Plot
plt = Plot.Return('plt')


## Level 0
def pFormat(p): return('p = '+'%.1e' % p)


## Level 1
def Overview(
        Data, FXs, FacNames=None, FacOrder=None, LevelsOrder=None,
        LevelsNames=None, StatsResults=None, SigArg={}, PlotType='BoxPlots',
        Ax=None, AxArgs={}, File='Overview', Ext=['svg'], Save=False, Show=True
    ):

    if FacNames is None: FacNames = [f'Factor{_+1}' for _ in range(FXs.shape[1])]
    if FacOrder is None: FacOrder = FacNames

    FXsOrder = [FXs[:,np.array(FacNames)==_].ravel() for _ in FacOrder]
    FacUniq = [np.unique(_) for _ in FXsOrder]
    if LevelsOrder is None: LevelsOrder = FacUniq
    if LevelsNames is None: LevelsNames = LevelsOrder

    Bars = np.unique(np.array(FXsOrder).T, axis=0)
    for LR,LevelOrder in enumerate(LevelsOrder[::-1]):
        LI = -LR-1
        Bars = np.vstack([Bars[Bars[:,LI]==L,:] for L in LevelOrder])

    X = np.arange(len(LevelsOrder[-1]))
    for L,Level in enumerate(LevelsOrder[:-1][::-1]):
        X = np.array([X+(l*(X[-1]+L+2)) for l,level in enumerate(Level)]).ravel()

    Fig, Ax, ReturnAx = Plot.FigAx(Ax, dict(figsize=Plot.FigSizeA4))

    ym = []
    for B,Bar in enumerate(Bars):
        i = np.prod([FXsOrder[l]==L for l,L in enumerate(Bar)], axis=0, dtype=bool)

        if PlotType == 'BoxPlots':
            Plot.BoxPlots([Data[i]], [X[B]], Width=0.5, Ax=Ax)
            ymax = np.nanmax(Data[i])
        elif PlotType == 'MeanSEM':
            Plot.MeanSEM([Data[i]], [X[B]], {'marker':'s'}, None, Ax=Ax)
            ymax = np.nanmax((
                np.nanmean(Data[i]),
                np.nanstd(Data[i])/(len(Data[i])**0.5)
            ))

        ym.append(ymax)
    ym = np.array(ym)


    # Stats
    ylim = Ax.get_ylim()
    Step = np.ptp(ylim)*0.05

    if StatsResults is not None:

        for F,Fac in enumerate(FacOrder[::-1]):
            F = -F-1
            AR = StatsResults['PWCs'][Fac]
            AR = AR[Stats.spk(AR)]

            kvpk = 'p.adj' if 'p.adj' in AR else 'p'
            fnl = [_ for _ in FacOrder if _ != Fac]
            fi = [list(FacOrder).index(_) for _ in fnl]
            fk = np.array([AR[_] for _ in fnl]).T

            for B,Bar in enumerate(fk):
                p = AR[kvpk][B]
                if p < 0.05:
                    i = np.prod([Bars[:,fi[l]]==L for l,L in enumerate(Bar)], axis=0, dtype=bool)
                    pStart = i*(Bars[:,F]==AR['group1'][B])
                    pEnd = i*(Bars[:,F]==AR['group2'][B])

                    ps, pe = (np.where(_)[0][0] for _ in (pStart,pEnd))

                    y = max(ym[ps:pe])+Step
                    Plot.SignificanceBar(
                        (X[pStart],X[pEnd]), [y]*2,
                        pFormat(p), Ax, SigArg, TicksDir=None, LineTextSpacing=1+Step
                    )
                    ym[ps:pe] = y


    # Text
    xtp = dict(va='top',ha='center')
    Y = min(ylim)-Step

    for xi,x in enumerate(X):
        Ax.text(x, Y, LevelsNames[::-1][0][xi%len(LevelsNames[::-1][0])], xtp)

    Y -= Step
    LenDone, Start = [len(LevelsNames[-1])], 0
    for L,Level in enumerate(LevelsNames[::-1][1:]):
        for xi,x in enumerate(Analysis.MovingAverage(X)[Start::np.prod(LenDone)]):
            Ax.text(x, Y, Level[xi%len(Level)], xtp)
        Y -= Step
        LenDone.append(len(Level))
        Start = np.prod(LenDone[1:])-1

    Ax.xaxis.set_visible(False)
    Ax.spines['bottom'].set_visible(False)

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)



