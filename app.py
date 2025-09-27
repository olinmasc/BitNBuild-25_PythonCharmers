import streamlit as st
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="Social Spark AI",
    page_icon="✨",
    layout="centered"
)

# --- App Title and Description ---
st.title("✨ Social Spark: AI Content Assistant")
st.write("Upload an image and let AI generate compelling social media content for you!")

# --- Image Upload ---
uploaded_file = st.file_uploader(
    "Choose an image to get started...",
    type=["jpg", "jpeg", "png"]
)

# --- Main Logic ---
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Uploaded Image", use_column_width=True)
    st.write("")

    with st.spinner("🤖 AI is thinking..."):
        # This is where you will call the functions from your teammates
        # For now, we'll use placeholders
        st.write("---")
        st.subheader("Your AI-Generated Content")

        # Placeholder for captions
        st.markdown("### ✒️ Captions")
        st.success("Witty: This is a placeholder for a witty caption!")
        st.info("Inspirational: This is a placeholder for an inspirational one!")

        # Placeholder for hashtags
        st.markdown("### #️⃣ Hashtags")
        st.code("#placeholder #AI #hackathon")
