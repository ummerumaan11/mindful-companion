import streamlit as st
import pandas as pd
import altair as alt

from crisis_detection import is_crisis_message, CRISIS_RESPONSE
from responses import find_topic, FALLBACK_RESPONSES, GREETING, TOPICS
from database import init_db, add_mood_entry, get_mood_history, add_journal_entry, get_journal_entries

st.set_page_config(page_title="Mindful Companion", page_icon="🌱", layout="centered")
init_db()

# ---------- Disclaimer (always visible) ----------
st.title("🌱 Mindful Companion")
st.warning(
    "**This is a student/portfolio project, not a licensed mental health service.** "
    "It cannot diagnose, treat, or provide therapy, and its responses are rule-based, not clinical advice. "
    "If you're struggling, please reach out to a real person — a doctor, therapist, or someone you trust.",
    icon="⚠️",
)

with st.sidebar:
    st.header("Emergency")
    st.markdown("**India:** Call **112**")
    st.divider()
    st.caption("These resources are always available here, regardless of what you type.")

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": GREETING}]
if "in_crisis_mode" not in st.session_state:
    st.session_state.in_crisis_mode = False

tab_chat, tab_mood, tab_journal = st.tabs(["Chat", "Mood tracker", "Journal"])

# ---------- Chat tab ----------
with tab_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("What's on your mind?")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Crisis check ALWAYS runs first and overrides everything else.
        if is_crisis_message(user_input):
            reply = CRISIS_RESPONSE
            st.session_state.in_crisis_mode = True
        else:
            topic_id, topic = find_topic(user_input)
            if topic:
                reply = f"{topic['acknowledgment']}\n\nHere's a technique that might help — **{topic['technique_name']}**:\n\n{topic['technique']}"
            else:
                import random
                reply = random.choice(FALLBACK_RESPONSES)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.in_crisis_mode:
        st.info("Crisis resources are shown in the sidebar and stay available throughout this conversation.")

# ---------- Mood tracker tab ----------
with tab_mood:
    st.subheader("How are you feeling right now?")
    mood = st.slider("Mood (1 = very low, 10 = very good)", 1, 10, 5)
    note = st.text_input("Anything you want to note about why? (optional)")
    if st.button("Log mood"):
        add_mood_entry(mood, note)
        st.success("Logged.")
        st.rerun()

    history = get_mood_history()
    if history:
        df = pd.DataFrame(history)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.subheader("Your mood over time")
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("timestamp:T", title="Date"),
            y=alt.Y("mood_score:Q", title="Mood", scale=alt.Scale(domain=[1, 10])),
            tooltip=["timestamp:T", "mood_score:Q", "note:N"],
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.caption("No entries yet — log your first mood check-in above.")

# ---------- Journal tab ----------
with tab_journal:
    st.subheader("Write a journal entry")
    entry_text = st.text_area("What's on your mind? This is just for you.", height=150)
    if st.button("Save entry") and entry_text.strip():
        add_journal_entry(entry_text.strip())
        st.success("Saved.")
        st.rerun()

    st.divider()
    st.subheader("Past entries")
    entries = get_journal_entries()
    if not entries:
        st.caption("No journal entries yet.")
    else:
        for e in entries:
            with st.expander(e["timestamp"][:19].replace("T", " ")):
                st.write(e["text"])
