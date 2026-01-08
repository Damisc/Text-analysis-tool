# importing flask module in the project is mandatory
# An object of flask class is our WSGI application
from flask import Flask

# Flask constructor takes the name of current module (__name__) as argument
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL sould call the associated function
@app.route("/health")
def healthCheck():
    return "Flask Server is up and Running"

@app.route("/analyze-stock")
def analyzeStock():
    return {"data": "analysis coming soon"}

# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application on the local development server
    app.run()