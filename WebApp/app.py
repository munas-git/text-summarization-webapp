from summarizer_build import *
from flask import Flask, render_template, request


app = Flask(__name__)
app.secret_key = 'forsummary'
UPLOAD_FOLDER = '../docUpload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods= ['GET'])
def index():
    return render_template('index.html')


@app.route('/text-summary', methods= ['GET', 'POST'])
def text_summary():
    if request.method == 'GET':
        return render_template('textSummary.html')
    elif request.method == 'POST':
        # Getting original text data and churn_level from form.
            original_text = request.form.get('original_text')
            churn_level = float(request.form.get('churn_level'))

            # Initializing summarizer.
            summarize = Summarizer(original_text, churn_level)

            # Converting original text to word and sentence tokens.
            word_sentence_tokens = summarize.word_sentence_tokenizer()
            
            try:
                # separating word and sentence tokens from word_sentence_tokens tuple.
                sentence_tokens_list = word_sentence_tokens[0]
                word_tokens_list = word_sentence_tokens[1]

                # Calculating word scores, returning word scores and most occuring word.
                word_frequency_scores_topic = word_count_vec(word_tokens_list)
                word_frequency_scores = word_frequency_scores_topic[0]
                topic_1 = word_frequency_scores_topic[1].capitalize()
                topic_2 = word_frequency_scores_topic[2].capitalize()

                # Scoring sentences based on word_frequency_scores.
                sentence_scores = sentence_scoring(sentence_tokens_list, word_frequency_scores)

                # Returning top n sentences in the order which they appear in original text.
                sorted_summary = summarize.summary_sorting(sentence_scores)

                # Swapping selected synonyms and returning final_summary string.
                final_summary = string_synonym_swap(sorted_summary)

                # Getting final details
                summary_length = len(final_summary)
                original_text_length = len(original_text)
                # topic_2 = topic_2,

                return render_template('result.html', final_summary = final_summary, topic_1 = topic_1, topic_2 = topic_2, original_text = original_text, summary_length = summary_length, original_text_length = original_text_length)
            except Exception:
                # Returns 'Summary Undetermined' to the final-summary field and 'Undetermined' for other summary information.
                message_2 = "Undetermined"
                return render_template('textSummary.html', final_summary = "Summary Undetermined", topic = message_2, original_text = original_text, summary_length = message_2, original_text_length = message_2)


@app.route("/doc-summary/", methods= ['GET', 'POST'])
def doc_summary():
    if request.method == "GET":
        return render_template("docSummary.html")
    elif request.method == "POST":
        # Getting document and churn level from form
        doc = request.files['uploadFile']
        churn_level = float(request.form.get('churn_level'))

        # Checking file extention
        if doc.filename.split(".")[-1] == "txt":
            original_text = extract_txt(doc)
        elif doc.filename.split(".")[-1] in ["doc", "docx"]:
            original_text = extract_docx(doc)

        # Initializing summarizer.
        summarize = Summarizer(original_text, churn_level)

        # Converting original text to word and sentence tokens.
        word_sentence_tokens = summarize.word_sentence_tokenizer()
        
        try:
            # separating word and sentence tokens from word_sentence_tokens tuple.
            sentence_tokens_list = word_sentence_tokens[0]
            word_tokens_list = word_sentence_tokens[1]

            # Calculating word scores, returning word scores and most occuring word.
            word_frequency_scores_topic = word_count_vec(word_tokens_list)
            word_frequency_scores = word_frequency_scores_topic[0]
            topic_1 = word_frequency_scores_topic[1].capitalize()
            topic_2 = word_frequency_scores_topic[2].capitalize()

            # Scoring sentences based on word_frequency_scores.
            sentence_scores = sentence_scoring(sentence_tokens_list, word_frequency_scores)

            # Returning top n sentences in the order which they appear in original text.
            sorted_summary = summarize.summary_sorting(sentence_scores)

            # Swapping selected synonyms and returning final_summary string.
            final_summary = string_synonym_swap(sorted_summary)

            # Getting final details
            summary_length = len(final_summary)
            original_text_length = len(original_text)

            return render_template('result.html', final_summary = final_summary, topic_1 = topic_1, topic_2 = topic_2, original_text = original_text, summary_length = summary_length, original_text_length = original_text_length)
        except Exception:
            # Returns 'Summary Undetermined' to the final-summary field and 'Undetermined' for other summary information.
            message_2 = "Undetermined"
            return render_template('textSummary.html', final_summary = "Summary Undetermined", topic = message_2, original_text = original_text, summary_length = message_2, original_text_length = message_2)


@app.route("/about/", methods= ["GET"])
def about():
    return render_template("about.html")


# run the server. 
if __name__ == '__main__':
    app.run(debug=False, port='0.0.0.0')