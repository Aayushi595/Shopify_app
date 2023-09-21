# routes/shopify.py

from flask import Blueprint, request, jsonify
import shopify
import requests
from config import WAPUSH_API_URL

app = Flask(__name__)
shopify_bp = Blueprint('shopify', __name__)
app.register_blueprint(shopify_bp)

shopify_bp = Blueprint('shopify', __name__)


# This route will be hit whenever Shopify sends a webhook request to the plugin. 
@shopify_bp.route('/webhook', methods=['POST'])
def handle_shopify_webhook():
    try:
        # Extract the webhook payload
        data = request.get_json()

        
        if data.get('topic') in ['orders/create', 'orders/cancelled','orders/fulfillment']:
            customer_name = data['customer']['first_name']
            customer_phone = data['customer'].get('phone')
            order_id = data['id']
        
        if data.get('topic') == ['orders/paid']:
            customer_name = data['customer']['first_name']
            customer_phone = data['customer'].get('phone')
            order_id = data['id']
            order_status = data['fulfillment_status']


        if data['topic'] == 'orders/create':
            message = f"Hello {customer_name}, thank you for placing an order with order ID {order_id}. Your order is currently being processed."

        elif data['topic'] == 'orders/cancelled':
            message = f"Hello {customer_name}, we regret to inform you that your order with order ID {order_id} has been cancelled."

        elif data['topic'] == 'orders/fulfilled':
            message = f"Hello {customer_name}, your order with order ID {order_id} has been shipped and is on its way to you."

        elif data['topic'] == 'orders/paid':
            message = f"Hello {customer_name}, your order with order ID {order_id} is {fulfillment_status} . Thank you for your purchase."

        
            
            # Calling WAPush API to send the WhatsApp notification
            response = requests.post(WAPUSH_API_URL, json={
                "phone_number": customer_phone,
                "message": message
            })
            
            if response.status_code == 200:
                print(f"WhatsApp notification sent for order {order_id}")
            else:
                print(f"Failed to send WhatsApp notification for order {order_id}")
            
            return jsonify({"message": "Webhook handled successfully."}), 200

    
        
        return jsonify({"message": "Webhook event not handled."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
