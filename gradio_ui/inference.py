import gradio as gr


import gradio as gr

from gradio_ui.components.helpers import (
    OUTPUT_FORMAT,
    edge_voices,
    get_folders,
    process_file_upload,
    show_autotune,
    swap_buttons,
    swap_visibility,
    update_edge_voices,
    update_models_list,
    update_visible,
)
from gradio_ui.components.settings import settings
from rvc.infer.infer import rvc_edgetts_infer, rvc_infer


def inference_tab():
    with gr.Row():
        with gr.Column(scale=1, variant="panel"):
            with gr.Group():
                rvc_model = gr.Dropdown(
                    label="Voice models:",
                    choices=get_folders(),
                    interactive=True,
                    visible=True,
                )
                ref_btn = gr.Button(
                    value="Refresh model list",
                    variant="primary",
                    interactive=True,
                    visible=True,
                )
            with gr.Group():
                autopitch = gr.Checkbox(
                    value=False,
                    label="Automatic pitch detection",
                    interactive=True,
                    visible=True,
                )
                autopitch_threshold = gr.Radio(
                    value=155.0,
                    choices=[("Male model", 155.0), ("Female model", 255.0)],
                    show_label=False,
                    interactive=True,
                    visible=False,
                )
                rvc_pitch = gr.Slider(
                    minimum=-24,
                    maximum=24,
                    step=1,
                    value=0,
                    label="Pitch adjustment",
                    info="-24 — Male model | 24 — Female model",
                    interactive=True,
                    visible=True,
                )
            with gr.Column():
                song_input = gr.Audio(
                    label="Audio",
                    type="filepath",
                    show_download_button=False,
                    show_share_button=False,
                    interactive=True,
                    visible=True,
                )

            

            with gr.Column():
                
                show_enter_button = gr.Button(
                    value="Enter file path",
                    interactive=True,
                    visible=True,
                )

    with gr.Group(), gr.Row(equal_height=True):
        generate_btn = gr.Button(
            value="Generate",
            variant="primary",
            interactive=True,
            visible=True,
            scale=2,
        )
        converted_voice = gr.Audio(
            label="Converted voice",
            show_download_button=True,
            show_share_button=False,
            interactive=False,
            visible=True,
            scale=9,
        )
        with gr.Column(min_width=160):
            output_format = gr.Dropdown(
                value="mp3",
                label="File format",
                choices=OUTPUT_FORMAT,
                interactive=True,
                visible=True,
            )

    # Settings component
    (
        f0_method,
        index_rate,
        volume_envelope,
        protect,
        stereo_sound,
        audio_upscaling,
        autotune,
        autotune_tonic,
        autotune_scale,
        autotune_strength,
        f0_min,
        f0_max,
    ) = settings()

    
    # Update pitch adjustment method
    autopitch.change(update_visible, inputs=autopitch, outputs=[autopitch_threshold, rvc_pitch])

    # Show autotune parameters
    autotune.change(show_autotune, inputs=autotune, outputs=[autotune_tonic, autotune_scale, autotune_strength])

    # Update model list
    ref_btn.click(update_models_list, None, outputs=rvc_model)

    # Start the conversion process
    generate_btn.click(
        rvc_infer,
        inputs=[
            rvc_model,
            song_input,
            f0_method,
            f0_min,
            f0_max,
            rvc_pitch,
            protect,
            index_rate,
            volume_envelope,
            autopitch,
            autopitch_threshold,
            autotune,
            autotune_tonic,
            autotune_scale,
            autotune_strength,
            audio_upscaling,
            stereo_sound,
            output_format,
        ],
        outputs=[converted_voice],
    )


