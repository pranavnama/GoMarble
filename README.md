# Review Scraper

## Overview

The Review Scraper is a web application designed to extract product reviews from e-commerce websites. It uses web scraping techniques to gather reviews, ratings, and reviewer information, and presents this data in a user-friendly format. This project is built using Python, Flask, and Selenium, and it provides a simple API for extracting reviews from specified URLs.

## Technologies Used

- **Python**: The primary programming language used for the backend.
- **Flask**: A lightweight web framework for building the API.
- **Selenium**: A web automation tool used for scraping data from web pages.
- **Streamlit**: A framework for building interactive web applications in Python.
- **Pandas**: A data manipulation library used for handling and displaying review data.
- **Plotly**: A graphing library used for visualizing data.
- **Gemini API**: A generative AI API used to analyze HTML content and extract CSS selectors for scraping.

## Features

- Extracts reviews, ratings, and reviewer names from specified product pages.
- Provides an API endpoint to request reviews from a given URL.
- Displays the extracted reviews and their distribution in a web application.
- Handles pagination to scrape multiple pages of reviews.
- Utilizes the Gemini API to dynamically generate CSS selectors for scraping.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.7 or higher
- pip (Python package installer)
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)
- An API key for the Gemini API (sign up at [Gemini API](https://gemini.com) to obtain your key)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/review-scraper.git
   cd review-scraper
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver**:
   - Download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/downloads).
   - Ensure that the ChromeDriver executable is in your system's PATH or specify its location in the code.

### Configuration

1. **Set Up Configuration**:
   - Open `app/config.py` and set the `CHROME_DRIVER_PATH` to the location of your ChromeDriver executable.
   - Set your Gemini API key in `app/config.py`:
     ```python
     GEMINI_API_KEY = 'your_gemini_api_key_here'
     ```

### Running the Application

1. **Start the Flask API**:
   ```bash
   python app/main.py
   ```

2. **Start the Streamlit App**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

3. **Access the Application**:
   - Open your web browser and go to `http://localhost:8501` to access the Streamlit application.

### Using the Application

1. **Enter the URL**:
   - In the Streamlit app, enter the URL of the product page you want to scrape reviews from.

2. **Scrape Reviews**:
   - Click the "Scrape Reviews" button. The application will extract reviews and display them in a table format.

3. **View Rating Distribution**:
   - The application will also show a bar chart representing the distribution of ratings.

## API Endpoint

### Extract Reviews

- **Endpoint**: `/api/reviews`
- **Method**: `GET`
- **Query Parameter**: `page` (the URL of the product page to scrape)

**Example Request**:
```
GET http://localhost:5000/api/reviews?page=http://example.com/product
```

**Response**:
```json
{
  "reviews_count": 5,
  "reviews": [
    {
      "title": "Best sheets ever",
      "body": "These sheets are incredibly soft and comfortable.",
      "rating": 5,
      "reviewer": "N C."
    },
    ...
  ]
}
```
