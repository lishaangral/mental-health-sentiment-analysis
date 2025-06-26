import streamlit as st
import threading
import os
import json

from screen_monitor import get_open_windows, start_monitoring

SETTINGS_FILE = "../data/user_settings.json"

st.set_page_config(page_title="Monitor Settings", layout="centered")
st.title("Real-Time Monitor Settings")

# --- Load user preferences ---
def load_user_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

# --- Save user preferences ---
def save_user_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# Load settings
user_settings = load_user_settings()
whitelisted_apps = user_settings.get("whitelisted_apps", [])
monitoring_enabled = user_settings.get("monitoring_enabled", False)
log_retention_days = user_settings.get("log_retention_days", 7)

# --- App whitelist section ---
st.subheader("Select Applications to Monitor")

windows = get_open_windows()
if not windows:
    st.error("⚠️ No active windows detected. Please open some apps.")
else:
    selected_apps = st.multiselect(
        "Choose apps to whitelist",
        windows,
        default=whitelisted_apps
    )

    if selected_apps != whitelisted_apps:
        user_settings["whitelisted_apps"] = selected_apps
        save_user_settings(user_settings)
        st.success("✅ App preferences saved.")

# --- Toggle for enabling/disabling monitoring ---
st.markdown("---")
st.subheader("Monitoring Toggle")
monitor_toggle = st.toggle("Enable Monitoring", value=monitoring_enabled)

if "monitoring" not in st.session_state:
    st.session_state.monitoring = monitoring_enabled
if "stop_flag" not in st.session_state:
    st.session_state.stop_flag = {"stop": not monitoring_enabled}

if monitor_toggle and not st.session_state.monitoring:
    st.session_state.stop_flag = {"stop": False}
    st.session_state.monitoring = True
    user_settings["monitoring_enabled"] = True
    save_user_settings(user_settings)
    st.success("✅ Monitoring started.")
    threading.Thread(
        target=start_monitoring,
        args=(selected_apps, st.session_state.stop_flag),
        daemon=True
    ).start()

elif not monitor_toggle and st.session_state.monitoring:
    st.session_state.stop_flag["stop"] = True
    st.session_state.monitoring = False
    user_settings["monitoring_enabled"] = False
    save_user_settings(user_settings)
    st.warning("⛔ Monitoring stopped.")

# --- Log Retention Settings ---
st.markdown("---")
with st.expander("🗑️ Log Retention Settings", expanded=False):
    retention_days = st.slider(
        "Days to keep prediction logs",
        min_value=1,
        max_value=30,
        value=log_retention_days,
        help="Older logs will be deleted automatically on app start."
    )
    if retention_days != log_retention_days:
        user_settings["log_retention_days"] = retention_days
        save_user_settings(user_settings)
        st.success(f"✅ Log retention updated to {retention_days} day(s).")

# --- Footer Caption ---
st.markdown("---")
st.caption("This system analyzes your screen every 10 seconds and logs detected sentiments only from selected apps.")
