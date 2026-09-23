"""
ThunAI Engineering Tools
========================

Local engineering, scientific calculation,
data analysis and visualization tools.

Designed to be connected to LangGraph + Qwen.

All calculations run locally.
No external API is required.
"""

import ast
import math
import operator
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
from langchain_core.tools import tool


# ============================================================
# 1. SAFE CALCULATOR
# ============================================================

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "fabs": math.fabs,
    "factorial": math.factorial,
    "ceil": math.ceil,
    "floor": math.floor,
    "degrees": math.degrees,
    "radians": math.radians,
    "abs": abs,
}

_ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def _evaluate(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numerical constants are allowed.")

    if isinstance(node, ast.BinOp):

        operation = type(node.op)

        if operation not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return _ALLOWED_OPERATORS[operation](left, right)

    if isinstance(node, ast.UnaryOp):

        operation = type(node.op)

        if operation not in _ALLOWED_OPERATORS:
            raise ValueError("Unary operator not allowed.")

        operand = _evaluate(node.operand)

        return _ALLOWED_OPERATORS[operation](operand)

    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function.")

        name = node.func.id

        if name not in _ALLOWED_FUNCTIONS:
            raise ValueError(
                f"Function '{name}' is not allowed."
            )

        arguments = [
            _evaluate(argument)
            for argument in node.args
        ]

        return _ALLOWED_FUNCTIONS[name](*arguments)

    if isinstance(node, ast.Name):

        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]

        raise ValueError(
            f"Variable '{node.id}' is not allowed."
        )

    raise ValueError(
        f"Expression '{type(node).__name__}' is not allowed."
    )


