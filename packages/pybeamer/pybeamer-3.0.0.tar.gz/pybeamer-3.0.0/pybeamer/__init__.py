

__all__ = ['retrieve_kw', 'checkForUnusedVars', 'ensureExtension', 'checkExtension', 
           'Holder', 'traverse', 'LimitedTypeList',  'NotAllowedType']

import numpy as np
import re
import colorlog
import traceback
import logging

_lMethodSearch=re.compile("_LimitedTypeList__(\S+)")


#
# Set logger
#
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter())
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
logger.addHandler(handler)


def retrieve_kw( kw, key, default = None ):
  if not key in kw or kw[key] is None:
    kw[key] = default
  return kw.pop(key)


def checkForUnusedVars(d, fcn = None):
  """
    Checks if dict @d has unused properties and print them as warnings
  """
  for key in d.keys():
    if d[key] is None: continue
    msg = 'Obtained not needed parameter: %s' % key
    if fcn:
      fcn(msg)
    else:
      print('WARNING:%s' % msg)

def ensureExtension( filename, extension ):
    return (filename + '.' + extension) if not filename.endswith(extension) else filename


def checkExtension( filename, extension ):
  extensions = extension.split('|')
  for ext in extensions:
    if filename.endswith(ext):
      return True
  return False



class Holder( object ):
  """
  A simple object holder
  """
  def __init__(self, obj = None, replaceable = True):
    self._obj = obj
    self._replaceable = replaceable
  def __call__(self):
    return self._obj
  def isValid(self):
    return self._obj not in (None, NotSet)
  def set(self, value):
    if self._replaceable or not self.isValid():
      self._obj = value
    else:
      raise RuntimeError("Cannot replace held object.")


def traverse(o, tree_types=(list, tuple),
    max_depth_dist=0, max_depth=np.iinfo(np.uint64).max, 
    level=0, parent_idx=0, parent=None,
    simple_ret=False, length_ret=False):
  """
  Loop over each holden element. 
  Can also be used to change the holden values, e.g.:
  a = [[[1,2,3],[2,3],[3,4,5,6]],[[[4,7],[]],[6]],7]
  for obj, idx, parent in traverse(a): parent[idx] = 3
  [[[3, 3, 3], [3, 3], [3, 3, 3, 3]], [[[3, 3], []], [3]], 3]
  Examples printing using max_depth_dist:
  In [0]: for obj in traverse(a,(list, tuple),0,simple_ret=False): print obj
  (1, 0, [1, 2, 3], 0, 3)
  (2, 1, [1, 2, 3], 0, 3)
  (3, 2, [1, 2, 3], 0, 3)
  (2, 0, [2, 3], 0, 3)
  (3, 1, [2, 3], 0, 3)
  (3, 0, [3, 4, 5, 6], 0, 3)
  (4, 1, [3, 4, 5, 6], 0, 3)
  (5, 2, [3, 4, 5, 6], 0, 3)
  (6, 3, [3, 4, 5, 6], 0, 3)
  (4, 0, [4, 7], 0, 4)
  (7, 1, [4, 7], 0, 4)
  (6, 0, [6], 0, 3)
  (7, 2, [[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 0, 1) 
  In [1]: for obj in traverse(a,(list, tuple),1): print obj
  ([1, 2, 3], 0, [[1, 2, 3], [2, 3], [3, 4, 5, 6]], 1, 3)
  ([2, 3], 0, [[1, 2, 3], [2, 3], [3, 4, 5, 6]], 1, 3)
  ([3, 4, 5, 6], 0, [[1, 2, 3], [2, 3], [3, 4, 5, 6]], 1, 3)
  ([4, 7], 0, [[4, 7], []], 1, 4)
  ([6], 0, [[[4, 7], []], [6]], 1, 3)
  ([[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 2, None, 1, 1)
  In [2]: for obj in traverse(a,(list, tuple),2,simple_ret=False): print obj
  ([[1, 2, 3], [2, 3], [3, 4, 5, 6]], 0, [[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 2, 2)
  ([[4, 7], []], 0, [[[4, 7], []], [6]], 2, 3)
  ([[[4, 7], []], [6]], 1, [[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 2, 2)
  In [3]: for obj in traverse(a,(list, tuple),3): print obj
  ([[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 0, None, 3, 1)
  In [4]: for obj in traverse(a,(list, tuple),4): print obj
  ([[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 1, None, 4, 1)
  In [5]: for obj in traverse(a,(list, tuple),5): print obj
  <NO OUTPUT>
  """
  if isinstance(o, tree_types):
    level += 1
    # FIXME Still need to test max_depth
    if level > max_depth:
      if simple_ret:
        yield o
      elif length_ret:
        yield level
      else:
        yield o, parent_idx, parent, 0, level
      return
    skipped = False
    isDict = isinstance(o, dict)
    if isDict:
      loopingObj = o.iteritems()
    else:
      loopingObj = enumerate(o)
    for idx, value in loopingObj:
      try:
        for subvalue, subidx, subparent, subdepth_dist, sublevel in traverse(value 
                                                                            , tree_types     = tree_types
                                                                            , max_depth_dist = max_depth_dist
                                                                            , max_depth      = max_depth
                                                                            , level          = level
                                                                            , parent_idx     = idx
                                                                            , parent         = o ):
          if subdepth_dist == max_depth_dist:
            if skipped:
              subdepth_dist += 1
              break
            else:
              if simple_ret:
                yield subvalue
              elif length_ret:
                yield sublevel
              else:
                yield subvalue, subidx, subparent, subdepth_dist, sublevel 
          else:
            subdepth_dist += 1
            break
        else: 
          continue
      except SetDepth as e:
        if simple_ret:
          yield o
        elif length_ret:
          yield level
        else:
          yield o, parent_idx, parent, e.depth, level
        break
      if subdepth_dist == max_depth_dist:
        if skipped:
          subdepth_dist += 1
          break
        else:
          if simple_ret:
            yield o
          elif length_ret:
            yield level
          else:
            yield o, parent_idx, parent, subdepth_dist, level
          break
      else:
        if level > (max_depth_dist - subdepth_dist):
          raise SetDepth(subdepth_dist+1)
  else:
    if simple_ret:
      yield o
    elif length_ret:
      yield level
    else:
      yield o, parent_idx, parent, 0, level






