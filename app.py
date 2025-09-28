import streamlit as st
from PIL import Image
import time
from vision import analyze_image
from language import generate_content
import google.generativeai as genai  # <-- ADD THIS IMPORT

# --- API KEY CONFIGURATION ---
# This block reads the secret key from the Streamlit dashboard
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except (KeyError, FileNotFoundError):
    st.error("❌ Error: GOOGLE_API_KEY is not set in Streamlit secrets.")
    st.info("Please add your Google API key to the Streamlit secrets manager.")
    st.stop()  # Stops the app from running further if the key is not found
# -----------------------------

# --- Page Configuration ---
st.set_page_config(
    page_title="Social Spark AI",
    page_icon="✨",
    layout="wide"
)

# --- Custom CSS for better styling ---
st.markdown("""
<style>
    /* Force dark theme for better visibility */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 3rem;
    }
    .main-header p {
        color: #f0f0f0 !important;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    
    .feature-box {
        background: #1E2130 !important;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #FFFFFF !important;
    }
    .feature-box h4 {
        color: #FFFFFF !important;
        margin-bottom: 0.5rem;
    }
    .feature-box p {
        color: #CCCCCC !important;
    }
    
    .content-section {
        background: #1E2130 !important;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        margin: 1rem 0;
        color: #FFFFFF !important;
    }
    .content-section h3, .content-section h4, .content-section p {
        color: #FFFFFF !important;
    }
    
    .success-banner {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white !important;
        text-align: center;
        margin: 1rem 0;
    }
    .success-banner h3 {
        color: white !important;
    }
    
    /* Fix all Streamlit text elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #FFFFFF !important;
    }
    
    /* Fix file uploader text */
    .stFileUploader label {
        color: #FFFFFF !important;
    }
    
    /* Fix tab text */
    .stTabs [data-baseweb="tab-list"] button {
        color: #FFFFFF !important;
    }
    
    /* Fix info boxes */
    .stAlert {
        background-color: #1E2130 !important;
        color: #FFFFFF !important;
    }
    
    /* Fix footer text */
    .footer-text {
        color: #CCCCCC !important;
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div class="main-header">
    <h1>✨ Social Spark: AI Content Assistant</h1>
    <p>Transform your images into engaging social media content with AI-powered creativity!</p>
</div>
""", unsafe_allow_html=True)

# --- Features Section ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 Smart Analysis</h4>
        <p>AI analyzes your image for objects, mood, and themes</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🎨 Multi-Tone Captions</h4>
        <p>Get witty, inspirational, professional, and casual options</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>#️⃣ Trending Hashtags</h4>
        <p>Relevant and trending hashtags for maximum reach</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h4>📊 Mood Analysis</h4>
        <p>Understanding your image's emotional impact</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Content Area ---
st.write("---")

# --- Image Upload Section ---
uploaded_file = st.file_uploader(
    "📤 **Choose an image to get started...**",
    type=["jpg", "jpeg", "png"],
    help="Upload JPG, JPEG, or PNG files (max 200MB)"
)

# --- Main Logic ---
if uploaded_file is not None:
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Uploaded Image", use_column_width=True)

        # Image info
        st.write(f"**File name:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size / 1024:.1f} KB")
        st.write(f"**Image dimensions:** {image.size[0]} x {image.size[1]}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)

        # Processing section
        if st.button("🚀 Generate Content Package", type="primary", use_container_width=True):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Step 1: Analyze the image
            status_text.text("🔍 Analyzing your image...")
            progress_bar.progress(25)
            time.sleep(1)

            description = analyze_image(uploaded_file)

            if description.startswith("Error"):
                st.error(f"❌ Image Analysis Failed: {description}")
            else:
                progress_bar.progress(50)
                status_text.text("🎨 Generating creative content...")
                time.sleep(1)

                # Step 2: Generate content based on the description
                content_package = generate_content(description)

                if content_package.startswith("Error"):
                    st.error(f"❌ Content Generation Failed: {content_package}")
                else:
                    progress_bar.progress(100)
                    status_text.text("✅ Content package ready!")
                    time.sleep(1)

                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()

                    # Success message
                    st.markdown("""
                    <div class="success-banner">
                        <h3>🎉 Your AI-Generated Content Package is Ready!</h3>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Results section (full width)
    if 'content_package' in locals() and not content_package.startswith("Error"):
        st.write("---")
        st.markdown('<div class="content-section">', unsafe_allow_html=True)

        # Tabs for better organization
        tab1, tab2, tab3 = st.tabs(
            ["📝 Content Package", "🔍 Image Analysis", "💡 Usage Tips"])

        with tab1:
            st.markdown("### ✨ Your AI-Generated Content")
            st.markdown(content_package)

            # Copy button simulation
            st.info(
                "💡 **Tip:** You can select and copy any text above to use in your social media posts!")

        with tab2:
            st.markdown("### 🔍 AI Image Analysis")
            st.markdown(f"**Image Description:** {description}")

        with tab3:
            st.markdown("### 💡 How to Use Your Content Package")
            st.markdown("""
            **🎯 Quick Usage Guide:**
            
            1. **Choose Your Tone:** Pick the caption that matches your brand voice
            2. **Mix & Match:** Combine elements from different captions
            3. **Hashtag Strategy:** Use 5-10 hashtags for optimal reach
            4. **Timing Matters:** Post when your audience is most active
            5. **Engage:** Respond to comments to boost engagement
            
            **📈 Pro Tips:**
            - Save captions you love for future reference
            - A/B test different tones to see what works best
            - Use location-specific hashtags when relevant
            - Add your own personal touch to make it uniquely yours
            """)

        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome section when no image is uploaded
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 🚀 Ready to spark your social media presence?")
    st.write(
        "Upload an image above to get started with AI-powered content generation!")

    st.markdown("#### What you'll get:")
    st.write(
        "• **4 Different Caption Styles:** Witty, Inspirational, Professional, and Casual")
    st.write("• **15 Relevant Hashtags:** A mix of trending and niche tags")
    st.write("• **Mood Analysis:** Understanding your image's emotional impact")
    st.write(
        "• **Smart Suggestions:** AI-powered recommendations for better engagement")

    st.write("*Perfect for influencers, businesses, content creators, and anyone looking to enhance their social media game!*")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.write("---")
st.markdown("""
<div class="footer-text">
    <p><small>Upload images responsibly and ensure you have the right to use them in your social media posts.</small></p>
</div>
""", unsafe_allow_html=True)
