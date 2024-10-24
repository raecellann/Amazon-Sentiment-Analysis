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
        response = requests.get(self.website_link, headers=self.headers_for_request)
        return response.text

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
        return re.findall(review_pattern, review_section.group(1))

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

    def calculate_star_rating(self, user_review):
        compound_score = user_review['compound']
        if compound_score >= 0.75:
            return 5
        elif compound_score >= 0.25:
            return 4
        elif compound_score >= 0:
            return 3
        elif compound_score >= -0.25:
            return 2
        else:
            return 1

    def analyze_reviews(self, reviews):
        sia = SentimentIntensityAnalyzer()
        for review in reviews:
            print('━━━━━━━━━━━━━━━━━━━━━━')
            print(review)
            user_rating = sia.polarity_scores(review)
            rating = self.calculate_star_rating(user_rating)
            print(f"Rating: {round(rating)}")
            print('――――――――――――――――――――――――――――――――――――――――――――――')

if __name__ == '__main__':
    link = input("Enter the Amazon Product link: \n")

    analyzer = AmazonReviewAnalyzer(link)
    page_content = analyzer.load_page()

    product_name = analyzer.extract_product_name(page_content)

    print(f"\nProduct Name: {product_name}")

    reviews = analyzer.gather_reviews(page_content)
    if reviews:
        analyzer.analyze_reviews(reviews)
    else:
        print("No reviews found.")
