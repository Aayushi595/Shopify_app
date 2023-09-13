

from flask import Flask, session

# Create the Flask app
app = Flask(__name__)

app.secret_key = 'your_secret_key'


from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    if 'access_token' in session:
        # User is authenticated, you can redirect or render a dashboard here
        return "Welcome! User is authenticated."
    else:
        return "Please authenticate first."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
