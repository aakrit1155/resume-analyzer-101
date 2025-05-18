import io
import os

import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# from dummy import DummyLLM as ChatGoogleGenerativeAI
from utils import get_images_from_pdf, image_to_base64

load_dotenv()
# Set page configuration
st.set_page_config(page_title="Resume Analysis Tool", page_icon="📄", layout="wide")

# Initialize session state variables if they don't exist
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GOOGLE_API_KEY", None)
if "resume_content" not in st.session_state:
    st.session_state.resume_content = None
if "job_description" not in st.session_state:
    st.session_state.job_description = None
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = []
if "initial_analysis_results" not in st.session_state:
    st.session_state.initial_analysis_results = None
if "is_image_converted" not in st.session_state:
    st.session_state.is_image_converted = False
if "images" not in st.session_state:
    st.session_state.images = []


sys_message = SystemMessage(
    content="You are a professional resume analysis assistant tasked with providing detailed feedback on the resume of the user. "
)


def start_over():
    # Clear all relevant session state variables
    st.session_state.resume_content = None
    st.session_state.job_description = None
    st.session_state.analysis_complete = False
    st.session_state.initial_analysis_results = None
    st.session_state.chat_history = []
    st.session_state.image_bytes = []
    st.session_state.is_image_converted = False
    st.session_state.images = []

    st.rerun()


# App title and description
st.title("Resume Analysis Tool")
if not st.session_state.analysis_complete:
    st.write(
        "Upload your resume and get personalized feedback for your target job positions."
    )

# Start Over button at the top (only shown after API key is provided)
if st.session_state.api_key is not None:
    if st.button("Start Over", key="start_over_top"):
        start_over()

# Step 1: API Key Input
if st.session_state.api_key is None:
    st.header("Step 1: Enter Google API Key")
    st.markdown(
        """
    To use this application, you need a Google API Key with access to Gemini Pro Vision model.
    
    **How to get a Google API Key:**
    1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Sign in with your Google account
    3. Click on "Create API Key" button
    4. Copy the generated API key
    """
    )

    api_key = st.text_input("Enter your Google API Key", type="password")

    if st.button("Submit API Key"):
        if api_key:
            st.session_state.api_key = api_key
            st.success("API Key submitted successfully!")
            st.rerun()
        else:
            st.error("Please enter a valid API Key")

