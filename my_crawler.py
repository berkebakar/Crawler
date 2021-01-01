import csv
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# Author: Berke Bakar
url = "https://www.trustradius.com/machine-learning"


def main():
    file = open("output.csv", "w")  # open output file
    writer = csv.writer(file, lineterminator="\n")  # create a csv writer
    writer.writerow(["productName", "ratings", "reviews", "stars"])  # write the column titles

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}  # headers for http request
    request = Request(url, headers=headers)
    page = urlopen(request)  # request page we want to scrap from
    html_data = page.read().decode("utf-8")  # read and decode data to a readable format

    soup = BeautifulSoup(html_data, "html.parser")  # we use beautifulSoup for parsing html contents

    product_card_list = soup.find(id="product_card_list")  # find the search result list div
    product_divs = product_card_list.select("div[class*=CategoryProduct_category-product-card__]")  # extract the divs that include product related divs

    for product in product_divs:
        title = product.select("div[class*=CategoryProduct_category-product-heading__]")[0]['title']  # select the correct div and extract the title attribute
        # initializing variables
        rating_count = 0
        review_count = 0
        star_count = 0
        rating_count_divs = product.select("div[class*=CategoryProduct_rating-count__]")  # selecting div that includes rating and review div

        if len(rating_count_divs) != 0:  # some products do not have reviews or ratings, so we have to check
            rating_div = rating_count_divs[0]  # first div contains rating count
            review_div = rating_count_divs[1]  # second div contains review count
            rating_count = int(rating_div.text.split(" ")[0])  # extract rating count from div and cast to integer
            review_count = int(review_div.text.split(" ")[0])  # extract review count from div and cast to integer

        stars_div = product.find(class_="trust-score__stars").find_all(class_="star")  # every product has star rating, find the divs that describe the star point

        for div in stars_div:  # for every star div in a product check if it is a full star or half star, increment star_count accordingly
            if "-full" in div['class']:
                star_count += 1
            elif "-half" in div['class']:
                star_count += 0.5

        writer.writerow([title, rating_count, review_count, star_count])  # write the results to output file

    return


if __name__ == '__main__':
    main()
