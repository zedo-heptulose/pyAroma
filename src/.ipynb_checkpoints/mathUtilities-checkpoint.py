import numpy as np

def align_matrix(_v1, _v2, **kwargs):
    '''
    given vectors v1 and v2,
    produces a rotation matrix that will align 
    v2 to v1.
    '''
    debug = kwargs.get('debug', False)
    
    v1 = _v1 / np.linalg.norm(_v1)
    v2 = _v2 / np.linalg.norm(_v2)
    
    if np.allclose(v1,v2,atol=1e-2):
        if debug:
            print('vectors are the same')
            
        return np.eye(3)
    if np.allclose(v1,-v2,atol=1e-2):
        if debug:
            print('vectors are antiparallel')
    
        z_axis = np.array([0,0,1])
        y_axis = np.array([0,1,0])
        rot_ax = np.cross(v1, z_axis)
        if np.allclose(rot_ax, np.array([0,0,0])):
            rot_ax = np.cross(v1, y_axis)
            if np.allclose(rot_ax, np.array([0,0,0])):
                raise ValueError("bad vector?")
        return rotation_about_axis(rot_ax, np.pi)
    
    if debug:   
        print('arbitrary angle')
    
    axis = kwargs.get('axis', None)
    if axis is None:
        axis = np.cross(v1, v2)
        
    if debug:
        tuple1 = ('v1', v1)
        tuple2 = ('v2', v2)
        tuple3 = ('axis', axis)
        
    
    angle_between = angle_about_axis(v1, v2, axis)
    
    par_angle = - angle_between
    
    par_matrix = rotation_about_axis(axis, par_angle)
    
    return par_matrix



def angle_about_axis(_v1, _v2, _axis, **kwargs):
    '''
    accepts:
    v1, v2, axis: numpy arrays
    returns:
    angle: float
    '''
    debug = kwargs.get('debug', False)
    
    v1 = _v1 / np.linalg.norm(_v1)
    v2 = _v2 / np.linalg.norm(_v2)
    axis = _axis / np.linalg.norm(_axis)
    
    if np.allclose(v1, v2,atol=1e-2):
        return 0
    if np.allclose(v1, -v2,atol=1e-2):
        return np.pi
    
    dot = np.dot(v1, v2)
    cross = np.cross(v1, v2)
    c_n = cross / np.linalg.norm(cross)
    
    if debug:
        debug_print_vectors(('v1', v1), ('v2', v2), ('axis', axis), ('cross', cross), ('c_n', c_n))
    
    if np.allclose(c_n, axis,atol = 1e-1):
        return np.arccos(dot)
    elif np.allclose(c_n, -axis,atol = 1e-1):
        return 2*np.pi - np.arccos(dot)
    else:
        raise ValueError('Axis not parallel to cross product of v1 and v2')



def rotation_about_axis(_axis, angle):
    """    
    Calculate the rotation matrix from axis and angle using Rodrigues' rotation formula.

    Args:
    axis: The rotation axis as a numpy array.
    angle: The rotation angle in radians.

    Returns:
    The rotation matrix.
    """
    # chatGPT code, this whole function. look here if something goes wrong (hasn't yet!)
    # very minor numerical instabilities but nothing that should meaningfully affect results
    
    axis = _axis.copy()
    if np.allclose(axis, np.array([0,0,0])):
        raise ValueError("zero vector forbidden")
    
    axis /= np.linalg.norm(axis)
    
    axis = np.asarray(axis)
    axis = axis / np.linalg.norm(axis)  # Normalize the axis vector
    
    # Rodrigues' rotation formula
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    cross_matrix = np.array([[0, -axis[2], axis[1]],
                             [axis[2], 0, -axis[0]],
                             [-axis[1], axis[0], 0]])
    rotation_matrix = np.eye(3) * cos_theta + sin_theta * cross_matrix + (1 - cos_theta) * np.outer(axis, axis)
    
    return rotation_matrix