import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import yaml
from pathlib import Path
from typing import Any, Dict, List, Union

# Define fontstyles
from matplotlib.font_manager import FontProperties
title_font = FontProperties(family='Arial',size=10, weight='bold')
axis_label_font = FontProperties(family='Arial',size=9, weight='bold')
tick_label_font = FontProperties(family='Arial',size=8, weight='light')
legend_font = FontProperties(family='Arial',size=5, weight='light')
text_font = FontProperties(family='Arial',size=7, weight='light')

fontstyle = [title_font, axis_label_font, tick_label_font, legend_font, text_font]
style_map = {
    # =====================
    # DRIVE (blue family)
    # =====================
    ('DRIVE', 'PASSIVE', 'IDLE'): {'color': '#0072B2', 'hatch': ''},       # base blue
    ('DRIVE', 'ATT', '1Q'):       {'color': '#56B4E9', 'hatch': '++++'},   # light blue
    ('DRIVE', 'ATT', '2Q'):       {'color': '#2C7FB8', 'hatch': '////'},   # mid blue
    ('DRIVE', 'PD', '1Q'):        {'color': '#A6CEE3', 'hatch': '++++'},   # very light blue
    ('DRIVE', 'PD', '2Q'):        {'color': '#6BAED6', 'hatch': '////'},   # light-mid blue

    # =========================
    # FLUX_BIAS (vermillion family)
    # =========================
    ('FLUX_BIAS', 'PASSIVE', 'IDLE'):           {'color': '#D55E00', 'hatch': ''},     # vermillion
    ('FLUX_BIAS', 'BIAS_RESISTOR_4K', 'IDLE'):  {'color': '#F4A582', 'hatch': '...'},  # light vermillion
    ('FLUX_BIAS', 'BIAS_RESISTOR_Still', 'IDLE'):{'color': '#E08214', 'hatch': '...'}, # orange-brown
    ('FLUX_BIAS', 'BIAS_RESISTOR_CP', 'IDLE'):  {'color': '#FDB863', 'hatch': '...'},  # lighter orange
    ('FLUX_BIAS', 'BIAS_RESISTOR_MXC', 'IDLE'): {'color': '#FEE0B6', 'hatch': '...'},  # very light

    # =====================
    # COUPLER (green family)
    # =====================
    ('COUPLER', 'PASSIVE', 'IDLE'):            {'color': '#009E73', 'hatch': ''},      # green
    ('COUPLER', 'RESISTOR_2Q_4K', '2Q'):       {'color': '#66C2A5', 'hatch': '...'},   # light green
    ('COUPLER', 'RESISTOR_2Q_Still', '2Q'):    {'color': '#41AE76', 'hatch': '...'},   # mid green
    ('COUPLER', 'RESISTOR_2Q_CP', '2Q'):       {'color': '#A1D99B', 'hatch': '...'},   # lighter green
    ('COUPLER', 'RESISTOR_2Q_MXC', '2Q'):      {'color': '#C7E9C0', 'hatch': '...'},   # very light green

    # =====================
    # PUMP (orange family)
    # =====================
    ('PUMP', 'PASSIVE', 'IDLE'):   {'color': '#E69F00', 'hatch': ''},      # orange
    ('PUMP', 'ATT', 'READOUT'):    {'color': '#F6C65B', 'hatch': '|||'},   # light orange

    # =============================
    # READOUT_PIN (purple family)
    # =============================
    ('READOUT_PIN', 'PASSIVE', 'IDLE'):  {'color': '#CC79A7', 'hatch': ''},     # purple
    ('READOUT_PIN', 'ATT', 'READOUT'):   {'color': '#E3A6C9', 'hatch': '|||'},  # light purple
    ('READOUT_PIN', 'PD', 'READOUT'):    {'color': '#F1C6DE', 'hatch': '|||'},  # very light purple (keep PD hatch consistent)

    # =============================
    # READOUT_POUT (yellow-brown family)
    # =============================
    ('READOUT_POUT', 'PASSIVE', 'IDLE'): {'color': '#B79F00', 'hatch': ''},     # darker yellow (less glaring than pure yellow)

    # =====================
    # AMP_BIAS (gray family)
    # =====================
    ('AMP_BIAS', 'PASSIVE', 'IDLE'):   {'color': '#4D4D4D', 'hatch': ''},       # dark gray
    ('AMP_BIAS', 'AMP', 'IDLE'):       {'color': '#7F7F7F', 'hatch': 'xxx'},    # mid gray
    ('AMP_BIAS', 'AMP_OHMIC', 'IDLE'): {'color': '#A6A6A6', 'hatch': '...'},    # light gray

    # ==========================
    # AMP_BIAS_50K (brown family)
    # ==========================
    ('AMP_BIAS_50K', 'PASSIVE', 'IDLE'):   {'color': '#8C510A', 'hatch': ''},     # brown
    ('AMP_BIAS_50K', 'AMP', 'IDLE'):      {'color': '#BF812D', 'hatch': 'xxx'},  # light brown
    ('AMP_BIAS_50K', 'AMP_OHMIC', 'IDLE'):{'color': '#DFC27D', 'hatch': '...'},  # pale brown

    # =====================
    # DC_TERMINAL (black-ish neutral)
    # =====================
    ('DC_TERMINAL', 'PASSIVE', 'IDLE'): {'color': '#1A1A1A', 'hatch': ''},       # near-black
}

