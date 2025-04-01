import spacy
import benepar
import warnings
import spacy_transformers
from nltk.corpus import cmudict
import logging
logger = logging.getLogger("CustomLogger")


class NLPmodel:
    """
    NLP Model Singleton that loads and manages multiple SpaCy models,
    Benepar for constituency parsing, and the CMU Pronouncing Dictionary.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._nlp_models = {}
            cls._instance._tokenizer = None
            cls._instance._cmu_dict = None
            cls._instance.load_nlp()
        return cls._instance


    def load_nlp(self, model_name="en_core_web_trf"):
        """
        Lazy-loads a specified SpaCy model with optional Benepar for constituency parsing.

        Args:
            model_name (str): Name of the SpaCy model to load. Defaults to "en_core_web_trf".

        Returns:
            spacy.Language: Loaded SpaCy language model.
        """
        if model_name not in self._nlp_models:
            self._nlp_models[model_name] = spacy.load(model_name)

            # Add Benepar (works with both Transformer and non-Transformer models)
            if "benepar" not in self._nlp_models[model_name].pipe_names:
                try:
                    self._nlp_models[model_name].add_pipe("benepar", config={"model": "benepar_en3"})
                except Exception as e:
                    logger.warning(f"Failed to add Benepar to {model_name}: {e}")

        logger.info(f"Successfully loaded {model_name} into NLPModel.")

        
    def get_nlp(self, model_name="en_core_web_trf"):
        if model_name not in self._nlp_models:
            self.load_nlp(model_name)
        return self._nlp_models[model_name]


    def get_tokenizer(self, model_name="en_core_web_trf"):
        """
        Retrieves the tokenizer from the specified SpaCy model.

        Args:
            model_name (str): Name of the SpaCy model to use. Defaults to "en_core_web_trf".

        Returns:
            spacy.tokenizer.Tokenizer: The tokenizer instance.
        """
        if model_name not in self._nlp_models:
            self.get_nlp(model_name)  # Ensure the model is loaded before accessing tokenizer

        return self._nlp_models[model_name].tokenizer


    def get_cmu_dict(self):
        """
        Lazy-loads the CMU Pronouncing Dictionary.

        Returns:
            dict: CMU Pronouncing Dictionary.
        """
        if self._cmu_dict is None:
            self._cmu_dict = cmudict.dict()
        return self._cmu_dict


# class NLPmodel:
#     """
#     NLP Model Singleton that loads and manages multiple SpaCy models,
#     Benepar for constituency parsing, and the CMU Pronouncing Dictionary.
#     """
#     _nlp_models = {}  # Dictionary to store multiple loaded models
#     _tokenizer = None
#     _cmu_dict = None

#     @classmethod
#     def get_nlp(cls, model_name="en_core_web_trf"):
#         """
#         Lazy-loads a specified SpaCy model with optional Benepar for constituency parsing.

#         Args:
#             model_name (str): Name of the SpaCy model to load. Defaults to "en_core_web_trf".

#         Returns:
#             spacy.Language: Loaded SpaCy language model.
#         """
#         if model_name not in cls._nlp_models:
#             cls._nlp_models[model_name] = spacy.load(model_name)

#             # Add Benepar (works with both Transformer and non-Transformer models)
#             if "benepar" not in cls._nlp_models[model_name].pipe_names:
#                 try:
#                     cls._nlp_models[model_name].add_pipe("benepar", config={"model": "benepar_en3"})
#                 except Exception as e:
#                     logger.warning(f"Failed to add Benepar to {model_name}: {e}")

#         logger.info(f"Successfully loaded {model_name} into NLPModel.")
#         return cls._nlp_models[model_name]

#     @classmethod
#     def get_tokenizer(cls, model_name="en_core_web_trf"):
#         """
#         Retrieves the tokenizer from the specified SpaCy model.

#         Args:
#             model_name (str): Name of the SpaCy model to use. Defaults to "en_core_web_trf".

#         Returns:
#             spacy.tokenizer.Tokenizer: The tokenizer instance.
#         """
#         if model_name not in cls._nlp_models:
#             cls.get_nlp(model_name)  # Ensure the model is loaded before accessing tokenizer

#         return cls._nlp_models[model_name].tokenizer

#     @classmethod
#     def get_cmu_dict(cls):
#         """
#         Lazy-loads the CMU Pronouncing Dictionary.

#         Returns:
#             dict: CMU Pronouncing Dictionary.
#         """
#         if cls._cmu_dict is None:
#             cls._cmu_dict = cmudict.dict()
#         return cls._cmu_dict



# class NLPmodel:
#     """
#     NLP Model Singleton that loads and manages SpaCy, Benepar, and CMU Pronouncing Dictionary.
#     """
#     _nlp = None
#     _tokenizer = None
#     _cmu_dict = None

#     @classmethod
#     def get_nlp(cls):
#         """
#         Lazy-loads the SpaCy model with Benepar for constituency parsing.
#         Suppresses PyTorch warnings related to TreeCRF.

#         Returns:
#             spacy.Language: Loaded SpaCy language model.
#         """
#         if cls._nlp is None:
#             cls._nlp = spacy.load("en_core_web_lg")

#             # Ensure Benepar is registered before adding
#             if not hasattr(benepar, "BeneparComponent"):
#                 raise ImportError("Benepar is not properly installed or registered!")

#             if "benepar" not in cls._nlp.pipe_names:
#                 cls._nlp.add_pipe("benepar", config={"model": "benepar_en3"})
                
#         return cls._nlp

#     @classmethod
#     def get_tokenizer(cls):
#         """
#         Lazy-loads the SpaCy tokenizer.

#         Returns:
#             spacy.tokenizer.Tokenizer: The tokenizer instance.
#         """
#         if cls._tokenizer is None:
#             cls._tokenizer = cls.get_nlp().tokenizer
#         return cls._tokenizer
    
#     @classmethod
#     def get_cmu_dict(cls):
#         """
#         Lazy-loads the CMU Pronouncing Dictionary.

#         Returns:
#             dict: CMU Pronouncing Dictionary.
#         """
#         if cls._cmu_dict is None:
#             cls._cmu_dict = cmudict.dict()
#         return cls._cmu_dict
