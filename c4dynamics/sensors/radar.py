import numpy as np
# from scipy.special import erfinv
import c4dynamics as c4d 
from c4dynamics.sensors.seeker import seeker

# np.warnings.filterwarnings('ignore', category = np.VisibleDeprecationWarning)                 
 
class radar(seeker):
  '''
  Range-direction detector.

  `radar` is a subclass of :class:`seeker <c4dynamics.sensors.seeker.seeker>` 
  and utilizes its functionality and errors model for angular measurements. 
  This documentation supplaments the information concerning range measurements. 
  Refer to :class:seeker for the full documentation.


  The `radar` class models sensors that 
  measure both the range and the direction to a target.
  The direction is measured in terms of azimuth and elevation. 
  Sensors that provide precise range measurements 
  typically use electro-magnetical technology, 
  though other technologies may also be employed. 

  As a subclass of `seeker`, the `radar`
  can operate in one of two modes: ideal mode, 
  providing precise range and direction measurements, 
  or non-ideal mode, 
  where measurements may be affected by errors such as
  `scale factor`, `bias`, and `noise`, 
  according to the errors model. 
  A random variable generation mechanism allows 
  for Monte Carlo simulations.   


  
  Parameters
  ==========

  origin : :class:`rigidbody <c4dynamics.states.lib.rigidbody.rigidbody>`, optional 
      A `rigidbody` object whose state vector :attr:`X <c4dynamics.states.state.state.X>` 
      determines the radar's initial position and attitude. 
      Defaults: a `rigidbody` object with zeros vector, `X = numpy.zeros(12)`.
  isideal : bool, optional 
      A flag indicating whether the errors model is off. 
      Defaults False. 



  Keyword Arguments 
  =================
  rng_noise_std : float 
      A standard deviation of the radar range. Default value for non-ideal radar: `rng_noise_std = 1m`. 
  bias_std : float 
      The standard deviation of the bias error, [radians]. Defaults :math:`0.3°`.
  scale_factor_std : float 
      The standard deviation of the scale factor error, [dimensionless]. Defaults :math:`0.07 (= 7\\%)`. 
  noise_std : float
      The standard deviation of the radar angular noise, [radians]. 
      Default value for non-ideal radar: :math:`0.8°`. 
  dt : float
      The time-constant of the operational rate of the radar 
      (below which the radar measures return None), [seconds]. Default value: :math:`dt = -1sec` 
      (no limit between calls to :meth:`measure`). 


  * Note the default values for angular parameters, `bias_std`, `scale_factor_std`, 
    and `noise_std`, differ from those in a `seeker` object. 

  

  See Also
  ========
  .filters 
  .eqm 
  .seeker

  


  **Functionality**


  At each sample the seeker returns measures based on the true geometry 
  with the target.

  Let the relative coordinates in an arbitrary frame of reference: 

  .. math::

    dx = target.x - seeker.x

    dy = target.y - seeker.y

    dz = target.z - seeker.z
  

  The relative coordinates in the seeker body frame are given by: 

  .. math::

    x_b = [BR] \\cdot [dx, dy, dz]^T 

  where :math:`[BR]` is a 
  Body from Reference DCM (Direction Cosine Matrix)
  formed by the seeker three Euler angles. See the `rigidbody` section below. 

  The azimuth and elevation measures are then the spatial angles: 
  
  .. math:: 

    az = tan^{-1}{x_b[1] \\over x_b[0]}

    el = tan^{-1}{x_b[2] \\over \\sqrt{x_b[0]^2 + x_b[1]^2}}

  
  Where:

  - :math:`az` is the azimuth angle
  - :math:`el` is the elevation angle
  - :math:`x_b` is the target-radar position vector in radar body frame


  For a `radar` object, the range is defined as: 

  .. math::

      range = \\sqrt{x_b^2 + y_b^2 + z_b^2}

  Where:

  - :math:`range` is the target-radar distance 
  - :math:`x_b` is the target-radar position vector in radar body frame


  .. figure:: /_static/figures/radar/definitions.svg
    
    Fig-1: Range and angles definition

      
  **Errors Model**
  
  The azimuth and elevation angles are subject to errors: scale factor, bias, and noise, 
  as detailed in `seeker`. 
  A `radar` instance has in addition range noise: 

  - ``Range Noise``: 
    represents random variations or fluctuations in the measurements 
    that are not systematic. 
    The noise at each sample (:meth:`measure`) 
    is a normally distributed variable 
    with `mean = 0` and `std = rng_noise_std`, where `rng_noise_std` 
    is a `radar` parameter with default value of `1m`.  

  Angular errors:

  - ``Bias``: 
    represents a constant offset or deviation from the 
    true value in the seeker's measurements. 
    It is a systematic error that consistently affects the measured values. 
    The bias of a `seeker` instance is a normally distributed variable with `mean = 0` 
    and `std = bias_std`, where `bias_std` is a parameter with default value of `0.3°`.
  - ``Scale Factor``: 
    a multiplier applied to the true value of a measurement. 
    It represents a scaling error in the measurements made by the seeker. 
    The scale factor of a `seeker` instance is 
    a normally distributed variable 
    with `mean = 0` and `std = scale_factor_std`, 
    , where `scale_factor_std` is a parameter with default value of `0.07`. 
  - ``Noise``: 
    represents random variations or fluctuations in the measurements 
    that are not systematic. 
    The noise at each seeker sample (:meth:`measure`) 
    is a normally distributed variable 
    with `mean = 0` and `std = noise_std`, where `noise_std` 
    is a parameter with default value of `0.8°`.    
   
  

  The errors model generates random variables for each radar instance, 
  allowing for the simulation of different scenarios or variations in the radar behavior
  in a technique known as Monte Carlo. 
  Monte Carlo simulations leverage this randomness to statistically analyze 
  the impact of these biases and scale factors over a large number of iterations, 
  providing insights into potential outcomes and system reliability.

  

  **Radar vs Seeker**
      
  
  The following table
  lists the main differences between 
  :class:`seeker <c4dynamics.sensors.seeker.seeker>` and :class:radar 
  in terms of measurements and 
  default error parameters:
     
    

  .. list-table:: 
    :widths: 22 13 13 13 13 13 13  
    :header-rows: 1

    * - 
      - Angles
      - Range
      - :math:`σ_{Bias}`
      - :math:`σ_{Scale Factor}`
      - :math:`σ_{Angular Noise}`
      - :math:`σ_{Range Noise}`

    * - Seeker 
      - ✔️
      - ❌
      - :math:`0.1°`
      - :math:`5%`
      - :math:`0.4°`
      - :math:`--`

    * - Radar 
      - ✔️
      - ✔️
      - :math:`0.3°`
      - :math:`7%`
      - :math:`0.8°`
      - :math:`1m`

    


  **rigidbody**
  
  The radar class is also a subclass of 
  :class:`rigidbody <c4dynamics.states.lib.rigidbody.rigidbody>`, i.e. 
  it suggests attributes of position and attitude and the manipulation of them.

  As a fundamental propety, the 
  rigidbody's state vector 
  :attr:`X <c4dynamics.states.state.state.X>` 
  sets the spatial coordinates of the radar:

  .. math::

    X = [x, y, z, v_x, v_y, v_z, {\\varphi}, {\\theta}, {\\psi}, p, q, r]^T 

  The first six coordinates determine the translational position and velocity of the radar 
  while the last six determine its angular attitude in terms of Euler angles and 
  the body rates. 

  Passing a rigidbody parameter as an `origin` sets 
  the initial conditions of the radar. 

  
  
  **Construction**

  A radar instance is created by making a direct call 
  to the radar constructor: 

  .. code:: 

    rdr = c4d.sensors.radar()

  Initialization of the instance does not require any 
  mandatory arguments, but the radar parameters can be 
  determined using the \\**kwargs argument as detailed above.




  Examples 
  ========

  **Target**
  

  For the examples below let's generate the trajectory of a target with constant velocity:   

  .. code::

    >>> tgt = c4d.datapoint(x = 1000, y = 0, vx = -80 * c4d.kmh2ms, vy = 10 * c4d.kmh2ms)
    >>> for t in np.arange(0, 60, 0.01):
    ...   tgt.inteqm(np.zeros(3), .01)
    ...   tgt.store(t)

  The method :meth:`inteqm <c4dynamics.states.lib.datapoint.datapoint.inteqm>` 
  of the 
  :class:`datapoint <c4dynamics.states.lib.datapoint.datapoint>` class 
  integrates the 3 degrees of freedom equations of motion with respect to 
  the input force vector (`np.zeros(3)` here). 
  
  .. figure:: /_static/figures/radar/target.png

  Since the call to :meth:`measure` requires a target as a `datapoint` object 
  we utilize a custom `create` function that returns a new `datapoint` object for 
  a given `X` state vector in time. 

  - :code:`c4d.kmh2ms` converts kilometers per hour to meters per second.
  - :code:`c4d.r2d` converts radians to degrees.
  - :code:`c4d.d2r` converts degrees to radians.

  
  **Origin**
  
  Let's also introduce a pedestal as an origin for the radar. 
  The pedestal is a `rigidbody` object with position and attitude: 

  .. code:: 

    >>> pedestal = c4d.rigidbody(z = 30, theta = -1 * c4d.d2r)



    

  **Ideal Radar**
  
  Measure the target position with an ideal radar:

  .. code::

    >>> rdr_ideal = c4d.sensors.radar(origin = pedestal, isideal = True)
    >>> for x in tgt.data():
    ...   rdr_ideal.measure(c4d.create(x[1:]), t = x[0], store = True)
    
  Comparing the radar measurements with the true target angles requires 
  converting the relative position to the radar body frame: 

  .. code:: 

    >>> dx =  tgt.data('x')[1] - rdr_ideal.x
    >>> dy =  tgt.data('y')[1] - rdr_ideal.y
    >>> dz =  tgt.data('z')[1] - rdr_ideal.z
    >>> Xb = np.array([rdr_ideal.BR @ [X[1] - rdr_ideal.x, X[2] - rdr_ideal.y, X[3] - rdr_ideal.z] for X in tgt.data()])

  where :attr:`rdr_ideal.BR <c4dynamics.states.lib.rigidbody.rigidbody.BR>` is a 
  Body from Reference DCM (Direction Cosine Matrix)
  formed by the radar three Euler angles

  Now `az_true` and `el_true` are the true target angles with respect to the radar, and 
  `rng_true` is the true range (`atan2d` is an aliasing of `numpy's arctan2` 
  with a modification returning the angles in degrees): 

  .. code:: 

    >>> az_true = c4d.atan2d(Xb[:, 1], Xb[:, 0])
    >>> el_true = c4d.atan2d(Xb[:, 2], c4d.sqrt(Xb[:, 0]**2 + Xb[:, 1]**2))
    >>> # plot results
    >>> fig, axs = plt.subplots(2, 1)
    >>> # range
    >>> axs[0].plot(tgt.data('t'), c4d.norm(Xb, axis = 1), label = 'target')
    >>> axs[0].plot(*rdr_ideal.data('range'), label = 'radar')
    >>> # angles 
    >>> axs[1].plot(tgt.data('t'), c4d.atan2d(Xb[:, 1], Xb[:, 0]), label = 'target azimuth')
    >>> axs[1].plot(*rdr_ideal.data('az', scale = c4d.r2d), label = 'radar azimuth')
    >>> axs[1].plot(tgt.data('t'), c4d.atan2d(Xb[:, 2], c4d.sqrt(Xb[:, 0]**2 + Xb[:, 1]**2)), label = 'target elevation')
    >>> axs[1].plot(*rdr_ideal.data('el', scale = c4d.r2d), label = 'radar elevation')

  .. figure:: /_static/figures/radar/ideal.png



  

  **Non-ideal Radar**
  

  Measure the target position with a *non-ideal* radar. 
  The radar's errors model introduces bias, scale factor, and 
  noise that corrupt the measurements: 

  .. code:: 

    >>> rdr = c4d.sensors.radar(origin = pedestal)
    >>> for x in tgt.data():
    ...   rdr.measure(c4d.create(x[1:]), t = x[0], store = True)

  With respect to the ideal radar: 

  .. code:: 

    >>> fig, axs = plt.subplots(2, 1)
    >>> # range     
    >>> axs[0].plot(*rdr_ideal.data('range'), label = 'target')
    >>> axs[0].plot(*rdr.data('range'), label = 'radar')
    >>> # angles  
    >>> axs[1].plot(*rdr_ideal.data('az', scale = c4d.r2d), label = 'target azimuth')
    >>> axs[1].plot(*rdr.data('az', scale = c4d.r2d), label = 'radar azimuth')
    >>> axs[1].plot(*rdr_ideal.data('el', scale = c4d.r2d), label = 'target elevation')
    >>> axs[1].plot(*rdr.data('el', scale = c4d.r2d), label = 'radar elevation')

  `target` labels mean the true position as measured by an ideal radar. 

  .. figure:: /_static/figures/radar/nonideal.png

  
  The bias, scale factor, and noise that used to generate these measures 
  can be examined by: 

  .. code::

    >>> rdr.rng_scale_factor 
    3
    >>> rdr.bias * c4d.r2d
    0.4
    >>> rdr.scale_factor
    1.07
    >>> rdr.noise_std
    0.01

  Points to consider here: 

  - The scale factor error increases with the angle, such that for a :math:`7%` 
    scale factor, 
    the error of :math:`Azimuth = 100°` is :math:`7°`, whereas the error for 
    :math:`Elevation = -15°` is only :math:`-1.05°`.  
  - The standard deviation of the noise in the two angle channels is the same. 
    However, as the `Elevation` values are confined to a smaller range, the effect 
    appears more pronounced there.  
    



  **Rotating Radar**
  

  Measure the target position with a rotating radar. 
  The radar origin is yawing (performed by the increment of :math:`\\psi`) in the direction of the target motion: 


  .. code::
    
    >>> rdr = c4d.sensors.radar(origin = pedestal)
    >>> for x in tgt.data():
    ...   rdr.psi += .02 * c4d.d2r 
    ...   rdr.measure(c4d.create(x[1:]), t = x[0], store = True)
    ...   rdr.store(x[0])

  The radar yaw angle: 

  .. figure:: /_static/figures/radar/psi.png

  And the target angles with respect to the yawing radar are: 

  .. code:: 

    >>> fig, axs = plt.subplots(2, 1)
    >>> # range    
    >>> axs[0].plot(*rdr_ideal.data('range'), label = 'ideal static')
    >>> axs[0].plot(*rdr.data('range'),label = 'non-ideal yawing')
    >>> # angles
    >>> axs[1].plot(*rdr_ideal.data('az', c4d.r2d), label = 'az: ideal static')
    >>> axs[1].plot(*rdr.data('az', c4d.r2d), label = 'az: non-ideal yawing')
    >>> axs[1].plot(*rdr_ideal.data('el', scale = c4d.r2d), label = 'el: ideal static')
    >>> axs[1].plot(*rdr.data('el', scale = c4d.r2d), label = 'el: non-ideal yawing')

  .. figure:: /_static/figures/radar/yawing.png

  
  - The rotation of the radar with the target direction 
    keeps the azimuth angle limited, such that non-rotating radars with limited FOV (field of view) 
    would have lost the target. 

    

  **Operation Time**
  
  By default, the radar returns measurments for each 
  call to :meth:`measure`. However, setting the parameter `dt` 
  to a positive number makes `measure` return `None` 
  for any `t < last_t + dt`, where `t` is the current measure time, 
  `last_t` is the last measurement time, and `dt` is the radar time-constant: 

  .. code:: 
  
    >>> tgt = c4d.datapoint(x = 100, y = 100)
    >>> rdr = c4d.sensors.radar(dt = 0.01)
    >>> for t in np.arange(0, .025, .005):
    ...   print(f'{t}: {rdr.measure(tgt, t = t)}')
    0.0:    (0.71, 0.005, 141.2)
    0.005:  (None, None, None)
    0.01:   (0.74, -0.007, 140.7)
    0.015:  (None, None, None)
    0.02:   (0.73, -0.02, 142.2)

    
  **Random Distribution** 

 
  The distribution of normally generated random variables 
  is characterized by its bell-shaped curve, which is symmetric about the mean.
  The area under the curve represents probability, with about `68%` of the data 
  falling within one standard deviation (1σ) of the mean, `95%` within two, 
  and `99.7%` within three,   
  making it a useful tool for understanding and predicting data behavior.


  In `radar` objects, and `seeker` objects in general, 
  the `bias` and `scale factor` vary 
  among different instances to allow a realistic simulation 
  of performance behavior in a technique known as Monte Carlo.
  
  Let's examine the `bias` distribution across   
  
  mutliple `radar` instances with a default `bias_std = 0.3°`
  in comparison to `seeker` instances with a default `bias_std = 0.1°`:
      

  





  .. code:: 
  
    >>> from c4dynamics.sensors import seeker, radar 
    >>> seekers = []
    >>> radars = []
    >>> for i in range(1000):
    >>> seekers.append(seeker().bias * c4d.r2d)
    >>> radars.append(radar().bias * c4d.r2d)

 
  The histogram highlights the broadening of the distribution 
  as the standard deviation increases:    


    >>> ax = plt.subplot()
    >>> ax.hist(seekers, 30, label = 'Seekers')
    >>> ax.hist(radars, 30, label = 'Radars') 

  .. figure:: /_static/figures/radar/bias2.png

  '''
  
  rng_noise_std = 0 

  def __init__(self, origin = None, isideal = False, **kwargs):

    kwargs['radar'] = True 
    super().__init__(origin = origin, isideal = isideal, **kwargs)
    self.rng_noise_std = kwargs.pop('rng_noise_std', 1)
    self.range = 0

    if isideal: 
      self.rng_noise_std = 0 





  def measure(self, target, t = -1, store = False):
    '''
    Measures range, azimuth and elevation between the radar and a `target`. 


    If the radar time-constant `dt` was provided when the `radar` was created, 
    then `measure` returns `None` for any `t < last_t + dt`, 
    where `t` is the time input, `last_t` is the last measurement time, 
    and `dt` is the radar time-constant. 
    Default behavior, returns measurements for each call.  
    
    If `store = True`, the method stores the measured 
    azimuth and elevation along with a timestamp 
    (`t = -1` by default, if not provided otherwise). 


    Parameters
    ----------
    target : `cartesian_state`
        A state object to measure by the radar, including at least one position coordinate (x, y, z).  
    store : bool, optional
        A flag indicating whether to store the measured values. Defaults `False`.
    t : float, optional
        Timestamp [seconds]. Defaults -1.

    Returns
    -------
    out : tuple
        range [meters, float], azimuth and elevation, [radians, float]. 
    

    Raises 
    ------
    ValueError
        If `target` doesn't include any position coordinate (x, y, z).  

                
    Example
    -------

    `measure` in a program simulating 
    real-time tracking of a constant velcoity target.

    
    The target is represented by a :class:`datapoint <c4dynamics.states.lib.datapoint.datapoint>` 
    and is simulated using the :mod:`eqm <c4dynamics.eqm>` module, 
    which integrating the point-mass equations of motion. 

    An ideal radar uses as reference to the true position of the target. 

    At each cycle, the the radars take measurements and store the samples for 
    later use in plotting the results.  

    
    .. code:: 

      >>> dt = 0.01
      >>> tgt = c4d.datapoint(x = 1000, vx = -80 * c4d.kmh2ms, vy = 10 * c4d.kmh2ms)
      >>> pedestal = c4d.rigidbody(z = 30, theta = -1 * c4d.d2r)
      >>> rdr = c4d.sensors.radar(origin = pedestal, dt = 0.05)
      >>> rdr_ideal = c4d.sensors.radar(origin = pedestal, isideal = True)
      >>> for t in np.arange(0, 60, dt):
      ...   tgt.inteqm(np.zeros(3), dt)
      ...   rdr_ideal.measure(tgt, t = t, store = True)  
      ...   rdr.measure(tgt, t = t, store = True)  
      ...   tgt.store(t)

    Before viewing the results, let's examine the error parameters generated by 
    the errors model (`c4d.r2d` converts radians to degrees): 

    .. code::

      >>> rdr.rng_noise_std
      1
      >>> rdr.bias * c4d.r2d
      -0.025
      >>> rdr.scale_factor
      0.99 
      >>> rdr.noise_std * c4d.r2d
      .8 

    Then we excpect a constant bias of -0.02° and a 'compression' or 'squeeze' of `5%` with 
    respect to the target (as represented by the ideal radar):  
    
    .. code::

      >>> ax = plt.subplots(2, 1)
      >>> # range      
      >>> axs[0].plot(*rdr_ideal.data('range'), '.m', label = 'target')
      >>> axs[0].plot(*rdr.data('range'), '.c', label = 'radar')
      >>> # angles 
      >>> axs[1].plot(*rdr_ideal.data('az', scale = c4d.r2d), '.m', label = 'target')
      >>> axs[1].plot(*rdr.data('az', scale = c4d.r2d), '.c', label = 'radar')
      
    .. figure:: /_static/figures/radar/measure.png

    The sample rate of the radar was set by the parameter `dt = 0.05`. 
    In cycles that don't satisfy `t < last_t + dt`, `measure` returns None, 
    as shown in a close-up view:  

    .. figure:: /_static/figures/radar/measure_zoom.png

    '''

    az, _ = super().measure(target, t = t, store = False)

    if az == None: # elapsed time is not enough 
      return None, None, None 

    self.range = self.P(target) + self.rng_noise_std * np.random.randn()  
    

    if store: 
      self.storeparams(['az', 'el', 'range'], t = t)

    return self.az, self.el, self.range 

    
    

