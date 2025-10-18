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
        
        # Get last mentioned product from slot
        last_product = tracker.get_slot("last_mentioned_product")
        
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
        
        # Handle contextual comparisons like "compare it with ednect" or "with ednect"
        if len(products) == 1 and last_product and last_product not in products:
            # User wants to compare last product with newly mentioned product
            products.insert(0, last_product)
        elif len(products) == 0 and last_product:
            # User said something like "compare it" without mentioning product
            products.append(last_product)
        
        # Check for phrases like "with X" where X is a product
        if 'with' in user_message and len(products) == 1 and last_product:
            if last_product not in products:
                products.insert(0, last_product)
        
        # Route to appropriate comparison
        if len(products) >= 2:
            response = self._compare_specific_products(products)
        elif len(products) == 1:
            response = self._suggest_comparison(products[0])
        else:
            response = self._general_comparison()
        
        dispatcher.utter_message(text=response)
        
        # Update context
        if products:
            return [SlotSet("last_mentioned_product", products[-1])]
        return []
    
    def _compare_specific_products(self, products: List[str]) -> str:
        """Generate concise comparisons based on products mentioned"""
        products_sorted = sorted(products)
        comparison_key = '-'.join(products_sorted)
        
        comparisons = {
            'desalite-ednect': self._compare_ednect_desalite(),
            'ednect-transtrack': self._compare_ednect_transtrack(),
            'desalite-transtrack': self._compare_desalite_transtrack(),
            'ednect-icebox': self._compare_ednect_icebox(),
            'desalite-icebox': self._compare_desalite_icebox(),
            'icebox-transtrack': self._compare_transtrack_icebox(),
            'desalite-ednect-transtrack': self._compare_three_school_transport(),
            'ednect-icebox-transtrack': self._compare_three_all_except_desalite(),
            'desalite-ednect-icebox': self._compare_three_school_icebox(),
            'desalite-icebox-transtrack': self._compare_three_desalite_transport_icebox(),
            'desalite-ednect-icebox-transtrack': self._compare_all_products(),
        }
        
        return comparisons.get(comparison_key, self._general_comparison())
    
    def _compare_ednect_desalite(self) -> str:
        return """**Ednect vs Desalite Connect - Both School ERPs:**

**EDNECT:**
- 10+ years experience, 500+ clients
- Proven stability & reliability
- Mature product with extensive track record

**DESALITE CONNECT:**
- 5+ years, modern interface
- Better UX/UI design
- Extra features: Library, Online Assessment, Digital Evaluation

**Common Features:** Student/Staff Management, Fees, Attendance, Timetable, Exams, Reports, Parent Portal

**Choose Ednect:** Want proven 10-year track record
**Choose Desalite:** Want modern interface & extra features

📞 Demo: +91 7099020876"""

    def _compare_ednect_transtrack(self) -> str:
        return """**Ednect vs TransTrack - Different Industries:**

**EDNECT (Education):**
- School/College management
- Students, Staff, Fees, Academics
- For: Educational institutions

**TRANSTRACK (Logistics):**
- Transport & fleet management
- Route optimization, Shipment tracking
- For: Logistics companies, transporters

**Can't compare directly** - serve different industries.

**Need both?** Schools with bus fleet or diversified business can use both.

📞 Ednect: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_desalite_transtrack(self) -> str:
        return """**Desalite Connect vs TransTrack - Different Industries:**

**DESALITE CONNECT (Education):**
- Modern school management ERP
- Student/Staff, Fees, Library, Online Assessment
- For: Schools, Colleges

**TRANSTRACK (Logistics):**
- Transport management system
- Route optimization, Real-time tracking, Cost savings
- For: Logistics companies, fleet operators

**Different purposes.** Use Desalite for school + TransTrack for school buses/transport division.

📞 Desalite: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_ednect_icebox(self) -> str:
        return """**Ednect vs IceBox - Different Industries:**

**EDNECT (Education):**
- School/College ERP - 10+ years
- Students, Staff, Fees, Academics, Exams
- For: Educational institutions

**ICEBOX (Cold Storage):**
- Warehouse management system
- Inventory, Temperature control, Automated workflow
- For: Cold storage facilities, warehouses

**Different industries.** Agricultural schools, culinary institutes, or research institutions might need both.

📞 Ednect: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_desalite_icebox(self) -> str:
        return """**Desalite Connect vs IceBox - Different Industries:**

**DESALITE CONNECT (Education):**
- Modern school ERP - 5+ years
- Student/Staff, Fees, Library, Digital Evaluation
- For: Schools, Colleges

**ICEBOX (Cold Storage):**
- Cold storage management
- Temperature control, Inventory, Security, Billing
- For: Warehouses, cold chain operations

**Different purposes.** Culinary/agricultural schools with storage needs could use both.

