import os
import yaml
from pyrateshield import labels
from pyrateshield.modelitem import ModelItem



CONSTANTS_FILE = "constants.yml"
ISOTOPES_FILE = "isotopes.yml"

class Isotope(ModelItem):
    _attr_dct = {
        "name": labels.NAME,
        "half_life": labels.HALF_LIFE,
        "self_shielding_options": labels.SELF_SHIELDING_OPTIONS,
    }
    spectrum = None
    
    def __eq__(self, other):
        return self.name == other.name
    
    def mass_number(self):
        mass_number = self.name.split('-')[1]
        try:
            mass_number = int(mass_number)
        except ValueError:
            # Cut off the m for Tc-99m
            mass_number = int(mass_number[:-1])
        return mass_number
    
    def __gt__(self, other):
        return self.mass_number() > other.mass_number()
    
    def __lt__(self, other):
        return self.mass_number() < other.mass_number()
    
    def __ge__(self, other):
        return self.mass_number() >= other.mass_number()
    
    def __le__(self, other):
        return self.mass_number() <= other.mass_number()
        

class ArcherParamsCT(ModelItem):
    _attr_dct = {
        "kvp": labels.KVP,
        "archer": labels.ARCHER,
        "scatter_fraction_body": labels.CT_SCATTER_FRACTION_BODY,
        "scatter_fraction_head": labels.CT_SCATTER_FRACTION_HEAD,
    }

class ArcherParamsXray(ModelItem):
    _attr_dct = {
        "kvp": labels.KVP,
        "archer": labels.ARCHER,
        "scatter_fraction": labels.XRAY_SCATTER_FRACTION,
    }



class Constants:
    def __init__(self):
        try:
            wdir = os.path.split(__file__)[0] 
        except:
            wdir = os.getcwd()
            
        with open(os.path.join(wdir, CONSTANTS_FILE)) as f:
            constants_yml = yaml.safe_load(f)
            
        with open(os.path.join(wdir, ISOTOPES_FILE)) as f:
            isotope_yml = (yaml.safe_load(f))            
        
        supported_isotopes = isotope_yml[labels.SUPPORTED_ISOTOPES]
        self.radtracer_supported_isotopes = supported_isotopes[labels.RADTRACER]
        self.pyshield_supported_isotopes = supported_isotopes[labels.PYSHIELD]
        
            
        isotopes = [Isotope.from_dict(item)\
                    for item in isotope_yml[labels.ISOTOPES]]
            
        # sort isotopes by mass number
        self.isotopes = sorted(isotopes)
        
        decay_chains = isotope_yml[labels.DECAY_CHAINS]
        self.decay_chains = decay_chains
        isotope_spectra = isotope_yml[labels.ISOTOPE_SPECTRA]
        for isotope in self.isotopes:
            spectrum = list(isotope_spectra[isotope.name])
            spectrum_with_parent = [(isotope.name, energy, intensity)\
                                    for energy, intensity in spectrum]
            for daughter, abundance in decay_chains.get(isotope.name, []):
                for energy, intensity in isotope_spectra[daughter]:
                    spectrum.append([energy, intensity*abundance])
                    spectrum_with_parent.append([daughter, energy, intensity*abundance])
            isotope.spectrum = spectrum
            isotope.spectrum_with_parent = spectrum_with_parent
            
        self.ct = [ArcherParamsCT.from_dict(item)\
                   for item in constants_yml[labels.CT_PARAMETERS]]
            
        self.xray = [ArcherParamsXray.from_dict(item)\
                     for item in constants_yml[labels.XRAY_PARAMETERS]]
        
        self.CT_body_part_options = constants_yml[labels.CT_BODY_PART_OPTIONS]
        
        self.self_shielding_pyshield = constants_yml[labels.SELF_SHIELDING_PYSHIELD]
    
        self.self_shielding_options = [labels.SELF_SHIELDING_NONE,
                                       labels.SELF_SHIELDING_BODY, 
                                       labels.SELF_SHIELDING_FACTOR]
        
        self.base_materials = [labels.EMPTY_TABLE] + constants_yml[labels.BASE_MATERIALS]
        self.buildup_materials = [labels.EMPTY_TABLE] + constants_yml[labels.BUILDUP_MATERIALS]
    
    
    def get_isotope_name_list(self):
        return [item.name for item in self.isotopes]
        

    def get_isotope_by_name(self, name):
       
       isotope = [x for x in self.isotopes if x.name == name]
       if len(isotope) == 0:
           raise KeyError(f'No isotope with name {name}')
       return isotope[0]
    
  
    
CONSTANTS = Constants()
