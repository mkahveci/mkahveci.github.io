import os
import requests
import json
import re
import sys
from datetime import datetime

# --- Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

# --- Helper Function for MarkdownV2 Escaping (CORRECTED) ---
def escape_markdown(text):
    """
    Escapes special characters in a string for Telegram's MarkdownV2 parse mode.
    This is critical for preventing Parse Errors, especially with financial data.
    """
    if text is None:
        return 'N/A'

    # Ensure input is a string for replacement
    text = str(text)

    # 1. Escape the core reserved and problematic characters for MarkdownV2.
    # Pattern: \, _, *, [, ], (, ), ~, `, >, #, +, -, =, |, {, }, ., !, $
    reserved_chars = r'([_*\[\]()~`>#+=\-|{}.!$])'

    # Use re.sub to replace these characters with an escaped version.
    escaped_text = re.sub(reserved_chars, r'\\\1', text)

    # 2. Handle the ampersand, often used in P&L, which is safer to escape.
    escaped_text = escaped_text.replace('&', r'\&')

    # 3. Handle percentage signs.
    escaped_text = escaped_text.replace('%', r'\%')

    return escaped_text

def safe_float(value):
    """Converts a value to float safely, returning 0.0 on error."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def get_top_trade(file_path):
    """
    Reads the JSON array and returns the *first* trade object listed in the file.
    """
    try:
        with open(file_path, 'r') as f:
            data_array = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON in {file_path}. Is the file valid JSON?")
        return None

    if not data_array:
        print("Error: Trade idea JSON file is empty.")
        return None

    # Return the first trade (top element in the JSON array)
    return data_array[0]

def format_management_alert(trade_data, latest_step):
    """Formats a Telegram message for an adjustment, close, or assignment."""

    ticker = escape_markdown(trade_data.get('ticker', 'N/A'))
    step_type = escape_markdown(latest_step.get('stepType', 'Update'))
    date = escape_markdown(latest_step.get('date', 'N/A'))
    action = escape_markdown(latest_step.get('actionTaken', 'N/A'))
    notes = escape_markdown(latest_step.get('notes', ''))

    # Custom profit/loss extraction based on step type
    pnl_text = ''

    def safe_float_local(value):
        """Internal helper for numeric conversion."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if step_type == escape_markdown('ASSIGNMENT'):
        pnl_amount = latest_step.get('netCostBasisPerShare', 'N/A')
        # Cost basis is just a value, escape it without numeric format
        pnl_text = f"New Cost Basis: *\\${escape_markdown(pnl_amount)}*"

    elif step_type == escape_markdown('WHEEL_STEP: SELL_COVERED_CALL'):
        credit = safe_float_local(latest_step.get('grossCreditTotal', 0.0))
        # FIX: Apply formatting, then escape the result
        credit_formatted = f"{credit:.2f}"
        pnl_text = f"Credit Received: *\\+\\${escape_markdown(credit_formatted)}*" # FIXED '+' ESCAPING

    elif step_type in [escape_markdown('CALLED_AWAY'), escape_markdown('CLOSE'), escape_markdown('CLOSED_INDEPENDENT_PUT')]:
        pnl_amount = safe_float_local(latest_step.get('grossProfitLossAmount', 0.0))
        pnl_type = escape_markdown(latest_step.get('grossProfitLossType', 'Profit/Loss'))
        emoji = "✅" if pnl_type == escape_markdown("Profit") else "❌"
        # FIX: Apply formatting, then escape the result
        pnl_amount_formatted = f"{pnl_amount:.2f}"
        pnl_text = f"{emoji} Final P/L: *\\${escape_markdown(pnl_amount_formatted)}* ({pnl_type})"

    elif step_type == escape_markdown('ADJUSTMENT'):
        change = safe_float_local(latest_step.get('netChange', 0.0))
        change_type = escape_markdown(latest_step.get('netChangeType', 'N/A'))
        # FIX: Apply formatting, then escape the result
        change_formatted = f"{change:.2f}"
        pnl_text = f"Net Change: *{change_type} of \\${escape_markdown(change_formatted)}*"

    else: # Default for OPEN_SHORT_PUT or unrecognized step
        credit = safe_float_local(latest_step.get('grossProfitLossAmount', 'N/A'))
        # FIX: Apply formatting, then escape the result
        credit_formatted = f"{credit:.2f}"
        pnl_text = f"Realized Options P/L: *\\+\\${escape_markdown(credit_formatted)}*" if credit != 0.0 else "" # FIXED '+' ESCAPING

    # Define the escaped separator line once for the reserved hyphens
    ESCAPED_SEPARATOR = escape_markdown("-----------------------------------------")

    message = (
        f"🔔 *TRADE MANAGEMENT: {ticker}* 🔔\n\n"
        f"🔄 *Event Type:* {step_type}\n"
        f"📅 *Date:* {date}\n"
        f"📝 *Action:* {action}\n"
        f"{ESCAPED_SEPARATOR}\n"
        f"{pnl_text}\n"
        f"{ESCAPED_SEPARATOR}\n"
    )

    if notes:
        message += f"\n*Notes/Rationale:*\n_{notes}_\n"

    # Permalink
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")
    message += (
        f"\n[View Full Progression on Kahveci Nexus]({STATIC_DOC_URL})"
    )

    return message

