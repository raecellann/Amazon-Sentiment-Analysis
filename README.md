# Amazon-Sentiment-Analysis 💭
    This project provides an Amazon product review sentiment analysis tool, using web scraping and natural language processing (NLP). The script scrapes user reviews from Amazon product pages, processes the review data, and performs sentiment analysis to determine an estimated star rating for each review based on the sentiment expressed.

# Key Features: 🟢
    - Web Scraping: The script fetches Amazon product pages and scrapes review data using requests and regular expressions.
    - Sentiment Analysis: Utilizes the VADER sentiment analysis model from the nltk library to analyze the polarity of each review and assign a star rating (1-5) based on sentiment scores.
    - Product Name Extraction: Automatically extracts the product name from the HTML of the product page.
    - Dynamic Review Analysis: Processes and analyzes reviews dynamically based on the input Amazon product link, making it adaptable to any Amazon product page.

# How It Works: 🚧
    - Scraping: The script sends an HTTP request to the provided Amazon product link and scrapes the HTML for product information and user reviews.
    - Review Extraction: Using regular expressions, the script identifies and extracts user reviews from the HTML.
    - Sentiment Analysis: Each review is processed through VADER's sentiment intensity analyzer, producing a compound score that is used to estimate a star rating:
        5 stars for very positive reviews
        4 stars for moderately positive reviews
        3 stars for neutral reviews
        2 stars for moderately negative reviews
        1 star for very negative reviews
    - Review Output: For each review, the sentiment analysis results are printed alongside the review text and an estimated star rating.

# Technologies Used: 👩🏻‍💻
    Python: The core programming language for implementing the web scraper and sentiment analysis logic.
    Requests: For sending HTTP requests and retrieving Amazon page content.
    nltk (VADER): Natural Language Toolkit's VADER model is used for sentiment analysis to classify reviews as positive, negative, or neutral.
    Regular Expressions: For parsing HTML and extracting review data from Amazon's structured content.

### How to Use: ⁉️

1. Clone the repository:

   ```bash
    git clone https://github.com/yourusername/Amazon-Sentiment-Analysis.git

2. Install the required dependencies

    ```bash
    pip install -r requirements.txt

3. Run the Python Script

4. Don't forget to enter the correct Amazon Product Link. 