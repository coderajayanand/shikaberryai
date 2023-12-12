
# from openai import OpenAI
# from openai.types.beta import Assistant, AssistantDeleted
import streamlit as st


col1, col2 = st.columns([1, 2])

# Add image to the top-left corner
with col1:
 image = st.image("/Users/TestVagrant-1/Downloads/shika.png", use_column_width=False, width=150)

caption_text = "Shikaberry Bot - An AI Assistant"
with col2:
 st.markdown(f'<div style="float: left; margin-right: 80px; margin-top: 80px; font-size:25px;">{caption_text}</div>', unsafe_allow_html=True)

# Add caption just below the image
caption_text = "By -- AJAY"
st.markdown(f'<p style="font-size:20px">{caption_text}</p>', unsafe_allow_html=True)


user_input = st.text_input("How may I help you", "")
print(user_input)
button_clicked = st.button("Generate Response!!")
st.markdown("<br>", unsafe_allow_html=True)

from openai import OpenAI
import time

class Assistant:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets[api_key])
        self.assistant = self.create_assistant()  # Create the assistant during initialization

    def create_assistant(self):
        self.assistant = self.client.beta.assistants.create(
        name="General knowledge tutor",
        instructions="You are an expert in general knowledge.",
        tools=[
            {"type": "code_interpreter"},  # Use the correct type value
        ],
        model="gpt-3.5-turbo-16k"
        )
        return self.assistant


    def generate_response(self, message):
        # If a thread doesn't exist, create one and store it
        print(f"Creating new thread")
        thread = self.client.beta.threads.create()
        thread_id = thread.id
        # Add message to thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )
        # Run the assistant and get the new message
        new_message = self.run_assistant(thread)
        return new_message

    def run_assistant(self, thread):
        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
        )
        # Wait for completion
        while run.status != "completed":
            # Be nice to the API
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        # Retrieve the Messages
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        new_message = messages.data[0].content[0].text.value
        return new_message


generatedOutput = ""
# Check if the button is clicked
if button_clicked:
    assistant = Assistant()
    generatedOutput = assistant.generate_response(user_input)
    print(generatedOutput)



st.markdown("""
## Result
            """+ generatedOutput + """ """ )



