<h1>Italian Tweets Analyzer</h1>

Italian tweets analyzer is a tool created for the thesis work at the University of Bari “Aldo Moro” of the course 
“Methods for the information retrieval”. It can perform analysis on Italian tweets and it provides several features. 
This project is an upgraded version of the tool: Hate-Tweet-Map. The main features of the program are described below. 

<h2>Tweets extraction</h2>

This program allows to define a query with the information you want to request from Twitter, then the request is sent to 
Twitter and the information obtained is saved within the database (MongoDB). To modify the request you want to send to 
Twitter, you need to edit the configuration file called “search_tweets.config”. This file contains some fields that 
require values, while others are optional. The mandatory fields are (at least one of them must be filled): 
<ul>
<li><code>Keyword</code>: keyword on which the search for tweets will be based. In fact, those tweets that contain the indicated keyword 
will be found. You can set multiple keywords and use logical operators like AND and OR. 
For example: “Joe Biden”, “Biden OR Trump”, “(Biden OR Trump) whitehouse” 
(the last query means “(Biden OR Trump) AND whitehouse”).</li>
</ul>
<ul>
<li><code>User</code>: In this field you can specify the user username or user’s ID. It is possible to insert multiple users. 
If this field and the keyword field are set, then will be find that contains the keyword specified from the user 
specified.</li>
</ul>
<ul>
<li><code>User_mentioned</code>: in this field you can enter the username of a specific user to search for tweets that mention him.</li>
</ul>
<ul>
<li><code>Hashtag</code>: in this field you can enter a specific hashtag for search tweets that contain it.</li>
</ul>
  
The optional fields are:
<ul>
<li><code>Lang</code>: this field indicates the language of the tweets that you want to retrieve. The values that this field accepts 
are those reported by ISO 639-1 code. An example values: it, en, pt, es.</li>
</ul>
<ul>
<li><code>Context_annotations</code>: this field indicates to twitter to include or not the context annotation for the tweet that 
have it. If this field is set to True, the field n_result will be set automatically to 100. 
Possible values are True/False.</li>
</ul>
<ul>
<li><code>N_results</code>: this field indicates to twitter to how many tweets the response should contain. Twitter allows to search 
for minimum 10 tweets to maximum 500 tweets for request. So if the value entered in this field is less than 10, this 
field will be automatically set to 10; if the value entered is greater than 500, more requests will be send to Twitter.
Possible values: any int number.</li>
</ul>
<ul>
<li><code>All_tweets</code>: this fields indicates to twitter to find all possible tweets. If this field is True, n_result will be set
to 500. Possible values: True/False.
</li>
</ul>
<ul>
<li><code>Time</code>: this field allows to search tweets in a specific range of time. This field has two sub-fields: <code>start_time</code> and 
<code>end_time</code>. The values in this fields must be in the ISO 8601/RFC 3339 format, so like: YYYY-MM-DDTHH:mm:ss+Z. 
The configurations that can be made are: 
</li>
&nbsp;
<ul>
<li>Only start_time is specified: end_time will be assumed to be current time (-30 sec).</li>
</ul>
&nbsp;
<ul>
<li>Only end_time is specified: start_time will be assumed 30 days before the end_time specified.</li>
</ul>
&nbsp;
<ul>
<li>Both are specified: the tweets in the range time will be found.</li>
</ul>
&nbsp;
<ul>
<li>None: by default, a request will return tweets from up to 30 days ago.</li>
</ul>
</ul>
<ul>
<li><code>Geo</code>: in this section is possible to set the geographical parameters, in this way it is possible to filter the tweets 
based on their geographical origin. This field has several sub-fields and only one of them must be set:</li> 
<ul>
&nbsp;
<li><code>Place</code>: matches tweets tagged with the specified location on twitter place ID. Multi-word place names (“New York City”,
“Palo Alto”) should be enclosed in quotes. Possible values: any name of city, enclosed in quotes if the place name 
consists of several words.</li>
</ul>
&nbsp;
<ul>
<li><code>Place_country</code>: attaches tweets where the country code associated with a tagged place/location matches the given ISO 
alpha-2 character code. Possible values: any name of country in ISO_3166-1_alpha-2 format.</li>
</ul>
&nbsp;
<ul>
<li><code>Bounding_box</code>: matches against the place.geo.coordinates object of the tweet when present, and in Twitter against a 
place geo polygon, where the place polygon is fully contained within the defined region. The coordinate values are 
indicated in the following fields: west_long, south_lat, east_long, north_lat.</li>
</ul>
&nbsp;
<ul>
<li><code>Point_radius</code>: matches again the place.geo.coordinates object of the tweet when present, and in twitter, against a 
place geo polygon, where the place polygon is fully contained within the defined region. The coordinate values are 
indicated in the following fields: longitude, latitude, radius.</li>
</ul>
</ul>
<ul>
<li><code>Filter_retweet</code>: this field indicates to Twitter to include or not the retweet in the response. If it is True, Twitter
response could contain also retweets; if false not. Possible values: True/False.</li>
</ul>
<ul>
<li><code>Filter_images</code>: this field indicates to find tweets that contain an image URL. For example, entering the hashtag 
#covid in the configuration file and setting True to this field, you will get all tweets with that particular hashtag 
that contain an image. Possible values are: True/False.</li>
</ul>

