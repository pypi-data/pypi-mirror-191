import numpy as np
import json


def _Approx2(y, st,ed,lm=1e-3):
	x=np.linspace(0,1,ed-st)
	cx=y[st]*(1-x)+y[ed-1]*x
	c=y[st:ed]-cx
	s=c*x*(x-1)
	t=(x*(x-1))**2
	A=s.sum()/(t+lm).sum()
	ys=A*x*(x-1)+cx
	if np.abs(A)<1e-6:
		A=0
	return ys,A


def _cfunc(A,st,ed,yst,yed,Xrng=None):
	if Xrng is None:
		x=np.linspace(0,1,ed-st)
	else:
		xst=(Xrng[0]-st)/(ed-st-1)
		xed=(Xrng[1]-st-1)/(ed-st-1)
		x=np.linspace(xst,xed,Xrng[1]-Xrng[0])
	cx=(yed-yst)*x+yst
	return A*x*(x-1)+cx


def _cdfunc(A,st,ed,yst,yed):
	x=np.linspace(0,1,ed-st)
	return (A*(2*x-1)+(yed-yst))/(ed-st)


def _JudgeEmx(y,st,ed,kxrate):
	if ed<=st:
		return 0,0
	ys,A=_Approx2(y,st,ed)
	slp=_cdfunc(A,st,ed,y[st],y[ed-1])*kxrate
	dy=np.abs(ys-y[st:ed])/np.sqrt(1+slp**2)
	return np.max(dy),A


def _Approxlines(y,th=1.5,xrate=0.6):
	yst=0
	yed=yst+1
	lines=[]
	kxrate=xrate*200/len(y)
	for i in range(len(y)):
		emx,A=_JudgeEmx(y,yst,i,kxrate)
		if emx>=th:
			lines.append((A,yst,i,y[yst],y[i-1]))
			yst=i
	i=len(y)
	if i>yst:
		i=len(y)
		lines.append((A,yst,i,y[yst],y[i-1]))
	else:
		pass
	return lines,xrate


def _AdjBorder(y,lines, xrate):
	vlines=lines[::-1]
	reslines=[]
	kxrate=xrate*200/len(y)
	red=vlines[0][2]-1
	for Lln,Rln in zip(vlines[1:],vlines[:-1]):
		A,st,ed,_,_=Lln
		lemx_bak=None
		remx_bak=None
		_,Ar=_JudgeEmx(y,ed,red+1,kxrate)
		prm_bak=(Ar,ed,red,y[ed],y[red])
		for n in range(ed-st-1):
			bdr=Lln[2]-n
			lemx,_=_JudgeEmx(y,st,bdr+1,kxrate)
			remx,Ar=_JudgeEmx(y,bdr,red+1,kxrate)
			if n>0:
				grad=lemx-lemx_bak+remx-remx_bak
				if grad>=0:
					break
			lemx_bak,remx_bak=lemx,remx
			prm_bak=(Ar,bdr,red+1,y[bdr],y[red])
		reslines.append(prm_bak)
		red=prm_bak[1]
	st=vlines[-1][1]
	_,Ar=_JudgeEmx(y,st,red+1,kxrate)
	reslines.append((Ar,st,red,y[st],y[red]))
	return reslines[::-1]


def _makecurve(lines):
	ys=np.zeros((lines[-1][2],))
	for a,st,ed,yst,yed in lines:
		ys[st:ed]=_cfunc(a,st,ed,yst,yed)
	return ys


def _makexycurves(x,lines):
	res=[]
	for a,st,ed,yst,yed in lines:
		xs=x[st:ed]
		ys=_cfunc(a,st,ed,yst,yed)
		res.append((xs,ys))
	return res


def _makemap_(map, vmin,vmax,lines):
	gst,ged=lines[0][1], lines[-1][2]
	# normalize map
	map=(map-vmin).astype(float)/(vmax-vmin)
	# clip and convert range to [gst,ged]
	map=np.clip(map,0,1)*(ged-gst)+gst
	resmap=np.zeros(map.shape)
	for A,st,ed,yst,yed in lines:
		whr=((map>=st) & (map<=ed))
		x=map[whr]
		x=(x-st)/(ed-st)
		resmap[whr]=A*(x-1)*x+(yed-yst)*x+yst
	return resmap


