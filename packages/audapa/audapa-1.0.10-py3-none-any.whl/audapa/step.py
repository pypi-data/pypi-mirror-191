
from . import point
from . import points
from . import draw
from . import drawscroll
from . import snap

#tests: 1 right circle,2 right inter,3 right margin
#       4 left free/inter/margin
#       5 landscape circle (inter easiest)

def pos_type(ix):
	return points.points[ix]._offset_-draw.offset-point.const
def left_type():
	p=point.lastselect
	ix=points.points.index(p)
	if ix==0 or points.points[ix-1]._offset_<draw.offset:
		return -point.const
	return pos_type(ix-1)
def right_type():
	p=point.lastselect
	ix=points.points.index(p)
	if ix+1==len(points.points) or points.points[ix+1]._offset_>(draw.offset+draw.size):
		return draw.size-point.const
	return pos_type(ix+1)

def autodrag(p,x,y):
	snap.autodrag(p,x+point.const,y+point.const)

def left(b,d):
	leftk()
def leftk():
	if drawscroll.landscape:
		limit=left_type()
	else:
		limit=-point.const
	p=point.lastselect
	x,y=draw.cont.get_child_position(p)
	x-=1 #on height is double
	if x>limit:
		autodrag(p,x,y)

def right(b,d):
	rightk()
def rightk():
	if drawscroll.landscape:
		limit=right_type()
	else:
		limit=draw.area.get_width()-point.const
	p=point.lastselect
	x,y=draw.cont.get_child_position(p)
	x+=1
	if x<limit:
		autodrag(p,x,y)

def up(b,d):
	upk()
def upk():
	if drawscroll.landscape:
		limit=-point.const
	else:
		limit=left_type()
	p=point.lastselect
	x,y=draw.cont.get_child_position(p)
	y-=1
	if y>limit:
		autodrag(p,x,y)

def down(b,d):
	downk()
def downk():
	if drawscroll.landscape:
		limit=draw.area.get_height()-point.const
	else:
		limit=right_type()
	p=point.lastselect
	x,y=draw.cont.get_child_position(p)
	y+=1
	if y<limit:
		autodrag(p,x,y)
