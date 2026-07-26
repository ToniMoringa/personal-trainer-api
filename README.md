# Personal Trainer Workout API

A backend REST API built with Flask, SQLAlchemy, and Marshmallow designed to manage workout sessions, exercise , and performance metrics.

## Features
Full CRUD operations for workouts and exercises
Many-to-many relationship tracking (reps, sets, duration)
Model-level validation with SQLAlchemy constraints
* **Exercises Management:** Create, view, and delete reusable exercises categorized by functional movement patterns and goals (e.g., glutes/hips, upper body width, core).
* **Workout Tracking:** Log custom workout sessions with durations, dates, and trainer notes.
* **Join Table Relationships:** Link multiple exercises to specific workouts while tracking sets, reps, and time caps.

## Setup & Installation

1. Clone the repository and navigate to the project directory:
   ```bash
    git clone <your-repository-url>
    cd personal-trainer-api
    pipenv install
    pipenv run flask db upgrade
    pipenv run python -m server.seed
    pipenv run flask run --port=5001
    ```

## Testing
```bash
pipenv run python -m unittest server.tests -v
```