📞 Desalite: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_transtrack_icebox(self) -> str:
        return """**TransTrack vs IceBox - Both Logistics, Different Focus:**

**TRANSTRACK (Transportation):**
- Goods in MOTION
- Route optimization, Shipment tracking, Carrier management
- For: Transport companies, fleet managers

**ICEBOX (Warehousing):**
- Goods in STORAGE
- Temperature control, Inventory, Security
- For: Cold storage, warehouses

**Work together:** Cold chain companies need BOTH - TransTrack for delivery + IceBox for storage.

📞 Contact: +91 8811047292"""

    def _compare_three_school_transport(self) -> str:
        return """**Ednect | Desalite | TransTrack:**

**School ERPs (Choose one):**
- **Ednect:** 10+ years, proven (500+ clients)
- **Desalite:** Modern UI, Library, Digital Evaluation
Both have: Student/Staff, Fees, Attendance, Exams

**TransTrack (Add if needed):**
- Transport/logistics management
- For: School buses OR separate transport business

**Common scenario:** School ERP + TransTrack for bus fleet management

📞 School ERPs: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_three_all_except_desalite(self) -> str:
        return """**Ednect | TransTrack | IceBox - 3 Industries:**

**EDNECT (Education):** School management - 10+ years
**TRANSTRACK (Logistics):** Transport & fleet management
**ICEBOX (Warehousing):** Cold storage management

**Use cases:**
- Education only → Ednect
- School + buses → Ednect + TransTrack
- School + cold storage → Ednect + IceBox (agricultural/culinary schools)
- All three → Diversified business group

📞 Ednect: +91 7099020876 | TransTrack/IceBox: +91 8811047292"""

    def _compare_three_school_icebox(self) -> str:
        return """**Ednect | Desalite | IceBox:**

**School ERPs (Choose one):**
- **Ednect:** 10+ years, proven track record
- **Desalite:** Modern interface, Library, Digital Evaluation

**ICEBOX (Cold Storage):**
- Warehouse management, Temperature control
- For: Cold storage facilities

**Use together:** Agricultural/culinary/research institutions needing both academics + storage.

📞 School ERPs: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_three_desalite_transport_icebox(self) -> str:
        return """**Desalite | TransTrack | IceBox - 3 Industries:**

**DESALITE (Education):** Modern school ERP
**TRANSTRACK (Logistics):** Transport management
**ICEBOX (Warehousing):** Cold storage management

**Common combinations:**
- School + buses → Desalite + TransTrack
- School + storage → Desalite + IceBox (culinary/agricultural schools)
- Cold chain → TransTrack + IceBox (storage + delivery)
- All three → Diversified business group

📞 Desalite: +91 7099020876 | TransTrack/IceBox: +91 8811047292"""

    def _compare_all_products(self) -> str:
        return """**Complete Product Suite:**

**EDUCATION (Choose one):**
- **Ednect:** 10+ years, 500+ clients, proven
- **Desalite:** Modern UI, Library, Digital Evaluation

**LOGISTICS:**
- **TransTrack:** Transport/fleet management, route optimization

**WAREHOUSING:**
- **IceBox:** Cold storage, temperature control, inventory

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
        return """**Our Product Suite:**

**EDUCATION:**
- **Ednect:** School ERP (10+ years, 500+ clients)
- **Desalite:** School ERP (Modern, 5+ years)

**LOGISTICS:**
- **TransTrack:** Transport management

**WAREHOUSING:**
- **IceBox:** Cold storage management

**Which to compare?** Examples:
- "Ednect vs Desalite" - School ERPs
- "TransTrack vs IceBox" - Logistics
- "All products" - Complete overview

