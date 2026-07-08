TEMP_STAGES = ['RT', '50K', '4K', 'Still', 'CP', 'MXC']
TEMP_STAGES_COLOSSUS = ['RT', '50K', '4K', '2K', 'Still', 'CP', 'MXC']


XLD400 = { # 2019krinnerEngineeringCryogenicSetups
    "cooling_power":{
        'RT'   : 100,
        '50K'  : 30, # Watts
        '4K'   : 1.5, # Watts # includes passive heat due to Cu and PhBr wires
        'Still': 40E-3, # Watts
        'CP'   : 200E-6, # Watts
        'MXC'  : 19E-6 # Watts
    },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 45, # Kelvin
        '4K'   : 4.2, # Kelvin
        'Still': 1.2, # Kelvin
        'CP'   : 140E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{
        'RT'   : 100, # arbitrary
        '50K'  : 20, # cm
        '4K'   : 29, # cm
        'Still': 25, # cm
        'CP'   : 17, # cm
        'MXC'  : 14 # cm
    }
}


KIDE = { # 2024blueforsKIDEProductOverview. Assuming 3 x XLD100sl
    "cooling_power":{
        'RT'   : 1000, # Watts
        '50K'  : 300, # Watts
        '4K'   : 2 * 3, # Watts # Assuming operating temperature of 4K [https://bluefors.com/products/measurement-infrastructure/high-density-wiring/]
        'Still': 90e-3, # Bluefors SC25
        'CP'   : 1E-3 * 3, # Watts
        'MXC'  : 30E-6 * 3 # Watts
    },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 40, # Kelvin
        '4K'   : 3.5, # Kelvin
        'Still': 1.2, # Kelvin
        'CP'   : 200E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{ # 2025raicuCryogenicThermalModeling - Table 1
        'RT'   : 100, # arbitrary
        '50K'  : 30.53, # cm
        '4K'   : 31.55, # cm
        'Still': 27.75, # cm
        'CP'   : 19.65, # cm
        'MXC'  : 19.65 # cm
    }
}

XLD1000SL = { # 2024blueforsKIDEProductOverview. Assuming 3 x XLD100sl
    "cooling_power":{ # 2025raicuCryogenicThermalModeling - Table 1
        'RT'   : 100, # Watts
        '50K'  : 30, # Watts 2 *PT420 pulse tubes
        '4K'   : 0.7, # Watts
        'Still': 7e-3, # Watts
        'CP'   : 1E-3, # Watts
        'MXC'  : 30E-6 # Watts
    },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 40, # Kelvin
        '4K'   : 3.5, # Kelvin
        'Still': 1.4, # Kelvin
        'CP'   : 200E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{ # 2025raicuCryogenicThermalModeling - Table 1
        'RT'   : 100, # arbitrary
        '50K'  : 30.53, # cm
        '4K'   : 31.55, # cm
        'Still': 27.75, # cm
        'CP'   : 19.65, # cm
        'MXC'  : 19.65 # cm
    }
}

# COLOSSUS = { # 2024hollisterUpdateColossusMK
#     "cooling_power":{ # 2024hollisterUpdateColossusMK
#     'RT'   : 20E3, # Watts
#     '50K'  : 9E3, # Watts
#     '4K'   : 200, # Watts 
#     'Still': 100e-3, # Watts
#     'CP'   : 2 * 1.5E-3, # Watts # 2 dilution units
#     'MXC'  : 10 *30E-6 # Watts # 10 dilution units
#     },
    
#     "temp":{
#         'RT'   : 300,
#         '50K'  : 80, # Kelvin
#         '4K'   : 5, # Kelvin
#         'Still': 1, # Kelvin
#         'CP'   : 100E-3, # Kelvin
#         'MXC'  : 20E-3 # Kelvin
#     },
    
#     "lengths":{ # 2025raicuCryogenicThermalModeling - Table 1
#         'RT'   : 100, # arbitrary
#         '50K'  : 24.64, # cm (9.7 inch)
#         '4K'   : 39.88, # cm (15.7 inch)
#         'Still': 100.84, # cm (18.2 + 21.5 = 39.7 inch)
#         'CP'   : 54.61, # cm (21.5 inch)
#         'MXC'  : 54.61, # cm (21.5 inch)
#     }
# }

COLOSSUS = { # 2024hollisterUpdateColossusMK
    "cooling_power":{ 
        'RT'   : 20E3, # Watts
        '50K'  : 9E3, # Watts
        '4K'   : 200, # Watts 
        '2K'   : 10, # Watts
        'Still': 100e-3, # Watts
        'CP'   : 2 * 1.5E-3, # Watts
        'MXC'  : 10 *30E-6 # Watts
        },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 80, # Kelvin
        '4K'   : 5, # Kelvin
        '2K'   : 2, # Kelvin
        'Still': 1, # Kelvin
        'CP'   : 100E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{ 
        'RT'   : 100, # arbitrary
        '50K'  : 24.64, # cm (9.7 inch)
        '4K'   : 39.88, # cm (15.7 inch)
        '2K'   : 54.61, # cm (21.5 inch)
        'Still': 46.23, # cm (18.2 inch)
        'CP'   : 54.61, # cm (21.5 inch)
        'MXC'  : 54.61, # cm (21.5 inch)
    }
}

COLOSSUS_CP = { # 2024hollisterUpdateColossusMK
    "cooling_power":{ 
        'RT'   : 20E3, # Watts
        '50K'  : 9E3, # Watts
        '4K'   : 200, # Watts 
        '2K'   : 10, # Watts
        'Still': 100e-3, # Watts
        'CP'   : 4 * 1.5E-3, # Watts
        'MXC'  : 8 *30E-6 # Watts
    },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 80, # Kelvin
        '4K'   : 5, # Kelvin
        '2K'   : 2, # Kelvin
        'Still': 1, # Kelvin
        'CP'   : 100E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{ 
        'RT'   : 100, # arbitrary
        '50K'  : 24.64, # cm (9.7 inch)
        '4K'   : 39.88, # cm (15.7 inch)
        '2K'   : 54.61, # cm (21.5 inch)
        'Still': 46.23, # cm (18.2 inch)
        'CP'   : 54.61, # cm (21.5 inch)
        'MXC'  : 54.61, # cm (21.5 inch)
    }
}


FRIDGE_LIBRARY = {
    "XLD400"   : XLD400,
    "XLD1000SL": XLD1000SL,
    "KIDE": KIDE,
    "COLOSSUS":COLOSSUS,
    "COLOSSUS_CP":COLOSSUS_CP,
}
