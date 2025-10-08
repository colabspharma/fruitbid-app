# =====================================================
# ⚙️ utils/common.py — Common Utilities for FruitBid
# =====================================================

import streamlit as st
import re
import os
import bcrypt
import requests
from db_utils import get_setting  # ✅ assuming you renamed db.py → db_utils.py


# =====================================================
# 📞 VALIDATION HELPERS
# =====================================================
def validate_mobile(val: str) -> bool:
    """✅ Validate Indian mobile number format (+91XXXXXXXXXX)."""
    return bool(re.fullmatch(r"\+91\d{10}", val or ""))


def validate_email(val: str) -> bool:
    """✅ Validate email format (basic RFC compliant)."""
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}", val or ""))


# =====================================================
# 🔐 ADMIN PASSWORD CHECK
# =====================================================
def check_admin_password(password: str) -> bool:
    """
    ✅ Compare entered admin password with the stored hash.
    Note: Hash should be stored in environment or DB, not re-generated each time.
    """
    stored_hash = os.getenv("ADMIN_PASSWORD_HASH")

    # If no pre-stored hash exists, create one temporarily (development fallback)
    if not stored_hash:
        temp_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        os.environ["ADMIN_PASSWORD_HASH"] = temp_hash.decode()
        stored_hash = temp_hash.decode()

    try:
        return bcrypt.checkpw(password.encode(), stored_hash.encode())
    except Exception:
        return False


# =====================================================
# 💰 PRICE FETCHING (MOCKED REAL-TIME)
# =====================================================
def fetch_real_time_price(item: str) -> float:
    """
    ✅ Fetch real-time market price.
    Replace with actual API integration later.
    """
    try:
        # Example placeholder for API request
        # response = requests.get(f"https://api.example.com/price?item={item}", timeout=5)
        # if response.status_code == 200:
        #     return float(response.json().get("price", 100))

        # Fallback mock data
        MARKET_PRICES = {
            "Apple": 200,
            "Mosambi": 50,
            "Banana": 40,
            "Papaya": 50,
            "Kiwi": 200,
            "Dragon Fruit": 250,
            "Pineapple": 60,
            "Custard Apple": 100,
            "Sapota": 60,
            "Mango": 120,
            "Spinach": 30,
            "Honey": 300,
        }
        return float(MARKET_PRICES.get(item, 100))
    except Exception as e:
        st.warning(f"⚠️ Price API error: {e}. Using fallback ₹100.")
        return 100.0


# =====================================================
# 🧮 PRICE MONITOR (WITH DISCOUNT)
# =====================================================
@st.cache_data(ttl=60)
def monitor_prices(item: str) -> float:
    """
    ✅ Calculate item price after applying discount.
    Cached for 1 minute (60s) for performance.
    """
    market_price = fetch_real_time_price(item)
    try:
        discount = float(get_setting("discount_pct", 20))
    except Exception:
        discount = 20.0

    final_price = market_price * (1 - discount / 100)
    return round(final_price, 2)
