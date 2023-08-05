from xyz.xyz import p,mfp,Fid

def px(String: str, C = 8388608):
    """
    It is first solve machine.
    """
    return p.px(String, C)

def pxy(String: str, C = 1000):
    """
    It is second solve machine.
    """
    return p.pxy(String, C)

def pxyz(String: str, C = 100):
    """
    It is third solve machine.
    """
    return p.pxyz(String, C)

def mfpx(String: str, C = 10000):
    """
    It is fourth solve machine.
    """
    return mfp.mfpx(String, C)

def mfpxy(String: str, C = 500):
    """
    It is fifth solve machine.
    """
    return mfp.mfpx(String, C)

def mfpxyz(String: str, C = 100):
    """
    It is sixth solve machine.
    """
    return mfp.mfpx(String, C)

def findx(String: str, Bools: bool = False):
    """
    It is first find machine
    """
    return Fid.Findx(String, Bools)

def findxy(String: str, Bools: bool = False):
    """
    It is second find machine
    """
    return Fid.Findxy(String, Bools)

def findxyz(String: str, Bools: bool = False):
    """
    It is third find machine
    """
    return Fid.Findxyz(String, Bools)