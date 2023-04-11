import streamlit as st
from streamlit_chat import message
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.title("A helpful assistant.")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}]

def generate_answer(prompt):
  st.session_state['messages'].append({"role": "user", "content": prompt})
  completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    max_tokens=200,
    messages=st.session_state['messages']
  )
  
  response = completion.choices[0].message.content
  st.session_state['messages'].append({"role": "assistant", "content": response})
  return response

               
response_container = st.container()
container = st.container()
with container:
    with st.form(clear_on_submit=True):
        user_input = st.text_area("Prompt", position="fixed", bottom=0)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_answer(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i)) 
