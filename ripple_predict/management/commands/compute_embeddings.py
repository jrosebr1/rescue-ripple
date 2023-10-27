# USAGE
# python manage.py compute_embeddings --tsv ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_dev.tsv --experiment ada-002

# import the necessary packages
from django.core.management.base import BaseCommand
from ripple_predict.models import SocialMediaPost
from ripple_predict.models import Embedding
from ripple_predict.tasks import compute_embeddings
from tqdm import tqdm
import pandas as pd


class Command(BaseCommand):

    # explain what this script does
    help = "Computes embeddings for input tweets using LLM"

    def add_arguments(self, parser):
        # path to input HumAID TSV file containing tweet IDs that we wish
        # to compute embeddings for
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

        # name of OpenAI model to use for computing embeddings
        parser.add_argument(
            "-model",
            "--model",
            type=str,
            default="text-embedding-ada-002",
            help="computing embeddings"
        )

    def handle(self, *args, **options):
        # load the input TSV file
        df = pd.read_csv(options["tsv"], sep="\t")

        # initialize a results count dictionary to store integer counts on
        # number of jobs submitted, along with number of jobs skipped due to
        # either (1) computed embeddings already existing in our database, or
        # (2) the original social media post not existing in our database
        job_counts = {
            "num_submitted": 0,
            "num_pred_exists": 0,
            "num_db_not_found": 0,
        }

        # loop over the dataframe of tweets
        for (_, row) in tqdm(df.iterrows(), total=len(df)):
            # attempt to process the row
            try:
                # grab the social media post associated with the row
                smp = SocialMediaPost.objects.get(post_id=row["tweet_id"])

                # if an embedding already exists for the combination of social
                # media post and experiment, then ignore it (otherwise we'd
                # have to recompute the embeddings, and pay for any associated
                # API costs)
                if Embedding.is_embedding_exist(smp, options["experiment"]):
                    # count the number of jobs skipped to the final output
                    # prediction already existing in our database
                    job_counts["num_pred_exists"] += 1
                    continue

                # submit the job to classify the current social media post
                compute_embeddings.apply_async(args=[
                    smp.id,
                    options["experiment"],
                    options["model"]
                ])
                job_counts["num_submitted"] += 1

            # could not find a social media post with the provided tweet ID in
            # the database
            except SocialMediaPost.DoesNotExist:
                # count the number of jobs skipped due to the social media post
                # from the TSV file not existing in our database
                job_counts["num_db_not_found"] += 1
                continue

        # loop over the final job counts
        for (count_name, count) in job_counts.items():
            # display statistics on the number of jobs
            self.stdout.write("* {}: {}".format(count_name, count))
