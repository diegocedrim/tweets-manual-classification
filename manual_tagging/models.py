from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.


@python_2_unicode_compatible
class TweetDataset(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TweetClassification(models.Model):
    key = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=200)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Tweet(models.Model):
    id_from_twitter = models.CharField(max_length=200)
    text = models.TextField()
    previous_classification = models.ForeignKey(TweetClassification, on_delete=models.CASCADE)
    dataset = models.ForeignKey(TweetDataset, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class TweetTag(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    classification = models.ForeignKey(TweetClassification, on_delete=models.CASCADE, null=True)
    last_update = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        if self.classification is not None:
            return "%s classified %s as %s" % (self.user.username, self.tweet.text, self.classification.label)
        else:
            return "%s need to classify %s" % (self.user.username, self.tweet.text)