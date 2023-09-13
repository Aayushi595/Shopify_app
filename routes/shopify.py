# routes/shopify.py

from flask import Blueprint, request, jsonify
import shopify
import requests
from config import WAPUSH_API_URL

shopify_bp = Blueprint('shopify', __name__)

# Shopify API Integration
# ...

# Route to handle incoming Shopify webhook notifications
@shopify_bp.route('/webhook', methods=['POST'])
def handle_shopify_webhook():
    try:
        # Verify the webhook request is from Shopify (you can implement this verification)
        # Extract the webhook payload
        data = request.get_json()

        # Check if the webhook is an order creation or order status change event
        if data.get('topic') in ['orders/create', 'orders/updated']:
            # Extract relevant information from the webhook payload
            order = data['order']
            customer = order['customer']
            customer_name = customer['first_name']
            customer_phone = customer.get('phone')
            order_id = order['order_number']
            order_status = order['financial_status']  # You can customize this based on your needs
            
            # Construct the WhatsApp message
            message = f"Hello {customer_name}, your order with order ID {order_id} is {order_status}."
            
            # Call your WAPush API to send the WhatsApp notification
            response = requests.post(WAPUSH_API_URL, json={
                "phone_number": customer_phone,
                "message": message
            })
            
            if response.status_code == 200:
                print(f"WhatsApp notification sent for order {order_id}")
            else:
                print(f"Failed to send WhatsApp notification for order {order_id}")
            
            return jsonify({"message": "Webhook handled successfully."}), 200

        # Handle other webhook events if needed
        
        return jsonify({"message": "Webhook event not handled."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
