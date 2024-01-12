import numpy as np

# directly import a submodule (eqm3) from the c4dynamics.eqm package:
import c4dynamics as c4d 
from c4dynamics.eqm import int3  
# from c4dynamics.src.main.py.eqm import eqm3

def create(X):
  if len(X) > 6:
    rb = c4d.rigidbody()
    rb.X = X
    return rb

  pt = c4d.datapoint()
  pt.X = X 
  return pt
  

class datapoint:





# .. automethod:: c4dynamics.datapoint
#     the datapoint object is the most basic element in the translational dynamics domain.
#     --
#     TBD:
#       - there should be one abstrcact class \ inerface of a 'bodyw type which defines eqm(), store() etc.
#           and datapoint and rigidbody impement it. the body also includes the drawing functions  
#       - all these nice things storage, plot etc. have to be move out of here. 
#       - add an option in the constructor to select the variables required for storage. 
#       - make a dictionary containing the variable name and the variable index in the data storage to save and to extract for plotting. 
#       - add total position, velocity, acceleration variables (path angles optional) and update them for each update in the cartesian components. 
  
  
#   # 
#   # position
#   ##
#    maybe it's a better choise to work with vectors?? 
#       maybe there's an option to define an array which will just designate its enteries. 
#       namely a docker that just references its variables 
#       -> this is actually a function! 
      
      
#       In Python, all variable names are references to values.
# https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference


#   https://docs.python.org/3/library/stdtypes.html
  
  
#   Lists may be constructed in several ways:
#     Using a pair of square brackets to denote the empty list: []
#     Using square brackets, separating items with commas: [a], [a, b, c]
#     Using a list comprehension: [x for x in iterable]
#     Using the type constructor: list() or list(iterable)
    
#   Tuples may be constructed in a number of ways:
#       Using a pair of parentheses to denote the empty tuple: ()
#       Using a trailing comma for a singleton tuple: a, or (a,)
#       Separating items with commas: a, b, c or (a, b, c)
#       Using the tuple() built-in: tuple() or tuple(iterable)
      
