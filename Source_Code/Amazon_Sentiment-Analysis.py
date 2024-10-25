import requests
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

class AmazonReviewAnalyzer:

    def __init__(self, website_link):
        self.website_link = website_link
        self.headers_for_request = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Referer': 'http://www.google.com/',
        }

    def load_page(self):
        try:
            response = requests.get(self.website_link, headers=self.headers_for_request)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None

    def extract_product_name(self, page_source):
        product_name_pattern = r'<span id="productTitle"[^>]*>(.*?)</span>'
        match = re.search(product_name_pattern, page_source)
        if match:
            return match.group(1).strip()
        return "Product name not found."

    def find_review_area(self, page_source):
        review_section_pattern = r'class="cr-widget-FocalReviews"([\s\S]*)'
        return re.search(review_section_pattern, page_source)

    def extract_reviews_from_area(self, review_section):
        review_pattern = r'<div\sclass="a-row a-spacing-small review-data">([\s\S]*?)<\/div>'
        reviews = re.findall(review_pattern, review_section.group(1))
        return reviews

    def extract_review_message(self, single_review_block):
        review_message_pattern = r'<span>([\s\S]*?)<\/span>'
        match = re.search(review_message_pattern, single_review_block)
        return match.group(1).replace("<br />", " ").strip() if match else None

    def gather_reviews(self, page_source):
        all_reviews = []
        review_section = self.find_review_area(page_source)
        if review_section:
            review_blocks = self.extract_reviews_from_area(review_section)
            for block in review_blocks:
                review_message = self.extract_review_message(block)
                if review_message:
                    all_reviews.append(review_message)
        return all_reviews

    def calculate_star_rating(self, sentiment_scores):
        compound_score = sentiment_scores['compound']
        if compound_score > 0.75:
            return 5
        elif 0.5 < compound_score <= 0.75:
            return 4
        elif -0.1 <= compound_score <= 0.5:
            return 3
        elif -0.5 <= compound_score < -0.1:
            return 2
        else:
            return 1

    def analyze_reviews(self, reviews):
        sia = SentimentIntensityAnalyzer()
        for review in reviews:
            print('━━━━━━━━━━━━━━━━━━━━━━')
            print(f"Review: {review}")

            user_rating = sia.polarity_scores(review)
            sentiment = "Positive" if user_rating['compound'] >= 0.05 else "Negative" if user_rating['compound'] <= -0.05 else "Neutral"

            print(f"Sentiment Scores: {user_rating}")
            print(f"Review Sentiment: {sentiment}")

            predicted_rating = self.calculate_star_rating(user_rating)
            print(f"Star Rating: {predicted_rating} stars")
            print('――――――――――――――――――――――――――――――――――――――――――――――')

REQUEST_URL = 'https://www.amazon.com/QEEIG-Floating-Shelves-Bathroom-Farmhouse/dp/B09T66W5D1/ref=sr_1_4?dib=eyJ2IjoiMSJ9.5XAwrJdUG3hQaLhulEB1euKQBtNV06NlnOG4zrrXXiW-oXAGiOIZ3aAvCH8zLdZEqcjMioAstQ5BEcI0cD31i0C8QJ9TIOwp0tilVk0Jb5PithiqvDG6LN4klPP76eEIKxJ__biNDAWwk0Dae1vEpeeA6tm-6sWTjYIKbaiW2TqnkYu1b_nHpNR5AcN1JG5F8YnIAqEx1gZ6TJiA131NL7tVA4NE2BKkS6g_r_5H8s1lP9e-boi312l46FFAE6idrurRVYYJ_3hGu71K6YgXgFDomGSjHNAcHQI5en64_uY.zP9HFccPBV2w0h6VWNRQYEHw3rMGNNPDFgGVq4f0rOA&dib_tag=se&keywords=Shelves&pf_rd_p=3bfbee16-7af3-47c3-b4e4-8cb236780a84&pf_rd_r=4X1FW8F4YESMAQ161YVK&qid=1729258473&s=furniture&sr=1-4'

if __name__ == '__main__':
    user_input = input("Enter the Amazon Product link: \n")
    REQUEST_URL = user_input.strip() or REQUEST_URL

    analyzer = AmazonReviewAnalyzer(REQUEST_URL)
    page_content = analyzer.load_page()

    if page_content:
        product_name = analyzer.extract_product_name(page_content)
        print(f"\nProduct Name: {product_name}")

        reviews = analyzer.gather_reviews(page_content)
        if reviews:
            analyzer.analyze_reviews(reviews)
        else:
            print("No reviews found.")
