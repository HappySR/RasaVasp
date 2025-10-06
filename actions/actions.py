from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

class ActionCompareProducts(Action):
    """Custom action to handle product comparisons"""
    
    def name(self) -> Text:
        return "action_compare_products"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Normalize variations
        user_message = user_message.replace('desallite', 'desalite')
        user_message = user_message.replace('des alite', 'desalite')
        
        # Detect if it's a comparison between Ednect and Desalite
        if ('ednect' in user_message and 'desalite' in user_message) or \
           ('ednect' in user_message and 'desalite connect' in user_message):
            
            response = """**Comparing Ednect vs Desalite Connect:**

Both are excellent School Management ERP systems from Vasp Technologies. Here are the key differences:

**EDNECT:**
- Developed by Vasp Technologies
- 10+ years of experience
- Served 500+ clients, 1K+ developments
- Used by: Heritage Public School, Reality Public School, Seppa Public School
- Modern Cloud ERP with innovative technology
- Comprehensive modules for complete school management

**DESALITE CONNECT:**
- 5+ years of experience in the market
- User-friendly interface design focus
- Used by prestigious institutions: Saint Francis De Sales Schools (multiple locations), Green Mount School, NPS International School, Shalom Public School
- Additional features: Library Management, Online Assessment, Digital Evaluation
- Proven track record with educational institutions

**Similarities:**
✓ Both offer: Staff, HR, Student, Fee, Attendance, Timetable, Report, Exam Management
✓ Cloud-based solutions
✓ Customizable to institution needs
✓ Integrated payment gateways
✓ Parent and student portals
✓ Comprehensive training and support

**Which to choose?**
- Ednect: Better for institutions wanting a mature product with extensive deployment history
- Desalite Connect: Better for institutions prioritizing user experience and working with educational networks

Would you like a personalized demo to see which fits your institution better? Contact: +91 7099020876"""
            
            dispatcher.utter_message(text=response)
            return []
        
        # Comparison with TransTrack
        elif ('transtrack' in user_message and ('ednect' in user_message or 'desalite' in user_message or 'icebox' in user_message)):
            response = """TransTrack is our **Transport Management System** (TMS), which is completely different from our school management systems:

**TransTrack** is for:
• Logistics and transportation companies
• Supply chain optimization
• Carrier management
• Route optimization
• Real-time shipment tracking

**Ednect/Desalite** are for:
• Educational institutions
• School administration
• Student and staff management
• Academic operations

These serve different industries. Which industry are you interested in?"""
            
            dispatcher.utter_message(text=response)
            return []
        
        # Comparison with IceBox
        elif 'icebox' in user_message and ('ednect' in user_message or 'desalite' in user_message or 'transtrack' in user_message):
            response = """IceBox is our **Cold Storage Management System**, which serves a different industry:

**IceBox** is for:
• Cold storage facilities
• Warehouse management
• Temperature-controlled storage
• Inventory tracking for perishables

**Ednect/Desalite** are for educational institutions.
**TransTrack** is for logistics/transportation.

These are industry-specific solutions. Which industry solution interests you?"""
            
            dispatcher.utter_message(text=response)
            return []
        
        # Generic comparison request
        else:
            response = """We offer 4 distinct products for different industries:

🏫 **School Management:**
   • Ednect (10+ years experience)
   • Desalite Connect (5+ years experience)

🚛 **Transport Management:**
   • TransTrack (Logistics & Supply Chain)

❄️ **Cold Storage Management:**
   • IceBox (Warehouse & Temperature Control)

Which products would you like me to compare?"""
            
            dispatcher.utter_message(text=response)
            return []


class ActionIntelligentResponse(Action):
    """Handle complex queries with multiple product mentions"""
    
    def name(self) -> Text:
        return "action_intelligent_response"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        intent = tracker.latest_message['intent'].get('name')
        
        # Detect multiple products in query
        products_mentioned = []
        if 'ednect' in user_message:
            products_mentioned.append('ednect')
        if 'desalite' in user_message or 'desalite connect' in user_message:
            products_mentioned.append('desalite')
        if 'transtrack' in user_message or 'trans track' in user_message:
            products_mentioned.append('transtrack')
        if 'icebox' in user_message or 'ice box' in user_message:
            products_mentioned.append('icebox')
        
        # If multiple products mentioned, provide comparative info
        if len(products_mentioned) > 1:
            return self._handle_multiple_products(dispatcher, products_mentioned, user_message)
        
        # If asking about features across products
        if any(word in user_message for word in ['all', 'every', 'which products', 'what products']):
            if 'feature' in user_message or 'module' in user_message:
                response = """Here's what each product offers:

**EDNECT & DESALITE CONNECT** (School Management):
• Staff & HR Management
• Student Management
• Fee Management
• Attendance Tracking
• Timetable Management
• Report Management
• Exam Result Management

**TRANSTRACK** (Transport Management):
• Transportation Planning
• Carrier Management
• Real-time Tracking
• Route Optimization
• Load Consolidation
• Supply Chain Analytics

**ICEBOX** (Cold Storage):
• Inventory Management
• Temperature Control
• Security Features
• Automated Workflow
• Detailed Billing & Reports

Which product's features interest you most?"""
                dispatcher.utter_message(text=response)
                return []
        
        # Default: Let normal flow handle it
        return []
    
    def _handle_multiple_products(self, dispatcher, products, user_message):
        if 'ednect' in products and 'desalite' in products:
            # Call comparison logic
            response = """Both Ednect and Desalite Connect are School Management ERPs:

**Key Difference:**
• Ednect: 10+ years experience, 500+ clients
• Desalite Connect: 5+ years, extensive school network

Both have same core features. Choice depends on your preference for:
- Deployment history (Ednect)
- User experience focus (Desalite)

Want a detailed comparison? Contact: +91 7099020876"""
            
        else:
            response = f"""You mentioned multiple products: {', '.join(products).upper()}

These serve different industries:
• Ednect/Desalite: Education
• TransTrack: Logistics
• IceBox: Cold Storage

Which specific product would you like to know about?"""
        
        dispatcher.utter_message(text=response)
        return []


