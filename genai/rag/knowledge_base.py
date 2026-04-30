
# Knowledge Base — TRAI Regulations +
# Telecom Fraud Patterns

# Ye documents haara RAG ka "brain" hain
# ChromaDB inhe vectors mein store karega

DOCUMENTS = [
    {
        "id": "trai_001",
        "title": "TRAI UCC Regulations — Definition",
        "content": """
        The Telecom Regulatory Authority of India (TRAI) defines Unsolicited 
        Commercial Communication (UCC) as any commercial communication which 
        a subscriber has not consented to receive. Under TRAI regulations, 
        telemarketers must register with the Do Not Disturb (DND) registry. 
        Unregistered telemarketers calling DND subscribers are liable for 
        penalties. Subscribers can report UCC through the DND app or by 
        calling 1909. Repeated violations can result in disconnection of 
        the telecom service.
        """
    },
    {
        "id": "trai_002",
        "title": "TRAI Regulations — Penalty Framework",
        "content": """
        TRAI imposes strict penalties on telemarketers violating UCC norms.
        First violation: Warning issued to the telemarketer.
        Second violation: Disconnection of telemarketer's SIM for 2 years.
        Third violation: Permanent blacklisting of the telemarketer.
        Telecom operators are required to implement a scrubbing mechanism 
        to filter calls from blacklisted numbers. Operators failing to 
        comply with TRAI directives can face financial penalties up to 
        Rs. 50 lakhs per violation.
        """
    },
    {
        "id": "trai_003",
        "title": "TRAI DND Registry — How It Works",
        "content": """
        The Do Not Disturb (DND) registry is maintained by TRAI to protect 
        subscribers from unwanted commercial calls. Subscribers can register 
        for full DND blocking or category-specific blocking. Once registered, 
        telemarketers are prohibited from calling these numbers. The registry 
        is updated every 7 days and all registered telemarketers must 
        download the updated DND list. Calls made to DND registered numbers 
        by unregistered entities constitute a UCC violation.
        """
    },
    {
        "id": "fraud_001",
        "title": "Telecom Fraud Pattern — Robocall Detection",
        "content": """
        Robocalls are automated calls made by dialers without human involvement.
        Key indicators of robocall activity include:
        - Very short call duration (2-5 seconds) indicating auto-disconnect
        - Extremely high call volume from a single number (100+ calls/day)
        - Uniform call timing patterns regardless of time of day
        - Zero voicemail messages left despite high call volume
        - Near-zero callback rate from called parties
        Robocalls are typically used for scam operations, fake loan offers,
        insurance fraud, and OTP bypassing attacks.
        """
    },
    {
        "id": "fraud_002",
        "title": "Telecom Fraud Pattern — International Revenue Share Fraud",
        "content": """
        International Revenue Share Fraud (IRSF) is one of the most costly
        telecom frauds globally. Fraudsters artificially inflate traffic to 
        premium international numbers and share the revenue with the number 
        owner. Key indicators include:
        - Unusually high international call ratio (20%+ of total calls)
        - Short duration international calls (10-30 seconds each)
        - Calls to unusual international destinations
        - High international charge ratio relative to domestic usage
        - Sudden spike in international calling from a previously domestic number
        IRSF costs the telecom industry over $6 billion annually worldwide.
        """
    },
    {
        "id": "fraud_003",
        "title": "Telecom Fraud Pattern — SIM Box Fraud",
        "content": """
        SIM Box fraud involves routing international calls through local SIM 
        cards to avoid international termination fees. Fraudsters install 
        boxes containing multiple SIM cards that receive VoIP calls and 
        re-originate them as local calls. Detection indicators:
        - High call volume with very similar duration patterns
        - Multiple calls to the same destination numbers
        - Calling patterns active 24 hours (automated systems)
        - Abnormal night-to-day call ratio (bots operate round the clock)
        - No voicemail usage despite massive call volumes
        SIM box fraud results in revenue loss for telecom operators and 
        compromises network quality.
        """
    },
    {
        "id": "fraud_004",
        "title": "Telecom Fraud Pattern — Account Takeover",
        "content": """
        Account takeover fraud occurs when fraudsters gain control of a 
        legitimate subscriber's account. Warning signs include:
        - Sudden change in calling patterns from historical baseline
        - High customer service call frequency (>3 calls) indicating disputes
        - New international destinations not previously called
        - Calls at unusual hours inconsistent with subscriber's history
        - Rapid exhaustion of prepaid balance or unusual postpaid bills
        Account takeover is often preceded by SIM swap attacks where the 
        fraudster convinces the operator to transfer the number to a new SIM.
        """
    },
    {
        "id": "fraud_005",
        "title": "Fraud Detection — Key CDR Metrics",
        "content": """
        Call Detail Records (CDR) contain valuable signals for fraud detection.
        High-risk indicators in CDR analysis:
        - CustServ Calls > 3: Strong indicator of fraud complaints against number
        - Day Mins > 300: Abnormally high daytime usage
        - Voicemail ratio near 0: Spammers never leave voicemail
        - Night-to-day ratio > 1: Automated systems operate at night
        - International charge ratio > 15%: Possible IRSF activity
        - Account call intensity high for new accounts: Fraud pattern
        These metrics when combined with ML models achieve high precision
        in identifying spam and fraudulent callers in telecom networks.
        """
    },
    {
        "id": "fraud_006",
        "title": "Fraud Detection — Industry Best Practices",
        "content": """
        Industry best practices for telecom fraud detection include:
        - Real-time CDR analysis with ML models for immediate flagging
        - Threshold-based alerting with human review for borderline cases
        - SHAP explainability to ensure transparent and auditable decisions
        - Regular model retraining as fraud patterns evolve
        - Multi-layer detection combining supervised and unsupervised methods
        - LLM-powered explanation systems for analyst-friendly alerts
        - RAG-based knowledge assistants for regulatory compliance queries
        The combination of classical ML and Generative AI provides both
        accuracy and interpretability in modern fraud detection systems.
        """
    },
    {
        "id": "trai_004",
        "title": "TRAI TCCCPR 2018 — Telecom Commercial Communications",
        "content": """
        The Telecom Commercial Communications Customer Preference Regulations 
        (TCCCPR) 2018 established a comprehensive framework for managing 
        commercial communications in India. Key provisions include:
        - Mandatory registration for all telemarketers
        - Consent-based communication framework
        - Distributed Ledger Technology (blockchain) for consent management
        - Headers and message templates must be pre-registered
        - Real-time monitoring of commercial communication traffic
        - Subscribers have the right to register preferences for 
          specific categories of commercial communications
        Non-compliance can result in disconnection and blacklisting.
        """
    },
]