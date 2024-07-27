import gradio as gr
import edge_tts
import os
from pathlib import Path
from typing import Optional
import time

from avaliableVoices import avaliableVoices

# Adjust paths to be relative to the project root
PROJECT_ROOT = Path(__file__).parent.parent
SAMPLES_DIR = PROJECT_ROOT / "samples"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)  # Create the output directory if it doesn't exist

def change_voice(voice: str) -> str:
    return str(SAMPLES_DIR / f"{voice}.wav")

def generate_output_filename(voice: str) -> str:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return f"{voice}_{timestamp}.mp3"

async def text_to_speech(text: str, voice: str, rate: int, volume: int) -> Optional[str]:
    rate_str = f"+{rate}%" if rate >= 0 else f"{rate}%"
    volume_str = f"+{volume}%" if volume >= 0 else f"{volume}%"
    
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, volume=volume_str)
    
    output_filename = generate_output_filename(voice)
    output_path = OUTPUT_DIR / output_filename
    await communicate.save(str(output_path))
    
    if output_path.exists():
        return str(output_path)
    else:
        raise gr.Error("Conversion failed")

def clear_speech() -> tuple:
    return "", None

def create_ui() -> gr.Blocks:
    with gr.Blocks(css="style.css", title="edge-tts-webui") as demo:
        gr.Markdown("# Microsoft Edge TTS (text-to-speech)")
        
        with gr.Row():
            with gr.Column():
                text = gr.TextArea(label="Text input:", elem_classes="text-area")
                btn = gr.Button("Generate", elem_id="submit-btn")
            
            with gr.Column():
                voices = gr.Dropdown(
                    choices=sorted(avaliableVoices),
                    value="af-ZA-AdriNeural",
                    label="Voice",
                    info="Please select a voice",
                    interactive=True
                )
                sample = gr.Audio(
                    label="Sample",
                    interactive=False,
                    elem_classes="sample"
                )
                voices.change(fn=change_voice, inputs=voices, outputs=sample)

                rate = gr.Slider(
                    -100, 100, step=1, value=0,
                    label="Speed",
                    info="Increase or decrease TTS speed",
                    interactive=True
                )
                volume = gr.Slider(
                    -100, 100, step=1, value=0,
                    label="Volume",
                    info="Increase or decrease volume",
                    interactive=True
                )
                audio = gr.Audio(label="Output", interactive=False, elem_classes="audio")
                clear = gr.Button("Clear", elem_id="clear-btn")
        
        btn.click(fn=text_to_speech, inputs=[text, voices, rate, volume], outputs=[audio])
        clear.click(fn=clear_speech, outputs=[text, audio])
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()