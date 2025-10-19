def format_telegram_message(data):
    """
    Formats the JSON data into a comprehensive Telegram Markdown message, 
    using nested keys for detailed metrics.
    """

    # --- TOP-LEVEL DATA ---
    trade_title = data.get('tradeTitle', 'New Trade Idea')
    ticker = data.get('ticker', 'N/A')
    current_price = data.get('currentPrice', 'N/A')
    expected_return = data.get('expectedReturnDisplay', 'N/A')
    summary_justification = data.get('summaryJustification', 'No summary provided.')
    publication_date = data.get('publicationDate', 'YYYY-MM-DD')
    
    # --- ANALYSIS DETAILS ---
    analysis = data.get('analysis', {})
    strategy = analysis.get('strategyType', 'N/A')
    
    # Trade Details
    trade_details = analysis.get('tradeDetails', {})
    expiration = trade_details.get('expiration', 'N/A')
    put_strike = trade_details.get('putStrike', 'N/A')
    max_profit = trade_details.get('maxProfit', 'N/A')
    
    # Metrics
    metrics = analysis.get('metrics', {})
    pop = metrics.get('pop', 'N/A')
    management = analysis.get('managementPlan', 'Standard management plan.')
    
    
    # --- MESSAGE CONSTRUCTION ---
    
    # 1. Title Block
    message = (
        f"🚨 *TRADE ALERT: {trade_title}* 🚨\n\n"
    )
    
    # 2. Key Metrics Block
    message += (
        f"📈 *Asset:* ${ticker} (Current Price: ${current_price})\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"📆 *Expiration:* {expiration} (Published: {publication_date})\n"
        f"🎯 *Entry Strike/Level:* ${put_strike}\n"
        f"-----------------------------------------\n"
        f"✅ *Prob. of Profit (PoP):* {pop}%\n"
        f"💰 *Max Annualized ROC:* {expected_return}\n"
        f"💵 *Max Profit:* ${max_profit}\n"
        f"-----------------------------------------\n"
    )
    
    # 3. Justification and Management Plan
    message += (
        f"\n*Summary Justification:*\n"
        f"_{summary_justification}_\n\n"
        f"*Management Plan:*\n"
        f"_{management}_\n\n"
    )
    
    # 4. Permalink (FIXED TO STATIC DOCUMENT PATH)
    # The URL is now fixed to the single page that displays all trade ideas data.
    STATIC_DOC_URL = "https://kahveci.pw/projectsgit/qma/docs/trade-ideas.html"
    
    message += (
        f"[View Full Analysis on Kahveci Nexus]({STATIC_DOC_URL})"
    )
    
    return message