📞 +91 7099020876 (School ERPs) | +91 8811047292 (TransTrack/IceBox)"""


class ActionIntelligentResponse(Action):
    """Handle ALL queries with context awareness and memory"""
    
    def name(self) -> Text:
        return "action_intelligent_response"
    
    def _get_conversation_history(self, tracker: Tracker, limit: int = 10) -> List[Dict]:
        """Get last N conversation turns"""
        events = tracker.events
        history = []
        
        for event in reversed(events):
            if event.get('event') == 'user':
                history.append({
                    'type': 'user',
                    'text': event.get('text', '').lower()
                })
            elif event.get('event') == 'bot':
                history.append({
                    'type': 'bot',
                    'text': event.get('text', '').lower()
                })
            
            if len(history) >= limit * 2:
                break
        
        return list(reversed(history))
    
    def _extract_product_from_history(self, history: List[Dict]) -> str:
        """Extract the most recently discussed product from conversation history"""
        for msg in reversed(history):
            text = msg.get('text', '').lower()
            
            # Normalize variations
            text = text.replace('desallite', 'desalite')
            text = text.replace('des alite', 'desalite')
            
            if 'desalite' in text or 'desalite connect' in text:
                return 'desalite'
            elif 'ednect' in text:
                return 'ednect'
            elif 'transtrack' in text or 'trans track' in text:
                return 'transtrack'
            elif 'icebox' in text or 'ice box' in text:
                return 'icebox'
        
        return None
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        intent = tracker.latest_message.get('intent', {}).get('name', '')
        
        # Normalize variations
        user_message = user_message.replace('desallite', 'desalite')
        user_message = user_message.replace('des alite', 'desalite')
        user_message = user_message.replace('trans track', 'transtrack')
        user_message = user_message.replace('ice box', 'icebox')
        
        # Get conversation history
        history = self._get_conversation_history(tracker, limit=10)
        
        # Get last mentioned product from slot
        last_product = tracker.get_slot("last_mentioned_product")
        
        # Check if this is a comparison request
        is_comparison_query = any(word in user_message for word in [
            'compare', 'comparison', 'vs', 'versus', 'difference', 
            'which is better', 'which one'
        ]) or intent == 'compare_any_products'
        
        # Detect products in current message
        products_mentioned = []
        if 'ednect' in user_message:
            products_mentioned.append('ednect')
        if 'desalite' in user_message or 'desalite connect' in user_message:
            products_mentioned.append('desalite')
        if 'transtrack' in user_message:
            products_mentioned.append('transtrack')
        if 'icebox' in user_message:
            products_mentioned.append('icebox')
        
        # Handle contextual comparison like "compare it to icebox"
        if is_comparison_query:
            # Check for pronouns indicating context reference
            has_pronoun = any(word in user_message for word in ['it', 'this', 'that'])
            
            if has_pronoun and last_product:
                # Add last product to comparison if not already there
                if last_product not in products_mentioned and len(products_mentioned) > 0:
                    products_mentioned.insert(0, last_product)
                elif len(products_mentioned) == 0:
                    products_mentioned.append(last_product)
            
            # If we have products to compare, do comparison
            if len(products_mentioned) >= 2:
                products_sorted = sorted(products_mentioned)
                comparison_key = '-'.join(products_sorted)
                
                comparisons = {
                    'desalite-ednect': self._compare_ednect_desalite(),
                    'ednect-transtrack': self._compare_ednect_transtrack(),
                    'desalite-transtrack': self._compare_desalite_transtrack(),
                    'ednect-icebox': self._compare_ednect_icebox(),
                    'desalite-icebox': self._compare_desalite_icebox(),
                    'icebox-transtrack': self._compare_transtrack_icebox(),
                }
                
                response = comparisons.get(comparison_key, self._general_comparison())
                dispatcher.utter_message(text=response)
                
                # Update last mentioned to the newly mentioned product (not the contextual one)
                if len(products_mentioned) > 1:
                    # The last one in the original list is the newly mentioned
                    return [SlotSet("last_mentioned_product", products_mentioned[-1])]
                return [SlotSet("last_mentioned_product", products_mentioned[0])]
        
        # Check for pronouns/references that need context (non-comparison)
        context_needed = any(word in user_message for word in [
            'it', 'its', 'this', 'that', 'the product', 'the system',
            'the software', 'the erp', 'them', 'those', 'these'
        ])
        
        # If no product mentioned but context needed, use history or slot
        if not products_mentioned and context_needed:
            referenced_product = self._extract_product_from_history(history)
            if referenced_product:
                products_mentioned.append(referenced_product)
            elif last_product:
                products_mentioned.append(last_product)
        
        # If still no product, use last mentioned from slot for certain queries
        if not products_mentioned and last_product:
            if any(keyword in user_message for keyword in [
                'feature', 'price', 'pricing', 'cost', 'client', 'customer',
                'implementation', 'workflow', 'benefit', 'service'
            ]) or context_needed:
                products_mentioned.append(last_product)
        
        # Determine query type
        is_feature_query = any(word in user_message for word in [
            'feature', 'features', 'module', 'modules', 'what can', 
            'what does', 'capabilities', 'functionality'
        ]) or intent in ['ask_ednect_features', 'ask_desalite_features', 
                          'ask_transtrack_features', 'ask_icebox_features']
        
        is_pricing_query = any(word in user_message for word in [
            'price', 'pricing', 'cost', 'how much', 'budget', 'afford'
        ]) or intent in ['ask_ednect_pricing', 'ask_pricing_general']
        
        is_client_query = any(word in user_message for word in [
            'client', 'clients', 'customer', 'customers', 'who use', 
            'which school', 'which company', 'who uses'
        ]) or intent in ['ask_ednect_clients', 'ask_desalite_clients']
        
        is_implementation_query = any(word in user_message for word in [
            'implementation', 'implement', 'setup', 'install', 'deploy'
        ]) or intent == 'ask_ednect_implementation'
        
        is_workflow_query = 'workflow' in user_message or intent == 'ask_icebox_workflow'
        
        is_benefit_query = any(word in user_message for word in [
            'benefit', 'benefits', 'advantage', 'advantages', 'why choose'
        ]) or intent in ['ask_transtrack_benefits', 'ask_icebox_benefits']
        
        is_service_query = 'service' in user_message or intent == 'ask_transtrack_services'
        
        is_about_query = any(word in user_message for word in [
            'about', 'tell me', 'what is', 'information', 'in depth', 
            'detail', 'details', 'describe'
        ]) or intent in ['ask_about_ednect', 'ask_about_desalite', 
                          'ask_about_transtrack', 'ask_about_icebox']
        
        # Handle contextual queries
        if products_mentioned:
            product = products_mentioned[0]
            
            # Route to appropriate response
            if is_feature_query:
                response = self._get_product_features(product)
            elif is_pricing_query:
                response = self._get_product_pricing(product)
            elif is_client_query:
                response = self._get_product_clients(product)
            elif is_implementation_query:
                response = self._get_product_implementation(product)
            elif is_workflow_query:
                response = self._get_product_workflow(product)
            elif is_benefit_query:
                response = self._get_product_benefits(product)
            elif is_service_query:
                response = self._get_product_services(product)
            elif is_about_query:
                response = self._get_product_about(product)
            else:
                # General product info
                product_name = product.upper() if product != 'desalite' else 'DESALITE CONNECT'
                response = f"""**About {product_name}** - I can help with:

- Features & modules
- Pricing information
- Client list
- Implementation details
- Demo requests

What would you like to know?

