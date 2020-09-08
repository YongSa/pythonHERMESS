# pythonHERMESS
Ground station software for REXUS experiment [HERMESS project](https://project-hermess.com).

## Installation
```shell script
# install python 3.7 with pip and venv
# go to project path
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

## Execution
```shell script
# go to project path
source .venv/bin/activate
python . --ports # display all possible ports
python . -p COM3 # use with COM3 port (exemplatory)
python . --help # display help text
deactivate
```