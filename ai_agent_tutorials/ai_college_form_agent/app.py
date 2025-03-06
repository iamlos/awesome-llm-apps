import streamlit as st
from crew import run_crew

# Streamlit UI
st.set_page_config(page_title="College Recruiting Form Filler", layout="wide")

st.title("🏆 College Recruiting Form Filler")
st.markdown("**Automatically find and fill recruiting forms for athletes!**")

# User input for college and sport
college = st.text_input("Enter College Name", "")
sport = st.text_input("Enter Sport", "")

if st.button("Start Process"):
    if college and sport:
        st.info(f"🔎 Searching for {college}'s {sport} recruiting form...")
        result = run_crew(college, sport)
        st.success("✅ Process Completed!")
        st.subheader("📌 Submission Report")
        st.markdown(result)  # Display CrewAI output
    else:
        st.warning("⚠️ Please enter both College Name and Sport.")

st.markdown("---")
st.caption("Powered by CrewAI & Streamlit")
