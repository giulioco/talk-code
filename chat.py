import os
import streamlit as st
import google.generativeai as genai
from export import parse_github_url, retrieve_github_repo_info

st.set_page_config(
    page_title="Chat with Gemini about your Repo", page_icon=":robot_face:"
)
st.title("Chat with Gemini about your Repo")

# Prompt the user for the API keys
google_api_key = st.text_input("Enter your Google AI Studio API key:", type="password")
github_token = st.text_input("Enter your GitHub Access Token:", type="password")

st.markdown(
    """
    **Note:** We do not store your API keys. They are only used for this session. You can review the code [here](https://github.com/giulioco/talk-code).
    """
)

# Prompt the user for the repo URL
repo_url = st.text_input("Enter the URL of the GitHub repo:")

if google_api_key and github_token and repo_url:
    # Parse the repo URL to get the owner and repo name
    owner, repo = parse_github_url(repo_url)

    # Construct the file path based on the repo name
    repo_file_path = os.path.join("repos", f"{repo}-formatted-prompt.txt")

    # Check if the repo has been exported
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
            genai.configure(api_key=google_api_key)
            model = genai.GenerativeModel("gemini-pro")

            with st.spinner("✋ Wait. Let him cook..."):
                # Create an empty placeholder for the response
                response_container = st.empty()

                # Initialize the response text
                response_text = ""

                try:
                    # Generate a response using the Gemini API
                    for chunk in model.generate_content(
                        prompt + "\n\n" + file_content + "\n\n" + repo_question,
                        stream=True,
                    ):
                        # Append the new chunk to the response text
                        response_text += chunk.text

                        # Update the response container with the current response text
                        response_container.markdown(response_text)

                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    else:
        # Display a loader while the repo is being exported
        with st.spinner("⏳ Fetching your repo..."):
            # Export the repo
            formatted_file = retrieve_github_repo_info(repo_url, github_token)
            output_file_name = f"repos/{repo}-formatted-prompt.txt"
            with open(output_file_name, "w", encoding="utf-8") as file:
                file.write(formatted_file)
            print(f"Repository information has been saved to {output_file_name}")

        # Reload the page to display the chat interface
        st.experimental_rerun()
else:
    if not google_api_key:
        st.warning("Please enter your Google AI Studio API key.")
    if not github_token:
        st.warning("Please enter your GitHub Access Token.")
    if not repo_url:
        st.warning("Please enter the URL of the GitHub repo.")