class dzradar:
  ''' 
  altitude radar
  
  Parameters
  ==========
  TODO complete 

  
  an electromagnetic radar 
  meausres target vertical position.
  vk: noise variance  

  TODO change this to be `sensor` namely a general sensor 
  that measure any magnitude following an error model 
  (starting simply with bias sf.). 
  then remove the range measure from the seeker and 
  use this that here. 

  '''
  
  # 
  # state vector
  #   r position (in one dimension range)
  #   v velocity 
  #   b ballistic coefficient 
  ##
  r = 0 # measured range 
  # vx = 0 # velocity 
  
  
  ts = 0 # 50e-3                        # sample time 
  q33 = 0
  data = np.array([[0, 0, 0, 0]])   # time, z target, v target, beta target 
  
  # luenberger gains 
  L = 0
  
  # 
  # seeker errors 
  ##
  bias = 0 # deg
  sf = 1 # scale factor error -10%
  noise = np.sqrt(500 * c4d.ft2m) # 1 sigma 
  # misalignment = 0.01 # deg

  def __init__(obj, x0, filtype, ts):
    '''
      initial estimate: 
      100025 ft    25ft error
      6150 ft/s    150ft/s error
      800 lb/ft^2  300lb/ft^2 
    '''
    obj.ts = ts
    if filtype == c4d.filters.filtertype.ex_kalman:
      obj.ifilter = c4d.filters.kalman(x0
                                           , [obj.noise
                                              , 141.42 * c4d.ft2m
                                              , 300 * c4d.lbft2tokgm2]
                                           , obj.ts)
    elif filtype == c4d.filters.filtertype.luenberger:
      # linear model
      beta0 = x0[2]
      A = np.array([[0, 1, 0], [0, -np.sqrt(2 * 0.0034 * c4d.g_ms2 / beta0)
                                , -c4d.g_ms2 / beta0], [0, 0, 0]])
      b = np.array([0, 0, 0])
      c = np.array([1, 0, 0])
      obj.ifilter = c4d.filters.luenberger(A, b, c)
    elif filtype == c4d.filters.filtertype.lowpass:
      obj.ifilter = c4d.filters.lowpass(.2, obj.ts, x0)
    else:
      print('filter type error')
      
    obj.data[0, :] =  np.insert(x0, 0, 0)  
      
      
  def measure(obj, x):
    # 
    # apply errors
    ##
    obj.r = x * obj.sf + obj.bias + obj.noise * np.random.randn(1) 
  
      
  def filter(obj, t):
    
    # check that t is at time of operation 
    
    
    if (1000 * t) % (1000 * obj.ts) > 1e-6 or t <= 0:
      return
    
    
    # print(t)
    rho = .0034 * np.exp(-obj.ifilter.x[0, 0] / 22000 / c4d.ft2m)
    f21 = -rho * c4d.g_ms2 * obj.ifilter.x[1, 0]**2 / 44000 / obj.ifilter.x[2, 0] 
    f22 =  rho * c4d.g_ms2 * obj.ifilter.x[1, 0] / obj.ifilter.x[2, 0]
    f23 = -rho * c4d.g_ms2 * obj.ifilter.x[1, 0]**2 / 2 / obj.ifilter.x[2, 0]**2 
    
    Phi = np.array([[1, obj.ifilter.dt, 0], 
                    [f21 * obj.ifilter.dt, 1 + f22 * obj.ifilter.dt, f23 * obj.ifilter.dt], 
                    [0, 0, 1]])
    
    Q   = np.array([[0, 0, 0], 
                    [0, obj.q33 * f23**2 * obj.ifilter.dt**3 / 3, obj.q33 * f23 * obj.ifilter.dt**2 / 2], 
                    [0, obj.q33 * f23 * obj.ifilter.dt**2 / 2, obj.q33 * obj.ifilter.dt]])

    f = lambda w: c4d.sensors.dzradar.system_model(w)

    #
    # prepare luenberger matrices
    ##

    ''' predict '''
    obj.ifilter.predict(f, Phi, Q)
    ''' correct '''    
    x = obj.ifilter.update(f, obj.r)  
 
    obj.r = x[0]
    #
    # store results 
    ##
 
    # obj.data = np.concatenate((obj.data, np.expand_dims(np.insert(x, 0, t), axis = 0)), axis = 0)  
    obj.data = np.vstack((obj.data, np.insert(x, 0, t))).copy()
    
    return obj.r

    

  @staticmethod
  def system_model(x):
    dx = np.zeros((len(x), 1))
    dx[0, 0] = x[1, 0]
    dx[1, 0] = .0034 * np.exp(-x[0, 0].astype('float') / 22000 / c4d.ft2m) * c4d.g_ms2 * x[1, 0]**2 / 2 / x[2, 0] - c4d.g_ms2
    dx[2, 0] = 0
    return dx