@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical and scientific calculations.

    Examples:
    sqrt(450**2 + 300**2)
    25 * 17
    sin(pi / 2)
    log10(1000)
    2**10
    """

    try:

        if len(expression) > 500:
            return "Error: expression is too long."

        tree = ast.parse(expression, mode="eval")

        result = _evaluate(tree.body)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)

    except ZeroDivisionError:
        return "Error: division by zero."

    except Exception as e:
        return f"Calculation error: {e}"


# ============================================================
# 2. UNIT CONVERSION
# ============================================================

@tool
def unit_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> str:
    """
    Convert common engineering units.

    Supported:
    temperature: C, F, K
    pressure: Pa, kPa, MPa, bar, atm, psi
    length: m, cm, mm, km, ft, inch
    mass: kg, g, tonne, lb
    volume: m3, L, mL, ft3
    flow: m3/s, L/s, L/min
    energy: J, kJ, MJ, Wh, kWh
    power: W, kW, MW
    """

    f = from_unit.lower().strip()
    t = to_unit.lower().strip()

    try:

        # ---------------- TEMPERATURE ----------------

        if f in ["c", "°c", "celsius"]:

            celsius = value

        elif f in ["f", "°f", "fahrenheit"]:

            celsius = (value - 32) * 5 / 9

        elif f in ["k", "kelvin"]:

            celsius = value - 273.15

        else:
            celsius = None

        if celsius is not None:

            if t in ["c", "°c", "celsius"]:
                return str(celsius)

            if t in ["f", "°f", "fahrenheit"]:
                return str(celsius * 9 / 5 + 32)

            if t in ["k", "kelvin"]:
                return str(celsius + 273.15)

        # ---------------- PRESSURE ----------------

        pressure = {
            "pa": 1,
            "kpa": 1000,
            "mpa": 1_000_000,
            "bar": 100_000,
            "atm": 101325,
            "psi": 6894.757
        }

        if f in pressure and t in pressure:

            pa = value * pressure[f]

            return str(pa / pressure[t])

        # ---------------- LENGTH ----------------

        length = {
            "m": 1,
            "cm": 0.01,
            "mm": 0.001,
            "km": 1000,
            "ft": 0.3048,
            "inch": 0.0254
        }

        if f in length and t in length:

            meters = value * length[f]

            return str(meters / length[t])

        # ---------------- MASS ----------------

        mass = {
            "kg": 1,
            "g": 0.001,
            "tonne": 1000,
            "lb": 0.453592
        }

        if f in mass and t in mass:

            kg = value * mass[f]

            return str(kg / mass[t])

        # ---------------- VOLUME ----------------

        volume = {
            "m3": 1,
            "l": 0.001,
            "ml": 0.000001,
            "ft3": 0.0283168
        }

        if f in volume and t in volume:

            m3 = value * volume[f]

            return str(m3 / volume[t])

        # ---------------- POWER ----------------

        power = {
            "w": 1,
            "kw": 1000,
            "mw": 1_000_000
        }

        if f in power and t in power:

            watts = value * power[f]

            return str(watts / power[t])

        # ---------------- ENERGY ----------------

        energy = {
            "j": 1,
            "kj": 1000,
            "mj": 1_000_000,
            "wh": 3600,
            "kwh": 3_600_000
        }

        if f in energy and t in energy:

            joules = value * energy[f]

            return str(joules / energy[t])

        return (
            f"Conversion from '{from_unit}' "
            f"to '{to_unit}' is not supported."
        )

    except Exception as e:

        return f"Conversion error: {e}"


# ============================================================
# 3. FLUID MECHANICS
# ============================================================

@tool
def reynolds_number(
    density: float,
    velocity: float,
    diameter: float,
    viscosity: float
) -> str:
    """
    Calculate Reynolds number.

    Re = rho * V * D / mu
    """

    try:

        Re = (
            density
            * velocity
            * diameter
            / viscosity
        )

        if Re < 2300:
            regime = "approximately laminar"

        elif Re < 4000:
            regime = "approximately transitional"

        else:
            regime = "approximately turbulent"

        return (
            f"Reynolds number = {Re:.6g}\n"
            f"Flow regime = {regime}"
        )

    except Exception as e:

        return f"Reynolds calculation error: {e}"


@tool
def pressure_drop_darcy(
    friction_factor: float,
    length: float,
    diameter: float,
    density: float,
    velocity: float
) -> str:
    """
    Calculate pressure drop using Darcy-Weisbach.

    Delta P = f * (L/D) * rho*V²/2
    """

    try:

        delta_p = (
            friction_factor
            * (length / diameter)
            * density
            * velocity ** 2
            / 2
        )

        return (
            f"Pressure drop = {delta_p:.6g} Pa\n"
            f"Pressure drop = {delta_p / 100000:.6g} bar"
        )

    except Exception as e:

        return f"Pressure-drop calculation error: {e}"


@tool
def fluid_velocity(
    flow_rate: float,
    diameter: float
) -> str:
    """
    Calculate fluid velocity from volumetric flow rate.

    V = Q / A
    """

    try:

        area = math.pi * diameter ** 2 / 4

        velocity = flow_rate / area

        return (
            f"Pipe area = {area:.6g} m²\n"
            f"Velocity = {velocity:.6g} m/s"
        )

    except Exception as e:

        return f"Velocity calculation error: {e}"


# ============================================================
# 4. HEAT TRANSFER
# ============================================================

@tool
def heat_transfer(
    mass_flow_rate: float,
    specific_heat: float,
    delta_temperature: float
) -> str:
    """
    Calculate sensible heat-transfer rate.

    Q = m_dot * Cp * DeltaT
    """

    try:

        Q = (
            mass_flow_rate
            * specific_heat
            * delta_temperature
        )

        return (
            f"Heat transfer rate = {Q:.6g} W\n"
            f"Heat transfer rate = {Q / 1000:.6g} kW"
        )

    except Exception as e:

        return f"Heat-transfer calculation error: {e}"


@tool
def heat_exchanger_duty(
    overall_heat_transfer_coefficient: float,
    area: float,
    lmtd: float
) -> str:
    """
    Calculate heat exchanger duty.

    Q = U * A * LMTD
    """

    try:

        Q = (
            overall_heat_transfer_coefficient
            * area
            * lmtd
        )

        return (
            f"Heat exchanger duty = {Q:.6g} W\n"
            f"Duty = {Q / 1000:.6g} kW"
        )

    except Exception as e:

        return f"Heat-exchanger calculation error: {e}"


# ============================================================
# 5. THERMODYNAMICS
# ============================================================

@tool
def ideal_gas_pressure(
    moles: float,
    temperature: float,
    volume: float
) -> str:
    """
    Calculate ideal-gas pressure.

    P = nRT/V

    Temperature in K.
    Volume in m³.
    """

    try:

        R = 8.314462618

        pressure = (
            moles
            * R
            * temperature
            / volume
        )

        return (
            f"Pressure = {pressure:.6g} Pa\n"
            f"Pressure = {pressure / 100000:.6g} bar"
        )

    except Exception as e:

        return f"Thermodynamic calculation error: {e}"


@tool
def ideal_gas_temperature(
    pressure: float,
    volume: float,
    moles: float
) -> str:
    """
    Calculate ideal-gas temperature.

    T = PV/(nR)

    Pressure in Pa.
    Volume in m³.
    """

    try:

        R = 8.314462618

        temperature = (
            pressure
            * volume
            / (moles * R)
        )

        return f"Temperature = {temperature:.6g} K"

    except Exception as e:

        return f"Thermodynamic calculation error: {e}"


# ============================================================
# 6. PROCESS CALCULATIONS
# ============================================================

@tool
def mass_flow_rate(
    density: float,
    volumetric_flow_rate: float
) -> str:
    """
    Calculate mass flow rate.

    m_dot = rho * Q
    """

    try:

        result = density * volumetric_flow_rate

        return f"Mass flow rate = {result:.6g} kg/s"

    except Exception as e:

        return f"Process calculation error: {e}"


@tool
def residence_time(
    volume: float,
    volumetric_flow_rate: float
) -> str:
    """
    Calculate residence time.

    tau = V/Q
    """

    try:

        tau = volume / volumetric_flow_rate

        return (
            f"Residence time = {tau:.6g} s\n"
            f"Residence time = {tau / 60:.6g} min"
        )

    except Exception as e:

        return f"Residence-time calculation error: {e}"


@tool
def concentration_dilution(
    initial_concentration: float,
    initial_volume: float,
    final_volume: float
) -> str:
    """
    Calculate final concentration using C1V1 = C2V2.
    """

    try:

        final_concentration = (
            initial_concentration
            * initial_volume
            / final_volume
        )

        return (
            f"Final concentration = "
            f"{final_concentration:.6g}"
        )

    except Exception as e:

        return f"Dilution calculation error: {e}"


# ============================================================
# 7. EQUIPMENT CALCULATIONS
# ============================================================

@tool
def cylindrical_tank_volume(
    diameter: float,
    height: float
) -> str:
    """
    Calculate volume of a cylindrical tank.

    V = pi * D² / 4 * H
    """

    try:

        volume = (
            math.pi
            * diameter ** 2
            / 4
            * height
        )

        return (
            f"Tank volume = {volume:.6g} m³\n"
            f"Tank volume = {volume * 1000:.6g} L"
        )

    except Exception as e:

        return f"Equipment calculation error: {e}"


@tool
def pipe_area(
    diameter: float
) -> str:
    """
    Calculate internal cross-sectional area of a circular pipe.
    """

    try:

        area = math.pi * diameter ** 2 / 4

        return f"Pipe area = {area:.6g} m²"

    except Exception as e:

        return f"Equipment calculation error: {e}"


# ============================================================
# 8. STATISTICS
# ============================================================

@tool
def statistical_analysis(
    values: str
) -> str:
    """
    Perform statistical analysis on comma-separated data.

    Returns:
    count
    mean
    median
    standard deviation
    variance
    minimum
    maximum
    range
    """

    try:

        data = np.array(
            [
                float(x.strip())
                for x in values.split(",")
            ]
        )

        if len(data) == 0:
            return "No data supplied."

        result = {
            "count": int(len(data)),
            "mean": float(np.mean(data)),
            "median": float(np.median(data)),
            "standard_deviation": float(np.std(data)),
            "variance": float(np.var(data)),
            "minimum": float(np.min(data)),
            "maximum": float(np.max(data)),
            "range": float(np.max(data) - np.min(data))
        }

        return str(result)

    except Exception as e:

        return f"Statistical analysis error: {e}"


@tool
def correlation_analysis(
    x_values: str,
    y_values: str
) -> str:
    """
    Calculate Pearson correlation between two datasets.
    """

    try:

        x = np.array(
            [float(v.strip()) for v in x_values.split(",")]
        )

        y = np.array(
            [float(v.strip()) for v in y_values.split(",")]
        )

        if len(x) != len(y):
            return "Error: datasets must have equal length."

        correlation, p_value = stats.pearsonr(x, y)

        return (
            f"Pearson correlation = {correlation:.6f}\n"
            f"P-value = {p_value:.6g}"
        )

    except Exception as e:

        return f"Correlation analysis error: {e}"


@tool
def linear_regression(
    x_values: str,
    y_values: str
) -> str:
    """
    Perform simple linear regression.

    Returns slope, intercept, R² and p-value.
    """

    try:

        x = np.array(
            [float(v.strip()) for v in x_values.split(",")]
        )

        y = np.array(
            [float(v.strip()) for v in y_values.split(",")]
        )

        if len(x) != len(y):
            return "Error: datasets must have equal length."

        result = stats.linregress(x, y)

        return (
            f"Slope = {result.slope:.6g}\n"
            f"Intercept = {result.intercept:.6g}\n"
            f"R² = {result.rvalue ** 2:.6g}\n"
            f"P-value = {result.pvalue:.6g}"
        )

    except Exception as e:

        return f"Regression error: {e}"


# ============================================================
# 9. DATAFRAME / CSV ANALYSIS
# ============================================================

@tool
def analyze_csv(
    file_path: str
) -> str:
    """
    Analyze a local CSV file.

    Returns:
    - rows
    - columns
    - column names
    - numerical summary
    """

    try:

        path = Path(file_path)

        if not path.exists():
            return f"File not found: {file_path}"

        df = pd.read_csv(path)

        result = {
            "rows": len(df),
            "columns": list(df.columns),
            "data_types": df.dtypes.astype(str).to_dict(),
            "summary": df.describe(
                include="all"
            ).to_string()
        }

        return str(result)

    except Exception as e:

        return f"CSV analysis error: {e}"


@tool
def analyze_excel(
    file_path: str,
    sheet_name: str = "Sheet1"
) -> str:
    """
    Analyze a local Excel spreadsheet.
    """

    try:

        path = Path(file_path)

        if not path.exists():
            return f"File not found: {file_path}"

        df = pd.read_excel(
            path,
            sheet_name=sheet_name
        )

        return (
            f"Rows: {len(df)}\n"
            f"Columns: {list(df.columns)}\n\n"
            f"Statistics:\n"
            f"{df.describe().to_string()}"
        )

    except Exception as e:

        return f"Excel analysis error: {e}"


# ============================================================
# 10. DATA FILTERING / AGGREGATION
# ============================================================

@tool
def dataframe_summary(
    file_path: str
) -> str:
    """
    Generate a concise summary of a CSV dataset.
    """

    try:

        df = pd.read_csv(file_path)

        result = []

        result.append(f"Rows: {len(df)}")
        result.append(f"Columns: {len(df.columns)}")
        result.append(
            f"Column names: {list(df.columns)}"
        )

        numeric = df.select_dtypes(
            include=np.number
        )

        if not numeric.empty:

            result.append(
                "\nNumerical statistics:"
            )

            result.append(
                numeric.describe().to_string()
            )

        return "\n".join(result)

    except Exception as e:

        return f"Dataframe analysis error: {e}"


# ============================================================
# 11. VISUALIZATION
# ============================================================

def _create_output_directory():

    directory = Path("generated_charts")

    directory.mkdir(
        exist_ok=True
    )

    return directory


@tool
def create_bar_chart(
    categories: str,
    values: str,
    title: str = "Bar Chart"
) -> str:
    """
    Create a bar chart.

    categories:
        comma-separated labels

    values:
        comma-separated numerical values
    """

    try:

        category_list = [
            x.strip()
            for x in categories.split(",")
        ]

        value_list = [
            float(x.strip())
            for x in values.split(",")
        ]

        if len(category_list) != len(value_list):
            return (
                "Error: categories and values "
                "must have the same length."
            )

        directory = _create_output_directory()

        filename = directory / "bar_chart.png"

        plt.figure()

        plt.bar(
            category_list,
            value_list
        )

        plt.xlabel("Category")
        plt.ylabel("Value")
        plt.title(title)

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        plt.savefig(filename)

        plt.close()

        return f"Bar chart created: {filename}"

    except Exception as e:

        return f"Bar-chart error: {e}"


@tool
def create_line_chart(
    x_values: str,
    y_values: str,
    title: str = "Line Chart"
) -> str:
    """
    Create a line chart.
    """

    try:

        x = [
            x.strip()
            for x in x_values.split(",")
        ]

        y = [
            float(v.strip())
            for v in y_values.split(",")
        ]

        if len(x) != len(y):
            return "Error: x and y must have equal length."

        directory = _create_output_directory()

        filename = directory / "line_chart.png"

        plt.figure()

        plt.plot(
            x,
            y,
            marker="o"
        )

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(title)

        plt.tight_layout()

        plt.savefig(filename)

        plt.close()

        return f"Line chart created: {filename}"

    except Exception as e:

        return f"Line-chart error: {e}"


@tool
def create_pie_chart(
    categories: str,
    values: str,
    title: str = "Pie Chart"
) -> str:
    """
    Create a pie chart.
    """

    try:

        category_list = [
            x.strip()
            for x in categories.split(",")
        ]

        value_list = [
            float(x.strip())
            for x in values.split(",")
        ]

        if len(category_list) != len(value_list):
            return (
                "Error: categories and values "
                "must have the same length."
            )

        directory = _create_output_directory()

        filename = directory / "pie_chart.png"

        plt.figure()

        plt.pie(
            value_list,
            labels=category_list,
            autopct="%1.1f%%"
        )

        plt.title(title)

        plt.tight_layout()

        plt.savefig(filename)

        plt.close()

        return f"Pie chart created: {filename}"

    except Exception as e:

        return f"Pie-chart error: {e}"


@tool
def create_scatter_plot(
    x_values: str,
    y_values: str,
    title: str = "Scatter Plot"
) -> str:
    """
    Create a scatter plot for two numerical variables.
    """

    try:

        x = np.array(
            [
                float(v.strip())
                for v in x_values.split(",")
            ]
        )

        y = np.array(
            [
                float(v.strip())
                for v in y_values.split(",")
            ]
        )

        if len(x) != len(y):
            return "Error: x and y must have equal length."

        directory = _create_output_directory()

        filename = directory / "scatter_plot.png"

        plt.figure()

        plt.scatter(
            x,
            y
        )

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(title)

        plt.tight_layout()

        plt.savefig(filename)

        plt.close()

        return f"Scatter plot created: {filename}"

    except Exception as e:

        return f"Scatter-plot error: {e}"


@tool
def create_histogram(
    values: str,
    title: str = "Histogram"
) -> str:
    """
    Create a histogram for numerical data.
    """

    try:

        data = np.array(
            [
                float(v.strip())
                for v in values.split(",")
            ]
        )

        directory = _create_output_directory()

        filename = directory / "histogram.png"

        plt.figure()

        plt.hist(data)

        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.title(title)

        plt.tight_layout()

        plt.savefig(filename)

        plt.close()

        return f"Histogram created: {filename}"

    except Exception as e:

        return f"Histogram error: {e}"


# ============================================================
# 12. ALL TOOLS
# ============================================================

tools = [

    # Calculator
    calculator,

    # Units
    unit_conversion,

    # Fluid mechanics
    reynolds_number,
    pressure_drop_darcy,
    fluid_velocity,

    # Heat transfer
    heat_transfer,
    heat_exchanger_duty,

    # Thermodynamics
    ideal_gas_pressure,
    ideal_gas_temperature,

    # Process calculations
    mass_flow_rate,
    residence_time,
    concentration_dilution,

    # Equipment
    cylindrical_tank_volume,
    pipe_area,

    # Statistics
    statistical_analysis,
    correlation_analysis,
    linear_regression,

    # Data analysis
    analyze_csv,
    analyze_excel,
    dataframe_summary,

    # Visualization
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_scatter_plot,
    create_histogram,
]