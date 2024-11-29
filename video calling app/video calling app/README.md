# Project Setup Instructions

## Prerequisites

Before running the project, ensure your system meets the following requirements:

- **Python**: Latest version installed
- **pip**: Latest version installed

## Setup Guide

### Step 1: Install virtualenv

Run the following command to install the virtual environment tool:
``pip install virtualenv``


### Step 2: Create a Virtual Environment
Use the following command to create a virtual environment named env:
``virtualenv env``

### Step 3: Configure Script Execution Permissions
To allow running external scripts, follow these steps:
1. Open PowerShell as Administrator.
``Set-ExecutionPolicy unrestricted``
2. When prompted, type A (Yes to All) and press Enter.

### Step 4: Activate the virtual environment
Ensure you activate your virtual environment
``.\env\Scripts\activate.ps1``

### Step 5: Install Required Dependencies
Install all required dependencies by running:
``pip install -r requirements.txt``

### Step 6: Run the Application
Start the application using:
``python m2m.py``

### Step 7: Start the application
Once the application is running, open your browser and navigate to:
http://localhost:5000/
