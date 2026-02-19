import unittest
from unittest.mock import patch, MagicMock
# We need to mock the PROFILE load before importing JobProcessor, 
# but JobProcessor imports Config which imports PROFILE.
# So we might need to patch 'src.config.PROFILE'

from src.job_processor import JobProcessor, Job
from src.config import Config

class TestJobProcessor(unittest.TestCase):
    def test_calculate_score_java_junior(self):
        # We rely on the actual profile.yaml for this test unless we mock it.
        # Assuming profile.yaml has "Java", "Spring Boot", "Junior" with positive weights.
        
        job = Job(
            title="Junior Java Developer",
            company="Tech Corp",
            location="Berlin",
            url="http://example.com",
            source="LinkedIn",
            description_snippet="We are looking for a Java developer with Spring Boot experience."
        )
        # Base: 50
        # Title "Junior": +10 (from profile.yaml target_roles or experience)
        # Location "Berlin": +10
        # Keywords "Java": +10
        # Keywords "Spring Boot": +10
        # Total expected: 90 or more (depending on exact weights in yaml)
        
        score = JobProcessor.calculate_score(job)
        self.assertTrue(score >= 80, f"Score {score} should be high")

    def test_calculate_score_senior_filter(self):
        job = Job(
            title="Senior Java Developer",
            company="Tech Corp",
            location="Berlin",
            url="http://example.com",
            source="LinkedIn"
        )
        # Base: 50
        # Title "Senior": -50 or (Negative keyword)
        # Location "Berlin": +10
        # Keywords "Java": +10
        # Total expected: Low
        score = JobProcessor.calculate_score(job)
        self.assertTrue(score < 50, f"Score {score} should be low due to Senior title")

    def test_process_job_valid(self):
        item = {
            "title": "Junior Backend Engineer - Berlin - Startup",
            "link": "https://www.linkedin.com/jobs/view/123",
            "snippet": "Join us as a Junior Backend Engineer using Java and Spring Boot."
        }
        job = JobProcessor.process_job(item)
        self.assertIsNotNone(job)
        self.assertEqual(job.title, "Junior Backend Engineer")
        self.assertEqual(job.location, "Berlin")

if __name__ == '__main__':
    unittest.main()
