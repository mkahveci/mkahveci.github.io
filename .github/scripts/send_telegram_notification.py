import os
import requests
import json
import re
import sys

# --- Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

# --- Helper Function for MarkdownV2 Escaping ---
def escape_markdown(text):
    """
    Escapes special characters in a string for Telegram's MarkdownV2 parse mode.
    """
    if text is None:
        return 'N/A'
    text = str(text)
    # Escape core reserved characters
    reserved_chars = r'([_*\[\]()~`>#+=\-|{}.!$])'
    # Use re.sub to escape the characters
    escaped_text = re.sub(reserved_chars, r'\\\1', text)
    return escaped_text

def get_top_trade(file_path):
    """Reads the JSON array and returns the first trade object."""
    try:
        with open(file_path, 'r') as f:
            data_array = json.load(f)
        if data_array and isinstance(data_array, list):
            return data_array[0]
        return None
    except Exception as e:
        print(f"Error reading local file: {e}")
        return None

def extract_trade_data(data):
    """Normalizes trade data for consistent key fields."""
    meta = data.get('meta', {})

    # Fallback logic for various JSON structures
    title = meta.get('tradeTitle') or data.get('tradeTitle') or 'New Trade Idea'
    ticker = meta.get('ticker') or data.get('ticker') or 'N/A'

    strat_details = data.get('strategyDetails', {})
    analysis = data.get('analysis', {})
    trade_details_old = analysis.get('tradeDetails', {})

    strategy = strat_details.get('type') or analysis.get('strategyType') or 'N/A'
    expiration = strat_details.get('expirationDate') or trade_details_old.get('expiration') or 'N/A'

    return {
        'title': title,
        'ticker': ticker,
        'strategy': strategy,
        'expiration': expiration
    }

def format_net_value_display(latest_step):
    """Formats the net change/credit value into an escaped Telegram string."""
    net_change = latest_step.get('netChange')
    net_credit = latest_step.get('netCredit')
    net_debit = latest_step.get('netDebit')

    # Prioritize netCredit/netDebit for clearer terminology, falling back to netChange
    if net_credit is not None:
         net_value = net_credit
         net_label = "Credit"
    elif net_debit is not None:
         net_value = -net_debit # Store debits as negative for consistent display logic
         net_label = "Debit"
    elif net_change is not None:
         net_value = net_change
         net_label = "Change"
    else:
        return escape_markdown('N/A'), escape_markdown('Change')

    # Format the net value (e.g., 104.00 -> $1.04)
    if isinstance(net_value, (int, float)):
        # Display as currency value / 100
        net_value_str = f"{abs(net_value) / 100.0:.2f}"

        if net_value > 0:
            prefix = "+" # Credit/Gain
        elif net_value < 0:
            prefix = "-" # Debit/Loss
        else:
            prefix = "" # Neutral

        net_value_display = escape_markdown(f"{prefix}${net_value_str}")

        # Adjust label for "Close" actions where net change often means P/L
        if latest_step.get('stepType', '').upper().startswith('CLOSE'):
             net_label = "P/L"
        elif net_credit is not None and net_debit is None:
             net_label = "Credit"
        elif net_debit is not None and net_credit is None:
             net_label = "Debit"


    else:
         net_value_display = escape_markdown(str(net_value))
         net_label = "Change"

    return net_value_display, escape_markdown(net_label)


def format_entry_alert(data, entry_step=None):
    """
    Formats a message for a NEW trade ENTRY, including execution details
    from the entry_step if available.
    """
    info = extract_trade_data(data)

    # Escape base data
    title = escape_markdown(info['title'])
    ticker = escape_markdown(info['ticker'])

    # Base data from general trade info (used if entry_step is missing)
    strategy_base = escape_markdown(info['strategy'])
    expiration_base = escape_markdown(info['expiration'])

    # Trade Execution Details (from the provided entry_step)
    if entry_step:
        step_type_raw = entry_step.get('stepType', 'Open Trade').replace('_', ' ')
        step_type = escape_markdown(step_type_raw)

        action_taken = escape_markdown(entry_step.get('actionTaken') or entry_step.get('action'))
        net_credit_display, net_label_display = format_net_value_display(entry_step)

        expiration_step = escape_markdown(entry_step.get('expiration'))
        dte_remaining = escape_markdown(str(entry_step.get('dteRemaining', 'N/A')))
        notes = escape_markdown(entry_step.get('notes'))

        # Use step-specific fields, fallback to base if step is missing data
        strategy_display = step_type
        expiration_display = expiration_step or expiration_base


        message = (
            f"🚨 *NEW TRADE ENTRY: {title}* 🚨\n\n"
            f"📈 *Asset:* `{ticker}`\n"
            f"🛠️ *Strategy:* {strategy_display}\n"
            f"📝 *Action:* `{action_taken}`\n"
            f"💰 *Net {net_label_display}:* {net_credit_display}\n"
            f"📆 *Expiration:* {expiration_display} \\(DTE: {dte_remaining}\\)\n\n"
            f"💡 *Notes:* {notes}"
        )

    # Fallback for V1 trade (no progression/steps)
    else:
        message = (
            f"🚨 *NEW TRADE: {title}* 🚨\n\n"
            f"📈 *Asset:* `{ticker}`\n"
            f"🛠️ *Strategy:* {strategy_base}\n"
            f"📆 *Expiration:* {expiration_base}\n"
        )

    # Static Links (Escaped) - appended to both entry and fallback
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")
    LINK_TEXT = escape_markdown("View Full Analysis on Kahveci Nexus")

    message += f"\n\n[{LINK_TEXT}]({STATIC_DOC_URL})"
    return message


