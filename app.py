#!/usr/bin/env python
# coding: utf-8

# In[9]:


import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Job Acceptance Prediction System",
    page_icon="💼",
    layout="wide"
)

# ==========================
# MODEL LOAD
# ==========================

model = pickle.load(
    open("job_acceptance_model.pkl", "rb")
)

# ==========================
# HISTORY FILE
# ==========================

HISTORY_FILE = "prediction_history.csv"

if "history" not in st.session_state:

    if os.path.exists(HISTORY_FILE):

        try:
            history_df = pd.read_csv(HISTORY_FILE)

            st.session_state.history = (
                history_df.to_dict("records")
            )

        except:
            st.session_state.history = []

    else:
        st.session_state.history = []

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.title-box {
    background: linear-gradient(
        90deg,
        #1e3c72,
        #2a5298
    );
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 38px;
    font-weight: bold;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(
        90deg,
        #00b09b,
        #96c93d
    );
    color: white;
    font-size: 18px;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #36d1dc,
        #5b86e5
    );
}

.history-card {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Prediction",
        "📜 History"
    ]
)

# ==========================
# PREDICTION PAGE
# ==========================

if page == "🏠 Prediction":

    st.markdown(
        """
        <div class="title-box">
        💼 Job Acceptance Prediction System
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.subheader("📊 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        candidate_name = st.text_input(
            "👤 Candidate Name"
        )

        age = st.number_input(
            "🎂 Age",
            18,
            60,
            25
        )

        experience = st.number_input(
            "💼 Experience (Years)",
            0,
            20,
            2
        )

        technical = st.slider(
            "💻 Technical Score",
            0,
            100,
            70
        )

    with col2:

        aptitude = st.slider(
            "🧠 Aptitude Score",
            0,
            100,
            70
        )

        skills = st.slider(
            "⚡ Skills Match %",
            0,
            100,
            70
        )

        communication = st.slider(
            "🗣 Communication Score",
            0,
            100,
            70
        )

    st.subheader("📈 Candidate Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Technical",
        technical
    )

    c2.metric(
        "Skills Match",
        skills
    )

    c3.metric(
        "Communication",
        communication
    )

    st.subheader("📋 Performance Overview")

    st.write("Technical")
    st.progress(technical)

    st.write("Aptitude")
    st.progress(aptitude)

    st.write("Skills Match")
    st.progress(skills)

    st.write("Communication")
    st.progress(communication)

    if st.button("🚀 Predict Now"):

        if candidate_name.strip() == "":

            st.warning(
                "Please enter candidate name"
            )

        else:

            sample = pd.DataFrame({

                "age_years": [age],
                "years_of_experience": [experience],
                "technical_score": [technical],
                "aptitude_score": [aptitude],
                "skills_match_percentage": [skills],
                "communication_score": [communication]

            })

            prediction = model.predict(
                sample
            )[0]

            timestamp = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            history_record = {

                "Candidate Name": candidate_name,
                "Age": age,
                "Experience": experience,
                "Technical": technical,
                "Aptitude": aptitude,
                "Skills": skills,
                "Communication": communication,
                "Prediction": prediction,
                "Time": timestamp
            }

            st.session_state.history.insert(
                0,
                history_record
            )

            pd.DataFrame(
                st.session_state.history
            ).to_csv(
                HISTORY_FILE,
                index=False
            )

            st.subheader(
                "🎯 Prediction Result"
            )

            if prediction == "Placed":

                st.success(
                    f"✅ {candidate_name} is likely to ACCEPT the Job"
                )

                st.balloons()

            else:

                st.error(
                    f"❌ {candidate_name} is likely to REJECT the Job"
                )

# ==========================
# HISTORY PAGE
# ==========================

elif page == "📜 History":

    st.markdown(
        """
        <div class="title-box">
        📜 Prediction History
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if len(
        st.session_state.history
    ) == 0:

        st.warning(
            "No prediction history available."
        )

    else:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        st.download_button(
            label="📥 Download History",
            data=history_df.to_csv(
                index=False
            ),
            file_name="Prediction_History.csv",
            mime="text/csv"
        )

        st.write("")
        st.write("### 🔍 Search Candidate")

        candidate_search = st.text_input(
            "Enter Candidate Name"
        )

        if candidate_search:

            result = history_df[
                history_df[
                    "Candidate Name"
                ].str.contains(
                    candidate_search,
                    case=False,
                    na=False
                )
            ]

            st.dataframe(
                result,
                use_container_width=True
            )

        st.write("")

        if st.button(
            "🗑 Clear Entire History"
        ):

            st.session_state.history = []

            pd.DataFrame().to_csv(
                HISTORY_FILE,
                index=False
            )

            st.success(
                "History Cleared Successfully!"
            )

            st.rerun()

# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.markdown(
    """
    <center>
    Developed with ❤️ using Streamlit
    </center>
    """,
    unsafe_allow_html=True
)


# In[ ]:




