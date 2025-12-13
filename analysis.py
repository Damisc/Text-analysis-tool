
def welcome_user():
    # Welcome user
    print("Welcome to the text analysis tool, i will mine and analyze a body of text from a file you give me")

def get_username():
    # print message prompting user to input their name 
    usernameFromInput = input("To begin, Please enter your username: ")
    return usernameFromInput

def greet_user(name):
    # Greet the user
    print("Hello " + name)
    
welcome_user()
username = get_username()
greet_user(username)