# MODIFIED TO INCLUDE EXECUTION DETAILS
def format_management_alert(data, latest_step):
    """Formats a message for a trade UPDATE (Close, Roll, etc) with execution details."""
    info = extract_trade_data(data)
    ticker = escape_markdown(info['ticker'])

    # --- Step Data Extraction ---
    step_type_raw = latest_step.get('stepType', 'Update').replace('_', ' ')
    step_type = escape_markdown(step_type_raw)

    date = escape_markdown(latest_step.get('date', 'N/A'))

    # Action taken is the full description of the legs
    action_raw = latest_step.get('action') or latest_step.get('actionTaken') or 'N/A'
    action = escape_markdown(action_raw)

    # Net value formatting
    net_value_display, net_label_display = format_net_value_display(latest_step)

    # Adjustment/Management specific fields
    notes = escape_markdown(latest_step.get('notes'))

    # If the adjustment is a roll, the expiration will be present in the step
    expiration_step = escape_markdown(latest_step.get('expiration', 'N/A'))
    dte_remaining = escape_markdown(str(latest_step.get('dteRemaining', 'N/A')))

    # --- Message Construction ---
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")
    LINK_TEXT = escape_markdown("View Full Progression on Kahveci Nexus")


    message = (
        f"🔔 *TRADE MANAGEMENT: {ticker}*\n\n"
        f"🔄 *Event Type:* {step_type}\n"
        f"📅 *Date:* {date}\n"
        f"📝 *Action:* `{action}`\n"
    )

    # Only include net value if it's not 'N/A'
    if net_value_display != escape_markdown('N/A'):
        message += f"💰 *Net {net_label_display}:* {net_value_display}\n"

    # Only include expiration fields if they are available (i.e., for a Roll)
    if expiration_step != escape_markdown('N/A'):
         message += f"📆 *New Expiration:* {expiration_step} \\(DTE: {dte_remaining}\\)\n"

    if notes != escape_markdown('N/A'):
         message += f"\n💡 *Notes:* {notes}\n"

    message += f"\n[{LINK_TEXT}]({STATIC_DOC_URL})"
    return message

def format_telegram_message(data):
    """Decides which message format to use based on trade progression."""
    progression = data.get('tradeProgression', [])

    entry_types = [
        'OPEN_TRADE', 'OPEN_SHORT_PUT', 'OPEN_LONG_CALL_CALENDAR',
        'OPEN_SHORT_STRANGLE', 'OPEN_IRON_CONDOR', 'OPEN_SHORT_VERTICAL',
    ]

    # If no progression, it's a new V1 trade (use entry format without step data)
    if not progression:
        return format_entry_alert(data)

    last_step = progression[-1]
    step_type = last_step.get('stepType', '').upper()

    # If the last step is an entry, use the dedicated entry alert
    if step_type in entry_types:
        return format_entry_alert(data, entry_step=last_step)

    # Otherwise, it is an Adjustment/Management Alert
    return format_management_alert(data, last_step)

def send_telegram_notification(message):
    """Sends the actual HTTP request."""
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Missing BOT_TOKEN or CHAT_ID.")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'MarkdownV2'
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Telegram notification sent successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"Error sending to Telegram: {e}")
        print(f"Response: {response.text}")
        raise

if __name__ == "__main__":
    if not all([BOT_TOKEN, CHAT_ID, FILE_PATH]):
        print("Setup error: Missing BOT_TOKEN, CHAT_ID, or FILE_PATH environment variables.")
        sys.exit(1)

    try:
        top_trade = get_top_trade(FILE_PATH)
        if top_trade:
            msg = format_telegram_message(top_trade)
            send_telegram_notification(msg)
        else:
            print("No valid trade data found.")
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)