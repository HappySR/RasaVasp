from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

class ActionCompareProducts(Action):
    """Custom action to handle all product comparisons with detailed insights"""
    
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
        """Generate detailed comparisons based on products mentioned"""
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
        """Detailed comparison between Ednect and Desalite Connect"""
        return """**📚 Comparing Ednect vs Desalite Connect:**

Both are comprehensive School Management ERP systems from Vasp Technologies, but with distinct advantages:

**EDNECT - The Veteran:**
✅ **Experience:** 10+ years in the market
✅ **Track Record:** 500+ clients, 1,000+ developments
✅ **Reputation:** Proven stability and reliability
✅ **Client Base:** Heritage Public School, Reality Public School, Seppa Public School
✅ **Strength:** Extensive deployment history, mature product with battle-tested features
✅ **Best For:** Institutions seeking a proven, long-standing solution

**DESALITE CONNECT - The Modern Choice:**
✅ **Experience:** 5+ years of focused development
✅ **Design Focus:** Enhanced user experience and modern interface
✅ **Client Base:** Prestigious educational networks (Saint Francis De Sales Schools across multiple locations, NPS International, Green Mount School)
✅ **Unique Features:** Library Management, Online Assessment, Digital Evaluation
✅ **Strength:** User-friendly design, extensive network of educational institutions
✅ **Best For:** Institutions prioritizing modern UX and educational network integration

**✨ Common Features (Both Offer):**
• Staff & HR Management
• Student Management with Admission Counseling
• Fee Management with Online Payment Gateway
• Attendance Tracking & Leave Management
• Timetable Management
• Report Generation & Management
• Exam Result Management
• Parent & Student Portals
• Cloud-based Access
• SMS & Communication Tools
• Customizable to Institution Needs

**💰 Pricing:** Both offer cost-effective, budgeted solutions

**🎯 Decision Factors:**
• Choose **Ednect** if you value extensive experience and want a mature product with proven track record
• Choose **Desalite Connect** if you prioritize modern UI/UX and want additional features like digital evaluation and library management

**📞 Want to see both in action?**
Schedule demos for both and decide which interface feels right!
Contact: +91 7099020876"""

    def _compare_ednect_transtrack(self) -> str:
        """Comparison between Ednect and TransTrack"""
        return """**🔄 Comparing Ednect vs TransTrack:**

These serve **completely different industries** and cannot be directly compared. Here's what each offers:

**📚 EDNECT - Education Management**
**Industry:** Educational Institutions (Schools, Colleges)
**Purpose:** Complete school administration and management

**Core Functions:**
• Student & Staff Management
• Academic Operations (Timetable, Exams, Results)
• Fee Collection & Financial Management
• Attendance & Leave Tracking
• Parent-Teacher Communication
• Admission Management

**Who Uses It:** Schools, Colleges, Educational Institutions
**Users:** Administrators, Teachers, Students, Parents
**Experience:** 10+ years, 500+ clients

---

**🚛 TRANSTRACK - Transport Management**
**Industry:** Logistics, Transportation, Supply Chain
**Purpose:** Optimize transportation and logistics operations

**Core Functions:**
• Transportation Planning & Route Optimization
• Carrier Selection & Management
• Real-time Shipment Tracking
• Load Consolidation
• Supply Chain Analytics
• Compliance & Regulatory Support
• Cost Optimization

**Who Uses It:** Logistics Companies, Transportation Businesses, Supply Chain Managers
**Users:** Fleet Managers, Dispatchers, Carriers, Logistics Coordinators

---

**🎯 Which Should You Choose?**

**Choose Ednect if:**
✅ You're running an educational institution
✅ You need to manage students, staff, academics
✅ You want to digitalize school operations

**Choose TransTrack if:**
✅ You're in logistics/transportation business
✅ You need to manage fleet and shipments
✅ You want to optimize supply chain operations

**❓ Do you run both a school AND a transport business?**
Great news! You can use BOTH products:
• Ednect for your educational operations
• TransTrack for your transportation/logistics division

**📞 Contact:** +91 7099020876 (Ednect) | +91 8811047292 (TransTrack)

Which industry are you primarily interested in?"""

    def _compare_desalite_transtrack(self) -> str:
        """Comparison between Desalite Connect and TransTrack"""
        return """**🔄 Comparing Desalite Connect vs TransTrack:**

These are **industry-specific solutions** that serve different business needs:

**📚 DESALITE CONNECT - School Management ERP**
**Industry:** Education Sector
**Experience:** 5+ years
**Focus:** Modern, user-friendly school administration

**What It Does:**
• Complete School Administration
• Student & Staff Management
• Fee Collection with Payment Gateway
• Attendance & Academic Tracking
• Library Management System
• Online Assessment & Digital Evaluation
• Parent-Student-Teacher Portals
• Report Card Generation

**Unique Strengths:**
✅ Enhanced user experience and modern interface
✅ Digital evaluation and online assessment tools
✅ Extensive educational network (Saint Francis De Sales Schools, NPS International, Green Mount School)
✅ Library management integration

**Target Users:** Schools, Colleges, Educational Networks
**Best For:** Institutions wanting modern UX with comprehensive features

---

**🚛 TRANSTRACK - Transport Management System**
**Industry:** Logistics & Supply Chain
**Focus:** Transportation optimization and efficiency

**What It Does:**
• Transportation Planning & Optimization
• Real-time Shipment Tracking & Visibility
• Carrier Management & Selection
• Route Optimization (minimize time & fuel costs)
• Load Consolidation
• Supply Chain Analytics & Insights
• Compliance & Regulatory Support
• Cost Reduction Strategies

**Unique Strengths:**
✅ Real-time tracking and visibility
✅ Data-driven route optimization
✅ Cost savings through load consolidation
✅ Comprehensive supply chain analytics

**Target Users:** Logistics Companies, Fleet Managers, Transportation Businesses
**Best For:** Companies wanting to optimize transportation operations and reduce costs

---

**🎯 Making Your Choice:**

**Choose Desalite Connect if:**
✅ You manage an educational institution
✅ You need modern school administration tools
✅ You want user-friendly interface for teachers and staff
✅ You need library and assessment management

**Choose TransTrack if:**
✅ You operate a logistics/transportation business
✅ You manage fleet or shipments
✅ You want to reduce transportation costs
✅ You need real-time tracking capabilities

**💼 Running Both Industries?**
Perfect! These systems can work together:
• Use Desalite Connect for your school operations
• Use TransTrack for school bus/transport logistics or separate transport business

**📞 Schedule Demos:**
Desalite Connect: +91 7099020876
TransTrack: +91 8811047292

Which solution interests you most?"""

    def _compare_ednect_icebox(self) -> str:
        """Comparison between Ednect and IceBox"""
        return """**🔄 Comparing Ednect vs IceBox:**

These products serve **entirely different industries** with no overlap:

**📚 EDNECT - School Management ERP**
**Industry:** Education
**Experience:** 10+ years, 500+ clients
**Purpose:** Complete educational institution management

**What It Manages:**
• Student & Staff Administration
• Academic Operations (Classes, Exams, Results)
• Fee Collection & Financial Management
• Attendance & Leave Systems
• Timetable & Schedule Management
• Parent-Teacher Communication
• Admission & Enrollment Processes

**Technology:** Cloud-based Modern ERP
**Users:** School Administrators, Teachers, Students, Parents
**Deployed At:** Heritage Public School, Reality Public School, Seppa Public School

**Best For:**
✅ Schools and educational institutions
✅ Academic administration
✅ Student lifecycle management

---

**❄️ ICEBOX - Cold Storage Management System**
**Industry:** Warehousing & Cold Chain
**Purpose:** Optimize cold storage and warehouse operations

**What It Manages:**
• Inventory Management (batch, brand, expiry, rack-wise sorting)
• Temperature Control & Monitoring (with real-time alerts)
• Warehouse Workflow Automation
• Vehicle Entry/Exit Management
• Weigh Bridge Operations
• Chamber Management (Goods In/Out/Shifting)
• Labour Allocation & Tracking
• Detailed Billing (Labour, Order, Rental)
• Security & Safety Monitoring

**Technology:** Automated workflow system with zero manual interference
**Users:** Warehouse Managers, Cold Storage Operators, Inventory Controllers
**Unique Feature:** Complete automation from vehicle arrival to departure

**Best For:**
✅ Cold storage facilities
✅ Warehouse operations
✅ Temperature-controlled storage
✅ Perishable goods management

---

**🎯 Decision Guide:**

**Choose Ednect if:**
✅ You're running a school or college
✅ You need to manage students and academics
✅ You want proven educational ERP with 10+ years experience

**Choose IceBox if:**
✅ You operate a cold storage facility
✅ You manage warehouses
✅ You need temperature monitoring and inventory control
✅ You handle perishable goods

**🏢 Do You Need Both?**
Some scenarios where you might:
• Educational institutions with research labs requiring cold storage
• Agricultural schools with produce storage facilities
• Institutions with large-scale food storage operations

Both systems can operate independently for their specific functions.

**📞 Get Started:**
Ednect: +91 7099020876
IceBox: +91 8811047292

Which industry solution do you need?"""

    def _compare_desalite_icebox(self) -> str:
        """Comparison between Desalite Connect and IceBox"""
        return """**🔄 Comparing Desalite Connect vs IceBox:**

These are **specialized solutions for different industries** with distinct purposes:

**📚 DESALITE CONNECT - School Management ERP**
**Industry:** Education
**Experience:** 5+ years with prestigious institutions
**Focus:** Modern, user-friendly school administration

**Core Capabilities:**
• Complete Student Management (Admission to Alumni)
• Staff & HR Management
• Fee Collection with Online Payment Gateway
• Automated Attendance System
• Academic Management (Timetable, Exams, Results)
• Library Management System
• Online Assessment & Digital Evaluation
• Report Card Management
• Parent & Student Portals

**Client Profile:**
Used by educational networks including Saint Francis De Sales Schools (multiple locations), NPS International School, Green Mount School, Shalom Public School

**Strengths:**
✅ Modern, intuitive user interface
✅ Comprehensive digital evaluation tools
✅ Integrated library management
✅ Strong educational network presence

**Best For:** Schools prioritizing user experience and modern features

---

**❄️ ICEBOX - Cold Storage Management System**
**Industry:** Warehousing & Cold Chain Logistics
**Focus:** Temperature-controlled storage optimization

**Core Capabilities:**
• Advanced Inventory Management (batch, brand, expiry, item, rack-wise)
• Precision Temperature Control (with real-time alerts)
• Automated Workflow (Vehicle → Weigh Bridge → Chamber → Exit)
• Security & Safety Monitoring
• Real-time Data Access
• Multi-Storage Support
• Detailed Billing System (Labour, Order, Rental)
• Goods Tracking (In/Out/Shifting)
• Digital Record Keeping

**Workflow Automation:**
Complete automation from vehicle arrival through gate entry, weigh bridge, chamber operations, to final exit - all without manual interference

**Strengths:**
✅ Zero manual intervention workflow
✅ Real-time temperature monitoring
✅ Comprehensive security features
✅ Automated billing and reporting

**Best For:** Cold storage facilities, warehouses, cold chain operations

---

**🎯 Which Solution Do You Need?**

**Choose Desalite Connect if:**
✅ You manage an educational institution
✅ You need modern school administration tools
✅ You want library and online assessment features
✅ You prioritize user-friendly interface

**Choose IceBox if:**
✅ You operate cold storage facilities
✅ You manage temperature-controlled warehouses
✅ You handle perishable goods
✅ You need automated workflow management

**🔗 Potential Integration Scenarios:**
• Culinary schools with cold storage for ingredients
• Agricultural universities with produce storage
• Research institutions with specimen storage
• Schools with large-scale food storage operations

While serving different industries, both can be deployed independently or together for institutions with diverse needs.

**📞 Schedule a Demo:**
Desalite Connect: +91 7099020876
IceBox: +91 8811047292

Which solution aligns with your business needs?"""

    def _compare_transtrack_icebox(self) -> str:
        """Comparison between TransTrack and IceBox"""
        return """**🔄 Comparing TransTrack vs IceBox:**

Both serve the **logistics and supply chain** sector but focus on different operational aspects:

**🚛 TRANSTRACK - Transport Management System (TMS)**
**Focus:** Transportation & Logistics Operations
**Core Purpose:** Optimize the movement of goods

**What It Manages:**
• Transportation Planning & Strategy
• Route Optimization (minimize time, fuel, costs)
• Carrier Selection & Management
• Real-time Shipment Tracking & Visibility
• Load Consolidation & Optimization
• Supply Chain Analytics & Insights
• Freight Cost Management
• Compliance & Regulatory Support
• Delivery Performance Monitoring

**Key Benefits:**
✅ Reduced transportation costs (fuel, time, resources)
✅ Improved delivery efficiency
✅ Real-time shipment visibility
✅ Data-driven decision making
✅ Better carrier relationships
✅ Enhanced customer service

**Best For:**
• Logistics companies
• Transportation businesses
• Fleet management operations
• Supply chain coordinators
• Companies shipping goods frequently

**Use Case:** Managing the transportation of goods from point A to point B efficiently

---

**❄️ ICEBOX - Cold Storage Management System**
**Focus:** Warehouse & Storage Operations
**Core Purpose:** Optimize storage of temperature-sensitive goods

**What It Manages:**
• Inventory Management (batch, brand, expiry, rack-wise)
• Precision Temperature Control & Monitoring
• Warehouse Workflow Automation
• Storage Space Optimization
• Goods Receiving & Dispatch
• Chamber Management (In/Out/Shifting)
• Weigh Bridge Operations
• Labour Management & Allocation
• Detailed Billing (Storage, Labour, Services)
• Security & Safety Systems

**Key Benefits:**
✅ Optimal temperature maintenance
✅ Reduced spoilage and waste
✅ Efficient space utilization
✅ Automated workflow (zero manual errors)
✅ Real-time inventory visibility
✅ Comprehensive security monitoring

**Best For:**
• Cold storage facilities
• Warehouses (especially temperature-controlled)
• Food processing companies
• Pharmaceutical storage
• Perishable goods management

**Use Case:** Managing the storage and handling of goods at a fixed location

---

**🎯 Key Differences:**

| Aspect | TransTrack | IceBox |
|--------|-----------|---------|
| **Focus** | Goods in MOTION | Goods in STORAGE |
| **Operation** | Transportation & Delivery | Warehousing & Storage |
| **Location** | Multiple points (routes) | Fixed facility |
| **Main Goal** | Efficient movement | Optimal storage conditions |
| **Temperature** | General monitoring | Precise control critical |
| **Primary Metric** | Delivery time & cost | Storage efficiency & quality |

---

**🤝 How They Work Together:**

Many businesses in cold chain logistics need BOTH:

**Example 1 - Cold Chain Company:**
• **TransTrack** manages refrigerated truck fleet and deliveries
• **IceBox** manages cold storage warehouse operations

**Example 2 - Food Distribution:**
• **TransTrack** optimizes distribution routes to retailers
• **IceBox** manages central cold storage facility

**Example 3 - Pharmaceutical Logistics:**
• **TransTrack** tracks temperature-sensitive shipments
• **IceBox** manages warehouse storage before distribution

---

**🎯 Which Do You Need?**

**Choose TransTrack if:**
✅ Your primary challenge is transportation efficiency
✅ You manage fleet or shipments
✅ You need route optimization
✅ You want to reduce delivery costs

**Choose IceBox if:**
✅ Your primary challenge is storage management
✅ You operate a warehouse or cold storage
✅ You need temperature control
✅ You want to optimize storage operations

**Choose BOTH if:**
✅ You run a complete cold chain operation
✅ You need end-to-end logistics management
✅ You handle both transportation AND storage

**💼 Complete Cold Chain Solution:**
TransTrack + IceBox = Comprehensive cold chain management from storage to delivery

**📞 Get Started:**
TransTrack: +91 8811047292
IceBox: +91 8811047292

Which aspect of your logistics needs optimization - transportation, storage, or both?"""

    def _compare_three_school_transport(self) -> str:
        """Comparison of Ednect, Desalite, and TransTrack"""
        return """**🔄 Comparing Ednect, Desalite Connect & TransTrack:**

You're looking at **2 School Management Systems + 1 Transport System**. Here's a comprehensive breakdown:

---

**📚 SCHOOL MANAGEMENT SYSTEMS (Both for Education):**

**EDNECT vs DESALITE CONNECT:**

| Feature | Ednect | Desalite Connect |
|---------|--------|------------------|
| **Experience** | 10+ years | 5+ years |
| **Clients** | 500+ | Growing network |
| **Reputation** | Veteran, proven | Modern, user-focused |
| **Unique Edge** | Extensive track record | Enhanced UX, Digital Evaluation |

**Common Features (Both Offer):**
✅ Student & Staff Management
✅ Fee Collection & Payment Gateway
✅ Attendance & Leave Management
✅ Timetable & Academic Management
✅ Exam & Result Management
✅ Parent & Student Portals
✅ SMS & Communication Tools

**Additional in Desalite:** Library Management, Online Assessment, Digital Evaluation

---

**🚛 TRANSTRACK - Transport Management System:**

**Industry:** Logistics & Transportation (NOT Education)

**What It Does:**
• Route optimization & planning
• Real-time shipment tracking
• Carrier management
• Load consolidation
• Supply chain analytics
• Cost reduction

**Who Uses It:** Logistics companies, fleet managers, transportation businesses

---

**🎯 DECISION GUIDE:**

**Scenario 1: You Run a School**
**Choose:** Ednect OR Desalite Connect
• **Ednect** if you want proven track record (10+ years)
• **Desalite** if you want modern UX and digital evaluation

**Do You Need TransTrack?**
Maybe! If your school has:
✅ School bus fleet to manage
✅ Student transportation operations
✅ Multiple pick-up/drop-off routes

Then: **School ERP (Ednect/Desalite) + TransTrack** = Complete solution

---

**Scenario 2: You Run a Transportation Business**
**Choose:** TransTrack only
(School ERPs wouldn't apply to your business)

---

**Scenario 3: You Run Both School & Transport Business**
**Perfect! You Need:**
• **Ednect or Desalite Connect** for school operations
• **TransTrack** for transport/logistics operations

---

**💡 Recommended Combinations:**

**For Schools with Transport:**
✅ **Desalite Connect + TransTrack** 
   - Modern school management + Professional fleet management

✅ **Ednect + TransTrack**
   - Established school ERP + Transportation optimization

**For Education + Logistics Groups:**
Use all three for different divisions:
• Ednect/Desalite for educational institutions
• TransTrack for logistics division

---

**📊 Quick Comparison:**

```
EDUCATION SECTOR:
├── Ednect (10+ years, 500+ clients)
└── Desalite Connect (5+ years, modern UX)

LOGISTICS SECTOR:
└── TransTrack (Transportation Management)
```

**📞 Next Steps:**

1. **Identify Your Primary Need:**
   - Education management? → Ednect or Desalite
   - Transportation optimization? → TransTrack
   - Both? → Combination solution

2. **Schedule Demos:**
   - School ERPs: +91 7099020876
   - TransTrack: +91 8811047292

3. **Get Custom Quote** for your specific requirements

Which combination suits your business needs?"""

    def _compare_three_all_except_desalite(self) -> str:
        """Comparison of Ednect, TransTrack, and IceBox"""
        return """**🔄 Comparing Ednect, TransTrack & IceBox:**

You're looking at **3 completely different industry solutions**. Here's what each offers:

---

**📚 EDNECT - School Management ERP**
**Industry:** Education
**Experience:** 10+ years, 500+ clients

**What It Manages:**
✅ Student & Staff Administration
✅ Academic Operations (Timetable, Exams, Results)
✅ Fee Collection & Financial Management
✅ Attendance & Leave Systems
✅ Parent-Teacher Communication
✅ Admission Management

**Target:** Schools, Colleges, Educational Institutions
**Best For:** Institutions needing proven, mature educational ERP

---

**🚛 TRANSTRACK - Transport Management System**
**Industry:** Logistics & Transportation

**What It Manages:**
✅ Route Optimization & Planning
✅ Real-time Shipment Tracking
✅ Carrier Management
✅ Load Consolidation
✅ Supply Chain Analytics
✅ Cost Reduction Strategies

**Target:** Logistics Companies, Fleet Managers, Transportation Businesses
**Best For:** Companies optimizing transportation operations

---

**❄️ ICEBOX - Cold Storage Management System**
**Industry:** Warehousing & Cold Chain

**What It Manages:**
✅ Inventory Management (batch, expiry, rack-wise)
✅ Precision Temperature Control
✅ Automated Warehouse Workflow
✅ Security & Safety Monitoring
✅ Detailed Billing Systems
✅ Multi-Storage Support

**Target:** Cold Storage Facilities, Warehouse Operations
**Best For:** Temperature-controlled storage and perishable goods management

---

**🎯 WHICH PRODUCTS DO YOU NEED?**

**Scenario 1: Single Industry**
Choose the product for your industry:
• Education → **Ednect**
• Logistics → **TransTrack**
• Cold Storage → **IceBox**

---

**Scenario 2: Diversified Business**

**Example A: Educational Institution with Facilities**
**Ednect + IceBox:**
• Agricultural university with produce storage
• Culinary school with ingredient cold storage
• Research institution with specimen storage

**Example B: School with Transportation**
**Ednect + TransTrack:**
• School with bus fleet management
• Educational institution with student transport
• Multi-campus college with shuttle services

**Example C: Cold Chain Logistics**
**TransTrack + IceBox:**
• Complete cold chain operation
• Storage facility with distribution fleet
• Refrigerated transportation company

---

**Scenario 3: Diversified Group (All Three)**

Perfect for business groups with multiple divisions:

```
EDUCATION DIVISION
└── Ednect (School/College Management)

LOGISTICS DIVISION
└── TransTrack (Fleet & Transportation)

WAREHOUSING DIVISION
└── IceBox (Cold Storage Operations)
```

**Real Example:**
A corporate group running:
• Educational institutions (use Ednect)
• Transportation/logistics company (use TransTrack)
• Cold storage facilities (use IceBox)

---

**📊 Industry Alignment:**

| Your Business | Recommended Products |
|---------------|---------------------|
| Education Only | **Ednect** |
| Logistics Only | **TransTrack** |
| Cold Storage Only | **IceBox** |
| School + Transport | **Ednect + TransTrack** |
| School + Cold Storage | **Ednect + IceBox** |
| Logistics + Warehousing | **TransTrack + IceBox** |
| Diversified Group | **All Three** |

---

**💰 Investment Approach:**

**Single Product:** Focused solution for specific industry
**Two Products:** Integrated solution for complementary operations
**All Three:** Complete business management suite for diversified groups

---

**🚀 Getting Started:**

**Step 1:** Identify which industries you operate in
**Step 2:** Schedule demos for relevant products
**Step 3:** Get custom quotes based on your needs

**📞 Contact:**
• Ednect: +91 7099020876
• TransTrack: +91 8811047292
• IceBox: +91 8811047292

**Which industries does your business operate in?**"""

    def _compare_three_school_icebox(self) -> str:
        """Comparison of Ednect, Desalite, and IceBox"""
        return """**🔄 Comparing Ednect, Desalite Connect & IceBox:**

You're looking at **2 School Management Systems + 1 Cold Storage System**:

---

**📚 SCHOOL MANAGEMENT SYSTEMS (Both for Education):**

**EDNECT - The Veteran**
✅ **Experience:** 10+ years, 500+ clients
✅ **Strength:** Proven track record, extensive deployments
✅ **Clients:** Heritage Public School, Reality Public School, Seppa Public School

**DESALITE CONNECT - The Modern Choice**
✅ **Experience:** 5+ years
✅ **Strength:** Enhanced UX, modern interface
✅ **Unique Features:** Library Management, Online Assessment, Digital Evaluation
✅ **Clients:** Saint Francis De Sales Schools (multiple locations), NPS International, Green Mount School

**What Both Offer:**
• Student & Staff Management
• Fee Collection with Payment Gateway
• Attendance & Leave Management
• Academic Management (Timetable, Exams, Results)
• Parent & Student Portals
• SMS & Communication Tools
• Cloud-based Access

**Key Difference:**
• **Ednect:** Mature product with 10+ years experience
• **Desalite:** Modern UX with digital evaluation & library management

---

**❄️ ICEBOX - Cold Storage Management System**

**Industry:** Warehousing & Cold Chain (NOT Education)

**What It Manages:**
✅ Inventory Management (batch, brand, expiry, rack-wise)
✅ Precision Temperature Control & Monitoring
✅ Automated Warehouse Workflow
✅ Security & Safety Systems
✅ Detailed Billing (Labour, Order, Rental)
✅ Multi-Storage Support

**Target Users:** Cold storage facilities, warehouse operators, food/pharma companies

---

**🎯 DECISION GUIDE:**

**Scenario 1: You Run a School/College**
**Choose:** Ednect OR Desalite Connect

**Pick Ednect if:**
✅ You want 10+ years of proven reliability
✅ You value extensive deployment history
✅ You want established ERP with 500+ clients

**Pick Desalite if:**
✅ You prioritize modern, user-friendly interface
✅ You need digital evaluation tools
✅ You want integrated library management

**Do You Need IceBox?**
Add IceBox if your institution has:
✅ Research labs with specimen storage
✅ Culinary/hospitality programs with ingredient storage
✅ Agricultural programs with produce storage
✅ Large-scale food service operations
✅ Medical/pharmacy programs with temperature-controlled storage

---

**Scenario 2: You Run a Cold Storage Facility**
**Choose:** IceBox only
(School ERPs wouldn't apply)

---

**Scenario 3: Diversified Educational Operations**

**Perfect Combination:**

**Option A: Ednect + IceBox**
• Established school management
• Cold storage for specialized programs

**Option B: Desalite Connect + IceBox**
• Modern school interface
• Cold storage operations
• Best for progressive institutions

---

**💡 REAL-WORLD USE CASES:**

**Agricultural University:**
• **Ednect/Desalite** for academic management
• **IceBox** for farm produce storage

**Culinary Institute:**
• **Ednect/Desalite** for student & course management
• **IceBox** for ingredient cold storage

**Medical College:**
• **Ednect/Desalite** for academic operations
• **IceBox** for pharmaceutical & specimen storage

**Hospitality School:**
• **Ednect/Desalite** for student management
• **IceBox** for food storage facilities

**Research Institution:**
• **Ednect/Desalite** for researcher & project management
• **IceBox** for temperature-sensitive research materials

---

**📊 Product Alignment:**

```
EDUCATION SECTOR:
├── Ednect (Traditional choice, 10+ years)
└── Desalite Connect (Modern choice, 5+ years)

WAREHOUSING SECTOR:
└── IceBox (Cold Storage Management)
```

---

**🔗 Integration Benefits:**

When combining School ERP + IceBox:
✅ Single vendor support
✅ Potential integration for cafeteria/food management
✅ Unified reporting across operations
✅ Cost benefits for multiple products

---

**📞 Next Steps:**

1. **For Education Management:**
   - Compare Ednect vs Desalite demos
   - Contact: +91 7099020876

2. **For Cold Storage:**
   - Schedule IceBox demo
   - Contact: +91 8811047292

3. **For Both:**
   - Mention your dual requirements for bundled solutions

**Which operations do you need to manage?**"""

    def _compare_three_desalite_transport_icebox(self) -> str:
        """Comparison of Desalite, TransTrack, and IceBox"""
        return """**🔄 Comparing Desalite Connect, TransTrack & IceBox:**

You're looking at **3 different industry solutions**. Here's a comprehensive comparison:

---

**📚 DESALITE CONNECT - School Management ERP**
**Industry:** Education
**Experience:** 5+ years with prestigious institutions

**Core Functions:**
✅ Student & Staff Management
✅ Fee Collection with Online Payment Gateway
✅ Attendance & Leave Management
✅ Academic Management (Timetable, Exams, Results)
✅ Library Management System
✅ Online Assessment & Digital Evaluation
✅ Parent & Student Portals
✅ Report Card Management

**Unique Strengths:**
• Modern, intuitive user interface
• Digital evaluation tools
• Integrated library management
• Used by educational networks (Saint Francis De Sales Schools, NPS International, Green Mount School)

**Target:** Educational institutions prioritizing modern UX

---

**🚛 TRANSTRACK - Transport Management System**
**Industry:** Logistics & Transportation

**Core Functions:**
✅ Transportation Planning & Route Optimization
✅ Real-time Shipment Tracking & Visibility
✅ Carrier Selection & Management
✅ Load Consolidation & Optimization
✅ Supply Chain Analytics
✅ Cost Reduction Strategies
✅ Compliance & Regulatory Support

**Unique Strengths:**
• Reduced transportation costs
• Improved delivery efficiency
• Data-driven decision making
• Real-time visibility across supply chain

**Target:** Logistics companies, fleet managers, transportation businesses

---

**❄️ ICEBOX - Cold Storage Management System**
**Industry:** Warehousing & Cold Chain

**Core Functions:**
✅ Inventory Management (batch, brand, expiry, rack-wise)
✅ Precision Temperature Control & Monitoring
✅ Automated Warehouse Workflow
✅ Security & Safety Monitoring
✅ Weigh Bridge & Chamber Management
✅ Detailed Billing Systems
✅ Labour Management & Allocation

**Unique Strengths:**
• Zero manual intervention workflow
• Real-time temperature alerts
• Complete automation from vehicle arrival to exit
• Multi-storage support

**Target:** Cold storage facilities, warehouse operations, perishable goods management

---

**🎯 WHICH PRODUCTS DO YOU NEED?**

**Scenario 1: Single Industry Focus**
• Education only → **Desalite Connect**
• Logistics only → **TransTrack**
• Cold Storage only → **IceBox**

---

**Scenario 2: Dual Operations**

**A) Education + Transportation**
**Desalite Connect + TransTrack:**
• School/college with bus fleet
• Educational institution with student transport services
• Multi-campus organization with shuttle operations
• Educational tour/trip management

**Benefits:**
✅ Manage academics with Desalite
✅ Optimize transport routes with TransTrack
✅ Track school buses in real-time
✅ Reduce transport costs

---

**B) Education + Cold Storage**
**Desalite Connect + IceBox:**
• Agricultural schools with produce storage
• Culinary institutes with ingredient cold storage
• Research institutions with specimen storage
• Hospitality schools with food storage

**Benefits:**
✅ Modern academic management
✅ Professional storage operations
✅ Temperature-controlled facilities for programs

---

**C) Logistics + Cold Storage**
**TransTrack + IceBox:**
• Cold chain logistics companies
• Food distribution businesses
• Pharmaceutical logistics
• Refrigerated transportation + storage operations

**Benefits:**
✅ Complete cold chain management
✅ Storage to delivery optimization
✅ End-to-end temperature monitoring
✅ Comprehensive supply chain solution

---

**Scenario 3: Diversified Business Group (All Three)**

**Example: Large Conglomerate**
```
EDUCATION DIVISION
└── Desalite Connect (Schools/Colleges)

LOGISTICS DIVISION
└── TransTrack (Fleet & Transportation)

WAREHOUSING DIVISION
└── IceBox (Cold Storage Facilities)
```

**Perfect for:**
• Business groups with multiple industry operations
• Organizations with diverse revenue streams
• Companies looking for unified technology solutions

---

**💡 REAL-WORLD COMBINATIONS:**

**Combination 1: Modern Educational Institute**
**Products:** Desalite Connect + TransTrack
**Use Case:** 
- Progressive school with 50+ buses
- Modern academic management interface
- Optimized student transportation with route tracking
- Reduced transport costs and improved safety

**Combination 2: Agricultural College**
**Products:** Desalite Connect + IceBox
**Use Case:**
- Student & course management
- Farm produce cold storage
- Research specimen preservation
- Food science program support

**Combination 3: Cold Chain Company**
**Products:** TransTrack + IceBox
**Use Case:**
- Cold storage warehouse operations
- Refrigerated truck fleet management
- Temperature-controlled distribution
- Complete cold chain visibility

**Combination 4: Diversified Group**
**Products:** All Three
**Use Case:**
- Educational institutions (Desalite)
- Logistics division (TransTrack)
- Cold storage facilities (IceBox)
- Single vendor, integrated support

---

**📊 Quick Comparison Matrix:**

| Feature | Desalite | TransTrack | IceBox |
|---------|----------|------------|--------|
| **Industry** | Education | Logistics | Warehousing |
| **Focus** | Academic Ops | Transportation | Storage |
| **Users** | Teachers/Students | Fleet Managers | Warehouse Staff |
| **Key Benefit** | Modern UX | Cost Reduction | Automation |
| **Mobility** | Cloud-based | Route Tracking | Fixed Location |

---

**💰 Investment Strategy:**

**Single Product:** ₹₹ - Industry-specific solution
**Two Products:** ₹₹₹ - Integrated complementary operations
**All Three:** ₹₹₹₹ - Complete business suite (best value for diversified groups)

---

**🚀 Getting Started:**

**Step 1: Identify Your Operations**
□ Education management?
□ Transportation/logistics?
□ Cold storage/warehousing?

**Step 2: Schedule Demos**
• Desalite Connect: +91 7099020876
• TransTrack: +91 8811047292
• IceBox: +91 8811047292

**Step 3: Discuss Integration**
Mention if you need multiple products for bundled pricing and integrated support.

**Which combination matches your business needs?**"""

    def _compare_all_products(self) -> str:
        """Comprehensive comparison of all four products"""
        return """**🔄 Complete Product Suite Comparison:**
**Ednect | Desalite Connect | TransTrack | IceBox**

---

**📊 OVERVIEW BY INDUSTRY:**

**🎓 EDUCATION MANAGEMENT (2 Products):**

**EDNECT vs DESALITE CONNECT**

| Aspect | Ednect | Desalite Connect |
|--------|--------|------------------|
| **Experience** | 10+ years | 5+ years |
| **Clients** | 500+ | Growing network |
| **Maturity** | Veteran, proven | Modern, progressive |
| **Interface** | Traditional | Enhanced UX |
| **Special Features** | Extensive track record | Library, Digital Evaluation |

**Common Features:**
✅ Student & Staff Management
✅ Fee Collection & Payment Gateway
✅ Attendance & Leave Management
✅ Academic Management (Timetable, Exams, Results)
✅ Parent & Student Portals
✅ SMS & Communication Tools

**When to Choose:**
• **Ednect:** Want proven 10+ year track record, 500+ clients
• **Desalite:** Want modern UX, digital evaluation, library management

---

**🚛 LOGISTICS MANAGEMENT:**

**TRANSTRACK - Transport Management System**

**Industry:** Logistics, Transportation, Supply Chain
**Core Functions:**
• Transportation Planning & Route Optimization
• Real-time Shipment Tracking
• Carrier Management
• Load Consolidation
• Supply Chain Analytics
• Cost Reduction

**Best For:** Logistics companies, fleet operations, supply chain optimization

---

**❄️ WAREHOUSING MANAGEMENT:**

**ICEBOX - Cold Storage Management System**

**Industry:** Warehousing, Cold Chain, Storage
**Core Functions:**
• Inventory Management (batch, brand, expiry, rack-wise)
• Precision Temperature Control
• Automated Workflow (Vehicle → Chamber → Exit)
• Security & Safety Monitoring
• Detailed Billing Systems

**Best For:** Cold storage facilities, warehouses, perishable goods management

---

**🎯 DECISION FRAMEWORK:**

**SINGLE INDUSTRY ORGANIZATIONS:**

**Education Only:**
→ Choose **Ednect** or **Desalite Connect**
- Ednect for proven stability
- Desalite for modern features

**Logistics Only:**
→ Choose **TransTrack**
- Optimize transportation operations

**Cold Storage Only:**
→ Choose **IceBox**
- Manage warehouse operations

---

**MULTI-INDUSTRY ORGANIZATIONS:**

**1️⃣ Education + Transportation**
**Products:** (Ednect OR Desalite) + TransTrack

**Use Cases:**
• Schools with bus fleet management
• Educational institutions with student transport
• Multi-campus organizations with shuttles
• Educational tour companies

**Benefits:**
✅ Academic operations + Transport optimization
✅ Student safety tracking
✅ Cost-effective route planning

---

**2️⃣ Education + Cold Storage**
**Products:** (Ednect OR Desalite) + IceBox

**Use Cases:**
• Agricultural universities with produce storage
• Culinary schools with ingredient storage
• Research institutions with specimen storage
• Food science programs
• Medical colleges with pharmaceutical storage

**Benefits:**
✅ Academic management + Professional storage
✅ Research support with proper storage
✅ Temperature-controlled facilities

---

**3️⃣ Logistics + Warehousing**
**Products:** TransTrack + IceBox

**Use Cases:**
• Cold chain logistics companies
• Food distribution businesses
• Pharmaceutical supply chain
• Storage + distribution operations

**Benefits:**
✅ Complete cold chain management
✅ Storage to delivery optimization
✅ End-to-end temperature monitoring
✅ Comprehensive supply chain visibility

---

**4️⃣ Education + Logistics + Warehousing**
**Products:** (Ednect OR Desalite) + TransTrack + IceBox

**Use Cases:**
• Agricultural university with:
  - Student management (School ERP)
  - Farm product distribution (TransTrack)
  - Cold storage for produce (IceBox)

• Hospitality group with:
  - Culinary school (School ERP)
  - Food distribution (TransTrack)
  - Ingredient storage (IceBox)

---

**5️⃣ Diversified Business Conglomerate (ALL FOUR)**
**Products:** Ednect + Desalite + TransTrack + IceBox

**Use Cases:**
• Large business groups with multiple divisions:
  ```
  EDUCATION DIVISION
  ├── K-12 Schools → Ednect
  └── Colleges/Universities → Desalite Connect
  
  LOGISTICS DIVISION
  └── Transport Operations → TransTrack
  
  WAREHOUSING DIVISION
  └── Cold Storage Facilities → IceBox
  ```

**Benefits:**
✅ Single vendor for all operations
✅ Unified support and training
✅ Potential integration across systems
✅ Volume pricing benefits
✅ Consistent technology stack

---

**💼 INDUSTRY-SPECIFIC RECOMMENDATIONS:**

**Education Sector:**
- **Primary/Secondary Schools:** Ednect (proven) or Desalite (modern)
- **With Bus Fleet:** Add TransTrack
- **With Food Programs:** Add IceBox

**Logistics Sector:**
- **Transportation Companies:** TransTrack
- **With Warehousing:** Add IceBox
- **Training Programs:** Add Ednect/Desalite

**Warehousing Sector:**
- **Cold Storage Facilities:** IceBox
- **With Distribution:** Add TransTrack

**Conglomerates:**
- **Multiple Industries:** Combination based on operations

---

**📊 FEATURE COMPARISON MATRIX:**

| Feature | Ednect | Desalite | TransTrack | IceBox |
|---------|--------|----------|------------|--------|
| **Industry** | Education | Education | Logistics | Warehousing |
| **Experience** | 10+ years | 5+ years | Proven | Automated |
| **Cloud-Based** | ✅ | ✅ | ✅ | ✅ |
| **Real-Time** | ✅ | ✅ | ✅ | ✅ |
| **Mobile Access** | ✅ | ✅ | ✅ | ✅ |
| **Customizable** | ✅ | ✅ | ✅ | ✅ |
| **Unique Strength** | Track Record | Modern UX | Cost Savings | Automation |

---

**💰 PRICING STRATEGY:**

**Single Product:** Industry-specific solution
**Two Products:** Complementary operations (potential bundle discount)
**Three Products:** Integrated business solution (better pricing)
**All Four Products:** Enterprise suite (best value for large groups)

💡 **Note:** Custom pricing based on requirements. Bundle discounts available for multiple products.

---

**🚀 IMPLEMENTATION ROADMAP:**

**Phase 1: Primary Operation**
Start with your core business (School/Logistics/Storage)

**Phase 2: Add Complementary**
Add products for related operations

**Phase 3: Full Integration**
Deploy complete suite for diversified operations

---

**📞 NEXT STEPS:**

**1. Identify Your Operations:**
□ Education management
□ Transportation/logistics
□ Cold storage/warehousing
□ Multiple industries

**2. Schedule Demos:**
• **School ERPs (Ednect/Desalite):** +91 7099020876
• **TransTrack & IceBox:** +91 8811047292
• **Email:** ajit@vasptechnologies.com

**3. Discuss Your Needs:**
Mention all operations you manage for:
✅ Custom recommendations
✅ Bundle pricing
✅ Integration planning
✅ Unified support

**4. Get Custom Proposal:**
We'll create a tailored solution package based on your specific requirements.

---

**🎁 SPECIAL BENEFITS FOR MULTIPLE PRODUCTS:**

✅ **Single Vendor Support** - One team for all systems
✅ **Unified Training** - Consistent learning experience
✅ **Volume Discounts** - Better pricing for multiple products
✅ **Integration Priority** - Custom integrations between systems
✅ **Dedicated Account Manager** - Personalized service

---

**Which operations do you need to digitalize?**

Let us know your industry mix, and we'll recommend the perfect combination!"""

    def _suggest_comparison(self, product: str) -> str:
        """Suggest what to compare a single product with"""
        suggestions = {
            'ednect': """You mentioned **Ednect**. Would you like to compare it with:

1️⃣ **Desalite Connect** - Alternative school management ERP
2️⃣ **TransTrack** - If you also have transportation needs
3️⃣ **IceBox** - If you have cold storage requirements

Or would you like detailed information about Ednect only?""",
            
            'desalite': """You mentioned **Desalite Connect**. Would you like to compare it with:

1️⃣ **Ednect** - Alternative school management ERP (10+ years experience)
2️⃣ **TransTrack** - If you also manage transportation
3️⃣ **IceBox** - If you have warehousing needs

Or would you like detailed information about Desalite Connect only?""",
            
            'transtrack': """You mentioned **TransTrack**. Would you like to compare it with:

1️⃣ **IceBox** - If you need both transportation AND storage management
2️⃣ **Ednect/Desalite** - If you're in education with transport needs

Or would you like detailed information about TransTrack only?""",
            
            'icebox': """You mentioned **IceBox**. Would you like to compare it with:

1️⃣ **TransTrack** - If you need both storage AND transportation
2️⃣ **Ednect/Desalite** - If you're an educational institution with storage needs

Or would you like detailed information about IceBox only?"""
        }
        
        return suggestions.get(product, self._general_comparison())
    
    def _general_comparison(self) -> str:
        """General comparison overview"""
        return """**Our Complete Product Suite:**

We offer 4 distinct products for different industries:

**🎓 EDUCATION MANAGEMENT:**
1️⃣ **Ednect** - School ERP (10+ years, 500+ clients)
2️⃣ **Desalite Connect** - School ERP (5+ years, modern UX)

**🚛 LOGISTICS MANAGEMENT:**
3️⃣ **TransTrack** - Transport Management System

**❄️ WAREHOUSING MANAGEMENT:**
4️⃣ **IceBox** - Cold Storage Management System

---

**Which products would you like me to compare?**

Examples:
• "Compare Ednect and Desalite" - School ERPs
• "Compare TransTrack and IceBox" - Logistics vs Storage
• "Compare all products" - Complete overview
• "Compare Ednect, TransTrack, and IceBox" - Multiple industries

**Or tell me your industry, and I'll recommend the right product(s):**
• Education → Ednect or Desalite
• Logistics → TransTrack
• Cold Storage → IceBox
• Multiple industries → Combination solution

What would you like to know more about?"""


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
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Check for job-related queries
        if any(word in user_message for word in ['job', 'vacancy', 'hiring', 'career', 'recruitment', 'employment']):
            response = """Thank you for your interest in career opportunities at Vasp Technologies!

For information about job openings and career opportunities, please:
📧 Email your resume to: hr@vasptechnologies.co.in
📞 Call: +91 7099020876

You can also check our website or LinkedIn page for current openings.

Is there anything else about our products I can help you with?"""
            dispatcher.utter_message(text=response)
            return []
        
        # Check for purchase/acquisition queries
        if any(word in user_message for word in ['buy', 'purchase', 'get', 'acquire', 'obtain', 'order']):
            response = """Great! Here's how to get started with our software:

1️⃣ **Request a Free Demo**
   📞 Call: +91 7099020876 (Ednect/Desalite) or +91 8811047292 (TransTrack/IceBox)
   📧 Email: ajit@vasptechnologies.com

2️⃣ **Consultation**
   Our team will understand your requirements

3️⃣ **Customization & Quotation**
   We'll provide a tailored solution and pricing

4️⃣ **Agreement & Implementation**
   Once approved, we begin setup and training

Would you like to schedule a demo now?"""
            dispatcher.utter_message(text=response)
            return []
        
        # Check for unrelated tech support
        if any(word in user_message for word in ['tech support', 'technical support', 'fix my', 'repair', 'not working', 'broken']):
            if not any(word in user_message for word in ['ednect', 'desalite', 'transtrack', 'icebox', 'vasp']):
                response = """I'm VaspX, an assistant for Vasp Technologies products (Ednect, Desalite Connect, TransTrack, and IceBox). I can only help with information about our products and services.

For general tech support or unrelated queries, please contact the relevant service provider.

How can I help you with Vasp Technologies products?"""
                dispatcher.utter_message(text=response)
                return []
        
        # Check if any product is mentioned
        products = []
        if 'ednect' in user_message:
            products.append('Ednect')
        if 'desalite' in user_message or 'desallite' in user_message:
            products.append('Desalite Connect')
        if 'transtrack' in user_message or 'trans track' in user_message:
            products.append('TransTrack')
        if 'icebox' in user_message or 'ice box' in user_message:
            products.append('IceBox')
        
        if products:
            response = f"I understand you're asking about {', '.join(products)}, but I'm not sure exactly what you'd like to know. \n\nI can help with:\n• Product features\n• Pricing\n• Implementation\n• Client list\n• Comparison\n• Contact information\n• Demo requests\n\nWhat would you like to know?"
        else:
            response = """I'm not sure I understood that correctly. I'm VaspX, here to help you with:

📚 **Products:** Ednect, Desalite Connect, TransTrack, IceBox
💡 **Information:** Features, Pricing, Clients, Implementation
📞 **Support:** Contact info, Demo requests, Training
🤝 **Other:** Careers, Purchase process, Technical specs

You can also speak directly with our team:
📞 +91 7099020876 / +91 8811047292

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

🎓 **Educational Institution?** → Ednect or Desalite Connect
🚛 **Logistics/Transportation?** → TransTrack
❄️ **Cold Storage/Warehouse?** → IceBox

Which industry are you in?"""
        
        dispatcher.utter_message(text=response)
        return []
    