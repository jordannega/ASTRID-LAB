# ASTRID Advanced Astrophysics & Orbital Mechanics Lab

An interactive, high-fidelity web application built with Streamlit and Plotly designed to simulate foundational and advanced astrophysical mechanics. The laboratory engine houses three core research domains: Keplerian orbital kinematics with dynamic vector plotting, stellar thermodynamics with habitable zone mapping, and general relativistic time dilation curves near gravitational singularities.

---

## 🌌 Core Research Domains

### 1. Orbital Kinematics & Dynamic Vectors
- Solves for planetary escape velocities ($v_{esc} = \sqrt{\frac{2GM}{R}}$) and Keplerian orbital periods.
- Utilizes the **Vis-Viva equation** ($v = \sqrt{GM(\frac{2}{r} - \frac{1}{a})}$) to map instantaneous orbital speed.
- Generates dynamic trajectory maps rendering proportional velocity vector arrows ($\vec{v}$) that automatically scale to illustrate true kinetic acceleration at periapsis and deceleration at apoapsis.

### 2. Stellar Flux & Habitable Zones
- Calculates the total energy output of stars (Luminosity) using the **Stefan-Boltzmann Law** ($L = 4\pi R^2 \sigma T^4$).
- Models boundaries for the circumstellar habitable zone (the "Goldilocks Zone") to map out the theoretical liquid water boundaries for varying stellar classifications (e.g., Sol, Sirius, Proxima Centauri).

### 3. Relativistic Time Dilation Matrix
- Simulates gravitational time warping using the **Schwarzschild metric** ($t' = t \sqrt{1 - \frac{2GM}{rc^2}}$).
- Generates smooth spacetime variance curves mapping coordinate time against radial proximity to a black hole's event horizon.

---

## 🛠️ Tech Stack & Architecture
- **Core Engine:** Python 3
- **UI Framework:** Streamlit 
- **Data Mechanics:** NumPy
- **Visualization Suite:** Plotly Dark Engine (vector annotations, radial geometry patches, and curve sweeps)
- **Deployment Ready:** Configured as a fully self-contained single-file architecture to eliminate local path resolving conflicts.

---

## 📦 Quickstart Local Deployment

1. Clone this repository:
   ```bash
   git clone [https://github.com/jordannega/ASTRRID-LAB.git](https://github.com/jordannega/ASTRRID-LAB.git)
   cd ASTRIR-LAB

2. Install the necessary calculation and plotting dependencies:

Bash
pip install -r requirements.txt

3. Spin up the localized simulation laboratory:

Bash
streamlit run app_astronomy.py
