def run_rule_checks(text):
    """
    Scans text for high-confidence phishing indicators.
    Returns: (is_phishing, reason)
    """
    # Keywords often found in your spam dataset
    blacklist = [
        'winner', 'prize', 'claim', 'urgent', 'verify', 
        'account suspended', 'free call', 'txt stop'
    ]
    
    normalized_text = text.lower()
    
    for trigger in blacklist:
        if trigger in normalized_text:
            return True, f"Keyword Match: {trigger}"
            
    return False, None