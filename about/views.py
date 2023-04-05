from django.shortcuts import render
from blog.models import Blog
from contact.forms import SubForm
from home.models import Like
from episodes.models import Episode


def index(request):
    podcast_count = Episode.objects.all().count()
    blog_count = Blog.objects.all().count()
    like_count = Like.objects.all().count()
    forms = SubForm(request.POST or None)
    if forms.is_valid():
        forms.save()
    ctx = {
        "podcast_count": podcast_count,
        "blog_count": blog_count,
        "like_count": like_count,
    }
    return render(request, 'about.html', ctx)
