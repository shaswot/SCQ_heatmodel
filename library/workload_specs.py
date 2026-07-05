############### ESM_CX_a ############################################
ESM_CX_a = {
    "NAME": "ESM_CX_a",
    "LATENCY": { 
        "1Q": 42.67, # ns [2024underwoodUsingCryogenicCMOSa - Fig 2. caption]
        "2Q": 71.1, # ns [2024underwoodUsingCryogenicCMOSa - Fig 2. caption]
        "READOUT": 215, #ns [2025springFastMultiplexedSuperconductingQubit]
        "IDLE": 0, # Key is necessary but value has no meaning
        "TOTAL": 1100 #ns [2025acharyaQuantumErrorCorrection]
    },
    "OPERATION_COUNT": {
        "1Q": 4,
        "2Q": 16,
        "READOUT": 4,
        "IDLE": 0 # Key is necessary but value has no meaning
    },
}

############## ESM_CZ_a ############################################
ESM_CZ_a = {
    "NAME": "ESM_CZ_a",
    "LATENCY": { 
        "1Q": 25, # ns [2025acharyaQuantumErrorCorrection - 105 qubit]
        "2Q": 42, # ns [2025acharyaQuantumErrorCorrection - 105 qubit]
        "READOUT": 375, #ns [2025acharyaQuantumErrorCorrection - 105 qubit]
        "IDLE": 0, # nreq
        "TOTAL": 1100 #ns [2025acharyaQuantumErrorCorrection]
    },
    "OPERATION_COUNT": { 
        "1Q": 16,
        "2Q": 16,
        "READOUT": 4,
        "IDLE": 0 # Key is necessary but value has no meaning
    },
}
#####################################################################