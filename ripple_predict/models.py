# import the necessary packages
from django.db import models


class SocialMediaPost(models.Model):
    # define the model schema
    post_id = models.CharField(max_length=32, db_index=True)
    text = models.TextField()
    label = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_social_media_post_exists(post_id):
        # the social media post exists in the database if there is already a
        # corresponding entry with the same post ID
        return SocialMediaPost.objects.filter(post_id=post_id).count() > 0

    def __str__(self):
        # return a string representation of the post
        return " : ".join([self.post_id, self.text[:32] + "..."])

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
    experiment = models.CharField(max_length=64, db_index=True)
    response = models.TextField()
    prediction = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_prediction_exist(smp, experiment):
        # return whether a prediction *already* exists in the database for the
        # provided combination of social media post and experiment name
        return Prediction.objects.filter(
            smp=smp,
            experiment=experiment
        ).count() > 0

    def __str__(self):
        # initialize the prediction to be considered "correct"
        label = "correct"

        # if the ground-truth label does not match the predicted label, then
        # update the label
        if self.smp.label != self.prediction:
            label = "incorrect"

        # return a string representation of the prediction
        return " : ".join([
            self.smp.post_id,
            self.experiment,
            "prediction: {} ({})".format(self.prediction, label)
        ])

    class Meta:
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"


class Embedding(models.Model):
    # define the model schema
    smp = models.ForeignKey(
        SocialMediaPost,
        on_delete=models.CASCADE,
        db_index=True
    )
    experiment = models.CharField(max_length=64, db_index=True)
    response = models.TextField()
    embeddings = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_embedding_exist(smp, experiment):
        # return whether an embedding *already* exists in the database for the
        # provided combination of social media post and experiment name
        return Embedding.objects.filter(
            smp=smp,
            experiment=experiment
        ).count() > 0

    def __str__(self):
        # return a string representation of the embedding
        return " : ".join([self.smp.post_id, self.experiment])

    class Meta:
        verbose_name = "Embedding"
        verbose_name_plural = "Embeddings"
