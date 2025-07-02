# Python-Weather-MCP

Simple weather MCP server, installs one tool which calls `get_forecast`

`get_forecast` takes in a `str` (city) and returns the current forecast for that city

# Requirements

1. An `.env` file with a OPENWEATHER_API_KEY
    - This can be obtained for free from (https://openweathermap.org/api)
2. Python version >=3.10

# Installing Dependencies

## Mise (recommended but preference)

Run `mise install`

## UV (recommended)

Run `uv sync`

## Pip

Run `pip install .`

# Using as an MCP Server

Add the `JSON` configuration below to the config for the application using the server 

- For VSCode it is in `/Users/NAME/Library/Application Support/Code/User/settings.json`
- For Claude Desktop it is in `~/Library/Application Support/Claude/claude_desktop_config.json`

## Mise

```
"python-weather-mcp": {
    "type": "stdio",
    "command": "mise",
        "args": [
            "--cd",
            "/ABSOLUTE/PATH/TO/PARENT/FOLDER/Python-Weather-MCP",
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

## Pip 

```
"python-weather-mcp": {
    "type": "stdio",
    "command": "python",
    "args": [
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/Python-Weather-MCP/weather.py"
    ]
}
```