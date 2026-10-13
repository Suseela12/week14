%pip install -q -U langgraph langchain-core langchain-google-genai requests
---------------------------------------------------------------------------------
import os
import ast
import operator
import requests

from google.colab import userdata
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

print("Libraries imported successfully")
----------------------------------------------------------------------------------------
import os
from google.colab import userdata

key = userdata.get("GEMINI_API_KEY")

os.environ["GOOGLE_API_KEY"] = key
os.environ.pop("GEMINI_API_KEY", None)

print("Gemini API key configured")
---------------------------------------------------------------------------------
@tool
def get_weather(city: str) -> str:
    """Get the current temperature in Celsius for a city."""

    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=15
        )
        geo_response.raise_for_status()
        places = geo_response.json().get("results", [])

        if not places:
            return f"City not found: {city}"

        place = places[0]

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m"
            },
            timeout=15
        )
        weather_response.raise_for_status()

        temperature = weather_response.json()["current"]["temperature_2m"]

        return f"Current temperature in {city} is {temperature} Celsius."

    except Exception as error:
        return f"Weather lookup failed: {error}"
      -------------------------------------------------------------------------------------
def evaluate_expression(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")

            return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](evaluate(node.operand))

        raise ValueError("Unsupported mathematical expression")

    return evaluate(ast.parse(expression, mode="eval").body)


@tool
def calculate(expression: str) -> str:
    """Calculate a basic arithmetic expression safely."""

    try:
        return str(evaluate_expression(expression))
    except Exception as error:
        return f"Calculation error: {error}"


tools = [get_weather, calculate]

print("Weather and calculator tools created")
-----------------------------------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)

print("Gemini LLM initialized")
----------------------------------------------------------------------------
agent = create_react_agent(
    model=llm,
    tools=tools
)

print("LangGraph ReAct agent created successfully")
----------------------------------------------------------------------------
print("Weather tool test:")
print(get_weather.invoke({"city": "London"}))

print("\nCalculator tool test:")
print("15% of 320 =", calculate.invoke({
    "expression": "320 * 15 / 100"
}))
-------------------------------------------------------------------------------
print("=== Agent Execution Trace (Tool Test) ===\n")

# Step 1: Get current weather
weather = get_weather.invoke({"city": "London"})
print("Action: get_weather")
print("Action Input: London")
print("Observation:", weather)

# Extract Celsius temperature
import re

match = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:°C|Celsius)", weather)

if not match:
    print("\nCould not retrieve temperature. Check internet/weather service.")
else:
    celsius = float(match.group(1))

    # Step 2: Convert Celsius to Fahrenheit
    fahrenheit = float(calculate.invoke({
        "expression": f"({celsius} * 9 / 5) + 32"
    }))

    print("\nAction: calculate")
    print("Action Input:", f"({celsius} * 9 / 5) + 32")
    print("Observation:", fahrenheit)

    # Step 3: Calculate 15% of 320
    percentage = float(calculate.invoke({
        "expression": "320 * 15 / 100"
    }))

    print("\nAction: calculate")
    print("Action Input: 320 * 15 / 100")
    print("Observation:", percentage)

    # Step 4: Add the results
    total = float(calculate.invoke({
        "expression": f"{fahrenheit} + {percentage}"
    }))

    print("\nAction: calculate")
    print("Action Input:", f"{fahrenheit} + {percentage}")
    print("Observation:", total)

    print("\n=== Final Answer ===")
    print(f"London temperature: {fahrenheit}°F")
    print(f"15% of 320: {percentage}")
    print(f"Combined total: {total}")
