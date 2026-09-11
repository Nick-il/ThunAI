from rag import agent


def ask(question):

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    print("\n================================")
    print("QUESTION")
    print("================================")
    print(question)

    print("\n================================")
    print("ANSWER")
    print("================================")
    print(result.get("answer", ""))


# Test 1
ask(
    "Calculate 25 * 17"
)


# Test 2
ask(
    "Calculate the Reynolds number for "
    "density 1000 kg/m3, velocity 2 m/s, "
    "diameter 0.1 m and viscosity 0.001 Pa.s"
)


# Test 3
ask(
    "Convert 100 degrees Celsius to Fahrenheit"
)


# Test 4
ask(
    "Calculate the heat transfer rate for "
    "mass flow rate 2 kg/s, specific heat "
    "4186 J/kg.K and temperature difference 20 K"
)


# Test 5
ask(
    "Find the mean and standard deviation of "
    "10,20,30,40,50"
)


# Test 6
ask(
    "Create a pie chart for Oil 50, Gas 30, Water 20"
)


# Test 7
ask(
    "What is machine learning?"
)