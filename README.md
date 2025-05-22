# SERonEmoDB - Speech Emotional Recognition

Building a deep learning system for identifying and classifying emotions from speech data.


## 📋 Contents

* [Prerequisites](#prerequisites)
* [Setup Conda Environment](#setup-conda-environment)
* [Usage](#usage)

  * [Git Guide](#git-guide)
  * [Running Tests (pytest)](#running-tests-pytest)
* [Project Structure](#project-structure)
* [Additional Documentation](#additional-documentation)

---

## Prerequisites

Before you begin, make sure you have installed:

* **[Git](https://git-scm.com/)** (with SSH support). Check out: [Git_Guide](docs%20/Git_Guide.md) for more information.
* **Conda** (Miniconda or Anaconda distribution)

  * Downloads: 
    * [Miniconda](https://docs.conda.io/en/latest/miniconda.html): light software run on CLI.
    * [Anaconda](https://www.anaconda.com/download): heavier softwar with fully GUI.
* **Git Bash** (Windows) or Terminal (macOS/Linux)

---

### Good news for lazy people ~_~ hehe. I created a `one_click_setup.sh` file for a fully setup for this project. If you got lucky enough, you can setup without any bugs ~_~.  

### Note: All setups run on CLI commands in side the repo project folder
For example:
    ```bash
    (test2) khoile@khoile-Legion-5-15IAH7H:~/Documents/Test_WorkFlow/SERonEmoDB$
    ```

## Setup Conda Environment

All project dependencies are specified in `environment.yml`. To create and activate the environment, run:

```bash
# 1. Create the environment (name & packages defined in environment.yml)
conda env create -f environment.yml

# 2. Activate the environment
conda activate my-project-env
```

> **Tip:** To update the environment after modifying `environment.yml`, run:
>
> ```bash
> conda env update -f environment.yml --prune
> ```

### Setup Conda env with requirements.txt

If you don't wanna use `environment.yml` or you get Errors, you can setup through `requirements.txt`

Full instructions here: [Conda Env Instruction](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

> Setup a conda env:
> ```bash
> conda create -n <my-project-env> python=3.xx
> ```

---

## Usage

### Git Guide

For a simple, one-stop Git reference (SSH Key, clone, branch, add, commit, push, pull), see:

* `docs/Git_Guide.md`

### Running Tests (pytest)

1. Ensure the environment is activated:

   ```bash
   conda activate my-project-env
   ```
2. Install test requirements (if separate):

   ```bash
   pip install pytest
   ```
3. Install the project package
    ```bash
    pip install -e . 
    ```
4. Run all tests:

   ```bash
   pytest
   ```

For more details on writing and organizing tests, see:

* `docs/pytest.md`

---

## Project Structure

```text
project-root/
├── README.md                # This file
├── environment.yml          # Conda environment definition
├── docs/
│   ├── Git_Guide.md         # Git workflow guide
│   └── pytest.md            # pytest usage guide
├── src/
│   └── SERonEmoDB/
│       ├── contracts/
│       │   ├── base_data.py
│       │   ├── base_model.py
│       │   └── types_.py
│       ├── data_ingest/
│       │   ├── __init__.py
│       │   └── data_ingest.py
│       ├── feature_extraction/
│       │   ├── __init__.py
│       │   └── feature_extraction.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── model.py
│       └── __init__.py
├── tests/                   # Unit tests
│   └── test_*.py
└── .gitignore
```

---
More instruction guides:

[How to use `pytest`](docs%20/Pytest_guide.md)

*Happy coding!*