def get_pq_dict(THL_DF,cooling_power_budget,QUBIT_GROUP_SIZE):
    # Calculate how many qubits are supported at each temperature stage

    # Cooling power at each temperature stage
    cooling_powers = np.array([cooling_power_budget[temp_stage] for temp_stage in ['50K','4K', 'Still', 'CP', 'MXC']])
    
    # Total heat load at each temperature stage
    ALL_DF = THL_DF[['50K', '4K', 'Still', 'CP', 'MXC']].copy()
    ALL_DF.loc["Total"] = ALL_DF.sum()
    total_load = np.array(ALL_DF.loc["Total"].tolist()) # includes heat load due to coupler qubits if any
    
    # No. of qubits supported by each temperature stage
    possible_groups = np.floor(cooling_powers/total_load).astype(int)
    possible_physical_qubits = possible_groups * QUBIT_GROUP_SIZE
    physical_qubits_dict = dict(zip(['50K', '4K', 'Still', 'CP', 'MXC'], possible_physical_qubits))
    print("The number of qubits supported at each temperature stage is:")
    print(physical_qubits_dict)
    
    # Display the bottleneck temperature stage
    bottleneck = min(physical_qubits_dict, key= physical_qubits_dict.get)
    print(f"\nThe bottleneck is at: {bottleneck}")
    
    max_no_of_groups = min(possible_groups)
    max_heat_loads = total_load * max_no_of_groups
    frac_of_cooling_power = np.round(max_heat_loads/cooling_powers * 100, 2)
    frac_of_cooling_power_dict = dict(zip(['50K','4K', 'Still', 'CP', 'MXC'], frac_of_cooling_power))
    
    max_supported_qubits = max_no_of_groups * QUBIT_GROUP_SIZE
    print(f"{max_supported_qubits=}")
    print(frac_of_cooling_power_dict)

    return physical_qubits_dict
    

