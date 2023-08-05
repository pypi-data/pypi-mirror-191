#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'Analysis.Stats'
print(f'[{ScriptName}] Loading dependencies...')
import inspect, numpy as np
from copy import deepcopy as dcp
from itertools import combinations, product
from scipy import stats as sst
from scipy.special import btdtr, fdtrc
from statsmodels.stats.multitest import multipletests

from sciscripts.Analysis.Analysis import IsInt, SortNatural
from sciscripts.IO.Txt import Print
from sciscripts.IO.Bin import MergeDictsAndContents


try:
    import pandas as pd
    AvailPandas = True
except ModuleNotFoundError as e:
    print(f'[{ScriptName}] {e}: Module `pandas` not available. Some functions will not work.')
    AvailPandas = False

try:
    from unidip import UniDip
    from unidip.dip import diptst
    AvailUnidip = True
except ModuleNotFoundError as e:
    print(f'[{ScriptName}] {e}: Module `unidip` not available. Some functions will not work.')
    AvailUnidip = False

try:
    # Silence R callback
    import rpy2.rinterface_lib.callbacks
    rpy2.rinterface_lib.callbacks.consolewrite_warnerror = lambda *args: None
    rpy2.rinterface_lib.callbacks.consolewrite_print = lambda *args: None

    from rpy2 import robjects as RObj
    from rpy2.robjects import packages as RPkg

    AvailRPy = True
except ModuleNotFoundError as e:
    print(f'[{ScriptName}] {e}: Module `rpy2` not available. Some functions will not work.')
    AvailRPy = False

print(f'[{ScriptName}] Done.')

SubAnovas = ('ANOVA','WelchAnOVa','KruskalWallis','Friedman')
SubPWCs = ('TTest', 'Wilcoxon', 'MannWhitneyU')


