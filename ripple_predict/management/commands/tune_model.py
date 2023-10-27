# USAGE
# python manage.py tune_model --train ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_train.tsv --dev ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_dev.tsv --test ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_test.tsv --experiment test-ada-002

# import the necessary packages
from django.core.management.base import BaseCommand
from ripple_predict.models import Embedding
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import json


class Command(BaseCommand):

    # define the SVM hyperparameters to tune
    SVM_PARAMS = {
        "C": [0.001, 0.01, 0.1, 1, 10, 100],
        "penalty": ["l1", "l2"],
        "loss": ["hinge", "squared_hinge"],
    }

    # explain what this script does
    help = "Performs hyperparameter tuning on tweet classifiers"

    def add_arguments(self, parser):
        # path to input training HumAID TSV containing tweet IDs
        parser.add_argument(
            "-t",
            "--train",
            type=str,
            required=True,
            help="path to HumAID training TSV file"
        )

        # path to input dev HumAID TSV containing tweet IDs
        parser.add_argument(
            "-d",
            "--dev",
            type=str,
            required=True,
            help="path to HumAID dev TSV file"
        )

        # path to input testing HumAID TSV containing tweet IDs
        parser.add_argument(
            "-f",
            "--test",
            type=str,
            required=True,
            help="path to HumAID testing TSV file"
        )

        # experiment name of model/algorithm being used
        parser.add_argument(
            "-e",
            "--experiment",
            type=str,
            required=True,
            help="experiment name of model/algorithm being used"
        )

    def handle(self, *args, **options):
        # build the training data split
        self.stdout.write("* loading data splits...")
        (X_train, y_train) = self.build_data_split(
            options["train"],
            options["experiment"]
        )

        # build the testing data split
        (X_test, y_test) = self.build_data_split(
            options["test"],
            options["experiment"]
        )

        # build the dev data split
        (X_dev, y_dev) = self.build_data_split(
            options["dev"],
            options["experiment"]
        )

        # perform a grid search on the SVM hyperparameters, making sure to use
        # larger max iterations on the SVM to encourage convergence
        model = GridSearchCV(
            LinearSVC(max_iter=10000, dual="auto"),
            self.SVM_PARAMS,
            cv=3,
            verbose=1,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # extract the best model and display its parameters
        best_model = model.best_estimator_
        self.stdout.write(model.best_params_)

        # TODO:
        # Remove dev set?

        # use the best model to make predictions on the test set
        y_pred = best_model.predict(X_test)
        self.stdout.write(classification_report(y_test, y_pred, digits=3))

    @staticmethod
    def build_data_split(input_path, experiment):
        # load the input TSV file
        df = pd.read_csv(input_path, sep="\t")

        # grab all embedding objects that (1) belong to the supplied experiment
        # and (2) exist in the tweet IDs
        embeddings = Embedding.objects.filter(
            experiment=experiment,
            smp__post_id__in=df["tweet_id"].to_list()
        )

        # build the data vectors and class labels
        X = np.array([json.loads(e.embeddings) for e in embeddings])
        y = np.array([e.smp.label for e in embeddings])

        # return the data and labels
        return (X, y)
