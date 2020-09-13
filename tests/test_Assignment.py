from unittest import TestCase
from Assignment import *


class TestAssignments(TestCase):
    def test_add(self):
        assignments = Assignments()
        self.assertIsNotNone(assignments)
        assignment1 = Assignment(title="Title1", due_time="2018-01-01")
        assignments.add(assignment1)
        self.assertEqual(assignments[0], assignment1)
        self.assertEqual(len(assignments), 1)
        assignment2 = Assignment(title="Title2", due_time="2018-01-01")
        assignments.add(assignment2)
        self.assertEqual(len(assignments), 2)
        self.assertEqual(assignments[1], assignment2)
        assignments.remove(0)
        self.assertRaises(KeyError, lambda: assignments[0])
        assignment3 = Assignment("Title3", "2018-1-1")
        assignments.add(assignment3)
        self.assertEqual(assignments[0], assignment3)
