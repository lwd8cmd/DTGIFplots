# GIF++ DT currents plots

Load DT chambers data and make plots

# Usage

* Download this project (gif.py and directory structure)
* Put data files in data/scan_nr/ (for example first scan in data/1/, second in data/2/, ...)
* Add attenuations time information in gif.py

These are at the beginning

```python
if scan == 1:
	def getAttenuation(time):# map time to attenuation
		if time > parser.parse("2015-08-13 20:35:00") \
			and time < parser.parse("2015-08-13 20:37:59"):
			return 46420
```

* Select scan_nr to analyze (change scan = 2) at the beginning of the file
* run script "python gif.py"
* plots are automatically saved in the same directory
