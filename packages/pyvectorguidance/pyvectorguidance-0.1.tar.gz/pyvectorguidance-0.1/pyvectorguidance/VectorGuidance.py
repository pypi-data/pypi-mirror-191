import numpy as np
from scipy.spatial.transform import Rotation as R

'''
Vector Guidance methods for interception and soft landing scenario.
author: Iftach Naftaly, 2.2023, iftahnaf@gmail.com
'''

class VectorGuidance():

    def __init__(self):
        pass

    def interception_controller_bounded(self, r, v, rho_u, tgo, gz):
        u = rho_u * (r + tgo*v)/(np.linalg.norm(r + tgo*v)) + np.array([0, 0, gz])
        return u

    def interception_tgo_bounded(self, r, v, vm, k, rho_u, min_tgo=0.01):
        drho = rho_u - k*np.linalg.norm(vm)**2
        f = [(drho**2)/4 , 0, -np.linalg.norm(v)**2, -2*np.dot(np.transpose(r), v), -np.linalg.norm(r)**2]
        roots = np.roots(f)
        real_sol = np.real(roots)[abs(np.imag(roots)) < 1e-5]
        real_sol = np.real(real_sol)[np.real(real_sol) > 0]
        if len(real_sol) > 1:
            tgo = np.min(real_sol)
        elif len(real_sol) == 0:
            tgo = min_tgo
        else:
            tgo = real_sol
        return tgo

    def interception_controller_lq(self):
        pass

    def interception_tgo_lq(self):
        pass

    def soft_landing_controller_lq(self):
        pass

    def soft_landing_tgo_lq(self):
        pass
    
class Utilities():

    def __init__(self):
        pass

    def acceleration_to_quaternion(self, u, yaw=0):
        projected_xb_des = np.array([np.cos(yaw), np.sin(yaw), 0])
        zb_des = u / np.linalg.norm(u)
        yb_des = np.cross(zb_des, projected_xb_des) / np.linalg.norm(np.cross(zb_des, projected_xb_des))
        xb_des = np.cross(yb_des, zb_des) / np.linalg.norm(np.cross(yb_des, zb_des))

        rotm = np.array([xb_des[0], yb_des[0], zb_des[0]],
                        [xb_des[1], yb_des[1], zb_des[1]],
                        [xb_des[2], yb_des[2], zb_des[2]])
        
        q = R.from_matrix(rotm).as_quat()
        return q

        