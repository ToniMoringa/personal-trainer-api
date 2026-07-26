import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'instance', 'app.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    return jsonify(workout_schema.dump(Workout.query.get_or_404(id))), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.json)
        new_workout = Workout(**data)
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(workout_schema.dump(new_workout)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return jsonify(exercise_schema.dump(Exercise.query.all(), many=True)), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    return jsonify(exercise_schema.dump(Exercise.query.get_or_404(id))), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.json)
        new_exercise = Exercise(**data)
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    try:
        data = workout_exercise_schema.load(request.json)
        join_entry = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(join_entry)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(join_entry)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)