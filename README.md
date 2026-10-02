## 🚀 Installation & Setup Guide

This project requires **Python 3.8 or higher**. Follow these steps to clone the repository, set up a virtual environment, and run the application locally on your machine.

### 1. Clone the Repository
Clone the project to your local machine and navigate into the project directory:
```bash
git clone https://github.com/GiproveR/dash-app
cd dash-app
```

### 2. Create a Virtual Environment
Create an isolated environment to ensure the project dependencies don't conflict with your global Python setup:
```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment based on your operating system:

* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

*Note: Once activated, you should see `(.venv)` appear at the beginning of your terminal prompt.*

### 4. Install Dependencies
Upgrade `pip` and install all required packages (including `dash`, `pandas`, and their dependencies) using the `requirements.txt` file:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the Application
Start the main script to launch your Dash server:
```bash
python main.py
```

Once running, the terminal will provide a local URL (usually `http://127.0.0.1:8050/`). Open this link in your web browser to view the application.
