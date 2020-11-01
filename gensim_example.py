import streamlit as st
from htbuilder import div, styles
from htbuilder.units import px
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords, textcleaner

from annotation_helper import annotate

with open("summarization_sample_gensim.txt", "r") as f:
    DEFAULT_TEXT = f.read()

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
COLORS = ["#8ef", "#faa", "#afa", "#fea"]

st.set_page_config(layout="wide")
st.title("Interactive GenSim Summarization")
st.markdown(
"""
Text processing with [gensim](https://radimrehurek.com/gensim/index.html)
"""
)

st.sidebar.title("Configuration")
st.sidebar.subheader(
"""
Summarization Options
"""
)
ratio = st.sidebar.slider('Ratio (Fraction of original sentences in output)', min_value=0.0, max_value=1.0, value=0.2)
word_count = st.sidebar.number_input("Word Count (Maximum words in summary)", min_value=None, max_value=150, step=10, value=50)
split_output = st.sidebar.checkbox("Split Output", value=False)
show_offsets = st.sidebar.checkbox("Show Offsets", value=False)
process_keywords = st.sidebar.checkbox("Process Keywords", value=False)

input_col, result_col = st.beta_columns(2)

input_col.header("Enter text to analyze")
text = input_col.text_area("", DEFAULT_TEXT, height=400)
summary = summarize(text, ratio=ratio, word_count=word_count, split=split_output)

result_col.header("Summary")
result_col.subheader("")
if summary:
    result_col.write(HTML_WRAPPER.format(summary), unsafe_allow_html=True)

if process_keywords:
    st.sidebar.subheader(
        """
        Keyword Options
        """
    )
    keyword_ratio = st.sidebar.slider('Ratio (Fraction of original sentences in output)', min_value=0.0, max_value=1.0,
                                      value=0.2, key="keyword_ratio")
    keyword_word_count = st.sidebar.number_input("Word Count (Maximum words in keywords)", min_value=None,
                                                 max_value=150, step=10, value=50, key="keyword_word_count")
    keyword_split_output = st.sidebar.checkbox("Split Output", value=False, key="keyword_split_output")
    keyword_scores = st.sidebar.checkbox("Return Scores", value=False)
    keyword_lemmatize = st.sidebar.checkbox("Lemmatize Words", value=False)
    keyword_deacc = st.sidebar.checkbox("Remove Accentuation", value=False)
    kw = keywords(text, ratio=keyword_ratio, words=keyword_word_count, split=keyword_split_output, scores=keyword_scores, pos_filter=('NN', 'JJ'), lemmatize=keyword_lemmatize, deacc=keyword_deacc)

    if kw:
        result_col.header("Keywords")
        kw_expander = result_col.beta_expander("Expand keywords!")
        if kw_expander:
            kw_expander.write(HTML_WRAPPER.format(kw), unsafe_allow_html=True)

if show_offsets:
    st.header("Offsets View")
    input_offset_col, result_offset_col = st.beta_columns(2)

    summary_out = div(style=styles(
        font_family="sans-serif",
        line_height="1.5",
        font_size=px(16),
    ))

    summaries = []
    if isinstance(summary, list):
        summaries = summary
    elif isinstance(summary, str):
        summaries = summary.split("\n")

    summary_colors = {}
    for num, summary_item in enumerate(summaries):
        color = COLORS[num%len(COLORS)]
        summary_out(annotate(summary_item, "", color))
        summary_colors[summary_item] = color

    input_out = div(style=styles(
        font_family="sans-serif",
        line_height="1.5",
        font_size=px(16),
    ))

    input_texts = textcleaner.get_sentences(text)
    for input_text in input_texts:
        if input_text in summaries:
            color = summary_colors.get(input_text)
            input_out(annotate(input_text, "", color))
        else:
            input_out(input_text)

    input_offset_col.write(HTML_WRAPPER.format(input_out), unsafe_allow_html=True)
    result_offset_col.write("""<div style="display: block; float:left;">{}</div>""".format(str(summary_out)), unsafe_allow_html=True)
