import os
import subprocess
import sys
import time

# --- Configuration ---
SUNA_REPO_URL = "https://github.com/kortix-ai/suna.git"
HOME_DIR = os.path.expanduser("~")
SUNA_DIR = os.path.join(HOME_DIR, "suna")
ENV_FILE_PATH = os.path.join(SUNA_DIR, ".env")

# --- Helper Functions ---
def print_info(message):
    """Prints an informational message."""
    print(f"\n[INFO] {message}")

def print_success(message):
    """Prints a success message."""
    print(f"[SUCCESS] {message}")

def print_warning(message):
    """Prints a warning message."""
    print(f"[WARNING] {message}")

def print_error(message):
    """Prints an error message and exits."""
    print(f"\n[ERROR] {message}")
    sys.exit(1)

def run_command(command, check=True):
    """Runs a command and returns its output."""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {command}\n{e.stderr}")

def check_installed(command):
    """Checks if a command is installed."""
    return subprocess.run(f"command -v {command}", shell=True, capture_output=True).returncode == 0

def prompt_user(message):
    """Prompts the user for input."""
    return input(f"\n{message}\n> ")

def pause_for_user(message="Press Enter to continue..."):
    """Pauses execution and waits for the user to press Enter."""
    input(f"\n{message}")

# --- Main Functions ---
def check_prerequisites():
    """Checks for and installs necessary prerequisites."""
    print_info("Checking prerequisites...")

    # Git
    if not check_installed("git"):
        print_error("Git is not installed. Please install it and rerun the script.")
    print_success("Git is installed.")

    # Homebrew
    if not check_installed("brew"):
        print_error("Homebrew is not installed. Please install it from https://brew.sh/ and rerun the script.")
    print_success("Homebrew is installed.")

    # Docker
    if not os.path.exists("/Applications/Docker.app"):
        print_error("Docker Desktop is not installed. Please install it from https://www.docker.com/products/docker-desktop/ and rerun the script.")

    docker_running = "running" in run_command("docker info")
    if not docker_running:
        print_error("Docker Desktop is not running. Please start it and rerun the script.")
    print_success("Docker is installed and running.")

    # Python 3.11
    if "3.11" not in run_command("python3 --version"):
        print_info("Python 3.11 not found. Installing via Homebrew...")
        run_command("brew install python@3.11")
    print_success("Python 3.11 is installed.")

    # Redis
    if not check_installed("redis-server"):
        print_info("Redis not found. Installing via Homebrew...")
        run_command("brew install redis")

    if "running" not in run_command("brew services list | grep redis"):
        print_info("Starting Redis server...")
        run_command("brew services start redis")
    print_success("Redis is installed and running.")

    # Supabase CLI
    if not check_installed("supabase"):
        print_info("Supabase CLI not found. Installing via Homebrew...")
        run_command("brew install supabase/tap/supabase")
    print_success("Supabase CLI is installed.")

def collect_api_keys():
    """Collects API keys from the user."""
    print_info("Collecting API keys...")

    llama_endpoint = prompt_user("Enter the local API endpoint for your LLama 3 instance (e.g., http://localhost:11434):")

    supabase_url = prompt_user("Enter your Supabase Project API URL:")
    supabase_anon_key = prompt_user("Enter your Supabase Anonymous Key:")
    supabase_service_key = prompt_user("Enter your Supabase Service Role Key:")

    daytona_api_key = prompt_user("Enter your Daytona API Key:")

    tavily_api_key = prompt_user("Enter your Tavily API Key (optional, press Enter to skip):")
    rapidapi_key = prompt_user("Enter your RapidAPI Key (optional, press Enter to skip):")

    return {
        "LLAMA_ENDPOINT": llama_endpoint,
        "SUPABASE_URL": supabase_url,
        "SUPABASE_ANON_KEY": supabase_anon_key,
        "SUPABASE_SERVICE_KEY": supabase_service_key,
        "DAYTONA_API_KEY": daytona_api_key,
        "TAVILY_API_KEY": tavily_api_key,
        "RAPIDAPI_KEY": rapidapi_key,
    }

def write_env_file(api_keys):
    """Writes the API keys to the .env file."""
    print_info(f"Writing API keys to {ENV_FILE_PATH}...")

    env_content = f"""
# Suna AI Configuration
# This file is managed by the Suna setup script.
# Please ensure this file is kept secure and not committed to version control.

# -- LLM Configuration --
# The local endpoint for your LLama 3 instance.
LLM_PROVIDER="litellm"
LITELLM_MODEL="ollama/llama3"
LITELLM_BASE_URL="{api_keys['LLAMA_ENDPOINT']}"

# -- Supabase Configuration --
SUPABASE_URL="{api_keys['SUPABASE_URL']}"
SUPABASE_ANON_KEY="{api_keys['SUPABASE_ANON_KEY']}"
SUPABASE_SERVICE_KEY="{api_keys['SUPABASE_SERVICE_KEY']}"

# -- Daytona Configuration --
DAYTONA_API_KEY="{api_keys['DAYTONA_API_KEY']}"

# -- Optional Services --
TAVILY_API_KEY="{api_keys['TAVILY_API_KEY']}"
RAPIDAPI_KEY="{api_keys['RAPIDAPI_KEY']}"
"""

    with open(ENV_FILE_PATH, "w") as f:
        f.write(env_content)

    print_success(".env file created successfully.")
    print_warning("The .env file contains sensitive API keys. Please ensure it is not committed to version control.")

