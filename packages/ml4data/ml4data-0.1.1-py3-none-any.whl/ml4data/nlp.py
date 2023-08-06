from typing import Dict, Union

from ml4data.base import ML4DataClient
from enum import Enum

class Lang(Enum):
    ENGLISH = 'en'
    SPANISH = 'es'

class NLPClient(ML4DataClient):
    base_url = ML4DataClient.base_url + '/text'

    def guess_gender(self, name: str):
        """ Guess the gender of any given name

        Parameters:
            name (str): Name to guess gender
        """
        return self._post('/gender-guesser',
                          params={'name': name})

    def analyze_sentiment(self, text: str) -> Dict:
        """ Analyze sentiment of a given text

        Parameters:
            text (str): Text to analyze sentiment
        """
        return self._get('/sentiment',
                         params={'text': text})

    def detect_language(self, text: str) -> Dict:
        """ Detect the language of a given text

        Parameters:
            text (str): Text to detect language
        """
        return self._get('/language',
                         params={'text': text})

    def extract_entities(self,
                         text: str,
                         lang: Union[str, Lang] = Lang.ENGLISH) -> Dict:
        """ Extracts entities of a given text

        Parameters:
            text (str): Text to extract entities
            lang (str or `nlp.Lang`): Language of given text
        """
        return self._get('/ner',
                         params={'text': text,
                                 'lang': Lang(lang)})

    def extract_keyphrases(self, text: str) -> Dict:
        """ Extracts keyphrases of a given text

        Parameters:
            text (str): Text to extract keyphrases
        """
        return self._get('/keyphrases',
                         params={'text': text})

    def classify_product(self, text) -> Dict:
        """ Classify product given a text description

        Parameters:
            text (str): Text to classify
        """
        return self._get('/products',
                         params={'text': text})

    def classify_supermarket_product(self, text) -> Dict:
        """ Classify product given a text description

        Parameters:
            text (str): Text to classify
        """
        return self._get('/products/supermarket',
                         params={'text': text})

    def analyze_company(self, name) -> Dict:
        """ Analyze a company by the name

        Parameters:
            text (str): Company name
        """
        return self._get('/company-guesser',
                         params={'name': name})