In the configuration file you can also edit the name of the database where the tweets will be saved.

<h2>Find information about Twitter users</h2>

The program explores the collection of tweets in the database and goes to find information on users who have published 
these posts. In the configuration file: “search_users.config”, you can edit the fields that indicate where to get the 
tweets and where to go to save the information of the users who have published those tweets.

<h2>Process Tweets</h2>

This tool allows you to perform different types of analysis on collected tweets. The possible analyses are described
below.

<h5>Entity Linker</h5>
ITA uses the TagMe service to find entities in the text of the tweet and to connect these with the 
respective Wikipedia page.

<h5>Geo</h5> 
ITA uses the geographic information in the tweet to find the coordinates of the place where the tweets have been 
posted. This process uses Open Street Map service. (This operation could be time expensive cause OSM allows to send only
one request per second)

<h5>Natural Language Processing</h5>
ITA uses spacy model to lemmatize the text of the tweet. In addition
save the POS and the Morphological information and the entities found by spacy in the text.

<h5>Sentiment Analysis</h5>
ITA uses three different services to perform sentiment analysis of the tweets collected in the
database.

<ul>

<li>Feel-it: model able to classify italian tweets and annotate them using basic emotions
like: anger, fear, joy, sadness. It can also perform sentiment analysis, telling if the content of a tweet
is positive, neutral or negative.</li>
&nbsp;
<li>Sent-it: model able to perform sentiment analysis on italian tweets. It can tell if the content of a tweet is:
positive, neutral or negative.</li>
&nbsp;
<li>Hate-speech-it: model that can perform sentiment analysis. The labels used by it are: accettable, inappropriate,
offensive, violent.</li>

</ul>

<h5>Genre classification</h5>
ITA allows you to perform genre classification: tweets are categorized according to their textual content; for example 
it can determine if a text represents a news, a legal document, the text of a song, etc.
The model used for genre classification is xml-roberta. The table below shows the labels used by the model and their 
description.

| Label                   | Description |
|-------------------------|------|
| Information/Explanation | An objective text that describes or presents an event, a person, a thing, a concept etc. |
| Instruction             | An objective text which instructs the readers on how to do something. |
| Legal                   |   An objective formal text that contains legal terms and is clearly structured.    |
| News                    |   An objective or subjective text which reports on an event recent at the time of writing or coming in the near future.   |
| Opinion/Argumentatio    |   A subjective text in which the authors convey their opinion or narrate their experience.   |
| Promotion               |   A subjective text intended to sell or promote an event, product, or service. It addresses the readers, often trying to convince them to participate in something or buy something.   |
| Forum                   |   A text in which people discuss a certain topic in form of comments.   |
| Prose/Lyrical	          |   A literary text that consists of paragraphs or verses.   |
| Other                   |   A text that which does not fall under any of other genre categories.   |



<h5>Image to text</h5>
Ita can capture the semantic meaning of an image and save it as a string, then it is saved within the database.
The model used for image captioning is vit-gpt2-image-captioningm which bases its operation on the Coco dataset.
COCO is a large-scale object detection, segmentation, and captioning dataset.

<h2>Process Tweets: configuration file</h2>


From the configuration file called “process_tweets.config” you can indicate 
which analysis perform on tweets. In the configuration file there are the following fields:
<ul>
<li><code>TagMe</code></li>
<ul>
<li><code>Enabled</code>: enable or disable this phase. Possible values are True/False.</li>
</ul>
<ul>
<li><code>Token</code>: the token obtained from TagMe to send the requests. Possible values: a valid TagMe token.</li>
</ul>
<ul>
<li><code>Is_tweet</code>: indicate to TagMe service if the text given is a tweet or not. Possible values are True/False.</li> 
</ul>
<ul>
<li><code>Rho_value</code>: estimates the confidence in the annotation. The threshold should be chosen in the interval [0,1].
A reasonable threshold is between 0.1 and 0.3. Possible values: any number between 0 and 1.</li>
</ul>
</ul>
<ul>
<li><code>Sentiment_analyze</code></li>
<ul>
<li><code>Sent_it</code>: enable or disable sent-it phase (true/false).</li>
<li><code>Feel_it</code>: enable or disable feel-it phase (true/false).</li>
<li><code>Hate_speech_it</code>: enable or disable hate_speech_it phase (true/false).</li>
</ul>
</ul>
<ul>
<li><code>Geocoding</code>: this section enables or disables the geocoding phase using Open Street Map service. 
Possible values are tru/false.</li>
</ul>
<ul>
<li><code>Genre_classification</code></li>
<ul>
<li><code>Roberta</code>: enable or disable the classification of tweets with Roberta (true/false).</li>
</ul>
</ul>
<ul>
<li><code>Image_to_text</code></li>
<ul>
<li><code>Image_captioning</code>: enable or disable the image captioning with the vit-gpt2-image-captioning</li>
</ul>
</ul>
<ul>
<li><code>Analyze_all_tweets</code>: there are two mode to select the tweets to analyze: all the tweets in the collection or only the 
tweets that have not yet been passed to the Natural Language Phase. To choose the first mode just set the 
analyze_all_tweets to True, otherwise to False.</li>
</ul>
<h2>Manage Tweets</h2>

