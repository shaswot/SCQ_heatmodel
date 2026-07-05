# # [2019krinnerEngineeringCryogenicSetups - Section 5.2]
# R_CP     = 0.42 # DC resistance of bias cables from Still to CP
# R_MXC    = 0.15 # DC resistance of bias cables from CP to MXC
# I_BIAS   = 1E-3 # Ampere; Max current amplitude required to bias qubits for 1Q operation
# I_2Q     = 0.4E-3 # Ampere: Current required to bias qubits for 2Q operation

# # Power required at the MXC for various qubit operations
# ########################################################
# DRIVE_CABLE_POWER_MXC_1Q = -73  #dBm (5.01e-11 W) Refer Explanations Notebook Sec 1 - assuming 100% duty cycle [2019krinnerEngineeringCryogenicSetups - Sec 2.2.2]

# READOUT_PIN_POWER_MXC    = -120 #dBm (1.00e-15 W) [2021bardinMicrowavesQuantumComputing] - Sec V (Pg. 418)
# TWPA_PUMP_POWER_MXC      = -55  #dBm (3.16e-09) [2019krinnerEngineeringCryogenicSetups] - Sec 3.4


# ### SIS Constants ###
# # Wire Dimensions
# length = 460E-3 # 460 mm # https://lownoisefactory.com/product/lnf-nano9m/
# area = 0.0509E-6 # 30 AWG = 0.0509 mm2 # https://lownoisefactory.com/product/lnf-nano9m/

# ## Average Resistivity for 30 AWG wire between 4K and 50K
# rho_Manganin = 4.491120e-07 # Ohm-m
# rho_Cu = 1.8266e-10 #Ohm-m

# ## Average Resistance
# R_Cu = rho_Cu * area * length # 1.651e-03 ohms
# R_Manganin = rho_Manganin * area * length # 4.059 Ohms
########################

ROW_ORDER = ["DRIVE", "FLUX_BIAS", "COUPLER", "PUMP", "READOUT_PIN", "READOUT_POUT", "AMP_BIAS","AMP_BIAS_50K", "DC_TERMINAL", "JJ_BIAS", "TOTAL"]
ORDER_DICT = {row: index for index, row in enumerate(ROW_ORDER)}