📞 +91 7099020876 / +91 8811047292"""
            
            dispatcher.utter_message(text=response)
            return [SlotSet("last_mentioned_product", product)]
        
        # If multiple products but not comparison, handle differently
        if len(products_mentioned) > 1:
            return self._handle_multiple_products(dispatcher, products_mentioned, user_message)
        
        # Default fallback
        return []
    
    def _compare_ednect_desalite(self) -> str:
        return """**Ednect vs Desalite Connect - Both School ERPs:**

**EDNECT:**
- 10+ years experience, 500+ clients
- Proven stability & reliability
- Mature product with extensive track record

**DESALITE CONNECT:**
- 5+ years, modern interface
- Better UX/UI design
- Extra features: Library, Online Assessment, Digital Evaluation

**Common Features:** Student/Staff Management, Fees, Attendance, Timetable, Exams, Reports, Parent Portal

**Choose Ednect:** Want proven 10-year track record
**Choose Desalite:** Want modern interface & extra features

📞 Demo: +91 7099020876"""

    def _compare_ednect_transtrack(self) -> str:
        return """**Ednect vs TransTrack - Different Industries:**

**EDNECT (Education):**
- School/College management
- Students, Staff, Fees, Academics
- For: Educational institutions

**TRANSTRACK (Logistics):**
- Transport & fleet management
- Route optimization, Shipment tracking
- For: Logistics companies, transporters

**Can't compare directly** - serve different industries.

📞 Ednect: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_desalite_transtrack(self) -> str:
        return """**Desalite Connect vs TransTrack - Different Industries:**

**DESALITE CONNECT (Education):**
- Modern school management ERP
- Student/Staff, Fees, Library, Online Assessment
- For: Schools, Colleges

**TRANSTRACK (Logistics):**
- Transport management system
- Route optimization, Real-time tracking, Cost savings
- For: Logistics companies, fleet operators

**Different purposes.**

📞 Desalite: +91 7099020876 | TransTrack: +91 8811047292"""

    def _compare_ednect_icebox(self) -> str:
        return """**Ednect vs IceBox - Different Industries:**

**EDNECT (Education):**
- School/College ERP - 10+ years
- Students, Staff, Fees, Academics, Exams
- For: Educational institutions

**ICEBOX (Cold Storage):**
- Warehouse management system
- Inventory, Temperature control, Automated workflow
- For: Cold storage facilities, warehouses

**Different industries.**

📞 Ednect: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_desalite_icebox(self) -> str:
        return """**Desalite Connect vs IceBox - Different Industries:**

**DESALITE CONNECT (Education):**
- Modern school ERP - 5+ years
- Student/Staff, Fees, Library, Digital Evaluation
- For: Schools, Colleges

**ICEBOX (Cold Storage):**
- Cold storage management
- Temperature control, Inventory, Security, Billing
- For: Warehouses, cold chain operations

**Different purposes.**

📞 Desalite: +91 7099020876 | IceBox: +91 8811047292"""

    def _compare_transtrack_icebox(self) -> str:
        return """**TransTrack vs IceBox - Both Logistics, Different Focus:**

**TRANSTRACK (Transportation):**
- Goods in MOTION
- Route optimization, Shipment tracking, Carrier management
- For: Transport companies, fleet managers

**ICEBOX (Warehousing):**
- Goods in STORAGE
- Temperature control, Inventory, Security
- For: Cold storage, warehouses

**Work together:** Cold chain companies need BOTH.

📞 Contact: +91 8811047292"""

    def _general_comparison(self) -> str:
        return """**Our Product Suite:**

**EDUCATION:**
- **Ednect:** School ERP (10+ years, 500+ clients)
- **Desalite:** School ERP (Modern, 5+ years)

**LOGISTICS:**
- **TransTrack:** Transport management

**WAREHOUSING:**
- **IceBox:** Cold storage management

📞 +91 7099020876 (School ERPs) | +91 8811047292 (TransTrack/IceBox)"""
    
    def _get_product_about(self, product: str) -> str:
        """Get general information about product"""
        about = {
            'ednect': """**Ednect - School Management ERP**

- 10+ years of experience
- 500+ satisfied clients
- 1000+ developments completed
- Modern Cloud ERP for educational institutions
- Complete school management solution

**Key Highlights:**
✓ Proven track record
✓ Cost-effective
✓ User-friendly
✓ Comprehensive features
✓ Reliable support

📞 Demo: +91 7099020876""",
            
            'desalite': """**Desalite Connect - Modern School ERP**

- 5+ years of experience
- Modern, intuitive interface
- Complete educational management solution
- Extra features: Library, Online Assessment, Digital Evaluation

**Key Highlights:**
✓ Modern UX/UI design
✓ User-friendly
✓ Comprehensive modules
✓ Advanced features
✓ Trusted by prestigious institutions

📞 Demo: +91 7099020876""",
            
            'transtrack': """**TransTrack - Transport Management System**

- Premier TMS solution
- Revolutionizing transportation & logistics
- Cost-effective and efficient
- Global reach with local expertise

**Key Highlights:**
✓ Route optimization
✓ Real-time tracking
✓ Cost savings
✓ Improved efficiency
✓ Comprehensive analytics

📞 Demo: +91 8811047292""",
            
            'icebox': """**IceBox - Cold Storage Management System**

- Cutting-edge warehouse management
- Temperature-controlled storage optimization
- Advanced analytics and security
- Complete automation

