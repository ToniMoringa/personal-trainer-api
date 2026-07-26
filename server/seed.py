from server.app import app, db
from server.models import Exercise, Workout, WorkoutExercise

def seed_data():
    with app.app_context():
        if Exercise.query.first() is None:
            exercises = [
                Exercise(name="Hip Thrusts", category="glutes_hips", equipment_needed=True),
                Exercise(name="Lat Pulldowns", category="upper_body_width", equipment_needed=True),
                Exercise(name="Oblique Twists", category="core", equipment_needed=False),
                Exercise(name="Chest Press", category="anterior_chain", equipment_needed=True),
                Exercise(name="Romanian Deadlifts", category="posterior_chain", equipment_needed=True),
            ]
            db.session.add_all(exercises)
            db.session.commit()

            workout = Workout(date="2026-07-27", duration_minutes=45, notes="Leg day focus")
            db.session.add(workout)
            db.session.commit()

            link = WorkoutExercise(
                workout_id=workout.id, 
                exercise_id=1, 
                reps=12, 
                sets=4
            )
            db.session.add(link)
            db.session.commit()
            print("(❁´◡`❁) Database seeded successfully!")
        else:
            print("️ Database already contains data. Skipping seed.")

if __name__ == '__main__':
    seed_data()