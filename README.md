# qemlib

A modular **Quantum Error Mitigation (QEM)** library built on Qiskit.

> `qemlib` provides research-oriented implementations of major quantum error mitigation techniques, designed for experimentation, benchmarking, and research workflows in noisy quantum computation.

---

## 🚀 Features
- **Dynamical Decoupling (DD)**
- **Zero Noise Extrapolation (ZNE)**
- **Pauli Twirling (PT)**
- **Readout Error Mitigation (REM)**
- Modular, researcher-focused API
- Full compatibility with Qiskit circuits


## 📦 Installation
Install from PyPI:

```bash
pip install qemlib
```

## ⚡ Quick Start
See the [`examples/`](examples) directory for complete usage demonstrations of all implemented mitigation techniques.


## 📁 Examples
- `dd_exp.ipynb` — Dynamical decoupling workflows
- `zne_exp.ipynb`, `zne_exp2.ipynb` — Zero noise extrapolation experiments
- `pt_exp.ipynb`, `pt_exp2.ipynb` — Pauli twirling tests
- `rem_exp.ipynb` — Readout error mitigation demo


## 🧠 Implemented Techniques

### Dynamical Decoupling (DD)
- **Location:** `qemlib/dd/`
- **Modules:**
  - `dd.py` — DD execution wrapper
  - `insertion.py` — Circuit-level DD insertion
  - `seq.py` — Sequence definitions (`xx`, `xp_xm`, `xy4`)

### Zero Noise Extrapolation (ZNE)
- **Location:** `qemlib/zne/`
- **Modules:**
  - `zne.py` — Core logic
  - `folding.py` — Circuit folding methods
  - `functional.py` — Workflow helpers
  - `models.py` — Extrapolation functions
  - `executor.py` — Execution abstraction
  - `plotting.py` — Visualization utilities

### Pauli Twirling (PT)
- **Location:** `qemlib/pt/`
- **Modules:**
  - `pt.py` — Twirling logic
  - `pauli.py` — Operator utilities
  - `twirl.py` — Transformation routines

### Readout Error Mitigation (REM)
- **Location:** `qemlib/rem/`
- **Modules:**
  - `rem.py` — Calibration and mitigation tools


## 🏗️ Architecture & Design Principles
- **Modular architecture** with clear separation of concerns:
  1. Circuit transformation
  2. Noise scaling
  3. Execution
  4. Post‑processing
- Minimal abstraction overhead
- Research‑oriented flexibility and transparency
- Built on top of Qiskit for compatibility and extensibility


## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request


## 📜 License
This project is released under the [MIT License](LICENSE).


## 📖 Citation
If you use **qemlib** in academic work, please cite:

```bibtex
@software{qemlib,
  author = {Hamza Benkadour},
  title = {qemlib: A Modular Quantum Error Mitigation Library},
  year = {2026},
  url = {https://github.com/hmzbn/qemlib}
}
```

---

Happy mitigating! 😊

