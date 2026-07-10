import sys
import git
import pathlib

# Set up the PROJ_ROOT variable
PROJ_ROOT_PATH = pathlib.Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
PROJ_ROOT =  str(PROJ_ROOT_PATH)
if PROJ_ROOT not in sys.path:
    sys.path.append(PROJ_ROOT)
#####################################################

import numpy as np
from scipy.integrate import quad
import math


from library.fridges import TEMP_STAGES, FRIDGE_LIBRARY


def cu_thermal_conductivity(T):
    # conductivity, k
    # https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm

    # Units = W/m.K
    # Assuming RRR = 50
    a = 1.8743
    b = -0.41538
    c = -0.6018
    d = 0.13294
    e = 0.26426
    f = -0.0219
    g = -0.051276	
    h = 0.0014871	
    i = 0.003723
    
    # Assuming RRR = 100
    # a = 2.2154
    # b = -0.47461
    # c = -0.88068
    # d = 0.13871	
    # e = 0.29505
    # f = -0.02043
    # g = -0.04831
    # h = 0.001281
    # i = 0.003207

    k = 10**((a + c*T**0.5 + e*T + g*T**1.5 + i*T**2) / (1 + b*T**0.5 + d*T + f*T**1.5 + h*T**2))
    
    return k # W per m-Kelvin 
#####################################################

def fiber_thermal_conductivity(T):
    # Silica Fiber Thermal Conductivity
    # Based on data from 
    # Smith, Terry Lee, P. J. Anthony, and A. C. Anderson. "Effect of neutron irradiation on the density of low-energy excitations in vitreous silica." Physical Review B 17.12 (1978): 4997.
    t_data = np.array([0.1, 1.0, 4, 50, 100, 400])
    g_data = np.array([3E-6, 1.5E-4, 1E-3, 3E-3, 5E-3, 2E-2])* 1E2 # W per cm-Kelvin * 1E2 ->  W per m-Kelvin
    
    log_t_data = np.log10(t_data)
    log_g_data = np.log10(g_data)

    coefficients = np.polyfit(log_t_data, log_g_data, 3)

    log_T = np.log10(T)
    log_y_pred = np.polyval(coefficients, log_T)
    return 10**log_y_pred # W per m-Kelvin 
#####################################################

def mn_thermal_conductivity(T):
    # Manganin Thermal Conductivity
    # Based on data from 
    # https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-accessories/cryogenic-wire
    ## Manganin - # 83-Cu, 13-Mn, 4-Ni
    x_temp = np.array([0.1, 0.4, 1, 4, 10, 20, 80, 150, 300])
    y_k = np.array([0.006, 0.02, 0.06, 0.5, 2, 3.3, 13, 16, 22])

    # Perform cubic fit
    coefficients = np.polyfit(x_temp, y_k, 3)

    return np.polyval(coefficients, T) # W per m-Kelvin 
#####################################################

def infer_thermal_conductivity(PHL_dict, default_lengths, default_temps):
    thermal_conductivity = {} # W-cm/K
    for temp_stage, PHL in PHL_dict.items():
        if temp_stage == '2K':
            thermal_conductivity[temp_stage] = None
            continue
        # conductive heat load is INVERSELY proportional to length
        # conductive heat load is DIRECTLY proportional to temperature difference
        # conductivity in Watt.cm/K (assuming cross sectional area is fixed)
        if PHL is not None:
            # get the temperature values for current and previous stage
            current_temp_stage_idx = TEMP_STAGES.index(temp_stage)
            if current_temp_stage_idx > 0:
                prev_temp_stage = TEMP_STAGES[current_temp_stage_idx - 1]
    
            T_lo = default_temps[temp_stage]
            T_hi = default_temps[prev_temp_stage]
            thermal_conductivity[temp_stage] = PHL_dict[temp_stage] * default_lengths[temp_stage] / (T_hi - T_lo)
        else:
            thermal_conductivity[temp_stage] = None
    return thermal_conductivity
#####################################################

