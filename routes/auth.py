

from flask import Blueprint, request, redirect, session
from config import SHOPIFY_API_KEY, ASSISTRO_AUTH_API, SHOPIFY_API_VERSION, redirect_url, webhook_endpoint


auth_bp = Blueprint('auth', __name__)

#fuunction for creating the webhook event
def create_shopify_webhooks(access_token, webhook_endpoint, shop_name):
    events = ['orders/create', 'orders/fulfilled', 'orders/paid', 'orders/cancelled']

    for event in events:
        endpoint = f"https://{shop_name}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/webhooks.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        webhook_data = {
            "webhook": {
                "topic": event,
                "address": webhook_endpoint ,  
                "format": "json"
            }
        }

        response = requests.post(endpoint, json=webhook_data, headers=headers)
        
        #for testing purpose only
        if response.status_code == 201:
            print(f"Webhook for {event} created successfully.")
        else:
            print(f"Failed to create webhook for {event}.")
            print(f"Response: {response.status_code} - {response.text}")



# Redirect store owners to Shopify for OAuth authentication when he wants to add our plugin
@auth_bp.route('/auth/shopify', methods=['GET'])
def authenticate_shopify():
    shop = request.args.get('shop')
    
    redirect_uri = 'https://localhost/apps/auth/shopify/callback'
    auth_url = f"https://{shop}.myshopify.com/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope=read_orders&redirect_uri={redirect_uri}"
    
    return redirect(auth_url)



# Handling the OAuth callback from Shopify with access token for the store owner
@auth_bp.route('/auth/shopify/callback', methods=['GET'])
def shopify_callback():
    access_token = request.args.get('access_token')
    shop_nm = request.args.get('shop')
    

    session['access_token'] = access_token
    session['shop_owner'] = shop
    
    if 'access_token' in session:
        create_shopify_webhooks(session['access_token'], webhook_endpoint, shop_nm)
        return redirect('ASSISTRO_AUTH_API')
    else:
        return redirect('redirect_url')
    



@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('access_token', None)
    session.pop('shop_owner', None)
    return "Logged out successfully."
