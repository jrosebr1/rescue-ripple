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
        return " : ".join([self.post_id, self.text[:32]])

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

    @staticmethod
    def is_prediction_exist(smp, experiment):
        # grab all predictions from the database for the provided combination of
        # social media post and experiment name
        predictions = Prediction.objects.filter(smp=smp, experiment=experiment)

        # return whether a prediction *already* exists in the database for this
        # combination
        return len(predictions) > 0

    class Meta:
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
