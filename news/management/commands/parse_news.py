from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import requests
from news.models import Category, News
from datetime import datetime


class Command(BaseCommand):
    help = 'Parses the latest news from kun.uz and saves them to the database'

    def handle(self, *args, **kwargs):
        url = "https://kun.uz/news/list"
        response = requests.get(url)
        webpage = response.content

        soup = BeautifulSoup(webpage, "html.parser")
        news_items = soup.find_all("div", class_="small-cards__default-item")

        with transaction.atomic():
            for item in news_items:
                time_and_category = item.find("div", class_="gray-text").get_text(strip=True)
                title = item.find("a", class_="small-cards__default-text").get_text(strip=True)
                link = item.find("a", class_="small-cards__default-text")["href"]
                full_link = f"https://kun.uz{link}"

                category_name, time = time_and_category.split(" | ")

                current_date = datetime.now().date()  # Assuming the date is today
                time_obj = datetime.strptime(time, "%H:%M").time()
                date_time = datetime.combine(current_date, time_obj)

                category, created = Category.objects.get_or_create(name=category_name)

                # Проверяем, существует ли новость с такой ссылкой
                if not News.objects.filter(link=full_link).exists():
                    # Получаем полный текст статьи
                    article_response = requests.get(full_link)
                    article_page = article_response.content
                    article_soup = BeautifulSoup(article_page, "html.parser")

                    # Извлекаем текст статьи без тегов HTML
                    content_div = article_soup.find("div", class_="news-inner__content-page")
                    article_text = ""
                    if content_div:
                        paragraphs = content_div.find_all("p")
                        article_text = "<br>".join([p.get_text(strip=True) for p in paragraphs])

                    news = News(
                        title=title,
                        text=article_text,
                        link=full_link,
                        date=date_time,
                        category=category
                    )
                    news.save()
                    self.stdout.write(self.style.SUCCESS(f"Saved news: {title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"News already exists: {title}"))
