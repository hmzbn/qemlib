qemlib

A modular Quantum Error Mitigation (QEM) library built on Qiskit.

qemlib provides clean, research-oriented implementations of major quantum error mitigation techniques, including:

Dynamical Decoupling (DD)

Zero Noise Extrapolation (ZNE)

Pauli Twirling (PT)

Readout Error Mitigation (REM)

The library is designed for experimentation, benchmarking, and research workflows in noisy quantum computation.

📦 Installation
Install from GitHub
pip install git+https://github.com/hmzbn/qemlib.git

🚀 Quick Start

See the examples/ directory for complete usage demonstrations.

🧠 Implemented Techniques
1️⃣ Dynamical Decoupling (DD)

Location: qemlib/dd/

Modules:

dd.py — DD execution wrapper

insertion.py — Circuit-level DD insertion

seq.py — DD sequence definitions

Available sequences:

xx

xp_xm

xy4

Custom sequences can be added in seq.py.

2️⃣ Zero Noise Extrapolation (ZNE)

Location: qemlib/zne/

Modules:

zne.py — Core ZNE logic

folding.py — Circuit folding methods

functional.py — ZNE execution workflow

models.py — Extrapolation functions

executor.py — Execution abstraction

plotting.py — Visualization utilities

3️⃣ Pauli Twirling (PT)

Location: qemlib/pt/

Modules:

pt.py — Pauli twirling logic

pauli.py — Pauli operator utilities

twirl.py — Twirling transformations

Pauli Twirling is used to randomize coherent errors into stochastic Pauli channels.

4️⃣ Readout Error Mitigation (REM)

Location: qemlib/rem/

Modules:

rem.py — Readout calibration and mitigation tools

Supports measurement calibration and expectation value computation workflows.

📂 Project Structure
qemlib/
│
├── examples/
│   ├── dd_exp.ipynb
│   ├── pt_exp.ipynb
│   ├── pt_exp2.ipynb
│   ├── rem_exp.ipynb
│   ├── zne_exp.ipynb
│   ├── zne_exp2.ipynb
│
├── qemlib/
│   ├── dd/
│   │   ├── __init__.py
│   │   ├── dd.py
│   │   ├── insertion.py
│   │   ├── seq.py
│   │
│   ├── pt/
│   │   ├── __init__.py
│   │   ├── pauli.py
│   │   ├── pt.py
│   │   ├── twirl.py
│   │
│   ├── rem/
│   │   ├── __init__.py
│   │   ├── rem.py
│   │
│   ├── zne/
│   │   ├── __init__.py
│   │   ├── executor.py
│   │   ├── folding.py
│   │   ├── functional.py
│   │   ├── models.py
│   │   ├── plotting.py
│   │   ├── zne.py
│   │
│   └── __init__.py
│
├── LICENSE
├── pyproject.toml
├── README.md
└── .gitignore
🎯 Design Principles

Modular architecture

Clear separation between:

Circuit transformation

Noise scaling

Execution

Post-processing

Minimal abstraction overhead

Research-oriented flexibility

Full compatibility with Qiskit circuits

📊 Example Notebooks

Example usage and experiments are provided in the examples/ directory, including:

DD experiments

ZNE experiments

Pauli Twirling benchmarks

Readout mitigation demonstrations

📜 License

This project is released under the MIT License.
See the LICENSE file for details.

🤝 Contributing

Contributions are welcome:

Fork the repository

Create a feature branch

Submit a pull request

📖 Citation

If you use qemlib in academic work, please cite:

@software{qemlib,
  author = {Hamza Benkadour},
  title = {qemlib: A Modular Quantum Error Mitigation Library},
  year = {2026},
  url = {https://github.com/hmzbn/qemlib}
}