class LimitedTypeList (type):
  """
    LimitedTypeList metaclass create lists which only accept declared types.

    One LimitedTypeList class must specify _acceptedTypes property as a tuple,
    which will be the only types accepted by the list.

    In case a class inherits from another classes that declare _acceptedTypes 
    and it does not declare this class attribute, then the first base class
    _acceptedTypes will be used.

    If none of the inherited classes define the __init__ method, the list 
    init method will be used. In case you have a inherited class with __init__
    method (case where the base class has __metaclass__ set to LimitedTypeList)
    and want to enforce that this class will use their own __init__ method, then
    set _useLimitedTypeList__init__ to True. If you do so, then the __init__ you declare
    will be overridden by the LimitedTypeList.
  """

  # TODO Add boolean to flag if the class can hold itself

  def __new__(cls, name, bases, dct):
    if not any( [ issubclass(base, list) for base in bases ] ):
      bases = (list,) + bases 
    import inspect
    import sys
    hasBaseInit = any([hasattr(base,'__init__') for base in bases if base.__name__ not in 
                                                                    ("list", "object", "Logger", "LoggerStreamable",)])
    for localFcnName, fcn in inspect.getmembers( sys.modules[__name__], inspect.isfunction):
      m = _lMethodSearch.match(localFcnName)
      if m:
        fcnName = m.group(1)
        if not fcnName in dct:
          if hasBaseInit and fcnName == '__init__' and not dct.get('_useLimitedTypeList__init__', False):
            continue
          dct[fcnName] = fcn
    return type.__new__(cls, name, bases, dct)

  def __init__(cls, name, bases, dct):
    ## Take care to _acceptedTypes be in the right specification
    if not '_acceptedTypes' in dct:
      for base in bases:
        if hasattr(base, '_acceptedTypes'):
          acceptedTypes = base._acceptedTypes
          break
      dct['_acceptedTypes'] = acceptedTypes
    else:
      acceptedTypes = dct['_acceptedTypes']
    if not type(acceptedTypes) is tuple:
      raise ValueError("_acceptedTypes must be declared as a tuple.")
    if not acceptedTypes:
      raise ValueError("_acceptedTypes cannot be empty.")
    return type.__init__(cls, name, bases, dct)

  def __call__(cls, *args, **kw):
    return type.__call__(cls, *args, **kw)