def edge_tts_tab():
    with gr.Row():
        with gr.Column(variant="panel", scale=1):
            with gr.Group():
                rvc_model = gr.Dropdown(
                    label="Voice models:",
                    choices=get_folders(),
                    interactive=True,
                    visible=True,
                )
                ref_btn = gr.Button(
                    value="Refresh model list",
                    variant="primary",
                    interactive=True,
                    visible=True,
                )
            with gr.Group():
                language = gr.Dropdown(
                    label="Language",
                    choices=list(edge_voices.keys()),
                    interactive=True,
                    visible=True,
                )
                tts_voice = gr.Dropdown(
                    value="en-GB-SoniaNeural",
                    label="Voice",
                    choices=["en-GB-SoniaNeural", "en-GB-RyanNeural"],
                    interactive=True,
                    visible=True,
                )
        with gr.Column(variant="panel", scale=2):
            with gr.Column(), gr.Group():
                autopitch = gr.Checkbox(
                    value=False,
                    label="Automatic pitch detection",
                    interactive=True,
                    visible=True,
                )
                autopitch_threshold = gr.Radio(
                    value=155.0,
                    choices=[("Male model", 155.0), ("Female model", 255.0)],
                    show_label=False,
                    interactive=True,
                    visible=False,
                )
                rvc_pitch = gr.Slider(
                    minimum=-24,
                    maximum=24,
                    step=1,
                    value=0,
                    label="Pitch adjustment",
                    info="-24 — Male model || 24 — Female model",
                    interactive=True,
                    visible=True,
                )
            synth_voice = gr.Audio(
                label="Synthesized TTS voice",
                show_download_button=True,
                show_share_button=False,
                interactive=False,
                visible=True,
            )

    with gr.Accordion("Speech synthesis settings", open=False), gr.Group(), gr.Row():
        tts_pitch = gr.Slider(
            minimum=-100,
            maximum=100,
            step=1,
            value=0,
            label="TTS pitch adjustment",
            info="-100 - male voice || 100 - female voice",
            interactive=True,
            visible=True,
        )
        tts_volume = gr.Slider(
            minimum=-100,
            maximum=100,
            step=1,
            value=0,
            label="Speech volume",
            info="Speech synthesis playback volume",
            interactive=True,
            visible=True,
        )
        tts_rate = gr.Slider(
            minimum=-100,
            maximum=100,
            step=1,
            value=0,
            label="Speech rate",
            info="Speech synthesis playback rate",
            interactive=True,
            visible=True,
        )

    tts_text = gr.Textbox(label="Enter text", lines=5)

    with gr.Group(), gr.Row(equal_height=True):
        generate_btn = gr.Button(
            value="Generate",
            variant="primary",
            interactive=True,
            visible=True,
            scale=2,
        )
        converted_synth_voice = gr.Audio(
            label="Converted TTS voice",
            show_download_button=True,
            show_share_button=False,
            interactive=False,
            visible=True,
            scale=9,
        )
        with gr.Column(min_width=160):
            output_format = gr.Dropdown(
                value="mp3",
                label="File format",
                choices=OUTPUT_FORMAT,
                interactive=True,
                visible=True,
            )

    # Settings component
    (
        f0_method,
        index_rate,
        volume_envelope,
        protect,
        stereo_sound,
        audio_upscaling,
        autotune,
        autotune_tonic,
        autotune_scale,
        autotune_strength,
        f0_min,
        f0_max,
    ) = settings()

    # Update TTS voice list
    language.change(update_edge_voices, inputs=language, outputs=tts_voice)

    # Update pitch adjustment method
    autopitch.change(update_visible, inputs=autopitch, outputs=[autopitch_threshold, rvc_pitch])

    # Show autotune parameters
    autotune.change(show_autotune, inputs=autotune, outputs=[autotune_tonic, autotune_scale, autotune_strength])

    # Update model list
    ref_btn.click(update_models_list, None, outputs=rvc_model)

    # Start the conversion process
    generate_btn.click(
        rvc_edgetts_infer,
        inputs=[
            rvc_model,
            f0_method,
            f0_min,
            f0_max,
            rvc_pitch,
            protect,
            index_rate,
            volume_envelope,
            autopitch,
            autopitch_threshold,
            autotune,
            autotune_tonic,
            autotune_scale,
            autotune_strength,
            stereo_sound,
            output_format,
            tts_voice,
            tts_text,
            tts_rate,
            tts_volume,
            tts_pitch,
            audio_upscaling,
        ],
        outputs=[synth_voice, converted_synth_voice],
    )