def manage_suna_repo():
    """Clones or updates the Suna AI repository."""
    print_info("Managing Suna AI repository...")

    if os.path.exists(SUNA_DIR):
        print_info("Suna repository already exists. Pulling latest changes...")
        os.chdir(SUNA_DIR)
        run_command("git pull")
    else:
        print_info(f"Cloning Suna repository into {SUNA_DIR}...")
        run_command(f"git clone {SUNA_REPO_URL} {SUNA_DIR}")
        os.chdir(SUNA_DIR)

    print_success("Suna repository is up to date.")

def guided_setup():
    """Provides guided instructions for the interactive setup.py wizard."""
    print_info("Starting the interactive Suna AI setup...")
    print_warning("The script will now pause and guide you through the `python setup.py` wizard.")
    print_warning("Please follow the instructions carefully.")

    pause_for_user()

    print_info("Step 1: Running `python setup.py`")
    print("The setup wizard will now start. Please follow the on-screen prompts and the instructions below.")

    # Instructions for the user
    print("\n--- Instructions for `setup.py` ---")
    print("1.  **LLM Provider**: When prompted for an LLM provider, choose an option that allows a custom endpoint. This might be 'OpenRouter' or a similar custom provider. You will need to enter the local LLama 3 endpoint you provided earlier.")
    print("2.  **Supabase**: Enter the Supabase URL and keys when prompted.")
    print("3.  **Redis**: Use the default Redis settings (localhost:6379).")
    print("4.  **Daytona**: Enter your Daytona API key when prompted.")
    print("5.  **Other Services**: Enter your Tavily and RapidAPI keys if you have them.")
    print("------------------------------------")

    pause_for_user("Press Enter to start the `python setup.py` wizard now...")

    # We can't fully automate this part, so we run it and let the user interact
    try:
        subprocess.run(["python3", "setup.py"], check=True)
    except subprocess.CalledProcessError:
        print_error("The `setup.py` wizard failed. Please check the output above for errors and try again.")

    print_success("`setup.py` wizard completed.")

def start_suna():
    """Starts the Suna AI services."""
    print_info("Starting Suna AI...")

    try:
        run_command("python3 start.py")
        print_success("Suna AI is starting up. This may take a few minutes.")

        # Give some time for the containers to start
        time.sleep(30)

        # Check Docker container status
        docker_status = run_command("docker ps")
        if "suna" in docker_status:
            print_success("Suna AI containers are running.")
        else:
            print_warning("Could not confirm Suna AI containers are running. Please check Docker Desktop.")

    except Exception as e:
        print_error(f"Failed to start Suna AI: {e}")

def generate_readme():
    """Generates a README.md file with setup and troubleshooting instructions."""
    print_info("Generating README.md...")

    readme_content = f"""
# Suna AI on macOS M1 Max - Automated Setup

This README provides instructions on how to use the automated setup script and provides manual setup guidance and troubleshooting tips.

## Automated Setup

To set up Suna AI using the automated script, simply run it from your terminal:

```bash
python3 suna_setup.py
```

The script will guide you through the process, check for prerequisites, collect necessary API keys, and provide instructions for the interactive parts of the setup.

## Manual Setup Instructions

If you prefer to set up Suna AI manually, follow these steps.

### 1. Prerequisites

- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Homebrew**: [Install Homebrew](https://brew.sh/)
- **Docker Desktop**: [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- **Python 3.11**: `brew install python@3.11`
- **Redis**: `brew install redis && brew services start redis`
- **Supabase CLI**: `brew install supabase/tap/supabase`

### 2. Clone the Repository

```bash
git clone {SUNA_REPO_URL} {SUNA_DIR}
cd {SUNA_DIR}
```

### 3. Configure Environment

Create a `.env` file in the `suna` directory with your API keys. See the Suna Self-Hosting guide for details on the required variables.

### 4. Run Setup

Execute the interactive setup wizard:

```bash
python3 setup.py
```

Follow the prompts to configure the LLM, Supabase, and other services.

### 5. Start Suna AI

```bash
python3 start.py
```

## Troubleshooting on macOS M1 Max

- **Docker Issues**: Ensure Docker Desktop has sufficient memory and CPU allocated. Check the container logs in Docker Desktop for specific errors.
- **`psycopg2` Errors**: If you encounter errors related to `psycopg2` during setup, you may need to install it with some extra flags: `pip install psycopg2-binary`.
- **Performance**: The M1 Max is powerful, but running multiple models and services can be resource-intensive. Monitor your system's activity and adjust Docker's resource limits if needed.

"""

    with open(os.path.join(SUNA_DIR, "README.md"), "w") as f:
        f.write(readme_content)

    print_success("README.md generated successfully.")

def main():
    """Main function to run the setup process."""
    print_info("--- Suna AI Automated Setup for macOS M1 Max ---")

    check_prerequisites()

    api_keys = collect_api_keys()

    manage_suna_repo()

    write_env_file(api_keys)

    guided_setup()

    start_suna()

    generate_readme()

    print_success("Suna AI setup is complete!")
    print_info(f"You can now access the Suna AI UI at: http://localhost:3000")

if __name__ == "__main__":
    main()
