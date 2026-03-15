import unittest

from tests._runner import run_model_file


EARLY_STOP_MODEL = "tests/models/on_solution/stop_after_three.py"
NATURAL_COMPLETION_MODEL = "tests/models/on_solution/natural_completion.py"
ALL_VARIABLE_TYPES_MODEL = "tests/models/on_solution/all_variable_types.py"


class TestOnSolutionAce(unittest.TestCase):
    def test_on_solution_stop_after_three(self):
        result = run_model_file(EARLY_STOP_MODEL, timeout=180)

        self.assertEqual(result['stop_requested_at'], 3)
        self.assertGreaterEqual(result['callback_count'], 3)
        self.assertIsNotNone(result['last_callback_values'])

        bounds = result['callback_bounds']
        self.assertGreaterEqual(len(bounds), 3)
        self.assertTrue(all(bounds[i] <= bounds[i + 1] for i in range(len(bounds) - 1)))

        self.assertEqual(result['last_callback_values'], result['final_values'])
        self.assertEqual(result['final_objective'], bounds[-1])
        self.assertEqual(result['final_bound'], bounds[-1])

    def test_on_solution_natural_completion(self):
        result = run_model_file(NATURAL_COMPLETION_MODEL, timeout=120)

        self.assertGreaterEqual(result['callback_count'], 1)
        self.assertIsNotNone(result['last_callback_values'])
        self.assertEqual(result['last_callback_values'], result['final_values'])

        bounds = result['callback_bounds']
        self.assertTrue(all(bounds[i] <= bounds[i + 1] for i in range(len(bounds) - 1)))
        self.assertEqual(result['final_objective'], bounds[-1])
        self.assertEqual(result['final_bound'], bounds[-1])

    def test_on_solution_all_variable_types(self):
        result = run_model_file(ALL_VARIABLE_TYPES_MODEL, timeout=120)

        self.assertGreaterEqual(result['callback_count'], 1)
        self.assertIsNotNone(result['last_callback'])

        callback = result['last_callback']
        self.assertEqual(callback['inst_iv'], result['final_iv'])
        self.assertEqual(callback['inst_sv'], result['final_sv'])
        self.assertEqual(callback['inst_ia'], result['final_ia'])
        self.assertEqual(callback['inst_sa'], result['final_sa'])

        callback_bound = callback['bound']
        self.assertEqual(callback_bound, result['final_bound'])


if __name__ == '__main__':
    unittest.main()
