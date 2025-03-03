# Emittance Scanner and Emittance Scanner GUI

## Configurations for Controller and Drive:

### ACR74C 
For controlling motion, the ACR74C indexer is used with the configurations (configured in parker motion manager):

- Master0: Units=mm
- Drive: Zeta
- Motor: Other; Rotary; Resolution=25000 pulses/rev
- Scaling: Transmission = Leadscrew: 2.54mm/rev
	 Reducer(s) = Gearbox: Input = 2
			       Output = 1
	==> Scaling: 1.27mm = 1 Revolution
- Fault: Enable Positive Hardware Limit Detection and Enable Negative Hardware Limit Detection: On; Deceleration = 5000

| Axis Input | Negative Limit Onboard Input | Positive Limit Onboard Input |
|------------|------------------------------|------------------------------|
| 0          | 1                            | 0                            |
| 1          | 4                            | 3                            |
| 2          | 7                            | 6                            |
| 3          | 10                           | 9                            |

All Normally Closed

### Zeta Drive DIP Switches for ZETA83-135 Motor (I=On, O=Off):
```
|1|2|3|4|5|6|7|8|9|10|11|12|	|1|2|3|4|5|6|
|I|I|O|I|I|O|O|O|O|O |O |O |	|O|O|O|I|I|I|
```
## Emittance_scanner.py

LabJack T8: AIN0: Input for current
		DAC1: Output to set plate Voltage: two 1.5V batteries are hooked up to lower the output Voltage by 3V because output needs to be between -2 and 2 V, but LabbJack T8 can only output 0-10V

Midpoint Offsets for AECR where measured; for VENUS they were taken from the LabView Emittance scanner program

Velocity 15mm/s; could potentially go faster

main() function combines all classes to a command line executable version of the Emittance_scanner program.
Every step is explained and build to handle wrong/undefined inputs
see docstrings and comments for more info 

## Emittance_scanner_GUI.py

Lets user define new variables or load file into program.
After having defined the variables and the number of scans per axis, the program let's you hit "Run x/y scan" and completes a number of scans automatically.

- Load Data Button let's user open a file from a previous scan, and Display the Data
- Reset Button, resets everything except Motor Instance.
- End Program Button clears all axes, i.e. moves all axes back to home limit and then closes the program see docstrings and comments for more info 

REQUIRED LIBRARIES:
- NUMPY
- MATPLOTLIB
- SCIPY
- LABJACK






