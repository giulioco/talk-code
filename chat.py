import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini about your Repo", page_icon=":robot_face:"
)
st.title("Chat with Gemini about your Repo")

# Prompt the user for the repo name
repo_name = st.text_input("Enter the name of the repo:")

if repo_name:
    # Construct the file path based on the repo name
    repo_file_path = os.path.join("repos", f"{repo_name}-formatted-prompt.txt")

    if os.path.exists(repo_file_path):
        # Read the content of the file
        with open(repo_file_path, "r") as file:
            file_content = file.read()

        # Create a prompt with context
        prompt = "This is a repo content, you are a helpful AI that helps developers with repo questions."

        # Initialize chat history if not already done
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if repo_question := st.chat_input("Ask a question about your repo:"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": repo_question})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(repo_question)

            # Set up the Gemini API key
            api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")

            with st.spinner("✋ Wait. Let him cook..."):
                # Generate a response using the Gemini API
                response = model.generate_content(
                    prompt + "\n\n" + file_content + "\n\n" + repo_question, stream=True
                )

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    for chunk in response:
                        st.write(chunk.text)
                    st.write()  # Add a newline after the response

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )

    else:
        st.error(f"File not found: {repo_file_path}")
else:
    st.warning("Please enter the name of the repo.")