**Key Highlights:**
✓ Temperature precision
✓ Real-time monitoring
✓ Automated workflow
✓ Digital records
✓ Enhanced security

📞 Demo: +91 8811047292"""
        }
        
        return about.get(product, "Product information not available.")
    
    def _get_product_features(self, product: str) -> str:
        """Get features for specific product"""
        features = {
            'ednect': """**Ednect Features:**

- **Staff Management** - Cloud-based staff data
- **HR Management** - Salary, performance, attendance
- **Student Management** - Admissions, circulars, SMS, lesson plans
- **Fee Management** - Dashboard, online payment gateway
- **Report Management** - Organized decision-making reports
- **Attendance Management** - Track student attendance & leaves
- **Timetable Management** - Efficient scheduling
- **Exam & Result Management** - Streamlined examination process

📞 Demo: +91 7099020876""",
            
            'desalite': """**Desalite Connect Features:**

- **Staff Management** - Cloud-based organization
- **HR Management** - Complete employee database
- **Student Management** - Admission counseling, communication
- **Fee Management** - Integrated payment gateway
- **Report Management** - Timely, organized information
- **Attendance Management** - Comprehensive tracking
- **Timetable Management** - User-friendly scheduling
- **Exam & Result Management** - Simplified process
- **Library Management** - Digital library system
- **Online Assessment** - Digital evaluation tools
- **Digital Evaluation** - Paperless grading

📞 Demo: +91 7099020876""",
            
            'transtrack': """**TransTrack Features:**

- **Transportation Planning & Optimization** - Data-driven insights
- **Carrier Selection & Management** - Trusted carrier network
- **Real-Time Tracking & Visibility** - Complete monitoring
- **Route Optimization** - Minimize transit time & fuel costs
- **Load Consolidation** - Reduce shipping costs
- **Supply Chain Analytics** - Data-driven decisions
- **Compliance & Regulatory Support** - Stay compliant

📞 Demo: +91 8811047292""",
            
            'icebox': """**IceBox Features:**

- **Inventory Management** - Batch, brand, expiry, rack-wise tracking
- **Temperature Control** - Precision control with real-time alerts
- **Security Features** - Comprehensive monitoring
- **Organized Reports** - Item-wise, storage-wise, vehicle reports
- **Detailed Billing** - Labour, order, rental bills
- **Digital Records** - Efficient data management
- **Real-Time Data Access** - Instant information
- **Multi-Storage Support** - Multiple facility management

📞 Demo: +91 8811047292"""
        }
        
        return features.get(product, "Product features not available.")
    
    def _get_product_pricing(self, product: str) -> str:
        """Get pricing info for specific product"""
        pricing = {
            'ednect': """**Ednect Pricing:**

- Cost-effective & budget-friendly
- Customized to your requirements
- Transparent - no hidden costs

For detailed pricing:
📞 +91 7099020876
📧 ajit@vasptechnologies.com

We offer a **FREE DEMO** to discuss your needs!""",
            
            'desalite': """**Desalite Connect Pricing:**

- Budget-friendly solution
- Customizable packages
- Transparent pricing

For detailed pricing:
📞 +91 7099020876
📧 ajit@vasptechnologies.com

Schedule a **FREE DEMO** to get accurate pricing!""",
            
            'transtrack': """**TransTrack Pricing:**

- Cost-effective TMS solution
- Customized to your business needs
- Transparent pricing structure

For detailed pricing:
📞 +91 8811047292
📧 ajit@vasptechnologies.com

Request a **FREE DEMO** today!""",
            
            'icebox': """**IceBox Pricing:**

- Affordable cold storage management
- Customizable to your facility
- No hidden costs

For detailed pricing:
📞 +91 8811047292
📧 ajit@vasptechnologies.com

Schedule a **FREE DEMO** now!"""
        }
        
        return pricing.get(product, "Pricing information not available.")
    
    def _get_product_clients(self, product: str) -> str:
        """Get client list for specific product"""
        clients = {
            'ednect': """**Ednect Clients:**

- Heritage Public School
- Reality Public School
- Seppa Public School

**Track Record:**
- 10+ years experience
- 500+ clients served
- 1000+ developments completed

📞 More info: +91 7099020876""",
            
            'desalite': """**Desalite Connect Clients:**

- Saint Francis De Sales Schools (Narengi, Dhemaji, Bahalpur, Pasighat, Medziphema)
- Saint Francis De Sales College, Aalo
- Queenie Secondary School, Shillong
- Green Mount School, Itanagar
- Shalom Public School, Guwahati
- NPS International School, Guwahati
- All Saints Hr. Sec. School, Peren
- St. Xavier's High School, Mushalpur
- Nand English High School, Narengi

📞 More info: +91 7099020876""",
            
            'transtrack': """**TransTrack Clients:**

We serve various logistics and transportation companies with proven results in:
- Cost reduction
- Route optimization
- Improved delivery times
- Enhanced customer satisfaction

📞 Client references: +91 8811047292""",
            
            'icebox': """**IceBox Clients:**

We serve cold storage facilities and warehouse operators with:
- Improved efficiency
- Better temperature control
- Increased profitability
- Enhanced security

📞 Client references: +91 8811047292"""
        }
        
        return clients.get(product, "Client information not available.")
    
    def _get_product_implementation(self, product: str) -> str:
        """Get implementation details"""
        implementation = {
            'ednect': """**Ednect Implementation:**

