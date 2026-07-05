"""Shared experiment configuration helpers.

This module replaces the per-experiment configure.py files while preserving the
three functions imported by the notebooks: get_NO_OF_CABLES, get_MXC_POWER, and
get_MUX_RATIO.
"""

from library.mxc_powers import (
    PUMP_POWER_MXC,
    READOUT_PIN_POWER_MXC,
    select_drive_power,
)
from library.utils import watts_to_dbm


def get_NO_OF_CABLES(QUBIT_TYPES, QUBIT_FREQ, QUBIT_COUPLING, READOUT_GROUP_SIZE):
    """Return the number of physical lines needed for each cable type.

    AMP_BIAS_50K is always included in the returned dictionary so one global
    configure file can serve both old and new experiments.  Existing notebooks
    iterate over CABLE_TYPES from hardware_config.yaml, so this extra key is
    ignored unless the YAML opts into AMP_BIAS_50K as an actual cable type.
    """
    qubit_freq = str(QUBIT_FREQ).strip().upper()
    qubit_coupling = str(QUBIT_COUPLING).strip().upper()
    num_qubits = QUBIT_TYPES["DATA"] + QUBIT_TYPES["ANCILLA"]

    no_of_cables = {
        "DRIVE": num_qubits,
        "PUMP": num_qubits / READOUT_GROUP_SIZE,
        "READOUT_PIN": num_qubits / READOUT_GROUP_SIZE,
        "READOUT_POUT": num_qubits / READOUT_GROUP_SIZE,
        "AMP_BIAS": num_qubits / READOUT_GROUP_SIZE,
        "AMP_BIAS_50K": num_qubits / READOUT_GROUP_SIZE,
        "DC_TERMINAL": num_qubits / READOUT_GROUP_SIZE,
    }

    if qubit_freq == "TUNABLE":
        no_of_cables["FLUX_BIAS"] = num_qubits

    if qubit_coupling == "TUNABLE":
        no_of_cables["COUPLER"] = QUBIT_TYPES["COUPLER"]

    return no_of_cables


def get_MXC_POWER(
    R_MXC,
    I_2Q,
    QUBIT_FREQ,
    QUBIT_COUPLING,
    DRIVE_POWER_PROFILE=None,
):
    """Return operation powers at MXC, in dBm where a cable has active power.

    Drive powers are selected in library.mxc_powers from QUBIT_FREQ and
    QUBIT_COUPLING.  DRIVE_POWER_PROFILE is an optional YAML escape hatch for
    same-topology experiments that intentionally use a different drive power.
    """
    qubit_freq = str(QUBIT_FREQ).strip().upper()
    qubit_coupling = str(QUBIT_COUPLING).strip().upper()
    drive_power = select_drive_power(
        qubit_freq,
        qubit_coupling,
        DRIVE_POWER_PROFILE=DRIVE_POWER_PROFILE,
    )

    mxc_power = {
        "DRIVE": {
            "1Q": drive_power["1Q"],
            "2Q": drive_power["2Q"],
            "READOUT": None,
            "IDLE": None,
        },
        "PUMP": {
            "1Q": None,
            "2Q": None,
            "READOUT": PUMP_POWER_MXC,
            "IDLE": None,
        },
        "READOUT_PIN": {
            "1Q": None,
            "2Q": None,
            "READOUT": READOUT_PIN_POWER_MXC,
            "IDLE": None,
        },
        "READOUT_POUT": {
            "1Q": None,
            "2Q": None,
            "READOUT": None,
            "IDLE": None,
        },
        "AMP_BIAS": {
            "1Q": None,
            "2Q": None,
            "READOUT": None,
            "IDLE": None,
        },
        "AMP_BIAS_50K": {
            "1Q": None,
            "2Q": None,
            "READOUT": None,
            "IDLE": None,
        },
        "DC_TERMINAL": {
            "1Q": None,
            "2Q": None,
            "READOUT": None,
            "IDLE": None,
        },
    }

    if qubit_freq == "TUNABLE":
        # Biasing dissipation is modeled by external resistor components.
        mxc_power["FLUX_BIAS"] = {
            "1Q": None,
            "2Q": None,
            "READOUT": None,
            "IDLE": None,
        }

    if qubit_coupling == "TUNABLE":
        # 2Q gates use the coupler line for tunable-coupling experiments.  The
        # MXC heat is R*I^2, converted to dBm for the existing attenuator model.
        flux_cable_power_mxc_2q = watts_to_dbm(R_MXC * I_2Q**2)
        mxc_power["COUPLER"] = {
            "1Q": None,
            "2Q": flux_cable_power_mxc_2q,
            "READOUT": None,
            "IDLE": None,
        }
        mxc_power["DRIVE"]["2Q"] = None

    return mxc_power


def get_MUX_RATIO(OPERATIONS, DRIVE_MUX, READIN_MUX, READOUT_GROUP_SIZE):
    """Return operation-count correction factors from drive/readout muxing."""
    mux_ratio = {}
    for operation in OPERATIONS:
        mux_ratio[operation] = 1.0

    mux_ratio["1Q"] = 1 / DRIVE_MUX
    mux_ratio["2Q"] = 1 / DRIVE_MUX
    mux_ratio["READOUT"] = 1 / (READIN_MUX * READOUT_GROUP_SIZE)

    return mux_ratio
