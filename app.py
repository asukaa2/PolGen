import logging
import os
import sys
import traceback
import warnings
from typing import Any

# Configuring the environment and logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Disable unnecessary TensorFlow logs
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"  # Disabling Gradio analytics
logging.basicConfig(level=logging.WARNING)  # Disable all logs, except WARNING and above
warnings.filterwarnings("ignore")  # Disable all warnings

import gradio as gr

from assets.model_installer import check_and_install_models
from assets.notebook_check import colab_check, kaggle_check
from assets.version import __version__, __version_info__
from gradio_ui.components.helpers import output_message
from gradio_ui.inference import edge_tts_tab, inference_tab
from gradio_ui.install import (
    files_upload,
    install_hubert_tab,
    url_zip_download,
    zip_upload,
)
from gradio_ui.welcome import welcome_tab

# Constants
DEFAULT_SERVER_NAME = "127.0.0.1"
DEFAULT_PORT = 4000
MAX_PORT_ATTEMPTS = 10

OUTPUT_MESSAGE_COMPONENT = output_message()
RUN_FROM_JUPYTER_NOTEBOOKS = colab_check() or kaggle_check()




def is_offline_mode() -> bool:
    return "--offline" in sys.argv


def get_title() -> str:
    """Формирует заголовок окна с версией."""
    base_title = f"PolGen v{__version__} - Politrees"
    if is_offline_mode():
        return f"{base_title} (offline)"
    return base_title


# Gradio Interface
with gr.Blocks(
    title=get_title(),
    css="footer{display:none !important}",
    theme=gr.themes.Base(
        primary_hue="green",
        secondary_hue="green",
        neutral_hue="neutral",
        spacing_size="sm",
        radius_size="lg",
    ),
) as PolGen:
    with gr.Tab("Велком/Контакты"):
        welcome_tab()

    with gr.Tab("RVC | Преобразование голоса"):
        inference_tab()

    if not is_offline_mode():
        with gr.Tab("TTS | Преобразование текста в речь"):
            edge_tts_tab()

    
    with gr.Tab("Загрузка моделей"):
        if not is_offline_mode():
            with gr.Tab("Загрузка RVC моделей"):
                url_zip_download(OUTPUT_MESSAGE_COMPONENT)
                zip_upload(OUTPUT_MESSAGE_COMPONENT)
                files_upload(OUTPUT_MESSAGE_COMPONENT)
                OUTPUT_MESSAGE_COMPONENT.render()

            with gr.Tab("Загрузка HuBERT моделей"):
                install_hubert_tab()
        else:
            with gr.Tab("Загрузка RVC моделей"):
                zip_upload(OUTPUT_MESSAGE_COMPONENT)
                files_upload(OUTPUT_MESSAGE_COMPONENT)
                OUTPUT_MESSAGE_COMPONENT.render()


PolGen.launch(
    favicon_path="assets/logo.ico",
    share=True,
)


