import streamlit as st
import google.generativeai as genai

# Configure API (using Streamlit secrets)
genai.configure(api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# App title and description
st.title("🇮🇳 Student Scheme Recommender")
st.markdown("""
Find government schemes and scholarships tailored to your profile in India.
Fill in your details below to get personalized recommendations.
""")

# Input fields for student profile
with st.form("student_profile"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, value=18)
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        education = st.selectbox(
            "Education Level",
            ["Select", "10th", "12th", "Diploma", "Undergraduate", "Postgraduate"]
        )
        income = st.text_input("Annual Income (INR)", placeholder="e.g., 500000")
    
    with col2:
        caste = st.selectbox(
            "Caste Category",
            ["Select", "General", "OBC", "SC", "ST", "EWS"]
        )
        state = st.text_input("State of Residence", placeholder="e.g., Maharashtra")
        disability = st.selectbox(
            "Do you have any disability?",
            ["No", "Yes"]
        )
        skills = st.text_input("Your Skills/Interests", placeholder="e.g., Programming, Arts")
    
    submitted = st.form_submit_button("Find Suitable Schemes")

# Generate recommendations when form is submitted
if submitted:
    if education == "Select" or caste == "Select" or not state:
        st.warning("Please fill all required fields")
    else:
        with st.spinner("Finding the best schemes for you..."):
            prompt = f"""
            You are a smart assistant helping students in India find suitable government schemes and scholarships.
            Based on the following user details, recommend the most relevant and personalized central or state government schemes with a short explanation each:

            - Age: {age}
            - Gender: {gender}
            - Education: {education}
            - Annual Income: {income}
            - Caste Category: {caste}
            - State: {state}
            - Disability: {disability}
            - Skill Interests: {skills}

            Provide 3-5 best scheme recommendations with:
            1. Scheme name (bold this)
            2. Brief description (1-2 sentences)
            3. Eligibility criteria
            4. Official website link if available

            Format the output clearly with bullet points and proper spacing.
            """
            try:
                response = model.generate_content(prompt)
                st.success("Here are your personalized scheme recommendations:")
                st.markdown(response.text)
                
                # Additional resources
                st.markdown("---")
                st.info("""
                **Note:** Always verify details on official government websites before applying.
                For more schemes, visit [https://scholarships.gov.in](https://scholarships.gov.in)
                """)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please try again later or check your internet connection.")

# Footer
st.markdown("---")
st.caption("This tool helps identify potential government schemes but doesn't guarantee eligibility.")
