# https://www.nltk.org/
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# https://pypi.org/project/Unidecode/
from unidecode import unidecode
import string
#https://www.sbert.net/
from sentence_transformers import SentenceTransformer, util
import csv
#https://scipy.org/
from scipy.stats import pearsonr


def execute_test_text_similarity():
    ground_truth_list = []
    estimated_target_list = []
    #download the sts-test.tsv from https://gluebenchmark.com/tasks, the task name is 'Semantic Textual Similarity Benchmark'
    # but the benchmark file can be found in the test folder
    ground_truth_list = []
    estimated_target_list = []
    with open("./test/sts-test.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            if len(row) == 7:
                ground_truth = float(int(float(row[4]))/5)
                ground_truth_list.append(ground_truth)
                sentence_1 = row[5]
                sentence_2 = row[6]
                consine_value = similarity(sentence_1, sentence_2)
                estimated_target_list.append(consine_value)

    #compute pearson similarity
    corr, p_value= pearsonr(estimated_target_list, ground_truth_list)
    
    test_description = 'corr:' + str(corr) + ' p_value:' + str(p_value)
    return test_description




def similarity(text, text_2):        
    print("start computing cosine similarity ...")
    sentence_processed = pre_process(text)
    sentence2_processed = pre_process(text_2)
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embedding_1= model.encode(sentence_processed, convert_to_tensor=True)
    embedding_2 = model.encode(sentence2_processed, convert_to_tensor=True)

    cosine_value = util.pytorch_cos_sim(embedding_1, embedding_2)


    return cosine_value.item()
                    
def pre_process(corpus):
    corpus = corpus.lower()
    stopset = stopwords.words('english') + list(string.punctuation)
    corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
    corpus = unidecode(corpus)
    return corpus

