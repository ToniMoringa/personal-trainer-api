import unittest
from server.app import app, db
from server.models import Workout

class TestWorkoutAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_invalid_workout_returns_400(self):
        """Ensure negative duration is rejected by model validation"""
        response = self.app.post('/workouts', json={"duration_minutes": -5})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_get_workouts_empty_returns_200(self):
        """Ensure GET endpoint works even with no data"""
        response = self.app.get('/workouts')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()