else:
    # Step 2: File Upload and Job Input (only if API key is provided)
    if st.session_state.resume_content is None:
        st.header("Step 2: Upload Resume and Enter Job Description")

        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
        job_description = st.text_area(
            "What job(s) are you applying for? (Include job titles, descriptions, or requirements)",
            height=150,
        )

        if uploaded_file is not None and job_description:
            if st.button("Analyze Resume"):

                images = get_images_from_pdf(pdf_bytes=uploaded_file.getvalue())
                if images:
                    st.session_state.image_bytes = []
                    print(f"Extracted {len(images)} from the uploaded PDF file.")
                    for img in images:
                        st.session_state.images.append(img)
                        st.session_state.image_bytes.append(image_to_base64(img))
                    st.session_state.is_image_converted = True
                    print(
                        f"The encoded file is of type: {type(st.session_state.image_bytes[0])}"
                    )
                else:
                    print("Image extraction failed!!!!")
                    st.session_state.image_bytes = []

                # Extract text content for display
                try:
                    text_content = ""

                    ## method 2
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
                    for page_num in range(len(pdf_reader.pages)):
                        text_content += pdf_reader.pages[page_num].extract_text()

                    st.session_state.resume_content = text_content
                    st.session_state.job_description = job_description
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
        else:
            if uploaded_file is None and job_description:
                st.info("Please upload your resume to continue.")
            elif uploaded_file is not None and not job_description:
                st.info("Please enter the job description to continue.")
            else:
                st.info(
                    "Please upload your resume and enter the job description to continue."
                )

    else:
        # Display the resume content
        with st.expander("View Your Resume Content (text)", expanded=False):
            st.write(st.session_state.resume_content)

        with st.expander("View Your Resume (Image)", expanded=False):
            for i, img in enumerate(st.session_state.images):
                st.markdown(f"--------PAGE-{i+1}----------")
                st.image(img, caption="resume", use_container_width=True)

    # Step 3: Resume Display and Analysis
    if (
        st.session_state.resume_content is not None
        and not st.session_state.analysis_complete
        and st.session_state.is_image_converted
    ):
        st.header("Step 3: Resume Analysis")

        st.write("Analyzing your resume for the specified job(s)...")

        # Initialize the LLM with Google Gemini
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=st.session_state.api_key,
                temperature=0.2,
            )

            # Construct the prompt for analysis
            analysis_prompt = f"""
            I'd like you to analyze a resume for a job application. I will provide:
            1. The resume as a PDF file
            2. The job description(s) the person is applying for
            
            Please analyze the resume in the context of the provided job description(s) and provide:
            - A detailed assessment of how well the resume matches the job requirements
            - Specific strengths in the resume that align with the job
            - Areas for improvement and specific recommendations to better align with the job requirements
            - Suggestions for better formatting, organization, or presentation
            - Any critical missing information that should be added
            
            Job Description:
            {st.session_state.job_description}
            
            Please provide a comprehensive, professional analysis that will help the applicant improve their chances of landing the job.
            """

            message = HumanMessage(
                content=[
                    {"type": "text", "text": analysis_prompt},
                ]
            )
            for img in st.session_state.image_bytes:
                message.content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img}"},
                    }
                )

            messages = [sys_message, message]

            with st.spinner("Analyzing your resume... This may take upto a minute."):
                response = llm.invoke(input=messages)

            # st.session_state.chat_history.append(AIMessage(content=response.content))
            st.session_state.initial_analysis_results = response.content

            st.session_state.analysis_complete = True
            st.rerun()

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            print(f"Error during analysis: {str(e)}")
            st.write("Please check your API key and try again, or start over.")

    # Step 4: Interactive Q&A
    if st.session_state.analysis_complete:
        st.header("Resume Analysis Results")

        with st.expander("### Initial Analysis", expanded=False):
            # Display the analysis results and chat history
            with st.chat_message("assistant"):
                st.write(st.session_state.initial_analysis_results)

        st.markdown("### Follow-up Questions")
        for msg in st.session_state.chat_history:
            if isinstance(msg, AIMessage):
                with st.chat_message("assistant"):
                    st.write(msg.content)
            elif isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.write(msg.content)

        # Interactive Q&A section
        st.markdown("### Ask Follow-up Questions")
        st.write(
            "You can ask questions about your resume, the analysis, or request specific advice."
        )

        with st.form(key="question_form", clear_on_submit=True):
            user_question = st.text_input(
                "Ask a question about your resume:", key="user_question_input"
            )
            submit_button = st.form_submit_button(label="Submit")

        if user_question and submit_button:
            try:
                # Initialize the LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=st.session_state.api_key,
                    temperature=0.5,
                )

                # Prepare the follow-up question context
                context = f"""
                I previously asked you to analyze a resume for the following job descriptions:
                {st.session_state.job_description}
                I have some follow-up questions based on your analysis.
                User: {user_question}
                
                Please answer this question based on the resume attached.
                """

                message = HumanMessage(
                    content=[
                        {"type": "text", "text": context},
                    ]
                )

                for img in st.session_state.image_bytes:
                    message.content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img}"},
                        }
                    )

                messages = [sys_message, message]
                with st.spinner("Thinking..."):
                    response = llm.invoke(input=messages)

                # Add to chat history
                st.session_state.chat_history.append(
                    HumanMessage(content=user_question)
                )
                st.session_state.chat_history.append(
                    AIMessage(content=response.content)
                )

                st.rerun()

            except Exception as e:
                st.error(f"Error processing question: {str(e)}")


# Footer
st.markdown("---")
st.markdown("Built by Aakrit using Streamlit, Langchain, and Google GenAI. (•‿•)")
