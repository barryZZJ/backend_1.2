from pydub import AudioSegment
from pydub.generators import Sine


def add_beep_to_stream(input_file, input_format, output_file, output_format, start_time_sec: float, duration_sec: float, beep_frequency=1000):
    audio = AudioSegment.from_file(input_file, format=input_format)

    beep = Sine(beep_frequency).to_audio_segment(duration=duration_sec * 1000)

    start_time_ms = int(start_time_sec * 1000)
    end_time_ms = int((start_time_sec + duration_sec) * 1000)

    audio = audio[:start_time_ms] + beep + audio[end_time_ms:]

    audio.export(output_file, format=output_format)


if __name__ == "__main__":
    input_file = "../../audios/audiotest.wav"
    input_format = 'wav'
    beeped_file = "../../audios/beeped.wav"
    output_format = 'wav'
    start_time = 2
    duration = 1

    add_beep_to_stream(input_file, input_format, beeped_file, output_format, start_time, duration)
