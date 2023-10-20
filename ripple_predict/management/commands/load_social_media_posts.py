# USAGE
# python manage.py load_social_media_posts --tsv ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_train.tsv

# import the necessary packages
from django.core.management.base import BaseCommand
from ripple_predict.models import SocialMediaPost
from tqdm import tqdm
import pandas as pd


class Command(BaseCommand):

    # explain what this script does
    help = "Ingests a TSV of HumAID data into database"

    def add_arguments(self, parser):
        # path to input HumAID TSV file containing tweet data that we'll be
        # adding to the database
        parser.add_argument(
            "-t",
            "--tsv",
            type=str,
            required=True,
            help="path to HumAID TSV file"
        )

    def handle(self, *args, **options):
        # load the input TSV file
        df = pd.read_csv(options["tsv"], sep="\t")

        # loop over the dataframe of tweets
        for (_, row) in tqdm(df.iterrows(), total=len(df)):
            # add the social media post to the database
            smp = SocialMediaPost(
                post_id=row["tweet_id"],
                text=row["tweet_text"],
                label=row["class_label"]
            )
            smp.save()
