# Notebook API

A RESTful API for managing notes built with FastAPI and SQLite.

## Features

- Create, read, update, and delete notes
- Notes support title, content, category, icons, and due dates
- SQLite database for storage
- CORS enabled for frontend integration

## Running Locally

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
```

2. Install dependencies:
```bash
pip install -r app/requirements.txt
```

3. Run the application:
```bash
./run_local.sh
```

The API will be available at `http://localhost:8000`

The docs of the API will be available at `http://localhost:8000/docs`. You can execute the methods directly from here for testing.


## Running with Docker

### Prerequisites

- Docker
- Docker Compose (optional)

### Using Docker

1. Build the image:
```bash
./build.sh
```

2. Run the container:
```bash
./up.sh
```

The API will be available at `http://localhost:8000`

The docs of the API will be available at `http://localhost:8000/docs`. You can execute the methods directly from here for testing.

## API Endpoints

- `GET /notes` - Get all notes
- `GET /notes/{id}` - Get a specific note
- `POST /notes` - Create a new note
- `PUT /notes/{id}` - Update a note
- `DELETE /notes/{id}` - Delete a note

## Example Note Format

```json
{
  "title": "Shopping List",
  "content": "Milk, Bread, Eggs",
  "category": "personal",
  "icon": "🛒",
  "duedate": "2025-05-10"
}
```

**Hints:** 
- you can use and interpret the icon field as you like. E.g. you can put unicode icons into it or encode png icons in base64 format.
- the values of category, icon and duedate are optional
