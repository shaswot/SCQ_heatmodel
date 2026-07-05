"""MXC power constants and selection helpers for experiment configuration.

The notebook-level configure API only needs operation powers at the mixing
chamber.  Keeping these constants here avoids copying drive/readout/pump power
values into every experiment folder.
"""

READOUT_PIN_POWER_MXC = -120  # dBm, 1.00e-15 W
PUMP_POWER_MXC = -55  # dBm, 3.16e-09 W

# The historical configure.py files mostly use the default drive powers.  The
# MXC_81 profile keeps the one existing lower-power variant explicit without
# putting the numeric constants back into an experiment-local configure.py.
DRIVE_POWER_PROFILES = {
    "DEFAULT": {
        "1Q": -71,
        "2Q": -66,
    },
    "MXC_81": {
        "1Q": -86,
        "2Q": -81,
    },
}

# Current experiments only exercise FIXED/FIXED and TUNABLE/TUNABLE, but the
# explicit topology map makes the intended qubit-frequency/coupling dependency
# visible and gives future mixed-topology experiments one place to change.
DRIVE_POWER_PROFILE_BY_QUBIT_CONFIG = {
    ("FIXED", "FIXED"): "DEFAULT",
    ("FIXED", "TUNABLE"): "DEFAULT",
    ("TUNABLE", "FIXED"): "DEFAULT",
    ("TUNABLE", "TUNABLE"): "DEFAULT",
}


def _normalize_qubit_config(value, field_name):
    """Normalize YAML strings and fail early on misspelled qubit settings."""
    normalized = str(value).strip().upper()
    if normalized not in {"FIXED", "TUNABLE"}:
        raise ValueError(f"{field_name} must be 'FIXED' or 'TUNABLE', got {value!r}")
    return normalized


def _normalize_profile(profile):
    """Return a canonical drive-power profile name."""
    normalized = str(profile).strip().upper()
    if normalized not in DRIVE_POWER_PROFILES:
        known_profiles = ", ".join(sorted(DRIVE_POWER_PROFILES))
        raise ValueError(
            f"Unknown DRIVE_POWER_PROFILE {profile!r}; expected one of {known_profiles}"
        )
    return normalized


def select_drive_power(QUBIT_FREQ, QUBIT_COUPLING, DRIVE_POWER_PROFILE=None):
    """Select 1Q/2Q drive powers for a qubit topology.

    DRIVE_POWER_PROFILE is optional and should only be used when two experiments
    have the same qubit topology but intentionally use different drive powers.
    The existing pd_MXC_81 experiment is such a case.
    """
    if DRIVE_POWER_PROFILE is not None:
        profile = _normalize_profile(DRIVE_POWER_PROFILE)
    else:
        qubit_freq = _normalize_qubit_config(QUBIT_FREQ, "QUBIT_FREQ")
        qubit_coupling = _normalize_qubit_config(QUBIT_COUPLING, "QUBIT_COUPLING")
        profile = DRIVE_POWER_PROFILE_BY_QUBIT_CONFIG[(qubit_freq, qubit_coupling)]

    # Return a copy so callers can safely set DRIVE["2Q"] to None for tunable
    # couplers without mutating the central profile table.
    return dict(DRIVE_POWER_PROFILES[profile])
