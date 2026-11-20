
import streamlit as st
import joblib
import re

# Page configuration
st.set_page_config(
    page_title="RoleRadar",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #f1f5f9;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #60a5fa;
}
.subtitle {
    color: #aab8cc;
    font-size: 17px;
}
div[data-testid="stMetric"] {
    background: #17243a;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #263954;
}
.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 9px;
    height: 45px;
    font-weight: bold;
}
.stDeployButton {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# Load models
models = {
    "SVM (Recommended)": joblib.load("models/svm_model.pkl"),
    "Logistic Regression": joblib.load("models/logistic_regression.pkl"),
    "Naive Bayes": joblib.load("models/naive_bayes.pkl"),
    "Random Forest": joblib.load("models/random_forest.pkl")
}

tfidf = joblib.load("models/tfidf_vectorizer.pkl")


# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Sample job postings
samples = {
    "Sample 1 - Software Developer Internship": {
        "title": "Software Developer Intern",
        "company": "ABC Technologies is an established software development company.",
        "description": "We are looking for a software developer intern to work with our engineering team on web applications. The selected candidate will participate in software development, testing and code reviews.",
        "requirements": "Knowledge of Python, Java, SQL and basic programming concepts. Good communication and problem solving skills.",
        "benefits": "Internship certificate, mentorship, practical experience and performance based stipend."
    },

    "Sample 2 - Suspicious Data Entry Job": {
        "title": "Work From Home Data Entry Job",
        "company": "Global Online Hiring Team. No company details available.",
        "description": "Earn huge money instantly by working only two hours daily. No experience required. Guaranteed high income. Pay a registration fee immediately to secure your position. Limited vacancies. Apply now.",
        "requirements": "Anyone can apply. No qualification or experience needed.",
        "benefits": "High guaranteed income and instant selection."
    },

    "Sample 3 - Marketing Internship": {
        "title": "Digital Marketing Intern",
        "company": "Bright Media Solutions is a digital marketing agency working with multiple businesses.",
        "description": "We are hiring a digital marketing intern to assist with social media campaigns, content planning, market research and performance analysis.",
        "requirements": "Basic knowledge of social media, communication skills and interest in digital marketing. Students may apply.",
        "benefits": "Practical training, mentorship, internship certificate and monthly stipend."
    },

    "Sample 4 - Suspicious Online Job": {
        "title": "Easy Online Work - Immediate Hiring",
        "company": "International Work Opportunities. Contact only through messaging.",
        "description": "Get guaranteed income from home without any interview. Earn thousands daily with no skills. Send your personal details and pay a small security deposit to activate your account. Immediate selection guaranteed.",
        "requirements": "No experience, education or interview required.",
        "benefits": "Guaranteed high earnings and instant joining."
    }
}


# Initialize input states
fields = ["title", "company", "description", "requirements", "benefits"]

for field in fields:
    st.session_state.setdefault(field, "")


# Sidebar
with st.sidebar:
    st.title("🔍 RoleRadar")
    st.write("Job Safety Assistant")
    st.divider()

    st.subheader("About Project")
    st.write(
        "A Machine Learning system that analyses "
        "job postings and identifies potentially "
        "fraudulent recruitment advertisements."
    )

    st.divider()
    st.subheader("ML Algorithms")
    st.write("""
    - Logistic Regression
    - Naive Bayes
    - Support Vector Machine
    - Random Forest
    """)

    st.divider()
    st.caption("Built using Python, Scikit-learn and Streamlit.")

    st.divider()
    st.subheader("📊 Dataset Information")

    st.write("**Dataset:** EMSCAD")
    st.write("**Total Records:** 17,880")
    st.write("**Genuine Jobs:** 17,014")
    st.write("**Fraudulent Jobs:** 866")

    st.caption("Source: Employment Scam Aegean Dataset")


# Header
st.markdown(
    '<div class="main-title">🔍 RoleRadar</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Fake Job & Internship Detection System</div>',
    unsafe_allow_html=True
)

st.write("")
st.info(
    "Analyse job postings and identify potentially fraudulent "
    "recruitment advertisements using Machine Learning."
)


# Dashboard information
st.subheader("💡 How RoleRadar Works")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 📝 01")
    st.markdown("**Enter Job Details**")
    st.write("Provide job title, company information and job description.")

with c2:
    st.markdown("### 🤖 02")
    st.markdown("**ML Analysis**")
    st.write("The selected machine learning model analyses the job posting.")

with c3:
    st.markdown("### 🛡️ 03")
    st.markdown("**Get Prediction**")
    st.write("View whether the posting is likely genuine or potentially fraudulent.")

st.divider()


# Model selection
st.subheader("⚙️ Select ML Model")

selected_model = st.selectbox(
    "Choose an algorithm",
    list(models.keys()),
    index=0
)

st.caption(
    "SVM is selected by default because it achieved the "
    "highest fraudulent-class F1-score in model evaluation."
)


st.divider()


# Sample selection
st.subheader("📝 Try Sample Job Postings")

sample_choice = st.selectbox(
    "Select a sample posting",
    ["Choose a sample"] + list(samples.keys())
)

if st.button("📥 Load Sample"):
    if sample_choice == "Choose a sample":
        st.warning("Please select a sample first.")
    else:
        for field in fields:
            st.session_state[field] = samples[sample_choice][field]

        st.rerun()


st.divider()


# Job information form
st.subheader("📋 Enter Job Posting Details")

col1, col2 = st.columns(2)

with col1:
    title = st.text_input(
        "Job Title",
        key="title"
    )

    company = st.text_area(
        "Company Profile",
        key="company",
        height=110
    )

    requirements = st.text_area(
        "Requirements",
        key="requirements",
        height=110
    )

with col2:
    description = st.text_area(
        "Job Description",
        key="description",
        height=180
    )

    benefits = st.text_area(
        "Benefits",
        key="benefits",
        height=110
    )


# Prediction
if st.button("🔍 Analyse Job Posting", use_container_width=True):

    if not title.strip() or not description.strip():
        st.warning("Please enter the job title and description.")

    else:
        job_text = " ".join([
            title,
            company,
            description,
            requirements,
            benefits
        ])

        cleaned_text = clean_text(job_text)

        transformed_text = tfidf.transform([cleaned_text])

        model = models[selected_model]

        prediction = model.predict(transformed_text)[0]

        st.divider()
        st.subheader("📊 Prediction Result")

        if prediction == 1:
            st.error("⚠️ Potentially Fraudulent Job Posting")
            st.markdown("**Risk Category: HIGH**")
            st.write(
                "The selected ML model has classified "
                "this posting as potentially fraudulent."
            )

        else:
            st.success("✅ Likely Genuine Job Posting")
            st.markdown("**Risk Category: LOWER**")
            st.write(
                "The selected ML model has classified "
                "this posting as likely genuine."
            )

        st.caption(
            "This is an ML prediction, not proof of fraud. "
            "Always verify the employer before sharing "
            "personal information or making payments."
        )


# Footer
st.divider()

st.markdown(
    "<center><b>RoleRadar</b> | "
    "Detect the fake. Find the real opportunity.</center>",
    unsafe_allow_html=True
)
