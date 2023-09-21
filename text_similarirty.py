# https://www.nltk.org/
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# https://pypi.org/project/Unidecode/
from unidecode import unidecode
import string
# https://www.sbert.net/
from sentence_transformers import SentenceTransformer, util
from text_extraction import text_recognition
from metric import Metric

class TextSimilarity(Metric):
    """
    Metric: Text Similarity
    """
    
    def __init__(self, id, filename, img_string):
        """
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        super().__init__(id, filename, img_string)
    
    def execute_metric(self):
        """
        Execute the metric.

        Returns:
            average_text_similarity: float.  Average Text Similarirty value
        """        
        print("start computing text similarity ...")
        texts = text_recognition(self.filename)
        comparing_sentence = 'predicted impact'
        comparing_sentence_two = 'impact uncertainty level' # the keyword chosen from specification
        sentence2_processed = self.pre_process(comparing_sentence)
        sentence3_processed = self.pre_process(comparing_sentence_two)
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        embedding_2 = model.encode(sentence2_processed, convert_to_tensor=True)
        embedding_3 = model.encode(sentence3_processed, convert_to_tensor=True)
        value_list = []
        for text in texts:
            if text != '':
                #do not calculate the simialrity if the string is actually a number
                if not text.isnumeric():
                    sentence = text
                    sentence_processed = self.pre_process(sentence)
                    embedding_1= model.encode(sentence_processed, convert_to_tensor=True)
                    
                    cosine_value_predicted = util.pytorch_cos_sim(embedding_1, embedding_2)
                    consine_value_uncertainty = util.pytorch_cos_sim(embedding_1, embedding_3)
                    if consine_value_uncertainty > cosine_value_predicted:
                        value_list.append(consine_value_uncertainty.item())
                    else:
                        value_list.append(cosine_value_predicted.item())
                        
        average_text_similarity = float(sum(value_list)) / len(value_list)

        return average_text_similarity
    
    def pre_process(self, corpus):
        """
        Initiate the metric calculation
        
        Args:
            corpus: str. The input str to be tokenized
            
        Returns:
            corpus: str. The tokenized str

         """

        corpus = corpus.lower()
        stopset = stopwords.words('english') + list(string.punctuation)
        corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
        corpus = unidecode(corpus)
        return corpus
    