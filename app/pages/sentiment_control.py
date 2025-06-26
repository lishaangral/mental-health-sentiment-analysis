import streamlit as st
import time

st.set_page_config(page_title="Sentiment Control", layout="wide")
st.title("🧘 Sentiment Control Hub")
st.markdown("Feeling overwhelmed or low? Take a moment to try one of these proven mood-balancing resources.")

# ---------------- Breathing Timer ----------------
st.subheader("🌬️ Guided Breathing Timer")

with st.expander("▶️ Start a 4-7-8 Breathing Cycle (Box Breathing)"):
    breath_phase = st.radio("Choose a phase to practice:", ["4-7-8 Breathing", "Box Breathing"])
    breath_cycles = st.slider("Number of cycles", 1, 5, 3)

    if st.button("Start Breathing"):
        for cycle in range(breath_cycles):
            st.write(f"🟢 Inhale... (4s)")
            time.sleep(4)
            st.write(f"🟡 Hold... (7s)" if breath_phase == "4-7-8 Breathing" else "🟡 Hold... (4s)")
            time.sleep(7 if breath_phase == "4-7-8 Breathing" else 4)
            st.write(f"🔵 Exhale... (8s)" if breath_phase == "4-7-8 Breathing" else "🔵 Exhale... (4s)")
            time.sleep(8 if breath_phase == "4-7-8 Breathing" else 4)
        st.success("✅ Breathing session complete!")

st.divider()

# ---------- Layout ----------
col1, col2 = st.columns(2)

# --------- Breathing Exercises ----------
with col1:
    st.subheader("🌬️ Breathing Exercises")
    st.video("https://www.youtube.com/watch?v=inpok4MKVLM", format="video/mp4")
    st.write("A quick and effective **5-minute breathing exercise** to help you reset your nervous system.")

    st.video("https://www.youtube.com/watch?v=8lB59zuw6Wk")
    st.write("Try this **box breathing technique** to improve focus and reduce anxiety.")

# --------- Calming Sounds ----------
with col2:
    st.subheader("🎧 Calming Sounds")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    st.write("Relax with some **ambient nature sounds** to calm your thoughts.")

    st.markdown("[🎵 Soothing Rain Sound (YouTube)](https://www.youtube.com/watch?v=e6j6iEbKXkM)")
    st.markdown("[🎵 Piano & Ocean Waves](https://www.youtube.com/watch?v=1ZYbU82GVz4)")

# ---------- Divider ----------
st.divider()
col3, col4 = st.columns(2)

# --------- Distraction / Entertainment ----------
with col3:
    st.subheader("🎬 Light-Hearted Distractions")
    st.video("https://www.youtube.com/watch?v=3eTOcrWuQ9M", format="video/mp4")
    st.caption("Pixar Short: Piper")

    st.video("https://www.youtube.com/watch?v=hzfH9aaKmmc", format="video/mp4")
    st.caption("Funny Animal Compilation")

    st.video("https://www.youtube.com/embed/videoseries?list=PLhSp9OSVmeyKQ3vMWVRPLdK6zVP7P-7jV")
    st.caption("Positive News Highlights Playlist")

with col4:
    st.subheader("🧠 Mindfulness & Refocus")

    st.video("https://www.youtube.com/watch?v=wGFog-OuFDM", format="video/mp4")
    st.caption("Mindfulness Bell Timer")

    st.markdown("🌳 [Headspace Guide to Meditation (Netflix)](https://www.netflix.com/title/81280926)")
    st.markdown("🧘 [Calm App - Meditations, Sleep, Focus](https://www.calm.com)")

st.markdown("---")
st.success("✅ Feel free to explore any of these resources whenever you need a break. Your well-being matters.")
