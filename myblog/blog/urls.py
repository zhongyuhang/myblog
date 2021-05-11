from . import views
from django.urls import path, include

app_name = 'blog'
urlpatterns = [
    # localhost:8000/blog/
    path('', views.index, name='index'),
    path('work/', views.work, name = 'work'),
    path('person/', views.person, name = 'person'),
    path('article-list/', views.BlogListView.as_view(), name = 'article-list'),
    path('contact/', views.contact, name = 'contact'),
    path('<int:article_id>/', views.detail, name = 'detail'),
    path('post_comment/<int:article_id>', views.post_comment, name = 'post_comment'),
]
