TEMP_STAGES = ['RT', '50K', '4K', 'Still', 'CP', 'MXC']

# 2019krinnerEngineeringCryogenicSetups
XLD400 = { 
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

COLOSSUS = { # 2024hollisterUpdateColossusMK
    "cooling_power":{ # 2024hollisterUpdateColossusMK
    'RT'   : 20E3, # Watts
    '50K'  : 9E3, # Watts
    '4K'   : 200, # Watts 
    'Still': 100e-3, # Watts
    'CP'   : 2 * 1.5E-3, # Watts # 2 dilution units
    'MXC'  : 10 *30E-6 # Watts # 10 dilution units
    },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 80, # Kelvin
        '4K'   : 5, # Kelvin
        'Still': 1, # Kelvin
        'CP'   : 100E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{ # 2025raicuCryogenicThermalModeling - Table 1
        'RT'   : 100, # arbitrary
        '50K'  : 24.64, # cm (9.7 inch)
        '4K'   : 39.88, # cm (15.7 inch)
        'Still': 100.84, # cm (18.2 + 21.5 = 39.7 inch)
        'CP'   : 54.61, # cm (21.5 inch)
        'MXC'  : 54.61, # cm (21.5 inch)
    }
}

COLOSSUS_CP = { # 2024hollisterUpdateColossusMK
    "cooling_power":{ 
    'RT'   : 20E3, # Watts
    '50K'  : 9E3, # Watts
    '4K'   : 200, # Watts 
    'Still': 100e-3, # Watts
    'CP'   : 4 * 1.5E-3, # Watts
    'MXC'  : 8 *30E-6 # Watts
    },
    
    "temp":{
        'RT'   : 300,
        '50K'  : 80, # Kelvin
        '4K'   : 5, # Kelvin
        'Still': 1, # Kelvin
        'CP'   : 100E-3, # Kelvin
        'MXC'  : 20E-3 # Kelvin
    },
    
    "lengths":{ # 2025raicuCryogenicThermalModeling - Table 1
        'RT'   : 100, # arbitrary
        '50K'  : 24.64, # cm (9.7 inch)
        '4K'   : 39.88, # cm (15.7 inch)
        'Still': 100.84, # cm (18.2 + 21.5 = 39.7 inch)
        'CP'   : 54.61, # cm (21.5 inch)
        'MXC'  : 54.61, # cm (21.5 inch)
    }
}



# XLD400 = { # 2019krinnerEngineeringCryogenicSetups
#     'RT'   : 100,
#     '50K'  : 30, # Watts
#     '4K'   : 1.5, # Watts # includes passive heat due to Cu and PhBr wires
#     'Still': 40E-3, # Watts
#     'CP'   : 200E-6, # Watts
#     'MXC'  : 19E-6 # Watts
# }

# XLD400_v2 = { # real 4K power without 24 twp cu and 24 twp phbr compensation
#     'RT'   : 100,
#     '50K'  : 30, # Watts
#     '4K'   : 1.5, # Watts
#     'Still': 40E-3, # Watts
#     'CP'   : 200E-6, # Watts
#     'MXC'  : 19E-6 # Watts
# }

# XLD400_v2 = { # 2019krinnerEngineeringCryogenicSetups - Sec 6 Proposed Setup
#     'RT'   : 100,
#     '50K'  : 30, # Watts
#     '4K'   : 1.5, # Watts
#     'Still': 40E-3, # Watts
#     'CP'   : 400E-6, # Watts
#     'MXC'  : 19E-6 # Watts
# }

# XLD1000SL_v1= { # 2022blueforsBlueforsXLD1000slSystem
#     'RT'   : 100, # Watts
#     '50K'  : 50, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
#     '4K'   : 1.8, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
#     'Still': 0.9, # Watts ~8.97416442e-01 from Still Estimate Notebook
#     'CP'   : 1E-3, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
#     'MXC'  : 30E-6 # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
# }

# XLD1000SL_v2= { # 2022blueforsBlueforsXLD1000slSystem
#     'RT'   : 100, # Watts
#     '50K'  : 50, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
#     '4K'   : 2.35, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
#     'Still': 1.0, # Watts ~9.98417455e-01 from Still Estimate Notebook
#     'CP'   : 1E-3, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
#     'MXC'  : 30E-6 # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
# }

# Most Realistic
XLD1000SL_v3= { # 2025raicuCryogenicThermalModeling - Table 1
    'RT'   : 100, # Watts
    '50K'  : 30, # Watts 2 *PT420 pulse tubes
    '4K'   : 0.7, # Watts
    'Still': 7e-3, # Watts
    'CP'   : 1E-3, # Watts
    'MXC'  : 30E-6 # Watts
}

# ULVAC_v1= {# UDR-1000 (low end)
#     'RT'   : 100, # Watts
#     '50K'  : 10, # Watts
#     '4K'   : 1, # Watts
#     'Still': 15e-3, # Watts
#     'CP'   : 1.5e-3, # Watts
#     'MXC'  : 10E-6 # Watts
# }

# ULVAC_v2= {# UDR-1000 (high end)
#     'RT'   : 100, # Watts
#     '50K'  : 16.7, # Watts
#     '4K'   : 1.7, # Watts
#     'Still': 30e-3, # Watts
#     'CP'   : 7e-4, # Watts
#     'MXC'  : 20E-6 # Watts
# }

# ULVAC_v3= {# UDR-1000 (target)
#     'RT'   : 100, # Watts
#     '50K'  : 16.7, # Watts
#     '4K'   : 1.7, # Watts
#     'Still': 30e-3, # Watts
#     'CP'   : 1.5e-3, # Watts
#     'MXC'  : 45E-6 # Watts
# }

# ULVAC_v4= {# UDR-1000 (highest end) x 3
#     'RT'   : 100, # Watts
#     '50K'  : 16.7, # Watts
#     '4K'   : 1.7 * 3, # Watts
#     'Still': 30e-3 * 3, # Watts
#     'CP'   : 1.5e-3 * 3, # Watts
#     'MXC'  : 45E-6 * 3 # Watts
# }


# KIDE_v1= { # https://bluefors.com/products/kide-cryogenic-platform/
#     'RT'   : 100, # Watts
#     '50K'  : 50, # Watts 
#     '4K'   : 6.0, # Watts # Ilkwon's Estimate from 2023mutusAlgorithmDrivenFault 
#     'Still': 2.81, # Watts  ~2.80813688e+00 from Still Estimate Notebook
#     'CP'   : 1E-3*3, # Watts 3 x XLD1000SL dilution units
#     'MXC'  : 3E-5*3 # Watts 3 x XLD1000SL dilution units
# }

# KIDE_v2= { # 2024blueforsKIDEProductOverview
#     'RT'   : 100, # Watts
#     '50K'  : 50, # Watts # 9 Pulse Tube Cryocoolers - pg. 9
#     '4K'   : 2.35, # Watts # Masubcichi sensei - 9 pulse tube coolers, only 1 is used to cool the 50K and 4K stage 
#     'Still': 2.81, # Watts  ~2.80813688e+00 from Still Estimate Notebook
#     'CP'   : 1E-3*3, # Watts 3 x XLD1000SL dilution units
#     'MXC'  : 3E-5*3 # Watts 3 x XLD1000SL dilution units
# }

# KIDE_v3= { # 2024blueforsKIDEProductOverview
#     'RT'   : 1000, # Watts
#     '50K'  : 350, # Watts
#     '4K'   : 2 * 3, # Watts # Assuming operating temperature of 4K [https://bluefors.com/products/measurement-infrastructure/high-density-wiring/]
#     'Still': 90e-3, # Bluefors SC25
#     'CP'   : 1E-3 * 3, # Watts
#     'MXC'  : 30E-6 * 3 # Watts
# }

# COLOSSUS= { # 2024hollisterUpdateColossusMK
#     'RT'   : 20E3, # Watts
#     '50K'  : 9E3, # Watts
#     '4K'   : 200, # Watts 
#     'Still': 100e-3, # Watts
#     'CP'   : 2 * 1.5E-3, # Watts # 2 dilution units
#     'MXC'  : 10 *30E-6 # Watts # 10 dilution units
# }

# COLOSSUS_CP= { # 2024hollisterUpdateColossusMK
#     'RT'   : 20E3, # Watts
#     '50K'  : 9E3, # Watts
#     '4K'   : 200, # Watts 
#     'Still': 100e-3, # Watts
#     'CP'   : 4 * 1.5E-3, # Watts
#     'MXC'  : 8 *30E-6 # Watts
# }

# COLOSSUS_MXC= { # 2024hollisterUpdateColossusMK
#     'RT'   : 20E3, # Watts
#     '50K'  : 9E3, # Watts
#     '4K'   : 200, # Watts 
#     'Still': 100e-3, # Watts
#     'CP'   : 1 * 1.5E-3, # Watts
#     'MXC'  : 11 *30E-6 # Watts
# }

FRIDGE_LIBRARY = {
    "XLD400"   : XLD400,
    # "XLD1000SL_v1" : XLD1000SL_v1,
    # "XLD1000SL_v2": XLD1000SL_v2,
    "XLD1000SL": XLD1000SL,
    # "KIDE_v1": KIDE_v1,
    # "KIDE_v2": KIDE_v2,
    "KIDE": KIDE,
    # "KIDE_v3": KIDE_v3,
    # "ULVAC_v1": ULVAC_v1,
    # "ULVAC_v2": ULVAC_v2,
    # "ULVAC_v3": ULVAC_v3,
    # "ULVAC_v4":ULVAC_v4,
    "COLOSSUS":COLOSSUS,
    "COLOSSUS_CP":COLOSSUS_CP,
    # "COLOSSUS_MXC":COLOSSUS_MXC,
}
