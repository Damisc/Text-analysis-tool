from random_username.generate import generate_username



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


def greet_user(name):
    # Greet the user
    print("Hello " + name)
    
welcome_user()
username = get_username()
greet_user(username)
