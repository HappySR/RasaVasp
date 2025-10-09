from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

class ActionCompareProducts(Action):
    """Custom action to handle all product comparisons with concise, scannable responses"""
    
    def name(self) -> Text:
        return "action_compare_products"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Normalize variations
        user_message = user_message.replace('desallite', 'desalite')
        user_message = user_message.replace('des alite', 'desalite')
        user_message = user_message.replace('trans track', 'transtrack')
        user_message = user_message.replace('ice box', 'icebox')
        
        # Detect products mentioned
        products = []
        if 'ednect' in user_message:
            products.append('ednect')
        if 'desalite' in user_message:
            products.append('desalite')
        if 'transtrack' in user_message:
            products.append('transtrack')
        if 'icebox' in user_message:
            products.append('icebox')
        
        # Route to appropriate comparison
        if len(products) >= 2:
            response = self._compare_specific_products(products)
        elif len(products) == 1:
            response = self._suggest_comparison(products[0])
        else:
            response = self._general_comparison()
        
        dispatcher.utter_message(text=response)
        return []
    
    def _compare_specific_products(self, products: List[str]) -> str:
        """Generate concise comparisons based on products mentioned"""
        products_sorted = sorted(products)
        comparison_key = '-'.join(products_sorted)
        
        comparisons = {
            # School Management Comparisons
            'desalite-ednect': self._compare_ednect_desalite(),
            
            # School vs Transport Comparisons
            'ednect-transtrack': self._compare_ednect_transtrack(),
            'desalite-transtrack': self._compare_desalite_transtrack(),
            
            # School vs Cold Storage Comparisons
            'ednect-icebox': self._compare_ednect_icebox(),
            'desalite-icebox': self._compare_desalite_icebox(),
            
            # Transport vs Cold Storage Comparison
            'icebox-transtrack': self._compare_transtrack_icebox(),
            
            # Three-way comparisons
            'desalite-ednect-transtrack': self._compare_three_school_transport(),
            'ednect-icebox-transtrack': self._compare_three_all_except_desalite(),
            'desalite-ednect-icebox': self._compare_three_school_icebox(),
            'desalite-icebox-transtrack': self._compare_three_desalite_transport_icebox(),
            
            # Four-way comparison
            'desalite-ednect-icebox-transtrack': self._compare_all_products(),
        }
        
        return comparisons.get(comparison_key, self._general_comparison())
    
    def _compare_ednect_desalite(self) -> str:
        """Concise comparison between Ednect and Desalite Connect"""
        return """**Ednect vs Desalite Connect - Both School ERPs:**

**EDNECT:**
• 10+ years experience, 500+ clients
• Proven stability & reliability
• Mature product with extensive track record

**DESALITE CONNECT:**
• 5+ years, modern interface
• Better UX/UI design
• Extra features: Library, Online Assessment, Digital Evaluation

**Common Features:** Student/Staff Management, Fees, Attendance, Timetable, Exams, Reports, Parent Portal

**Choose Ednect:** Want proven 10-year track record
**Choose Desalite:** Want modern interface & extra features

📞 Demo: +91 7099020876"""

    def _compare_ednect_transtrack(self) -> str:
        """Concise comparison between Ednect and TransTrack"""
        return """**Ednect vs TransTrack - Different Industries:**

**EDNECT (Education):**
• School/College management
• Students, Staff, Fees, Academics
• For: Educational institutions

**TRANSTRACK (Logistics):**
• Transport & fleet management
• Route optimization, Shipment tracking
• For: Logistics companies, transporters

**Can't compare directly** - serve different industries.

**Need both?** Schools with bus fleet or diversified business can use both.

📞 Ednect: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_desalite_transtrack(self) -> str:
        """Concise comparison between Desalite Connect and TransTrack"""
        return """**Desalite Connect vs TransTrack - Different Industries:**

**DESALITE CONNECT (Education):**
• Modern school management ERP
• Student/Staff, Fees, Library, Online Assessment
• For: Schools, Colleges

**TRANSTRACK (Logistics):**
• Transport management system
• Route optimization, Real-time tracking, Cost savings
• For: Logistics companies, fleet operators

**Different purposes.** Use Desalite for school + TransTrack for school buses/transport division.

