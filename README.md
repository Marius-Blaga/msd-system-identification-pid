# Mass-Spring-Damper System: Identification & PID Control 🤖

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Control Systems](https://img.shields.io/badge/Library-Control_Systems-orange)](https://python-control.readthedocs.io/)

A comprehensive implementation of a mechanical **Mass-Spring-Damper (MSD)** system, developed as part of my **Automation & Applied Informatics** studies (Year 3).

## 🎯 Project Goals
- **Numerical Simulation:** Open-loop response of a 2nd order mechanical system.
- **System Identification:** Parametric identification using Input-Output data.
- **Control Design:** PID tuning (Ziegler-Nichols & Optimization) to meet settling time and overshoot constraints.

## 💻 Tech Stack
- **Languages:** Python 3.10+
- **Libraries:** NumPy, SciPy, Control, Matplotlib, Seaborn
- **Environment:** Jupyter Notebooks for step-by-step analysis.

## 📂 Project Structure
- `src/` - Core modules (reusable logic for identification & control).
- `notebooks/` - Step-by-step simulation and plotting.
- `data/` - Simulated datasets (CSV format).
- `figures/` - Automatically generated plots.

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Marius-Blaga/msd-system-identification-pid.git](https://github.com/Marius-Blaga/msd-system-identification-pid.git)
   cd msd-system-identification-pid