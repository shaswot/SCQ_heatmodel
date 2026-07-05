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
from library.utils import watts_to_dbm, dBm2Watts
#####################################################

# Power required at the MXC for various qubit operations
########################################################
DRIVE_CABLE_POWER_MXC_1Q = -80  #dBm
DRIVE_CABLE_POWER_MXC_2Q = -80  #dBm
# DRIVE_CABLE_POWER_MXC_1Q = -70  #dBm
# DRIVE_CABLE_POWER_MXC_2Q = -70  #dBm
READOUT_PIN_POWER_MXC    = -120 #dBm (1.00e-15 W) [2021bardinMicrowavesQuantumComputing] - Sec V (Pg. 418)
PUMP_POWER_MXC      = -55  #dBm (3.16e-09) [2019krinnerEngineeringCryogenicSetups] - Sec 3.4
    
def get_NO_OF_CABLES(QUBIT_TYPES, QUBIT_FREQ, QUBIT_COUPLING, READOUT_GROUP_SIZE):
    NUM_QUBITS = QUBIT_TYPES["DATA"] + QUBIT_TYPES["ANCILLA"]
    # NO_OF_CABLES = {
    # "DRIVE"       : QUBIT_TYPES["DATA"] + QUBIT_TYPES["ANCILLA"],
    # "PUMP"        : QUBIT_TYPES["ANCILLA"]/READOUT_GROUP_SIZE,
    # "READOUT_PIN" : QUBIT_TYPES["ANCILLA"]/READOUT_GROUP_SIZE,
    # "READOUT_POUT": QUBIT_TYPES["ANCILLA"]/READOUT_GROUP_SIZE, 
    # "AMP_BIAS"    : QUBIT_TYPES["ANCILLA"]/READOUT_GROUP_SIZE, 
    # }
    NO_OF_CABLES = {
        "DRIVE"       : NUM_QUBITS,
        "PUMP"        : NUM_QUBITS/READOUT_GROUP_SIZE,
        "READOUT_PIN" : NUM_QUBITS/READOUT_GROUP_SIZE,
        "READOUT_POUT": NUM_QUBITS/READOUT_GROUP_SIZE, 
        "AMP_BIAS"    : NUM_QUBITS/READOUT_GROUP_SIZE, 
    }
    if QUBIT_FREQ == "TUNABLE":
        NO_OF_CABLES["FLUX_BIAS"] = NUM_QUBITS
    if QUBIT_COUPLING == "TUNABLE":
        NO_OF_CABLES["COUPLER"] = QUBIT_TYPES["COUPLER"]
    return NO_OF_CABLES
    
def get_MXC_POWER(R_MXC, I_2Q, QUBIT_FREQ, QUBIT_COUPLING):   
    MXC_POWER = {
        "DRIVE": {"1Q": DRIVE_CABLE_POWER_MXC_1Q, 
                  "2Q": DRIVE_CABLE_POWER_MXC_2Q,
                  "READOUT" : None,
                  "IDLE" : None,
                 },
        "PUMP": {"1Q": None, 
                      "2Q": None,
                      "READOUT" : PUMP_POWER_MXC,
                      "IDLE" : None,
                     },
        "READOUT_PIN": {"1Q": None, 
                        "2Q": None,
                        "READOUT" : READOUT_PIN_POWER_MXC,
                        "IDLE" : None,
                       },
        "READOUT_POUT": {"1Q": None, 
                         "2Q": None,
                         "READOUT" : None,
                        "IDLE" : None,
                        },
        "AMP_BIAS": {"1Q": None, 
                      "2Q": None,
                      "READOUT" : None,
                      "IDLE" : None,
                       },
    }
    if QUBIT_FREQ == "TUNABLE":
        MXC_POWER["FLUX_BIAS"] = {"1Q": None, # Power dissipated during biasing modeled by external resistor
                                  "2Q": None, # Power dissipated during biasing modeled by external resistor
                                  "READOUT" : None, # Power dissipated during biasing modeled by external resistor
                                  "IDLE" : None, # Power dissipated during biasing modeled by external resistor
                             }
    if QUBIT_COUPLING == "TUNABLE":
        # Refer Explanations Notebook Sec 2 [2019krinnerEngineeringCryogenicSetups - Section 5.2]
        # 2Q Gate Power: FLUX_CABLE_POWER_MXC_2Q (-46.2 dBm)
        FLUX_CABLE_POWER_MXC_2Q = watts_to_dbm(  (R_MXC * I_2Q**2) ) # Watts, 
        MXC_POWER["COUPLER"] = {"1Q": None, # Power for biasing (during 1Q operation)
                                 "2Q": FLUX_CABLE_POWER_MXC_2Q, # Power for 2Q gates + biasing
                                 "READOUT" : None, # Power for biasing (during readout)
                                 "IDLE" : None,
                                 }
        MXC_POWER["DRIVE"]["2Q"] = None
        
    return MXC_POWER

def get_MUX_RATIO(OPERATIONS, DRIVE_MUX, READIN_MUX, READOUT_GROUP_SIZE):
    # Initialize Correction Ratio dictionary
    # Default value for corrections is 1.0
    MUX_RATIO = {}
    for operation in OPERATIONS:
        MUX_RATIO[operation] = 1.0

    # Correction for input line (DRIVE, READOUT_PIN) multiplexing
    MUX_RATIO["1Q"] = 1 / DRIVE_MUX
    MUX_RATIO["2Q"] = 1 / DRIVE_MUX
    
    # Correction for using readout multiplexing
    MUX_RATIO['READOUT'] = 1 / (READIN_MUX * READOUT_GROUP_SIZE)

    return MUX_RATIO