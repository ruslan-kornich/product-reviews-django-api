import os
import csv
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_reviews.settings")
django.setup()

from api.models import Product, Review


def parse_and_save_data():
    # Path to the folder with CSV files
    data_folder = os.path.join(settings.BASE_DIR, "data")

    # Parsing the Products.csv file
    with open(
        os.path.join(data_folder, "Products.csv"), "r", encoding="utf-8"
    ) as products_file:
        products_reader = csv.DictReader(products_file)
        for row in products_reader:
            product, created = Product.objects.get_or_create(
                title=row["Title"], asin=row["Asin"]
            )

    # Parsing Reviews.csv file
    with open(
        os.path.join(data_folder, "Reviews.csv"), "r", encoding="utf-8"
    ) as reviews_file:
        reviews_reader = csv.DictReader(reviews_file)
        for row in reviews_reader:
            product = Product.objects.get(asin=row["Asin"])
            review = Review.objects.create(
                product=product, title=row["Title"], review=row["Review"]
            )


if __name__ == "__main__":
    parse_and_save_data()
