import streamlit as st
import os
from core import Core
import pathlib

TEMP_DIR = 'temp'

pathlib.Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)

######################### RESUME EXTRACTOR ##########################
def resume_extractor(file_path, file_path_linkapi, api_key):
    qabot = Core(api_key)
    persona_res, questions_ask, feature1, feature2, feature3, feature4, feature5, feature6 = qabot.run(file_path, file_path_linkapi)
    return persona_res, questions_ask, feature1, feature2, feature3, feature4, feature5, feature6

# Function to save the uploaded file to a temporary directory
def save_uploaded_file(uploaded_file, temp_dir):
    if uploaded_file is not None:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    
def display(persona_res, questions_ask, feature1, feature2, feature3, feature4, feature5, feature6):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Persona", "Questions", "Feature1", "Feature2", "Feature3", "Feature4", "Feature5", "Feature6"])
    with tab1:
        st.header("Persona")
        st.write(persona_res)

    with tab2:
        st.header("Questions")
        st.write(questions_ask)

    with tab3:
        st.header("Complexity of projects worked on? Level of expertise based on real projects worked on")
        st.write(feature1)

    with tab4:
        st.header("Progression of expertise based on types of projects, skills used and responsibilities")
        st.write(feature2)

    with tab5:
        st.header("How effectively have the courses, certifications, and licenses acquired been used in their projects and experiences?")
        st.write(feature3)

    with tab6:
        st.header("Have they been taking courses and obtaining certifications that align with their role and responsibility or acquiring other skills?")
        st.write(feature4)
    
    with tab7:
        st.header("Career paths top 5")
        st.write(feature5)

    with tab8:
        st.header("Career Roadmap")
        st.write(feature6)
    


# Streamlit app starts here
def main():
    st.title("🔍 Candidate Persona Analyser :sunglasses:")

    # Text input field for inserting API key
    api_key = st.text_input("🔑 Insert API Key :red[*]")

    # Create a temporary directory in the root folder of the app
    temp_dir = TEMP_DIR

    # Create an upload file box
    uploaded_file = st.file_uploader("📁 Upload resume :red[*]", type=["pdf"])

    # Create an upload file box
    uploaded_linkapi_file = st.file_uploader("📁 Upload linkedin reponse in JSON :green[(Optinal)] ", type=["json"])

    # Check if a file is uploaded
    if uploaded_file is not None and api_key:
        # Save the uploaded file to the temporary directory
        file_path = save_uploaded_file(uploaded_file, temp_dir)
        file_path_linkapi = None
        if uploaded_linkapi_file is not None:
            file_path_linkapi = save_uploaded_file(uploaded_linkapi_file, temp_dir)

        # Display a button to perform a task
        if st.button("Analyze Resume"):
            # Display a loader while the task is performed
            with st.spinner("Performing task..."):
                # Perform the task
                persona_res, questions_ask, feature1, feature2, feature3, feature4, feature5, feature6 = resume_extractor(file_path, file_path_linkapi, api_key)
                display(persona_res, questions_ask, feature1, feature2, feature3, feature4, feature5, feature6)

if __name__ == "__main__":
    main()