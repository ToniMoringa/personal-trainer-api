from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade="all, delete-orphan")

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False, default=datetime.now().strftime("%Y-%m-%d"))
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    __table_args__ = (db.CheckConstraint('duration_minutes > 0', name='positive_duration'),)
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade="all, delete-orphan")

    @db.validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0: raise ValueError("Duration must be positive.")
        return value

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    __table_args__ = (
        db.CheckConstraint('reps >= 0', name='non_negative_reps'),
        db.CheckConstraint('sets > 0', name='positive_sets'),
    )
    @db.validates('reps', 'sets')
    def validate_metrics(self, key, value):
        if value is not None and value < 0: raise ValueError(f"{key} cannot be negative.")
        return value