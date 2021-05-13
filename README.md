# Faceit stat finder

©Samuel Lehikoinen 2021

A program that helps user to find Counter-Strike Global Offensive server's players' Faceit information.

## Getting started

Clone the project
`git clone https://github.com/samuellehikoinen/faceit_stat_finder.git`

Install requirements
`pip install -r requirements.txt`

Create .exe file from main.py
`pyinstaller -F faceit_stat_finder/main.py`

Run the main.exe file, that is in the newly created dist file
`dist/main.exe`

## Usage

Type `status` in CS:GO console and copy the output into the programs input line.

If you need to add another player/server to be checked, pressing enter once results in a new line to be typed on.

Pressing enter twice initiates the check up.

Command `exit` closes the program.

Command `ohjeet` shows the instructions (currently only in finnish).

## Acknowledgements
* Lehikoinen J. for propositions
* Virtanen O. for testing
