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
from library.utils import watts_to_dbm, dBm2Watts

#####################################################
# Add DC resistance for flux-bias and coupler-bias lines
def add_flux_coupler_DC_resistance(COMP_CONFIG,
                                   QUBIT_FREQ, 
                                   QUBIT_COUPLING, 
                                   R_4K, R_Still, R_CP, R_MXC,
                                   I_BIAS, I_2Q):
    if QUBIT_FREQ == "TUNABLE":
        [comp.set_values(R_4K, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["4K"]]
        [comp.set_values(R_Still, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["Still"]]
        [comp.set_values(R_CP, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["CP"]]
        [comp.set_values(R_MXC, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["MXC"]]
    if QUBIT_COUPLING == "TUNABLE":
        [comp.set_values(R_4K, I_2Q) for comp in COMP_CONFIG["COUPLER"]["4K"]]
        [comp.set_values(R_Still, I_2Q) for comp in COMP_CONFIG["COUPLER"]["Still"]]
        [comp.set_values(R_CP, I_2Q) for comp in COMP_CONFIG["COUPLER"]["CP"]]
        [comp.set_values(R_MXC,I_2Q) for comp in COMP_CONFIG["COUPLER"]["MXC"]]

    return COMP_CONFIG
#######################################################################
def add_ohmic_resistors_amp_at_4K(CABLE_CONFIG_NAMES, COMP_CONFIG, fridge):
    # Determine current in amplifier
    current = None
    if CABLE_CONFIG_NAMES['AMP_BIAS']['4K'] is not None:
        for component in COMP_CONFIG['AMP_BIAS']['4K']:
            if isinstance(component, AMPLIFIER):
                current = component.I

    # 4K stage
    # Determine Ohmic resistance for amplifier Biasing
    resistance = None
    name = None
    
    diam = 0.2546E-3 # m (AWG30)
    area = np.pi * (diam/2)**2

    T_RT = fridge["temp"]["RT"]
    T_50K = fridge["temp"]["50K"]
    T_4K = fridge["temp"]["4K"]
    
    length_4K = fridge["lengths"]["4K"] * 1E-2 # cm -->m
    length_50K = fridge["lengths"]["50K"] * 1E-2 # cm --> m
    
    if CABLE_CONFIG_NAMES['AMP_BIAS']['4K'] is not None:
        if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
            resistance = get_resistance(cu_electrical_resistivity, length_4K, area, T_4K, T_50K)
            name = "ohmic_Cu"
        if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
            resistance = get_resistance(mn_electrical_resistivity, length_4K, area, T_4K, T_50K)
            name = "ohmic_Mn"
        if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
            resistance = 0.0
            name = "ohmic_YBCO"
    else:
        resistance = 0.0
        name = "ohmic_zero"

    # Create Ohmic Resistor
    if CABLE_CONFIG_NAMES['AMP_BIAS']['4K'] is not None:
        if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
            ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
            if COMP_CONFIG['AMP_BIAS']['4K']is not None:
                COMP_CONFIG['AMP_BIAS']['4K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['4K'] = [ohmic_resistor]
        
        elif 'SIS_v1' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # SIS_v1_5w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 3)/2 # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['4K']is not None:
                COMP_CONFIG['AMP_BIAS']['4K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['4K'] = [ohmic_resistor]
            
        elif 'SIS_v2' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # SIS_v2_9w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 7)/2 # [SIS_up, SIS_up_V+, SIS_up_V-, SIS_down, SIS_down_V+, SIS_down_V-, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['4K']is not None:
                COMP_CONFIG['AMP_BIAS']['4K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['4K'] = [ohmic_resistor]

    # 50K stage
    # Ohmic resistance for amplifier Biasing
    resistance = None
    name = None
    if CABLE_CONFIG_NAMES['AMP_BIAS']['50K'] is not None:
        if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].lower():
            resistance_4K_cu = get_resistance(cu_electrical_resistivity, length_4K, area, T_4K, T_50K)
            resistance_50K_cu = get_resistance(cu_electrical_resistivity, length_50K, area, T_50K, T_RT)
            resistance = resistance_50K_cu + resistance_4K_cu # half of ohmic heat from 4K flows to 50K stage
            name = "ohmic_Cu"
        if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].lower():
            resistance_4K_mn = get_resistance(mn_electrical_resistivity, length_4K, area, T_4K, T_50K)
            resistance_50K_mn = get_resistance(mn_electrical_resistivity, length_4K, area, T_50K, T_RT)
            resistance = resistance_50K_mn + resistance_4K_mn # half of ohmic heat from 4K flows to 50K stage
            name = "ohmic_Mn"
        if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].lower():
            resistance = 0.0
            name = "ohmic_YBCO"
    else:
        resistance = 0.0
        name = "ohmic_zero"
    # 
    # Ohmic Resistor
    if CABLE_CONFIG_NAMES['AMP_BIAS']['50K'] is not None:
        if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K']:
            ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
            if COMP_CONFIG['AMP_BIAS']['50K']is not None:
                COMP_CONFIG['AMP_BIAS']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['50K'] = [ohmic_resistor]
        
        elif 'SIS_v1' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].split('_') # SIS_v1_5w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 3)/2 # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['50K']is not None:
                COMP_CONFIG['AMP_BIAS']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['50K'] = [ohmic_resistor]
            
        elif 'SIS_v2' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].split('_') # SIS_v2_9w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 7)/2 # [SIS_up, SIS_up_V+, SIS_up_V-, SIS_down, SIS_down_V+, SIS_down_V-, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['50K']is not None:
                COMP_CONFIG['AMP_BIAS']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['50K'] = [ohmic_resistor]
    return COMP_CONFIG
########################################################################

def add_ohmic_resistors_amp_at_50K(CABLE_CONFIG_NAMES, COMP_CONFIG, fridge):
    # Determine current in amplifier
    current = None
    if CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'] is not None:
        for component in COMP_CONFIG['AMP_BIAS_50K']['50K']:
            if isinstance(component, AMPLIFIER):
                current = component.I

    # 50K stage
    # Ohmic resistance for amplifier Biasing
    resistance = None
    name = None

    diam = 0.2546E-3 # m (AWG30)
    area = np.pi * (diam/2)**2

    T_hi = fridge["temp"]["RT"]
    T_lo = fridge["temp"]["50K"]
    length = fridge["lengths"]["50K"] * 1E-2 # cm --> m

    if CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'] is not None:
        if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'].lower():
            resistance = get_resistance(cu_electrical_resistivity, length, area, T_lo, T_hi)
            name = "ohmic_Cu"
        if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'].lower():
            resistance = get_resistance(mn_electrical_resistivity, length, area, T_lo, T_hi)
            name = "ohmic_Mn"
        if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'].lower():
            resistance = 0.0
            name = "ohmic_YBCO"
    else:
        resistance = 0.0
        name = "ohmic_zero"

    # Ohmic Resistor
    if CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'] is not None:
        if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K']:
            ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
            if COMP_CONFIG['AMP_BIAS_50K']['50K']is not None:
                COMP_CONFIG['AMP_BIAS_50K']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS_50K']['50K'] = [ohmic_resistor]
    return COMP_CONFIG
########################################################################

# Amplifier Class
#################
class AMPLIFIER():
    def __init__(self, V, I, name):
        self.name = name
        self.V = V # operating voltage
        self.I = I # operating current

    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # then override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
        
        power = self.V * self.I # dissipative power in Watts due to biasing (always ON)
        return power # dissipative power in Watts due to biasing (always ON)
########################################################################

class AMP_OHMIC_RESISTOR():
    def __init__(self,R,I,name):
        """
        R: float
            Resistance in ohms
        I: float
            Current in biasing wires in amperes
            Includes both incoming and outgoing currents
        name : stf
            Name of the component

        Returns power in Watts due to ohmic (joule) heating
        """
        self.name = name
        self.R = R
        self.I = I
        
    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
        
        power = 0.0
        if self.R == None or self.I == None:
            error_message = "Error: Values have not been set properly.\n"
            error_message += f"R = {self.R},  I = {self.I}"
            raise ValueError(error_message)
        else:
            ### factor = 2: incoming and outgoing current flows through both HEMT_Vd and HEMT_GND
            ### factor = 0.5: assuming joule heat flows equally into 50K and 4K thermal plate anchors
            power = 0.5 * 2 * self.I**2 * self.R
            return power
########################################################################

def SIS_current_split(SIS_I, num_LO_pair):
    # split_no: No. of wires in which LO current is split
    ## Currents
    SIS_up       = 25E-6  # 2023kojimaCharacterizationLownoiseSuperconductor
    SIS_up_vs1   = 0 
    SIS_up_vs2   = 0
    SIS_down     = 110E-6 # 2023kojimaCharacterizationLownoiseSuperconductor
    SIS_down_vs1 = 0
    SIS_down_vs2 = 0
    SIS_GND      = SIS_up + SIS_down
    SIS_LO       = SIS_I/ num_LO_pair # split current flowing through single wire 
    return [SIS_up, SIS_up_vs1, SIS_up_vs2, SIS_down, SIS_down_vs1, SIS_down_vs2, SIS_GND, SIS_LO, num_LO_pair]
########################################################################

class SIS_OHMIC_RESISTOR():
    def __init__(self,R, current_list, name):
        """
        R: float
            Resistance in ohms
        current: float
            LO current
        name : stf
            Name of the component

        Returns power in Watts due to ohmic (joule) heating
        """
        self.name = name
        self.R = R
        self.current_list= current_list # LO current
        
    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        num_LO_pair = 1
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
        
        power = 0.0   
        SIS_up, SIS_up_vs1, SIS_up_vs2, SIS_down, SIS_down_vs1, SIS_down_vs2, SIS_GND, SIS_LO, num_LO_pair = self.current_list
        
        ### factor = 0.5: assuming joule heat flows equally into 50K and 4K thermal plate anchors
        P_up       = SIS_up**2       * self.R * 0.5
        P_up_vs1   = SIS_up_vs1**2   * self.R * 0.5
        P_up_vs2   = SIS_up_vs2**2   * self.R * 0.5
        P_down     = SIS_down**2     * self.R * 0.5
        P_down_vs1 = SIS_down_vs1**2 * self.R * 0.5
        P_down_vs2 = SIS_down_vs2**2 * self.R * 0.5
        P_GND      = SIS_GND**2      * self.R * 0.5
        ### factor = 2: current flows through both LO_in and LO_out
        P_LO = (num_LO_pair * 2) * SIS_LO**2 * self.R * 0.5 # ohmic dissipation through all LO wires  

        if self.R == None or self.current_list == None:
            error_message = "Error: Values have not been set properly.\n"
            error_message += f"R = {self.R},  current_list = {self.current_list}"
            raise ValueError(error_message)
        else:
            power = P_up + P_up_vs1 + P_up_vs2 + \
                    P_down + P_down_vs1 + P_down_vs2 + \
                    P_GND + P_LO
        return power
########################################################################

class BIAS_RESISTOR():
    def __init__(self, name):
        """
        R: float
            Resistance in ohms
        name : stf
            Name of the component

        Returns power in Watts due to biasing ONLY
        """
        self.name = name
        self.R = None
        self.I_BIAS= None

    def set_values(self, R, I_BIAS):
        self.R = R
        self.I_BIAS= I_BIAS
    
    def power_dissipation(self, operation, MXC_POWER):
        power = 0.0

        if self.R == None or self.I_BIAS == None:
            error_message = "Error: Values have not been set properly. Use set_values(R, I_BIAS) to set up the BIAS_RESISTOR object:\n"
            error_message += f"R = {self.R},  I_BIAS = {self.I_BIAS}"
            raise ValueError(error_message)
        else:
            power = self.R * self.I_BIAS**2

        return power
########################################################################

class RESISTOR_2Q():
    def __init__(self, name):
        """
        R: float
            Resistance in ohms
        name : stf
            Name of the component

        Returns power in Watts due to 2Q operation ONLY
        """
        self.name = name
        self.R = None
        self.I_2Q = None
    
    def set_values(self, R, I_2Q):
        self.R = R
        self.I_2Q= I_2Q
    
    def power_dissipation(self, operation, MXC_POWER):
        power = 0.0
        if self.R == None or self.I_2Q == None:
            error_message = "Error: Values have not been set properly. Use set_values(R, I_2Q) to set up the BIAS_RESISTOR object:\n"
            error_message += f"R = {self.R},  I_2Q = {self.I_2Q}"
            raise ValueError(error_message)
        else:
            power =   self.R * self.I_2Q**2
            
        return power
########################################################################

class PhotoDetector():
    def __init__(self, Z, R, name):
        """
        Z : float
            Load impedance seen by the photodiode (in ohms).
        R : float
            Photodiode responsivity (in amperes per watt), i.e. A/W.
            A prefectly efficient photodiode has R = 1.2 Amp per Watt for a wavelength of 1490 nm
        MXC_POWER: dict
            Power required at the qubit for various operations (1Q, 2Q and Readout) in dBm
        name : stf
            Name of the Photodiode component
        """
        self.Z = Z
        self.R = R
        self.name = name
    
    def power_dissipation(self, operation, MXC_POWER):
        """
        Calculates the active heat load (P_act) in a photonic-link approach, 
        where all incident optical power is dissipated at millikelvin temperature.
        
        Parameters
        ----------
        operation : str
            Type　of operation i.e., 1Q, 2Q or Readout

        MXC_POWER : dict
            Power required at MXC for [cable_type][operation]
        Returns
        -------
        float
            The active heat load P_act (in watts).
        """
        power = 0.0
        # P_mu = Desired microwave power at the qubit (in watts).
        P_mu = None
        if operation == '1Q':
            P_mu = dBm2Watts(MXC_POWER['DRIVE']['1Q'])
        elif operation == '2Q':
            P_mu = dBm2Watts(MXC_POWER['DRIVE']['2Q'])
        elif operation == 'READOUT':
            P_mu = dBm2Watts(MXC_POWER['READOUT_PIN']['READOUT'])
        
        # Implements: P_act = sqrt( (2 * P_mu) / (Z * R^2) )
        if P_mu is not None:
            power = np.sqrt(2.0 * P_mu / self.Z) / self.R

        return power
########################################################################

# Component Instantiations
def create_comp_instance(comp_type_str):
    if comp_type_str == "HEMT_8G":
        # HEMT Amplifier Instantiation
        # https://lownoisefactory.com/product/lnf-lnc4_8f/
        HEMT_V = 0.6 # Volts
        HEMT_I = 13E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "HEMT_8G_HP":
        # HEMT Amplifier Instantiation
        # https://lownoisefactory.com/product/lnf-lnc4_8g/
        HEMT_V = 1 # Volts
        HEMT_I = 20E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "HEMT_8G_LP":
        # HEMT Amplifier Instantiation
        # https://lownoisefactory.com/product/lnf-lnc4_8g/
        HEMT_V = 0.1 # Volts
        HEMT_I = 3E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "ULP_HEMT":
        # HEMT Amplifier Instantiation
        # 2024zengSubmWCryogenicInP
        HEMT_V = 0.08 # Volts
        HEMT_I = 1.5E-3 + 1E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "HEMT_8C":
        # LNF-LNC4_8C [2019krinnerEngineeringCryogenicSetups]
        # https://lownoisefactory.com/wp-content/uploads/2022/03/lnf-lnc4_8c.pdf
        HEMT_V = 0.7 # Volts
        HEMT_I = 15E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "SIS":
        # SIS Amplifier Instantiation      
        # Active Power [2025murayamaFabricationEvaluationWaveguide]
        # SIS_V = 305E-6 # Volts (Local oscillator)
        # SIS_I = 22E-3 # Amperes

        # (9.3E-3*25E-6 + 10.5E-3*110E-6 + 0.305E-3*22E-3) = 8.1 uW / 22E-3
        SIS_V = 368.068E-6 # equivalent volts for same power of 8.1 uW
        SIS_I = 22E-3 # Amperes
        SIS = AMPLIFIER(SIS_V, SIS_I, comp_type_str)
        return SIS
    elif comp_type_str == "PD":
        # Photodetector Instantiation
        PD = PhotoDetector(Z = 10_000,
                            R = 1,
                            name = comp_type_str)
        return PD
    elif comp_type_str == "BIAS_RESISTOR_4K":
        BIAS_RESISTOR_4K = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_4K
    elif comp_type_str == "BIAS_RESISTOR_Still":
        BIAS_RESISTOR_Still = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_Still
    elif comp_type_str == "BIAS_RESISTOR_CP":
        BIAS_RESISTOR_CP = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_CP
    elif comp_type_str == "BIAS_RESISTOR_MXC":
        BIAS_RESISTOR_MXC = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_MXC
    elif comp_type_str == "RESISTOR_2Q_4K":
        RESISTOR_2Q_4K = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_4K
    elif comp_type_str == "RESISTOR_2Q_Still":
        RESISTOR_2Q_Still = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_Still
    elif comp_type_str == "RESISTOR_2Q_CP":
        RESISTOR_2Q_CP = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_CP
    elif comp_type_str == "RESISTOR_2Q_MXC":
        RESISTOR_2Q_MXC = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_MXC
    else:
        return None
#####################################################
        
def get_comp_config(comp_config_names):
    comp_config = {}
    for cable_type, config in comp_config_names.items():
        comp_config[cable_type]={}
        for temp_stage, comp_names in config.items():
            if comp_names is not None:
                if isinstance(comp_names, list):
                    for comp_name in comp_names:
                        comp_config[cable_type][temp_stage] = [create_comp_instance(comp_name) for comp_name in comp_names]
                else:
                    comp_config[cable_type][temp_stage] = [create_comp_instance(comp_names)]
            else:
                comp_config[cable_type][temp_stage] = None
    return comp_config
#####################################################
        
# Electrical Resistivity of Copper
###################################
def _vander_desc(x, deg):
    """Vandermonde with descending powers: [x^deg, x^(deg-1), ..., 1]."""
    x = np.asarray(x, dtype=float)
    return np.vstack([x**k for k in range(deg, -1, -1)]).T

def _poly_derivative_row_desc(x0, deg):
    """
    Row vector r such that r @ c = p'(x0),
    where c are coefficients in descending-power order.
    """
    r = np.zeros(deg + 1, dtype=float)
    # p(x) = sum_{j=0..deg} c[j] * x^(deg-j)
    # p'(x)= sum c[j]*(deg-j)*x^(deg-j-1), for deg-j >= 1
    for j in range(deg):
        power = deg - j
        r[j] = power * (x0 ** (power - 1))
    return r

def constrained_polyfit_loglog(T, rho, deg, T_plateau, rho_plateau, T_anchor, rho_anchor):
    """
    Fit p(log10(T)) = log10(rho) for T > T_plateau with constraints:
      p(log10(T_plateau)) = log10(rho_plateau)   (C0 at join)
      p'(log10(T_plateau)) = 0                   (C1 smooth at join)
      p(log10(T_anchor)) = log10(rho_anchor)     (anchor)
    Returns coefficients in descending powers for np.polyval.
    """
    T = np.asarray(T, dtype=float)
    rho = np.asarray(rho, dtype=float)

    mask = T > T_plateau
    x = np.log10(T[mask])
    y = np.log10(rho[mask])

    A = _vander_desc(x, deg)

    # Constraint matrix C c = d
    xP = np.log10(T_plateau)
    xA = np.log10(T_anchor)
    CP = _vander_desc(np.array([xP]), deg)[0]          # p(xP)
    dCP = _poly_derivative_row_desc(xP, deg)           # p'(xP)
    CA = _vander_desc(np.array([xA]), deg)[0]          # p(xA)

    C = np.vstack([CP, dCP, CA])
    d = np.array([np.log10(rho_plateau), 0.0, np.log10(rho_anchor)], dtype=float)

    # Solve min ||A c - y||^2 subject to C c = d via KKT system
    ATA = A.T @ A
    ATy = A.T @ y

    KKT = np.block([
        [2.0 * ATA, C.T],
        [C,         np.zeros((C.shape[0], C.shape[0]))]
    ])
    rhs = np.concatenate([2.0 * ATy, d])

    sol = np.linalg.solve(KKT, rhs)
    c = sol[:deg + 1]
    return c
#####################################################    

def cu_electrical_resistivity(T):
    """
    The electrical resistivity (rho) of Copper (ohm-meter) at cryogenic temperatures is shown in https://www.copper.org/resources/properties/cryogenic/
    
    This is a log-log plot. 
    We observe that the electrical resistivity is almost constant from 4K to 20K and rises slowly until 60 K and then slowly tapers off.
    
    We are interested in the electrical resisitvity within the temperature range of 4K to 50K and 50K to 300K. 
    Thus we can model the resistivity as a piece-wise function that is constant until 20K.
    From 20K onwards, the resistivity smoothly fits into a 4th degreee polynomial fit (in a log-log scale).
    This is a good approximation model within the temperature range of our interest.
    """
    
    # Data from https://www.copper.org/resources/properties/cryogenic/
    t_data = np.array([4, 5, 6, 7, 10, 20, 40, 50, 70, 100, 200, 300], dtype=float)
    rho_data = np.array([0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.05, 0.09, 0.2, 0.3, 1.0, 1.6], dtype=float) * 1e-8 # ohm-meter

    # Model settings
    rho_plateau = 0.03 * 1e-8 # constant rho until plateau ends at T_plateau_hi
    T_plateau_hi = 20.0 # constant rho until 20K
    T_anchor = 70.0 # anchoring temperature for polyfit
    rho_anchor = 0.2 * 1e-8 # rho at T_anchor
    degree = 4  # 4th degree polynomial fit

    coefficients = constrained_polyfit_loglog(
                            t_data, rho_data, degree,
                            T_plateau_hi, rho_plateau,
                            T_anchor, rho_anchor
                            )    
    T = np.asarray(T, dtype=float)
    out = np.empty_like(T, dtype=float)

    plateau = T <= T_plateau_hi
    out[plateau] = rho_plateau

    if np.any(~plateau):
        logT = np.log10(T[~plateau])
        log_rho = np.polyval(coefficients, logT)
        out[~plateau] = 10.0 ** log_rho

    return out.item() if out.shape == () else out # ohm-meter
#####################################################

def mn_electrical_resistivity(T):
    """
    A key feature of Manganin is that its resistance changes very little with temperature even at cryogenic temperatures.

    Hence we can model the resistivity from 4K to 50K using a linear fit using the values provided in https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-accessories/cryogenic-wire
    """
    
    # Assuming 30 AWG
    ## Manganin - # 83-Cu, 13-Mn, 4-Ni
    x_temp = np.array([4.2, 77, 305])
    y_rho_data = np.array([8.64, 9.13, 9.69]) # ohm/m for 30 AWG wire
    diam = 0.2546E-3 # m (AWG30)
    area = np.pi * (diam/2)**2
    y_rho = y_rho_data * area # ohm-meter

    coefficients = np.polyfit(x_temp, y_rho, 2) # linear fit

    return np.polyval(coefficients,T)
#####################################################

def get_resistance(resistivity_func, length, area, T_lo, T_hi):
    total_int, _ = quad(resistivity_func, T_lo, T_hi)
    average_rho = total_int / (T_hi - T_lo)
    return  average_rho * length / area
#####################################################


