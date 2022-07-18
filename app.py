import requests
import os
from app_functions import get_top_headlines, search_articles
import streamlit as st
from PIL import Image


API_KEY = ""
#add your news API key here
# sample API_KEY = "0123456789"

image = Image.open(r'..\NewsSummary_Streamlit\news_summary_logo.png')

st.image(image, caption='Smart NEWS')

st.sidebar.image(image, use_column_width=True)
search_choice = st.sidebar.radio('', options=['Top Headlines', 'Search Term'])
sentences_count = st.sidebar.slider('Max sentences per summary:', min_value=1,
                                                                  max_value=10,
                                                                  value=3)

if search_choice == 'Top Headlines':   

    st.markdown(
    """
    <style>
    div[role=“listbox”] li: {
    background-color: red;
    }

    div[data-baseweb=“select”] > div {
    background-color: #99cfdd;
    }

    div[data-baseweb=“input”] > div {
    background-color: #99cfdd;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )


    category = st.sidebar.selectbox('Search By Category:', options=['business',
                                                            'entertainment',
                                                            'general',
                                                            'health',
                                                            'science',
                                                            'sports',
                                                            'technology'], index=2)

    summaries = get_top_headlines(sentences_count, apiKey=API_KEY,
                                                   sortBy='publishedAt',
                                                   country='us',
                                                   category=category)


elif search_choice == 'Search Term':
    search_term = st.sidebar.text_input('Enter Search Term:')

    if not search_term:
        summaries = []
        st.write('Please enter a search term =)')
    else:
        summaries = search_articles(sentences_count, apiKey=API_KEY,
                                                     sortBy='publishedAt',
                                                     q=search_term)

for i in range(len(summaries)):
    try:
        st.title(summaries[i]['title'])
        st.write(f"published at: {summaries[i]['publishedAt']}")
        st.write(f"source: {summaries[i]['source']['name']}")
        # img
        url_image = Image.open(requests.get(summaries[i]['urlToImage'], stream=True).raw)
        st.image(url_image, caption='Smart NEWS')
        #####
        st.write(summaries[i]['summary'])
        st.write(f"More details:{summaries[i]['url']}")
    except Exception as e:
        continue
