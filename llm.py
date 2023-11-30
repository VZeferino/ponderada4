import gradio as gr
from langchain.llms import Ollama
import requests
from bs4 import BeautifulSoup

history = ["Answer prompts like you are a safety expert for industrial environments."]
link = "https://www.deakin.edu.au/students/study-support/faculties/sebe/abe/workshop/rules-safety" 

def text(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return text
    except requests.exceptions.RequestException as e:
        return f"Error obtaining content from the link: {e}"

def generate_response(prompt):
    context = text(link)
    if "Error" in context:
        return context

    history.append("Consider the following text as context: "+ context)
    history.append("Question: " + prompt)
    full_prompt = "\n".join(history)
    
    oll = Ollama(base_url='http://localhost:11434', model="orca-mini")
    response = oll(full_prompt)
    
    return response

def main():
    with gr.Blocks() as demo:
        gr.Markdown("### Safety Expert Chatbot")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Your Question")
        msg.submit(generate_response, inputs=msg, outputs=chatbot)
    
    demo.launch()

if __name__ == "__main__":
    main()