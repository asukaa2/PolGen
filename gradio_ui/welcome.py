import gradio as gr


def welcome_tab():
    gr.HTML("<center><h1 style='font-size: 3em;'><b>Welcome to PolGen</b></h1></center>")
    with gr.Row():
        with gr.Column(variant="panel"):
            gr.HTML("<center><h2><a href='https://t.me/Politrees2'>Telegram DM</a></h2></center>")
            gr.HTML("<center><h2><a href='https://vk.com/artem__bebroy'>VKontakte</a></h2></center>")
        with gr.Column(variant="panel"):
            gr.HTML("<center><h2><a href='https://t.me/pol1trees'>Telegram Channel</a></h2></center>")
            gr.HTML("<center><h2><a href='https://t.me/+GMTP7hZqY0E4OGRi'>Telegram Chat</a></h2></center>")

    with gr.Column(variant="panel"):
        gr.HTML("<center><h2><a href='https://www.youtube.com/@Politrees'>YouTube</a></h2></center>")
        gr.HTML("<center><h2><a href='https://github.com/Politrees/PolGen'>GitHub</a></h2></center>")
