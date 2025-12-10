import os
import requests
import json
import re
import sys

# --- Configuration (Kept for completeness) ---
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

# NEW HELPER FUNCTION TO GET REALIZED P/L
def format_realized_pnl_display(latest_step):
    """
    Attempts to find the final realized P/L, preferring a direct field
    or parsing the notes, and formats it for display.
    """
    # 1. Check for a direct field (e.g., if JSON structure includes it)
    pnl_value = latest_step.get('realizedPNL')
    pnl_label = "P/L"

    # 2. If not found, attempt to parse the notes field
    notes = latest_step.get('notes', '')
    pnl_match = re.search(r'\(\$([\d\.\,]+) realized (gain|loss)\)', notes, re.IGNORECASE)

    if pnl_match:
        # Extract the number and determine sign
        pnl_str = pnl_match.group(1).replace(',', '')
        pnl_value = float(pnl_str)

        # If it's a loss, make the value negative
        if pnl_match.group(2).lower() == 'loss':
            pnl_value = -pnl_value

        pnl_label = "Realized P/L"

    # 3. Fallback to transaction net change (as cents)
    elif latest_step.get('netChange') is not None or latest_step.get('netCredit') is not None:
        return format_transaction_net_value_display(latest_step)


    # 4. Format the final realized P/L value
    if isinstance(pnl_value, (int, float)):
        # Display as currency value (NO division by 100 for realized P/L)
        net_value_str = f"{abs(pnl_value):.2f}"

        if pnl_value > 0:
            prefix = "+"
        elif pnl_value < 0:
            prefix = "-"
        else:
            prefix = ""

        net_value_display = escape_markdown(f"{prefix}${net_value_str}")

    else:
        # Final fallback if parsing failed
        net_value_display = escape_markdown('N/A')
        pnl_label = "Change"

    return net_value_display, escape_markdown(pnl_label)

def format_transaction_net_value_display(latest_step):
    """
    Formats the net credit/debit value of the *transaction* (used for Entry/Roll).
    Values are assumed to be in cents and displayed as currency.
    """
    net_change = latest_step.get('netChange')
    net_credit = latest_step.get('netCredit')
    net_debit = latest_step.get('netDebit')

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

    # Format the net value (dividing by 100 for transaction price)
    if isinstance(net_value, (int, float)):
        net_value_str = f"{abs(net_value) / 100.0:.2f}"

        if net_value > 0:
            prefix = "+"
        elif net_value < 0:
            prefix = "-"
        else:
            prefix = ""

        net_value_display = escape_markdown(f"{prefix}${net_value_str}")
    else:
         net_value_display = escape_markdown(str(net_value))

    return net_value_display, escape_markdown(net_label)

# ... (format_entry_alert remains the same as it uses format_transaction_net_value_display)

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
        # Use transaction net value for Entry
        net_credit_display, net_label_display = format_transaction_net_value_display(entry_step)

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


# REVISED format_management_alert
def format_management_alert(data, latest_step):
    """Formats a message for a trade UPDATE (Close, Roll, etc) with execution details."""
    info = extract_trade_data(data)
    ticker = escape_markdown(info['ticker'])

    # --- Step Data Extraction ---
    step_type_raw = latest_step.get('stepType', 'Update').replace('_', ' ')
    step_type_upper = latest_step.get('stepType', '').upper()
    step_type = escape_markdown(step_type_raw)

    date = escape_markdown(latest_step.get('date', 'N/A'))

    # Action taken is the full description of the legs
    action_raw = latest_step.get('action') or latest_step.get('actionTaken') or 'N/A'
    action = escape_markdown(action_raw)

    # Net value formatting: Use Realized P/L for CLOSES, use Transaction Net Value otherwise
    if step_type_upper.startswith('CLOSE'):
        net_value_display, net_label_display = format_realized_pnl_display(latest_step)
    else:
        net_value_display, net_label_display = format_transaction_net_value_display(latest_step)

    # Adjustment/Management specific fields
    notes = escape_markdown(latest_step.get('notes'))

    # Conditional Expiration details
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

    # Include net value
    if net_value_display != escape_markdown('N/A'):
        message += f"💰 *Net {net_label_display}:* {net_value_display}\n"

    # Only include expiration fields for non-Closing actions, or if it's explicitly a Roll
    if step_type_upper.startswith('ROLL') or (step_type_upper != 'CLOSE' and expiration_step != escape_markdown('N/A')):
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