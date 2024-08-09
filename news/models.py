from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    link = models.URLField()
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return self.title
