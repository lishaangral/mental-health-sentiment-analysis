import streamlit as st
import json
import os

# File to store user preferences
SETTINGS_FILE = "../data/user_settings.json"

# Load or initialize settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "enable_distress_alerts": True,
            "enable_daily_reminder": True
        }

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

st.set_page_config(page_title="Notification Settings", layout="centered")
st.title("Manage Your Notifications")

# Load settings
settings = load_settings()

# UI toggles
st.subheader("Notification Preferences")
settings["enable_distress_alerts"] = st.toggle("Alert me when signs of distress are detected", value=settings["enable_distress_alerts"])
settings["enable_daily_reminder"] = st.toggle("Send me daily dashboard check-in notifications", value=settings["enable_daily_reminder"])

# Save button
if st.button("Save Preferences"):
    save_settings(settings)
    st.success("Preferences saved successfully!")

# Display current settings
st.markdown("---")
st.write("### Current Settings")
st.json(settings)

st.markdown("---")
st.info("You can always come back here to update your notification preferences.")
