from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaulttags import register
import datetime
from .models import *
# Create your views here.


@login_required
def index(request):
    user = request.user
    total_tweets = TweetTag.objects.filter(user__id=user.id).count()
    total_classified = TweetTag.objects.filter(user__id=user.id, classification__isnull=False).count()
    total_relevant = TweetTag.objects.filter(user__id=user.id, classification__key='RELEVANT').count()
    total_news = TweetTag.objects.filter(user__id=user.id, classification__key='NEWS').count()
    total_noise = TweetTag.objects.filter(user__id=user.id, classification__key='NOISE').count()
    progress = "%.1f%%" % (100*float(total_classified)/total_tweets)
    context = {
        'total_tweets':total_tweets,
        'total_relevant': total_relevant,
        'total_classified': total_classified,
        'total_news': total_news,
        'total_noise': total_noise,
        'progress': progress
    }

    if user.is_superuser:
        all_users_progress = []
        users = User.objects.all().order_by("username")
        for user in users:
            total_tweets = TweetTag.objects.filter(user__id=user.id).count()
            if int(total_tweets) == 0:
                continue
            total_classified = TweetTag.objects.filter(user__id=user.id, classification__isnull=False).count()
            progress = "%.1f%%" % (100 * float(total_classified) / total_tweets)
            name = user.first_name + " " + user.last_name
            all_users_progress.append((name, total_tweets, total_classified, progress))
        context["all_users_progress"] = all_users_progress

    return render(request, 'manual_tagging/index.html', context=context)


@login_required
def save_tags(request):
    for name in request.POST.keys():
        if "classification_tag_" in name:
            tag_id = int(name.split("_")[-1])
            tag = get_object_or_404(TweetTag, pk=tag_id)
            if tag.user.id != request.user.id:
                return HttpResponseRedirect(reverse('manual_tagging:index'))
            classification = get_object_or_404(TweetClassification, pk=int(request.POST[name]))
            tag.classification = classification
            tag.last_update = datetime.datetime.now()
            tag.save()
    return HttpResponseRedirect(reverse('manual_tagging:next_tweets', kwargs={'size': request.POST['size']}))


@login_required
def next_tweets(request, size):
    size = int(size)
    size = max(10, min(size, 100))  # size will be always between 10 and 100 (inclusive)
    empty_tags = TweetTag.objects.filter(user__id=request.user.id, classification=None, last_update=None)[:size]
    classifications = TweetClassification.objects.all().order_by('label')
    context = {'tags': empty_tags, 'classifications': classifications, 'size': size}
    return render(request, 'manual_tagging/next_tweets.html', context)


@login_required
def latest_classified(request):
    user_id = request.user.id
    last = TweetTag.objects.filter(user__id=user_id, classification__isnull=False).order_by("-last_update")[:100]
    context = {'last': last}
    return render(request, 'manual_tagging/latest_classified.html', context)


@login_required
def save_single_tag(request):
    for name in request.POST.keys():
        if "classification_tag_" in name:
            tag_id = int(name.split("_")[-1])
            tag = get_object_or_404(TweetTag, pk=tag_id)
            if tag.user.id != request.user.id:
                return HttpResponseRedirect(reverse('manual_tagging:index'))
            classification = get_object_or_404(TweetClassification, pk=int(request.POST[name]))
            tag.classification = classification
            tag.last_update = datetime.datetime.now()
            tag.save()
    return HttpResponseRedirect(reverse('manual_tagging:latest_classified'))


@login_required
def load_single_tag(request, tag_id):
    tag = get_object_or_404(TweetTag, pk=tag_id)
    classifications = TweetClassification.objects.all().order_by('label')
    context = {'tag': tag, 'classifications': classifications}
    return render(request, 'manual_tagging/single_tweet.html', context)