**Process:**
1. Initial consultation & requirement analysis
2. System customization to your needs
3. Setup and configuration
4. Comprehensive staff training
5. Smooth transition and go-live
6. Ongoing support

**Timeline:** Varies based on institution size
**Support:** Online and in-person assistance
**Training:** Hands-on instruction for all staff

📞 Contact: +91 7099020876""",
            
            'desalite': """**Desalite Connect Implementation:**

**Process:**
1. Requirement analysis
2. Customization based on your needs
3. Installation and setup
4. User training sessions
5. Testing and deployment
6. Post-implementation support

**Features:**
✓ Smooth transition
✓ Comprehensive training
✓ Dedicated support team
✓ Customizable workflow

📞 Contact: +91 7099020876""",
            
            'transtrack': """**TransTrack Implementation:**

**Process:**
1. Business requirement analysis
2. System configuration
3. Carrier network integration
4. User training
5. Testing and validation
6. Go-live and support

**Timeline:** Based on business complexity
**Support:** Dedicated implementation team

📞 Contact: +91 8811047292""",
            
            'icebox': """**IceBox Implementation:**

**Process:**
1. Facility assessment
2. System customization
3. Hardware integration (if needed)
4. Software setup and configuration
5. Staff training
6. Testing and deployment
7. Ongoing support

**Features:**
✓ Automated workflow setup
✓ Complete staff training
✓ Real-time monitoring activation

📞 Contact: +91 8811047292"""
        }
        
        return implementation.get(product, "Implementation information not available.")
    
    def _get_product_workflow(self, product: str) -> str:
        """Get workflow details (mainly for IceBox)"""
        if product == 'icebox':
            return """**IceBox Workflow Process:**

1. **Vehicle Arrival** → Gate Entry → Service Allocation
2. **Reference ID Generation**
3. **Weigh Bridge:** Weight Capture → Entry → Payment → Document Generation
4. **Chamber Process:** Goods In/Out/Shifting → Labour Allocation → Authorization → Document Generation
5. **Post Chamber:** Weight Recording for Discrepancy Tracking
6. **Exit:** Pass Generation → Vehicle Departure after Approval

**Key Features:**
✓ Fully automated
✓ No manual interference
✓ Real-time tracking
✓ Complete documentation

📞 Demo: +91 8811047292"""
        else:
            return f"Workflow information is specific to IceBox. For {product.upper()}, please ask about features or implementation process."
    
    def _get_product_benefits(self, product: str) -> str:
        """Get benefits of product"""
        benefits = {
            'ednect': """**Why Choose Ednect?**

✓ **10+ Years Experience** - Proven track record
✓ **500+ Clients** - Trusted by institutions
✓ **Cost-Effective** - Budget-friendly solution
✓ **Comprehensive Features** - All-in-one ERP
✓ **Reliable Support** - Dedicated team
✓ **User-Friendly** - Easy to use
✓ **Customizable** - Tailored to your needs
✓ **Cloud-Based** - Access anywhere

📞 Demo: +91 7099020876""",
            
            'desalite': """**Why Choose Desalite Connect?**

✓ **Modern Interface** - Intuitive UX/UI
✓ **Extra Features** - Library, Online Assessment, Digital Evaluation
✓ **5+ Years Experience** - Trusted solution
✓ **Prestigious Clients** - Used by top institutions
✓ **User-Friendly** - Easy adoption
✓ **Comprehensive** - Complete school management
✓ **Efficient** - Streamlined processes
✓ **Cost-Effective** - Value for money

📞 Demo: +91 7099020876""",
            
            'transtrack': """**Why Choose TransTrack?**

✓ **Experience** - Years of industry expertise
✓ **Reliability** - Meet deadlines consistently
✓ **Cost Savings** - Optimize transportation costs
✓ **Customer-Centric** - Personalized solutions
✓ **Improved Service** - Better customer satisfaction
✓ **Increased Profitability** - ROI-focused
✓ **Reduced Risk** - Compliance support
✓ **Better Analytics** - Data-driven decisions

📞 Demo: +91 8811047292""",
            
            'icebox': """**Why Choose IceBox?**

✓ **Digital Records** - Paperless efficiency
✓ **Simplified Tracking** - Easy goods management
✓ **Real-Time Access** - Instant data availability
✓ **Multi-Storage Support** - Multiple facilities
✓ **Improved Efficiency** - Automated workflow
✓ **Increased Profitability** - Better space utilization
✓ **Customer Retention** - Better service
✓ **Temperature Precision** - Real-time alerts

📞 Demo: +91 8811047292"""
        }
        
        return benefits.get(product, "Benefits information not available.")
    
    def _get_product_services(self, product: str) -> str:
        """Get services offered (mainly for TransTrack)"""
        if product == 'transtrack':
            return """**TransTrack Services:**

- **Strategic Transportation Planning** - Data-driven route planning
- **Carrier Management** - Vetting and network management
- **Real-Time Tracking** - Advanced GPS technology
- **Route Optimization** - Traffic, weather, capacity analysis
- **Load Consolidation** - Cost reduction expertise
- **Supply Chain Analytics** - Comprehensive reporting
- **Compliance Support** - Full regulatory assistance