def _LimitedTypeList__setitem(self, k, var):
  """
    Default override setitem
  """
  # This is default overload for list setitem, checking if item is accepted
  if not isinstance(var, self._acceptedTypes):
    raise NotAllowedType(self, var, self._acceptedTypes)
  list.setitem(self, k, var)

def _LimitedTypeList__append(self, var):
  """
    Default append method
  """
  # This is default overload for list append, checking if item is accepted
  if not isinstance(var, self._acceptedTypes):
    raise NotAllowedType( self, var, self._acceptedTypes)
  list.append(self,var)

#def _LimitedTypeList__pop(self, index = -1):
#  """
#    Default append method
#  """
#  if self.__class__.__name__ == "_TexObjectContextManager":
#    print ":: poping ", repr(self[index]), " from TexObjectContextManager ::"
#    import traceback
#    print "STACK:", ''.join(traceback.format_stack())
#  list.pop(self, index)
#
def _LimitedTypeList__extend(self, var):
  """
    Default append method
  """
  # This is default overload for list append, checking if item is accepted
  if not isinstance(var, self._acceptedTypes):
    raise NotAllowedType( self, var, self._acceptedTypes)
  list.extend(self,var)

def _LimitedTypeList____add__(self, var):
  """
    Default __add__ method
  """
  if type(var) in (list, tuple, type(self)):
    for value in var:
      if not isinstance(value, self._acceptedTypes):
        raise NotAllowedType( self, value, self._acceptedTypes )
  else:
    if not isinstance(var, self._acceptedTypes):
      raise NotAllowedType( self, var, self._acceptedTypes)
    var = [ var ]
  # This is default overload for list iadd, checking if item is accepted
  copy = list.__add__(self, var)
  return copy 

# Uncomment this in case you want to have LimitedTypeLists Specifying its type
#def _LimitedTypeList____str__(self):
#  """
#    Default __str__ method
#  """
#  return '< ' + self.__class__.__name__ + list.__str__(self) + ' >'

#def _LimitedTypeList____repr__(self):
#  """
#    Default __repr__ method
#  """
#  return '< ' + self.__class__.__name__ + list.__repr__(self) + ' >'

def _LimitedTypeList____iadd__( self, var, *args ):
  """
    Default __iadd__ method
  """
#  if self.__class__.__name__ == "_TexObjectContextManager":
#    print ":: adding ", repr(var), " to TexObjectContextManager ::"
#    import traceback
#    print "STACK:", ''.join(traceback.format_stack())
  for arg in args:
    if not isinstance( arg, self._acceptedTypes ):
      raise NotAllowedType( self, arg, self._acceptedTypes )
  if type(var) in (list, tuple, type(self)):
    for value in var:
      if not isinstance( value, self._acceptedTypes ):
        raise NotAllowedType( self, value, self._acceptedTypes )
  else:
    if not isinstance(var, self._acceptedTypes):
      raise NotAllowedType( self, var, self._acceptedTypes)
    var = [ var ]
  # This is default overload for list iadd, checking if item is accepted
  list.__iadd__(self, var)
  if args:
    list.__iadd__(self, args)
  return self


def _LimitedTypeList____init__( self, *args ):
  """
    Default __init__ method
  """
  if args:
    self.__iadd__(*args)

def _LimitedTypeList____call__( self ):
  """
    Default __call__ method.
    Yield holden objects.
  """
  for obj in self:
    yield obj

class NotAllowedType(ValueError):
  """
    Raised by LimitedTypeList to sign that it was attempted to add an item to the
    list which is not an allowedType instance.
  """
  def __init__( self , obj, input_, allowedTypes ):
    ValueError.__init__(self, ("Attempted to add to %s an object (type=%s) which is not an "
      "instance from the allowedTypes: %s!") % (obj.__class__.__name__, type(input_),allowedTypes,) )



from . import TexAPI
__all__.extend( TexAPI.__all__ )
from .TexAPI import *

from . import BeamerAPI
__all__.extend( BeamerAPI.__all__ )
from .BeamerAPI import *

