from matplotlib import pyplot as plt

from xyz.meq import x

def geq(*Eq):
    """Before you use this function, write it "from xyz import meq" or "import numpy as np;x = np.array(range(-10,11))".
    useage:
        geq(x + 3)
    geq(x + 3) is 'y = x + 3'
"""
    global x
    Eq = list(Eq)
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.grid(color="gray",alpha=.5,linestyle="--")
    for i in range(len(Eq)):
        plt.plot(x,Eq[i])
    plt.show()