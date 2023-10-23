# USAGE
#

# import the necessary packages
from django.core.management.base import BaseCommand
from ripple_predict.models import Prediction
from sklearn.metrics import classification_report
import pandas as pd


class Command(BaseCommand):

    # explain what this script does
    help = "Classifies a set of input tweets using prompt-based methods"

    def add_arguments(self, parser):
        # path to input HumAID TSV file containing tweet IDs that we've
        # classified and now want to compute classification metrics on
        parser.add_argument(
            "-t",
            "--tsv",
            type=str,
            required=True,
            help="path to HumAID TSV file"
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
        # load the input TSV file
        df = pd.read_csv(options["tsv"], sep="\t")

        # filter our predictions based on the tweet ID and experiment name,
        # then extract the ground-truth labels and predicted labels, such
        # that we can compute a classification report
        predictions = Prediction.objects.filter(
            smp__post_id__in=df["tweet_id"],
            experiment=options["experiment"]
        )
        y_true = [p.smp.label for p in predictions]
        y_pred = [p.prediction for p in predictions]

        # display our classification report
        self.stdout.write(classification_report(y_true, y_pred))