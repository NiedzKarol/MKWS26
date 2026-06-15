# Computer Methods in Combustion - Final Project

**Topic:** Numerical Analysis of Nitrogen Oxides (NOx) Emissions in Methane Combustion using Cantera

## Overview
This repository contains the final project for the "Computer Methods in Combustion" course. The project investigates the formation of nitrogen oxides (specifically thermal NO) during the combustion of methane ($CH_4$). The analysis is performed using 0D constant-pressure reactor simulations with the **Cantera** open-source chemical kinetics software and the **GRI 3.0** kinetic mechanism.

The main goal of the project is to evaluate the influence of:
- Initial mixture temperature ($T_{init}$),
- Equivalence ratio ($\Phi$),
- Residence time,

on the thermal NO production via the Zeldovich mechanism.

## Repository Structure
- `simulation.py` - The main Python script containing the chemical kinetics simulations using Cantera.
- `report.tex` - The LaTeX source code for the final scientific report.
- `plot_time_history.png` - Generated plot showing NO formation over time.
- `plot_no_vs_temp.png` - Generated plot showing final NO emission vs initial temperature for different equivalence ratios.
- `plot_contour.png` - Generated contour map of NO emission vs Temperature and Equivalence Ratio.
- `Report.pdf` - The final compiled version of the report (add this after compiling LaTeX).

## Requirements
To run the simulation, you need to have Python installed along with the following libraries:
```bash
pip install cantera numpy matplotlib
