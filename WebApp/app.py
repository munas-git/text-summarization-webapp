from summarizer_build import *
from flask import Flask, render_template, request


app = Flask(__name__)
app.secret_key = 'forsummary'


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
            sum_type = int(request.form.get(sum_type))

            # Initializing summarizer.
            summarize = Summarizer(original_text, churn_level)

            # Converting original text to word and sentence tokens.
            word_sentence_tokens = summarize.word_sentence_tokenizer()
            
            try:
                # Extractve summary
                if sum_type == 0:
                    # separating word and sentence tokens from word_sentence_tokens tuple.
                    sentence_tokens_list = word_sentence_tokens[0]
                    word_tokens_list = word_sentence_tokens[1]

                    # Calculating word scores, returning word scores and most occuring word.
                    word_frequency_scores_topic = word_count_vec(word_tokens_list)
                    word_frequency_scores = word_frequency_scores_topic[0]
                    topic_1 = word_frequency_scores_topic[1].title()
                    topic_2 = word_frequency_scores_topic[2].title()

                    # Scoring sentences based on word_frequency_scores.
                    sentence_scores = sentence_scoring(sentence_tokens_list, word_frequency_scores)

                    # Returning top n sentences in the order which they appear in original text.
                    sorted_summary = summarize.summary_sorting(sentence_scores)

                    # Swapping selected synonyms and returning final_summary string.
                    final_summary = string_synonym_swap(sorted_summary)

                    # Getting final details
                    summary_length = len(final_summary.split())
                    original_text_length = len(original_text.split())

                    # Language detection
                    lang = lang_detect([original_text.lower()])
                
                else: 
                    # Abstractive summary
                    final_summary = abs_summary(original_text, churn_level)

                    # Other info
                    summarize = Summarizer(original_text, churn_level)

                    # Converting original text to word and sentence tokens.
                    word_sentence_tokens = summarize.word_sentence_tokenizer()

                    # separating word and sentence tokens from word_sentence_tokens tuple.
                    sentence_tokens_list = word_sentence_tokens[0]
                    word_tokens_list = word_sentence_tokens[1]

                    # Calculating word scores, returning word scores and most occuring word.
                    word_frequency_scores_topic = word_count_vec(word_tokens_list)
                    word_frequency_scores = word_frequency_scores_topic[0]
                    topic_1 = word_frequency_scores_topic[1].title()
                    topic_2 = word_frequency_scores_topic[2].title()

                    # Getting final details
                    summary_length = len(final_summary.split())
                    original_text_length = len(original_text.split())

                    # Language detection
                    lang = lang_detect([original_text.lower()]) 
                    
                return render_template('result.html', final_summary = final_summary, topic_1 = topic_1, topic_2 = topic_2, original_text = original_text, summary_length = summary_length, original_text_length = original_text_length, lang_ = lang)
            except Exception:
                # Returns 'Summary Undetermined' to the final-summary field and 'Undetermined' for other summary information.
                message = "invalid"
                return render_template('textSummary.html', message_= message)


@app.route("/doc-summary/", methods= ['GET', 'POST'])
def doc_summary():
    if request.method == "GET":
        return render_template("docSummary.html")
    elif request.method == "POST":
        
        try:
            # Getting document and churn level from form
            doc = request.files['uploadFile']
            churn_level = float(request.form.get('churn_level'))
            sum_type = int(request.form.get(sum_type))

            # Checking file extention
            if doc.filename.split(".")[-1] == "txt":
                original_text = extract_txt(doc)
            elif doc.filename.split(".")[-1] in ["doc", "docx"]:
                original_text = extract_docx(doc)

            # Extractve summary
            if sum_type == 0:
                # Initializing summarizer.
                summarize = Summarizer(original_text, churn_level)

                # Converting original text to word and sentence tokens.
                word_sentence_tokens = summarize.word_sentence_tokenizer()

                # separating word and sentence tokens from word_sentence_tokens tuple.
                sentence_tokens_list = word_sentence_tokens[0]
                word_tokens_list = word_sentence_tokens[1]

                # Calculating word scores, returning word scores and most occuring word.
                word_frequency_scores_topic = word_count_vec(word_tokens_list)
                word_frequency_scores = word_frequency_scores_topic[0]
                topic_1 = word_frequency_scores_topic[1].title()
                topic_2 = word_frequency_scores_topic[2].title()

                # Scoring sentences based on word_frequency_scores.
                sentence_scores = sentence_scoring(sentence_tokens_list, word_frequency_scores)

                # Returning top n sentences in the order which they appear in original text.
                sorted_summary = summarize.summary_sorting(sentence_scores)

                # Swapping selected synonyms and returning final_summary string.
                final_summary = string_synonym_swap(sorted_summary)

                # Getting final details
                summary_length = len(final_summary.split())
                original_text_length = len(original_text.split())

                # Language detection + file format validation
                lang = lang_detect([original_text.lower()])
            else:
                # Abstractive summary
                final_summary = abs_summary(original_text, churn_level)

                # Other info
                summarize = Summarizer(original_text, churn_level)

                # Converting original text to word and sentence tokens.
                word_sentence_tokens = summarize.word_sentence_tokenizer()

                # separating word and sentence tokens from word_sentence_tokens tuple.
                sentence_tokens_list = word_sentence_tokens[0]
                word_tokens_list = word_sentence_tokens[1]

                # Calculating word scores, returning word scores and most occuring word.
                word_frequency_scores_topic = word_count_vec(word_tokens_list)
                word_frequency_scores = word_frequency_scores_topic[0]
                topic_1 = word_frequency_scores_topic[1].title()
                topic_2 = word_frequency_scores_topic[2].title()

                # Getting final details
                summary_length = len(final_summary.split())
                original_text_length = len(original_text.split())

                # Language detection
                lang = lang_detect([original_text.lower()])

            return render_template('result.html', final_summary = final_summary, topic_1 = topic_1, topic_2 = topic_2, original_text = original_text, summary_length = summary_length, original_text_length = original_text_length, lang_ = lang)
        except Exception:
            message = "invalid"
            return render_template('docSummary.html', message_= message)


@app.route("/about/", methods= ["GET"])
def about():
    return render_template("about.html")


# run the server. 
if __name__ == '__main__':
    app.run(debug=False)