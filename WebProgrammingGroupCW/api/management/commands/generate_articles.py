
import json
from django.core.management.base import BaseCommand
from faker import Faker
from ...models import NewsArticle, Category

class Command(BaseCommand):
    help = 'Generate and add articles for each category'

    def handle(self, *args, **options):
        categories = Category.objects.all()

        articles_data = {}

        fake = Faker()

        for category in categories:
            articles_data[category.id] = []

            for _ in range(10):
                title = fake.sentence()
                content = fake.text()
                article = NewsArticle.objects.create(title=title, content=content, category=category)
                articles_data[category.id].append({'id': article.id, 'title': title, 'content': content})

        # Save articles_data as JSON or perform other actions
