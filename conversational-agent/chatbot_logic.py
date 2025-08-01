# chatbot_logic.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

faq_data = [ 
    # Greetings (expanded)
    {"question": "hi|hello|hey|good morning|good afternoon|good evening|hiya|yo|what's up|howdy|greetings|sup|hey there|hello there|nice to meet you|pleased to meet you|good day|morning|afternoon|evening", "answer": "Hello! How can I assist you today?"},
    # Thanks (expanded)
    {"question": "thank you|thanks|thanks a lot|thank you so much|appreciate it|thx|ty|much appreciated|many thanks|thanks for your help|thanks for helping|thank you very much|thanks so much|thanks for your assistance|thanks for your support|grateful|cheers", "answer": "You're welcome! If you need anything else, just ask."},
    # Ending chat (expanded)
    {"question": "good night|bye|see you|goodbye|see ya|see you later|talk to you later|end chat|exit|close chat|farewell|take care|catch you later|see you soon|see you next time|have a nice day|have a good day|have a great day|peace out|later|bye bye|ciao|adios|until next time|sign off|logging off|disconnect|stop chat|stop talking|quit", "answer": "Goodbye! If you have more questions, feel free to chat again. Have a great day!"},
{"question": "How can I reset my password?",
     "answer": "To reset your password, follow these steps:\n1. Go to the login page.\n2. Click on 'Forgot Password'.\n3. Enter your registered email address.\n4. Follow the link sent to your inbox to reset your password."},

    {"question": "What payment methods are accepted?",
     "answer": "We accept the following payment methods:\n- 💸 UPI (Google Pay, PhonePe, Paytm)\n- 💳 Credit/Debit Cards (Visa, MasterCard, RuPay)\n- 🏦 Net Banking\n- 📲 Wallets (Paytm Wallet, Amazon Pay)"},

    {"question": "Do you ship internationally?",
     "answer": "Yes, we ship to select countries outside India.\nCurrently, international shipping is available to:\n- 🇺🇸 United States\n- 🇬🇧 United Kingdom\n- 🇩🇪 Germany\n- 🇦🇪 United Arab Emirates\nInternational shipping charges apply and vary by destination."},

    {"question": "How do I contact customer support?",
     "answer": "You can contact us through the following channels:\n- 📧 Email: <a href='mailto:support@example.com'>support@example.com</a>\n- 📞 Phone: <a href='tel:+911800123456'>1800-123-456</a> (Mon–Fri, 9AM–6PM IST)"},

    {"question": "How can I track my delivery?",
     "answer": "You can track your order using our tracking portal:\n👉 <a href='https://track.example.com'>track.example.com</a>\nEnter your order ID and registered email/mobile to get real-time status."},

    {"question": "What is your return policy?",
     "answer": "We offer a 30-day return policy for most items.\n✅ Conditions:\n- Product must be unused and in original packaging.\n- Return must be initiated within 30 days of delivery.\n- Refund is processed within 5–7 business days after inspection.\n📌 Note: Some perishable items are non-returnable."},

    {"question": "How do I create a new account?",
     "answer": "Follow these steps to create your account:\n1. Go to our website homepage.\n2. Click on 'Sign Up' or 'Register'.\n3. Fill in your name, email, mobile number, and password.\n4. Click 'Create Account'.\n✅ You'll receive a welcome email upon successful registration."},

    {"question": "How do I delete my account?",
     "answer": "To delete your account permanently:\n1. Login to your account.\n2. Go to 'Settings' > 'Account Settings'.\n3. Click on 'Delete My Account'.\n4. Confirm the deletion via OTP sent to your registered mobile/email.\n❗ Note: This action is irreversible."},

    {"question": "What is the refund policy?",
     "answer": "Refunds are processed under these terms:\n- You must raise a return or refund request within 30 days.\n- Item must pass inspection.\n- Refund is credited to your original payment method within 5–7 working days.\n⚠️ Digital products are not eligible for refund."},

    {"question": "Can I pay using PhonePe?",
     "answer": "Yes! We accept PhonePe as one of our UPI payment options.\nJust choose UPI at checkout and select PhonePe from the list of apps."},

    {"question": "How long does delivery take within India?",
     "answer": "📦 Standard delivery time within India is 3–7 business days.\n📌 Remote locations may take additional time.\nTrack your order here: <a href='https://track.example.com'>track.example.com</a>"},

    {"question": "How do I return a damaged product?",
     "answer": "If you've received a damaged product:\n1. Raise a return request within 48 hours of delivery.\n2. Upload clear photos of the damage.\n3. Our support team will arrange a free pickup.\n4. Refund or replacement will be processed post verification."},

    {"question": "Can I cancel an order after placing it?",
     "answer": "Yes, you can cancel an order within 2 hours of placing it.\nGo to 'My Orders' > Select Order > 'Cancel'.\nIf the order is already shipped, cancellation is not possible."},

    {"question": "What is the delivery charge?",
     "answer": "Delivery is free for orders above ₹499.\nA flat ₹50 delivery fee applies to orders below that."},

    {"question": "How do I reset my account password?",
     "answer": "Click 'Forgot Password' on the login page.\nEnter your registered email.\nClick the link sent to your inbox and set a new password."},

    {"question": "Is Cash on Delivery available?",
     "answer": "Yes, COD is available for orders up to ₹2,000.\nAdditional ₹30 COD charge applies."},

    {"question": "Can I return an opened item?",
     "answer": "Opened items can only be returned if damaged or defective.\nEnsure the original packaging is retained."},

    {"question": "What products are non-returnable?",
     "answer": "Products that are non-returnable include:\n- Perishable goods (groceries, fresh food)\n- Intimate wear\n- Gift cards and digital downloads"},

    {"question": "Do you offer gift wrapping?",
     "answer": "Yes, gift wrapping can be selected at checkout for ₹49 extra.\nIncludes decorative wrap and custom message card."},

    {"question": "How can I change my shipping address?",
     "answer": "You can change your shipping address before the order is shipped.\nGo to 'My Orders' > Edit Address."},

    {"question": "Why am I locked out of my account?",
     "answer": "Multiple failed login attempts trigger a 2-hour lock. Reset your password or contact support for immediate help."},

    {"question": "How do I update my email address?",
     "answer": "Go to Profile > Edit Contact Info. Verify the new email via OTP to complete the change."},

    {"question": "How do I enable two-factor authentication?",
     "answer": "Go to Account Settings > Security > Enable 2FA. Choose SMS or authenticator app for verification codes."},

    {"question": "Are there hidden charges?",
     "answer": "No hidden fees. Final checkout price includes product cost + GST + shipping (if applicable)."},

    {"question": "Do you offer EMI options?",
     "answer": "Yes! EMI via Credit Cards (3–12 months) and select debit cards. Check eligibility at checkout."},

    {"question": "Why was my card declined?",
     "answer": "Common reasons: Insufficient funds, incorrect CVV, or bank restrictions. Try another card or UPI."},

    {"question": "Do you offer same-day delivery?",
     "answer": "Yes, in 15 major cities for orders placed before 12 PM. Extra ₹99 fee applies."},

    {"question": "Can I change my delivery date?",
     "answer": "For premium orders, use the 'Reschedule' option in tracking portal. Standard orders cannot be changed."},

    {"question": "What if I miss my delivery?",
     "answer": "Courier will attempt 2 more times. After that, contact support to rearrange delivery."},

    {"question": "How do I exchange a product?",
     "answer": "Initiate a return for the original item and place a new order for the replacement."},

    {"question": "Where is my refund?",
     "answer": "Refunds take 5–10 business days post-approval. Check with your bank if delayed further."},

    {"question": "Can I return a gifted item?",
     "answer": "Yes! Use the gift receipt number to process returns. Refund goes to the original payer."},

    {"question": "The website isn't loading—what do I do?",
     "answer": "Clear browser cache or try incognito mode. If issues persist, check our server status page."},

    {"question": "Why can't I add items to my cart?",
     "answer": "Likely a browser glitch. Refresh or switch devices. Ensure cookies are enabled."},

    {"question": "How do I disable notifications?",
     "answer": "Go to Profile > Notification Preferences > Toggle off email/SMS alerts."},

    {"question": "How do I check product authenticity?",
     "answer": "All products include a QR code for verification. Scan it using our app."},

    {"question": "Can I request a product demo?",
     "answer": "Yes! Book a video demo via 'Contact Us'. Available for electronics & appliances."},

    {"question": "Where are your products manufactured?",
     "answer": "Sourced globally—60% made in India, 40% imported from EU/US/ASEAN countries."},

    {"question": "How does your loyalty program work?",
     "answer": "Earn 1 point per ₹100 spent. 100 points = ₹50 discount. Gold tier unlocks free shipping."},

    {"question": "How do I redeem reward points?",
     "answer": "At checkout, toggle 'Use Points' and apply your balance to the order total."},

    {"question": "Do points expire?",
     "answer": "Yes, points expire after 365 days of inactivity. Regular purchases keep them active."},

    {"question": "Do you offer bulk discounts?",
     "answer": "Yes! Email bulkorders@example.com with your requirements for negotiated pricing."},

    {"question": "Can I get a tax invoice?",
     "answer": "Download invoices from 'My Orders' or request via email to billing@example.com."},

    {"question": "Do you have a business account option?",
     "answer": "Yes—register as a business to access GST invoices, bulk pricing, and dedicated support."},

    {"question": "How do I unsubscribe from emails?",
     "answer": "Click 'Unsubscribe' in any newsletter footer or adjust preferences in your account."},

    {"question": "Can I order without creating an account?",
     "answer": "Yes! Use 'Guest Checkout', but tracking/returns require account registration later."},

    {"question": "Do you support screen readers for accessibility?",
     "answer": "Yes, our website is WCAG 2.1 compliant. Use alt text and ARIA labels for navigation."},

    {"question": "What's your customer satisfaction rate?",
     "answer": "We maintain a 96% satisfaction score based on post-purchase surveys."},

    {"question": "Are your packaging materials eco-friendly?",
     "answer": "Yes! 100% recycled/recyclable materials. Opt out of excess packaging at checkout."},

    {"question": "How do I apply a discount coupon?",
     "answer": "Paste the code in the 'Promo Code' box at checkout or select from saved offers."},

    {"question": "Do you price-match competitors?",
     "answer": "Yes! Submit a claim within 48 hours of purchase with proof of lower pricing."},
    # Hours variations
    {"question": "what are your hours|working hours|business hours|when are you open|opening hours|opening time|closing time|when do you close|when do you open|office hours|timings|work hours|hours of operation|what time do you open|what time do you close|store hours|shop hours|service hours|support hours|customer service hours|when is your office open|when is your office closed|when can I contact you|when are you available|availability|office timing|office timings|office schedule|office open|office close|office opening|office closing|office working hours|office business hours|office operation hours|office support hours|office customer service hours|office service hours|office shop hours|office store hours|office work hours|office hours of operation|office opening time|office closing time|office open time|office close time|office open hours|office close hours|office open timings|office close timings|office open schedule|office close schedule|office open availability|office close availability|office open support|office close support|office open customer service|office close customer service|office open service|office close service|office open shop|office close shop|office open store|office close store|office open work|office close work|office open operation|office close operation|office open business|office close business|office open business hours|office close business hours|office open operation hours|office close operation hours|office open support hours|office close support hours|office open customer service hours|office close customer service hours|office open service hours|office close service hours|office open shop hours|office close shop hours|office open store hours|office close store hours|office open work hours|office close work hours|office open hours of operation|office close hours of operation|office open opening time|office close opening time|office open closing time|office close closing time|office open open time|office close open time|office open close time|office close close time|office open open hours|office close open hours|office open close hours|office close close hours|office open open timings|office close open timings|office open close timings|office close close timings|office open open schedule|office close open schedule|office open close schedule|office close close schedule|office open open availability|office close open availability|office open close availability|office close close availability|office open open support|office close open support|office open close support|office close close support|office open open customer service|office close open customer service|office open close customer service|office close close customer service|office open open service|office close open service|office open close service|office close close service|office open open shop|office close open shop|office open close shop|office close close shop|office open open store|office close open store|office open close store|office close close store|office open open work|office close open work|office open close work|office close close work|office open open operation|office close open operation|office open close operation|office close close operation|office open open business|office close open business|office open close business|office close close business", "answer": "We're open Monday to Friday, 9am to 5pm."},
    # Office location variations
    {"question": "where is your office located|office location|where are you located|address|location|where is your office|where can I find you|where is your company|where is your business|where is your store|where is your shop|where is your headquarters|where is your main office|where is your branch|where is your branch office|where is your head office|where is your corporate office|where is your registered office|where is your admin office|where is your admin branch|where is your admin headquarters|where is your admin main office|where is your admin branch office|where is your admin head office|where is your admin corporate office|where is your admin registered office|where is your admin admin office|where is your admin admin branch|where is your admin admin headquarters|where is your admin admin main office|where is your admin admin branch office|where is your admin admin head office|where is your admin admin corporate office|where is your admin admin registered office|where is your admin admin admin office|where is your admin admin admin branch|where is your admin admin admin headquarters|where is your admin admin admin main office|where is your admin admin admin branch office|where is your admin admin admin head office|where is your admin admin admin corporate office|where is your admin admin admin registered office|where is your admin admin admin admin office|where is your admin admin admin admin branch|where is your admin admin admin admin headquarters|where is your admin admin admin admin main office|where is your admin admin admin admin branch office|where is your admin admin admin admin head office|where is your admin admin admin admin corporate office|where is your admin admin admin admin registered office|where is your admin admin admin admin admin office|where is your admin admin admin admin admin branch|where is your admin admin admin admin admin admin admin headquarters|where is your admin admin admin admin admin admin admin main office|where is your admin admin admin admin admin admin admin branch office|where is your admin admin admin admin admin admin admin head office|where is your admin admin admin admin admin admin admin corporate office|where is your admin admin admin admin admin admin admin registered office|where is your admin admin admin admin admin admin admin admin office|where is your admin admin admin admin admin admin admin admin branch|where is your admin admin admin admin admin admin admin admin headquarters|where is your admin admin admin admin admin admin admin admin main office|where is your admin admin admin admin admin admin admin admin branch office|where is your admin admin admin admin admin admin admin admin head office|where is your admin admin admin admin admin admin admin admin corporate office|where is your admin admin admin admin admin admin admin admin registered office|where is your admin admin admin admin admin admin admin admin admin office|where is your admin admin admin admin admin admin admin admin admin branch|where is your admin admin admin admin admin admin admin admin admin headquarters|where is your admin admin admin admin admin admin admin admin admin main office|where is your admin admin admin admin admin admin admin admin admin branch office|where is your admin admin admin admin admin admin admin admin admin head office|where is your admin admin admin admin admin admin admin admin admin corporate office|where is your admin admin admin admin admin admin admin admin admin registered office", "answer": "Our main office is at 123 Business Park, Suite 456."},
] # Copy the full FAQ list here

model = SentenceTransformer("all-MiniLM-L6-v2")

questions = [item["question"] for item in faq_data]
embeddings = model.encode(questions)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def get_response(user_input, top_k=1, threshold=5.0):  # increased threshold for better matching
    query_vec = model.encode([user_input])
    D, I = index.search(np.array(query_vec), k=top_k)
    match_score = D[0][0]
    best_idx = I[0][0]

    # ✅ L2 score is better when smaller
    if match_score < threshold:
        return faq_data[best_idx]["answer"]
    else:
        return "🤖 Sorry, I couldn’t find an exact answer. Please contact support."
