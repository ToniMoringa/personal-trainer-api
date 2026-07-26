from marshmallow import Schema, fields, validate

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int()
    exercise_id = fields.Int(required=True)

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Str(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str()
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, dump_only=True)