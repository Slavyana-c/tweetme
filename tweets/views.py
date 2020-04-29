import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS= settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next")
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse({}, status=201)
        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    # REST API VIEW
    qs = Tweet.objects.all()
    tweets_list = [{'id': x.id, 'content': x.content, "likes": random.randint(0, 100)} for x in qs]
    data = {
        'isUser': False,
        'response': tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    # REST API VIEW

    data = {
        'id': tweet_id,
        # "image_path": obj.image.url
    }
    status = 200

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not found'
        status = 404

    return JsonResponse(data, status=status)