📞 Desalite: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_ednect_icebox(self) -> str:
        """Concise comparison between Ednect and IceBox"""
        return """**Ednect vs IceBox - Different Industries:**

**EDNECT (Education):**
• School/College ERP - 10+ years
• Students, Staff, Fees, Academics, Exams
• For: Educational institutions

**ICEBOX (Cold Storage):**
• Warehouse management system
• Inventory, Temperature control, Automated workflow
• For: Cold storage facilities, warehouses

**Different industries.** Agricultural schools, culinary institutes, or research institutions might need both.

📞 Ednect: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_desalite_icebox(self) -> str:
        """Concise comparison between Desalite Connect and IceBox"""
        return """**Desalite Connect vs IceBox - Different Industries:**

**DESALITE CONNECT (Education):**
• Modern school ERP - 5+ years
• Student/Staff, Fees, Library, Digital Evaluation
• For: Schools, Colleges

**ICEBOX (Cold Storage):**
• Cold storage management
• Temperature control, Inventory, Security, Billing
• For: Warehouses, cold chain operations

**Different purposes.** Culinary/agricultural schools with storage needs could use both.

📞 Desalite: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_transtrack_icebox(self) -> str:
        """Concise comparison between TransTrack and IceBox"""
        return """**TransTrack vs IceBox - Both Logistics, Different Focus:**

**TRANSTRACK (Transportation):**
• Goods in MOTION
• Route optimization, Shipment tracking, Carrier management
• For: Transport companies, fleet managers

**ICEBOX (Warehousing):**
• Goods in STORAGE
• Temperature control, Inventory, Security
• For: Cold storage, warehouses

**Work together:** Cold chain companies need BOTH - TransTrack for delivery + IceBox for storage.

📞 Contact: +91 8811047292"""

    def _compare_three_school_transport(self) -> str:
        """Concise comparison of Ednect, Desalite, and TransTrack"""
        return """**Ednect | Desalite | TransTrack:**

**School ERPs (Choose one):**
• **Ednect:** 10+ years, proven (500+ clients)
• **Desalite:** Modern UI, Library, Digital Evaluation
Both have: Student/Staff, Fees, Attendance, Exams

**TransTrack (Add if needed):**
• Transport/logistics management
• For: School buses OR separate transport business

**Common scenario:** School ERP + TransTrack for bus fleet management

📞 School ERPs: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_three_all_except_desalite(self) -> str:
        """Concise comparison of Ednect, TransTrack, and IceBox"""
        return """**Ednect | TransTrack | IceBox - 3 Industries:**

**EDNECT (Education):** School management - 10+ years
**TRANSTRACK (Logistics):** Transport & fleet management
**ICEBOX (Warehousing):** Cold storage management

**Use cases:**
• Education only → Ednect
• School + buses → Ednect + TransTrack
• School + cold storage → Ednect + IceBox (agricultural/culinary schools)
• All three → Diversified business group

📞 Ednect: +91 7099020876 | TransTrack/IceBox: +91 8811047292"""

    def _compare_three_school_icebox(self) -> str:
        """Concise comparison of Ednect, Desalite, and IceBox"""
        return """**Ednect | Desalite | IceBox:**

**School ERPs (Choose one):**
• **Ednect:** 10+ years, proven track record
• **Desalite:** Modern interface, Library, Digital Evaluation

**ICEBOX (Cold Storage):**
• Warehouse management, Temperature control
• For: Cold storage facilities

**Use together:** Agricultural/culinary/research institutions needing both academics + storage.

