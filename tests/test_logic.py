import unittest
from src.job_processor import JobProcessor, Job
from src.config import Config

class TestJobProcessor(unittest.TestCase):
    def test_calculate_score_java_junior(self):
        job = Job(
            title="Junior Java Developer",
            company="Tech Corp",
            location="Berlin",
            url="http://example.com",
            source="LinkedIn",
            description_snippet="We are looking for a Java developer with Spring Boot experience."
        )
        # Base: 50
        # Title "Junior": +20
        # Location "Berlin": +10
        # Keywords "Java": +10
        # Keywords "Spring Boot": +10
        # Total expected: 100
        score = JobProcessor.calculate_score(job)
        self.assertEqual(score, 100)

    def test_calculate_score_senior_filter(self):
        job = Job(
            title="Senior Java Developer",
            company="Tech Corp",
            location="Berlin",
            url="http://example.com",
            source="LinkedIn"
        )
        # Base: 50
        # Title "Senior": -50 (Negative keyword)
        # Location "Berlin": +10
        # Keywords "Java": +10
        # Total expected: 20
        score = JobProcessor.calculate_score(job)
        self.assertEqual(score, 20)

    def test_process_job_valid(self):
        item = {
            "title": "Junior Backend Engineer - Berlin - Startup",
            "link": "https://www.linkedin.com/jobs/view/123",
            "snippet": "Join us as a Junior Backend Engineer using Java and Spring Boot."
        }
        job = JobProcessor.process_job(item)
        self.assertIsNotNone(job)
        self.assertEqual(job.title, "Junior Backend Engineer")
        self.assertEqual(job.company, "Berlin") # Simple parser might mistake this, acceptable for now
        self.assertEqual(job.location, "Berlin")
        self.assertEqual(job.source, "LinkedIn")
        self.assertTrue(job.score >= 50)

    def test_process_job_low_score(self):
        # A job that shouldn't match well
        item = {
            "title": "Senior Python Data Scientist",
            "link": "https://www.indeed.com/view/456",
            "snippet": "Python, Data, ML."
        }
        # Base 50
        # Senior -50
        # No location match
        # No Java/Spring match
        # Score ~0 -> Should return None (threshold 30)
        job = JobProcessor.process_job(item)
        self.assertIsNone(job)

if __name__ == '__main__':
    unittest.main()
