import re
import sys
from xyz.xyz.Fid import *

def px(String: str, C = 8388608) -> str:
    """
    It is String Plus function.
    """
    p2 = re.compile(r'sqrt(?P<sqrts>[(].+[)])')
    p2.sub(r'\g<sqrts>**(1/2)',String)
    p = re.compile(r'([x])')
    c = 0
    if Findx(String) == None:
        return None
    fst = String.split('=')[0]
    scd = String.split('=')[1]
    if Findx(fst, True) == None:
        fst = eval(fst)
    if Findx(scd, True) == None:
        scd = eval(scd)
    while c < int(C):
        stf = String.split('=')[0]
        sts = String.split('=')[1]
        try:
            stf = p.sub(str(c), stf)
        except:
            stf = String.split('=')[0]
        try:
            sts = p.sub(str(c), sts)
        except:
            sts = String.split('=')[1]
        if eval(stf) == eval(sts):
            return c
        else:
            c += 1
            try:
                if sys.argv[1] == "-debug":
                    print(str(c))
            except:
                pass
            continue
    return 'Can\'t calculate!'


def pxy(String: str, C = 1000) -> str:
    """
    It is String Plus function.
    """
    p2 = re.compile(r'sqrt(?P<sqrts>[(].+[)])')
    p2.sub(r'\g<sqrts>**(1/2)',String)
    p = re.compile(r'([x])')
    py = re.compile(r'([y])')
    c = 0
    d = 0
    if Findxy(String) == None:
        return None
    F = String.split(',')[0]
    fst = F.split('=')[0]
    scd = F.split('=')[1]
    S = String.split(',')[1]
    sfst = S.split('=')[0]
    sscd = S.split('=')[1]
    if Findxy(fst, True) == None:
        fst = eval(fst)
    if Findxy(scd, True) == None:
        scd = eval(scd)
    if Findxy(sfst, True) == None:
        sfst = eval(sfst)
    if Findxy(sscd, True) == None:
        sscd = eval(sscd)
    while c < int(C):
        while d < int(C):
            F = String.split(',')[0]
            stf = F.split('=')[0]
            sts = F.split('=')[1]
            S = String.split(',')[1]
            sstf = S.split('=')[0]
            ssts = S.split('=')[1]
            try:
                stf = p.sub(str(c), stf)
                stf = py.sub(str(d), stf)
                sstf = p.sub(str(c), sstf)
                sstf = py.sub(str(d), sstf)
            except Exception as e:
                print(e)
                stf = String.split('=')[0]
            try:
                sts = p.sub(str(c), sts)
                sts = py.sub(str(d), sts)
                ssts = p.sub(str(c), ssts)
                ssts = py.sub(str(d), ssts)
            except:
                sts = String.split('=')[1]
            if eval(stf) == eval(sts) and eval(sstf) == eval(ssts):
                return 'x: %s, y: %s'%(c, d)
            else:
                d += 1
                try:
                    if sys.argv[1] == "-debug":
                        print(str(c), str(d))
                except:
                    pass
                continue
        c += 1; d=0
    return 'Can\'t calculate!'

def pxyz(String: str, C = 100) -> str:
    """
    It is String Plus function.
    """
    p2 = re.compile(r'sqrt(?P<sqrts>[(].+[)])')
    p2.sub(r'\g<sqrts>**(1/2)',String)
    p = re.compile(r'([x])')
    py = re.compile(r'([y])')
    pz = re.compile(r'([z])')
    c = 0
    d = 0
    e = 0
    if Findxyz(String) == None:
        return None
    F = String.split(',')[0]
    fst = F.split('=')[0]
    scd = F.split('=')[1]
    S = String.split(',')[1]
    sfst = S.split('=')[0]
    sscd = S.split('=')[1]
    T = String.split(',')[2]
    tfst = T.split('=')[0]
    tscd = T.split('=')[1]
    if Findxyz(fst, True) == None:
        fst = eval(fst)
    if Findxyz(scd, True) == None:
        scd = eval(scd)
    if Findxyz(sfst, True) == None:
        sfst = eval(sfst)
    if Findxyz(sscd, True) == None:
        sscd = eval(sscd)
    if Findxyz(tfst, True) == None:
        tfst = eval(tfst)
    if Findxyz(tscd, True) == None:
        tscd = eval(tscd)
    while c < int(C):
        d = e = 0
        while d < int(C):
            e = 0
            while e < int (C):
                F = String.split(',')[0]
                stf = F.split('=')[0]
                sts = F.split('=')[1]
                S = String.split(',')[1]
                sstf = S.split('=')[0]
                ssts = S.split('=')[1]
                T = String.split(',')[2]
                tstf = T.split('=')[0]
                tsts = T.split('=')[1]
                try:
                    stf = p.sub(str(c), stf)
                    stf = py.sub(str(d), stf)
                    stf = pz.sub(str(e), stf)
                    sstf = p.sub(str(c), sstf)
                    sstf = py.sub(str(d), sstf)
                    sstf = pz.sub(str(e), sstf)
                    tstf = p.sub(str(c), tstf)
                    tstf = py.sub(str(d), tstf)
                    tstf = pz.sub(str(e), tstf)
                except Exception as e:
                    print(e)
                    stf = String.split('=')[0]
                try:
                    sts = p.sub(str(c), sts)
                    sts = py.sub(str(d), sts)
                    sts = pz.sub(str(e), sts)
                    ssts = p.sub(str(c), ssts)
                    ssts = py.sub(str(d), ssts)
                    ssts = pz.sub(str(e), ssts)
                    tsts = p.sub(str(c), tsts)
                    tsts = py.sub(str(d), tsts)
                    tsts = pz.sub(str(e), tsts)
                except:
                    sts = String.split('=')[1]
                if eval(stf) == eval(sts) and eval(sstf) == eval(ssts) and eval(tstf) == eval(tsts):
                    return 'x: %s, y: %s, z: %s'%(c, d, e)
                else:
                    e += 1
                    try:
                        if sys.argv[1] == "-debug":
                            print(str(c), str(d), str(e))
                    except:
                        pass
                    continue
            d += 1; e = 0
        c += 1; d = 0; e = 0
    return 'Can\'t calculate!'