import openai
import spacy
import chromadb


api_key = "OPENAI_KEY"
openai.api_key = api_key


nlp = spacy.load("en_core_web_md")

chroma_db = chromadb.connect("your_chroma_db_connection_string")

def text_to_vector(text):
    doc = nlp(text)
    return doc.vector


def query_chroma_db(user_vector, similarity_threshold=0.7):
    results = chroma_db.similarity_search(user_vector)
    filtered_results = [(context, score) for context, score in results if score >= similarity_threshold]
    return filtered_results


def get_gpt3_response(user_question, context):
    combined_input = f"User: {user_question}\nContext: {context}"

    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=combined_input,
        max_tokens=50 h
    )
    return response.choices[0].message["content"]


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    user_vector = text_to_vector(user_input)
    retrieved_contexts = query_chroma_db(user_vector)

    if retrieved_contexts:
        best_context, _ = retrieved_contexts[0]
        chatbot_response = get_gpt3_response(user_input, best_context)
    else:
        chatbot_response = "I'm sorry, I don't have enough information to answer your question."

    print("Chatbot:", chatbot_response)
