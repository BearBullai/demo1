# Updated Streamlit App with Enhanced Premium Section

import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Email Confirmation Function ---
def send_confirmation_email(name, email, plan, txn_id):
    sender_email = "bearbullai01@gmail.com"
    sender_password = "jjna ywrx hnjf rkpt"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = "Premium Access Confirmed"
    body = f"""
    Hello {name},

    Thank you for subscribing to the {plan} Premium Plan.

    ✅ Your premium access will be activated shortly.
    📄 Transaction ID: {txn_id}

    Regards,  
    Quantum Finance Team
    """

    admin_body = f"""
    New Premium Subscription:

    Name: {name}
    Email: {email}
    Plan: {plan}
    Transaction ID: {txn_id}
    """

    try:
        msg_user = MIMEMultipart()
        msg_user['From'] = sender_email
        msg_user['To'] = email
        msg_user['Subject'] = subject
        msg_user.attach(MIMEText(body, 'plain'))

        msg_admin = MIMEMultipart()
        msg_admin['From'] = sender_email
        msg_admin['To'] = sender_email
        msg_admin['Subject'] = "New Premium Subscription"
        msg_admin.attach(MIMEText(admin_body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg_user.as_string())
            server.sendmail(sender_email, sender_email, msg_admin.as_string())

        return True
    except Exception as e:
        print("Email failed:", e)
        return False

# --- Black-Scholes Pricing Function ---
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type")

# --- Streamlit Config ---
st.set_page_config(page_title="Black-Scholes Futuristic", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .video-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        z-index: -1;
        opacity: 0.3;
    }
    .glass {
        background: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
        color: white;
    }
    h1, h2, h3 {
        color: #00ffe1;
    }
    .stButton>button {
        background-color: #00b3b3 !important;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- Video Background ---
video_path = "background.mp4"
if os.path.exists(video_path):
    st.markdown(f"""
        <video autoplay loop muted class="video-bg">
            <source src="{video_path}" type="video/mp4">
        </video>
    """, unsafe_allow_html=True)

# --- Navigation ---
page = st.sidebar.selectbox("Navigate", ["Home", "Premium"])

# --- Home Page ---
if page == "Home":
    st.markdown("""
    <div class="glass">
        <h1>💹 Welcome to BearBullAI</h1>
        <p>This app visualizes European option pricing using the Black-Scholes Model — complete with live video background, stunning visuals, and interactive 3D surfaces.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.image("assets/stock.jpg", caption="Stock Market Overview", use_container_width=True)
    with col2:
        st.image("assets/trading.jpg", caption="Trading Technology", use_container_width=True)

    st.markdown("""<br><br><div class="glass">""", unsafe_allow_html=True)
    st.subheader("📟 Option Price Calculator")

    col1, col2, col3 = st.columns(3)
    with col1:
        S = st.number_input("Current Stock Price (S)", min_value=0.01, value=100.0)
    with col2:
        K = st.number_input("Strike Price (K)", min_value=0.01, value=100.0)
    with col3:
        T = st.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0)

    col4, col5, col6 = st.columns(3)
    with col4:
        r = st.number_input("Risk-Free Rate (r)", min_value=0.0, value=0.05)
    with col5:
        sigma = st.number_input("Volatility (σ)", min_value=0.01, value=0.2)
    with col6:
        option_type = st.selectbox("Option Type", ["call", "put"])

    if st.button("Calculate Option Price"):
        price = black_scholes(S, K, T, r, sigma, option_type)
        st.success(f"The {option_type} option price is: **${price:.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 3D Plot ---
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🌐 3D Option Surface Plot (Call Option)")
    strike = K
    S_vals = np.linspace(50, 150, 50)
    T_vals = np.linspace(0.01, 2.0, 50)
    S_grid, T_grid = np.meshgrid(S_vals, T_vals)
    Z = np.vectorize(lambda S, T: black_scholes(S, strike, T, r, sigma, 'call'))(S_grid, T_grid)

    fig = go.Figure(data=[go.Surface(z=Z, x=S_vals, y=T_vals, colorscale='Viridis')])
    fig.update_layout(
        scene=dict(
            xaxis_title='Stock Price (S)',
            yaxis_title='Time to Maturity (T)',
            zaxis_title='Call Option Price'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Premium Page ---
elif page == "Premium":
    st.markdown("""
    <div class="glass">
        <h2>💼 Premium Nifty & BankNifty Signals</h2>
        <p>Unlock access to highly accurate market calls curated by experts.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Premium Plans")
    plan = st.radio("Choose Your Plan", ["💡 Daily - ₹199", "📆 Weekly - ₹349"])

    if plan == "💡 Daily - ₹199":
        st.write("""
        ✅ Get 2 premium calls daily  
        🎯 Accuracy: **85%**  
        💰 Price: ₹199/day
        """)
    else:
        st.write("""
        ✅ Get 10 premium calls weekly  
        🎯 Accuracy: **80%**  
        💰 Price: ₹349/week
        """)

    st.markdown("### 💵 Make Payment")
    st.markdown("Click the link below to complete payment:")
    st.markdown("[Pay Now](https://your-payment-link.com)")  # Replace with actual link
    st.image("assets/qr_code.png", caption="Scan to Pay via UPI", width=200)

    st.markdown("### 🧾 Enter Your Details")
    with st.form("premium_form"):
        name = st.text_input("Full Name")
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email ID")
        txn_id = st.text_input("Transaction ID")
        submitted = st.form_submit_button("Submit & Confirm")

    if submitted:
        if name and mobile and email and txn_id:
            df_entry = pd.DataFrame([[name, mobile, email, plan, txn_id]],
                                    columns=["Name", "Mobile", "Email", "Plan", "Transaction ID"])
            file_path = "premium_users.csv"
            if os.path.exists(file_path):
                df_entry.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df_entry.to_csv(file_path, index=False)

            email_sent = send_confirmation_email(name, email, plan, txn_id)
            if email_sent:
                st.success("✅ Thank you! Your premium access will be activated shortly. A confirmation email has been sent.")
            else:
                st.warning("✅ Info saved, but failed to send confirmation email. Please check the email setup.")
        else:
            st.error("⚠️ Please fill all the details.")

# --- Footer ---
st.markdown("""
<br><center style='color:#aaa;'>
    Built with ⚡ Python, Streamlit, and Plotly | © 2025 Quantum Finance
</center>
""", unsafe_allow_html=True)
