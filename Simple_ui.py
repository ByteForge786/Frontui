import streamlit as st
import ctranslate2
import transformers
from huggingface_hub import snapshot_download

@st.cache_resource
def load_model():
    model_id = "ByteForge/Defog_llama-3-sqlcoder-8b-ct2-int8_float16"
    model_path = snapshot_download(model_id)
    model = ctranslate2.Generator(model_path)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
    return model, tokenizer

# Load model and tokenizer
model, tokenizer = load_model()

def generate_sql(prompt):
    messages = [
        {"role": "system", "content": "You are SQL Expert. Given a input question and schema, answer with correct sql query"},
        {"role": "user", "content": prompt},
    ]
    input_ids = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    input_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(input_ids))
    results = model.generate_batch([input_tokens], include_prompt_in_result=False, max_length=256, sampling_temperature=0.6, sampling_topp=0.9, end_token=terminators)
    output = tokenizer.decode(results[0].sequences_ids[0])
    return output

# Streamlit UI
st.title("SQL Query Generator")

# Text area for user input
user_input = st.text_area("Enter your schema and question:", height=200)

# Button to submit
if st.button("Generate SQL"):
    if user_input:
        with st.spinner("Generating SQL query..."):
            # Get response from LLM
            response = generate_sql(user_input)
        
        # Display response
        st.write("Generated SQL Query:")
        st.code(response, language="sql")
    else:
        st.warning("Please enter a schema and question.")

# Optional: display conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if user_input and st.session_state.get('last_input') != user_input:
    st.session_state.conversation.append(("You", user_input))
    st.session_state.conversation.append(("SQL Generator", response))
    st.session_state['last_input'] = user_input

if st.session_state.conversation:
    st.write("Conversation History:")
    for role, message in st.session_state.conversation:
        st.write(f"{role}:")
        if role == "SQL Generator":
            st.code(message, language="sql")
        else:
            st.text(message)
        st.write("---")
