"""Compatibility layer

I'm aiming to support Python 3 as well as 2.6+, let's see how this works out!
"""
import warnings


try:
	from enum import Enum
except ImportError:
	Enum = object

try:
	xrange = xrange
except NameError:
	xrange = range

def range(*args, **kwargs):
	warnings.warn('Most interesting! The code is using range(...)',
		DeprecationWarning, stacklevel=2)
	return xrange(*args, **kwargs)
	
