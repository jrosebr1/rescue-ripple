# import the necessary packages
from django.db import models


class SocialMediaPost(models.Model):
    # define the model schema
    post_id = models.CharField(max_length=32, db_index=True)
    text = models.TextField()
    label = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return a string representation of the post
        return "{} : {}".format(self.post_id, self.text[:32])

    class Meta:
        verbose_name = "SocialMediaPost"
        verbose_name_plural = "SocialMediaPosts"


class Prediction(models.Model):
    # define the model schema
    smp = models.ForeignKey(
        SocialMediaPost,
        on_delete=models.CASCADE,
        db_index=True
    )
    algo = models.CharField(max_length=64, db_index=True)
    response = models.TextField()
    prediction = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)
