
PAN'13 Training Corpus for Author Profiling Task
================================================

Corpus description
------------------

The corpus consists of XML documents containing conversations (HTML format) about many different topics grouped by author and labeled with his/her language, gender and age group.

There are two languages (English and Spanish), two genders (Male and Female), and three groups of age (10s: 13-17,  20s: 23-27 and 30s: 33-47).

Each author is presented as a separate XML file, the name of which provides information about language, gender and age group in order to facilitate file tasks, and grouped by language in two separate folders, EN and ES.

Each XML document name is formatted as:

UUID_lang_agegroup_gender.xml

For example:

303232a213161ece822fe69176d48e58_en_20s_female.xml

And each XML file is formatted as follows:

<author lang="lang_code" gender="gender_code" age_group="age_group">
	<conversations count="number_of_conversations_in_file">
		<conversation id="UUID">
			[Original HTML Content of the conversation]
		</conversation>

		<conversation id="UUID">
			[Original HTML Content of the conversation]
		</conversation>

		....

	</conversations>
</author>


English corpus incorporates 236,000 authors (files), with 413,564 conversations and 180,809,187 words. Spanish corpus incorporates 75,900 authors (files), with 126,453 conversations and 21,824,198 words.

The distribution of the training data is:

LANG	AGE_GROUP	GENDER		N. OF AUTHORS (FILES)
-------------------------------------------------------------
EN	10s		MALE			8,600
			FEMALE			8,600
	20s		MALE			42,900
			FEMALE			42,900
	30s		MALE			66,800
			FEMALE			66,800
-------------------------------------------------------------
ES	10s		MALE			1,250
			FEMALE			1,250
	20s		MALE			21,300
			FEMALE			21,300
	30s		MALE			15,400
			FEMALE			15,400
-------------------------------------------------------------

Moreover, documents from authors who pretend to be minors have been included (e.g., documents composed of chat lines of sexual predators).

For any doubt or problem, please get in touch with us.

