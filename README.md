# LMS Charger

## Introduction 
LMS Charger is a miniature module with USB-C designed for charging
Li-Po bateries. I designed this module while working on other projects
where I needed small Li-Po battery and available solutions were too big
for the application. I also needed some other features.

## Features
- USB-C input - for charging the battery
- MCP73833 - battery charger with selectable current up to 500mA,
  selectable resistor is used to set the current.
- Power Path - for powering the output from the USB, while the
  battery is being charged.

## Safety
 - This module was designed for Li-Po batteries with protection circuit
   inside the package, don't use with unprotected batteries. Li-Ion
   can be used, but use those with protection circuit.
 - The output of module is either 5V or VBAT, depending on whether the
   USB is connected. Connect only with electronics that can handle
   this voltage range.