📞 School ERPs: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_three_desalite_transport_icebox(self) -> str:
        """Concise comparison of Desalite, TransTrack, and IceBox"""
        return """**Desalite | TransTrack | IceBox - 3 Industries:**

**DESALITE (Education):** Modern school ERP
**TRANSTRACK (Logistics):** Transport management
**ICEBOX (Warehousing):** Cold storage management

**Common combinations:**
• School + buses → Desalite + TransTrack
• School + storage → Desalite + IceBox (culinary/agricultural schools)
• Cold chain → TransTrack + IceBox (storage + delivery)
• All three → Diversified business group

📞 Desalite: +91 7099020876 | TransTrack/IceBox: +91 8811047292"""

    def _compare_all_products(self) -> str:
        """Comprehensive but concise comparison of all four products"""
        return """**Complete Product Suite:**

**EDUCATION (Choose one):**
• **Ednect:** 10+ years, 500+ clients, proven
• **Desalite:** Modern UI, Library, Digital Evaluation

**LOGISTICS:**
• **TransTrack:** Transport/fleet management, route optimization

**WAREHOUSING:**
• **IceBox:** Cold storage, temperature control, inventory

---

**Common Scenarios:**

**Single industry:** Pick your match
**School + buses:** School ERP + TransTrack
**School + storage:** School ERP + IceBox (agricultural/culinary)
**Cold chain:** TransTrack + IceBox
**Diversified group:** Multiple products

📞 School ERPs: +91 7099020876 | TransTrack/IceBox: +91 8811047292
📧 ajit@vasptechnologies.com"""

    def _suggest_comparison(self, product: str) -> str:
        """Concise suggestions for single product mention"""
        suggestions = {
            'ednect': """**You asked about Ednect** (School ERP - 10+ years)

Compare with:
1. **Desalite Connect** - Alternative school ERP (modern UI)
2. **TransTrack** - If you have transport needs
3. **IceBox** - If you have storage needs

📞 More info: +91 7099020876""",
            
            'desalite': """**You asked about Desalite Connect** (Modern School ERP)

Compare with:
1. **Ednect** - Alternative school ERP (10+ years proven)
2. **TransTrack** - If you manage transportation
3. **IceBox** - If you have warehousing needs

📞 More info: +91 7099020876""",
            
            'transtrack': """**You asked about TransTrack** (Transport Management)

Compare with:
1. **IceBox** - If you need storage + transport
2. **Ednect/Desalite** - If you're a school with transport

📞 More info: +91 8811047292""",
            
            'icebox': """**You asked about IceBox** (Cold Storage Management)

Compare with:
1. **TransTrack** - If you need storage + transport
2. **Ednect/Desalite** - If you're a school with storage

📞 More info: +91 8811047292"""
        }
        
        return suggestions.get(product, self._general_comparison())
    
    def _general_comparison(self) -> str:
        """Concise general overview"""
        return """**Our Product Suite:**

**EDUCATION:**
• **Ednect:** School ERP (10+ years, 500+ clients)
• **Desalite:** School ERP (Modern, 5+ years)

**LOGISTICS:**
• **TransTrack:** Transport management

**WAREHOUSING:**
• **IceBox:** Cold storage management

**Which to compare?** Examples:
• "Ednect vs Desalite" - School ERPs
• "TransTrack vs IceBox" - Logistics
• "All products" - Complete overview

📞 +91 7099020876 (School ERPs) | +91 8811047292 (TransTrack/IceBox)"""