**Contact:**
📞 +91 8811047292
📧 ajit@vasptechnologies.com"""
        else:
            return f"Services information is specific to TransTrack. For {product.upper()}, please ask about features or benefits."
    
    def _handle_multiple_products(self, dispatcher, products, user_message):
        """Handle queries about multiple products"""
        if 'ednect' in products and 'desalite' in products:
            response = """**Both are School ERPs:**

- **Ednect:** 10+ years, 500+ clients (proven)
- **Desalite:** 5+ years, modern UX (extra features)

Both have same core features. Main difference: Experience vs Modern UI.

📞 Detailed comparison: +91 7099020876"""
            
        else:
            response = f"""**You mentioned: {', '.join([p.upper() for p in products])}**

- **Ednect/Desalite:** Education
- **TransTrack:** Logistics
- **IceBox:** Cold Storage

Different industries. Which comparison do you need?

📞 +91 7099020876 or +91 8811047292"""
        
        dispatcher.utter_message(text=response)
        return [SlotSet("last_mentioned_product", products[0])]


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
        elif 'desalite' in user_message or 'desallite' in user_message:
            current_product = 'desalite'
        elif 'transtrack' in user_message:
            current_product = 'transtrack'
        elif 'icebox' in user_message:
            current_product = 'icebox'
        
        slots_to_set = []
        if current_product:
            slots_to_set.append(SlotSet("last_mentioned_product", current_product))
        
        return slots_to_set


class ActionFallbackWithContext(Action):
    """Intelligent fallback that considers conversation context"""
    
    def name(self) -> Text:
        return "action_fallback_with_context"
    
    def _get_recent_context(self, tracker: Tracker) -> str:
        """Extract recently discussed product from conversation"""
        events = tracker.events
        
        for event in reversed(events[-20:]):
            if event.get('event') == 'user':
                text = event.get('text', '').lower()
                
                text = text.replace('desallite', 'desalite')
                
                if 'desalite' in text:
                    return 'desalite'
                elif 'ednect' in text:
                    return 'ednect'
                elif 'transtrack' in text:
                    return 'transtrack'
                elif 'icebox' in text:
                    return 'icebox'
        
        return None
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from rasa_sdk.events import SlotSet
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        user_message = user_message.replace('desallite', 'desalite')
        
        # Get last mentioned product
        last_product = tracker.get_slot("last_mentioned_product")
        
        # Check for context-dependent queries
        context_words = ['it', 'its', 'this', 'that', 'the product', 'the system', 'the software']
        needs_context = any(word in user_message for word in context_words)
        
        if needs_context or not last_product:
            if not last_product:
                last_product = self._get_recent_context(tracker)
        
        # Handle contextual queries
        if last_product and needs_context:
            try:
                if any(word in user_message for word in ['feature', 'features', 'module', 'modules', 'what can', 'capabilities']):
                    response = self._get_contextual_features(last_product)
                    dispatcher.utter_message(text=response)
                    return [SlotSet("last_mentioned_product", last_product)]
                
                elif any(word in user_message for word in ['price', 'pricing', 'cost', 'how much']):
                    response = self._get_contextual_pricing(last_product)
                    dispatcher.utter_message(text=response)
                    return [SlotSet("last_mentioned_product", last_product)]
                
                elif any(word in user_message for word in ['client', 'clients', 'customer', 'who use']):
                    response = self._get_contextual_clients(last_product)
                    dispatcher.utter_message(text=response)
                    return [SlotSet("last_mentioned_product", last_product)]
                
                else:
                    product_name = last_product.upper() if last_product != 'desalite' else 'DESALITE CONNECT'
                    response = f"""**About {product_name}** - I can help with:

- Features & modules
- Pricing information
- Client list
- Implementation details
- Demo requests

What would you like to know?

📞 +91 7099020876 / +91 8811047292"""
                    dispatcher.utter_message(text=response)
                    return [SlotSet("last_mentioned_product", last_product)]
            except Exception as e:
                # Safe fallback
                response = """I can help you with:

- Product features
- Pricing information
- Client references
- Demo requests

📞 +91 7099020876 / +91 8811047292"""
                dispatcher.utter_message(text=response)
                return []
        
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

- Features & pricing
- Implementation
- Client list
- Comparisons
- Demo requests

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
    
    def _get_contextual_features(self, product: str) -> str:
        """Get features based on context"""
        features = {
            'ednect': """**Ednect Features:**

- **Staff Management** - Cloud-based staff data
- **HR Management** - Salary, performance, attendance
- **Student Management** - Admissions, circulars, SMS, lesson plans
- **Fee Management** - Dashboard, online payment gateway
- **Report Management** - Organized decision-making reports
- **Attendance Management** - Track student attendance & leaves
- **Timetable Management** - Efficient scheduling
- **Exam & Result Management** - Streamlined examination process

📞 Demo: +91 7099020876""",
            
            'desalite': """**Desalite Connect Features:**

- **Staff Management** - Cloud-based organization
- **HR Management** - Complete employee database
- **Student Management** - Admission counseling, communication
- **Fee Management** - Integrated payment gateway
- **Report Management** - Timely, organized information
- **Attendance Management** - Comprehensive tracking
- **Timetable Management** - User-friendly scheduling
- **Exam & Result Management** - Simplified process
- **Library Management** - Digital library system
- **Online Assessment** - Digital evaluation tools
- **Digital Evaluation** - Paperless grading

