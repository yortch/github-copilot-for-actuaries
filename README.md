# GitHub Copilot for P&C Actuarial Teams — Demo Workshop

> **Audience:** North America Property & Casualty actuarial professionals at an insurance carrier  
> **Goal:** Demonstrate how GitHub Copilot accelerates actuarial workflows — reserving, pricing, CAT modeling, data validation, and legacy code migration  
> **Prerequisites:** Python 3.10+, VS Code with GitHub Copilot extension

---

## Setting Up Your Environment (New to Python?)

If you're coming from Excel/VBA/SAS and this is your first time using Python, follow these steps to get up and running.

### 1. Install Python

Download Python 3.10 or higher from [python.org](https://www.python.org/downloads/). During installation on Windows, **check the box that says "Add Python to PATH"** — this lets you run `python` from any terminal.

To verify the installation, open a terminal and run:

```bash
python --version
```

You should see something like `Python 3.12.x`.

### 2. Install VS Code and the Python Extension

1. Download and install [Visual Studio Code](https://code.visualstudio.com/)
2. Open VS Code and go to the **Extensions** panel (click the square icon on the left sidebar, or press `Ctrl+Shift+X`)
3. Search for **"Python"** and install the extension published by **Microsoft**

The Python extension gives you:
- **IntelliSense** — autocomplete and hover documentation for Python code
- **Linting & error checking** — red squiggles under mistakes, just like spell-check in Word
- **Run/debug support** — run scripts with a single click or step through code line by line
- **Jupyter notebook support** — run code cells interactively
- **Virtual environment detection** — automatically finds and activates your project's venv (see below)

After installing, you'll see a **Python version indicator** in the bottom-left status bar of VS Code. Click it to select which Python interpreter to use.

### 3. What Is a Virtual Environment (venv)?

A **virtual environment** (venv) is an isolated Python installation for a specific project. Think of it like a separate toolbox for each project — the packages you install in one project don't interfere with another.

**Why does this matter?**
- This project needs `pandas>=2.0` and `statsmodels>=0.14`. Another project might need different versions.
- Without a venv, installing packages goes into your system-wide Python, which can cause version conflicts.
- With a venv, each project gets its own `pip` and its own set of packages — clean and conflict-free.

**Analogy for spreadsheet users:** A venv is like having a separate Excel add-in configuration for each workbook. One workbook can use the actuarial add-in v3 while another uses v2, and they don't step on each other.

### 4. Create and Activate a Virtual Environment

Open a terminal in VS Code (`Ctrl+`` ` or **Terminal → New Terminal**) and run:

```bash
# Create a virtual environment in a folder called .venv
python -m venv .venv
```

This creates a `.venv/` folder in your project directory. Now activate it:

**Windows (Git Bash):**
```bash
source .venv/Scripts/activate
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

When activated, you'll see `(.venv)` at the beginning of your terminal prompt. This means any `pip install` commands will install packages into the venv, not your system Python.

> **VS Code tip:** After creating the venv, VS Code should automatically detect it. If it doesn't, click the Python version in the bottom-left status bar and select the interpreter inside `.venv/`. This ensures VS Code uses the venv for running scripts, linting, and IntelliSense.

### 5. Install Dependencies and Generate Data

With your venv activated, install the project's required packages and generate the sample datasets:

```bash
pip install -r requirements.txt
python data/generate_sample_data.py
```

> **What just happened?** `pip install -r requirements.txt` reads the list of packages (pandas, numpy, matplotlib, etc.) and installs them into your venv. `generate_sample_data.py` creates the synthetic insurance data files that all the demos use.

### 6. Deactivating the Virtual Environment

When you're done working, you can deactivate the venv:

```bash
deactivate
```

This returns you to your system Python. Next time you open the project in VS Code, reactivate the venv (or let VS Code do it automatically if it's configured).

---

## Quick Start (for experienced Python users)

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
python data/generate_sample_data.py
```

---

## Demo Overview

| # | Demo | Actuarial Domain | Copilot Features | Time |
|---|------|-----------------|-------------------|------|
| 1 | [Loss Triangle & Chain Ladder](demo1_loss_triangle/) | Reserving | Code generation from comments, autocomplete | 20 min |
| 2 | [Bornhuetter-Ferguson](demo2_bornhuetter_ferguson/) | Reserving | Chat `/explain`, refactoring between methods | 15 min |
| 3 | [Frequency-Severity GLM](demo3_glm_pricing/) | Ratemaking / Pricing | Statistical code generation, inline suggestions | 20 min |
| 4 | [CAT Exceedance Curve](demo4_cat_modeling/) | Catastrophe Modeling | Simulation code, visualization | 15 min |
| 5 | [VBA-to-Python Migration](demo5_vba_migration/) | Legacy Modernization | Cross-language translation, `/explain` | 15 min |
| 6 | [Data Validation & Tests](demo6_data_validation/) | Regulatory / Filing | Test generation, data quality checks | 10 min |
| 7 | [Experience Study](demo7_experience_study/) | Ratemaking / Filing | Multi-step calculations, utility functions | 15 min |

### Customization Feature Demos

| # | Demo | What It Shows | Copilot Feature | Time |
|---|------|--------------|-----------------|------|
| A | [Instruction Files in Action](#demo-a-instruction-files-in-action-10-min) | Auto-loaded actuarial context | Workspace & file-scoped instructions | 10 min |
| B | [Skills — Guided Workflows](#demo-b-skills--guided-workflows-15-min) | Multi-step actuarial procedures | On-demand skill playbooks | 15 min |
| C | [Custom Agents — Actuarial Personas](#demo-c-custom-agents--actuarial-personas-15-min) | Specialized AI team members | `@agent` invocation in Chat | 15 min |
| D | [Combining All Three](#demo-d-combining-all-three-10-min) | Full reserving → pricing → QA workflow | Instructions + Skills + Agents together | 10 min |

---

## Presenter Notes

### How to Run Each Demo

Each demo folder contains a Python file with **comment prompts** designed to trigger Copilot suggestions. The recommended workflow:

1. **Open the `.py` file** in VS Code with Copilot enabled
2. **Delete the code below the comment prompts** (the "answer key" is there for reference)
3. **Place your cursor after a comment** and let Copilot generate the code
4. **Use Copilot Chat** to ask questions, explain code, or refactor

### Key Talking Points for Insurance Audience

- **"Copilot understands actuarial concepts"** — Show it generating chain ladder, BF, GLM code from plain English comments
- **"Accelerates migration from Excel/VBA/SAS"** — Demo 5 is the crowd-pleaser for teams with legacy tools
- **"Catches mistakes with test generation"** — Demo 6 shows how Copilot helps build guardrails
- **"Works with your existing stack"** — Python, R, SQL, VBA — Copilot handles all of them
- **"Keeps your code private"** — Copilot Business/Enterprise does NOT train on your code

### Demo Delivery Tips

- Start each demo by showing the **comment prompt only** (hide the solution)
- Let Copilot generate the code live — the "wow moment" is seeing it understand actuarial context
- If Copilot gives a slightly wrong answer, **show how Chat can fix it** — that's a realistic workflow
- Encourage the audience to think about **their own VBA macros / Excel models** they could migrate

---

## Sample Data

All demos use synthetic data generated by `data/generate_sample_data.py`. The data simulates a mid-size P&C insurer writing:
- **Personal Auto** and **Homeowners** lines of business
- Policy years 2015–2024
- ~50,000 policies with realistic loss distributions
- Territories across several US states

No real policyholder or claims data is used.

---

## Repository Structure

```
actuarial-demo/
├── README.md
├── requirements.txt
├── data/
│   ├── generate_sample_data.py      # Creates all sample datasets
│   ├── loss_triangle.csv            # (generated) Paid loss triangle
│   ├── policy_data.csv              # (generated) Policy-level exposure data
│   ├── claim_data.csv               # (generated) Individual claim records
│   └── cat_event_history.csv        # (generated) Historical CAT events
├── demo1_loss_triangle/
│   └── chain_ladder.py              # Chain ladder & IBNR calculation
├── demo2_bornhuetter_ferguson/
│   └── bf_method.py                 # BF method with comparison to CL
├── demo3_glm_pricing/
│   └── freq_sev_glm.py             # Poisson/Gamma GLM for ratemaking
├── demo4_cat_modeling/
│   └── cat_exceedance.py           # Monte Carlo simulation, OEP/AEP curves
├── demo5_vba_migration/
│   ├── premium_calc.vba            # Original VBA macro
│   └── premium_calc.py             # Migrated Python version
├── demo6_data_validation/
│   ├── validation_rules.py         # Data quality checks
│   └── test_actuarial_calcs.py     # Unit tests for actuarial functions
├── demo7_experience_study/
│   └── rate_indication.py          # Loss trending & rate indication
└── .github/
    ├── copilot-instructions.md     # Workspace-level Copilot context
    ├── instructions/
    │   ├── reserving.instructions.md
    │   ├── ratemaking.instructions.md
    │   ├── catastrophe-modeling.instructions.md
    │   ├── data-validation.instructions.md
    │   └── vba-migration.instructions.md
    ├── skills/
    │   ├── loss-triangle-analysis/SKILL.md
    │   ├── rate-indication/SKILL.md
    │   └── vba-to-python-migration/SKILL.md
    └── agents/
        ├── reserving-actuary.agent.md
        ├── pricing-actuary.agent.md
        ├── data-quality-reviewer.agent.md
        └── legacy-code-migrator.agent.md
```

---

## Copilot Customization Files

This repo includes **instruction files**, **skills**, and **custom agents** that teach Copilot actuarial domain knowledge. These are powerful for day-to-day use beyond the demos.

### Instruction Files (`.github/instructions/`)
Automatically loaded based on context. Copilot reads these when you work on relevant files:
| File | Triggers On |
|------|------------|
| `reserving.instructions.md` | Loss triangles, chain ladder, BF, IBNR, development factors |
| `ratemaking.instructions.md` | GLMs, pricing, rate indications, pure premium, relativities |
| `catastrophe-modeling.instructions.md` | Monte Carlo, OEP/AEP, VaR/TVaR, return periods |
| `data-validation.instructions.md` | Data quality, regulatory filings, NAIC, ASOP |
| `vba-migration.instructions.md` | Any `.vba` file (auto-applied via `applyTo` pattern) |

### Skills (`.github/skills/`)
On-demand multi-step workflows Copilot can follow:
- **loss-triangle-analysis** — Full chain ladder workflow from raw data to IBNR
- **rate-indication** — End-to-end ratemaking from experience compilation to indicated rate change
- **vba-to-python-migration** — Structured migration preserving exact business logic

### Custom Agents (`.github/agents/`)
Specialized personas you can invoke with `@agent-name` in Copilot Chat:
- **@reserving-actuary** — Triangle analysis, IBNR, BF/CL comparisons
- **@pricing-actuary** — GLM modeling, rate indications, filing exhibits
- **@data-quality-reviewer** — Validation checks, outlier detection, audit prep
- **@legacy-code-migrator** — VBA/SAS/Excel to Python conversion

---

## Demoing the Customization Features

These demos showcase how instruction files, skills, and custom agents make Copilot **domain-aware** for actuarial work. Run these after the code demos (1–7) to show the team how to customize Copilot for their own workflows.

### Demo A: Instruction Files in Action (~10 min)

Show how Copilot automatically picks up actuarial context from instruction files — no special commands needed.

| Step | What to Do | What to Show |
|------|-----------|--------------|
| 1 | Open `demo1_loss_triangle/chain_ladder.py` and ask Copilot Chat: **"Add a tail factor to this analysis"** | Copilot references "tail factor" terminology and applies a CDF adjustment — because `reserving.instructions.md` loaded automatically |
| 2 | Open `demo5_vba_migration/premium_calc.vba` and ask: **"Explain this code"** | The `applyTo: "**/*.vba"` pattern on `vba-migration.instructions.md` auto-activates — Copilot explains using VBA-to-Python mapping patterns from the instruction file |
| 3 | Create a new empty `.py` file and type a comment: `# Validate that paid losses do not exceed incurred losses` then let Copilot autocomplete | Copilot generates a validation function consistent with the rules in `data-validation.instructions.md` |
| 4 | Open `copilot-instructions.md` and walk through the contents | Explain that this file gives Copilot workspace-wide context — it knows the LOBs, states, and coding conventions for every interaction |

**Key talking point:** *"Instruction files are like onboarding documents for Copilot. Once they're in your repo, every team member gets the same domain context automatically."*

### Demo B: Skills — Guided Workflows (~15 min)

Show how skills give Copilot a structured, multi-step playbook to follow.

| Step | What to Do | What to Show |
|------|-----------|--------------|
| 1 | Open Copilot Chat and type: **"Perform a chain ladder analysis on the personal auto loss triangle in data/loss_triangle.csv"** | The `loss-triangle-analysis` skill activates — Copilot follows the 5-step workflow: build triangle → link ratios → CDFs → ultimates/IBNR → visualization |
| 2 | Follow up: **"Now compare with Bornhuetter-Ferguson using a 65% expected loss ratio"** | Copilot uses the same skill's structure to extend the analysis with a BF comparison |
| 3 | Ask: **"Calculate the indicated rate change for Personal Auto with 4% loss trend and 30% expense ratio"** | The `rate-indication` skill guides Copilot through: experience compilation → development → trending → on-leveling → indicated change |
| 4 | Open `premium_calc.vba` and ask: **"Migrate this VBA code to Python with unit tests"** | The `vba-to-python-migration` skill ensures Copilot preserves exact business logic and produces tests alongside the code |

**Key talking point:** *"Skills are like actuarial procedures in a manual — Copilot follows the same steps your team would, but in seconds instead of hours."*

### Demo C: Custom Agents — Actuarial Personas (~15 min)

Show how custom agents act as specialized AI team members with focused expertise.

| Step | What to Do | What to Show |
|------|-----------|--------------|
| 1 | In Copilot Chat, type: **@reserving-actuary Analyze the loss triangle in data/loss_triangle.csv and estimate IBNR for each accident year** | The reserving actuary agent runs a full reserve analysis — chain ladder + BF comparison, factor selection table, IBNR summary, and visualization |
| 2 | Follow up with: **@reserving-actuary The 2023 accident year link ratio looks high — should we exclude it?** | Shows the agent's domain reasoning — it will discuss factor selection, volatility in immature years, and recommend an approach |
| 3 | Switch agents: **@pricing-actuary Build a frequency-severity GLM for Personal Auto using the policy and claim data** | The pricing actuary runs the GLM workflow — Poisson frequency, Gamma severity, relativities table, and model diagnostics |
| 4 | Try: **@data-quality-reviewer Run validation checks on the claim and policy data before I use it for reserving** | The data quality agent runs structural and statistical checks, returning a severity-classified issue table with remediation recommendations |
| 5 | Try: **@legacy-code-migrator Convert premium_calc.vba to Python and verify the output matches** | The migration agent explains the VBA, writes Python, and produces unit tests — all in one interaction |

**Key talking point:** *"Custom agents are like having a junior analyst who already knows your team's methods — you tell them what to do, and they follow your playbook."*

### Demo D: Combining All Three (~10 min)

The real power is when instructions, skills, and agents work together. Run this as a capstone demo.

| Step | What to Do | What to Show |
|------|-----------|--------------|
| 1 | Ask: **@reserving-actuary Perform a full reserve analysis for Personal Auto and present results suitable for a reserve committee** | The agent uses its persona constraints + the reserving instruction file's terminology + the loss-triangle-analysis skill's workflow to produce committee-ready output |
| 2 | Then ask: **@pricing-actuary Using the IBNR estimates from the reserve analysis, calculate the indicated rate change for Personal Auto** | Shows agents building on each other's work — the pricing actuary references the reserving output and follows the rate-indication skill workflow |
| 3 | Finally: **@data-quality-reviewer Review the data used in the reserve and pricing analyses — are there any quality issues I should disclose in the filing?** | The data quality agent audits the underlying data with regulatory awareness from `data-validation.instructions.md` — ASOP #23 compliance |

**Key talking point:** *"This is a full actuarial workflow — reserving, pricing, and data quality review — with Copilot acting as three different specialists, all following your team's standards."*

### Tips for Demoing Customization Features

- **Show the source files** — Open the `.agent.md`, `SKILL.md`, and `.instructions.md` files so the audience sees they're just Markdown. No code required.
- **Emphasize editability** — Change a line in an instruction file (e.g., swap "volume-weighted" to "simple average") and show how Copilot's behavior changes immediately.
- **Connect to their workflow** — Ask: *"What methods does your team use? What terminology? We can encode that in instruction files today."*
- **Highlight governance** — Instruction files and skills are version-controlled, reviewed in PRs, and shared across the team. This replaces tribal knowledge with documented, auditable standards.
