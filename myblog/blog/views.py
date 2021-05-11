from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from .models import Article
from .models import Comment
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import markdown
import json
from django.urls import reverse
from django.core.cache import cache

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

def work(request):
    return render(request, 'blog/work.html')

def person(request):
    return render(request, 'blog/person.html')

def contact(request):
    return render(request, 'blog/contact.html')

def top(request):
    return render(request, 'blog/top.html')

def header(request):
    return render(request, 'blog/header.html')

def foot(request):
    return render(request, 'blog/foot.html')

def hot_articles():
    md_key = f"most_view_md_{datetime.now().hour}"
    # Adding '-' to the column name indicates that the results are in descending order.
    if cache.has_key(md_key):
        articles = cache.get(md_key)
    else:
        # Hot articles are updated every an hours
        articles = Article.objects.order_by('-views')[:3]
        cache.set(md_key, articles, 60 * 60)
    return articles

class BlogListView(ListView):
    model = Article
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BlogListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['hot_articles'] = hot_articles()
        return context

def detail(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    article.views = F('views') + 1
    article.save()
    article = get_object_or_404(Article, pk = article_id)
    # md_key = f"{article.id}_md_key_{datetime.timestamp(article.created_at)}"
    # if cache.has_key(md_key):
    #     article.body = cache.get(md_key)
    # else:
    #     article.body = markdown.markdown(
    #             article.body,
    #             extensions=[
    #                 'markdown.extensions.extra',
    #                 'markdown.extensions.codehilite',
    #                 'markdown.extensions.toc',
    #             ],
    #             safe_mode = True,
    #             enable_attributes = False
    #         )
    #     cache.set(md_key, article.body, 60*60*24)
    article.body = markdown.markdown(
            article.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ],
            safe_mode = True,
            enable_attributes = False
        )
    comments = article.comments.all()
    return render(request, 'blog/article_detail.html', {'article' : article, 'comments' : comments, 'hot_articles': hot_articles()})

def post_comment(request, article_id):
    comment = request.POST.get('comment')
    if comment:
        Comment.objects.create(comment=comment, article_id=article_id)
    else:
        print("no comment")
    return HttpResponseRedirect(reverse('blog:detail', args=(article_id, )))
