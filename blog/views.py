from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm

from .models import Tag, Category, Blog, Comment


def index(request):
    blogs = Blog.objects.order_by('-id')
    tags = Tag.objects.all()
    categories = Category.objects.all()
    tag = request.GET.get('tag')
    cat = request.GET.get('cat')
    d = request.GET.get('d')
    if tag:
        blogs = blogs.filter(tags__title__exact=tag)
    if cat:
        blogs = blogs.filter(category__title__exact=cat)
    if d:
        blogs = blogs.filter(title__icontains=d)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(blogs, 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    ctx = {
        'blogs': page_obj,
        'tags': tags,
        'categories': categories,
    }
    return render(request, 'blog.html', ctx)


def detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    articles = Blog.objects.all()
    comments = Comment.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular_posts = Blog.objects.order_by('-id')[:3]
    form = CommentForm()
    if request.method == "POST":
        # if not request.user.is_authenticated:
        #     return redirect("account:login")
        form = CommentForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = request.user.id
            obj.article_id = blog.id
            obj.save()
            return redirect('.')
    ctx = {
        'object': blog,
        'categories': categories,
        'tags': tags,
        'popular_posts': popular_posts,
        'form': form,
        'articles': articles,
        'comments': comments

    }
    return render(request, 'detail.html', ctx)