def format_initial_alert(data):
    """Formats a Telegram message for a brand new trade idea (OPEN)."""

    trade_title = escape_markdown(data.get('tradeTitle', 'New Trade Idea'))
    ticker = escape_markdown(data.get('ticker', 'N/A'))

    # Prices and percentages must be converted to string, then escaped
    current_price_str = escape_markdown(safe_float(data.get('currentPrice', 'N/A')))
    pop_str = escape_markdown(safe_float(data.get('analysis', {}).get('metrics', {}).get('pop', 'N/A')))
    max_profit_str = escape_markdown(safe_float(data.get('analysis', {}).get('tradeDetails', {}).get('maxProfit', 'N/A')))

    expected_return = escape_markdown(data.get('expectedReturnDisplay', 'N/A'))
    summary_justification = escape_markdown(data.get('summaryJustification', 'No summary provided.'))
    publication_date = escape_markdown(data.get('publicationDate', 'YYYY-MM-DD'))

    analysis = data.get('analysis', {})
    strategy = escape_markdown(analysis.get('strategyType', 'N/A'))
    trade_details = analysis.get('tradeDetails', {})
    spread_details = trade_details.get('spreadDetails', {})
    expiration = escape_markdown(trade_details.get('expiration', 'N/A'))
    management = escape_markdown(analysis.get('managementPlan', 'Standard management plan.'))

    # Dynamic Strike Price Generation (Updated with escaping)
    s_put = escape_markdown(spread_details.get('shortPutStrike', 'N/A'))
    s_call = escape_markdown(spread_details.get('shortCallStrike', 'N/A'))

    strike_line = ""
    if strategy in [escape_markdown('Short Put'), escape_markdown('Cash-Secured Put')]:
        strike_line = f"🎯 *Short Put Strike:* *\\${s_put}*"
    elif strategy in [escape_markdown('Short Strangle'), escape_markdown('Iron Condor'), escape_markdown('Skewed Iron Condor'), escape_markdown('Delta-Skewed Short Iron Condor'), escape_markdown('Covered Short Strangle')]:
        strike_line = f"🎯 *Strikes (P/C):* *\\${s_put} / \\${s_call}*"
    else:
        strike_line = f"🎯 *Strikes:* See trade details"

    # Define the escaped separator line once for the reserved hyphens
    ESCAPED_SEPARATOR = escape_markdown("-----------------------------------------")

    # MESSAGE CONSTRUCTION (Using MarkdownV2 Bolding/Italics)
    message = (
        f"🚨 *NEW TRADE: {trade_title}* 🚨\n\n"
        f"📈 *Asset:* `{ticker}` (Current Price: \\${current_price_str})\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"📆 *Expiration:* {expiration} (Published: {publication_date})\n"
        f"{strike_line}\n"
        f"{ESCAPED_SEPARATOR}\n"
        f"✅ *Prob\\. of Profit (PoP):* *{pop_str}*\\%\n" # Escaping %
        f"💰 *Max Annualized ROC:* {expected_return}\n"
        f"💵 *Max Profit:* *\\${max_profit_str}*\n"
        f"{ESCAPED_SEPARATOR}\n"
        f"\n*Summary Justification:*\n"
        f"_{summary_justification}_\n\n"
        f"*Management Plan:*\n"
        f"_{management}_\n\n"
    )

    # Permalink
    STATIC_DOC_URL = escape_markdown("[https://kahveci.pw/trades/](https://kahveci.pw/trades/)")
    message += (
        f"\n[View Full Analysis on Kahveci Nexus]({STATIC_DOC_URL})"
    )

    return message

def format_telegram_message(data):
    """Determines if the alert is for a new trade or a management step."""

    progression = data.get('tradeProgression', [])

    if not progression:
        # No progression steps: must be a brand new trade open
        return format_initial_alert(data)
    else:
        # Progression steps exist: send alert for the LAST (latest) step
        return format_management_alert(data, progression[-1])

def send_telegram_notification(message):
    """Sends the formatted message via the Telegram API."""

    local_bot_token = os.environ.get('BOT_TOKEN')
    local_chat_id = os.environ.get('CHAT_ID')

    if not all([local_bot_token, local_chat_id]):
        print("Error: Missing BOT_TOKEN or CHAT_ID during function call. Check GitHub secrets.")
        raise ValueError("Missing Telegram BOT_TOKEN or CHAT_ID.")

    TELEGRAM_API_URL = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){local_bot_token}/sendMessage"

    payload = {
        'chat_id': local_chat_id,
        'text': message,
        'parse_mode': 'MarkdownV2'  # CRITICAL FIX: CHANGED TO MARKDOWNV2
    }

    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()
        print(f"Telegram notification sent successfully. Status: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        print(f"Error sending message to Telegram API: {e}")
        # Print the problematic payload text for debugging if it fails again
        print(f"Attempted Payload Text: {message}")
        print(f"Response Content: {response.text}")
        raise

if __name__ == "__main__":

    local_file_path = os.environ.get('FILE_PATH')

    if not all([os.environ.get('BOT_TOKEN'), os.environ.get('CHAT_ID'), local_file_path]):
        print("Setup error: One or more environment variables (secrets or file path) are missing.")
        sys.exit(1)

    try:
        top_trade = get_top_trade(local_file_path)

        if top_trade:
            # Format message based on whether it's an OPEN or a management step
            message = format_telegram_message(top_trade)
            send_telegram_notification(message)
        else:
            print("No valid trade data found to send notification.")
    except Exception as e:
        print(f"A final critical error occurred: {e}")
        sys.exit(1)