📞 Demo: +91 7099020876""",
            
            'transtrack': """**TransTrack Features:**

- **Transportation Planning & Optimization** - Data-driven insights
- **Carrier Selection & Management** - Trusted carrier network
- **Real-Time Tracking & Visibility** - Complete monitoring
- **Route Optimization** - Minimize transit time & fuel costs
- **Load Consolidation** - Reduce shipping costs
- **Supply Chain Analytics** - Data-driven decisions
- **Compliance & Regulatory Support** - Stay compliant

📞 Demo: +91 8811047292""",
            
            'icebox': """**IceBox Features:**

- **Inventory Management** - Batch, brand, expiry, rack-wise tracking
- **Temperature Control** - Precision control with real-time alerts
- **Security Features** - Comprehensive monitoring
- **Organized Reports** - Item-wise, storage-wise, vehicle reports
- **Detailed Billing** - Labour, order, rental bills
- **Digital Records** - Efficient data management
- **Real-Time Data Access** - Instant information
- **Multi-Storage Support** - Multiple facility management

📞 Demo: +91 8811047292"""
        }
        
        return features.get(product, "Product information not found.")
    
    def _get_contextual_pricing(self, product: str) -> str:
        """Get pricing based on context"""
        pricing = {
            'ednect': """**Ednect Pricing:**

- Cost-effective & budget-friendly
- Customized to your requirements
- Transparent - no hidden costs

For detailed pricing:
📞 +91 7099020876
📧 ajit@vasptechnologies.com

We offer a **FREE DEMO** to discuss your needs!""",
            
            'desalite': """**Desalite Connect Pricing:**

- Budget-friendly solution
- Customizable packages
- Transparent pricing

For detailed pricing:
📞 +91 7099020876
📧 ajit@vasptechnologies.com

Schedule a **FREE DEMO** to get accurate pricing!""",
            
            'transtrack': """**TransTrack Pricing:**

- Cost-effective TMS solution
- Customized to your business needs
- Transparent pricing structure

For detailed pricing:
📞 +91 8811047292
📧 ajit@vasptechnologies.com

Request a **FREE DEMO** today!""",
            
            'icebox': """**IceBox Pricing:**

- Affordable cold storage management
- Customizable to your facility
- No hidden costs

For detailed pricing:
📞 +91 8811047292
📧 ajit@vasptechnologies.com

Schedule a **FREE DEMO** now!"""
        }
        
        return pricing.get(product, "Pricing information not available.")
    
    def _get_contextual_clients(self, product: str) -> str:
        """Get clients based on context"""
        clients = {
            'ednect': """**Ednect Clients:**

- Heritage Public School
- Reality Public School
- Seppa Public School

**Track Record:**
- 10+ years experience
- 500+ clients served
- 1000+ developments completed

📞 More info: +91 7099020876""",
            
            'desalite': """**Desalite Connect Clients:**

- Saint Francis De Sales Schools (Narengi, Dhemaji, Bahalpur, Pasighat, Medziphema)
- Saint Francis De Sales College, Aalo
- Queenie Secondary School, Shillong
- Green Mount School, Itanagar
- Shalom Public School, Guwahati
- NPS International School, Guwahati
- All Saints Hr. Sec. School, Peren
- St. Xavier's High School, Mushalpur
- Nand English High School, Narengi

📞 More info: +91 7099020876""",
            
            'transtrack': """**TransTrack Clients:**

We serve various logistics and transportation companies with proven results in:
- Cost reduction
- Route optimization
- Improved delivery times
- Enhanced customer satisfaction

📞 Client references: +91 8811047292""",
            
            'icebox': """**IceBox Clients:**

We serve cold storage facilities and warehouse operators with:
- Improved efficiency
- Better temperature control
- Increased profitability
- Enhanced security

📞 Client references: +91 8811047292"""
        }
        
        return clients.get(product, "Client information not available.")


class ActionProvideRecommendation(Action):
    """Provide product recommendations based on user needs"""
    
    def name(self) -> Text:
        return "action_provide_recommendation"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        if any(word in user_message for word in ['school', 'college', 'education', 'student', 'institute']):
            response = """**For Education:**

**EDNECT** → 10+ years, proven (500+ clients)
**DESALITE** → Modern UI, extra features (Library, Digital Evaluation)

Both have: Student/Staff, Fees, Attendance, Exams, Reports

📞 Demo: +91 7099020876"""
        
        elif any(word in user_message for word in ['transport', 'logistics', 'shipping', 'delivery', 'carrier']):
            response = """**For Logistics/Transport:**

**TRANSTRACK** - Transport Management System
- Route optimization
- Real-time tracking
- Cost savings
- Fleet management

📞 Demo: +91 8811047292"""
        
        elif any(word in user_message for word in ['cold storage', 'warehouse', 'storage', 'cold chain', 'temperature']):
            response = """**For Cold Storage/Warehouse:**

**ICEBOX** - Cold Storage Management
- Temperature control
- Inventory tracking
- Automated workflow
- Security monitoring

📞 Demo: +91 8811047292"""
        
        else:
            response = """**What's your industry?**

🎓 **Education** → Ednect or Desalite
🚛 **Logistics** → TransTrack
❄️ **Cold Storage** → IceBox

📞 +91 7099020876 / +91 8811047292"""
        
        dispatcher.utter_message(text=response)
        return []
    