def plot_heat_load(df_plot, title, config_name, physical_qubits_dict, legend_bbox=(1.0, 1.0)):
    
    # # Change amplifier name and ohmic resistor to generic labels
    # --- Generate new column labels ---
    renamed_labels = [
        (a, 'AMP_OHMIC', c) if a == 'AMP_BIAS' and c == 'IDLE' and 'ohmic' in b.lower()
        else (a, 'PASSIVE', c)  if a == 'AMP_BIAS' and b == 'PASSIVE' and c == 'IDLE'
        else (a, 'AMP', c)  if a == 'AMP_BIAS' and c == 'IDLE'
        else (a, b, c)
        for a, b, c in df_plot.columns
    ]
    
    # --- Apply the renamed columns to df_plot ---
    df_plot.columns = pd.MultiIndex.from_tuples(renamed_labels, names=df_plot.columns.names)

    renamed_labels = [
        (a, 'AMP_OHMIC', c) if a == 'AMP_BIAS_50K' and c == 'IDLE' and 'ohmic' in b.lower()
        else (a, 'PASSIVE', c)  if a == 'AMP_BIAS_50K' and b == 'PASSIVE' and c == 'IDLE'
        else (a, 'AMP', c)  if a == 'AMP_BIAS_50K' and c == 'IDLE'
        else (a, b, c)
        for a, b, c in df_plot.columns
    ]
    
    # --- Apply the renamed columns to df_plot ---
    df_plot.columns = pd.MultiIndex.from_tuples(renamed_labels, names=df_plot.columns.names)
    
    # 1) Decide the plotting order of stacks (columns)
    # Reorder columns: PASSIVE first
    original_columns = df_plot.columns.tolist()
    passive_cols = [col for col in df_plot.columns if col[1] == 'PASSIVE']
    active_cols  = [col for col in df_plot.columns if col[1] != 'PASSIVE']
    reordered_columns = passive_cols + active_cols
    
    # Reorder df_plot accordingly
    df_plot = df_plot[reordered_columns].copy()
    cols = list(df_plot.columns)
    
    # Index: temperature stages (e.g., "4K", "Still", "CP", "MXC")
    # Columns: MultiIndex with levels (Cable, Component, Operation)
    
    # 2) (Optional but helpful) ensure the columns are a proper 3-level MultiIndex
    # If they already are, this does nothing.
    if not isinstance(df_plot.columns, pd.MultiIndex) or df_plot.columns.nlevels != 3:
        raise ValueError("dataframe columns must be a 3-level MultiIndex: (Cable, Component, Operation)")
        
    # 4) Define fallbacks (only used if a stack tuple isn’t in style_map)
    # fallback_colors = plt.cm.tab20.colors  # a nice, long qualitative palette
    # fallback_hatches = ['/', '\\', 'x', '-', '+', 'o', 'O', '.', '*']  # repeats cyclically
    fallback_color = 'white' 
    fallback_hatch = '//'   
    
    # 5) X positions and labels (temperature stages)
    x = np.arange(len(df_plot.index))
    # xticklabels = df_plot.index.astype(str)
    # xticklabels = ["4K", "Still (1K)", "CP (100 mK)", "MXC (10 mK)" ]
    xticklabels = ["50K", "4K", "Still", "CP", "MXC" ]
    
    # 6) Create the figure/axes
    # IEEE TQE Guidelines
    # Single column: 3.5" (wide) x 8.5" (height)
    # Double column: 7.16" (wide) x 8.5" (height)
    fig, ax = plt.subplots(figsize=(7.16, 3))
    
    # 7) Build the stacked bars
    bottom = np.zeros(len(x), dtype=float)
    
    for i, col in enumerate(cols):
        values = df_plot[col].astype(float).values
    
        # pull style from style_map if present, else fallback
        style = style_map.get(col, {})
        color = style.get('color', fallback_color)
        hatch = style.get('hatch', fallback_hatch)
    
        # readable label in legend
        label = f"{col[0]} | {col[1]} | {col[2]}"
    
        bars = ax.bar(
            x,
            values,
            bottom=bottom,
            label=label,
            color=color,
            edgecolor='black',
            linewidth=0.4
        )
        # apply hatch to each rectangle
        for b in bars:
            b.set_hatch(hatch)
    
        bottom += values  # update stack baseline

    # Display no. of supported qubits on top of the bar
    possible_physical_qubits = list(physical_qubits_dict.values())
    totals = df_plot.sum(axis=1)  # Sum over column. Get bar height
    for i, total in enumerate(totals):
        ax.text(i, total, f'{possible_physical_qubits[i]}', ha='center', va='bottom', fontproperties=text_font)
    
    # Draw horizantal line at y=1
    ax.axhline(y=1, color='k', linestyle='--',linewidth=0.6)
    
    # 8) Axis cosmetics
    # Set titles 
    ax.set_title(title, fontproperties=title_font)
    ax.set_xlabel("Temperature Stage", fontproperties=axis_label_font)
    ax.set_ylabel("Normalized Heat Load", fontproperties=axis_label_font)
    ax.set_xticks(x)
    ax.set_xticklabels(xticklabels, fontproperties=tick_label_font, rotation=0)
    for label in ax.get_yticklabels() :
        label.set_fontproperties(tick_label_font)
    ax.set_ylim(0, 1.1) # Set max y-value to be slightly higher than the tallest bar
    
    # 9) Legend: shrink and place outside
    ax.legend(ncol=1, 
              bbox_to_anchor=legend_bbox, 
              loc='upper left',
              prop=legend_font,
              frameon=False,
              borderaxespad=0.)
    
    ax.margins(x=0.02)
    plt.tight_layout()
    plt.savefig(f"./{config_name}_THL.png",dpi=600)
    plt.show()

    # Save plot dataframe as pickle file
    df_plot_saved = df_plot.copy()
    df_plot_saved["Total"] = totals
    df_plot_saved.to_pickle(config_name + ".pkl")

    # Save no. of physical qubits as pickle file
    df_pq = pd.DataFrame([physical_qubits_dict], index=["PQ"])
    df_pq.to_pickle("PQ_"+config_name+".pkl")

    # Return the plot dataframe
    return df_plot_saved

