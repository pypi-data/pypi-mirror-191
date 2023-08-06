# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""
import numpy as np
import scipy.interpolate as si
from pyrateshield.pyshield import tables

         

DEBUG = False



make_list = lambda item: item if isinstance(item, (list, tuple)) else [item]

    


def attenuation(energy_keV, material, thickness):
    """
    Attenuation for a given energy through a matrial with thickness.
    Args:
        energy_keV: the energy of  the photon in keV
        material: name of the material
        thickness: thickness of the material
    Returns:
        a:  attenation factor (float)
    """
    thickness = np.asarray(thickness)
    
    a = np.exp(-u_linear(energy_keV, material) * thickness)

    return a


def u_linear(energy_keV, material):
    """
    Args:
      energy_keV: the energy of  the photon in keV
      material: name of the material
    Returns:
      Linear attenuation coefficient in [cm^-1]
    Raises:
      NameError if material is not defined in the pyshield recources
    """

    mu_p_i = u_mass(energy_keV, material)

    return mu_p_i * material.density

def u_mass(energy_keV, material):
    try:
        table = tables.ATTENUATION_TABLES[material.attenuation_table]
    except NameError:
        raise NameError(material.attenuation_table + ' not in attenuation table!')

    energies = np.array(table[tables.ENERGY_MeV])

    mu_p = np.array(table[tables.MASS_ATTENUATION])

    interp_fcn = si.interp1d(energies, mu_p)
    mu_p_i = interp_fcn(energy_keV / 1e3)

    return mu_p_i

def interp2d_pairs(*args,**kwargs):
    # https://stackoverflow.com/questions/47087109/evaluate-the-output-from-scipy-2d-interpolation-along-a-curve
    """ Same interface as interp2d but the returned interpolant will evaluate its inputs as pairs of values.
    """
    # Internal function, that evaluates pairs of values, output has the same shape as input
    def interpolant(x,y,f):
        x,y = np.asarray(x), np.asarray(y)
        return (si.dfitpack.bispeu(f.tck[0], f.tck[1], f.tck[2], f.tck[3], f.tck[4], x.ravel(), y.ravel())[0]).reshape(x.shape)
    # Wrapping the scipy interp2 function to call out interpolant instead
    return lambda x,y: interpolant(x,y,si.interp2d(*args,**kwargs))

    # # Create the interpolant (same interface as interp2d)
    # f = interp2d_pairs(X,Y,Z,kind='cubic')
    # # Evaluate the interpolant on each pairs of x and y values
    # z=f(x,y)

# def buildup(energy_keV, material, thickness):
#     """
#     Buildup for a given energy through a matrial with thickness.
#     Args:
#         energy_keV: the energy of  the photon in keV
#         material: name of the material
#         thickness: thickness of the material
#     Returns:
#         b:  buildup factor (float)
#     """
#     # if thickness == 0:
#     #     return 1
    
    
#     if isinstance(thickness, (float, int)) or thickness.ndim == 0:
#         thickness = [float(thickness)]
    
#     thickness = np.asarray(thickness)
    
#     index = thickness > 0

#     return BuildupHelper.calculate(material, energy_keV, thickness)
#     try:
#         table = PHYSICS[BUILDUP][material.buildup_table]
#     except NameError:
#         raise NameError(material.name + ' not in buildup table!')
    
#     n_mfp       = np.asarray(tables.BUILDUP_TABLES[tables.MFP], 'float64')
#     table       = table.drop(tables.MFP, axis=1)
    
#     factors     = np.asarray(table, 'float64')
#     energies    = np.asarray(table.columns, dtype='float64')
    
#     n_mfpi      = number_mean_free_path(energy_keV, 
#                                       material, 
#                                       thickness[index])

#     interp_func2d = interp2d(energies, n_mfp, factors)
#     interp_func1d = lambda ii: interp_func2d(energy_keV/1000, ii)
    
#     n_mfpi    = number_mean_free_path(energy_keV, material.name, 
#                                       thickness[index])#[index])
    
#     buildup_values = np.asarray([float(interp_func1d(ii)) for ii in n_mfpi])
    
#     buildup = np.ones(len(thickness))
#     buildup[index] = buildup_values.flatten()

#     return buildup


def number_mean_free_path(energy_keV, material, thickness):
    """"
    Args:
      energy_keV: the energy of  the photon in keV
      material: name of the material
      thickness: thickness of the material
    Retuns:
      number of mean free paths for a given photon enery, material and
      material thicknesss
    """
    
    # 1 mean free path = 1 / u_lin
    

    return thickness * u_linear(energy_keV, material)




class BuildupHelper:
    _interpolators = None

    
    @staticmethod
    def interpolant(x,y,f):
        # https://stackoverflow.com/questions/47087109/evaluate-the-output-from-scipy-2d-interpolation-along-a-curve
        """ Same interface as interp2d but the returned interpolant will evaluate its inputs as pairs of values.
        """
        x,y = np.asarray(x), np.asarray(y)
        return (si.dfitpack.bispeu(f.tck[0], f.tck[1], f.tck[2], f.tck[3], f.tck[4], x.ravel(), y.ravel())[0]).reshape(x.shape)
        # Wrapping the scipy interp2 function to call out interpolant instead
        #return lambda x,y: interpolant(x,y,si.interp2d(*args,**kwargs))

    @classmethod
    def _get_interpolator(cls, material):
        if cls._interpolators is None:
            cls._interpolators = {}
        
        if material.buildup_table not in cls._interpolators.keys():
            table       = tables.BUILDUP_TABLES[material.buildup_table]
            n_mfp       = np.asarray(table[tables.MFP], 'float64')
            table       = table.drop(tables.MFP, axis=1)
            factors     = np.asarray(table, 'float64')
            energies    = np.asarray(table.columns, dtype='float64')
            interpolator = si.interp2d(energies, n_mfp, factors)
            interp_fcn = lambda x, y: cls.interpolant(x, y, interpolator)
            cls._interpolators[material.buildup_table] = interp_fcn
        return cls._interpolators[material.buildup_table]
    
    @classmethod
    def calculate(cls, material, energy_keV,  thickness):
        # 2DO cutoff at lowest mean free path instead of 0
        interpolator = cls._get_interpolator(material)
        
        if isinstance(thickness, np.ndarray):
            index = thickness > 0
            thickness = thickness[index]
        else:
            index = None
        
        n_mfpi = number_mean_free_path(energy_keV, material, thickness)
        
        if not isinstance(energy_keV, np.ndarray) and index is not None:
            energy_keV = np.ones(len(n_mfpi)) * energy_keV
        
    
        values = interpolator(energy_keV/1000, n_mfpi)
        
        if index is not None:
            buildup = np.ones(len(index))
             
            buildup[index] = values.flatten()
        else:
            buildup = values
        return buildup
 


if __name__ == "__main__":
    isotope = 'F-18'
    
    a = attenuation(511, 'Water', 25)
    b = buildup(511, 'Water', 25)










