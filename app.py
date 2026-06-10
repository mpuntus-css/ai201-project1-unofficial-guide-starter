from __future__ import annotations

import gradio as gr

from query import ask


def handle_query(question: str):
    result = ask(question)
    sources = "\n".join(f"• {source}" for source in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide\nAsk questions about UW-Stevens Point professor and course reviews.")

    with gr.Column():
        inp = gr.Textbox(label="Your question", placeholder="Ask about professor reviews, course difficulty, and student advice...")
        btn = gr.Button("Ask")
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()