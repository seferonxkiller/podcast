from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Episode, Season
from .forms import CommentForm
from blog.models import Tag, Category
from home.models import Like
from django.views.decorators.csrf import csrf_exempt


def index(request):
    episode = Episode.objects.all()
    season = Season.objects.all()
    tags = Tag.objects.all() 
    categories = Category.objects.all()
    tag = request.GET.get('tag')
    cat = request.GET.get('cat')
    q = request.GET.get('q')
    if tag:
        episode = episode.filter(tags__title__exact=tag)
    if cat:
        episode = episode.filter(category__title__exact=cat)
    if q:
        episode = episode.filter(title__icontains=q)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(episode, 3)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    try:
        user_id = request.user.profile.id
    except:
        user_id = None
    my_liked_episodes = Like.objects.filter(author_id=user_id).values_list('episode_id')
    my_liked_episodes_list = [i[0] for i in my_liked_episodes]
    ctx = {
        'episode': page_obj,
        'tags': tags,
        'categories': categories,
        'season': season,
        'my_liked_episodes_list': my_liked_episodes_list
    }
    return render(request, 'episodes.html', ctx)


def episodes_detail(request, pk):
    episode = get_object_or_404(Episode, id=pk)
    tag = Tag.objects.all()
    categories = Category.objects.all()
    try:
        user_id = request.user.profile.id
    except:
        user_id = None
    my_liked_episodes = Like.objects.filter(author_id=user_id).values_list('episode_id')
    my_liked_episodes_list = [i[0] for i in my_liked_episodes]
    form = CommentForm()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse('episodes:detail', kwargs={"pk": pk}))
        form = CommentForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author_id = request.user.id
            obj.article_id = episode.id
            obj.save()
            return redirect('.')
    ctx = {
        "episode": episode,
        "tag": tag,
        "categories": categories,
        "form": form,
        'my_liked_episodes_list': my_liked_episodes_list
    }
    return render(request, 'episode.html', ctx)


def get_ids_list(request):
    episode = Episode.objects.all().order_by('-id')
    ids_list = [i.id for i in episode]
    return JsonResponse({"ids_list": ids_list})


@csrf_exempt
def like(request):
    print('like')
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You should authorize"}, status=401)
    if request.method == 'POST':
        episode_id = int(request.POST.get('episode_id'))
        user_id = request.user.profile.id
        likes = Like.objects.values_list('episode_id', 'author_id')
        print(episode_id)
        print(episode_id, user_id)
        if (episode_id, user_id) in likes:
            Like.objects.get(episode_id=episode_id, author_id=user_id).delete()
            return JsonResponse({"detail": "Un-Liked"})
        Like.objects.create(episode_id=episode_id, author_id=user_id)
        return JsonResponse({"detail": "Liked"})
    return JsonResponse({"detail": "Method not allowed"}, status=405)