#######################################################################

def df_float_formatter(x):
    if x in (0, 0.0, None) or pd.isna(x):
        return " "
    return f"{x:.2e}" if isinstance(x, float) else str(x)

def df_int_formatter(x):
    if x in (0, 0.0, None) or pd.isna(x):
        return " "
    return f"{int(round(x))}"

def _process_commas_recursively(obj: Any) -> Any:
    """
    Recursively convert comma-separated strings into lists.
    Leaves None, numbers, and bools as-is; trims whitespace on strings.
    """
    if isinstance(obj, dict):
        return {k: _process_commas_recursively(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_process_commas_recursively(v) for v in obj]
    if isinstance(obj, str):
        s = obj.strip()
        if "," in s:
            parts = [p.strip() for p in s.split(",")]
            # Only treat as list if there are at least 2 non-empty items
            if sum(1 for p in parts if p != "") > 1:
                return parts
        return s
    return obj

def load_config(config_file: str|Path) -> dict:
    """
    Load a YAML config file, then recursively convert comma-separated
    strings into lists (e.g., 'A, B' -> ['A', 'B']). YAML null -> None.
    """
    path = Path(config_file)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return _process_commas_recursively(data)


def check_activation_matrix(activation_matrix, operations):
    """
    Checks that every operation specified in the activation_matrix exists in the operations list.
    
    Parameters:
        activation_matrix (dict): Dictionary whose values are lists of operations.
        operations (list): List of allowed operations.
    
    Returns:
        bool: True if all operations are valid, otherwise raises a ValueError.
        
    Raises:
        ValueError: If any operation in the activation matrix is not in the allowed operations.
    """
    missing_ops = []  # To collect any invalid operation along with its key.
    
    # Iterate through each key and its associated list of operations.
    for cable, op_list in activation_matrix.items():
        for op in op_list:
            if op not in operations:
                missing_ops.append((cable, op))
    
    if missing_ops:
        error_message = "Error: The following operations are not allowed:\n"
        for cable, op in missing_ops:
            error_message += f" - Operation '{op}' found in '{cable}' is not in allowed list {operations}\n"
        raise ValueError(error_message)
    
    return True


def watts_to_dbm(power_watts):
    # Avoid taking log of zero or negative numbers by setting them to NaN
    if power_watts <= 0:
        return np.nan
    return 10 * np.log10(power_watts * 1000)

def dBm2Watts(dBm):
    """
    Converts dBm to Watts

    Parameters
    ----------
    dBm: Power in dBm

    Returns
    -------
    Equivalent power in Watts
    """

    if dBm is not None:
        return 10 ** ((dBm-30)/10)
    else:
        return 0

    
# def get_OPERATION_COUNTS(OPERATIONS, QUBIT_TYPES, WORKLOAD):
#     OPERATIONS_Spec= WORKLOAD["OPERATIONS_Spec"]
    
#     # Workload requires a certain number of qubits.
#     # Given the system qubit size, calculate the number of qubit groups
#     no_of_groups = {}
#     for qubit_type in ["DATA", "ANCILLA"]:
#         no_of_groups[qubit_type] = QUBIT_TYPES[qubit_type]/WORKLOAD[qubit_type]
#         if not no_of_groups[qubit_type].is_integer():
#             error_message = f"Number of Qubit Groups = {no_of_groups[qubit_type]} is not an integer."
#             raise ValueError(error_message)
    
#     # Calculate the different types of operations and the total number of operations for a given workload
#     OPERATION_COUNTS = {}
#     for qubit_type, count_dict in OPERATIONS_Spec.items():
#         OPERATION_COUNTS[qubit_type] = {}
#         for operation, operation_count in count_dict.items():
#             OPERATION_COUNTS[qubit_type][operation] = operation_count * no_of_groups[qubit_type]
    
#     # Sum the subkey values into a new dictionary
#     total_operations = {}
#     for operation in OPERATIONS:
#         total_operations[operation] = 0
#         for qubit_type in OPERATION_COUNTS.keys():
#             total_operations[operation] = total_operations[operation] + OPERATION_COUNTS[qubit_type][operation]
    
#     if "COUPLER" in QUBIT_TYPES:
#         OPERATION_COUNTS["COUPLER"] = {}
#         for op in OPERATIONS:
#             OPERATION_COUNTS["COUPLER"][op] = 0.0
#         OPERATION_COUNTS["COUPLER"]["2Q"] = OPERATION_COUNTS["DATA"]["2Q"] + OPERATION_COUNTS["ANCILLA"]["2Q"] 
    
#     OPERATION_COUNTS["TOTAL"] = total_operations
#     return OPERATION_COUNTS


# def get_DUTY_CYCLES(OPERATIONS, OPERATION_COUNTS, LATENCY, QUBIT_TYPES):
#     # Check that OPERATION_COUNTS has the same or subset of keys in the first level as QUBIT_TYPES
#     if set(OPERATION_COUNTS.keys()) <= set(QUBIT_TYPES.keys()):
#         raise ValueError(
#             f"Top-level keys mismatch:\n"
#             f"OPERATION_COUNTS keys: {set(OPERATION_COUNTS.keys())}\n"
#             f"QUBIT_TYPES keys: {set(QUBIT_TYPES.keys())}"
#         )
    
#     # Check that OPERATION_COUNTS has the same keys in the second level as OPERATIONS
#     expected_op_keys = set(OPERATIONS)
    
#     for label, op_dict in OPERATION_COUNTS.items():
#         if set(op_dict.keys()) != expected_op_keys:
#             raise ValueError(
#                 f"Second-level keys mismatch for '{label}':\n"
#                 f"Expected: {expected_op_keys}\n"
#                 f"Found: {set(op_dict.keys())}"
#             )

#     # First compute each qubit type’s duty cycles
#     OPERATION_DUTY_CYCLES = {}
#     for qubit_type, operation_count_dict in OPERATION_COUNTS.items():
#         OPERATION_DUTY_CYCLES[qubit_type] = {}
#         for operation, count in operation_count_dict.items():
#             OPERATION_DUTY_CYCLES[qubit_type][operation] = OPERATION_COUNTS[qubit_type][operation] * LATENCY[operation] / LATENCY["TOTAL"]

#     # Then do a weighted average based on how many data vs. ancilla qubits
#     AVG_OPERATION_DUTY_CYCLES = {
#         op: np.average(
#             [OPERATION_DUTY_CYCLES[qtype][op] for qtype in QUBIT_TYPES],
#             weights=[QUBIT_TYPES[qtype] for qtype in QUBIT_TYPES]
#         )
#         for op in OPERATIONS
#     }

#     return OPERATION_DUTY_CYCLES, AVG_OPERATION_DUTY_CYCLES