#   The arguments to the range constructor must be integers
  


  #
  # position
  #  NOTE: why actually there should be a docstring to every one of the variables. 
  #         unless otherwise mentioned it should transparent to users. and only attributes 
  #         - methods and variables for user ex should be docced.   
  ##
  x = 0 
  ''' float; Cartesian coordinate representing the x-position of the datapoint. '''  
  y = 0 
  ''' float; Cartesian coordinate representing the y-position of the datapoint. '''
  z = 0 
  ''' float; Cartesian coordinate representing the z-position of the datapoint. '''

  # 
  # velocity
  ##
  vx = 0 
  ''' float; Component of velocity along the x-axis. '''
  vy = 0 
  ''' float; Component of velocity along the y-axis. '''
  vz = 0 
  ''' float; Component of velocity along the z-axis. '''

  #
  # acceleration
  ##
  ax = 0  
  ''' float; Component of acceleration along the x-axis. '''
  ay = 0  
  ''' float; Component of acceleration along the y-axis. '''
  az = 0  
  ''' float; Component of acceleration along the z-axis. '''

  # 
  # mass  
  ## 
  mass = 1.0 
  ''' float; Mass of the datapoint. '''

  # https://www.geeksforgeeks.org/getter-and-setter-in-python/
  # https://stackoverflow.com/questions/4555932/public-or-private-attribute-in-python-what-is-the-best-way
  # https://stackoverflow.com/questions/17576009/python-class-property-use-setter-but-evade-getter
  
  


  def __init__(self, **kwargs):
    # reset mutable attributes:
    # 
    # variables for storage
    ##
    

    self._data = []    # for permanent class variables (t, x, y .. )
    self._vardata = {} # for user additional variables 

    self.__dict__.update(kwargs)
    

    self.x0 = self.x
    self.y0 = self.y
    self.z0 = self.z
    self.vx0 = self.vx
    self.vy0 = self.vy
    self.vz0 = self.vz
    
    # fol = os.getcwd() + '/fig'
    # if not os.path.exists(fol):
    #   os.mkdir(fol)

  
    # 
    # variables for storage
    ##
    # _data = [] # np.zeros((1, 10))
    # state variables 
    self._didx = {'t': 0, 'x': 1, 'y': 2, 'z': 3
                  , 'vx': 4, 'vy': 5, 'vz': 6}
                    # , 'ax': 7, 'ay': 8, 'az': 9}
    
    





  @property
  def X(self):
    '''
    Array of the state variables.
    
    X gets or sets the position and velocity variables of a datapoint 
    and rigidbody objects.   
    
    The variables of a datapoint object (position and
    velocity):

    .. math:: 

      X = [x, y, z, vx, vy, vz]  

    The variables of a rigidbody object (extended by 
    the angular position and angular 
    velocity):

    .. math:: 

      X = [x, y, z, v_x, v_y, v_z, {\\varphi}, {\\theta}, {\\psi}, p, q, r]
    

    Parameters (X.setter)
    ---------------------
     x : numpy.array or list
        Values vector to set the first N consecutive indices of the state. 
    
        
    Returns (X.getter)
    ------------------
    out : numpy.array 
        :math:`[x, y, z, v_x, v_y, v_z]` for a datapoint object.

        :math:`[x, y, z, v_x, v_y, v_z, {\\varphi}, {\\theta}, {\\psi}, p, q, r]` for a rigidbody object. 
    

      
    Examples
    --------

    Datapoint state

    .. code:: 
    
      >>> pt = c4d.datapoint()
      >>> print(pt.X)
      [0 0 0 0 0 0]
      >>> # Update the state:
      >>> #       x     y    z  vx vy vz 
      >>> pt.X = [1000, 100, 0, 0, 0, -100] 
      >>> print(pt.X)
      [1000  100    0    0    0 -100]
    
    Rigidbody state

    .. code:: 

      >>> # Get the current state of a rigidbody: 
      >>> rb = c4d.rigidbody(theta = 5 * c4d.d2r)
      >>> print(rb.X)
      [0.  0.  0.  0.  0.  0.   0.   0.08726646   0.   0.   0.   0.]
      >>> # Update only the translational variables of the rigidbody:
      >>> rb.X = [1000, 100, 0, 0, 0, -100] 
      >>> print('  '.join([f'{x}' for x in rb.X]))
      1000.0  100.0  0.0  0.0  0.0  -100.0  0.0  0.08726646259971647  0.0  0.0  0.0  0.0
      
    Partial state 

    Using the setter is possible only to N first consecutive indices. 
    To update other indices, concatenate them by using the X getter.
    The following example sets only the angular variables of a rigidbody: 
    
    .. code:: 
    
      >>> Xangular = np.array([5, -10, 0, 1, -1, 0]) * c4d.d2r 
      >>> rb.X = np.concatenate((rb.X[:6], Xangular))
      >>> print(rb.X[:6])
      [1000.  100.    0.    0.    0. -100.]
      >>> print('  '.join([f'{x * c4d.r2d}' for x in rb.X[6:]]))
      5.0  -10.0  0.0  1.0  -1.0  0.0

    '''

    xout = [] 

    for k in self._didx.keys():
      if k == 't': continue
      xout.append(eval('self.' + k))

    return np.array(xout) 


  @property
  def X0(self):
    '''
    Returns a vector of the initial conditions. 
    
    Initial variables of a datapoint object:

    .. math:: 

      X_0 = [x_0, y_0, z_0, {v_x}_0, {v_y}_0, {v_z}_0]  

    Initial variables of a rigidbody object:

    .. math:: 

      X_0 = [x_0, y_0, z_0, {v_x}_0, {v_y}_0, {v_z}_0, {\\varphi}_0, {\\theta}_0, {\\psi}_0, p_0, q_0, r_0]
      
        
    Returns
    -------
    out : numpy.array 
        :math:`[x_0, y_0, z_0, {v_x}_0, {v_y}_0, {v_z}_0]` for a datapoint object. 
        :math:`[x_0, y_0, z_0, {v_x}_0, {v_y}_0, {v_z}_0, {\\varphi}_0, {\\theta}_0, {\\psi}_0, p_0, q_0, r_0]` for a rigidbody object. 
    

        
    Examples
    --------

    Datapoint initial conditions 

    .. code:: 
    
      >>> pt = c4d.datapoint(x = 1000, vx = -200)
      >>> print(pt.X0)
      [1000    0    0 -200    0    0]

    Change pt.X and check again: 

    .. code::

      >>> pt.X = [500, 500, 0, 0, 0, 0]
      >>> print(pt.X)
      [500 500   0   0   0   0]
      >>> print(pt.X0)
      [1000    0    0 -200    0    0]


    Rigidbody initial conditions: 

    .. code::

      rb = c4d.rigidbody(theta = 5 * c4d.d2r)
      print(rb.X0 * c4d.r2d)
      #x    y    z    vx   vy   vz   phi theta psi  p    q    r
      [0.   0.   0.   0.   0.   0.   0.   5.   0.   0.   0.   0.]
      
    '''
    xout = [] 

    for k in self._didx.keys():
      if k == 't': continue
      xout.append(eval('self.' + k + '0'))

    return np.array(xout) 
  

  @property
  def pos(self):
    ''' 
    Returns a translational position vector. 
     
    .. math:: 

      pos = [x, y, z]      
        

    Returns
    -------
    out : numpy.array 
        :math:`[x, y, z]` 
  
        
    Examples
    --------

    .. code:: 
    
      >>> pt = c4d.datapoint(x = 1000, y = -20, vx = -200)
      >>> print(pt.pos)
      [1000    -20    0]

    '''
    return np.array([self.x, self.y, self.z])


  @property
  def vel(self):
    ''' 
    Returns a translational velocity vector. 
     
    .. math:: 

      vel = [v_x, v_y, v_z]      
        

    Returns
    -------
    out : numpy.array 
        :math:`[v_x, v_y, v_z]` 
  
        
    Examples
    --------

    .. code:: 
    
      >>> pt = c4d.datapoint(x = 1000, y = -20, vx = -200)
      >>> print(pt.vel)
      [-200    0    0]

    '''
    return np.array([self.vx, self.vy, self.vz])
  

  @X.setter
  def X(self, x):
    ''' Docstring under X.getter '''
    for i, k in enumerate(self._didx.keys()):
      if k == 't': continue
      if i > len(x): break 
      # eval('self.' + k + ' = ' + str(x[i - 1]))
      setattr(self, k, x[i - 1])

 

  #
  # methods
  ##


  #
  # storage operations 
  ##
  def store(self, t = -1):
    ''' 
    Stores the current state of the datapoint.

    The current state is defined by the vector of variables 
    as given by the :attr:`X <datapoint.X>`:

    Datapoint: :math:`[t, x, y, z, vx, vy, vz]`. 

    Rigidbody: :math:`[t, x, y, z, vx, vy, vz, \\phi, \\theta, \\psi, p, q, r]`. 


    Parameters 
    ----------
    t : float or int, optional 
        Values vector to set the first N consecutive indices of the state. 
    
    Note
    ----
    1. Time t is an optional parameter with a default value of t = -1.
    The time is always appended at the head of the array to store. However, 
    if t is not given, default t = -1 is stored instead.

    2. The method :attr:`store <datapoint.store>` goes together with 
    the methods :attr:`get_data <datapoint.get_data>` 
    and :attr:`timestate <datapoint.timestate>` as input and outputs. 


    Examples
    --------

    Store the given state without time stamps:

    .. code:: 
      
      >>> pt = c4d.datapoint()
      >>> for i in range(3):
      ...    pt.X = np.random.randint(1, 100, 6)
      ...    pt.store()
      >>> for x in pt.get_data():
      ...    print(x)
      [-1 30 67 69 67 31 37]
      [-1 87 62 36  2 44 97]
      [-1 30 30  6 75  7 11]

    A default of t = -1 was appended to the stored vector.
    In this case, it is a good practice to exclude the vector header (time column):

    .. code::

      >>> for x in pt.get_data():

      ...    print(x[1:])
      [30 67 69 67 31 37]
      [87 62 36  2 44 97]
      [30 30  6 75  7 11]

    Store with time stamps: 
    
    .. code::           
     
      >>> t = 0
      >>> dt = 1e-3
      >>> h0 = 100 
      >>> pt = c4d.datapoint(z = h0)
      >>> while pt.z >= 0: 
      ...     pt.inteqm([0, 0, -c4d.g_ms2], dt)
      ...    t += dt
      ...    pt.store(t)
      >>> for z in pt.get_data('z'):
      ...    print(z)
      99.999995096675
      99.99998038669999
      99.99995587007498
      ...
      0.00033469879436880123
      -0.043957035930635484


    ''' 
    
    self._data.append([t] + self.X.tolist())
    

  def storevar(self, var, t = -1):
    ''' 
    Stores additional user-defined variables. 

    User-defined variables are those that do not appear 
    with new constructed instance of a :class:`datapoint` or 
    a :class:`rigidbody` object. 


    Parameters 
    ----------
    var : string
        Name of the user-defined variable to store. 
    t : float or int, optional 
        Values vector to set the first N consecutive indices of the state. 
    
    Note
    ----
    1. Time t is an optional parameter with a default value of t = -1.
    The time is always appended at the head of the array to store. However, 
    if t is not given, default t = -1 is stored instead.

    2. The method :attr:`storevar <datapoint.storevar>` goes together with 
    the method :attr:`get_data <datapoint.get_data>` 
    as input and output. 
    

    Examples
    --------

    The morphospectra extends the datapoint class to include also a dimension
    state. 
    The X.setter overrides the datapoint.X.setter to update the dimension with 
    respect to the input coordinates. 

    .. code:: 
      
      >>> class morphospectra(c4d.datapoint):
      ...   def __init__(self): 
      ...     super().__init__()  
      ...     self.dim = 0
      ...   @c4d.datapoint.X.setter
      ...   def X(self, x):
      ...     # override X.setter mechanism
      ...     for i, k in enumerate(self._didx.keys()):
      ...       if k == 't': continue
      ...       if i > len(x): break 
      ...       setattr(self, k, x[i - 1]) 
      ...       # update current dimension 
      ...       if x[2] != 0:
      ...         # z 
      ...         self.dim = 3
      ...         return None 
      ...       if x[1] != 0:
      ...         # y 
      ...         self.dim = 2
      ...         return None
      ...       if x[0] != 0:
      ...         self.dim = 1
      ... 
      >>> spec = morphospectra()
      >>> for r in range(10):
      ...   spec.X = np.random.choice([0, 1], 3)
      ...   spec.store()
      ...   spec.storevar('dim')
      ... 
      >>> x_hist = spec.get_data()
      >>> print('x y z  | dim')
      >>> print('------------')
      >>> for x, dim in zip(spec.get_data()[:, 1 : 4].tolist(), spec.get_data('dim')[:, 1:].tolist()):
      ...   print(*(x + [' | '] + dim))
      x y z  | dim
      ------------
      0 1 0  |  2
      1 1 0  |  2
      1 0 0  |  1
      0 1 1  |  3
      1 0 0  |  1
      1 1 1  |  3
      1 1 0  |  2
      1 1 0  |  2
      1 0 1  |  3
      1 0 1  |  3




    '''
    # TODO: add the docstring the example of the kalman variables store from the detect track exmaple. 
    lvar = var if isinstance(var, list) else [var]
    for v in lvar:
      if v not in self._vardata:
        self._vardata[v] = []
      self._vardata[v].append([t, getattr(self, v)])

  
  def get_data(self, var = None):
    ''' 
    Returns an array of state histories.

    Returns the time histories of the variable `var`
    at the samples that sotred with :attr:`store <datapoint.store>` or 
    :attr:`storevar <datapoint.storevar>`. 
    Possible values of `var` for built-in state variables:

    't', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'phi', 'theta', 'psi', 'p', 'q', 'r'. 

    For user defined variables, any value of `var` is optional, if `var` matches the 
    variable name and it has histories of stored samples. 

    If `var` is not introduced, returns the histories of the entire state. 
    If histories were'nt stored, returns an empty array. 


    Parameters
    ----------
    var : string 
        The name of the variable of the required histories. 
    
        
    Returns
    -------
    out : numpy.array 
        An array of the sample histories. 
        if `var` is introduced, out is one-dimensioanl numpy array.
        If `var` is not introduced, then nxm two dimensional numpy array is returned, 
        where n is the number of stored samples, and m is 1 + 6 (time + state variables) 
        for a datapoint object, and 1 + 12 (time + state variables) for a rigidbody object. 

            
    Note
    ----
    The time stamps are also stored on calling to the store functions 
    (:attr:`store <datapoint.store>`, :attr:`storevar <datapoint.storevar>`).
    To get an array of the time histories, :attr:`get_data <datapoint.get_data>`
    should be called with as: `get_data('t')`. If :attr:`get_data <datapoint.get_data>`
    is called without explicit `var`, the location of the time histories is the first column.

    Examples
    --------

    `get_data` of a specific variable: 
    
    .. code::           
     
      >>> t = 0
      >>> dt = 1e-3
      >>> h0 = 100 
      >>> pt = c4d.datapoint(z = h0)
      >>> while pt.z >= 0: 
      ...    pt.inteqm([0, 0, -c4d.g_ms2], dt)
      ...    t += dt
      ...    pt.store(t)
      >>> for z in pt.get_data('z'):
      ...    print(z)
      99.999995096675
      99.99998038669999
      99.99995587007498
      ...
      0.00033469879436880123
      -0.043957035930635484


    `get_data` of an entire state:  

    .. code:: 
      
      >>> pt = c4d.datapoint()
      >>> for i in range(3):
      ...    pt.X = np.random.randint(1, 100, 6)
      ...    pt.store()
      >>> for x in pt.get_data():
      ...    print(x)
      [-1 30 67 69 67 31 37]
      [-1 87 62 36  2 44 97]
      [-1 30 30  6 75  7 11]

    A default of t = -1 was appended to the stored vector.
    In this case, it is a good practice to exclude the vector header (time column):

    .. code::

      >>> for x in pt.get_data():

      ...    print(x[1:])
      [30 67 69 67 31 37]
      [87 62 36  2 44 97]
      [30 30  6 75  7 11]


    `get_data` of a user defined variable: 
    
    The morphospectra extends the datapoint class to include also a dimension
    state. 
    The X.setter overrides the datapoint.X.setter to update the dimension with 
    respect to the input coordinates. 

    .. code:: 
      
      >>> class morphospectra(c4d.datapoint):
      ...   def __init__(self): 
      ...     super().__init__()  
      ...     self.dim = 0
      ...   @c4d.datapoint.X.setter
      ...   def X(self, x):
      ...     # override X.setter mechanism
      ...     for i, k in enumerate(self._didx.keys()):
      ...       if k == 't': continue
      ...       if i > len(x): break 
      ...       setattr(self, k, x[i - 1]) 
      ...       # update current dimension 
      ...       if x[2] != 0:
      ...         # z 
      ...         self.dim = 3
      ...         return None 
      ...       if x[1] != 0:
      ...         # y 
      ...         self.dim = 2
      ...         return None
      ...       if x[0] != 0:
      ...         self.dim = 1
      ... 
      >>> spec = morphospectra()
      >>> for r in range(10):
      ...   spec.X = np.random.choice([0, 1], 3)
      ...   spec.store()
      ...   spec.storevar('dim')
      ... 
      ... # get the data of the user-defined 'dim' variable: 
      ... dim_history = spec.get_data('dim')[:, 1:]
      ...
      >>> print('x y z  | dim')
      >>> print('------------')
      >>> for x, dim in zip(spec.get_data()[:, 1 : 4].tolist(), spec.get_data('dim')[:, 1:].tolist()):
      ...   print(*(x + [' | '] + dim))
      x y z  | dim
      ------------
      0 1 0  |  2
      1 1 0  |  2
      1 0 0  |  1
      0 1 1  |  3
      1 0 0  |  1
      1 1 1  |  3
      1 1 0  |  2
      1 1 0  |  2
      1 0 1  |  3
      1 0 1  |  3

    '''
    # one of the pregiven variables t, x, y ..
    
    if var is None: 
      return np.array(self._data)
     
    idx = self._didx.get(var, -1)
    if idx >= 0:
      return np.array(self._data)[:, idx] if self._data else np.empty(1)

    # else \ user defined variables 
    return np.array(self._vardata.get(var, np.empty((1, 2))))
    

  def timestate(self, t):
    '''
    Returns the state as stored at time t. 

    The function searches the closest time  
    to the time t in the sampled histories and 
    returns the state that stored at the time.  

    Parameters
    ----------
    t : float or int  
        The time of the required sample. 
            
    Returns
    -------
    out : numpy.array 
        An array of the sample at time t. 
        One-dimensioanl numpy array of 6 state variables 
        for a datapoint object or 
        12 variables for a rigidbody object. 


    Examples
    --------

    .. code:: 

      >>> pt = c4d.datapoint()
      >>> time = np.linspace(-2, 3, 1000)
      >>> for t in time: 
      ...   pt.X = np.random.randint(1, 100, 6)
      ...   pt.store(t)
      >>> print(pt.timestate(0))
      [6, 9, 53, 13, 49, 99]

    '''
    # TODO how about throwing a warning when dt is too long? 
    times = self.get_data('t')
    if times.size == 0: 
      out = None
    else:
      idx = min(range(len(times)), key = lambda i: abs(times[i] - t))
      out = self._data[idx][1:]

    return out 
    

  # 
  # to norms:
  ##
  def P(self):
    ''' 
    Returns the Euclidean norm of the position coordinates in three dimensions. 
    
    This method computes the Euclidean norm (magnitude) of a 3D vector represented
    by the instance variables self.x, self.y, and self.z:

    .. math::
      P = \\sqrt{x^2 + y^2 + z^2}
            

    Returns
    -------
    out : numpy.float64
        Euclidean norm of the 3D position vector.


    Examples
    --------
    .. code::

      >>> pt = c4d.datapoint(x = 7, y = 24)
      >>> print(pt.P())
      25.0
      >>> pt.X = np.zeros(6)
      >>> print(pt.P())
      0.0

    '''
    return np.sqrt(self.x**2 + self.y**2 + self.z**2)
  
  
  def V(self):
    ''' 
    Returns the Euclidean norm of the velocity coordinates in three dimensions. 

    This method computes the Euclidean norm (magnitude) of a 3D vector represented
    by the instance variables self.vx, self.vy, and self.vz:

    .. math::
      V = \\sqrt{v_x^2 + v_y^2 + v_z^2}

            

    Returns
    -------
    out : numpy.float64
        Euclidean norm of the 3D velocity vector.


    Examples
    --------
    .. code::

      >>> pt = c4d.datapoint(vx = 7, vy = 24)
      >>> print(pt.V())
      25.0
      >>> pt.X = np.zeros(6)
      >>> print(pt.V())
      0.0

    '''
    return np.sqrt(self.vx**2 + self.vy**2 + self.vz**2)
  
  
  #
  # two objects operation
  ##
  def dist(self, dp2):
    ''' 
    Calculates the Euclidean distance between the self body and 
    a second datapoint 'dp2'.

    .. math:: 

      dist = \\sqrt{(self.x - dp2.x)^2 + (self.y - dp2.y)^2 + (self.z - dp2.z)^2}
    

    This method computes the Euclidean distance between the current 3D point
    represented by the instance variables self.x, self.y, and self.z, and another
    3D point represented by the provided DataPoint object, dp2.

    
    Parameters
    ----------
    dp2 : datapoint
        A second datapoint object for which the distance should be calculated.  

    Returns
    -------
    out : numpy.float64
        Euclidean norm of the 3D range vector.


    Examples
    --------
    .. code::
    
      >>> camera = c4d.datapoint()
      >>> car = c4d.datapoint(x = -100, vx = 40, vy = -7)
      >>> dist = []
      >>> time = np.linspace(0, 10, 1000)
      >>> for t in time:
      ...   car.inteqm(np.zeros(3), time[1] - time[0])
      ...   dist.append(camera.dist(car))
      >>> plt.plot(time, dist, 'm', linewidth = 2)

    .. figure:: /_static/figures/distance.png



    '''
    return np.sqrt((self.x - dp2.x)**2 + (self.y - dp2.y)**2 + (self.z - dp2.z)**2)
  
  
  #
  # runge kutta integration
  ##
  def inteqm(self, forces, dt):
    ''' 
    Advances the state vector, `datapoint.X`, with respect to the input
    forces on a single step of time, `dt`.

    Integrates equations of three degrees translational motion using the Runge-Kutta method. 

    This method numerically integrates the equations of motion for a dynamic system
    using the fourth-order Runge-Kutta method as given by 
    :func:`int3 <c4dynamics.eqm.int3>`. 

    The derivatives of the equations are of three dimensional translational motion as 
    given by 
    :py:func:`eqm3 <c4dynamics.eqm.eqm3>` 
    
    
    Parameters
    ----------
    forces : numpy.array or list
        An external forces vector acting on the body, `forces = [Fx, Fy, Fz]`  
    dt : float
        Interval time step for integration.


    Returns
    -------
    out : numpy.float64
        An acceleration array at the final time step.


    
    Examples
    --------

    A Helium balloon of 100g weight floats with lift force of L = 0.05N
    and expreiences a side wind of 10k speed.

    .. code::

      >>> t1, t2, dt = 0, 10, 0.01
      >>> F = [0, 0, .05]
      >>> hballoon = c4d.datapoint(mass = 0.1, vx = 10 * c4d.k2ms)
      >>> for t in np.arange(t1, t2, dt):
      ...    hballoon.inteqm(F, dt)
      ...    hballoon.store(t)
      >>> hballoon.draw('side')
      >>> plt.gca().invert_yaxis()

    .. figure:: /_static/figures/inteqm3.png


    '''
    self.X, acc = int3(self, forces, dt, derivs_out = True)
    return acc
     
  
  
  # 
  # plot functions
  ##
  def draw(self, var, ax = None):
    ''' 
    Draws plots of trajectories or variable evolution over time. 

    `var` can be `top` or `side` for trajectories, or each one of the state variables. 


    Parameters
    ----------

    var : string
        The variable to be plotted. 
        Possible variables for trajectories: 'top', 'side'.
        For time evolution, any one of the state variables is possible: 
        'x', 'y', 'z', 'vx', 'vy', 'vz' - for datapoint object, and
        also 'phi', 'theta', 'psi', 'p', 'q', 'r' - for rigidbody object. 

        

    Notes
    -----
    
    - The function uses matplotlib for plotting.

    - Trajectory views ('top' and 'side') show the crossrange vs. downrange or downrange vs. altitude.
    
    



    Examples
    --------

    .. code:: 

      >>> pt = c4d.datapoint()
      >>> for t in np.arange(0, 10, .01):
      ...   pt.x = 10 + np.random.randn()
      ...   pt.store(t)
      >>> pt.draw('x')
      >>> plt.gca().set_ylim(0, 13)

    .. figure:: /_static/figures/draw_x.png


    .. code::

      >>> t1, t2, dt = 0, 10, 0.01
      >>> F = [0, 0, .05]
      >>> hballoon = c4d.datapoint(mass = 0.1, vx = 10 * c4d.k2ms)
      >>> for t in np.arange(t1, t2, dt):
      ...    hballoon.inteqm(F, dt)
      ...    hballoon.store(t)
      >>> hballoon.draw('side')
      >>> plt.gca().invert_yaxis()

    .. figure:: /_static/figures/inteqm3.png


    
    
    '''

    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = (6.0, 4.0) # set default size of plots
    # plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams["font.size"] = 14
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams["font.family"] = "Times New Roman"   # "Britannic Bold" # "Modern Love"#  "Corbel Bold"# 
    plt.style.use('dark_background')  # 'default' # 'seaborn' # 'fivethirtyeight' # 'classic' # 'bmh'
    
    # plt.ion()
    # plt.show()

    # grid
    # increase margins for labels. 
    # folder for storage
    # dont close
    # integrate two objects for integration and plotting.
    
    if ax is None: 
      _, ax = plt.subplots()
    
    if var.lower() == 'top':
      # x axis: y data
      # y axis: x data 
      x = self.get_data('y')
      y = self.get_data('x')
      xlabel = 'Crossrange'
      ylabel = 'Downrange'
      title = 'Top View'
    elif var.lower() == 'side':
      # x axis: x data
      # y axis: z data 
      x = self.get_data('x')
      y = self.get_data('z')
      xlabel = 'Downrange'
      ylabel = 'Altitude'
      title = 'Side View'
      ax.invert_yaxis()
    else: 
      uconv = 1
      if self._didx[var] >= 7: # 7 and above are angular variables 
        uconv = 180 / np.pi     
      
      if not len(np.flatnonzero(self.get_data('t') != -1)): # values for t weren't stored
        x = range(len(np.array(self.get_data('t')))) # t is just indices 
        xlabel = 'Sample'
      else:
        x = np.array(self.get_data('t')) 
        xlabel = 'Time'
      y = np.array(self._data)[:, self._didx[var]] * uconv if self._data else np.empty(1) # used selection 
      

      if 1 <= self._didx[var] <= 6:
        # x, y, z, vx, vy, vz
        title = ylabel = var.title()
      elif 7 <= self._didx[var] <= 9: 
        # phi, theta, psi
        title = '$\\' + var + '$'
        ylabel = title + ' (deg)'
      elif 10 <= self._didx[var] <= 12: 
        # p, q, r 
        title = var.title()
        ylabel = var + ' (deg/sec)'

    ax.plot(x, y, 'm', linewidth = 2)

    ax.set_title(title)
    # plt.xlim(0, 1000)
    # plt.ylim(0, 1000)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha = 0.5)
    # plt.axis('off')
    # plt.savefig(self.fol + "/" + var) 
    # fig.tight_layout()
    
    # plt.pause(1e-3)
    # plt.show() # block = True # block = False


