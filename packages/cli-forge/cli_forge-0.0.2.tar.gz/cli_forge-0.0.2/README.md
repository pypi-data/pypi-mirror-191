# CLI Forge

A tool for building simple CLIs

## Installation

`pip install pick`

## Input

### Basic

```py
from cli-forge import cli_prompt

basic_input = cli_prompt("What is your name?")
```

### Select

```py
from cli-forge import cli_prompt

select_input = cli_prompt("What currency will you be using?", options=["£", "$"], select=True)
```

### Multi-select

```py
from cli-forge import cli_prompt

multi_select_input = cli_prompt("Which languages would you like to include?", options=["English", "Italian", "Spanish"], options_format=["EN", "IT", "ES"], multiselect=True)
```

### Options

- `prompt`: prompt above the options
- `options`: (optional) list of options
- `select`: (optional) if True, allows you select an option
- `multiselect`: (optional) if True, allows you to select multiple options
- `options_format`: (optional) allows you to format your output for use in your program

## Input

### Usage

```py
from cli-forge import cli_progress

cli_progress(10, 1, "Fetching data...")
# function
cli_progress(10, 2, "Fetching data...")
# ...
```

### Options

- `length`: number of progress units
- `progress`: progress level (out of length)
- `prefix`: text before the progress bar
- `size`: (optional) progress bar size on screen
- `end`: (optional) if True, allows you to end the progress bar before it completes