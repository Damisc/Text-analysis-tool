from random_username.generate import generate_username
from nltk.tokenize import word_tokenize, sent_tokenize



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


# Get user details
welcome_user()
username = get_username()
greet_user(username)


# Extract and tokenize text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

print(articleWords)
# for sentenceText in articleSentences:
#     print(sentenceText + "\n")