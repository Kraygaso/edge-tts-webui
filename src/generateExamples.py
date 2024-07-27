import edge_tts
import asyncio
import os
import logging
from typing import List

from avaliableVoices import avaliableVoices

logging.basicConfig(level=logging.INFO)

SAMPLE_TEXT = "This is an example."

async def generate_voice_sample(voice: str, output_path: str) -> None:
    """Generate a voice sample for a given voice and save it to the specified path."""
    communicate = edge_tts.Communicate(SAMPLE_TEXT, voice)
    await communicate.save(output_path)
    logging.info(f"Generated example: {voice}")

async def generate_voice_samples(voices: List[str], voices_dir: str) -> None:
    """Generate voice samples for all available voices."""
    os.makedirs(voices_dir, exist_ok=True)

    for index, voice in enumerate(voices, start=1):
        output_path = os.path.join(voices_dir, f"{voice}.wav")
        
        if os.path.exists(output_path):
            logging.info(f"[{index}/{len(voices)}] Skipping example generation for {voice} as the file already exists.")
            continue

        try:
            await generate_voice_sample(voice, output_path)
            logging.info(f"[{index}/{len(voices)}] Generated example: {voice}")
        except Exception as e:
            logging.error(f"[{index}/{len(voices)}] Failed to generate example for {voice}: {str(e)}")

async def main() -> None:
    """Main function to run the voice sample generation process."""
    voices_dir = input("Enter the path to the voices folder: ")
    await generate_voice_samples(avaliableVoices, voices_dir)

if __name__ == "__main__":
    asyncio.run(main())