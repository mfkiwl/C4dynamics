import numpy as np
# import c4dynamics as c4d 
from c4dynamics.states.state import state 

# from enum import Enum


class pixelpoint(state):
  ''' 
  A data point in a video frame with a bounding box. 

  :class:`pixelpoint` is a data structure for managing 
  object detections in tracking missions. 
  It provides properties and methods to 
  conveniently interact with computer vision modules. 

  The `pixelpoint` state variables are 
  the object center and the bounding box: 
  
  .. math:: 

    X = [x, y, w, h]^T 

  - Center pixel, bounding box size. 



  
  **Arguments** 

  x : float or int 
      The x-coordinate of the center of the object.

  y : float or int 
      The y-coordinate of the center of the object.

  w : float or int
      The width of the bounding box.
  
  h : float or int
      The height of the bounding box.
  

  These variables use for streamlined operations through 
  the state vector :attr:`X <c4dynamics.states.state.state.X>`.

  Parameters define the object and are not part of the state. 
  For the `pixelpoint` class these are the frame size and the object classification. 


  Parameters
  ==========

  fsize : (int, int)
      Frame size in pixels. 

  class_id : str
      Class label associated with the object.

  Example 
  =======

  A `pixelpoint` instance is typically created 
  when a new object is detected.  

  For a given detection `d` with the following indices: 

  - [0] : x-center
  - [1] : y-center
  - [2] : width
  - [3] : height
  - [4:end] : probabilities for each class of the list `class_names` 
  
  and for frames with dimensions `(f_width, f_height)`, the following snippet 
  constructs a `pixelpoint` and updates its properties. 
  
  .. code:: 

    >>> pp = pixelpoint(x = d[0], y = d[1], w = d[2], h = d[3])
    >>> pp.fsize = (f_width, f_height)
    >>> pp.class_id = class_names[numpy.argmax(d[4:])]

      
  See Also
  ========
  .lib
  .state 

  


  '''  
  # framepoint/ imagepoint
  # pixeldata/ pixelbox/ imagebox

  # 
  # NOTE override the .X property: will distance the devs from a datapoint class. 
  #     con: much easier 

  # __slots__ = ['_boxwidth', '_boxheight', '_framewidth', '_frameheight'] 

  # ppunits = ('pixels', 'normalized')

  def __init__(self, x = 0, y = 0, w = 0, h = 0):
  # def __init__(self, bbox, class_id, framesize):
      
 
    ppargs = {}
    ppargs.setdefault('x', x) 
    ppargs.setdefault('y', y) 
    ppargs.setdefault('w', w) 
    ppargs.setdefault('h', h) 
     

    # super().__init__(x = bbox[0], y = bbox[1], w = bbox[2], h = bbox[3])
    super().__init__(**ppargs)
    # NOTE what's the ultimate state? with velocities or not? 
    #       they can be added later. 
    # but if in anyway they are added, why not to introduce them here?
    #       

    # self._units = 'pixels'


    # NOTE still not sure whats the best idea to init of these properties: 
    # on the one hand they are not part of he state and shoudlnt be provdied as variables
    # on the other they are necessary for methods like box. 
    # also the filters inherit from the state class i.e. they are states 
    # nontheless they are initialized not only with the state vairables but also with parameters. 
    self._frameheight = None
    self._framewidth = None
    self._class = None 

    # - x (float): X-coordinate of the center of the bounding box in relative coordinates.
    # - y (float): Y-coordinate of the center of the bounding box in relative coordinates.


    # self._boxwidth = bbox[2]
    # ''' float; Width of the bounding box in a normalized format 
    # (0 = left image edge, 1 = right image edge. '''

    # self._boxheight = bbox[3]
    # ''' float; Height of the bounding box in a normalized format
    # (0 = upper image edge, 1 = bottom image edge. '''


    # self._framewidth = framesize[0]
    # ''' int; Width of the frame in pixels. '''

    # self._frameheight = framesize[1]
    # ''' int; Height of the frame in pixels. '''


    # self.class_id = class_id 
    # ''' string; Class label associated with the data point. '''
    


  @property
  def X(self): 
    return super().X.astype(np.int64)
  

  # parameters 

  @property
  def fsize(self):
    '''
    Gets and sets the frame size. 

    Parameters
    ----------
    fsize : tuple 
        Size of the frame in pixels (width, height).
        - (width)  int : Frame width in pixels. 
        - (height) int : Frame height in pixels. 


    Returns
    -------
    out : tuple 
        A tuple of the frame size in pixels (width, height). 
        

    Raises
    ------
    ValueError
        If `fsize` doesn't have exactly two elements, a ValueError is raised.

        
    .. include:: ../../states.lib.pixelpoint.examples.rst
        
    '''
    return (self._framewidth, self._frameheight)

  @fsize.setter
  def fsize(self, fsize):
    if len(fsize) != 2:
      raise ValueError('fsize must have exactly two elements.')

    self._framewidth  = fsize[0]
    self._frameheight = fsize[1]
    
  
  @property  
  def class_id(self):
    '''
    Gets and sets the object classification. 

    
    Parameters
    ----------
    class_id : str 
        Class label associated with the data point.

        
    Returns 
    -------
    out : str 
        The current class label associated with the data point.


    Raises
    ------
    ValueError
        If `class_id` is not str, a ValueError is raised.
   
    
    .. include:: ../../states.lib.pixelpoint.examples.rst

    ''' 
    return self._class 

  @class_id.setter 
  def class_id(self, class_id):
    if not isinstance(class_id, str):
      raise TypeError('class_id must be an str object')

    self._class = class_id 
  


  # properties 

  @property
  def box(self):
    '''
    Returns the box coordinates.
     
    The box coordinates are given by: 
    `[(x top left, y top left), (x bottom right, y bottom right)]` 

    Returns
    -------
    out : list[tuple] 
        List containing two tuples representing 
        top-left and bottom-right coordinates (in pixels).
  
    
    .. include:: ../../states.lib.pixelpoint.examples.rst
        
    ''' 
    # if self._units == 'normalized':
    #   if self._frameheight is None or self._framewidth is None: 
    #     raise ValueError('When ''pixelpoint'' units are ''normalized'', the property ''fsize'' '
    #                         'must be set first with the frame width and height.')

    #   x = int(self.x * self._framewidth)
    #   y = int(self.y * self._frameheight)

    #   w = self.w * self._framewidth
    #   h = self.h * self._frameheight

    # else: # units = pixels. 

    x = self.x
    y = self.y

    w = self.w  
    h = self.h      


    # top left
    xtl = x - int(w / 2)
    ytl = y - int(h / 2)

    # bottom right 
    xbr = x + int(w / 2)
    ybr = y + int(h / 2)

    return [(xtl, ytl), (xbr, ybr)]









  @property
  def Xpixels(self):
    '''
    Returns the state vector in pixel coordinates.  

    When pixelpoint.units are set to `normalized`, the method `Xpixels` 
    is used to return the state vector in pixels. 

    Returns
    -------
    out : numpy.int32
      A numpy array of the normalized coordinates :math:`[x, y, v_x, v_y]` transformed
      to pixel coordinates considering the specific dimensions of the image. 
         
        
    Examples
    --------

    .. code:: 

      >>> imagename = 'planes.jpg'
      >>> imgpath = os.path.join(os.getcwd(), 'examples', 'resources', imagename)
      >>> img = cv2.imread(imgpath)
      >>> yolo3 = c4d.detectors.yolov3()
      >>> pts = yolo3.detect(img)
      >>> print('{:^10} | {:^12} | {:^12} | {:^12} | {:^12}'.format(
      ...     '# object', 'X normalized', 'Y normalized', 'X pixels', 'Y pixels'))
      >>> for i, p in enumerate(pts):
      ...     X = p.Xpixels
      ...     print('{:^10d} | {:^12.3f} | {:^12.3f} | {:^12d} | {:^12d}'.format(
      ...            i, p.x, p.y, X[0], X[1]))
      # object | X normalized | Y normalized |   X pixels   |   Y pixels  
        0      |    0.427     |    0.339     |     503      |     232     
        1      |    0.411     |    0.491     |     484      |     336     
        2      |    0.550     |    0.397     |     648      |     272     
        3      |    0.507     |    0.916     |     598      |     627     

    '''
    # TODO complete with full state vector. 

    # superx = super().X
    return np.array([self.x * self._framewidth        # x
                      , self.y * self._frameheight      # y
                        , self.w * self._framewidth       # w
                          , self.h * self._frameheight]      # h   
                            , dtype = np.int32)
  

  
  @staticmethod
  def boxcenter(box):
    # XXX seems like useless function and indeed is not in use anywhere. 
    '''
    
    Calculates the center coordinates of bounding boxes.

    Given a list of bounding boxes, this static method computes the center
    coordinates for each box.



    Parameters
    ----------
    out : list[box] 
      List containing one pixelpoint.box or more. where  
      every pixelpoint.box has two tuples 
      representing top-left and bottom-right coordinates.

    Returns
    -------
    out : numpy.ndarray
        An array containing center coordinates for each bounding box in the
        format [[center_x1, center_y1], [center_x2, center_y2], ...].

    '''

    return np.array([[(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] for b in box]) 





  # def set_box_size(self, width, height):
  #   # TODO document! 
  #   '''
  #   Sets the box size (box width, box height) 
  #   without changing the center. 


  #   Parameters
  #   ----------
  #   b : tuple(width, height)
  #     A tuple containing two integers representing width and height (in pixels).

      
  #   Note
  #   ----
  #   This function sets the box width and height without
  #   chaning the box center. 
  #   The center of the box is modified only by 
  #   direct substitution to the state variables 
  #   or by setting the state vector (:attr:`X <datapoint.X>`). 

      
        
  #   Examples
  #   --------

  #   .. code:: 

  #       >>> width  = 800
  #       >>> height = 600
  #       >>> radius = 50
  #       >>> img = np.zeros((height, width, 3), dtype = np.uint8)
  #       >>> cv2.circle(img, (width // 2, height // 2), radius, (255, 0, 0), -1)
  #       >>> fdp = c4d.pixelpoint(bbox = (0, 0, 0, 0), class_id = 'ball', framesize = (width, height))
  #       >>> fdp.x = 0.5 
  #       >>> fdp.y = 0.5 
  #       >>> fdp.set_box_size(2 * radius + 2, 2 * radius + 2)
  #       >>> cv2.rectangle(img, fdp.box[0], fdp.box[1], [255, 255, 255], 2)
  #       >>> _, ax3 = plt.subplots()
  #       >>> ax3.axis('off')
  #       >>> ax3.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

  #   .. figure:: /_static/images/fdp_setboxsize.png
    


  #   '''

  #   # self._boxwidth  = width  / self._framewidth
  #   # self._boxheight = height / self._frameheight










  # class ppunits(Enum):
  #   pixels = 'pixels'
  #   normalized = 'normalized'


  # @property  
  # def units(self):
  #   '''
  #   Gets and sets the image coordinates units. 

  #   Select between two modes of units: 
  #   - pixels (default): the image coordinates range between `[0 : width - 1]` horizontally and `[0 : height - 1]` vertically. 
  #   - normalized: the image coordinates range between `[0 : 1]` in both axes where `0` represents the top and the left edges and `1` the opposite.  

  #   Note 
  #   ---- 
  #   Setting `units` as 'normalized' must be preceded by setting the frame size by the `fsize` property.


  #   Parameters
  #   ----------
  #   units : str
  #       Required units. 
  #       - 'pixels' (default) : image coordinates are `[0 : width - 1]` in the horizontal plane and `[0 : height - 1]` vertical plane.
  #       - 'normalized' : coordinates are `[0 : 1]` in the horizontal plane and `[0 : 1]` vertical plane. `0` represents the top and the left edges. 

  #   Returns
  #   -------
  #   out : str
  #       Current coordinates units. 


  #   Raises
  #   ------
  #   ValueError
  #       - If `units` is not in 'pixels' or 'normalized', a ValueError is raised.
  #       - If `units` is 'normalized' and the `fsize` property is not set, a ValueError is raised.
            
  #   Example
  #   -------    
    
  #   '''
  #   return self._units 

  # @units.setter 
  # def units(self, units):
  #   if not units in pixelpoint.ppunits:
  #     raise ValueError(f'Invalid units. Choose from {[value for option in pixelpoint.ppunits]}')
  #   if units == 'normalized' and self.fsize is None: 
  #     raise ValueError(f'`fsize` property must be set before `units = ''normalized''` is selected')
    
  #   # if self._units == 'normalized' and (self._frameheight is None or self._framewidth is None): 
  #   #   raise ValueError('When pixelpoint units are ''normalized'', the property ''fsize'' '
  #   #                         'must be set first with the frame width and height.')

  #   #
  #   # currently leaving it because it's too complicated to track after the updates
  #   # of the state and verify it's normalized. it probably invloves overriding X which 
  #   # i dont want to do right now.  
  #   ## 
    
  #   self._units = units 
  
  
  # Note
  # ----
  # The pixelpoint has two modes to represent the state coordinates 
  # (:attr:`X <c4dynamics.states.state.state.X>`); pixels (default) and normalized, 
  # controlled by the property 
  # (:attr:`units <c4dynamics.states.lib.pixelpoint.pixelpoint.units>`). 
  # In the `pixels` mode, the coordinates are directly represented by the pixel dimensions. 
  # The `normalized` mode represents the image by normalized coordinates, 
  # ranging from `0` to `1`, where `0` represents 
  # the left or the upper edge, and `1` represents the right or the bottom edge. 

