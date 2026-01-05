# antigravity api project

this project consists of a fastapi backend and a react frontend.

## prerequisites

- python 3.8+
- node.js and npm

## installation

### backend setup

1. create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### frontend setup

1. navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. install dependencies:
   ```bash
   npm install
   ```

## running the project

### using the start script

you can run both the backend and frontend simultaneously using the provided shell script from the root directory:

```bash
chmod +x start.sh
./start.sh
```

### manual start

1. start the backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## project structure

- `/crud`: contains backend crud logic
- `/models`: database models definitions
- `/routers`: api route definitions
- `/schemas`: pydantic schemas for data validation
- `/frontend`: react application with vite
- `main.py`: entry point for the fastapi application
- `database.py`: database connection settings
- `start.sh`: helper script to run both applications