class ActionExtractContext(Action):
    """Extract and store context from user queries"""
    
    def name(self) -> Text:
        return "action_extract_context"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Extract product mentions
        current_product = None
        if 'ednect' in user_message:
            current_product = 'ednect'
        elif 'desalite' in user_message:
            current_product = 'desalite'
        elif 'transtrack' in user_message:
            current_product = 'transtrack'
        elif 'icebox' in user_message:
            current_product = 'icebox'
        
        # Extract institution type if mentioned
        institute_type = None
        if any(word in user_message for word in ['school', 'college', 'university', 'institution']):
            if 'school' in user_message:
                institute_type = 'school'
            elif 'college' in user_message:
                institute_type = 'college'
            elif 'university' in user_message:
                institute_type = 'university'
        
        slots_to_set = []
        if current_product:
            slots_to_set.append(SlotSet("product_name", current_product))
        if institute_type:
            slots_to_set.append(SlotSet("institute_type", institute_type))
        
        return slots_to_set


class ActionFallbackWithContext(Action):
    """Intelligent fallback that considers context"""
    
    def name(self) -> Text:
        return "action_fallback_with_context"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        
        # Check if any product is mentioned
        products = []
        if 'ednect' in user_message.lower():
            products.append('Ednect')
        if 'desalite' in user_message.lower():
            products.append('Desalite Connect')
        if 'transtrack' in user_message.lower():
            products.append('TransTrack')
        if 'icebox' in user_message.lower():
            products.append('IceBox')
        
        if products:
            response = f"I understand you're asking about {', '.join(products)}, but I'm not sure exactly what you'd like to know. \n\nI can help with:\n• Product features\n• Pricing\n• Implementation\n• Client list\n• Comparison\n• Contact information\n\nWhat would you like to know?"
        else:
            response = """I'm not sure I understood that correctly. I can help you with:

📚 **Products:** Ednect, Desalite Connect, TransTrack, IceBox
💡 **Information:** Features, Pricing, Clients, Implementation
📞 **Support:** Contact info, Demo requests, Training

What would you like to know about?"""
        
        dispatcher.utter_message(text=response)
        return []


class ActionProvideRecommendation(Action):
    """Provide product recommendations based on user needs"""
    
    def name(self) -> Text:
        return "action_provide_recommendation"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Detect user's industry/need
        if any(word in user_message for word in ['school', 'college', 'education', 'student', 'institute']):
            response = """For educational institutions, I recommend:

**EDNECT or DESALITE CONNECT** - Both are excellent School Management ERPs

Choose **Ednect** if:
✓ You want proven track record (10+ years, 500+ clients)
✓ You need extensive ERP experience
✓ You're looking for comprehensive deployments

Choose **Desalite Connect** if:
✓ You prioritize user-friendly interface
✓ You're part of an educational network
✓ You want additional features like Library & Digital Evaluation

Both offer the same core functionality. Would you like a demo? Call: +91 7099020876"""
        
        elif any(word in user_message for word in ['transport', 'logistics', 'shipping', 'delivery', 'carrier']):
            response = """For transportation and logistics needs, I recommend:

**TRANSTRACK** - Our Transport Management System

Perfect for:
✓ Logistics companies
✓ Transportation businesses
✓ Supply chain optimization
✓ Fleet management
✓ Shipment tracking

Features: Route optimization, Real-time tracking, Carrier management, Cost savings

Contact: +91 8811047292"""
        
        elif any(word in user_message for word in ['cold storage', 'warehouse', 'storage', 'cold chain', 'temperature']):
            response = """For cold storage and warehouse management, I recommend:

**ICEBOX** - Our Cold Storage Management System

Perfect for:
✓ Cold storage facilities
✓ Warehouse operations
✓ Temperature-controlled storage
✓ Perishable goods management

Features: Temperature control, Inventory tracking, Automated workflow, Security monitoring

Contact: +91 8811047292"""
        
        else:
            response = """To recommend the right product, I need to know your industry:

🏫 **Educational Institution?** → Ednect or Desalite Connect
🚛 **Logistics/Transportation?** → TransTrack
❄️ **Cold Storage/Warehouse?** → IceBox

Which industry are you in?"""
        
        dispatcher.utter_message(text=response)
        return []