from tools import *


print("\n==============================")
print("1. CALCULATOR")
print("==============================")

print(
    calculator.invoke("sqrt(450**2 + 300**2)")
)


print("\n==============================")
print("2. UNIT CONVERSION")
print("==============================")

print(
    unit_conversion.invoke({
        "value": 100,
        "from_unit": "C",
        "to_unit": "F"
    })
)


print("\n==============================")
print("3. REYNOLDS NUMBER")
print("==============================")

print(
    reynolds_number.invoke({
        "density": 1000,
        "velocity": 2,
        "diameter": 0.1,
        "viscosity": 0.001
    })
)


print("\n==============================")
print("4. PRESSURE DROP")
print("==============================")

print(
    pressure_drop_darcy.invoke({
        "friction_factor": 0.02,
        "length": 100,
        "diameter": 0.1,
        "density": 1000,
        "velocity": 2
    })
)


print("\n==============================")
print("5. FLUID VELOCITY")
print("==============================")

print(
    fluid_velocity.invoke({
        "flow_rate": 0.01,
        "diameter": 0.1
    })
)


print("\n==============================")
print("6. HEAT TRANSFER")
print("==============================")

print(
    heat_transfer.invoke({
        "mass_flow_rate": 2,
        "specific_heat": 4186,
        "delta_temperature": 20
    })
)


print("\n==============================")
print("7. HEAT EXCHANGER")
print("==============================")

print(
    heat_exchanger_duty.invoke({
        "overall_heat_transfer_coefficient": 500,
        "area": 20,
        "lmtd": 30
    })
)


print("\n==============================")
print("8. IDEAL GAS PRESSURE")
print("==============================")

print(
    ideal_gas_pressure.invoke({
        "moles": 10,
        "temperature": 300,
        "volume": 1
    })
)


print("\n==============================")
print("9. IDEAL GAS TEMPERATURE")
print("==============================")

print(
    ideal_gas_temperature.invoke({
        "pressure": 101325,
        "volume": 1,
        "moles": 40
    })
)


print("\n==============================")
print("10. MASS FLOW RATE")
print("==============================")

print(
    mass_flow_rate.invoke({
        "density": 850,
        "volumetric_flow_rate": 0.02
    })
)


print("\n==============================")
print("11. RESIDENCE TIME")
print("==============================")

print(
    residence_time.invoke({
        "volume": 50,
        "volumetric_flow_rate": 0.5
    })
)


print("\n==============================")
print("12. DILUTION")
print("==============================")

print(
    concentration_dilution.invoke({
        "initial_concentration": 10,
        "initial_volume": 2,
        "final_volume": 10
    })
)


print("\n==============================")
print("13. TANK VOLUME")
print("==============================")

print(
    cylindrical_tank_volume.invoke({
        "diameter": 4,
        "height": 10
    })
)


print("\n==============================")
print("14. PIPE AREA")
print("==============================")

print(
    pipe_area.invoke({
        "diameter": 0.2
    })
)


print("\n==============================")
print("15. STATISTICS")
print("==============================")

print(
    statistical_analysis.invoke(
        "10,20,30,40,50,60,70"
    )
)


print("\n==============================")
print("16. CORRELATION")
print("==============================")

print(
    correlation_analysis.invoke({
        "x_values": "1,2,3,4,5",
        "y_values": "2,4,6,8,10"
    })
)


print("\n==============================")
print("17. LINEAR REGRESSION")
print("==============================")

print(
    linear_regression.invoke({
        "x_values": "1,2,3,4,5",
        "y_values": "2,4,5,8,10"
    })
)


print("\n==============================")
print("18. BAR CHART")
print("==============================")

print(
    create_bar_chart.invoke({
        "categories": "A,B,C,D",
        "values": "10,20,15,30",
        "title": "Test Bar Chart"
    })
)


print("\n==============================")
print("19. LINE CHART")
print("==============================")

print(
    create_line_chart.invoke({
        "x_values": "1,2,3,4,5",
        "y_values": "10,20,15,25,30",
        "title": "Test Line Chart"
    })
)


print("\n==============================")
print("20. PIE CHART")
print("==============================")

print(
    create_pie_chart.invoke({
        "categories": "Oil,Gas,Water",
        "values": "50,30,20",
        "title": "Production Composition"
    })
)


print("\n==============================")
print("21. SCATTER PLOT")
print("==============================")

print(
    create_scatter_plot.invoke({
        "x_values": "1,2,3,4,5",
        "y_values": "2,5,4,8,10",
        "title": "Test Scatter Plot"
    })
)


print("\n==============================")
print("22. HISTOGRAM")
print("==============================")

print(
    create_histogram.invoke({
        "values": "10,12,15,15,16,18,20,21,21,25",
        "title": "Test Histogram"
    })
)