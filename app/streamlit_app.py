import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Review Scraper",
    page_icon="📊",
    layout="wide"
)

def create_rating_chart(reviews):
    df = pd.DataFrame(reviews)
    rating_counts = df['rating'].value_counts().sort_index()
    fig = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        labels={'x': 'Rating', 'y': 'Count'},
        title='Rating Distribution'
    )
    return fig

st.title("Review Scraper")

url = st.text_input("Enter URL to scrape reviews from:")

if st.button("Scrape Reviews"):
    if url:
        with st.spinner("Scraping reviews..."):
            response = requests.get(f"http://localhost:5000/api/reviews?page={url}")
            if response.status_code == 200:
                data = response.json()
                reviews = data['reviews']
                
                st.success(f"Found {len(reviews)} reviews across {data['pages_scraped']} pages")
                
                # Display reviews
                st.subheader("Reviews")
                df = pd.DataFrame(reviews)
                st.dataframe(df)
                
                # Display rating distribution
                st.subheader("Rating Distribution")
                st.plotly_chart(create_rating_chart(reviews))
            else:
                st.error("Failed to scrape reviews. Please try again.")
    else:
        st.warning("Please enter a URL")