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