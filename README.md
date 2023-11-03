IMAGE

# Rescue Ripple: Zero-shot, Prompt-based Classification with LLMs for Disaster Tweet Analysis

In times of crisis, rapid and accurate analysis of social media can be lifesaving. Twitter, a primary platform for real-time communication, provides critical data that, if promptly and correctly analyzed, can significantly aid disaster response efforts. This work introduces "Rescue Ripple," a simplistic, yet highly efficient approach employing zero-shot, prompt-based classification with Large Language Models (LLMs) to analyze disaster-related tweets. Unlike traditional methods requiring extensive labeled datasets and computationally intensive training, our zero-shot framework demonstrates the capability to classify tweets effectively without task-specific fine-tuning.

We leverage the pre-existing knowledge encapsulated within state-of-the-art LLMs to interpret the context and content of tweets, applying carefully engineered prompts to guide the model towards accurate classification. This research not only challenges the status quo by showcasing that zero-shot classification can rival traditional machine learning classifiers in accuracy but also highlights a remarkable improvement in efficiency, a critical factor during disaster scenarios.

In a comparative study against the baseline methods reported with the [HumAID dataset](#), Rescue Ripple achieves comparable, and in some cases superior, performance metrics.

Furthermore, by utilizing LLM embeddings as feature representations for a Linear SVM, we provide an approach that balances the trade-off between performance and computational demand, especially suitable for resource-constrained environments.

This work's findings underscore the untapped potential of LLMs in real-world humanitarian applications and set the stage for future research into low-resource, high-impact machine learning solutions for disaster management.

## HumAID dataset

> _"The HumAID Twitter dataset consists of several thousands of manually annotated tweets that has been collected during 19 major natural disaster events including earthquakes, hurricanes, wildfires, and floods, which happened from 2016 to 2019 across different parts of the World. The annotations in the provided datasets consists of following humanitarian categories. The dataset consists only english tweets and it is the largest dataset for crisis informatics so far." - [Alam et al. (2021)](https://crisisnlp.qcri.org/humaid_dataset)

The HumAID dataset seeks to classify classify input tweets into one of the following humanatarian categories, with the aim of helping disaster response:

- Caution and advice
- Displaced people and evacuations
- Dont know cant judge
- Infrastructure and utility damage
- Injured or dead people
- Missing or found people
- Not humanitarian
- Other relevant information
- Requests or urgent needs
- Rescue volunteering or donation effort
- Sympathy and support

In total, there are **77,196 tweets** in the HumAID dataset.

## Prompt

The [`humaid_zero_shot_prompt.md`](#) file contains the zero-shot prompt for tweet classification:

```
Act as a machine learning model with expert knowledge in disaster management, emergency management, and the classification of social media posts.

You are currently involved in a research project testing your ability to categorize tweets into the following {labels} to help in humanitarian and disaster aid. The results of your analysis will be included in a research paper.

Below is an input {tweet}. Your goal is to use your expert knowledge of disaster/emergency management, coupled with expert ability to classify social media, to categorize the tweet into one of the {labels}.

Format your output using the {formatting} instructions.

Formatting:
- Return only the main response
- Remove pre-text, post-text
- Format response as JSON variable using the {JSON template}

Labels:
`caution_and_advice`: Reports of warnings issued or lifted, guidance and tips related to the disaster
`sympathy_and_support`: Tweets with prayers, thoughts, and emotional support
`requests_or_urgent_needs`: Reports of urgent needs or supplies such as food, water, clothing, money, medical supplies or blood
`displaced_people_and_evacuations`: People who have relocated due to the crisis, even for a short time (includes evacuations)
`injured_or_dead_people`: Reports of injured or dead people due to the disaster
`missing_or_found_people`: Reports of missing or found people due to the disaster event
`infrastructure_and_utility_damage`: Reports of any type of damage to infrastructure such as buildings, houses, roads, bridges, power lines, communication poles, or vehicles
`rescue_volunteering_or_donation_effort`: Reports of any type of rescue, volunteering, or donation efforts such as people being transported to safe places, people being evacuated, people receiving medical aid or food, people in shelter facilities, donation of money, or services, etc.
`other_relevant_information`: If the tweet does not belong to any of the above categories, but it still contains important information useful for humanitarian aid, belong to this category
`not_humanitarian`: If the tweet does not convey humanitarian aid-related information

JSON Template:
{
	"label": null, // using {tweet}, select one of {labels} that best categorizes it
	"confidence": null // provide the confidence of your prediction by selecting a value between 0.0 and 1.0 in 0.1 increments, zero being no confidence and 1.0 being extremely confident
}

Tweet:
{{ post }}
```

As you can see in the [`classify_post_with_prompt`](#) method, we load this prompt from disk, set the `{{ post }}` template variable (i.e., the tweet itself), and then submit the request to OpenAI for classification. The resulting prediction is then stored in the database.

## Results

TABLE

In this study, we juxtapose the performance of various machine learning and deep learning algorithms against our proposed methodologies for the classification of disaster-centric tweets.

Our empirical results underscore that while deep learning classifiers established by Alam et al. exhibit a pronounced dominance over traditional machine learning counterparts, **our zero-shot classification strategy leveraging LLMs delivers a commendable average F1 score of 0.716, thereby _outperforming_ traditional machine learning approaches.**

This result not only signifies the capability of zero-shot learning to nearly bridge the gap to deep learning efficacy without the need for explicit task-oriented training but also accentuates the potential utility of LLMs in swiftly adapting to the volatile domain of disaster response. 

Perhaps more interestingly, our 'Embedding + SVM' experiments, which utilizes the sophisticated semantic comprehension of LLM-derived embeddings with the computational frugality of a Linear SVM, demonstrates an impressive average F1 score of 0.763, **which is _nearly_ the accuracy of the more complicated, computationally expensive methods discussed by Alam et al.**

In some instances, such as '2018 Hurricane Florence', 'Hurricane' (i.e., _all_ tweets about hurricanes), and 'All' (i.e., _every_ tweet in the HumAID database, we _outperform_ the best deep learning methods from Alam at el.

These findings advocate for the 'Embedding + SVM' model as a potent alternative to more computationally demanding deep learning models, offering substantial implications for scenarios where expedient and resource-efficient deployment is paramount for an effective disaster response.



### Cost

Applying our prompt-based classification method to the entire HumAID dataset of 77,196 tweets using `gpt-3.5-turbo` cost ~$35 USD.

Computing embeddings with `text-embedding-ada-002` cost us only $0.28.


## Getting Started

This section provides instructions on how to configure your development environment and replicate the results presented here.

### Requirements

...

### Starting Redis, Celery, and Flower

To start, make sure you have [Redis](https://redis.io/) installed on your machine. You can then launch Redis via:

```
$ redis-server
```

If you haven't initialized your Django database and created a Django superuser, do so now (these commands only need to be ran _once_):

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

Next, launch your [Celery](#) workers:

```
$ celery -A rescue_ripple worker -l INFO
```

Finally (and optionally), you can use [Flower](#) to monitor the Celery tasks:

```
$ celery -A rescue_ripple flower
```

Once launched, Flower can be accessed via `http://localhost:5555/` on your machine.

### Adding the HumAID tweet dataset to the database

This work builds on _HumAID: Human-Annotated Disaster Incidents Data from Twitter_ (Alam et al. 2021), the authors of which have curated the dataset used in this exploration.

If you haven't yet, [download the HumAID dataset from the CrisisNLP website](https://crisisnlp.qcri.org/humaid_dataset).

Specifically, you will need:

1. [Event wise dataset (set1) 47,868 tweets](https://crisisnlp.qcri.org/data/humaid/HumAID_data_events_set1_47K.tar.gz)
2. [Event wise dataset (set2) 29,328 tweets](https://docs.google.com/forms/d/e/1FAIpQLSdnin1lFg2hBLc0QqJ2dndmz4RTG8V-U8sQGD81NjejE8jxvQ/viewform) (once you fill in the form you will receive a link to download the tarball)
3. [Event type dataset](https://crisisnlp.qcri.org/data/humaid/HumAID_data_event_type.tar.gz)
4. [All Combined dataset](https://crisisnlp.qcri.org/data/humaid/HumAID_data_all_combined.tar.gz)

After downloading and extracting the four files, your directory structure should look something like the following:

```
$ tree
.
├── HumAID_data_all_combined.tar.gz
├── HumAID_data_event_type.tar.gz
├── HumAID_data_events_set1_47K.tar.gz
├── HumAID_data_events_set2_29K.tar.gz
├── all_combined
│   ├── Licensing.txt
│   ├── Readme.txt
│   ├── all_dev.tsv
│   ├── all_test.tsv
│   └── all_train.tsv
├── event_type
│   ├── Licensing.txt
│   ├── Readme.txt
│   ├── earthquake_dev.tsv
│   ├── earthquake_test.tsv
│   ├── earthquake_train.tsv
│   ├── fire_dev.tsv
│   ├── fire_test.tsv
│   ├── fire_train.tsv
│   ├── flood_dev.tsv
│   ├── flood_test.tsv
│   ├── flood_train.tsv
│   ├── hurricane_dev.tsv
│   ├── hurricane_test.tsv
│   └── hurricane_train.tsv
├── events_set1
│   ├── Licensing.txt
│   ├── Readme.txt
│   ├── canada_wildfires_2016
│   │   ├── canada_wildfires_2016_dev.tsv
│   │   ├── canada_wildfires_2016_test.tsv
│   │   └── canada_wildfires_2016_train.tsv
│   ├── cyclone_idai_2019
│   │   ├── cyclone_idai_2019_dev.tsv
│   │   ├── cyclone_idai_2019_test.tsv
│   │   └── cyclone_idai_2019_train.tsv
│   ├── ecuador_earthquake_2016
│   │   ├── ecuador_earthquake_2016_dev.tsv
│   │   ├── ecuador_earthquake_2016_test.tsv
│   │   └── ecuador_earthquake_2016_train.tsv
│   ├── hurricane_harvey_2017
│   │   ├── hurricane_harvey_2017_dev.tsv
│   │   ├── hurricane_harvey_2017_test.tsv
│   │   └── hurricane_harvey_2017_train.tsv
│   ├── hurricane_irma_2017
│   │   ├── hurricane_irma_2017_dev.tsv
│   │   ├── hurricane_irma_2017_test.tsv
│   │   └── hurricane_irma_2017_train.tsv
│   ├── hurricane_maria_2017
│   │   ├── hurricane_maria_2017_dev.tsv
│   │   ├── hurricane_maria_2017_test.tsv
│   │   └── hurricane_maria_2017_train.tsv
│   ├── hurricane_matthew_2016
│   │   ├── greece_wildfires_2018
│   │   │   ├── greece_wildfires_2018_dev.tsv
│   │   │   ├── greece_wildfires_2018_test.tsv
│   │   │   └── greece_wildfires_2018_train.tsv
│   │   ├── hurricane_matthew_2016_dev.tsv
│   │   ├── hurricane_matthew_2016_test.tsv
│   │   ├── hurricane_matthew_2016_train.tsv
│   │   └── maryland_floods_2018
│   │       ├── maryland_floods_2018_dev.tsv
│   │       ├── maryland_floods_2018_test.tsv
│   │       └── maryland_floods_2018_train.tsv
│   ├── italy_earthquake_aug_2016
│   │   ├── italy_earthquake_aug_2016_dev.tsv
│   │   ├── italy_earthquake_aug_2016_test.tsv
│   │   └── italy_earthquake_aug_2016_train.tsv
│   ├── kaikoura_earthquake_2016
│   │   ├── kaikoura_earthquake_2016_dev.tsv
│   │   ├── kaikoura_earthquake_2016_test.tsv
│   │   └── kaikoura_earthquake_2016_train.tsv
│   ├── puebla_mexico_earthquake_2017
│   │   ├── puebla_mexico_earthquake_2017_dev.tsv
│   │   ├── puebla_mexico_earthquake_2017_test.tsv
│   │   └── puebla_mexico_earthquake_2017_train.tsv
│   └── srilanka_floods_2017
│       ├── srilanka_floods_2017_dev.tsv
│       ├── srilanka_floods_2017_test.tsv
│       └── srilanka_floods_2017_train.tsv
├── events_set2
│   ├── Licensing.txt
│   ├── Readme.txt
│   ├── california_wildfires_2018
│   │   ├── california_wildfires_2018_dev.tsv
│   │   ├── california_wildfires_2018_test.tsv
│   │   └── california_wildfires_2018_train.tsv
│   ├── hurricane_dorian_2019
│   │   ├── hurricane_dorian_2019_dev.tsv
│   │   ├── hurricane_dorian_2019_test.tsv
│   │   └── hurricane_dorian_2019_train.tsv
│   ├── hurricane_florence_2018
│   │   ├── hurricane_florence_2018_dev.tsv
│   │   ├── hurricane_florence_2018_test.tsv
│   │   └── hurricane_florence_2018_train.tsv
│   ├── kerala_floods_2018
│   │   ├── kerala_floods_2018_dev.tsv
│   │   ├── kerala_floods_2018_test.tsv
│   │   └── kerala_floods_2018_train.tsv
│   ├── midwestern_us_floods_2019
│   │   ├── midwestern_us_floods_2019_dev.tsv
│   │   ├── midwestern_us_floods_2019_test.tsv
│   │   └── midwestern_us_floods_2019_train.tsv
│   └── pakistan_earthquake_2019
│       ├── pakistan_earthquake_2019_dev.tsv
│       ├── pakistan_earthquake_2019_test.tsv
│       └── pakistan_earthquake_2019_train.tsv
```

You are now ready to move on to running the scripts used to relicate our results.

### Adding HumAID tweets to the Django database

The HumAID dataset contains a number of `.tsv` files. The `.tsv` files that contain the contents of the tweets can be found in the `events_set1` and `events_set2` directories.

Use the following command to ingest _all_ HumAID tweets into the database:

```
$ python manage.py load_humaid_tweets --events-set1 HumAID/events_set1 --events-set2 HumAID/events_set2
```

### Classify HumAID tweets with prompt-based methods

With the HumAID tweets added to the database, you can use the `classify_with_prompt` command to classify any of the tweet IDs.

Here is an example command to classify only the testing tweets in the 2016 Canada Wildfires directory using `gpt-3.5-turbo`:

```
$ python manage.py classify_with_prompt --tsv HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_test.tsv --prompt humaid_zero_shot_prompt.md --experiment zero-shot-gpt-3.5-turbo --model gpt-3.5-turbo
```

Or, if you want to classify _all_ tweets from the test set, you could use this command:

```
$ python manage.py classify_with_prompt --tsv HumAID/all_combined/all_test.tsv --prompt humaid_zero_shot_prompt.md --experiment zero-shot-gpt-3.5-turbo --model gpt-3.5-turbo
```

_**Note:** Make sure both Redis and Celery are running before you run `classify_with_prompt`! Celery handles managing all LLM prompt tasks, and is **required** when running the code from this repo.

### Computing prompt-based classification accuracy

Now that all tweets have been classified using the prompt, you can run the following command to compute a classification report for a given set or subset.

This command will evaluate Rescue Ripple on the 2016 Canada Wildfires testing set:

```
$ python manage.py compute_classification_report --tsv HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_test.tsv --experiment zero-shot-gpt-3.5-turbo
```

Whereas this command will perform an evaluation on all tweets belogning to the testing set:

```
$ python manage.py compute_classification_report --tsv HumAID/all_combined/all_test.tsv --experiment zero-shot-gpt-3.5-turbo
```

### Computing LLM embeddings on HumAID dataset

The `compute_embeddings` command is used to submit every tweet to OpenAI's API. The resulting vector embeddings are stored in the database

Similar to the `classify_with_prompt` command, you can either run `compute_embeddings` on a _subset_ of HumAID or the _entire_ dataset.

Here's how to use the command on the 2019 US Midwestern Floods training set:

```
$ python manage.py compute_embeddings --tsv HumAID/events_set2/midwestern_us_floods_2019/midwestern_us_floods_2019_train.tsv --experiment ada-002
```

Or, you can compute embeddings for the _entire_ HumAID dataset using the following three commands:

```
$ python manage.py compute_embeddings --tsv HumAID/all_combined/all_test.tsv --experiment ada-002
$ python manage.py compute_embeddings --tsv HumAID/all_combined/all_dev.tsv --experiment ada-002
$ python manage.py compute_embeddings --tsv HumAID/all_combined/all_train.tsv --experiment ada-002
```

Note that computing embeddings for the entire dataset will result in a `db.sqlite3` file that is ~6GB.

### Training and tuning Linear SVM hyperparameters

Now that we have our embeddings, we can train a Linear SVM on them.

Here is how to tune the hyperparameters on the 2016 Canada Wildfires subset:

```
$ python manage.py tune_model \
  --train HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_train.tsv \
  --dev HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_dev.tsv \
  --test HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_test.tsv \
  --experiment ada-002
```

And here is how to evaluate the accuracy of Rescue Ripple on all tweets in HumAID:

```
$ python manage.py tune_model \
  --train HumAID/all_combined/all_train.tsv \
  --dev HumAID/all_combined/all_dev.tsv \
  --test HumAID/all_combined/all_test.sv
  --experiment ada-002
```

Note that hyperparameter tuning can take multiple hours.

The [tune_models.sh](#) file provides further examples of hyperparameter tuning examples.

## License

...


