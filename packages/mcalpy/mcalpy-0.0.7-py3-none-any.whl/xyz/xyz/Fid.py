def Findx(String, b = False) -> int:
    """
    It is find x.
    If String has x return True.
    Unless String x return None 
    """
    st = str(String)
    if b == False:
        if st.split('=')[1].count("x") == 0 and st.split('=')[0].count("x") == 0:
            return None
    elif b == True:
        if st.count("x") == 0:
            return None
    return True

def Findxyz(String, b = False) -> int:
    """
    It is find x and y, z.
    If String has x and y, z return True.
    Unless String x and y, z return None 
    """
    st = str(String)
    if b == False:
        if (st.split('=')[1].count("x") == 0 and st.split('=')[0].count("x") == 0) or (st.split('=')[1].count("y") == 0 and st.split('=')[0].count("y") == 0)\
            or (st.split('=')[1].count("z") == 0 and st.split('=')[0].count("z") == 0) or (st.count(",") != 2):
            return None
    elif b == True:
        if (st.count("x") == 0) and (st.count("y") == 0) and (st.count("z") == 0):
            return None
    return True

def Findxy(String, b = False) -> int:
    """
    It is find x and y.
    If String has x and y return True.
    Unless String x and y return None 
    """
    st = str(String)
    if b == False:
        if (st.split('=')[1].count("x") == 0 and st.split('=')[0].count("x") == 0) or (st.split('=')[1].count("y") == 0 and st.split('=')[0].count("y") == 0) or (st.count(",") != 1):
            return None
    elif b == True:
        if (st.count("x") == 0) and (st.count("y") == 0):
            return None
    return True
