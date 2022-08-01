# Importing important libraries.
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from string import punctuation
punctuation = punctuation + '’'
from words_synonyms import words_synonyms


class Summarizer():
    '''
    Class containing functions to clean, format and summarize text
    Parameters:
    > self : text, type - string
    > self : churn_level float specifying percentage of original content to capture
    '''


    def __init__ (self, text, churn_level):
        self.text = text
        self.churn_level = float(churn_level)
        self.text_topic = '' # List that will contain string topics.

    
    def word_sentence_tokenizer(self):
        """ 
        This function breaks text into word and sentence tokens   
        
        Parameters:

        > self : text, type -string
        > self : churn_level float specifying percentage of original content to capture

        return:

        (sent_tokens, word_tokens) : Tuple containing sentences (sentence tokens) and
        texts (text tokens) contained in text provided
        """

        sent_tokens = sent_tokenize(self.text, 'english')
        word_tokens = word_tokenize(self.text, 'english')
        return(sent_tokens, word_tokens)

    
    def word_count_vec(self, word_tokens):
        '''
         This function produces a dictionary containing the normalized scores of each word tokens in a list
         
         Parameters:
         
         > word_tokens = [] # List of words
         
         return:

         word_frequency_scores : Dictionary of word tokens and their normalized scores

        '''
        clean_words = []
        word_frequency_scores = {}

        # Looping through to calculate word frequencies
        for word in word_tokens:
            if word.strip().lower() not in stop_words:
                if word not in punctuation:
                    clean_words.append(word)
                    if word not in word_frequency_scores:
                        word_frequency_scores[word] = 1
                    else:
                        word_frequency_scores[word] += 1
        
        # Looping through to normalize word_frequency_scores using linear / minmax scaler
        max_frequency = max(word_frequency_scores.values())
        min_frequency = min(word_frequency_scores.values())
        for word in word_frequency_scores.keys():
            word_frequency_scores[word] = (word_frequency_scores[word] - min_frequency) / (max_frequency - min_frequency)

        topic = max(word_frequency_scores, key=word_frequency_scores.get)
        self.text_topic += topic
        return(word_frequency_scores)
    

    def sentence_scoring(self, sentence_tokens, word_frequency_scores):
        '''
        This function calculates scores for each sentence and returns a dictionary containing sentence, score and order.
        
        Parameters:

        > sentence_tokens: List containing sentence tokens
        > word_frequency_scores: Dictionary containing word tokens and their (normalized) scores

        return:

        sentence_scores : Dictionary of sentences and their scores.

        '''
        sentence_scores = {}
        for sentence in sentence_tokens:
            for word in word_tokenize(sentence, 'english'):
                if word.lower() in word_frequency_scores.keys():
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequency_scores[word.lower()]
                    else:
                        sentence_scores[sentence] += word_frequency_scores[word.lower()]
        return(sentence_scores)

        
    def summary_sorting(self, sentence_scores):
        '''
        This function selects the top n sentences based on the sentence scores
        then organizes the final sentence in asccending order of how they appeared in original text

        Parameters:

        self:churn_level - percentage of original content to capture
        sentence_scores - Dictionary containing sentences and their scores.

        return:

        final_summary : String of final / formatted summary output.
        '''

        order_sorted_sentences = []
        score_sorted_sentences = []
        sentence_score_order_tuples = []

        # multiplying churn level by number of sentences then converting to integer 
        top_n_sentences = int(self.churn_level * len(sentence_scores.keys()))

        order = 1
        # sort all sentences in descending order of their sentence_score values
        for sentence, score in sentence_scores.items():
            sentence_score_order_tuples.append((sentence, score, order))
            order += 1
        score_sorted_sentences = sorted(sentence_score_order_tuples, key=lambda tup: tup[1], reverse=True)
        # Slicing from first to top_n_sentences and appending result to produce final summary.
        top_n_slice = score_sorted_sentences[0:top_n_sentences]
        order_sorted_sentences = sorted(top_n_slice, key=lambda tup: tup[2], reverse=False)
        final_summary_list = [sentence[0] for sentence in order_sorted_sentences]
        final_sorted_summary_string = ' '.join(final_summary_list)
        return(final_sorted_summary_string)


def extract_txt(document):
    """
    Function to extract text from .txt file extension document

    Parameters:
    
    > Document with file extension .txt
    
    return:
    
    full_text_string : String of text contained in the .txt document provided
    """
    with open(document) as text:
        full_text_string = text.read().replace("\n", '')
        return(full_text_string)
    

def string_synonym_swap(text):
    """
    This function converts strings to their synonyms    
    It also returns text containing CAPITAL letters or ending with 's', 'ing' , 'ed' as they are,
    including some specified texts whose synonyms are relative to how they appear in sentences.

    Parameters:
    
    > text_list : Strings to be converted to synonyms

    return:

    > test_synonyms : Synonym converted string of text provided. 
    """
    synonyms = [] # final list of synonyms with first index
    text_list = text.split()
    
    for text in text_list:
        text = text.replace('”', '').replace('“', '') # This helps to conquer the problem behing reported speech "This is reported speech content being altered."
        try:
            if text.islower() and len(text) >= 3:
                synonyms.append(words_synonyms[text])
            elif text in stop_words or text in punctuation or len(text) <3:
                synonyms.append(words_synonyms[text])
            else:
                synonyms.append(text)
        except Exception:
            synonyms.append(text)
        
        # Loops through each token, checks if the token is a punctuation. if it is not a punctuation, it appends the token with a space before to the string-text body
        # if the token is a punctuation, it appens the token to the text body without a space before.
        # 'what is that?' will appear as 'what is that ? ' if this for loop didn't exist.
        string = ''
        for token in synonyms:
            if token not in punctuation:
                string += ' '+token
            else:
                string += token 
    return(string.strip())