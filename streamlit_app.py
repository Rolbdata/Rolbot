import streamlit as st
from openai import OpenAI
import tiktoken

# Imposta la tua API key (occhio a non condividerla pubblicamente!)
OPENAI_API_KEY = "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"  # Sostituisci con la tua vera API Key

# Carica le informazioni dal file
def load_personal_info(file_path="informazioni_rolando.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Conta i token di un testo
def count_tokens(text, model="gpt-4-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Inizializza elementi nella sessione
if "messages" not in st.session_state:
    st.session_state.messages = []
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

# Carica info e client
personal_info = load_personal_info()
client = OpenAI(api_key=OPENAI_API_KEY)

# Titolo
st.title("Chatbot di Rolando")
st.markdown("🤖 Puoi fare **fino a 3 domande** riguardo **Rolando**.")

# Mostra chat precedente
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if st.session_state.questions_asked >= 3:
    st.warning("Hai raggiunto il limite massimo di 3 domande. Grazie per aver usato il chatbot!", icon="⚠️")
else:
    if prompt := st.chat_input("Fai una domanda su Rolando..."):
        if "rolando" not in prompt.lower():
            st.error("Puoi fare solo domande relative a **Rolando**.")
        else:
            st.session_state.questions_asked += 1
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            context = (
                "Le seguenti informazioni sono su Rolando. Usa SOLO queste informazioni per rispondere. "
                "Se non puoi rispondere basandoti su di esse, rispondi 'Non lo so'.\n\n"
                f"{personal_info}\n\n"
                f"Domanda: {prompt}"
            )

            if count_tokens(context) > 50000:
                st.error("Il contesto è troppo lungo. Riduci la dimensione del file.")
            else:
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "system", "content": context}]
                )
                assistant_response = response.choices[0].message.content
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
