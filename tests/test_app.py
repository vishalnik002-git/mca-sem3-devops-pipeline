import os
import tempfile
import unittest

class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        import app as module
        self.module = module
        self.previous = module.DB
        module.DB = __import__('pathlib').Path(self.temp.name) / 'test.db'
        self.client = module.app.test_client()

    def tearDown(self):
        self.module.DB = self.previous
        self.temp.cleanup()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'DevOps Control Center',response.data)

    def test_health(self):
        data = self.client.get('/api/health').json
        self.assertEqual(data['status'],'healthy')

    def test_initial_stats(self):
        self.assertEqual(self.client.get('/api/stats').json['total'],0)

    def test_invalid_kind(self):
        self.assertEqual(self.client.post('/api/runs',json={'kind':'unknown'}).status_code,400)

    def test_docker_blocked_by_default(self):
        if os.environ.get('ENABLE_DOCKER_BUILDS') != '1':
            self.assertEqual(self.client.post('/api/runs',json={'kind':'docker'}).status_code,403)

    def test_runs_empty(self):
        self.assertEqual(self.client.get('/api/runs').json['runs'],[])

if __name__ == '__main__':
    unittest.main()
