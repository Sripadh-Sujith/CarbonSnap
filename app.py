
from carbonsnap_core import model
from PIL import Image
import json
import streamlit as st



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CarbonSnap",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon='favicon.ico'
)

# ---------------- GLOBAL STYLING ----------------
st.markdown("""
<style>

/* Message Card Base */
.message-card {
    font-weight: 500;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    .message-card {
        background: linear-gradient(
            135deg,
            rgba(34,197,94,0.15),
            rgba(59,130,246,0.15)
        );
        border: 1px solid rgba(255,255,255,0.1);
    }
}

/* Light mode */
@media (prefers-color-scheme: light) {
    .message-card {
        background: linear-gradient(
            135deg,
            rgba(34,197,94,0.08),
            rgba(59,130,246,0.08)
        );
        border: 1px solid rgba(0,0,0,0.08);
    }
}

</style>
""", unsafe_allow_html=True)
# ---------------- HEADER ----------------
st.markdown("""
<h2 style='text-align: center;'>🌍 CarbonSnap</h2>
<p style='text-align: center; color: gray;'>
Snap an object. Instantly understand its carbon footprint—and make smarter, sustainable choices.
</p>
""", unsafe_allow_html=True)

st.divider()

# ---------------- CAMERA ----------------
st.markdown("##### 📸 Capture")

camera_image = st.camera_input(" ", label_visibility="collapsed")
st.write('Ensure good lighting for better object identification')
# ---------------- PROCESS ----------------
if camera_image:
    image = Image.open(camera_image).convert("RGB")

   
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Analyze Impact", use_container_width=True):

        with st.spinner("Analyzing impact..."):

            response = model(image)
            res = json.loads(response)

        st.divider()

        # ---------------- OBJECT CARD ----------------
        st.markdown(f"""
        <div class="card">
            <div class="small-text">Detected Object</div>
            <div class="big-text">{res['object']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ---------------- IMPACT ----------------
        impact = res["impact_level"].lower()

        if impact == "low":
            st.success(f"🌱 Impact Level: {impact.upper()}")
        elif impact == "medium":
            st.warning(f"⚠️ Impact Level: {impact.upper()}")
        else:
            st.error(f"🔥 Impact Level: {impact.upper()}")
        st.divider()
        # ---------------- CARBON ----------------
        st.markdown("### 🌫 Carbon Footprint")
        st.markdown(f"""
        <div class="card">
            <div class="big-text">{res["carbon_estimate"]}</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        # ---------------- EXPLANATION ----------------
        st.markdown("### 🧠 Explanation")
        st.markdown(f"""
        <div class="card">
            {res["explanation"]}
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        # ---------------- ALTERNATIVES ----------------
        st.markdown("### 💡 Better Alternatives")
        alternatives_html = "".join(
            [f"<li>{alt}</li>" for alt in res["alternatives"]]
        )

        st.markdown(f"""
        <div class="card">
            <ul style="padding-left: 20px; margin: 0;">
                {alternatives_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        # ---------------- FUTURE IMPACT ----------------
        st.markdown("### 🔮 Future Impact")
        st.markdown(f"""
        <div class="card">
            {res["future_impact"]}
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        # ---------------- MESSAGE ----------------
        st.markdown("### 🌏 Message to the World")
        st.markdown(f"""
        <div class="card message-card">
            {res["message"]}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)