class ActionIntelligentResponse(Action):
    """Handle complex queries with multiple product mentions"""
    
    def name(self) -> Text:
        return "action_intelligent_response"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Normalize variations
        user_message = user_message.replace('desallite', 'desalite')
        user_message = user_message.replace('des alite', 'desalite')
        user_message = user_message.replace('trans track', 'transtrack')
        user_message = user_message.replace('ice box', 'icebox')
        
        # Detect multiple products in query
        products_mentioned = []
        if 'ednect' in user_message:
            products_mentioned.append('ednect')
        if 'desalite' in user_message or 'desalite connect' in user_message:
            products_mentioned.append('desalite')
        if 'transtrack' in user_message:
            products_mentioned.append('transtrack')
        if 'icebox' in user_message:
            products_mentioned.append('icebox')
        
        # If multiple products mentioned, provide comparative info
        if len(products_mentioned) > 1:
            return self._handle_multiple_products(dispatcher, products_mentioned, user_message)
        
        # If asking about features across products
        if any(word in user_message for word in ['all', 'every', 'which products', 'what products']):
            if 'feature' in user_message or 'module' in user_message:
                response = """**Product Features:**

**EDNECT & DESALITE** (School):
Student/Staff, Fees, Attendance, Exams, Reports, Parent Portal

**TRANSTRACK** (Logistics):
Route optimization, Real-time tracking, Cost savings

**ICEBOX** (Cold Storage):
Temperature control, Inventory, Security, Billing

📞 +91 7099020876 (School) | +91 8811047292 (TransTrack/IceBox)"""
                dispatcher.utter_message(text=response)
                return []
        
        # Default: Let normal flow handle it
        return []
    
    def _handle_multiple_products(self, dispatcher, products, user_message):
        if 'ednect' in products and 'desalite' in products:
            response = """**Both are School ERPs:**

• **Ednect:** 10+ years, 500+ clients (proven)
• **Desalite:** 5+ years, modern UX (extra features)

Both have same core features. Main difference: Experience vs Modern UI.

📞 Detailed comparison: +91 7099020876"""
            
        else:
            response = f"""**You mentioned: {', '.join(products).upper()}**

• **Ednect/Desalite:** Education
• **TransTrack:** Logistics
• **IceBox:** Cold Storage

Different industries. Which comparison do you need?

📞 +91 7099020876 or +91 8811047292"""
        
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
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Check for job-related queries
        if any(word in user_message for word in ['job', 'vacancy', 'hiring', 'career', 'recruitment', 'employment']):
            response = """**Career Opportunities:**

📧 hr@vasptechnologies.co.in
📞 +91 7099020876

Check our website/LinkedIn for openings."""
            dispatcher.utter_message(text=response)
            return []
        
        # Check for purchase/acquisition queries
        if any(word in user_message for word in ['buy', 'purchase', 'get', 'acquire', 'obtain', 'order']):
            response = """**Get Started:**

1. **Free Demo** - See it in action
2. **Consultation** - Discuss requirements
3. **Quote** - Customized pricing
4. **Implementation** - Setup & training

📞 +91 7099020876 (Ednect/Desalite) | +91 8811047292 (TransTrack/IceBox)
📧 ajit@vasptechnologies.com"""
            dispatcher.utter_message(text=response)
            return []
        
        # Check for unrelated tech support
        if any(word in user_message for word in ['tech support', 'technical support', 'fix my', 'repair', 'not working', 'broken']):
            if not any(word in user_message for word in ['ednect', 'desalite', 'transtrack', 'icebox', 'vasp']):
                response = """I'm VaspX - I help with Vasp Technologies products (Ednect, Desalite, TransTrack, IceBox).

For unrelated tech support, contact the relevant provider.

📞 Our support: +91 7099020876 / +91 8811047292"""
                dispatcher.utter_message(text=response)
                return []
        
        # Check if any product is mentioned
        products = []
        if 'ednect' in user_message:
            products.append('Ednect')
        if 'desalite' in user_message or 'desallite' in user_message:
            products.append('Desalite')
        if 'transtrack' in user_message or 'trans track' in user_message:
            products.append('TransTrack')
        if 'icebox' in user_message or 'ice box' in user_message:
            products.append('IceBox')
        
        if products:
            response = f"""**About {', '.join(products)}** - I can help with:

• Features & pricing
• Implementation
• Client list
• Comparisons
• Demo requests

What would you like to know?

📞 +91 7099020876 / +91 8811047292"""
        else:
            response = """**VaspX - How can I help?**

**Products:** Ednect, Desalite, TransTrack, IceBox
**Info:** Features, Pricing, Clients, Demos
**Support:** Contact, Training, Implementation

📞 +91 7099020876 / +91 8811047292"""
        
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
            response = """**For Education:**

**EDNECT** → 10+ years, proven (500+ clients)
**DESALITE** → Modern UI, extra features (Library, Digital Evaluation)

Both have: Student/Staff, Fees, Attendance, Exams, Reports

📞 Demo: +91 7099020876"""
        
        elif any(word in user_message for word in ['transport', 'logistics', 'shipping', 'delivery', 'carrier']):
            response = """**For Logistics/Transport:**

**TRANSTRACK** - Transport Management System
• Route optimization
• Real-time tracking
• Cost savings
• Fleet management

📞 Demo: +91 8811047292"""
        
        elif any(word in user_message for word in ['cold storage', 'warehouse', 'storage', 'cold chain', 'temperature']):
            response = """**For Cold Storage/Warehouse:**

**ICEBOX** - Cold Storage Management
• Temperature control
• Inventory tracking
• Automated workflow
• Security monitoring

📞 Demo: +91 8811047292"""
        
        else:
            response = """**What's your industry?**

🎓 **Education** → Ednect or Desalite
🚛 **Logistics** → TransTrack
❄️ **Cold Storage** → IceBox

📞 +91 7099020876 / +91 8811047292"""
        
        dispatcher.utter_message(text=response)
        return []
    