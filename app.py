from summarizer_build import *
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route('/summarize/', methods= ['GET', 'POST'])
def first():
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        default_churn = 60

        # Getting original text data from form.
        original_text = request.form.get('original_text', None)

        # Initializing summerizer.
        summarize = Summarizer(original_text, default_churn)

        # Converting original text to word and sentence tokens.
        word_sentence_tokens = summarize.word_sentence_tokenizer()

        # separating word and sentence tokens from word_sentence_tokens tuple.
        sentence_tokens_list = word_sentence_tokens[0]
        word_tokens_list = word_sentence_tokens[1]

        # Calculating word scores, returning word scores and most occuring word.
        word_frequency_scores_topic = word_count_vec(word_tokens_list)
        word_frequency_scores = word_frequency_scores_topic[0]
        topic = word_frequency_scores_topic[1].capitalize()

        # Scoring sentences based on word_frequency_scores.
        sentence_scores = sentence_scoring(sentence_tokens_list, word_frequency_scores)

        # Returning top n sentences in the order which they appear in original text.
        sorted_summary = summarize.summary_sorting(sentence_scores)

        # Swapping selected synonyms and returning final_summary string.
        final_summary = string_synonym_swap(sorted_summary)

        return render_template('test.html', final_summ = final_summary, top = topic, original = original_text)


# run the server. 
if __name__ == '__main__':
    app.run()