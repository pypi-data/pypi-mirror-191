
import os

from . import play
from . import points

def file():
	temp=loc()
	play.save_opened(temp)
	play.wavefile.close()
	play.wave_open(temp)

def loc():
	return points.fpath(play.entry.get_text(),"temp")

def close():
	temp=loc()
	if os.path.exists(temp):
		os.remove(temp)
