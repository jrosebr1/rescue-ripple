#!/bin/zsh

# define the list of 'events_set1' experiments
events_set1=(
  "canada_wildfires_2016"
  "cyclone_idai_2019"
  "ecuador_earthquake_2016"
  "hurricane_harvey_2017"
  "hurricane_irma_2017"
  "hurricane_maria_2017"
  "hurricane_matthew_2016"
  "italy_earthquake_aug_2016"
  "kaikoura_earthquake_2016"
  "puebla_mexico_earthquake_2017"
  "srilanka_floods_2017"
)

# define the list of 'events_set2' experiments
events_set2=(
  "california_wildfires_2018"
  "hurricane_dorian_2019"
  "hurricane_florence_2018"
  "kerala_floods_2018"
  "midwestern_us_floods_2019"
  "pakistan_earthquake_2019"
)

# loop over the 'events_set1' experiments
for experiment in "${events_set1[@]}"; do
  # run the current experiment
  echo "${experiment}"
  python manage.py tune_model \
    --train ~/Desktop/HumAID/events_set1/${experiment}/${experiment}_train.tsv \
    --dev ~/Desktop/HumAID/events_set1/${experiment}/${experiment}_dev.tsv \
    --test ~/Desktop/HumAID/events_set1/${experiment}/${experiment}_test.tsv \
    --experiment ada-002
  echo "================================"
  echo -e "\n\n"
done

# loop over the 'events_set2' experiments
for experiment in "${events_set2[@]}"; do
  # run the current experiment
  echo "${experiment}"
  python manage.py tune_model \
    --train ~/Desktop/HumAID/events_set2/${experiment}/${experiment}_train.tsv \
    --dev ~/Desktop/HumAID/events_set2/${experiment}/${experiment}_dev.tsv \
    --test ~/Desktop/HumAID/events_set2/${experiment}/${experiment}_test.tsv \
    --experiment ada-002
  echo "================================"
  echo -e "\n\n"
done
