# routes/auth.py

from flask import Blueprint, request, redirect, session
from config import SHOPIFY_API_KEY, ASSISTRO_AUTH_API

auth_bp = Blueprint('auth', __name__)

# Redirect users to Shopify for OAuth authentication
@auth_bp.route('/auth/shopify', methods=['GET'])
def authenticate_shopify():
    shop = request.args.get('shop')
    
    # Redirect to Shopify's OAuth authorization URL
    redirect_uri = 'https://localhost/apps/Plugin/auth/shopify/callback'
    auth_url = f"https://{shop}.myshopify.com/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope=read_orders&redirect_uri={redirect_uri}"
    
    return redirect(auth_url)

# Handle the OAuth callback from Shopify
@auth_bp.route('/auth/shopify/callback', methods=['GET'])
def shopify_callback():
    
    # Extract the access token and shop name from the callback
    # Store the Shopify access token in the session
    
    access_token = request.args.get('access_token')
    shop = request.args.get('shop')
    
    # Store the Shopify access token in the session
    session['access_token'] = access_token
    session['shop_owner'] = shop
    
    return redirect('/register')  # Assistro ko external api ko use krna h.

# Implement a route to log out the user if needed
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('access_token', None)
    session.pop('shop_owner', None)
    return "Logged out successfully."