class SS_Drive():
    def __init__(self, name):
        self.name = name
        self.PHL_dict ={  #[2019krinnerEngineeringCryogenicSetups]
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 45E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 1E-3,  # (W/channel); from 50K plate to 4K plate
            'Still': 4E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 0.4E-6,   # (W/channel); from Still plate to CP plate
            'MXC'  : 13E-9 # (W/channel); from CP plate to MXC plate
                        }
        self.default_lengths = FRIDGE_LIBRARY["XLD400"]["lengths"]  #[2019krinnerEngineeringCryogenicSetups]

        self.default_temps = FRIDGE_LIBRARY["XLD400"]["temp"] #[2019krinnerEngineeringCryogenicSetups]

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)
       
      
    
    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class SS_Flux():
    def __init__(self, name):
        self.name = name
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 56E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 1.2E-3,  # (W/channel); from 50K plate to 4K plate
            'Still': 2E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 0.3E-6,   # (W/channel); from Still plate to CP plate
            'MXC'  : 29E-9 # (W/channel); from CP plate to MXC plate
            }

        self.default_lengths = FRIDGE_LIBRARY["XLD400"]["lengths"]  #[2019krinnerEngineeringCryogenicSetups]

        self.default_temps = FRIDGE_LIBRARY["XLD400"]["temp"] #[2019krinnerEngineeringCryogenicSetups]

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)
   
    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class GHOST():
    def __init__(self, name):
        self.name = name
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : None,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }
    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        return None
#####################################################

class NbTi_coax():
    def __init__(self, name):
        self.name = name
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : None,  # (W/channel); from 50K plate to 4K plate
            'Still': 1E-6,  # Fig.1 [2019krinnerEngineeringCryogenicSetups]
            'CP'   : 180E-9,   # (W/channel); from Still plate to CP plate
            'MXC'  : 2E-9 # (W/channel); from CP plate to MXC plate
            }

        self.default_lengths = FRIDGE_LIBRARY["XLD400"]["lengths"]  #[2019krinnerEngineeringCryogenicSetups]

        self.default_temps = FRIDGE_LIBRARY["XLD400"]["temp"] #[2019krinnerEngineeringCryogenicSetups]

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)
    
    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class Cu_35_bias():
    def __init__(self, name):
        ####### 2019krinnerEngineeringCryogenicSetups - Fig 1 ##########
        # Values are for TWP i.e., two strands of cables
        # AWG35
        PHL_twp_cu_4K = 1E-3
        PHL_twp_cu_50K = 1E-2 

        self.name = name
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 3*PHL_twp_cu_50K/2,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 3*PHL_twp_cu_4K/2,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
                        }
        self.default_lengths = FRIDGE_LIBRARY["XLD400"]["lengths"]  #[2019krinnerEngineeringCryogenicSetups]

        self.default_temps = FRIDGE_LIBRARY["XLD400"]["temp"] #[2019krinnerEngineeringCryogenicSetups]

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class Ag():
    def __init__(self, name):

        self.name = name
        self.PHL_dict ={ # https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 2.7E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 0.8E-3,  # (W/channel); from 50K plate to 4K plate
            'Still': 5.4E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 290E-9,   # (W/channel); from Still plate to CP plate
            'MXC'  : 5.9E-9 # (W/channel); from CP plate to MXC plate
            }
        self.default_lengths ={ # 2025paluchThermalizationFlexibleMicrowave
            'RT'   : 32, # arbitrary
            '50K'  : 32, # cm
            '4K'   : 32, # cm
            'Still': 14, # cm
            'CP'   : 14, # cm
            'MXC'  : 20 # cm
            }
        self.default_temps ={ # https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : 300,
            '50K'  : 50, # Kelvin
            '4K'   : 4, # Kelvin
            'Still': 0.6, # Kelvin
            'CP'   : 100E-3, # Kelvin
            'MXC'  : 10E-3 # Kelvin
            }

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class NbTi():
    def __init__(self, name):

        self.name = name
        self.PHL_dict ={# https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : None,  # (W/channel); from 50K plate to 4K plate
            'Still': 540E-9,  # (W/channel); from 4K plate to Still plate
            'CP'   : 29E-9 ,  # (W/channel); from Still plate to CP plate
            'MXC'  : 590E-12 # (W/channel); from CP plate to MXC plate
            }
        self.default_lengths ={ # 2025paluchThermalizationFlexibleMicrowave
            'RT'   : 32, # arbitrary
            '50K'  : 32, # cm
            '4K'   : 32, # cm
            'Still': 14, # cm
            'CP'   : 14, # cm
            'MXC'  : 20 # cm
            }

        self.default_temps ={ # https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : 300,
            '50K'  : 50, # Kelvin
            '4K'   : 4, # Kelvin
            'Still': 0.6, # Kelvin
            'CP'   : 100E-3, # Kelvin
            'MXC'  : 10E-3 # Kelvin
            }

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class HDW():
    def __init__(self, name):
        self.name = name
        self.PHL_dict ={ # 2025raicuCryogenicThermalModeling - Table V (Measured HL)
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 7.566E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 3.157E-4,  # (W/channel); from 50K plate to 4K plate
            'Still': 2.373E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 5.491E-7,   # (W/channel); from Still plate to CP plate
            'MXC'  : 1.132E-8 # (W/channel); from CP plate to MXC plate
            }
        
        self.default_lengths = FRIDGE_LIBRARY["XLD1000SL"]["lengths"]  #[2019krinnerEngineeringCryogenicSetups]
        
        self.default_temps = FRIDGE_LIBRARY["XLD1000SL"]["temp"] #[2019krinnerEngineeringCryogenicSetups]
        
        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################

