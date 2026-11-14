import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(len(result['customer_hubs']),1)
        self.assertEqual(len(result['links']),1)
        self.assertEqual([r['status'] for r in result['satellites']],['new','shipped'])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['records'].append({'customer':'c1','order':'o1','status':'new','loaded_at':'2025-01-04'})
        self.assertEqual([r['status'] for r in run(data)['satellites']], ['new','shipped','new'])
        data['records'] = []
        self.assertEqual(run(data)['satellites'], [])


if __name__ == '__main__':
    unittest.main()
