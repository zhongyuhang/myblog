import datetime
from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length = 255)
    body = MDTextField(null = True)
    desc = models.TextField(default = '')
    cover = models.ImageField(upload_to = 'images/', default = 'default.jpg')
    views = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    processed_photo = ImageSpecField(
            source="cover",
            processors=[ResizeToFill(750, 375)], # 处理后的图像大小
            format='JPEG',  # 处理后的图片格式
            options={'quality': 98} # 处理后的图片质量
        )
    
    processed_photo_type2 = ImageSpecField(
            source="cover",
            processors=[ResizeToFill(60, 60)], # 处理后的图像大小
            format='JPEG',  # 处理后的图片格式
            options={'quality': 98} # 处理后的图片质量
        )

    def __str__(self):
        return self.title

    class Meta:
    	ordering = ['-created_at']

class Comment(models.Model):
    comment = models.TextField()
    article = models.ForeignKey(Article, on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add = True)
