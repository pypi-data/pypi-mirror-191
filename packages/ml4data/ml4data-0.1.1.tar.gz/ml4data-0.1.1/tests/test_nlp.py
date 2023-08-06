import os
import unittest
from ml4data import NLPClient

class NLPTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = NLPClient(os.environ['API_KEY'])
        
    def assertIsConfidence(self, value: float):
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 1)
    
    def test_guess_gender(self):
        response = self.client.guess_gender('Amanda Gris')
        self.assertIn('firstNames', response)
        self.assertIn('lastNames', response)
        self.assertIn('gender', response)
        
    def test_analyze_sentiment(self):
        response = self.client.analyze_sentiment('Este cine no esta bueno porque era muy sucio')
        self.assertEqual(response['class'], 'neg')
        self.assertIsConfidence(response['negativeConfidence'])
        self.assertIsConfidence(response['neutralConfidence'])
        self.assertIsConfidence(response['positiveConfidence'])
        self.assertEqual(response['negativeConfidence'] + response['neutralConfidence'] + response['positiveConfidence'], 1)
    
    def test_detect_language(self):
        response = self.client.detect_language('This is text is written in english')
        self.assertEqual(response['language'], 'en')
        self.assertIsConfidence(response['confidenceScore'])
    
    def test_extract_entities(self):
        text = 'Net income was $9.4 million compared to the prior year of $2.7 million.'
        response = self.client.extract_entities(text)
        for entity in response:
            entity_text = text[entity['startIndex']:entity['endIndex']+1]
            self.assertEqual(entity_text, entity['entityText'])
    
    def test_extract_keyphrases(self):
        text = 'AI Platform Pipelines has two major parts'
        response = self.client.extract_keyphrases(text)
        for keyphrase in response:
            self.assertIn(keyphrase.lower(), text.lower())
            
    def test_classify_product(self):
        response = self.client.classify_product('Nike')
        self.assertIsConfidence(response['confidenceScore'])
        
    def test_analyze_company(self):
        response = self.client.analyze_company('Facebook')
        for suggestion in response['otherSuggestions']:
            self.assertIsConfidence(suggestion['confidenceScore'])
            
            
        
if __name__ == '__main__':
    unittest.main()