The program allows you to: 
<ul>
<li>extract tweets from the database and save them on .json or .csv file;</li> 
<li>delete some tweets.</li>
</ul>
The criteria to select the tweets to extract/delete are defined in the manage_tweets.config file. Is possible to modify 
that file to set the criteria. The configuration file has the following fields: 
<ul>
<li><code>mode</code>: the mode indicates what the script have to do: extract and save the tweets in a file or delete them. 
Possible values are: extract/delete. This field is mandatory to set.</li>
</ul>
<ul>
<li><code>Criteria</code></li>
<ul>
<li><code>sentiment</code>: by setting this field it’s possible to retrieve tweets with a specific sentiment, in particular 
choosing between neutral, positive or negative sentiment. Possible values are: negative/positive/neutral.</li>
</ul>
<ul>
<li><code>Keywords</code>: setting this field it’s possible to retrieve tweets that contains specific words.</li>
</ul>
<ul>
<li><code>Words</code>: a list of words to search separated by a comma. Example: sun,sea,island</li>
</ul>
<ul>
<li><code>Path</code>: the path to a .txt file that contains the words to search. The .txt file must contain each word to search in a 
different line and just one word in a line. Possible values: a valid path to a .txt file.</li>
</ul>
<ul>
<li><code>Postag</code>: by setting this field it’s possible to retrieve tweets that contains a word with a specific POS tag. 
Possible values: any valid POS value.</li>

<ul>
<li><a href="https://spacy.io/usage/linguistic-features" target="_blank">Here for a generic understanding</a></li>
<li><a href="https://spacy.io/models/it#it_core_news_lg-labels" target="_blank">here for a complete list of italian SpaCy’s POS values (see labels scheme section in it_core_news_lg)</a></li>
<li><a href="https://spacy.io/models/en#en_core_web_lg-labels" target="_blank">here for a complete list of english SpaCy’s POS values (see labels scheme section in en_core_web_lg)</a></li>
</ul>
</ul>
<ul>
<li><code>Morph</code>: by setting this field it’s possible to retrieve tweets that contains a word with a specific morphology. 
Possible values are any valid morph value.</li>
<ul>
<li><a href="https://spacy.io/usage/linguistic-features" target="_blank">Here for a generic understanding</a></li>
<li><a href="https://spacy.io/models/it#it_core_news_lg-labels" target="_blank">here for a complete list of italian SpaCy’s POS values (see labels scheme section in it_core_news_lg)</a></li>
<li><a href="https://spacy.io/models/en#en_core_web_lg-labels" target="_blank">here for a complete list of english SpaCy’s POS values (see labels scheme section in en_core_web_lg)</a></li>
</ul>
</ul>
<ul>
<li><code>Raw_query</code>: by setting this field it’s possible to write an own query. The query must be a mongodb query and must take
in account the fields of the tweet saved in the collection. Possible values: any valid mongodb query.</li>
</ul>
<ul>
<li><code>Logical_operator</code>: if more than one criteria are set, it’s necessary to define how logically connect the crierias are. 
Possible values: or/and</li>
</ul>
</ul>
<h2>Database</h2>

ITA interfaces with a mongodb database where it saves tweets and extracts them in order to perform operations on them.
In each configuration file you must indicate:
<ul>
<li><code>url</code>: string with which you can connect to the database;</li>
<li><code>database</code>: name of the database;</li>
<li><code>collection</code> name of the database's collection.</li>
</ul>

<h2>Changelog</h2>

<ul>
<li><a href="https://darioamorosodaragona.gitlab.io/hatemap/index.html#" target="_blank">Hate-Tweet-Map-1.0</a>, developed by Dario Amoroso d'Aragona</li>
<li><a href="https://github.com/swapUniba/Hate-Tweet-Map-2.0#" target="_blank">Hate-Tweet-Map-2.0</a>, developed by Marco Sallustio</li>
<li>Italian tweets analyzer, developed by Davide Savino Volpicella</li>
</ul>