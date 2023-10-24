# USAGE
# python manage.py load_humaid_tweets --events-set1 ~/Desktop/HumAID/events_set1 --events-set2 ~/Desktop/HumAID/events_set2

# import the necessary packages
from django.core.management.base import BaseCommand
from ripple_predict.humaid import HumAIDDatasetLoader
from ripple_predict.models import SocialMediaPost
from tqdm import tqdm


class Command(BaseCommand):

    # explain what this script does
    help = "Ingests HumAID tweet TSV files into database"

    def add_arguments(self, parser):
        # path to first HumAID events base directory
        parser.add_argument(
            "-a",
            "--events-set1",
            type=str,
            required=True,
            help="path to first HumAID events base directory"
        )

        # path to first HumAID events base directory
        parser.add_argument(
            "-b",
            "--events-set2",
            type=str,
            required=True,
            help="path to second HumAID events base directory"
        )

    def handle(self, *args, **options):
        # load the HumAID tweet dataset from disk
        self.stdout.write("* loading HumAID dataset..")
        dataset = HumAIDDatasetLoader(
            options["events_set1"],
            options["events_set2"]
        ).load(verbose=True)

        # indicate that we are now adding social media posts to the database,
        # then initialize the number of tweets skipped due to *already*
        # existing in the database
        self.stdout.write("* adding HumAID tweets to database...")
        num_skipped = 0

        # loop over the dataset dictionary
        for (tweet_id, data) in tqdm(dataset.items()):
            # check to see if a social media post already exists for the
            # current tweet ID
            if SocialMediaPost.is_social_media_post_exists(tweet_id):
                # increment the number of skipped tweets and continue looping
                num_skipped += 1
                continue

            # add the social media post to the database
            smp = SocialMediaPost(
                post_id=tweet_id,
                text=data["tweet_text"],
                label=data["class_label"]
            )
            smp.save()

        # display the number of tweets skipped
        self.stdout.write("* num_skipped: {}".format(num_skipped))
