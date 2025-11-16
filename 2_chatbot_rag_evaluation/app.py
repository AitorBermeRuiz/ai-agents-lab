import gradio as gr
from controller import ChatbotController


def create_controller():
    """Factory function to create a new controller instance per session."""
    return ChatbotController()


async def respond(msg, history_state, controller_state):
    # Create controller on first message if not exists
    if controller_state is None:
        controller_state = create_controller()

    response = await controller_state.get_response(msg, history_state)
    history_state.append({"role": "user", "content": msg})
    history_state.append({"role": "assistant", "content": response})
    return history_state, history_state, controller_state


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", min_width=800, min_height=600, label="Assistant")
    msg = gr.Textbox(label="User", placeholder="Would you like to know more about Aitor? Write your question here...    (ONLY ENGLISH SUPPORTED)")

    history_state = gr.State([])
    controller_state = gr.State(None)  # Per-session controller instance

    msg.submit(
        respond,
        inputs=[msg, history_state, controller_state],
        outputs=[chatbot, history_state, controller_state]
    )
    msg.submit(lambda: "", None, msg)

demo.launch(inbrowser=True)