class HEMT_Bias_Cu ():
    # PHL due to three strands of AWG 30 copper wires
    # three wires (ground, bias, gate) per one amplifier
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(cu_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 3 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class Fiber ():
    def __init__(self, name):
        self.name = name
        self.diam = 250E-6 #m 2021lecocqControlReadoutSuperconducting
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': True,  # (W/channel); from 4K plate to Still plate
            'CP'   : True,   # (W/channel); from Still plate to CP plate
            'MXC'  : True # (W/channel); from CP plate to MXC plate
            }
    
    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(fiber_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        return result * area / (cable_length*1E-2) #cable length is in cm
#####################################################

class HEMT_Bias_Mn ():
    # PHL due to three strands of AWG 30 Manganin wires
    # three wires (ground, bias, gate) per one amplifier
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(mn_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 3 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################
        
class HEMT_Bias_YBCO ():
    # PHL due to three strands of YBCO flexlines
    # three wires (ground, bias, gate) per one amplifier
    def __init__(self, name):
        self.name = name
        
        width = 1E-3 # line width
        thickness = 100E-6 + 1E-6 #100um(kapton) + 1um(YBCO film)
        self.area = width * thickness

        # 2021solovyovYBCOonKaptonMaterialHighDensity
        # https://www.osti.gov/servlets/purl/1764583
        # Assuming worst-case conductivity
        self.YBCO_conductivity = 12 # W per sqm for 1 m long cable between 50K and 4K # overestimation

        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # For 3 wires per amplifier
        return self.YBCO_conductivity * 3 * (self.area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class ULP_HEMT_Bias_Cu ():
    # PHL due to six strands of AWG 30 copper wires
    # three wires (ground, bias, gate) per amplifier stage
    # 2024zengSubmWCryogenicInP (dual bias)
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(cu_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 6 wires per amplifier
        return result * 6 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class ULP_HEMT_Bias_Mn ():
    # PHL due to six strands of AWG 30 copper wires
    # three wires (ground, bias, gate) per amplifier stage
    # 2024zengSubmWCryogenicInP (dual bias)
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(mn_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 6 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class ULP_HEMT_Bias_YBCO ():
    # PHL due to six strands of YBCO flexlines
    # three wires (ground, bias, gate) per amplifier stage
    # 2024zengSubmWCryogenicInP (dual bias)
    def __init__(self, name):
        self.name = name
        
        width = 1E-3 # line width
        thickness = 100E-6 + 1E-6 #100um(kapton) + 1um(YBCO film)
        self.area = width * thickness

        # 2021solovyovYBCOonKaptonMaterialHighDensity
        # https://www.osti.gov/servlets/purl/1764583
        # Assuming worst-case conductivity
        self.YBCO_conductivity = 12 # W per sqm for 1 m long cable between 50K and 4K # overestimation

        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # For 6 wires per amplifier
        return self.YBCO_conductivity * 6 * (self.area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class SIS_v1_5w_Bias_Cu ():
    # PHL due to five strands of AWG 30 copper wires required for SIS operation
    # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(cu_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 5 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class SIS_v1_5w_Bias_Mn ():
    # PHL due to five strands of AWG 30 Manganin wires required for SIS operation
    # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(mn_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 5 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class SIS_v1_5w_Bias_YBCO ():
    # PHL due to five strands of YBCO flexlines
    # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
    def __init__(self, name):
        self.name = name
        
        width = 1E-3 # line width
        thickness = 100E-6 + 1E-6 #100um(kapton) + 1um(YBCO film)
        self.area = width * thickness

        # 2021solovyovYBCOonKaptonMaterialHighDensity
        # https://www.osti.gov/servlets/purl/1764583
        # Assuming worst-case conductivity
        self.YBCO_conductivity = 12 # W per sqm for 1 m long cable between 50K and 4K # overestimation

        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # For 6 wires per amplifier
        return self.YBCO_conductivity * 5 * (self.area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class SIS_v1_13w_Bias_Mn ():
    # PHL due to thirteen strands of AWG 30 Manganin wires required for SIS operation
    # Assuming a 5 way LO current split
    # [SIS_up, SIS_down, GND, (LO_in, LO_out)*5]
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(mn_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 13 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

class YBCO_rf ():
    # PHL due to RF YBCO flexlines
    def __init__(self, name):
        self.name = name
        
        width = 1E-3 # line width
        thickness = 100E-6 + 1E-6 #100um(kapton) + 1um(YBCO film)
        self.area = width * thickness

        # 2021solovyovYBCOonKaptonMaterialHighDensity
        # https://www.osti.gov/servlets/purl/1764583
        # Assuming worst-case conductivity
        self.YBCO_conductivity = 12 # W per sqm for 1 m long cable between 50K and 4K # overestimation

        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Assuming two assume two YBCO ground planes with widths equal to twice the signal-line pitch
        # Approximately equal to 5 strips (2*(ground planes with 2xwidth) + signal plane)
        return self.YBCO_conductivity * 5 * (self.area/(cable_length*1E-2)) #cable length is in cm
#####################################################
class Agv2():
    def __init__(self, name):

        self.name = name
        self.PHL_dict ={ # https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 2.7E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 0.8E-3,  # (W/channel); from 50K plate to 4K plate
            '2K'   : True,
            'Still': 5.4E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 290E-9,   # (W/channel); from Still plate to CP plate
            'MXC'  : 5.9E-9 # (W/channel); from CP plate to MXC plate
            }
        self.default_lengths ={ # 2025paluchThermalizationFlexibleMicrowave
            'RT'   : 32, # arbitrary
            '50K'  : 32, # cm
            '4K'   : 32, # cm
            'Still': 14, # cm
            'CP'   : 14, # cm
            'MXC'  : 20 # cm
            }
        self.default_temps ={ # https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : 300,
            '50K'  : 50, # Kelvin
            '4K'   : 4, # Kelvin
            'Still': 0.6, # Kelvin
            'CP'   : 100E-3, # Kelvin
            'MXC'  : 10E-3 # Kelvin
            }

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)
        self.thermal_conductivity["2K"] = self.thermal_conductivity["4K"]

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################
class NbTiv2():
    def __init__(self, name):

        self.name = name
        self.PHL_dict ={# https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : None,  # (W/channel); from 50K plate to 4K plate
            '2K'   : True,
            'Still': 540E-9,  # (W/channel); from 4K plate to Still plate
            'CP'   : 29E-9 ,  # (W/channel); from Still plate to CP plate
            'MXC'  : 590E-12 # (W/channel); from CP plate to MXC plate
            }
        self.default_lengths ={ # 2025paluchThermalizationFlexibleMicrowave
            'RT'   : 32, # arbitrary
            '50K'  : 32, # cm
            '4K'   : 32, # cm
            'Still': 14, # cm
            'CP'   : 14, # cm
            'MXC'  : 20 # cm
            }

        self.default_temps ={ # https://delft-circuits.com/wp-content/uploads/2026/03/Brochure_2026_Delft_Circuits.pdf
            'RT'   : 300,
            '50K'  : 50, # Kelvin
            '4K'   : 4, # Kelvin
            'Still': 0.6, # Kelvin
            'CP'   : 100E-3, # Kelvin
            'MXC'  : 10E-3 # Kelvin
            }

        self.thermal_conductivity = infer_thermal_conductivity(self.PHL_dict, self.default_lengths, self.default_temps)
        self.thermal_conductivity["2K"] = self.thermal_conductivity["4K"]

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        temp_diff = T_hi - T_lo 
        if self.thermal_conductivity[temp_stage] is not None:
            return self.thermal_conductivity[temp_stage] *  temp_diff /cable_length
        else:
            return None
#####################################################
class HEMT_Bias_Cuv2 ():
    # PHL due to three strands of AWG 30 copper wires
    # three wires (ground, bias, gate) per one amplifier
    def __init__(self, name):
        self.name = name
        self.diam = 0.2546E-3 # m (AWG30)
        self.PHL_dict ={
            'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : True,  # (W/channel); from 300K flange to 50K plate
            '4K'   : True,  # (W/channel); from 50K plate to 4K plate
            '2K'   : True,
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

    def get_PHL(self, temp_stage, cable_length, T_lo, T_hi): # cable lengths in cm
        # Integrate cu_thermal_conductivity(T) from T_hi to T_lo
        result, error = quad(cu_thermal_conductivity, T_lo, T_hi)
        # Get cross sectional area of wire 
        area = np.pi * (self.diam/2)**2
        # For 3 wires per amplifier
        return result * 3 * (area/(cable_length*1E-2)) #cable length is in cm
#####################################################

CABLE_REGISTRY = {
    "SS_Drive": SS_Drive,
    "SS_Flux": SS_Flux,
    "NbTi_coax": NbTi_coax,
    "GHOST": GHOST,
    "Cu_35_bias": Cu_35_bias,
    "Ag": Ag,
    "NbTi": NbTi,
    "HDW": HDW,
    "HEMT_Bias_Cu":HEMT_Bias_Cu,
    "Fiber":Fiber,
    "HEMT_Bias_Mn":HEMT_Bias_Mn,
    "HEMT_Bias_YBCO":HEMT_Bias_YBCO,
    "ULP_HEMT_Bias_Cu":ULP_HEMT_Bias_Cu,
    "ULP_HEMT_Bias_Mn":ULP_HEMT_Bias_Mn,
    "ULP_HEMT_Bias_YBCO":ULP_HEMT_Bias_YBCO,
    "SIS_v1_5w_Bias_Cu":SIS_v1_5w_Bias_Cu,
    "SIS_v1_5w_Bias_Mn":SIS_v1_5w_Bias_Mn,
    "SIS_v1_5w_Bias_YBCO":SIS_v1_5w_Bias_YBCO,
    "SIS_v1_13w_Bias_Mn":SIS_v1_13w_Bias_Mn,
    "YBCO_rf":YBCO_rf,
    "Agv2": Agv2,
    "NbTiv2": NbTiv2,
    "HEMT_Bias_Cuv2":HEMT_Bias_Cuv2,
}

#####################################################
def create_cable_instance(cable_name):
    if cable_name in list(CABLE_REGISTRY.keys()):
        cable_class = CABLE_REGISTRY[cable_name]
        return cable_class(cable_name)
    else:
        print(f"Cable class {cable_name} does not exist.")
        return None
#####################################################

def get_cable_config(cable_config_names):
    cable_config = {}
    for cable_type, config in cable_config_names.items():
        cable_config[cable_type]={}
        for temp_stage, cable_name in config.items():
            if cable_name is not None:
                cable_config[cable_type][temp_stage] = create_cable_instance(cable_name)
            else:
                cable_config[cable_type][temp_stage] = None
    return cable_config
#####################################################
    
def cable_attenuator_dissipation(cable_attenuator_config, output_power_MXC):
    """
    Outputs the power inputs (or equivalently the power dissipated by the attenuators) at each temperature stage for a given cable. 
    At 10-20 dB attenuation, almost all (90%-99%) of the input power is dissipated in the attenuator so ** input power = dissipated power **

    Parameters
    ----------
    attenuator_config : dict
        configuration of attenuators in dB: {'RT'   : ATT_RT
                                             '50K'  : ATT_50K
                                             '4K'   : ATT_4K, 
                                             'Still': ATT_Still, 
                                             'CP'   : ATT_CP,
                                             'MXC'  : ATT_MXC}
        negative values not allowed
            
    output_power_MXC in dBm : int
        the final power level expected at MXC (qubit)

    Returns
    -------
    dict
        dictionary with keys ['RT','50K','4K', 'Still', 'CP', 'MXC'] whose values indicate the power dissipated by the attenuators at each stage in dBm.
        If no power is dissipated (i.e., the attenuator does not exist), then it returns None.
    """
    # Check if attenuations are all non-negative
    try:
        all(value >= 0 for value in cable_attenuator_config.values())
    except:
        print("Attenuator values must always be non-negative")

    # Initialize output dictionary
    output_dict = { 'RT'   : None,
                    '50K'  : None,        
                    '4K'   : None, 
                    'Still': None, 
                    'CP'   : None,
                    'MXC'  : None}

    # When output_power_MXC is not given
    if output_power_MXC is None:
        return output_dict

    # Given the output power, calculate the input power required
    total_line_attenuation = sum(value for value in cable_attenuator_config.values())
    input_power            = output_power_MXC + total_line_attenuation

    # Calculate the power dissipated at each stage
    remaining_power = input_power
    for key in cable_attenuator_config.keys():
        if cable_attenuator_config[key] > 0: # only positive values (in dBm allowed)
            output_dict[key] = remaining_power
            remaining_power -= cable_attenuator_config[key]
        else:
            output_dict[key] = None

    # Check if the final power matches the desired output power value
    try:
        remaining_power - cable_attenuator_config['MXC'] == output_power_MXC
    except:
        print("Final power level does not match the desired value.")

    return output_dict
#####################################################
def cable_attenuator_dissipationv2(cable_attenuator_config, output_power_MXC):
    """
    Outputs the power inputs (or equivalently the power dissipated by the attenuators) at each temperature stage for a given cable. 
    At 10-20 dB attenuation, almost all (90%-99%) of the input power is dissipated in the attenuator so ** input power = dissipated power **

    Parameters
    ----------
    attenuator_config : dict
        configuration of attenuators in dB: {'RT'   : ATT_RT
                                             '50K'  : ATT_50K
                                             '4K'   : ATT_4K, 
                                             '2K'   : ATT_2K, 
                                             'Still': ATT_Still, 
                                             'CP'   : ATT_CP,
                                             'MXC'  : ATT_MXC}
        negative values not allowed
            
    output_power_MXC in dBm : int
        the final power level expected at MXC (qubit)

    Returns
    -------
    dict
        dictionary with keys ['RT','50K','4K', 'Still', 'CP', 'MXC'] whose values indicate the power dissipated by the attenuators at each stage in dBm.
        If no power is dissipated (i.e., the attenuator does not exist), then it returns None.
    """
    # Check if attenuations are all non-negative
    try:
        all(value >= 0 for value in cable_attenuator_config.values())
    except:
        print("Attenuator values must always be non-negative")

    # Initialize output dictionary
    output_dict = { 'RT'   : None,
                    '50K'  : None,        
                    '4K'   : None, 
                    '2K'   : None, 
                    'Still': None, 
                    'CP'   : None,
                    'MXC'  : None}

    # When output_power_MXC is not given
    if output_power_MXC is None:
        return output_dict

    # Given the output power, calculate the input power required
    total_line_attenuation = sum(value for value in cable_attenuator_config.values())
    input_power            = output_power_MXC + total_line_attenuation

    # Calculate the power dissipated at each stage
    remaining_power = input_power
    for key in cable_attenuator_config.keys():
        if cable_attenuator_config[key] > 0: # only positive values (in dBm allowed)
            output_dict[key] = remaining_power
            remaining_power -= cable_attenuator_config[key]
        else:
            output_dict[key] = None

    # Check if the final power matches the desired output power value
    try:
        remaining_power - cable_attenuator_config['MXC'] == output_power_MXC
    except:
        print("Final power level does not match the desired value.")

    return output_dict
