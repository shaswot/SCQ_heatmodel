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
#####################################################################
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



# ############### ESM_CZ_a ############################################
# ESM_CZ_a = {
#     "NAME": "ESM_CZ_a",
#     "LATENCY_Spec": { 
#         "1Q": 25, # ns [2025acharyaQuantumErrorCorrection - 105 qubit]
#         "2Q": 42, # ns [2025acharyaQuantumErrorCorrection - 105 qubit]
#         "READOUT": 400, #ns [2025acharyaQuantumErrorCorrection - 105 qubit]
#         "IDLE": 0, # nreq
#         "TOTAL": 1100 #ns [2025acharyaQuantumErrorCorrection]
#     },
#     "OPERATIONS_Spec": { 
#         "ANCILLA":{
#             "1Q": 8,
#             "2Q": 8,
#             "READOUT": 4,
#             "IDLE":0,
#         },
#         "DATA":{
#             "1Q": 12,
#             "2Q": 8,
#             "READOUT": 0,
#             "IDLE":0,
#         },
#     },
#     "DATA": 4,
#     "ANCILLA":4,
# }
# #####################################################################

# ############### ESM_CX_a ############################################
# ESM_CX_a = {
#     "NAME": "ESM_CX_a",
#     "LATENCY_Spec": { 
#         "1Q": 42.67, # ns [2024underwoodUsingCryogenicCMOSa - Fig 2. caption]
#         "2Q": 71.1, # ns [2024underwoodUsingCryogenicCMOSa - Fig 2. caption]
#         "READOUT": 100, #ns [2025springFastMultiplexedSuperconductingQubit]
#         "IDLE": 0, # nreq
#         "TOTAL": 1100 #ns [2025acharyaQuantumErrorCorrection]
#     },
#     "OPERATIONS_Spec": { # Using values from Ilkwon's spreadsheet
#         "ANCILLA":{
#             "1Q": 4,
#             "2Q": 8,
#             "READOUT": 4,
#             "IDLE":0,
#         },
#         "DATA":{
#             "1Q": 0,
#             "2Q": 8,
#             "READOUT": 0,
#             "IDLE":0,
#         },
#     },
#     "DATA": 4,
#     "ANCILLA":4,
# }
# #####################################################################



############## WORKLOAD_v1###########################################
LATENCY_v1 = { # Ilkwon's spreadsheet
    "1Q": 42.67, # ns [2024underwoodUsingCryogenicCMOSa - Fig 2. caption]
    "2Q": 533.33, # ns [Median Gate time of ibm_sherbook (https://quantum.ibm.com/services/resources?tab=systems&system=ibm_sherbrooke)]
    "READOUT": 1216, #ns [Median Readout length of ibm_sherbook (https://quantum.ibm.com/services/resources?tab=systems&system=ibm_sherbrooke)]
    "IDLE": 0,
    "TOTAL": 2*42.67 + 4*533.33 + 1*1216 # Ilkwon's estimate
}

QEC_OPERATIONS_v1 = { # Using values from Ilkwon's spreadsheet
                      # Assumes 4 ancilla qubits and 4 data qubits
    "ANCILLA":{
        "1Q": 4,
        "2Q": 8,
        "READOUT": 4,
        "IDLE":0,
    },
    "DATA":{
        "1Q": 0,
        "2Q": 8,
        "READOUT": 0,
        "IDLE":0,
    }
}

WORKLOAD_v1 = {
    "NAME": "WORKLOAD_v1",
    "LATENCY_Spec": LATENCY_v1,
    "OPERATIONS_Spec": QEC_OPERATIONS_v1,
    "DATA": 4,
    "ANCILLA":4,
}
#####################################################################

############## WORKLOAD_v2###########################################
LATENCY_v2 = { # 2017versluisScalableQuantumCircuit  - Fig.5a
    "1Q": 20, # ns
    "2Q": 40, # ns
    "READOUT": 500, #ns 
    "IDLE": 0,
    "TOTAL": 700 # Ilkwon's estimate
}

QEC_OPERATIONS_v2 = { # 2017versluisScalableQuantumCircuit  - Fig.5a
                      # Refer Explanation Notebook - Section 4
    "ANCILLA":{ # For ONE ancilla qubit
        "1Q": 2,
        "2Q": 4,
        "READOUT": 1,
        "IDLE":0, # No meaning
    },
    "DATA":{# Refer Explanation Notebook - Section 4
            # For ONE data qubit
        "1Q": 2+2+2,
        "2Q": 4+3+3,
        "READOUT": 0,
        "IDLE":0,
    }
}

WORKLOAD_v2 = {
    "NAME": "WORKLOAD_v2",
    "LATENCY_Spec": LATENCY_v2,
    "OPERATIONS_Spec": QEC_OPERATIONS_v2,
    "DATA": 1, # For ONE data qubit
    "ANCILLA":1, # For ONE ancilla qubit
}
#####################################################################

############## WORKLOAD_v3###########################################
LATENCY_v3 = { # [2025acharyaQuantumErrorCorrection - Supplementary Information]
    "1Q": 25, # ns
    "2Q": 42, # ns
    "READOUT": 376.75, #ns 
    "IDLE": 0,
    "TOTAL": 1100 # Ilkwon's estimate
}

QEC_OPERATIONS_v3 = { # 2017versluisScalableQuantumCircuit  - Fig.5a
                      # Refer Explanation Notebook - Section 4
    "ANCILLA":{ # For ONE ancilla qubit
        "1Q": 2,
        "2Q": 4,
        "READOUT": 1,
        "IDLE":0, # No meaning
    },
    "DATA":{# Refer Explanation Notebook - Section 4
            # For ONE data qubit
        "1Q": 2+2+2,
        "2Q": 4+3+3,
        "READOUT": 0,
        "IDLE":0,
    }
}

WORKLOAD_v3 = {
    "NAME": "WORKLOAD_v3",
    "LATENCY_Spec": LATENCY_v2,
    "OPERATIONS_Spec": QEC_OPERATIONS_v2,
    "DATA": 1, # For ONE data qubit
    "ANCILLA":1, # For ONE ancilla qubit
}
#####################################################################