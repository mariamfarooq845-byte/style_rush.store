import streamlit as st
import pandas as pd

# Configure the web page
st.set_page_config(
    page_title="Style-Rush | Luxury Pakistani Perfumes",
    page_icon="✨",
    layout="wide"
)

# 🔗 LINK YOUR DATABASE HERE:
# Paste your shared Google Sheets URL inside the quotes below:
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1wBWoN-Dz74k8oiWfPEY3Z1LHYtycz7qdJ3mwp3XVj0w/edit?usp=sharing"

# Function to automatically convert your normal sheet link into a data stream
def load_live_inventory(url):
    try:
        # Converts regular edit link into an export CSV link
        csv_url = url.split('/edit')[0] + '/export?format=csv'
        df = pd.read_csv(csv_url)
        return df.to_dict(orient='records')
    except Exception as e:
        return []

# Fetch live inventory from your phone's Google Sheet
inventory = load_live_inventory(GOOGLE_SHEET_URL)

# Custom Black & Gold Premium Business Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f3e5ab; }
    h1, h2, h3, p { color: #e6c687 !important; font-family: 'Georgia', serif; }
    .perfume-card {
        border: 2px solid #d4af37; padding: 20px; border-radius: 10px;
        background-color: #1a1a1a; margin-bottom: 20px; text-align: center;
    }
    .gold-text { color: #d4af37; font-weight: bold; font-size: 20px; }
    div.stButton > button {
        background-color: #d4af37 !important; color: #0d0d0d !important;
        font-weight: bold !important; border-radius: 5px !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #f3e5ab !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("✨ STYLE-RUSH ✨")
st.subheader("100% Original & Branded Luxury Perfumes")
st.write("🇵🇰 **Proudly Pakistani Brand** | Delivering Premium Scents Nationwide")
st.write("---")

# --- LIVE STOREFRONT CATALOGUE ---
st.header(" Our Premium Collection")
st.write("Select a perfume from your live catalog to place an order.")

if not inventory:
    st.warning("⚠️ Connecting to your live inventory database... Make sure your Google Sheet link is correct and has data!")
else:
    # Display products dynamically in a 3-column grid directly from your sheet
    cols = st.columns(3)
    for idx, item in enumerate(inventory):
        col_target = cols[idx % 3]
        with col_target:
            # Display image if URL is provided in the sheet, otherwise show a clean placeholder box
            if pd.notna(item.get('Image_URL')) and str(item['Image_URL']).startswith('http'):
                st.image(item['Image_URL'], use_container_width=True)
            
            st.markdown(f"""
            <div class="perfume-card">
                <h3>{item['Name']}</h3>
                <p class="gold-text">Rs. {int(item['Price']):,}</p>
                <p>{item['Description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Order {item['Name']}", key=f"order_{idx}"):
                st.session_state['selected_perfume'] = f"{item['Name']} (Rs. {int(item['Price']):,})"

st.write("---")

# --- DELIVERY HANDLING SYSTEM ---
st.header("🛍️ Secure Checkout (All Over Pakistan)")
default_perfume = st.session_state.get('selected_perfume', "")
chosen_product = st.text_input("Selected Perfume:", value=default_perfume)

name = st.text_input("Full Name:")
phone = st.text_input("Phone Number (e.g., 03001234567):")
address = st.text_area("Complete Delivery Address:")
city = st.selectbox("Select Your City:", ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala"])

if st.button("🚀 CONFIRM ORDER"):
    if name and phone and address and chosen_product:
        st.success(f"🎉 **Order Placed Successfully, {name}!**")
        st.info(f"📦 Shipping **{chosen_product}** to {city}. We will contact you at {phone} to arrange delivery.")
        # Note: In the final global version, we can make these orders automatically email you or save to another sheet!
    else:
        st.error("❌ Please select a perfume and complete all fields.")
