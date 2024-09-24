"""
Responsible for communicating with Stripe
"""

from flask import Blueprint
import os
import stripe

# Stripe API key
stripe.api_key = os.environ.get("test_stripe_api")

# stripe.checkout.Session.create(
    
# )