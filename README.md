# Python-Weather-MCP
Simple weather MCP server

# Requirements

1. An `.env` file with a OPENWEATHER_API_KEY
    - This can be obtained for free from (https://openweathermap.org/api)
2. Python version >=3.10

# Installing Dependencies

OPENWEATHER_API_KEY

## If Using Mise (my preference)
Run `mise install`

## UV (recommended)

### Sync (recommended)

Run `uv pip sync uv.lock`

### Install

Run `uv pip install .`

# Using as an MCP Server


## Mise

```
"python-weather-mcp": {
    "type": "stdio",
    "command": "mise",
        "args": [
            "--cd",
            "/Users/rnash/Development/Python-Weather-MCP/",
            "run",
            "app"
        ],
}
```

## UV

```
"python-weather-mcp": {
    "type": "stdio",
    "command": "uv",
        "args": [
            "--directory",
            "/ABSOLUTE/PATH/TO/PARENT/FOLDER/Python-Weather-MCP",
            "run",
            "weather.py"
        ],
}
```