import gradio as gr
from controller import ChatbotController


controller = ChatbotController()
def respond(msg, history_state):
    response = controller.get_response(msg, history_state)
    history_state.append({"role":"user", "content":msg})
    history_state.append({"role":"assistant", "content":response})
    return history_state, history_state

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", min_width=800, min_height=600, label="Assistant")
    msg = gr.Textbox(label="User", placeholder="Would you like to know more about Aitor? Write your question here...")

    history_state = gr.State([])
    msg.submit(respond, inputs=[msg, history_state], outputs=[chatbot, history_state])
    msg.submit(lambda: "", None, msg)

demo.launch(inbrowser=True)
