
import numpy as np
from collections import OrderedDict
from PIL import ImageDraw, Image, ImageFont


def isScalarLike(expression):
	if hasattr(expression, "ndim"):
		if expression.ndim==0:
			return True
		return False
	if hasattr(expression, "__getitem__"):
		return False
	return True


def rgb2id(r,g,b):
	return r+g*256+b*65536


def colorlist(seed1=36, seed2=59):
	dct=OrderedDict()
	for n in range(216):
		c = (n+seed1)*seed2
		r = c%6
		g = (c//6)%6
		b = (c//36)%6
		if r==0 and g==0 and b==0:
			continue
		id = rgb2id(r*0x33, g*0x33, b*0x33)
		if id not in dct:
			dct[id]=True
	res = [(d,n) for n,d in enumerate(dct)]
	for n, d in enumerate(dct):
		if n==41:
			break
		res.append((d-0x1a,n+215))
	return res


def getFontSize():
	fon=ImageFont.load_default()
	sz=fon.getsize("ABCD")
	return sz


def drawTexts(im, Texts, lts):
	lblpi=Image.fromarray(im)
	lbldrw=ImageDraw.Draw(lblpi)
	for txt, (l,t) in zip(Texts, lts):
		lbldrw.text((l, t), txt, (0,0,0))
	return np.array(lblpi)


class ColorRegendItem:
	def __init__(self, color, ids):
		self.color_from_int=False
		if isScalarLike(color):
			self.color_from_int=True
			self.color=np.frombuffer(np.array(color,dtype=int).tobytes()[:3],dtype=np.uint8)
		else:
			self.color=np.array(color, dtype=np.uint8)
		if isinstance(ids, (tuple, list)):
			self.ids=np.array(ids, type(ids[0]))
		else:
			self.ids=ids
		
	def getTargetDim(self, targrtch=None):
		tids=self.id_pickup(targrtch)
		return len(tids)

	def color2idmap(self, im, res, targetch=None):
		mask=(im==self.color).prod(axis=-1).astype(bool)
		tids=self.id_pickup(targetch)
		res[mask]=tids

	def idmap2color(self, im, res, targetch=None):
		tids=self.id_pickup(targetch)
		if isScalarLike(tids) and im.ndim>2:
			im=im[...,0]
		mask=(im==tids)
		if not isScalarLike(tids):
			mask=mask.prod(axis=-1).astype(bool)
		res[mask]=self.color
	
	def id_pickup(self, targetch=None):
		if targetch is None:
			return self.ids
		if isScalarLike(targetch):
			return self.ids[targetch]
		res_ids=[]
		for d in targetch:
			if isScalarLike(d):
				res_ids.append(self.ids[d:d+1])
			else:
				if len(d)==1:
					res_ids.append(self.ids[d[0]:])
				else:
					res_ids.append(self.ids[d[0],d[1]])
		return np.concatenate(res_ids, axis=0)

	def idstr(self):
		if isScalarLike(self.ids):
			return str(self.ids)
		else:
			return str(tuple(self.ids))

	def __str__(self):
		return str(tuple(self.color))+": "+self.idstr()
	
	def __repr__(self):
		return str(self)
	
	def toDict(self, keys):
		if self.color_from_int:
			color=rgb2id(*self.color)
		else:
			color=self.color
		dct={}
		if isScalarLike(self.ids):
			lst=[color, self.ids]
		else:
			lst=[color, *self.ids]
		for k, v in zip(keys, lst):
			if k is not None:
				dct[k]=v
		return dct


class ColorRegend(list):
	def __init__(self, *color_ids):
		"""generates colorregend class.

		Args:
			(1) Nothing: Same as (2) with the default seed specified
			(2) size(int), seed1(int) , seed2(int): a sequential color legend seeded by the arguments
			(3) labels(array): parsed as [(color,ids),...]. ids can be specified with either "int" or "(int,int,...)".
			(4) colors(array), ids(array) 
		"""
		super().__init__()
		if len(color_ids)==0:
			itr=colorlist()[:16]
		elif isScalarLike(color_ids[0]):
			# a list of [int, int, ...]
			itr=colorlist(*color_ids[1:])[:color_ids[0]]
		elif len(color_ids)==1:
			# a list of [[color, ids]...]
			itr=color_ids[0]
		else:
			# a list of [color...],[ids...]
			itr=zip(*color_ids)
		for color, ids in itr:
			self.append(color, ids)

	def color2ids(self, im, res=None, targetch=None, default=-1):
		"""generate idsmap from colormap

		Args:
			im: input colormap
			res(array, optional): output target(inplace)
			targetch(int or array, optional): Channel(s) of ids you want to get
			default: default value of idsmap

		Returns:
			idsmap
		"""
		self.chk_len()
		if res is None:
			shp=list(im.shape[:2])
			tids=self[0].id_pickup(targetch)
			if not isScalarLike(tids):
				shp.append(len(tids))
				tp=type(tids[0])
			else:
				tp=type(tids)
			res=np.zeros(shp, dtype=tp)+default
		self.chk_matchdim(res, self[0].id_pickup(targetch))
		for item in self:
			item.color2idmap(im, res, targetch)
		return res

	def ids2color(self, im, res=None, targetch=None, default=0):
		"""generate color from idsmap

		Args:
			im: input idsmap
			res(array, optional): output target(inplace)
			targetch(int or array, optional): Channel(s) of ids you want to match
			default: default value of colormap

		Returns:
			colormap
		"""
		self.chk_len()
		self.chk_matchdim(im, self[0].id_pickup(targetch))
		if res is None:
			shp=list(im.shape[:2])+[3]
			if not isScalarLike(default):
				default=np.array(default, dtype=np.uint8)
			res=np.zeros(shp, dtype=np.uint8)+default
		for item in self:
			item.idmap2color(im, res, targetch)
		return res
	
	def makeColorTable(self, names=None):
		if names is None:
			names=[]
		txts=[]
		for nam in names:
			txts.append(nam)
		for n in range(len(txts), len(self)):
			txts.append("#"+self[n].idstr())
		
		# max is: 16 chars.
		ths=[12, 24, 48]
		cnt=len(txts)
		k=1
		for n, t in enumerate(ths):
			if t*k<cnt:
				k+=1
		sz=getFontSize()
		txtsz=[sz[0]*4, sz[1]]
		barw=(txtsz[0]//2)
		blanksz=[5, 5]
		
		rows=(cnt+k-1)//k
		
		CellSz=[txtsz[0]+blanksz[0]+barw, txtsz[1]+blanksz[1]]
		ImageSz=[blanksz[0]+CellSz[0]*k, blanksz[1]+CellSz[1]*rows]
		im=np.zeros([*ImageSz[::-1], 3], dtype=np.uint8)+255
		lts=[]
		for n in range(cnt):
			r=n%rows
			c=n//rows
			L=blanksz[0]+CellSz[0]*c
			T=blanksz[1]+CellSz[1]*r
			im[T:T+txtsz[1], L:L+barw]=self[n].color
			lts.append((L+barw+blanksz[0], T))
		im=drawTexts(im, txts, lts)
		return im

	def toAnnotation(self, keys):
		res=[]
		for item in self:
			res.append(item.toDict(keys))
		return res

	def append(self, *one_of_color_ids):
		if len(one_of_color_ids)==1:
			if isinstance(one_of_color_ids, ColorRegendItem):
				newitem=one_of_color_ids
			else:
				newitem=ColorRegendItem(*one_of_color_ids[0])
			super().append(newitem)
		else:
			# call itself at one argument.
			self.append(one_of_color_ids)

	def __add__(self, mustbesameclass):
		if not isinstance(mustbesameclass, ColorRegend):
			raise ValueError("__add__ can only take ColorRegend-class object as an argument.")
		return super().__add__(mustbesameclass)
	
	def __mul__(self, any):
		raise NotImplementedError("Calling __mul__ is not allowed.")

	def __repr__(self):
		return "ColorRegend: "+super().__repr__()
	
	def chk_len(self):
		if len(self) == 0:
			raise ValueError("please set ids at least one.")
	
	def chk_matchdim(self, tgim, tids):
		if tgim.ndim==2:
			if not isScalarLike(tids):
				raise ValueError("image.ndim==2,  which expects tids to be scalar.")
			return
		ch=tgim.shape[-1]
		if isScalarLike(tids):
			if ch!=1:
				raise ValueError("tids is scalar, but image channel is not one. ==", ch)
		elif ch != len(tids):
			raise ValueError("image.channels==", ch, " mismatched to tids==", tids)



def fromAnnotation(annot, keys=["id", "category_id","iscrowd","area", None]):
	anns=[]
	f = (lambda n,a,k: a[k] if k is not None else n)
	for n, a in enumerate(annot):
		ids = [f(n,a,k) for k in keys[1:]]
		anns.append((a[keys[0]], ids))
	cn = ColorRegend(anns)
	return cn


if __name__=="__main__":
	import matplotlib.pyplot as plt
	# test-pattern
	cckeys=["id", "category_id", "iscrowd", "area", None]
	test_ann=[{'id': 5931152, 'category_id': 23, 'iscrowd': 0, 'bbox': [1, 69, 585, 564], 'area': 275827}, {'id': 3834981, 'category_id': 193, 'iscrowd': 0, 'bbox': [0, 0, 586, 421], 'area': 88715}]
	# from dict
	cn=fromAnnotation(test_ann, cckeys)
	# to dict: expected not to be changed.
	print("RW-test: ", cn.toAnnotation(cckeys))
	# simple test case
	print("**********")
	ca=ColorRegend([[(87,76,65), (54,56)], [[65,54,43], (32,66)]])
	print("color-regend: ", ca)
	# making test colored map
	testmat=np.zeros([3,3,3], dtype=int)+ca[0].color[None,None,...]
	testmat[1,1]=ca[1].color
	print("testmat: ", testmat)
	# convert to id-map
	convmat=ca.color2ids(testmat)
	print("convmat: ", convmat)
	# reverse to color map.
	retmat=ca.ids2color(convmat, targetch=None)
	print("retmat", retmat)
	# id-pattern change
	cb=ColorRegend([[ca[0].color, 0],[ca[1].color, 1]])
	convmat=cb.color2ids(testmat)
	print("convmat-2: ", convmat)
	retmat=cb.ids2color(convmat)
	print("retmat-2: ", retmat)
	#
	# cm=ColorRegend()
	# colormap from randomseed.
	cm=ColorRegend(52, 36, 59)
	# a simple idmap.
	mp=np.arange(48)[None,...].repeat(32,axis=0)
	# idmap to colormap
	q=cm.ids2color(mp)
	# colormap to idmap
	inv=cm.color2ids(q)
	# show 3 maps.
	plt.subplot(411).imshow(mp)
	plt.subplot(412).imshow(q)
	plt.subplot(413).imshow(inv)
	# show color-table
	g=cm.makeColorTable(["TestLabel", "Foo"])
	plt.subplot(414).imshow(g)
	plt.show()
