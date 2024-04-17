from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    asin = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.product.title}"
