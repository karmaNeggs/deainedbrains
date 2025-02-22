import os
import streamlit as st
from PIL import Image
import pytesseract
from openai import OpenAI

# Optional: Configure Streamlit page
st.set_page_config(
    page_title="Drained Brains",
    layout="centered"
)

# Load your OpenAI key securely (Render, local env, etc.)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# --- TOP SECTION: TITLE, INTRO, QUICK LINKS ---
st.markdown("<h1 style='text-align: center;'>Drained Brains</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Together for better care of our elders back home")
    st.caption("A caption Some description lorem ipsum about Drained Brains... _italics_ :blue[colors] and emojis :sunglasses:\n\n ")
    st.session_state.show_newsletter_form = False

    if st.button("Get our Newsletter"):
        st.session_state.show_newsletter_form = True
   
with col2:    
    col2a, col2b = st.columns(2)
    with col2b:
        st.caption(" \n\n Check Our :green[Toolkit] :sunglasses:")
        st.link_button("Community", "https://www.reddit.com/r/drainedbrains/", icon="👩🏼‍❤️‍👨🏻", type="secondary", disabled=False, use_container_width=False)
        st.link_button("Med Check", "#prescription-check", icon="🔍", type="secondary", disabled=False, use_container_width=False)
        st.link_button("Resources", "#resources", icon="📚", type="secondary", disabled=False, use_container_width=False)

# -------------------------------------------------------
# FUNCTION: Renders the Newsletter Form
# -------------------------------------------------------

@st.dialog(" ")
def render_newsletter_form():

    st.markdown("Hello 👋, Subscribe for Reliable info")
    email = st.text_input("Enter your email:")

    if st.button("Subscribe"):
        add_email_to_sheet(email)
        st.success("Thank you for subscribing!")
        st.session_state.show_newsletter_form = False

def add_email_to_sheet(email):
    pass


st.write("---")

if st.session_state.show_newsletter_form:
    render_newsletter_form()

# --- PRESCRIPTION CHECKER SECTION ---
st.subheader("Prescription Check")
st.write("Summarize your symptoms and enter exact prescription (with dosage) in detail:")

prescription_text = st.text_area("Prescription Text (please mask personal details):")
uploaded_image = st.file_uploader(
    "Optional: Upload prescription image (crop out names)",
    type=["jpg", "jpeg", "png", "HEIC", "heic"]
)

if st.button("Submit"):
    # (1) Extract text from image if provided
    prescription_scan = ""
    if uploaded_image:
        image = Image.open(uploaded_image)
        try:
            prescription_scan = pytesseract.image_to_string(image)
        except Exception as e:
            st.write("**Prescription scanning error**")

    st.write("**Extracted Prescription**:")
    st.write(f"From text input:\n{prescription_text}")
    st.write(f"From image:\n{prescription_scan}")

    # (2) Build your prompt
    prompt = (
        f"Prescription:\n{prescription_text}\n\n"
        f"Prescription reference read from image (unreliable):\n{prescription_scan}"
    )

    # (3) Call your LLM
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert mental health practitioner that checks if a prescription for Geriatric mental health makes sense with. make sure to respond succinctly and only about the prescriptions as follows: (1. Report if there is a fault in prescription, any critical issues like medicines on wrong time, too much quantity or incompatible with symptoms if provided. (2. Report if there is an addiction causing medicine or major side effects causing drug. (3. Report if image or text is unreadable and ask for text input if not clear"},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",
        )

        result = chat_completion.choices[0].message.content.strip()

        st.write("Results:")
        st.write(result)

    except Exception as e:
        st.error(f"Error calling the AI API: {e}")

st.write("---")




# --- DIRECTORIES & RESOURCES ---


col1_directory, col_resources = st.columns(2)
with col1_directory:
    st.subheader("Doctors Directory")
    st.markdown("- [iCALL's crowdsourced list of Mental Health Professionals We Can Trust (23rd April 2021)](https://docs.google.com/spreadsheets/u/2/d/1pzckT6ns2H1IlmwYwJa8EnBh_1u3gRA9cEOoA4zfilc/htmlview#)")
    st.markdown("- [iCALL's Helpline](https://icallhelpline.org/)")
    st.markdown("- [Therapists listing](https://themindclan.com/professionals/)")
    st.markdown("- [IACP directory](https://iacp.in/wp-content/uploads/2022/01/directory.pdf)")

with col_resources:
    st.subheader("Resources")
    st.markdown("- [Essential elder care checklist](https://www.talkspace.com/blog/aging-parents-checklist/)")
    st.markdown("- [Know your nedical prescription](https://www.1mg.com/articles/know-your-medical-prescription/?srsltid=AfmBOopqxCbk5Kph2oWEQfnQvSvAwuZSTpOzHJ-MPBspQr9JhQ6J59b8)")
    st.markdown("- [Blog article 3](https://example.com)")
    st.markdown("- [Blog article 4](https://example.com)")

st.write("---")

# --- ABOUT SECTION ---
st.subheader("About Us")
st.write(
    "At our core, we believe that the mental well-being of our elders matters—and it’s time we stand up for \n"
    "Welcome to our community. We are a passionate movement dedicated to transforming the mental health care of our beloved elders. Born from personal heartbreak and lived experience, we know too well the devastating impact of neglect, misprescription, and isolation on our parents—our pillars of strength. When those who cared for us are left to suffer in silence, it ignites an anger we simply cannot ignore 😡.\n"
    "Our mission is clear: to offer accessible, reliable, and compassionate medical support for geriatric mental health. We empower you with a comprehensive toolkit featuring a second opinion checker and a checklist to monitor everyday well-being, alongside our thought-provoking book, Un-subscription Society. Stay informed and connected through our channels on Reddit, Instagram, Facebook, and TikTok—where expert advice meets heartfelt stories.\n"
    "Whether you’re balancing a career while caring for aging parents or supporting them from afar as an NRI, you’re not alone. With our support bot, engaging newsletter, and anonymous case broadcasts, we’re here to help you reclaim dignity and spark the change our parents deserve ❤️. Join us, and together, let’s revolutionize care for those who gave us everything."
)

# --- SOCIAL ICONS / LINKS ---
st.subheader("Connect with us:")
st.markdown("""
[![Reddit](https://static-00.iconduck.com/assets.00/reddit-icon-256x256-7e3aoes6.png)](https://www.reddit.com/r/drainedbrains/)
[![Instagram](https://images.freeimages.com/image/thumbs/dcb/instacam-story-button-png-5690392.png)](https://example.com)
""")

# --- FOOTER LINKS ---
st.write("---")
st.markdown("[RESOURCES](https://example.com) | [About us](https://example.com) | [Blog](https://example.com) | [Disclaimers](https://example.com) | [T & C](https://example.com)")
