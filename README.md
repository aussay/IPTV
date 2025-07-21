# Suna AI Automated Setup for macOS M1 Max

This repository contains a Python script to automate the local setup of Suna AI on a MacBook Pro M1 Max.

## Features

- **Prerequisite Checks**: Verifies the installation of `git`, `brew`, Docker, and Python 3.11.
- **Automated Installation**: Installs `redis` and the Supabase CLI if they are not present.
- **Guided Setup**: Provides step-by-step instructions for the interactive `setup.py` wizard.
- **LLM Integration**: Configures Suna AI to use a local LLama 3 model.
- **Environment Configuration**: Creates a `.env` file with the necessary API keys.
- **Idempotent**: The script can be run multiple times without causing issues.

## How to Use

1.  **Ensure Prerequisites**:
    *   Make sure you have `git` and `brew` installed.
    *   Install and start Docker Desktop.
    *   Have your LLama 3 model running and accessible via a local API endpoint.

2.  **Run the Script**:
    Open your terminal and run the following command:

    ```bash
    python3 suna_setup.py
    ```

3.  **Follow the Prompts**:
    The script will guide you through the setup process. You will be asked to provide API keys and to follow instructions for the interactive `setup.py` wizard.

## Manual Setup

If you prefer to set up Suna AI manually, you can follow the instructions in the `README.md` file that will be generated in the `suna` directory after you run the script.

## Architectural Choices

*   **Interactive Guidance for `setup.py`**: The `setup.py` script for Suna AI is an interactive wizard. Instead of attempting to programmatically pipe inputs to this script (which can be fragile), this setup script provides clear, step-by-step instructions to the user. This approach is more robust and ensures that the user can correctly configure the setup, especially when dealing with complex options like custom LLM providers.
*   **Single Script**: The entire automation is contained within a single Python script for simplicity and ease of use. This avoids the need for complex project structures or multiple files.
*   **Idempotency**: The script is designed to be idempotent, meaning it can be run multiple times without causing errors. It checks for existing installations and repositories to avoid duplicate actions.
*   **LLM Integration**: The script specifically addresses the integration of a local LLama 3 model by configuring the `.env` file to use LiteLLM with a custom base URL. This is a key requirement of the task and is handled in a way that is both automated and transparent to the user.
*   **Security**: API keys are collected interactively and stored in a `.env` file, which is a standard and secure way to manage sensitive information. The user is also warned not to commit this file to version control.
