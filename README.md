# ⚛️ Q-Refine: Quantum AI Robustness Benchmark

<div align="center">
  <img src="assets/q_refine_logo.png" alt="Q-Refine Logo" width="300"/>
</div>

**Q-Refine** is an enterprise-grade platform for evaluating and mitigating hardware noise in Quantum AI circuits. It features a proprietary Zero-Noise Extrapolation (ZNE) engine built from scratch to automatically "sanitize" noisy quantum circuits without the overhead of physical ancilla qubits.

## ✨ Advanced Features
1. **True Quantum AI Circuits:** Benchmarks Parameterized Quantum Circuits (PQCs) used in Quantum Neural Networks (QNNs) and VQE.
2. **Real-Time Hardware Noise Profiling:** Uses IBM Digital Twins to fetch and simulate accurate T1/T2 relaxation times and readout errors.
3. **Automated Error Mitigation (ZNE):** Folds circuits automatically to extrapolate the pure "Zero-Noise" answer mathematically.
4. **Topology Optimizer:** Analyzes the physical layout of the backend and re-routes qubits to minimize SWAP gate errors.
5. **CI/CD Integration:** Includes a GitHub Action workflow to automatically benchmark your quantum circuits on every commit.

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/q-refine.git
cd q-refine

# Install dependencies
pip install qiskit qiskit-aer matplotlib numpy streamlit jupyter
```

---

## 🚀 How to Run (3 Ways)

Q-Refine is designed for different types of users, from enterprise managers to core quantum researchers.

### 1. The Streamlit Web Dashboard (For Presentations & Enterprise)
Run the beautiful interactive web interface where you can adjust noise sliders and generate visual reports live in your browser.
```bash
streamlit run app.py
```
*This will open a browser window at `http://localhost:8501`.*

### 2. The Command-Line Pipeline (For Automation & CI/CD)
Run the automated pipeline to execute the entire benchmarking process in one shot. It will print the analysis and generate a `q_refine_dashboard.png` image.
```bash
python q_refine_pipeline.py
```

### 3. Jupyter Notebook (For Developers & Researchers)
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

## 🛡️ Security Note
This tool evaluates algorithms locally. If you switch `use_real_hardware=True` in the Profiler, ensure your IBM Quantum API Token is saved using `QiskitRuntimeService.save_account()` and **never** hardcoded into the scripts.
