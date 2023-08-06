import os

import spacy

from typing import List, Dict

# for en_core_web_trf to work properly
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class Nlp:

    MODEL_DICT = {
        'small':   'en_core_web_sm',
        'large':   'en_core_web_lg',
        'roberta': 'en_core_web_trf'
    }

    ENTITIES = {
        'PERSON': 'People, including fictional.',
        'NORP': 'Nationalities or religious or political groups.',
        'FAC': 'Buildings, airports, highways, bridges, etc.',
        'ORG': 'Companies, agencies, institutions, etc.',
        'GPE': 'Countries, cities, states.',
        'LOC': 'Non-GPE locations, mountain ranges, bodies of water.',
        'PRODUCT': 'Objects, vehicles, foods, etc. (Not services.)',
        'EVENT': 'Named hurricanes, battles, wars, sports events, etc.',
        'WORK_OF_ART': 'Titles of books, songs, etc.',
        'LAW': 'Named documents made into laws.',
        'LANGUAGE': 'Any named language.',
        'DATE': 'Absolute or relative dates or periods.',
        'TIME': 'Times smaller than a day.',
        'PERCENT': 'Percentage, including ”%“.',
        'MONEY': 'Monetary values, including unit.',
        'QUANTITY': 'Measurements, as of weight or distance.',
        'ORDINAL': '“first”, “second”, etc.',
        'CARDINAL': 'Numerals that do not fall under another type.'
    }

    class Model:

        @staticmethod
        def get(
              # model_name: str = 'en_core_web_sm') -> 'spacy ner model':
              model_name: str = 'en_core_web_sm'):
            nlp = spacy.load(model_name)
            return nlp

    class LabeledTokens:

        @staticmethod
        def get(
              doc: str,
              # model: 'spacy model') -> List[Dict[str, str]]:
              model) -> List[Dict[str, str]]:

            out = model(doc)
            d_labeled_tokens = {(e.text, e.label_) for e in out.ents}
            a_labeled_tokens = list(d_labeled_tokens)
            return a_labeled_tokens

    @classmethod
    def get(
          cls,
          doc: str,
          model_name: str = 'en_core_web_sm') -> List[Dict[str, str]]:

        model = cls.Model.get(model_name)
        out = cls.LabeledTokens(model, doc)
        return out

    @staticmethod
    def extract(
          # inp: 'output of spacy model',
          inp,
          entity: str) -> set:
        ret_lis = []
        for i in filter(lambda x: x.label_ == entity, inp.ents):
            ret_lis.append(i.text)
        return set(ret_lis)
