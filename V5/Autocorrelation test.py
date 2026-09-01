
goodlist = [0.30,0.35,0.28,0.40,0.25,0.38]


def autocorrelation():
    global goodlist
    autocorrelationy = []
    kx = []
    totalsum: int = 0
    for x in goodlist:
        totalsum+=x
    mean = totalsum/(len(goodlist))
    difflist = []
    for x in range(0, len(goodlist)):
        difflist.append(goodlist[x]-mean)
        
    bottom = sum(d**2 for d in difflist)
            
    for k in range(1, 4):
        kx.append(k)
        top = 0
        for index in range(0, len(goodlist)-k):
            top += (difflist[index])*(difflist[index+k])
            
        autocorrelationy.append(top/bottom)


    print(autocorrelationy)
    print(kx)


autocorrelation()
