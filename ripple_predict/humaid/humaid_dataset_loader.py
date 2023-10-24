# import the necessary packages
from pathlib import Path
from tqdm import tqdm
import pandas as pd


class HumAIDDatasetLoader:

    def __init__(self, events_set1_path, events_set2_path):
        # store the path to the two base event set directories
        self.events_set1_path = events_set1_path
        self.events_set2_path = events_set2_path

        # initialize a dictionary to store the loaded dataset
        self.dataset = {}

    def load(self, verbose=False):
        # grab all TSV file paths from the two input events directories
        events1_paths = self.find_tsv_files(self.events_set1_path)
        events2_paths = self.find_tsv_files(self.events_set2_path)

        # combine the two sets into a single set of paths
        tsv_paths = set(events1_paths)
        tsv_paths.update(events2_paths)
        tsv_paths = sorted(tsv_paths)

        # check if we are in verbose mode
        if verbose:
            # wrap the iterator in a progress bar
            tsv_paths = tqdm(tsv_paths)

        # loop over the TSV file paths
        for p in tsv_paths:
            # load the current TSV file, set the tweet ID as the index of the
            # dataframe, and then convert the dataframe to a dictionary such
            # that the key to the dictionary is the tweet ID and the value is
            # a dictionary of tweet text and class label
            df = pd.read_csv(p, sep="\t")
            df = df.set_index("tweet_id")
            df.index = df.index.astype("str")
            tweets = df.to_dict("index")

            # update the dataset dictionary
            self.dataset.update(tweets)

        # return the dataset dictionary
        return self.dataset

    @staticmethod
    def find_tsv_files(base_dir):
        # find all TSV files in the input base directory
        return [f for f in Path(base_dir).rglob("*.tsv")]
