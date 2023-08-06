if __name__=="__main__":
    from map_linedata import data as _default_data
    from base import createGradMap, ColorMap as BaseColorMap
    from confusematrix import makeConfuseMatrix as _makeConfuseMatrix
    from segmentation import ColorRegend, fromAnnotation
else:
    from .map_linedata import data as _default_data
    from .base import createGradMap, ColorMap as BaseColorMap
    from .confusematrix import makeConfuseMatrix as _makeConfuseMatrix
    from .segmentation import ColorRegend, fromAnnotation


__version__ = "0.0.3"


class ColorMap(BaseColorMap):
    def __init__(self):
        self.load_default()

    def load_default(self):
        self.dict = _default_data.copy()
    
    def makeConfuseMatrix(self, map, cmap="gray", classes=None):
        if classes is None:
            classes = [""]*map.shape[0]
        im = self.getColormap(map, cmap)
        return _makeConfuseMatrix(map, im, classes)


if __name__=="__main__":
    import numpy as np
    cmp=ColorMap()
    cmp.dict={}
    lns=[[(0,0,1,0,255),(0,1,2,255,22)]]*3
    cmp.registerCustomCmap_fromLineProp("uuu", lns)
    cmp.saveAs("ttt.ttt")
    cmp.load_default()
    print([k for k in cmp.dict])
    print("*******")
    cmp.load("ttt.ttt")
    ccc=cmp.createColormap("jet")//2+cmp.createColormap("viridis")//2
    cmp.registerCustomCmap_fromPlot("utt", ccc[0,:].transpose(1,0))
    map=np.random.uniform(size=(6,6))
    classes=["2","3","d","f","a","g"]
    im=cmp.makeConfuseMatrix(map, classes=classes)
    print([k for k in cmp.dict])
    import matplotlib.pyplot as plt
    #plt.imshow(cmp.createColormap("utt"))
    plt.subplot(211).imshow(im)
    # test maps.
    u=ColorRegend()
    iim=createGradMap()*20
    q=u.ids2color(iim.astype(int))
    plt.subplot(212).imshow(q)
    plt.show()
