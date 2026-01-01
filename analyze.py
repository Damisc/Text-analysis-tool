from random_username.generate import generate_username
import re, nltk, json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("vader_lexicon")
wordLematizer = WordNetLemmatizer()
stopWords = set(stopwords.words("english"))
sentimentAnalyzer = SentimentIntensityAnalyzer()




def welcome_user():
    # Welcome user
    print("Welcome to the text analysis tool, i will mine and analyze a body of text from a file you give me")

def get_username():

    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:

        # print message prompting user to input their name 
        UserInput = " "
        if attempts == 0:
            UserInput = "\nTo begin, Please enter your username:\n"
        else:
            UserInput = "\nPlease try again: \n"
        usernameFromInput = input(UserInput)

        # Validate username
        if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
            print("Your username must be at least 5 characters long, alphanumeric only (a-z/A-Z/0-9), no spaces, not begin with numbers.")
        else:
            return usernameFromInput
        attempts += 1

    print("\nExhausted all " + str(max_attempts) + " attempts, assigning new username instead ....")
    return generate_username()[0]


# Greet user
def greet_user(name):
    # Greet the user
    print("Hello " + name)

# Get text from file
def getArticleText():
    f = open("files/article.txt", "r")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ").replace("\n", "")

# Extract Sentences
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)


# Extract words from list of sentences
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

# Extract Key sentences based on search pattern
def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        # If sentence matches desired pattern, add to matchedSentences
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

# Get the average words per sentence, excluding punctuation
def getWordsPerSentence(sentences):
    totalWOrdsPerSentence = 0
    for sentence in sentences:
        totalWOrdsPerSentence += len(sentence.split(" "))
    return totalWOrdsPerSentence / len(sentences)


# convert pos from POS tag function into wordnet compatible pos tag
posToWordnetTag = {
    "j": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV
}

def treebankPosToWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetTag:
        return posToWordnetTag[posFirstChar]
    return wordnet.NOUN
  

# convert raw list of (word, POS) tuple to a list of strings that only include valid english words
def cleanseWordList(posTaggedWordTuples):
    cleansedWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleansedWord = word.replace(".", "").lower()
        if (not re.search(invalidWordPattern, cleansedWord)) and len(cleansedWord) > 1 and cleansedWord not in stopWords:
            cleansedWords.append(wordLematizer.lemmatize(cleansedWord, treebankPosToWordnetPos(pos)))
    return cleansedWords


# Get user details
welcome_user()
username = get_username()
greet_user(username)

# Extract and tokenize text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

# Analytics
stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss/g"
keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# Get word analytics
wordsPosTagged = nltk.pos_tag(articleWords)
articleWordsCleansed = cleanseWordList(wordsPosTagged)

# Generate word cloud
seperator = " "
wordCloudFilePath = "results/wordcloud.png"
wordcloud = WordCloud(width = 1000, height = 700, random_state = 1, background_color = "white", colormap = "tab20", collocations = False).generate(seperator.join(articleWordsCleansed))
wordcloud.to_file(wordCloudFilePath)

# Run sentiment analysis
sentimentResult = sentimentAnalyzer.polarity_scores(articleTextRaw)

# collate analysis into one dictionary
finalResult = {
    "username": username,
    "data":{
        "keySentences": keySentences,
        "wordsPerSentence": round(wordsPerSentence, 1),
        "sentiment": sentimentResult,
        "wordCloudFilePath": wordCloudFilePath
    },
    "metadata":{
        "sentencesAnalyzed" : len(articleSentences),
        "wordsAnalyzed" : len(articleWordsCleansed)
    }
}
finalResultJson = json.dumps(finalResult, indent=4)

# Printing to test code
print(finalResultJson)

