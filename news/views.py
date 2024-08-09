from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
import asyncio
import aiohttp


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

async def fetch_news_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'category']
    ordering_fields = ['date', 'title']

    @action(detail=False, methods=['post'])
    def parse(self, request):
        asyncio.run(self.parse_news(request))
        return Response({"status": "parsing started"})

    async def parse_news(self, request):
        url = 'https://kun.uz/news/list'  # Замените на реальный URL
        data = await fetch_news_data(url)
        for item in data:
            # Преобразование и сохранение данных
            news = News.objects.create(
                title=item['title'],
                text=item['text'],
                link=item['link'],
                date=item['date'],
                category=Category.objects.get_or_create(name=item['category'])[0]
            )
        news.save()
        return Response(data)
