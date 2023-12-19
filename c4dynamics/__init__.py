'''

C4dynamics
==========

C4dynamics Provides
  1. Datapoint objects and sensors for algorithms development.  
  2. Internal systems and 3rd party integrated libraries.
  3. Fast algorithmic operations over objects and systems. 

  

  
How to use the documentation
----------------------------
Documentation is currently availble through examples, 
readme pages, and inline comments.



Available subpackages
---------------------
sensors
  models of EO and EM sensors: radar, camera, imu, gps. 
detectors
  objects detection models to computer vision manipulations.
filters
  kalman filter, asytmptotic observer (luenberger), and lowpass filter.
eqm 
  runge kutta solvers for integrating the equations of motion on the datapoint and rigidbody objects. 
rotmat
  rotation matrices and rotational operations. 
'''

  
# make c_datapoint, c_rigidbody, rotmat belong to pri 
# rather than their modules:
# from .datapoint import c_datapoint 
# from .rigidbody import c_rigidbody


#
# routines 
## 
# from .src.main import py
from . import eqm 
# from .src.main.py.eqm import eqm  
from . import rotmat
# from .src.main.py.rotmat import *

#
# utils
##
from .utils.params import *  
from .utils.gen_gif import gen_gif
from .utils.cprint import print

#
# body objects 
## 
from .body.datapoint import datapoint 
from .body.rigidbody import rigidbody 

#
# sensors
## 
from . import seekers
from . import filters
from . import detectors


#
# version
##
__version__ = '1.0.50'
