# Experiment 14: LangGraph ReAct Agent

## Aim
To build a basic LLM agent using LangGraph's `create_react_agent` with weather and calculator tools.

## Tools
- **get_weather(city):** Retrieves the current temperature in Celsius using Open-Meteo.
- **calculate(expression):** Safely evaluates basic arithmetic expressions.

## Algorithm
1. Install the required packages.
2. Configure the OpenAI API key.
3. Define the weather and calculator tools.
4. Initialize `ChatOpenAI` with `gpt-4o-mini` and temperature 0.
5. Build the agent using `create_react_agent`.
6. Submit a query that requires weather information and multiple calculations.
7. Print tool actions, observations, and the final answer.

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

Windows Command Prompt:

```cmd
set OPENAI_API_KEY=your_api_key_here
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Never upload your API key to GitHub.

## Run

```bash
python src/experiment.py
```

## Expected Output

The output includes weather-tool results, calculator actions, and a final combined answer. The temperature and total vary with the live weather data.

Example calculation if the temperature is 18°C:

- Fahrenheit: `18 × 9 / 5 + 32 = 64.4°F`
- 15% of 320: `320 × 15 / 100 = 48`
- Combined total: `64.4 + 48 = 112.4`

## Result
A LangGraph ReAct agent was created to use tools for live weather retrieval and arithmetic, then combine the results into a final answer.
