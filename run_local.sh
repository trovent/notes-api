# run application locally
# Usage: ./run_local.sh
# This script is used to run the application locally.
# It sets up the environment and starts the application.
# Check if the script is being run from the correct directory
if [ ! -d "app" ]; then
    echo "Please run this script from the root directory of the project."
    exit 1
fi
# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate the virtual environment before running this script."
    echo "Create a virtual environment with 'python3 -m venv venv' and activate it with 'source venv/bin/activate'."
    exit 1
fi

# run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000

