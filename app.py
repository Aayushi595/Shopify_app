from flask import Flask
from routes.auth import auth_bp
from routes.shopify import shopify_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(shopify_bp, url_prefix='/shopify')


# @app.route('/')
# def entry():
#     if 'access_token' in session:
#         # User is authenticated, you can redirect or render a dashboard here
#         return "Welcome! User is authenticated."
#     else:
#         return "Please authenticate first."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