#%% Level 0
def _CohensD(DataA, DataB):
    n1, n2 = (len(_) for _ in (DataA, DataB))
    mean1, mean2 = (np.nanmean(_) for _ in (DataA, DataB))
    var1, var2 = (np.nanvar(_) for _ in (DataA, DataB))

    StDAll = (((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))**0.5
    D = (mean1-mean2)/StDAll
    return(D)


def _Friedman(*Data, method="f"):
    """
    Modified from Raphael Vallat (pingouin package)
    @https://github.com/raphaelvallat/pingouin/blob/master/pingouin/nonparametric.py

    to:

    1. Accept a list of arrays;
    2. Return only statistic and p;
    3. Change default method to `f` (Gorsuch and Lehmann, 2017).

    Unlike `scipy.stats.friedmanchisquare`, this implementation allows
    >=2 observations (instead of >=3).
    """
    X = np.array(Data).T
    n, k = X.shape
    ranked = sst.rankdata(X, axis=1)
    ssbn = (ranked.sum(axis=0) ** 2).sum()

    ties = 0
    for i in range(n):
        replist, repnum = sst.find_repeats(X[i])
        for t in repnum:
            ties += t * (t * t - 1)

    W = (
        (12 * ssbn - 3 * n**2 * k * (k + 1) ** 2) /
        (n**2 * k * (k - 1) * (k + 1) - n * ties)
    )

    if method == "chisq":
        Q = n * (k - 1) * W
        ddof1 = k - 1
        p_unc = sst.chi2.sf(Q, ddof1)
        Test = dict(W=W, Q=Q, DFn=ddof1, p=p_unc)
    elif method == "f":
        F = W * (n - 1) / (1 - W)
        ddof1 = k - 1 - 2 / n
        ddof2 = (n - 1) * ddof1
        p_unc = sst.f.sf(F, ddof1, ddof2)
        Test = dict(W=W, F=F, DFn=ddof1, DFd=ddof2, p=p_unc)

    return(Test)


def _WelchAnOVa(*args):
    """
    Modified from duke08542
    @ https://github.com/scipy/scipy/issues/11122

    to export degrees of freedom, f and p.
    """
    args = [np.asarray(arg, dtype=float) for arg in args]
    k = len(args)
    ni =np.array([len(arg) for arg in args])
    mi =np.array([np.mean(arg) for arg in args])
    vi =np.array([np.var(arg,ddof=1) for arg in args])
    wi = ni/vi

    tmp =sum((1-wi/sum(wi))**2 / (ni-1))
    tmp /= (k**2 -1)

    dfbn = k - 1
    dfwn = 1 / (3 * tmp)

    m = sum(mi*wi) / sum(wi)
    f = sum(wi * (mi - m)**2) /((dfbn) * (1 + 2 * (dfbn - 1) * tmp))
    prob = fdtrc(dfbn, dfwn, f)   # equivalent to stats.f.sf

    Test = dict(F=f, DFn=dfbn, DFd=dfwn, p=prob)
    return(Test)


def _KendallsW(*Data):
    """
    Modified from Ugo L.
    @ https://github.com/ugolbck/kendall-w/blob/master/kendall_w/kendall_w.py
    """
    LevelsNo = len(Data)
    if LevelsNo < 2:
        raise ValueError("The number of levels in `Factor` must be >=2.")

    N = [len(_) for _ in Data]
    if len(np.unique(N)) > 1:
        raise ValueError("The number of data points must match between levels of `Factor`.")
    N = N[0]

    Sums = [sum(_) for _ in Data]
    RankSumMean = sum(Sums)/LevelsNo
    SqSum = sum([(_ - RankSumMean)**2 for _ in Sums])
    W = (12*SqSum)/(N**2 * (LevelsNo**3 - LevelsNo))

    return(W)


def FreedmanDiaconis(Signal, IQR=(25, 75)):
    SignalIQR = sst.iqr(Signal, rng=IQR)
    BinWidth = (2 * SignalIQR)/(Signal.shape[0]**(1/3))
    BinSize = np.ptp(Signal)/BinWidth
    return(BinSize, BinWidth)


def GetSigEff(Anova):
    pss = Anova['p']<0.05
    if True in pss:
        pssFacOrder = sorted(
            [_.split(':') for _ in Anova['Effect'][pss]],
            key=lambda x:len(x), reverse=True
        )
        pssFacOrder = [sorted(pssFacOrder[0])]+[
            sorted(p) if len(p)>1 else p for p in pssFacOrder[1:]
            # if not np.prod([_ in pssFacOrder[0] for _ in ['Epoch', 'Class']])
        ]
    else:
        pssFacOrder = []

    return(pssFacOrder)


def IsBalanced(Factor, FactorsGroupBy=[]):
    ThisFactor = np.array(Factor)
    if ThisFactor.dtype == np.dtype('O'):
        raise TypeError('`Factor` should be a list or array of strings!')

    if len(FactorsGroupBy):
        Bal = [[f==fac for fac in np.unique(f)] for f in FactorsGroupBy]
        Bal = [
            np.prod(
                [Bal[e][el] for e,el in enumerate(p)]
                , axis=0
            ).astype(bool)
            for p in product(*(range(len(_)) for _ in Bal))
        ]

        Bal = [
            np.unique([
                ThisFactor[i*(ThisFactor==_)].shape
                for _ in np.unique(ThisFactor)
            ]).shape[0] == 1
            for i in Bal
        ]

        Bal = False not in Bal
    else:
        Bal = [len(ThisFactor[ThisFactor==_]) for _ in np.unique(ThisFactor)]
        Bal = np.unique(Bal).shape[0] == 1


    return(Bal)


def MergeDictList(List):
    TestFCKeys = np.unique([_ for K in List for _ in K.keys()])
    for T,TFC in enumerate(List):
        for K in TestFCKeys:
            if len(TFC.keys())>0 and K not in TFC.keys():
                List[T][K] = np.empty(len(list(TFC.values())[0]))*np.nan
            # elif len(TFC.keys())==0:
                # print(List)
                # raise ValueError('[FixThis] There should not be any empty dicts here!')

        # for tk in Test.keys():
            # if tk not in List and tk not in FactorGBNames:
                # List[tk] = [np.nan]*len(list(List.values())[0])

    Dict = {}
    for TFC in List:
        # if len(TFC.keys())==0: continue
        Dict = MergeDictsAndContents(Dict, TFC)

    return(Dict)


def NaNDrop(Data, Factor, Paired):
    Balanced = False
    if Paired:
        Balanced = True
        FLs = np.unique(Factor)
        fad = [Data[Factor==l] for l in FLs]

        if np.unique([_.shape[0] for _ in fad]).shape[0]!=1:
            Balanced = False

    if Balanced:
        di = np.arange(len(Data))
        dd = [Data[Factor==L] for L in np.unique(Factor)]
        di = [di[Factor==L] for L in np.unique(Factor)]
        Val = np.nanprod([~np.isnan(_) for _ in dd], axis=0).astype(bool)
        Val = np.unique([_ for v in di for _ in v[Val]])
        Valid = np.zeros(len(Data)).astype(bool)
        Valid[Val] = True
    else:
        Valid = ~np.isnan(Data)

    return(Valid)


def OrderKeys(Dict, FactorNames):
    Keys = list(Dict.keys())
    Order = sorted([_ for _ in Keys if _ in FactorNames])
    Order += sorted([_ for _ in Keys if _.startswith('Effect')])
    Order += [_ for _ in Keys if _ == 'nlevels']
    Order += sorted([_ for _ in Keys if _[:5]=='group' and IsInt(_[5:])])
    Order += sorted([_ for _ in Keys if _[0]=='n' and IsInt(_[1:])])
    Order += sorted([
        _ for _ in Keys if (
            _.startswith('max') or
            _.startswith('mean') or
            _.startswith('min') or
            _.startswith('std') or
            _.startswith('sem') or
            _.startswith('var')
        )
    ])
    Order += sorted([_ for _ in Keys if _ in ('DFn','DFd')], reverse=True)
    Order += sorted([_ for _ in Keys if _ not in Order])
    return(Order)


def pFormat(p):
    if p<0.05: return('%.1e' % p)
    else: return(str(round(p,3)))


def Summary(Data, Factor=[], FactorsGroupBy=[], FactorGBNames=[]):
    FunctionName = inspect.stack()[0][3]

    Factor = np.array(Factor)
    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Test = {}
    FLs = np.unique(Factor) if len(Factor) else []

    if len(FLs) == 0:
        Test = {_:[] for _ in FactorGBNames}
        if len(FactorsGroupBy):
            FacPr = tuple(product(*[np.unique(_) for _ in FactorsGroupBy]))

            TestFC = [Test]
            for FC in FacPr:
                i = np.prod([FactorsGroupBy[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
                TFC = Summary(Data[i])

                for fn,FN in enumerate(FactorGBNames):
                    try:
                        TFC[FN].append(FC[fn])
                    except KeyError:
                        TFC[FN] = np.array([FC[fn]]*len(list(TFC.values())[0]))

                TestFC.append(TFC)

            Test = MergeDictList(TestFC)

        else:
            if Data.size>0:
                Test['max'] = [np.nanmax(Data)]
                Test['mean'] = [np.nanmean(Data)]
                Test['min'] = [np.nanmin(Data)]
                Test['n'] = [Data.shape[0]]
                Test['std'] = [np.nanstd(Data)]
                Test['var'] = [np.nanvar(Data, ddof=1)]
            else:
                for k in ('max', 'mean', 'min', 'n', 'std','var'):
                    # if k not in Test: Test[k] = []
                    Test[k] = [np.nan]

        Test = {k:np.array(v) for k,v in Test.items()}
        Test['sem'] = Test['std']/(Test['n']**0.5)

    else:
        if len(FactorsGroupBy):
            Test = {**Test, **{_:[] for _ in FactorGBNames}}
            FacPr = tuple(product(*[np.unique(_) for _ in FactorsGroupBy]))

            TestFC = [Test]
            for FC in FacPr:
                i = np.prod([FactorsGroupBy[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
                TFC = Summary(Data[i], Factor[i])

                for fn,FN in enumerate(FactorGBNames):
                    try:
                        TFC[FN].append(FC[fn])
                    except KeyError:
                        TFC[FN] = np.array([FC[fn]]*len(list(TFC.values())[0]))

                TestFC.append(TFC)

            Test = MergeDictList(TestFC)

        else:
            Test[f'nlevels'] = np.array([len(FLs)])
            for L,FL in enumerate(FLs):
                i = Factor==FL
                Test[f'group{L+1}'] = np.array([FL])
                Test[f'n{L+1}'] = np.array([Data[i].shape[0]])
                Test[f'n{L+1}'] = np.array([Data[i].shape[0]])
                if Data[i].size>0:
                    Test[f'max{L+1}'] = np.array([np.nanmax(Data[i])])
                    Test[f'mean{L+1}'] = np.array([np.nanmean(Data[i])])
                    Test[f'min{L+1}'] = np.array([np.nanmin(Data[i])])
                    Test[f'std{L+1}'] = np.array([np.nanstd(Data[i])])
                    Test[f'var{L+1}'] = np.array([np.nanvar(Data[i], ddof=1)])
                else:
                    for k in ('max', 'mean', 'min', 'std','var'):
                        Test[f'{k}{L+1}'].append(np.nan)

                Test[f'sem{L+1}'] = Test[f'std{L+1}']/(Test[f'n{L+1}']**0.5)

    Test = {K: Test[K] for K in OrderKeys(Test, FactorGBNames)}

    return(Test)


def SummaryPairwise(Data, Factor=[], FactorsGroupBy=[], FactorGBNames=[]):
    FunctionName = inspect.stack()[0][3]
    Factor = np.array(Factor)

    Test = {}
    FLs = np.unique(Factor) if len(Factor) else []
    FacPrL = tuple(combinations(FLs,2))

    if len(FLs) > 2:
        if len(FactorsGroupBy):
            Test = {**Test, **{_:[] for _ in FactorGBNames}}
            FacPr = tuple(product(*[np.unique(_) for _ in FactorsGroupBy]))

            TestFC = [Test]
            for FC in FacPr:
                i = np.prod([FactorsGroupBy[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
                TFC = SummaryPairwise(Data[i], Factor[i])

                for fn,FN in enumerate(FactorGBNames):
                    try:
                        TFC[FN].append(FC[fn])
                    except KeyError:
                        TFC[FN] = np.array([FC[fn]]*len(list(TFC.values())[0]))

                TestFC.append(TFC)

            Test = MergeDictList(TestFC)

        else:
            TestFC = [Test]
            for FC in FacPrL:
                i = np.sum([Factor==L for L in FC], axis=0, dtype=bool)
                TFC = SummaryPairwise(Data[i], Factor[i])
                TestFC.append(TFC)

            Test = MergeDictList(TestFC)

    else:
        Test[f'nlevels'] = np.array([len(FLs)])
        for L,FL in enumerate(FLs):
            i = Factor==FL
            Test[f'group{L+1}'] = np.array([FL])
            Test[f'n{L+1}'] = np.array([Data[i].shape[0]])
            Test[f'n{L+1}'] = np.array([Data[i].shape[0]])
            if Data[i].size>0:
                Test[f'max{L+1}'] = np.array([np.nanmax(Data[i])])
                Test[f'mean{L+1}'] = np.array([np.nanmean(Data[i])])
                Test[f'min{L+1}'] = np.array([np.nanmin(Data[i])])
                Test[f'std{L+1}'] = np.array([np.nanstd(Data[i])])
                Test[f'var{L+1}'] = np.array([np.nanvar(Data[i], ddof=1)])
            else:
                for k in ('max', 'mean', 'min', 'std','var'):
                    Test[f'{k}{L+1}'].append(np.nan)

            Test[f'sem{L+1}'] = Test[f'std{L+1}']/(Test[f'n{L+1}']**0.5)

    Test = {K: Test[K] for K in OrderKeys(Test, [])}

    return(Test)


def PearsonRP2D(Data, Mode='Bottom', Alt='two.sided'):
    # # Slow, stable mode:
    # n = Data.shape[1]
    # r = np.ones((n, n), dtype=float)
    # p = np.ones((n, n), dtype=float)

    # for L in range(n):
    #     for C in range(n):
    #         if L == C:
    #             LCr, LCp = (1,0)
    #         else:
    #             if Mode.lower() == 'bottom' and L < C:
    #                 LCr, LCp = [np.nan]*2
    #             elif Mode.lower() == 'upper' and L > C:
    #                 LCr, LCp = [np.nan]*2
    #             else:
    #                 LCr, LCp = sst.pearsonr(Data[:,L], Data[:,C])

    #         r[L,C], p[L,C] = LCr, LCp

    # Faster, may break in the future because of btdtr
    n, Cols = Data.shape
    r = np.corrcoef(Data.T)
    if Mode.lower() == 'bottom':
        for l in range(r.shape[0]): r[l,l+1:] = np.nan
    elif Mode.lower() == 'upper':
        for l in range(r.shape[0]): r[l,:l+1] = np.nan

    # Taken from scipy.stats.pearsonr
    ab = n/2 - 1
    alternative = Alt.replace('.','-')
    if alternative == 'two-sided':
        p = 2*btdtr(ab, ab, 0.5*(1 - abs(np.float64(r))))
    elif alternative == 'less':
        p = 1 - btdtr(ab, ab, 0.5*(1 - abs(np.float64(r))))
    elif alternative == 'greater':
        p = btdtr(ab, ab, 0.5*(1 - abs(np.float64(r))))
    else:
        raise ValueError('alternative must be one of '
                         '["two-sided", "less", "greater"]')
    return(r, p)


def PToStars(p, Max=3):
    No = 0
    while p < 0.05 and No < Max:
        p *=10
        No +=1

    return(No)


def RAdjustNaNs(Array):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    NaN = RObj.NA_Real
    for I, A in enumerate(Array):
        if A != A: Array[I] = NaN

    return(Array)


def RCheckPackage(Packages):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RPacksToInstall = [Pack for Pack in Packages if not RPkg.isinstalled(Pack)]

    if len(RPacksToInstall) > 0:
        print(f'[{ScriptName}] {str(RPacksToInstall)} not installed. Install now?')
        Ans = input('[y/N]: ')

        if Ans.lower() in ['y', 'yes']:
            from rpy2.robjects.vectors import StrVector as RStrVector

            RUtils = RPkg.importr('utils')
            RUtils.chooseCRANmirror(ind=1)

            RUtils.install_packages(RStrVector(RPacksToInstall))

        else: print(f'[{ScriptName}] Aborted.')

    return(None)


def RModelToDict(Model):
    Dict = {}
    Dict['l'] = []

    for C,Col in Model.items():
        try:
            Dict[C] = np.array(list(Col.iter_labels()))
        except AttributeError:
            if C is None and 'rpy2.robjects.vectors.DataFrame' in str(type(Col)):
                Dict['l'] += [{c: RModelToDict(col) for c,col in Col.items()}]
            elif 'rpy2.robjects.vectors.DataFrame' in str(type(Col)):
                Dict[C] = RModelToDict(Col)
            elif C is None:
                Dict = np.array(Col)
            else:
                Dict[C] = np.array(Col)
        except IndexError:
            continue

    if type(Dict) == dict:
        if not len(Dict['l']): del(Dict['l'])
        if list(Dict.keys()) == ['l']: Dict = Dict['l']

    return(Dict)


def sak(d):
    k = [_ for _ in SubAnovas if _ in d.keys()]
    k = k[0] if len(k) else None
    return(k)


def spk(d):
    k = [_ for _ in SubPWCs if _ in d.keys()]
    k = k[0] if len(k) else None
    return(k)


#%% Level 1
def _RFriedman(Data, Factor, Id, FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj='holm'):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    if 'int' not in str(type(Id[0])):
        _, Id = np.unique(Id,return_inverse=True)

    Values = RObj.FloatVector(Data)
    Idv = RObj.IntVector(Id)
    FactorsV = [RObj.FactorVector(_) for _ in [Factor]+FactorsGroupBy]
    Frame = {([FactorName]+FactorGBNames)[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame['Id'] = Idv
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    RObj.globalenv['Id'] = Idv
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[([FactorName]+FactorGBNames)[F]] = FFactor

    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''

    Model = RObj.r(f'''Frame %>% {fGB} friedman_test(Values~{FactorName}|Id) %>% adjust_pvalue(method="{pAdj}")''')
    Modelc = RObj.r(f'''Frame %>% {fGB} friedman_effsize(Values~{FactorName}|Id)''')

    Result = {'Friedman': RModelToDict(Model), 'FriedmanEffect': RModelToDict(Modelc)}
    Result['Friedman']['Effect'] = np.array([FactorName]*len(Result['Friedman']['p']))
    return(Result)


def _RKruskalWallis(Data, Factor, FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj='holm'):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in [Factor]+FactorsGroupBy]
    Frame = {([FactorName]+FactorGBNames)[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[([FactorName]+FactorGBNames)[F]] = FFactor

    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''

    Model = RObj.r(f'''Frame %>% {fGB} kruskal_test(Values~{FactorName}) %>% adjust_pvalue(method="{pAdj}")''')
    Modelc = RObj.r(f'''Frame %>% {fGB} kruskal_effsize(Values~{FactorName})''')

    Result = {'KruskalWallis': RModelToDict(Model), 'KruskalWallisEffect': RModelToDict(Modelc)}
    Result['KruskalWallis']['Effect'] = np.array([FactorName]*len(Result['KruskalWallis']['p']))
    return(Result)


def _RLevene(Data, Factor, FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj='holm'):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    FunctionName = inspect.stack()[0][3]
    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in [Factor]+FactorsGroupBy]
    Frame = {([FactorName]+FactorGBNames)[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[([FactorName]+FactorGBNames)[F]] = FFactor

    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''

    try:
        Model = RObj.r(f'''Frame %>% {fGB} levene_test(Values~{FactorName}) %>% adjust_pvalue(method="{pAdj}")''')
        Result = {f'{FunctionName}': RModelToDict(Model)}
    except Exception as e:
        print(f"[{ScriptName}.{FunctionName}] Cannot calculate test.")
        Result = {f'{FunctionName}': {}}

    return(Result)


def _RShapiro(Data, Factors, FactorNames=[], pAdj='holm'):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    FunctionName = inspect.stack()[0][3]
    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in Factors]
    Frame = {FactorNames[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,Factor in enumerate(FactorsV): RObj.globalenv[FactorNames[F]] = Factor

    try:
        Model = RObj.r(f'''Frame %>% group_by({','.join(FactorNames)}) %>% shapiro_test(Values) %>% adjust_pvalue(method="{pAdj}")''')
        Result = {f'{FunctionName}': RModelToDict(Model)}
    except Exception as e:
        print(f"[{ScriptName}.{FunctionName}] Cannot calculate test.")
        Result = {f'{FunctionName}': {}}


    return(Result)


def _RTTest(Data, Factor, Paired, FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj= "holm", EqualVar=False, Alt="two.sided", ConfLevel=0.95):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in [Factor]+FactorsGroupBy]
    Frame = {([FactorName]+FactorGBNames)[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[([FactorName]+FactorGBNames)[F]] = FFactor

    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''
    PairedV = 'TRUE' if Paired else 'FALSE'
    EqualVarV = 'TRUE' if EqualVar else 'FALSE'

    try:
        Modelt = RObj.r(f'''Frame %>% {fGB} pairwise_t_test(Values~{FactorName}, paired={PairedV}, var.equal={EqualVarV}, alternative="{Alt}", conf.level={ConfLevel}) %>% adjust_pvalue(method="{pAdj}")''')
    except:
        Modelt = RObj.r(f'''Frame %>% {fGB} pairwise_t_test(Values~{FactorName}, paired={PairedV}, alternative="{Alt}") %>% adjust_pvalue(method="{pAdj}")''')

    Modelc = RObj.r(f'''Frame %>% {fGB} cohens_d(Values~{FactorName}, conf.level={ConfLevel}, var.equal={EqualVarV}, paired={PairedV})''')

    Result = {'TTest': RModelToDict(Modelt), 'CohensD': RModelToDict(Modelc)}
    return(Result)


def _RWilcoxon(Data, Factor, Paired, FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj= "holm", Alt="two.sided", ConfLevel=0.95):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['rstatix','coin']); RPkg.importr('rstatix')

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in [Factor]+FactorsGroupBy]
    Frame = {([FactorName]+FactorGBNames)[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[([FactorName]+FactorGBNames)[F]] = FFactor

    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''
    PairedV = 'TRUE' if Paired else 'FALSE'

    try:
        Modelt = RObj.r(f'''Frame %>% {fGB} pairwise_wilcox_test(Values~{FactorName}, paired={PairedV}, alternative="{Alt}", conf.level={ConfLevel}) %>% adjust_pvalue(method="{pAdj}")''')
    except:
        Modelt = RObj.r(f'''Frame %>% {fGB} pairwise_wilcox_test(Values~{FactorName}, paired={PairedV}, alternative="{Alt}") %>% adjust_pvalue(method="{pAdj}")''')

    Modelc = RObj.r(f'''Frame %>% {fGB} wilcox_effsize(Values~{FactorName}, conf.level={ConfLevel}, paired={PairedV}, alternative="{Alt}")''')

    Result = {'Wilcoxon': RModelToDict(Modelt), 'WilcoxonEffSize': RModelToDict(Modelc)}
    return(Result)


def Calculate(CalcFun, Data, Factor, Paired, Id=[], EffArgs={}, FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Describe=True):
    FunctionName = CalcFun.__name__

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Factor = np.array(Factor)
    Test = {}

    if len(FactorsGroupBy):
        Test = {**Test, **{_:[] for _ in FactorGBNames}}
        FacPr = tuple(product(*[np.unique(_) for _ in FactorsGroupBy]))

        TestFC = [Test]
        for FC in FacPr:
            i = np.prod([FactorsGroupBy[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
            # iFLs = np.unique(Factor[i])
            IdFC = Id[i] if len(Id) else []

            TFC = Calculate(
                CalcFun, Data[i], Factor[i], Paired, IdFC, EffArgs,
                [], [], pAdj, Describe
            )


            for fn,FN in enumerate(FactorGBNames):
                try:
                    TFC[FN].append(FC[fn])
                except KeyError:
                    TFC[FN] = np.array([FC[fn]]*len(list(TFC.values())[0]))

            TestFC.append(TFC)

        Test = MergeDictList(TestFC)

        Test = {k:np.array(v) for k,v in Test.items()}
        if 'p' in Test.keys():
            if 'Effect' in Test.keys():
                EfU = np.unique(Test['Effect'])
                Test['p.adj'] = np.empty(len(Test['p']))*np.nan

                for efu in EfU:
                    i = Test['Effect']==efu
                    Test['p.adj'][i] = multipletests(Test['p'][i], method=pAdj)[1]

            else:
                Test['p.adj'] = multipletests(Test['p'], method=pAdj)[1]

    else:
        Valid = NaNDrop(Data, Factor, Paired)
        DataValid, FacValid = Data[Valid], Factor[Valid]
        try:
            FLs = np.unique(FacValid)
            fad = [DataValid[FacValid==l] for l in FLs]

            if len(Id):
                IdValid = Id[Valid]
                # Ensure subjects are in the right order
                fId = [IdValid[FacValid==l] for l in FLs]
                fIdU = [np.unique(_) for _ in fId]

                SameId = True
                for L,Level in enumerate(fIdU[:-1]):
                    eq = Level.tolist() == fIdU[L+1].tolist()
                    SameId = SameId and eq

                if SameId:
                    fIdOrder = [[np.where(f==uId)[0] for uId in fIdU[0]] for f in fId]
                    Balanced = [False not in [_.shape[0]==1 for _ in f] for f in fIdOrder]
                    Balanced = False not in Balanced
                else:
                    Balanced = False

                if Balanced:
                    fIdOrder = [[_[0] for _ in f] for f in fIdOrder]
                    fad = [Level[fIdOrder[L]] for L,Level in enumerate(fad)]


            EffOut = CalcFun(*fad, **EffArgs)
            try: len(EffOut)
            except: EffOut = [EffOut]

        except Exception as e:
            print(f"[{ScriptName}.{FunctionName}] Cannot calculate test.")
            print(f'[{ScriptName}.{FunctionName}] {e}')
            EffOut = [np.nan]

        Test = Summary(DataValid, FacValid) if Describe else {}
        # Test = Summary(Data, Factor) if Describe else {}

        # if 'nlevels' in Test and Test['nlevels'][0]==1:
            # print('Debug', '-'*50)
            # # print(FactorNames[0], FactorGBNames)
            # print(FacValid)
            # print(Print(DataValid))
            # print('-'*50)

        if type(EffOut) == dict:
            for K,V in EffOut.items():
                try: len(V)
                except:
                    EffOut[K] = np.array([EffOut[K]])

            Test = {**Test, **EffOut}
            if 'p.adj' not in Test.keys() and 'p' in Test.keys():
                Test['p.adj'] = dcp(Test['p'])
        else:
            Test['Statistic'] = np.array([EffOut[0]])

            s = EffOut[0]
            if len(EffOut) == 2:
                p = EffOut[1]
                Test['p'] = np.array([p])
                Test['p.adj'] = np.array([p])

    Result = {K: Test[K] for K in OrderKeys(Test, FactorGBNames)}

    return(Result)


def GetAnovaReport(Result, FacNames):
    FunctionName = inspect.stack()[0][3]
    print(f"[{ScriptName}.{FunctionName}] Deprecated.")
    print(f"[{ScriptName}.{FunctionName}] Run `GetFullReport(Result)` instead.")
    return(None)


def GetEffectReport(Result, FacNames, SigOnly=True):
    Thr = 0.05 if SigOnly else np.inf

    Report = []

    for E,Ef in enumerate(Result['Effect']):
        EM, SM, DFn, DFd, s, p = (
            Result[_][E] for _ in (
                'EffectMethod', 'StatsMethod', 'DFn', 'DFd',
                'Statistic', 'p.adj'
            )
        )

        if p < Thr and s != float('inf'):
            try:
                DFn, DFd = (int(round(_)) for _ in (DFn,DFd))
            except ValueError:
                DFn, DFd = 0, 0

            if DFn==0 or DFd < 2: continue

            s, p = (pFormat(_) for _ in (s,p))

            fns = ' '.join([
                f'{_} {Result[_][E]}' for _ in FacNames
                if _ in Result.keys()
            ])
            if len(fns):
                fns = 'For '+fns+', '
                ec = 'e'
            else:
                ec = 'E'

            Report.append(
                f"    {fns}{ec}ffect of {Ef} ({EM}, {SM}({DFn},{DFd}) = {s}, p = {p})."
            )

    if len(Report):
        # Report = [f'{len(FacNames)}-way analysis of variance:']+Report
        Report = sorted(Report, key=SortNatural)
        Report = '\n'.join(Report)+'\n'
    else:
        Report = ''

    return(Report)


def GetPWCsReport(Result, FacNames, SigOnly=True):
    Thr = 0.05 if SigOnly else np.inf
    Levels = np.unique([Result['group1'], Result['group2']])
    Levels = [_ for _ in Levels if _.lower() != 'nan']
    Pairs = tuple(combinations(Levels,2))

    Keys = (
        'n1', 'n2', 'mean1', 'mean2', 'sem1', 'sem2',
        'group1', 'group2', 'PWCMethod', 'EffectSize', 'p.adj'
    )

    Report = []
    for Pair in Pairs:
        i = np.prod([
            sum([Result[f'group{g}']==_ for _ in Pair])
            for g in ('1','2')
        ], axis=0).astype(bool)

        for ip,p in enumerate(Result['p.adj'][i]):
            if p < Thr:
                fns = ' '.join([
                    f'{_} {Result[_][ip]}' for _ in FacNames
                    if _ in Result.keys()
                ])

                n1,n2,m1,m2,s1,s2,g1,g2,PM,e,p = (
                    Result[_][ip] for _ in Keys
                )

                n1, n2 = (int(_) for _ in (n1,n2))
                m1,m2,s1,s2 = (pFormat(_) for _ in (m1,m2,s1,s2))
                e, p = (pFormat(_) for _ in (e,p))

                d = 'in' if m2>m1 else 'de'

                Report.append(
                    f"    For {fns}, {g2} is {d}creased compared to {g1} (n = {n2} and {n1}; {g2}: {m2}+-{s2}; {g1}: {m1}+-{s1}; {PM} eff. size = {e}; p = {p})."
                )

    if len(Report):
        # Report = ['Pairwise comparisons:']+Report
        Report = sorted(Report, key=SortNatural)
        Report = '\n'.join(Report)+'\n'
    else:
        Report = ''

    return(Report)


def HartigansDip(
        Data, FactorsGroupBy=[], FactorGBNames=[], isHist=False, TestNo=100,
        Alpha=0.05, GetAllIndices=False, pAdj='holm', Describe=True, Verbose=False
    ):
    FunctionName = inspect.stack()[0][3]

    if not AvailUnidip:
        raise ModuleNotFoundError(
            f"[{ScriptName}.{FunctionName}] Module `unidip` not available."
        )

    Test = Summary(Data, [], FactorsGroupBy, FactorGBNames) if Describe else {}

    if Verbose:
        print(f"[{ScriptName}.{FunctionName}] Running {FunctionName} for {TestNo} iterations...")

    if len(FactorsGroupBy):
        Test = {**Test, **{_:[] for _ in FactorGBNames}}
        Test = {**Test, **{_:[] for _ in ('indices','dip','p')}}
        FacPr = tuple(zip(*[Test[_] for _ in FactorGBNames]))

        for fc,FC in enumerate(FacPr):
            if Verbose: print(f"[{ScriptName}.{FunctionName}]     {fc+1} of {len(FacPr)}...")
            i = np.prod([FactorsGroupBy[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
            Res = HartigansDip(Data[i], [], [], isHist, TestNo)

            for K in ('indices','dip','p'):
                Test[K].append(Res[FunctionName][K][0])

            for fn,FN in enumerate(FactorGBNames): Test[FN].append(FC[fn])

        Test = {k:np.array(v) for k,v in Test.items()}
        Test['p.adj'] = multipletests(Test['p'], method=pAdj)[1]

    else:
        Sorted = Data.copy() if isHist else np.msort(Data)
        Dip, p, Index = diptst(Sorted, is_hist=isHist, numt=TestNo)
        Test['dip'] = [Dip]
        Test['p'] = [p]
        if p < Alpha and GetAllIndices:
            if Verbose:
                print(f"[{ScriptName}.{FunctionName}]     Getting dip indices...")

            Index = UniDip(Sorted, is_hist=isHist, ntrials=TestNo, alpha=Alpha).run()

        # if p > Alpha: Index = []
        Index = np.array(Index)
        if len(Index.shape) == 1: Index = Index.reshape((Index.shape[0],1))
        Index = Index.T

        Test['indices'] = Index

    Res = {FunctionName: {K:Test[K] for K in OrderKeys(Test, FactorGBNames)}}
    Res[FunctionName] = {k:np.array(v) for k,v in Res[FunctionName].items()}

    if Verbose:
        print(f"[{ScriptName}.{FunctionName}] Done.")

    return(Res)


def RPCA(Matrix):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['stats']); Rstats = RPkg.importr('stats')
    RMatrix = RObj.Matrix(Matrix)
    PCA = Rstats.princomp(RMatrix)
    return(PCA)


def _RAnOVa(Data, Factors, Id, Paired, FactorNames=[], FactorsGroupBy=[], FactorGBNames=[], pAdj='holm'):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]
    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]
    if 'int' not in str(type(Id[0])):
        _, Id = np.unique(Id,return_inverse=True)

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in Factors+FactorsGroupBy]
    Idv = RObj.IntVector(Id)

    Frame = {(list(FactorNames)+list(FactorGBNames))[f]: F for f,F in enumerate(FactorsV)}
    Frame['Id'] = Idv
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Id'] = Idv
    RObj.globalenv['Values'] = Values
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[(list(FactorNames)+list(FactorGBNames))[F]] = FFactor

    FactorsW = ','.join([FactorNames[_] for _ in range(len(Factors)) if Paired[_]])
    FactorsB = ','.join([FactorNames[_] for _ in range(len(Factors)) if not Paired[_]])
    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''

    Model = RObj.r(f'''invisible(Frame %>% {fGB} anova_test(dv=Values, wid=Id, between=c({FactorsB}), within=c({FactorsW})) %>% adjust_pvalue(method="{pAdj}"))''')
    Result = RModelToDict(Model)

    if 'ANOVA' not in Result.keys() and 'anova' not in Result.keys(): Result = {'ANOVA': Result}
    if 'anova' in Result.keys() and 'ANOVA' not in Result.keys(): Result['ANOVA'] = Result.pop('anova')

    if type(Result['ANOVA']) == list:
        N = np.unique([len(_) for _ in Result.values()])
        if len(N) > 1:
            raise IndexError('All values should have the same length.')

        fKeys = {_ for _ in Result.keys() if _ != 'ANOVA'}
        a = {}
        for n in range(N[0]):
            rKeys = list(Result['ANOVA'][n].keys())
            if 'ANOVA' in rKeys:
                for k in rKeys:
                    if k not in a.keys(): a[k] = {}

                    sKeys = list(Result['ANOVA'][n][k].keys())
                    for s in sKeys:
                        if s not in a[k].keys(): a[k][s] = []
                        a[k][s].append(Result['ANOVA'][n][k][s])

                    for f in fKeys:
                        if f not in a[k].keys(): a[k][f] = []
                        a[k][f].append([Result[f][n]]*Result['ANOVA'][n][k][s].shape[0])
            else:
                if 'ANOVA' not in a.keys(): a['ANOVA'] = {}

                for k in rKeys:
                    if k not in a['ANOVA'].keys(): a['ANOVA'][k] = []
                    kn = Result['ANOVA'][n][k].shape[0] if len(Result['ANOVA'][n][k].shape) else 1

                    if kn==1:
                        a['ANOVA'][k].append([Result['ANOVA'][n][k]])
                    else:
                        a['ANOVA'][k].append(Result['ANOVA'][n][k])

                for f in fKeys:
                    if f not in a['ANOVA'].keys(): a['ANOVA'][f] = []
                    a['ANOVA'][f].append([Result[f][n]]*kn)


        Result = {K: {k: np.concatenate(v) for k,v in V.items()} for K,V in a.items()}

    Result = {T: {K:V for K,V in Test.items() if '<.05' not in K} for T,Test in Result.items()}

    if 'p' in Result['ANOVA'].keys():
        Result['ANOVA']['StatsMethod'] = np.array(['F']*len(Result['ANOVA']['p']))

    if 'F' in Result['ANOVA'].keys():
        Result['ANOVA']['Statistic'] = Result['ANOVA'].pop('F')

    return(Result)


def _RAnOVaAfex(Data, Factors, Paired, Id=[], FactorNames=[]):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RCheckPackage(['afex']); RPkg.importr('afex')

    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in Factors]
    Frame = {FactorNames[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values

    if len(Id):
        Idv = RObj.IntVector(Id)
        RObj.globalenv['Id'] = Idv
        Frame['Id'] = Idv

    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,Factor in enumerate(FactorsV): RObj.globalenv[FactorNames[F]] = Factor

    FactorsW = '*'.join([FactorNames[_] for _ in range(len(Factors)) if Paired[_]])
    FactorsAll = '*'.join(FactorNames)

    Model = RObj.r(f'''aov_car(Values ~ {FactorsAll} + Error(1|Id/({FactorsW})), Frame, na.rm=TRUE)''')
    Result = RModelToDict(Model)
    return(Result)


def _RWelchAnOVa(Data, Factor, FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj='holm'):
    if not AvailRPy:
        raise e(f'[analysis.stats] {e}: module `rpy2` not available.')

    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in [Factor]+FactorsGroupBy]
    Frame = {([FactorName]+FactorGBNames)[f]: F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,FFactor in enumerate(FactorsV):
        RObj.globalenv[([FactorName]+FactorGBNames)[F]] = FFactor

    fGB = f"group_by({','.join(FactorGBNames)}) %>%" if len(FactorsGroupBy) else ''

    Model = RObj.r(f'''Frame %>% {fGB} welch_anova_test(Values~{FactorName}) %>% adjust_pvalue(method="{pAdj}")''')
    Result = {'WelchAnOVa': RModelToDict(Model)}

    for Key in ('<.05','.y.','method','Effect'):
        Result = {T: {K:V for K,V in Test.items() if Key not in K} for T,Test in Result.items()}

    return(Result)


def AnOVaPwr(GroupNo=None, SampleSize=None, Power=None,
           SigLevel=None, EffectSize=None):
    if not AvailRPy:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    FunctionName = inspect.stack()[0][3]
    RCheckPackage(['pwr']); Rpwr = RPkg.importr('pwr')

    if GroupNo is None: GroupNo = RObj.NULL
    if SampleSize is None: SampleSize = RObj.NULL
    if Power is None: Power = RObj.NULL
    if SigLevel is None: SigLevel = RObj.NULL
    if EffectSize is None: EffectSize = RObj.NULL

    Results = Rpwr.pwr_anova_test(k=GroupNo, power=Power, sig_level=SigLevel,
                                  f=EffectSize, n=SampleSize)

    print(f"[{ScriptName}.{FunctionName}] Running {Results.rx('method')[0][0]}...")
    AnOVaResults = {}
    for Key, Value in {'k': 'GroupNo', 'n': 'SampleSize', 'f': 'EffectSize',
                       'power':'Power', 'sig.level': 'SigLevel'}.items():
        AnOVaResults[Value] = Results.rx(Key)[0][0]

    print(f"[{ScriptName}.{FunctionName}] Done.")
    return(AnOVaResults)


def Shapiro(Data, Factors, FactorNames=[], pAdj='holm', Describe=True):
    FunctionName = inspect.stack()[0][3]
    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]

    Factors = [np.array(_) for _ in Factors]
    Test = {}
    sf = sst.shapiro

    Test = {**Test, **{_:[] for _ in FactorNames}}
    Test = {**Test, **{_:[] for _ in ('statistic','p')}}
    FacPr = tuple(product(*[np.unique(_) for _ in Factors]))

    TestFC = [Test]
    for FC in FacPr:
        i = np.prod([Factors[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
        DataValid = Data[i][~np.isnan(Data[i])]
        pdes = Summary(DataValid) if Describe else {}

        try:
            s, p = sf(DataValid)
        except Exception as e:
            Suf = f" for {FC}." if len(FC)<5 else '.'
            print(f"[{ScriptName}.{FunctionName}] Cannot calculate test{Suf}")
            print(f'[{ScriptName}.{FunctionName}] {e}')
            s, p = np.nan, np.nan

        pdes['statistic'] = np.array([s])
        pdes['p'] = np.array([p])

        for fn,FN in enumerate(FactorNames): pdes[FN] = np.array([FC[fn]])
        TestFC.append(pdes)

    Test = MergeDictList(TestFC)

    Test = {k:np.array(v) for k,v in Test.items()}
    Test['p.adj'] = multipletests(Test['p'], method=pAdj)[1]

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorNames)
    }}

    return(Result)


#%% Level 2
def CalculatePairwise(CalcFun, Data, Factor, Paired, Id=[], EffArgs={}, FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Describe=True):
    FunctionName = CalcFun.__name__

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Factor = np.array(Factor)
    FLs = np.unique(Factor)

    Test = {}

    if len(FLs) < 2:
        if Describe:
            Test = Summary(Data, Factor, FactorsGroupBy, FactorGBNames)

        print(f"[{ScriptName}.{FunctionName}] Cannot calculate test.")
        print(f'[{ScriptName}.{FunctionName}] The number of levels in `Factor` must be at least 2.')
        return(Test)

    elif len(FLs) > 2:
        FLPairs = list(combinations(FLs,2))
        Res = [Test]

        for FLPair in FLPairs:
            FLi = (Factor==FLPair[0])+(Factor==FLPair[1])
            IdFL = Id[FLi] if len(Id) else []
            FGB = [_[FLi] for _ in FactorsGroupBy]

            TestFL = Calculate(
                CalcFun, Data[FLi], Factor[FLi], Paired, IdFL, EffArgs,
                FGB, FactorGBNames, pAdj, Describe
            )

            Res.append(TestFL)

        Test = MergeDictList(Res)

        if 'p' in Test.keys():
            Test['p.adj'] = multipletests(Test['p'], method=pAdj)[1]


    else:
        Test = Calculate(
            CalcFun, Data, Factor, Paired, Id, EffArgs,
            FactorsGroupBy, FactorGBNames, pAdj, Describe
        )

    return(Test)


def Friedman(Data, Factor, Id, FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Method='F', Describe=True):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Factor = np.array(Factor)
    FLs = np.unique(Factor)

    sf = _Friedman
    sfa = {'method': Method.lower()}
    # sf = sst.friedmanchisq
    # sfa = {}

    Test = Calculate(
        _Friedman, Data, Factor, True, Id, sfa,
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    # Desc = Test if Describe else Summary(Data, Factor, FactorsGroupBy, FactorGBNames)
    # Test['EffectSize'] = Test['Statistic']/(Desc['n1']*(len(FLs)-1))
    # Test['EffectSizeMethod'] = np.array(['Kendall W']*len(Desc['n1']))

    sk = 'Q' if Method=='ChiSq' else 'F'
    Test['Statistic'] = Test.pop(sk)
    Test['EffectSize'] = Test.pop('W')
    Test['StatsMethod'] = np.array([Method]*len(Test['p']))
    Test['EffectSizeMethod'] = np.array(['KendallsW']*len(Test['p']))

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def GetFullReport(Result, SigOnly=True):
    FunctionName = inspect.stack()[0][3]
    Report = ''

    if 'Effect' not in Result or type(Result['Effect']) != dict:
        print(f'[{FunctionName}] No `Effect` dict found in `Result` dict.')
        return(Report)

    FacNames = np.unique([
        _ for _ in Result['Effect']['Effect'] if ':' not in _
    ])

    r = GetEffectReport(Result['Effect'], FacNames, SigOnly)
    if len(r):
        r = f'{len(FacNames)}-way analysis of variance:\n'+r

    Report += r

    if 'FXs' in Result:
        for fx,FX in Result['FXs'].items():
            r = GetEffectReport(FX['Effect'], FacNames, SigOnly)
            if len(r): r = f'{fx} analysis of variance:\n'+r
            Report += r

    if 'PWCs' in Result:
        for pwc,PWC in Result['PWCs'].items():
            r = GetPWCsReport(PWC['PWCs'], FacNames, SigOnly)
            if len(r): r = f'{pwc} pairwise comparisons:\n'+r
            Report += r

    return(Report)



def KendallsW(Data, Factor, FactorsGroupBy=[], FactorGBNames=[], Describe=True):
    FunctionName = inspect.stack()[0][3]
    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Test = Calculate(
        _KendallsW, Data, Factor, True, [], {},
        FactorsGroupBy, FactorGBNames, '', Describe
    )

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def KruskalWallis(Data, Factor, FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Method='F', Describe=True):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Factor = np.array(Factor)
    FLs = np.unique(Factor)

    Test = Calculate(
        sst.kruskal, Data, Factor, False, [], {'nan_policy':'omit'},
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Desc = Test if Describe else Summary(Data, Factor, FactorsGroupBy, FactorGBNames)
    n = sum([v[0] for k,v in Desc.items() if k[0]=='n' and IsInt(k[1:])])

    if Method=='ChiSq':
        Test['DF'] = np.repeat([len(FLs)-1], len(Test['p']))

        # eta squared based on the H-statistic (Tomczak and Tomczak, 2014)
        Test['EffectSize'] = (Test['Statistic']-len(FLs)+1)/(n-(len(FLs)))
        Test['EffectSizeMethod'] = np.array(['eta2[H]']*len(Test['p']))

    else:
        DFn = len(FLs)-1
        DFd = n-len(FLs)
        Test['DFn'] = np.repeat([DFn], len(Test['p']))
        Test['DFd'] = np.repeat([DFd], len(Test['p']))
        Test['Statistic'] = sst.f.ppf(1-Test['p'], dfn=Test['DFn'], dfd=Test['DFd'])

        # Partial eta squared based on F (Cohen, 1965; Lakens 2013)
        Test['EffectSize'] = (
            (Test['Statistic'] * Test['DFn']) /
            (Test['Statistic'] * Test['DFn'] + Test['DFd'])
        )

        Test['EffectSizeMethod'] = np.array(['eta2[F]']*len(Test['p']))

    Test['StatsMethod'] = np.array([Method]*len(Test['p']))

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def IsNormal(Data, Factors, pAdj, FactorNames=[]):
    FunctionName = inspect.stack()[0][3]

    Res = Shapiro(Data, Factors, FactorNames, pAdj)
    if 'p.adj' in Res['Shapiro'].keys():
        IN = np.nanmin(Res['Shapiro']['p.adj'])>0.05
    else:
        print(f"[{ScriptName}.{FunctionName}] Assuming normally-distributed samples.")
        IN = True

    return(IN, Res)


def Levene(Data, Factors, FactorNames=[], FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Center='auto', Describe=True):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    if Center == 'auto':
        IN = IsNormal(Data, Factors, pAdj, FactorNames)[0]
        LCenter = 'mean' if IN else 'median'

    else:
        LCenter = Center

    if len(Factors) == 1:
        FLs = np.unique(Factors[0])
        sfa = {'center': LCenter}

        Test = Calculate(
            sst.levene, Data, Factors[0], False, [], sfa,
            FactorsGroupBy, FactorGBNames, pAdj, Describe
        )

        # print('Debug', '-'*50)
        # print(FactorNames[0], FactorGBNames)
        # print(Print(Test))
        # print('-'*50)

        n1 = [v for k,v in Test.items() if k[0]=='n' and IsInt(k[1:])]
        Desc = Test if Describe else Summary(Data, Factors[0], FactorsGroupBy, FactorGBNames)

        n = [v for k,v in Desc.items() if k[0]=='n' and IsInt(k[1:])]
        # print(Describe)
        Test['DFn'] = Desc['nlevels']-1
        try:
            Test['DFd'] = sum(n) - len(FLs)
        except Exception as e:
            print(Print(Test), FactorGBNames)
            print(Print({K:V.shape[0] for K,V in Test.items()}))
            print(n, n1)
            raise Exception(e)
        # print(FactorNames, FactorGBNames)
        # print(Data)
        # print('='*50)
    else:
        Test = []
        for F,Factor in enumerate(Factors):
            FLs = np.unique(Factor)

            TestFC = Levene(
                Data, [Factor], [FactorNames[F]], FactorsGroupBy,
                FactorGBNames, pAdj, LCenter, Describe=False
            )['Levene']

            TestFC['Factor'] = [FactorNames[F]]*len(TestFC['p'])
            TestFC['nlevels'] = [len(FLs)]*len(TestFC['p'])
            Test.append(TestFC)

        Test = MergeDictList(Test)

        if 'p' in Test.keys():
            Test['p.adj'] = multipletests(Test['p'], method=pAdj)[1]

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def WelchAnOVa(Data, Factor, FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Describe=True):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Factor = np.array(Factor)
    FLs = np.unique(Factor)

    Test = Calculate(
        _WelchAnOVa, Data, Factor, True, [], {},
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Test['Statistic'] = Test.pop('F')
    Test['StatsMethod'] = np.array(['F']*len(Test['p']))

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


#%% Level 3
def CohensD(Data, Factor, FactorsGroupBy=[], FactorGBNames=[], Describe=True):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    Test = CalculatePairwise(
        _CohensD, Data, Factor, False, [], {},
        FactorsGroupBy, FactorGBNames, '', Describe
    )

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def KolmogorovSmirnov(
        Data, Factor='norm', FactorsGroupBy=[],
        FactorGBNames=[], pAdj='holm', Alt="two.sided", Mode='auto',
        Describe=True
    ):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    sfa = {'alternative': Alt.replace('.','-'), 'mode': Mode}

    if type(Factor) == str:
        Test = Summary(Data, Factor, [], []) if Describe else {}
        s, p = sst.kstest(Data, Factor, **sfa)
        Test['Statistic'] = np.array([s])
        Test['p'] = np.array([p])

    else:
        Test = CalculatePairwise(
            sst.kstest, Data, Factor, False, [], sfa,
            FactorsGroupBy, FactorGBNames, pAdj, Describe
        )

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def MannWhitneyU(
        Data, Factor, FactorsGroupBy=[],
        FactorGBNames=[], pAdj= "holm", Alt="two.sided", Describe=True
    ):

    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    sfa = {'alternative': Alt.replace('.','-'), 'nan_policy':'omit'}

    Test = CalculatePairwise(
        sst.mannwhitneyu, Data, Factor, False, [], sfa,
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Test['t-statistic'] = Test.pop('Statistic')
    Test['z-statistic'] = sst.norm.isf(Test['p']/2)

    Desc = Test if Describe else SummaryPairwise(Data, Factor, FactorsGroupBy, FactorGBNames)
    EffSizeN = Desc['n1']+Desc['n2']
    Test['EffectSize'] = Test['z-statistic']/(EffSizeN**0.5)

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def PearsonR(
        Data, Factor, FactorsGroupBy=[], FactorGBNames=[],
        pAdj= "holm", Alt="two.sided", Describe=True
    ):

    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    sfa = {'alternative': Alt.replace('.','-')}

    Test = CalculatePairwise(
        sst.pearsonr, Data, Factor, True, [], sfa,
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Desc = Test if Describe else Summary(Data, Factor, FactorsGroupBy, FactorGBNames)
    Test['df'] = Desc['n1']-2

    if 'Statistic' in Test.keys():
        Test['r'] = Test.pop('Statistic')

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def SpearmanR(
        Data, Factor, FactorsGroupBy=[], FactorGBNames=[],
        pAdj= "holm", Alt="two.sided", Describe=True
    ):

    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    sfa = {'alternative': Alt.replace('.','-')}

    Test = CalculatePairwise(
        sst.spearmanr, Data, Factor, True, [], sfa,
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Test['r'] = Test.pop('Statistic')

    Desc = Test if Describe else Summary(Data, Factor, FactorsGroupBy, FactorGBNames)
    Test['df'] = Desc['n1']-2

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def TTest(
        Data, Factor, Paired,
        FactorsGroupBy=[], FactorGBNames=[], pAdj= "holm", EqualVar=False,
        Alt="two.sided", Describe=True
    ):
    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    sf = sst.ttest_rel if Paired else sst.ttest_ind
    sfa = {'alternative': Alt.replace('.','-'), 'nan_policy':'omit'}
    if not Paired: sfa['equal_var'] = EqualVar

    Test = CalculatePairwise(
        sf, Data, Factor, Paired, [], sfa,
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Eff = CohensD(Data, Factor, FactorsGroupBy, FactorGBNames, Describe)
    Test['EffectSize'] = Eff['CohensD']['Statistic']
    Test['EffectSizeMethod'] = np.array(['CohensD']*len(Test['p']))

    Desc = Test if Describe else Summary(Data, Factor, FactorsGroupBy, FactorGBNames)

    if Paired: Test['df'] = Desc['n1']-1
    else:
        n1 = Desc['n1']
        n2 = Desc['n2']
        v1 = Desc['var1']
        v2 = Desc['var2']

        if EqualVar:
            df, _ = sst._stats_py._equal_var_ttest_denom(v1, n1, v2, n2)
        else:
            df, _ = sst._stats_py._unequal_var_ttest_denom(v1, n1, v2, n2)

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def TukeyHSD(Data, Factor, FactorsGroupBy=[], FactorGBNames=[], Describe=True):
    FunctionName = inspect.stack()[0][3]

    Factor = np.array(Factor)
    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    if len(FactorsGroupBy):
        Test = {_:[] for _ in FactorGBNames}
        FacPr = tuple(product(*[np.unique(_) for _ in FactorsGroupBy]))

        TestFC = [Test]
        for FC in FacPr:
            i = np.prod([FactorsGroupBy[l]==L for l,L in enumerate(FC)], axis=0, dtype=bool)
            FactorNameFC = ':'.join(FC)

            TFC = TukeyHSD(
                Data[i], Factor[i], [], [], Describe
            )[FunctionName]

            for fn,FN in enumerate(FactorGBNames):
                try:
                    TFC[FN] += [FC[fn]]*len(TFC['p'])
                except KeyError:
                    TFC[FN] = np.array([FC[fn]]*len(TFC['p']))

            TestFC.append(TFC)

        Test = MergeDictList(TestFC)

    else:
        FLs = np.unique(Factor).tolist()
        All = [Data[Factor==L] for L in FLs]
        hsd = sst.tukey_hsd(*All)

        FacPr = tuple(combinations(FLs,2))

        if Describe:
            Test = SummaryPairwise(Data, Factor, FactorsGroupBy, FactorGBNames)
        else:
            Test = {
                f'group{G+1}': np.array([Pair[G] for Pair in FacPr])
                for G in range(2)
            }

        Test['Statistic'] = [np.nan for _ in Test['group1']]
        Test['p'] = [np.nan for _ in Test['group1']]
        for FC in FacPr:
            i, j = (FLs.index(_) for _ in (FC[0],FC[1]))

            G1 = (Test['group1']==FC[0])+(Test['group2']==FC[0])
            G2 = (Test['group1']==FC[1])+(Test['group2']==FC[1])
            G = np.where(G1*G2)[0]
            if len(G) != 1:
                raise ValueError(f'[{ScriptName}.{FunctionName}] Levels not matching.')
            G = G[0]

            Test['Statistic'][G] = hsd.statistic[i,j]
            Test['p'][G] = hsd.pvalue[i,j]

        Eff = CohensD(Data, Factor, FactorsGroupBy, FactorGBNames, Describe=True)
        Eff = Eff['CohensD']

        Test['EffectSize'] = [np.nan for _ in Test['p']]
        for d,D in enumerate(Eff['Statistic']):
            i = np.where((
                (np.array(Test['group1'])==Eff['group1'][d]) *
                (np.array(Test['group2'])==Eff['group2'][d])
            ))[0]
            if len(i) != 1:
                raise ValueError(f'[{ScriptName}.{FunctionName} CohensD not matching TukeyHSD.')

            i = i[0]
            Test['EffectSize'][i] = D

        Test['EffectSizeMethod'] = np.array(['CohensD']*len(Test['p']))
    Test['p.adj'] = dcp(Test['p'])

    Result = {FunctionName: {
        K: np.array(Test[K]) for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


def Wilcoxon(
        Data, Factor, FactorsGroupBy=[],
        FactorGBNames=[], pAdj= "holm", Alt="two.sided", Describe=True
    ):

    FunctionName = inspect.stack()[0][3]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    sfa = {'alternative': Alt.replace('.','-'), 'nan_policy':'omit'}

    Test = CalculatePairwise(
        sst.wilcoxon, Data, Factor, True, [], sfa,
        FactorsGroupBy, FactorGBNames, pAdj, Describe
    )

    Test['t-statistic'] = Test.pop('Statistic')
    Test['z-statistic'] = sst.norm.isf(Test['p']/2)

    Desc = Test if Describe else SummaryPairwise(Data, Factor, FactorsGroupBy, FactorGBNames)

    EffSizeN = Desc['n1']
    Test['EffectSize'] = Test['z-statistic']/(EffSizeN**0.5)

    Result = {FunctionName: {
        K:Test[K] for K in OrderKeys(Test, FactorGBNames)
    }}

    return(Result)


#%% Level 4
def Correlation(
        Data, Factor, Paired, Parametric='auto', FactorName='Factor',
        FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Alt="two.sided",
        Describe=True
    ):
    FunctionName = inspect.stack()[0][3]

    if Parametric == 'auto':
        IN, Results = IsNormal(Data, [Factor], pAdj, [FactorName])
    else:
        Results = {}
        IN = Parametric

    sf = PearsonR if IN else SpearmanR
    Corrs = sf(
        Data, Factor, FactorsGroupBy,
        FactorGBNames, pAdj, Alt, Describe
    )

    Results = {**Results, **Corrs}

    return(Results)


def PairwiseComp(Data, Factor, Paired, Parametric='auto', FactorName='Factor', FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Alt="two.sided", Describe=True):
    FunctionName = inspect.stack()[0][3]

    if Parametric == 'auto':
        IN, Results = IsNormal(Data, [Factor], pAdj, [FactorName])
    else:
        Results = {}
        IN = Parametric

    LCenter = 'mean' if IN else 'median'

    IsEqVar = Levene(Data, [Factor], [FactorName], FactorsGroupBy, FactorGBNames, pAdj, LCenter, Describe)
    if 'p.adj' in IsEqVar['Levene'].keys():
        Results.update(IsEqVar)
        IsEqVar = np.nanmin(IsEqVar['Levene']['p.adj'])>0.05
    else:
        print(f"[{ScriptName}.{FunctionName}] Assuming unequal variances.")
        IsEqVar = False


    Bal = IsBalanced(Factor, FactorsGroupBy)

    fn = FunctionName
    try:
        if IN:
            Valid = NaNDrop(Data, Factor, Paired)
            DataValid, FacValid = Data[Valid], Factor[Valid]
            FGBValid = [_[Valid] for _ in FactorsGroupBy]
            BalValid = IsBalanced(FacValid, FGBValid)

            if not Paired and Bal and BalValid:
                fn = 'TukeyHSD'
                PWCs = TukeyHSD(
                    DataValid, FacValid, FGBValid, FactorGBNames, Describe
                )
            else:
                fn = 'TTest'
                PWCs = TTest(
                    Data, Factor, Paired*Bal, FactorsGroupBy, FactorGBNames, pAdj, IsEqVar, Alt, Describe
                )
        else:
            if Paired and Bal:
                fn = 'Wilcoxon'
                PWCs = Wilcoxon(
                    Data, Factor, FactorsGroupBy, FactorGBNames, pAdj, Alt, Describe
                )
            else:
                if Paired and not Bal:
                    print(f"[{ScriptName}.{FunctionName}] Data paired but not balanced. Assuming independent samples.")

                fn = 'MannWhitneyU'
                PWCs = MannWhitneyU(
                    Data, Factor, FactorsGroupBy, FactorGBNames, pAdj, Alt, Describe
                )

        if len(PWCs):
            K = fn
            PWCs = PWCs[K]
            PWCs['PWCMethod'] = np.array([K]*len(PWCs['p']))
            PWCs = {'PWCs': PWCs}

    except Exception as e:
        print(f"[{ScriptName}.{fn}] Cannot calculate test for {FactorName}.")
        print(f'[{ScriptName}.{fn}] {e}')
        PWCs = {}

    Results = {**Results, **PWCs}

    return(Results)


def Effect(Data, Factors, Id, Paired, Parametric='auto', FactorNames=[], FactorsGroupBy=[], FactorGBNames=[], pAdj='holm', Alt="two.sided", Describe=True):
    FunctionName = inspect.stack()[0][3]
    Factors = [np.array(_) for _ in Factors]

    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]

    if not len(FactorGBNames):
        FactorGBNames = [f'FactorGB{_+1}' for _ in range(len(FactorsGroupBy))]

    if 'int' not in str(type(Id[0])):
        _, Id = np.unique(Id,return_inverse=True)

    Factors = list(Factors)
    for F,Factor in enumerate(Factors):
        if 'str' not in str(type(Factor[0])):
            Factors[F] = np.array(Factor).astype(str)

    if Parametric == 'auto':
        IN, Results = IsNormal(Data, Factors, pAdj, FactorNames)
    else:
        Results = {}
        IN = Parametric

    LCenter = 'mean' if IN else 'median'

    IsEqVarL = Levene(Data, Factors, FactorNames, FactorsGroupBy, FactorGBNames, pAdj, LCenter, Describe)
    if 'p.adj' in IsEqVarL['Levene'].keys():
        IsEqVar = np.nanmin(IsEqVarL['Levene']['p.adj'])>0.05
    else:
        print(f"[{ScriptName}.{FunctionName}] Assuming unequal variances.")
        IsEqVar = False

    if 'p.adj' in IsEqVarL['Levene'].keys():
        Results.update(IsEqVarL)

    if len(Factors) == 1:
        fn = FunctionName
        try:
            Bal = IsBalanced(Factors[0], FactorsGroupBy)
            FLs = np.unique(Factors[0])

            if IN:# and IsEqVar: # _RAnOVa already corrects for unequal variance
                fn = '_RAnOVa'
                try:
                    Test = _RAnOVa(Data, Factors, Id, Paired, FactorNames, FactorsGroupBy, FactorGBNames, pAdj)
                except Exception as e:
                    print(f"[{ScriptName}.{fn}] Cannot calculate test for {FactorNames[0]}.")
                    print(f'[{ScriptName}.{fn}] {e}')
                    Test = {}

            # elif IN and not IsEqVar:
                # fn = 'WelchAnOVa'
                # Test = WelchAnOVa(Data, Factors[0], FactorNames[0], FactorsGroupBy, FactorGBNames, pAdj)

            elif Bal and Paired[0]:
                fn = 'Friedman'
                Test = Friedman(Data, Factors[0], Id, FactorsGroupBy, FactorGBNames, pAdj, 'F', Describe=False)

            else:
                fn = 'KruskalWallis'
                Test = KruskalWallis(Data, Factors[0], FactorsGroupBy, FactorGBNames, pAdj, 'F', Describe=False)

            if len(Test):
                K = sak(Test)
                Results = {**Results, **{k:v for k,v in Test.items() if k!=K}}
                Test = Test[K]
                Test['EffectMethod'] = np.array([K]*len(Test['p']))
                Test['Effect'] = np.array([FactorNames[0]]*len(Test['p']))
        except Exception as e:
            print(f"[{ScriptName}.{fn}] Cannot calculate test for {FactorNames[0]}.")
            print(f'[{ScriptName}.{fn}] {e}')
            Test = {}

    else:
        if IN:
            fn = '_RAnOVa'
            try:
                Test = _RAnOVa(Data, Factors, Id, Paired, FactorNames, FactorsGroupBy, FactorGBNames, pAdj)
                K = sak(Test)
                Results = {**Results, **{k:v for k,v in Test.items() if k!=K}}
                Test = Test[K]
                Test['EffectMethod'] = np.array([K]*len(Test['p']))
            except Exception as e:
                print(f"[{ScriptName}.{fn}] Cannot calculate test for {':'.join(FactorNames)}.")
                print(f'[{ScriptName}.{fn}] {e}')
                Test = {}
        else:
            Tests = []
            for F,Factor in enumerate(Factors):
                TestFC = Effect(
                    Data, [Factor], Id, [Paired[F]], IN, [FactorNames[F]],
                    FactorsGroupBy, FactorGBNames, pAdj, Alt, Describe=False
                )
                Tests.append(TestFC)

            Tests = MergeDictList(Tests)

            Test = Tests['Effect']


    if 'Effect' in Test.keys() and 'p' in Test.keys():
        EfU = np.unique(Test['Effect'])
        Test['p.adj'] = np.empty(len(Test['p']))*np.nan

        for efu in EfU:
            i = Test['Effect']==efu
            Test['p.adj'][i] = multipletests(Test['p'][i], method=pAdj)[1]

    # Results = {**Results, **Test}
    Results[FunctionName] = {
        K:Test[K] for K in OrderKeys(Test, list(FactorNames)+list(FactorGBNames))
    }

    return(Results)



#%% Level 5
def Full(Data, Factors, Id, Paired=[], Parametric='auto', FactorNames=[], pAdj='holm', Describe=True):
    FunctionName = inspect.stack()[0][3]

    Factors = [np.array(_) for _ in Factors]
    if not len(Paired):
        print(f"[{ScriptName}.{FunctionName}] Assuming all factors are between-subject (unpaired).")
        Paired = [False for _ in Factors]

    if not len(FactorNames):
        FactorNames = [f'Factor{_+1}' for _ in range(len(Factors))]

    if 'int' not in str(type(Id[0])):
        _, Id = np.unique(Id,return_inverse=True)

    Factors = list(Factors)
    for F,Factor in enumerate(Factors):
        if 'str' not in str(type(Factor[0])):
            Factors[F] = np.array(Factor).astype(str)


    print(f"[{ScriptName}.{FunctionName}] Getting full AnOVa...")
    Results = Effect(Data, Factors, Id, Paired, Parametric, FactorNames, [], [], pAdj, Describe=Describe)


    if Parametric == 'auto':
        IN = np.nanmin(Results['Shapiro']['p.adj'])>0.05
    else:
        IN = Parametric

    LCenter = 'mean' if IN else 'median'
    IsEqVar = np.nanmin(Results['Levene']['p.adj'])>0.05

    FactorsWi = [_ for _ in range(len(FactorNames)) if Paired[_]]
    FactorsBi = [_ for _ in range(len(FactorNames)) if not Paired[_]]
    FactorsW = [FactorNames[_] for _ in FactorsWi]
    FactorsB = [FactorNames[_] for _ in FactorsBi]

    Combs = [
        ':'.join(_)
        for c in range(len(FactorNames))
        for _ in combinations(FactorNames,c+1)
    ]
    FullpsFacOrder = sorted(
        (_.split(':') for _ in Combs),
        key=lambda x:len(x), reverse=True
    )
    FullpsFacOrder = [sorted(FullpsFacOrder[0])]+[
        sorted(p) if len(p)>1 else p for p in FullpsFacOrder[1:]
    ]

    FullpsFacOrder = [_ for _ in FullpsFacOrder if len(_) != len(Factors)]
    ToRun = dcp(FullpsFacOrder)
    SubCs, PWCs, Corrs = {}, {}, {}

    if len(Factors) == 1:
        print(f"[{ScriptName}.{FunctionName}] Getting pairwise comparisons...")
        PWCs[FactorNames[0]] = PairwiseComp(Data, Factors[0], Paired[0], IN, FactorNames[0], pAdj=pAdj, Describe=Describe)
    else:
        print(f"[{ScriptName}.{FunctionName}] Getting sub-AnOVas and pairwise comparisons...")
        while len(ToRun):
            PS = ToRun[0]
            PSs = ':'.join(PS)

            psGB = [Factors[FactorNames.index(_)] for _ in FactorNames if _ not in PS]
            psGBNames = [_ for _ in FactorNames if _ not in PS]
            psWB = [Factors[FactorNames.index(_)] for _ in PS]
            psPaired = [Paired[FactorNames.index(_)] for _ in PS]

            if len(PS) == 1:
                FInd = FactorNames.index(PS[0])

                SubCs[PSs] = Effect(Data, psWB, Id, psPaired, IN, PS, psGB, psGBNames, pAdj, Describe=Describe)
                PWCs[PSs] = PairwiseComp(Data, Factors[FInd], Paired[FInd], IN, PSs, psGB, psGBNames, pAdj, Describe=Describe)

                Bal = IsBalanced(Factors[FInd], psGB)

                if Paired[FInd] and Bal:
                    Corrs[PSs] = Correlation(
                            Data, Factors[FInd], Paired, IN, PSs,
                            psGB, psGBNames, pAdj, Describe=Describe
                        )
            else:
                SubCs[PSs] = Effect(Data, psWB, Id, psPaired, IN, PS, psGB, psGBNames, pAdj, Describe=Describe)

            if PSs in SubCs.keys():
                if type(SubCs[PSs]['Effect']) == dict:
                    if 'Effect' in SubCs[PSs]['Effect'].keys():
                        pssFacOrder = GetSigEff(SubCs[PSs]['Effect'])
                    else:
                        pssFacOrder = []
                else:
                    raise TypeError('This should be a dict. Check R output')
            else:
                SubCs[PSs] = {}
                pssFacOrder = []

            if not len(pssFacOrder):
                pssFacOrder = [
                    sorted(_)
                    for _ in tuple(combinations(PS, len(PS)-1))
                ]
            else:
                pssFacOrder = [sorted(pssFacOrder[0])] + [
                    sorted(_)
                    for p in pssFacOrder
                    for _ in tuple(combinations(p, len(p)-1))
                ]

            ToRun = [
                _
                for _ in ToRun+pssFacOrder
                if ':'.join(_) not in SubCs.keys()
                and len(_)
            ]

    if len(SubCs): Results['FXs'] = {**SubCs}
    if len(PWCs): Results['PWCs'] = {**PWCs}
    if len(Corrs): Results['Corrs'] = {**Corrs}

    print(f"[{ScriptName}.{FunctionName}] Done."); print()
    return(Results)


def AnOVa(Data, Factors, Id, Paired=[], Parametric='auto', FactorNames=[], GetAllPairwise=True, GetInvalidPWCs=True, pAdj='holm', Describe=True):
    FunctionName = inspect.stack()[0][3]
    print(f"[{ScriptName}.{FunctionName}] Deprecated.")
    print(f"[{ScriptName}.{FunctionName}] Run `Full(**Args)` instead.")



