# Allows users to change notification settings


import streamlit as st
import json
import os

# file to store user preferences
SETTINGS_FILE = os.path.join("..", "data", "user_settings.json")


# load or initialize settings
def load_settings():
    default_settings = {
        "enable_notifications": True,
        "notification_interval": 30,  # in minutes
        "enable_distress_alerts": False,  # <- Add this line
        "channels": {
            "email": False,
            "desktop": True,
            "sms": False
        }
    }

    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    # Load and merge existing settings with defaults (to handle updates gracefully)
    with open(SETTINGS_FILE, "r") as f:
        current_settings = json.load(f)

    # Add missing keys if settings file is old or partial
    for key, val in default_settings.items():
        if key not in current_settings:
            current_settings[key] = val

    save_settings(current_settings)  # Update with missing defaults
    return current_settings


settings = load_settings()

def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


st.set_page_config(page_title="Notification Settings", layout="centered")
st.title("Manage Your Notifications")

# load settings
settings = load_settings()

# UI toggles
st.subheader("Notification Preferences")
settings["enable_distress_alerts"] = st.toggle("Alert me when signs of distress are detected", value=settings["enable_distress_alerts"])
settings["enable_daily_reminder"] = st.toggle("Send me daily dashboard check-in notifications", value=settings["enable_daily_reminder"])

# save button
if st.button("Save Preferences"):
    save_settings(settings)
    st.success("Preferences saved successfully!")

# display current settings
st.markdown("---")
st.write("### Current Settings")
st.json(settings)

st.markdown("---")
st.info("You can always come back here to update your notification preferences.")
