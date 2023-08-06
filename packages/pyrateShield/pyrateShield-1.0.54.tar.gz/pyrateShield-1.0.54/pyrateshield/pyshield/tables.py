import os
import pandas as pd


#ENERGY_keV = 'Energy [keV]'
MFP = 'mfp'
MASS_ATTENUATION = 'mu/p [cm^2/g]'
ENERGY_MeV = 'Energy [MeV]'

folder = os.path.dirname(__file__)

file = os.path.join(folder, 'buildup.xls')
BUILDUP_TABLES = pd.read_excel(os.path.join(folder, file), sheet_name=None)

file = os.path.join(folder, 'attenuation.xls')
ATTENUATION_TABLES = pd.read_excel(os.path.join(folder, file), sheet_name=None)





  