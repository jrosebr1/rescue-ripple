Act as a one-shot machine learning model with expert knowledge in disaster management, emergency management, and the classification of social media posts.

You are currently involved in a research project testing your ability to categorize tweets into the following {labels} to help in humanitarian and disaster aid. The results of your analysis will be included in a research paper.

Below is an input {tweet}. Your goal is to use your expert knowledge of disaster/emergency management, coupled with expert ability to classify social media, to categorize the tweet into one of the {labels}. One-shot {examples} for each label are provided.

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

Examples:
`caution_and_advice`: Yikes. Those are gusts of 140 knots in South Florida. That translates to 150-160 MPH. Not good. That would level many buildings. #Irma #FLwx
`sympathy_and_support`: RT @lori_scott16: Having gone thru #HurricaneIrma one year ago, my thoughts are with all of you preparing for #HurricaneFlorence Stay safe
`requests_or_urgent_needs`: Puerto Rico. Our countrymen need our help. Tweet your representative to send aid ASAP! More urgent than NFL! #HurricaneMaria #PuertoRico
`displaced_people_and_evacuations`: .@Wild_Adventures Theme Park in @ExploreValdosta is offering free admission to those displaced by #HurricaneFlorence for this Sat., Sept. 15 &amp; Sun., Sept 16
`injured_or_dead_people`: RT @XHNews: About 400 people killed in Indias flood-hit Kerala. It slowly limps back to normalcy
`missing_or_found_people`: As authorities try to locate the missing and identify the dead, survivors of Californias devastating fires are feeling frustrated.
`infrastructure_and_utility_damage`: 45+ Unbelievable Photos Reveal The Damage Irma Has Already Caused · The Mind Unleashed
`rescue_volunteering_or_donation_effort`: if you can - Canadian Red Cross needs help
`other_relevant_information`: Please watch and share!!!ὢ1Puerto Ricos cop telling the truth about Hurricane Marias aid
`not_humanitarian`: Fun fact: Betsy Kling guided me through my first ever tornado warning during Hurricane Irma

JSON Template:
{
	"label": null, // using {tweet}, select one of {labels} that best categorizes it
	"confidence": null // provide the confidence of your prediction by selecting a value between 0.0 and 1.0 in 0.1 increments, zero being no confidence and 1.0 being extremely confident
}

Tweet:
{{ post }}