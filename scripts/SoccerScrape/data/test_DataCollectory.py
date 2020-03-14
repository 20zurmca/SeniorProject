import unittest
import DataCollector

class TestDataCollector(unittest.TestCase):
    
    def test_patriot_data_collection(self):
        dc = DataCollector()
        dc.extract_prior_patriot_league_conference_data()
        print('test_prior_patriot_data_collection: Data extracted')
        
    
    
if __name__ == '__main__':
    unittest.main()