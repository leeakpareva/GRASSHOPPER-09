import streamlit as st
import os
import openai
import pandas as pd
import time
from dotenv import load_dotenv

# ✅ **Set Page Config First**
st.set_page_config(page_title="GRASSHOPPER-09", page_icon="favicon.ico")

# ✅ Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    st.error("🚨 `.env` file NOT found in the project directory!")

# ✅ Fetch the API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("🚨 OpenAI API Key is missing! Please check your `.env` file.")
    st.stop()
else:
    openai.api_key = openai_api_key

# ✅ Store generated outfits for "My Wardrobe" & Chat Memory
if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🎨 **Apply Styling**
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');

        body {
            background-color: #FFFFFF;
            color: #333333;
            font-family: 'Atkinson Hyperlegible', sans-serif;
        }

        /* Header & Subheader Styling */
        .header-text {
            text-align: center;
            font-size: 60px;
            font-weight: bold;
            color: black;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        /* Sidebar Styling */
        div[data-testid="stSidebarNav"] {
            background-color: #FFFFFF;
        }
        div[data-testid="stSidebarNav"] span {
            color: black !important;
        }

        /* Search Bar Styling */
        div[data-testid="stTextInput"] input {
            background-color: #F5F5F5;
            color: #000000;
            border-radius: 12px;
            padding: 12px;
            font-size: 18px;
            border: 1px solid #D3D3D3;
        }

        /* Button Styling */
        div[data-testid="stButton"] button {
            background-color: #000000;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            width: 100%;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🟣 **Header**
st.markdown('<p class="header-text">GRASSHOPPER-09</p>', unsafe_allow_html=True)

# ✅ **Multi-Page Navigation**
page = st.sidebar.radio("Navigate", ["Home", "My Wardrobe", "About"])

if page == "Home":
    st.markdown('<p class="header-text">Generate a Fashion Look</p>', unsafe_allow_html=True)

    # ✅ **First Search Bar: Fashion Outfit Generator**
    fashion_idea = st.text_input("Describe your fashion idea or event")

    if st.button("Generate Fashion Outfit"):
        if fashion_idea:
            with st.spinner("Generating your outfit... 🔄"):
                time.sleep(2)
                prompt = f"A stylish {fashion_idea} outfit, elegant, trendy, and modern."

                try:
                    response = openai.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        n=1,
                        size="1024x1024"
                    )
                    image_url = response.data[0].url
                    st.image(image_url, caption=f"AI-Generated Outfit for: {fashion_idea}")

                    # ✅ Save to "My Wardrobe"
                    outfit_data = {"idea": fashion_idea, "image_url": image_url}
                    st.session_state.wardrobe.append(outfit_data)

                    # ✅ Save Outfit to Chat Memory
                    st.session_state.chat_history.append(f"Generated outfit: {fashion_idea}")

                    # ✅ Suggest a Fashion Store Link
                    store_search = f"https://www.google.com/search?q={fashion_idea.replace(' ', '+')}+fashion+outfit"
                    st.markdown(f"[Find a similar look online]({store_search}) 🔗", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"⚠️ Error generating outfit: {e}")
        else:
            st.warning("Please enter a fashion idea.")

    # ✅ **Second Search Bar: AI Fashion Chat**
    st.markdown("---")
    st.markdown('<p class="header-text">💬 Chat with Your AI Fashion Advisor</p>', unsafe_allow_html=True)
    chat_input = st.text_input("Ask anything about your generated outfit or fashion trends")

    if st.button("Chat Now"):
        if chat_input:
            with st.spinner("Thinking... 🤖"):
                time.sleep(1)

                messages = [{"role": "system", "content": "You are a professional fashion stylist."}]

                # ✅ Append outfit history for better responses
                for outfit in st.session_state.chat_history:
                    messages.append({"role": "user", "content": outfit})

                messages.append({"role": "user", "content": chat_input})

                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history.append(f"User: {chat_input}")
                st.session_state.chat_history.append(f"AI: {reply}")

                st.write(f"**AI Fashion Advisor:** {reply}")
        else:
            st.warning("Please enter a question.")

elif page == "My Wardrobe":
    # ✅ **Display Saved Outfits (No Dress Icon)**
    st.markdown('<p class="header-text">My Wardrobe</p>', unsafe_allow_html=True)
    if len(st.session_state.wardrobe) == 0:
        st.info("No outfits saved yet. Generate a look on the home page!")
    else:
        for item in st.session_state.wardrobe:
            st.subheader(item["idea"])
            st.image(item["image_url"], caption=f"Saved Look: {item['idea']}")

elif page == "About":
    # ✅ **Revamped About Page**
    st.markdown('<p class="header-text">About</p>', unsafe_allow_html=True)
    st.write(
        """
        **Fashion is more than just style—it's a fusion of technology and self-expression.**  

        Welcome to **GRASSHOPPER-09**, where Artificial Intelligence meets fashion to redefine how we design, style, and experience clothing.  

        As a **Fashion Technologist**, I am driven by a vision:  
        - To harness AI and data science to empower designers and stylists  
        - To integrate blockchain into fashion for **sustainability and digital ownership**  
        - To create cutting-edge, AI-first tools that **revolutionize fashion decision-making**  

        With over a decade of experience in **AI, digital transformation, and blockchain**, I am pioneering the future of **automated styling, trend prediction, and intelligent fashion ecosystems**.  

        Whether you're a designer, a brand, or an individual, **GRASSHOPPER-09 is your gateway to the next evolution of fashion.**  

        Let's build the future of fashion together. 🚀  
        """
    )
