from django.db import models

# Create your models here.
class Page(models.Model):
    pageid = models.IntegerField(primary_key=True)
    page_name = models.CharField(max_length=100)
    page_content = models.TextField()