def _makemap(map, vmin,vmax,lines):
	gst,ged=lines[0][1], lines[-1][2]
	vinv=(ged-gst)/(vmax-vmin)
	st0=gst/vinv
	map=(map.astype(float)-(vmin+st0))*vinv
	map=np.clip(map,gst,ged)
	resmap=np.zeros(map.shape)
	for A,st,ed,yst,yed in lines:
		whr=((map>=st) & (map<=ed))
		sinv=1/(ed-st)
		x=map[whr]
		# about 6% shorter than.
		# x=(x-st)*sinv
		# resmap[whr]=(A*x+(yed-yst-A))*x+yst
		C=(yed-yst-A*(st*sinv+1))*sinv
		D=(A*sinv*sinv)
		resmap[whr]=(D*x+(C-D*st))*x+(yst-st*C)
	return resmap


def _getrgblines(rgbbar):
	res=[]
	for cbar in rgbbar:
		fbar=cbar.astype(float)
		tmplines,xrate=_Approxlines(fbar, 3.5)
		tmplines=_AdjBorder(fbar, tmplines,0)
		res.append(tmplines)
	return res


def _createGradMap(size=(256,256), t=1):
	xmap=np.linspace(0, 1, size[0])[None, ...].repeat(size[1],axis=0)
	ymap=np.linspace(0, 1, size[1])[...,None].repeat(size[0],axis=1)
	return xmap*t+ymap*(1-t)

def createGradMap(size=(256,256), t=1):
	ts=None
	b=False
	if hasattr(t, "shape"):
		if t.ndim==0:
			b=True
	elif not hasattr(t, "__getitem__"):
		b=True
	if b:
		return _createGradMap(size,t)
	ress=[]
	for tu in t:
		ress.append(_createGradMap(size,tu))
	return np.stack(ress).transpose(1,2,0)

class ColorMap:
	def __init__(self):
		self.dict={}

	def getColormap(self, map1d2d, cmap, vmin=None, vmax=None):
		assert(cmap in self.dict)
		if vmin is None:
			vmin=0 if map1d2d.dtype==np.uint8 else np.min(map1d2d)
		if vmax is None:
			vmax=255 if map1d2d.dtype==np.uint8 else np.max(map1d2d)
		rgblines=self.dict[cmap]
		rgbmap=np.zeros((*map1d2d.shape,3),dtype=np.uint8)
		for n, lines in enumerate(rgblines):
			rgbmap[...,n]=np.clip(_makemap(map1d2d, vmin, vmax, lines),0,255).astype(np.uint8)
		return rgbmap

	def createColormap(self, cmap, size=(256,256), t=1):
		map=createGradMap(size, t)
		return self.getColormap(map, cmap)

	def registerCustomCmap_fromLineProp(self, cmap, rgbline):
		assert(len(rgbline)==3)
		for lns in rgbline:
			edbak=None
			for ln in lns:
				assert(len(ln)==5)
				st,ed=ln[1:3]
				if edbak is not None:
					assert(st==edbak)
				assert(st<ed)
				edbak=ed
		self.dict[cmap]=rgbline
		return True

	def registerCustomCmap_fromPlot(self, cmap, rgbline):
		assert(len(rgbline)==3)
		for ln in rgbline:
			if not hasattr(ln, "shape"):
				return False
		self.dict[cmap]=_getrgblines(rgbline)
		return True

	def saveAs(self, path):
		fp=open(path, "w")
		json.dump(self.dict, fp)
		fp.close()

	def load(self, path, append=True):
		fp=open(path, "r")
		tgdict=json.load(fp)
		fp.close()
		if append:
			self.dict.update(tgdict)
		else:
			self.dict=tgdict

