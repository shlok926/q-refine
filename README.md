<div align="center">
  <img src="assets/q_refine_logo.png" alt="Q-Refine Logo" width="250"/>

  <h1>Q-Refine ⚛️</h1>

  <p><em>Enterprise-grade platform for evaluating and mitigating hardware noise in Quantum AI circuits using Zero-Noise Extrapolation (ZNE).</em></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/Framework-Qiskit-purple.svg" alt="Qiskit" />
    <img src="https://img.shields.io/badge/UI-Streamlit-red.svg" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg" alt="Status" />
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" />
  </p>

  <p>
    <a href="#-quick-start">🚀 Quick Start</a> •
    <a href="#-how-to-run-3-ways">💻 Demos</a> •
    <a href="#-architecture">🏗️ Architecture</a> •
    <a href="https://github.com/shlok926/q-refine/issues">🐞 Report Bug</a>
  </p>
</div>

---

## 🎯 Key Features at a Glance

| 🧠 Quantum AI Circuits | 📡 Hardware Profiling | 🛡️ ZNE Mitigation | 🗺️ Topology Optimizer |
| :--- | :--- | :--- | :--- |
| **QNNs & VQE Ready**<br>Benchmarks Parameterized Quantum Circuits instead of basic algorithms. | **IBM Digital Twins**<br>Fetches live T1/T2 relaxation times and readout errors via API. | **Mathematical Accuracy**<br>Proprietary circuit folding and Richardson extrapolation. | **Smart Routing**<br>Analyzes physical backend layout to minimize SWAP gate errors. |

---

## 📑 Table of Contents
- [🎯 Key Features at a Glance](#-key-features-at-a-glance)
- [🛠️ Installation](#️-installation)
- [🚀 How to Run (3 Ways)](#-how-to-run-3-ways)
- [🏗️ Architecture](#️-architecture)
- [🛡️ Security Note](#️-security-note)

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/shlok926/q-refine.git
cd q-refine

# Install dependencies
pip install qiskit qiskit-aer matplotlib numpy streamlit jupyter
```

---

## 🚀 How to Run (3 Ways)

Q-Refine is designed for different types of users, from enterprise managers to core quantum researchers.

### 1. 🌐 The Streamlit Web Dashboard (For Presentations)
Run the beautiful interactive web interface where you can adjust noise sliders and generate visual reports live in your browser.
```bash
streamlit run app.py
```
*This will open a browser window at `http://localhost:8501`.*

### 2. ⚡ The Command-Line Pipeline (For Automation & CI/CD)
Run the automated pipeline to execute the entire benchmarking process in one shot. It will print the analysis and generate a `q_refine_dashboard.png` image.
```bash
python q_refine_pipeline.py
```

### 3. 📓 Jupyter Notebook (For Developers & Researchers)
If you want to play with the Q-Sanitizer step-by-step or modify the circuits mathematically, use the interactive notebook.
```bash
jupyter notebook demo.ipynb
```

---

## 🏗️ Architecture

```text
q_refine/
├── circuits/            # Quantum AI circuits (QNN, VQE, BV, Grover)
├── benchmark_engine/    # Hardware Profilers & IBM Digital Twins
├── mitigation_engine/   # Custom ZNE Engine & Topology Optimizers
└── core/                # Dashboards & Utilities
```

---

## 🛡️ Security Note
This tool evaluates algorithms locally. If you switch `use_real_hardware=True` in the Profiler, ensure your IBM Quantum API Token is saved using `QiskitRuntimeService.save_account()` and **never** hardcoded into the scripts.
