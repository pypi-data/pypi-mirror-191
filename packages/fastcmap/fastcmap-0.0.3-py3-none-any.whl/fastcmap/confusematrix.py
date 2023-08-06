import numpy as np
from PIL import ImageDraw, Image, ImageFont

def _makeMatrixField(map, cmap, cellsize, percent=True):
	fpi=Image.fromarray(cmap)
	fpi=fpi.resize((cmap.shape[1]*cellsize, cmap.shape[0]*cellsize), Image.NEAREST)
	fdrw=ImageDraw.Draw(fpi)
	fon=fdrw.getfont()
	ymat=np.array([0.299,0.587,0.114])
	for iy in range(map.shape[0]):
		for ix in range(map.shape[1]):
			cx=cellsize*(2*ix+1)//2
			cy=cellsize*(2*iy+1)//2
			if percent:
				s="%2.0f%%" % (map[iy,ix]*100,)
			else:
				s=str(map[iy,ix])
			y=ymat@cmap[iy,ix]
			fclr=255 if y<90 else 0
			sz=fon.getsize(s)
			fdrw.text((cx-sz[0]//2,cy-sz[1]//2), s,(fclr,fclr,fclr))
	return np.array(fpi)

def _makeLabelField(classes, cellsize):
	lc=len(classes)
	maxsz=0
	fon=ImageFont.load_default()
	for i in range(lc):
		sz=fon.getsize(classes[i])
		if maxsz<sz[0]:
			maxsz=sz[0]
	lblmap=np.zeros((cellsize*lc, maxsz+6, 3),dtype=np.uint8)+255
	lblpi=Image.fromarray(lblmap)
	lbldrw=ImageDraw.Draw(lblpi)
	for i in range(lc):
		sz=fon.getsize(classes[i])
		cx=maxsz+3-sz[0]
		cy=cellsize*(2*i+1)//2-sz[1]//2
		lbldrw.text((cx,cy), classes[i], (0,0,0))
	return np.array(lblpi)


def _drawRectOutside(map, bdr, ltrb):
	l,t,r,b=ltrb
	map[t-bdr:t,l-bdr:r+bdr]=0
	map[b:b+bdr, l-bdr:r+bdr]=0
	map[t-bdr:b+bdr, l-bdr:l]=0
	map[t-bdr:b+bdr, r:r+bdr]=0

def _buildConfuseMap(matrixcontent, lblmap, ltrb=(0.005, 0.01, 0.01, 0.005), bdr=2):
	mh,mw=matrixcontent.shape[:2]
	lh,lw=lblmap.shape[:2]
	sl,st,sr,sb=(0.5+np.array(mh*4)*ltrb).astype(int)
	bim=np.zeros((st+sb+mh+lw+bdr*2, sl+sr+mw+lw+bdr*2,3),dtype=np.uint8)+255
	ml, mt=sl+lw+bdr, st+bdr
	mr, mb=ml+mw, mt+mh
	# draw border.
	_drawRectOutside(bim, bdr, (ml, mt, mr, mb))
	# draw contents.	
	bim[mt:mt+lh,sl:sl+lw]=lblmap
	bim[mt:mb, ml:mr]=matrixcontent
	bim[mb+bdr:mb+bdr+lw,ml:ml+lh]=lblmap.transpose(1,0,2)[::-1]
	return bim

def makeConfuseMatrix(map, cmap, classes, cellsize=32, border=2):
	mtx=_makeMatrixField(map, cmap, cellsize)
	lfld=_makeLabelField(classes, cellsize)
	return _buildConfuseMap(mtx, lfld, bdr=border)

if __name__=="__main__":
	# confusematrix test sample.
	from base import ColorMap
	import matplotlib.pyplot as plt
	classes=["apple","banana","carrot","donut","egg","fish","grape","hotdog","icecream","jelly","kiwi","lemon","melon","noodle"]
	cmp=ColorMap()
	cmp.registerCustomCmap_fromLineProp("gray", [[[0,0,1,0,255]]]*3)
	tgc=classes[:8]
	lc=len(tgc)
	map=np.random.uniform(size=(lc,lc))
	cmap=cmp.getColormap(map, "gray",0,1)
	im=makeConfuseMatrix(map, cmap, tgc)
	plt.imshow(im)
	plt.show()

