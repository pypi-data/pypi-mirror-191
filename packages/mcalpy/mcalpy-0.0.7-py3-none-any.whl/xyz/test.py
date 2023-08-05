from xyz.xyz import p

if __name__ == '__main__':
    print(p.px("x + x = x"))                             #x: 0
    print(p.pxy("x + y = x + y, x * y = x * y"))         #x: 0, y: 0
    print(p.pxyz("x + 2 = 6, y + 1 = 4, z = x + y + x")) #x: 4, y: 3, z: 11