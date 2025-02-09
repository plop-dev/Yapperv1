import machine  # type: ignore ONLY MICROPYTHON
import utime  # type: ignore ONLY MICROPYTHON
import array
import struct


def setup_adc(pin=26):
    """Set up the ADC for the microphone."""
    return machine.ADC(pin)


def record_audio(adc, sample_rate=2500, record_time=5):
    """Record audio from the ADC for a given duration.

    Args:
        adc: The ADC object.
        sample_rate: Samples per second.
        record_time: Duration of recording in seconds.

    Returns:
        An array.array containing 16-bit signed samples.
    """
    num_samples = sample_rate * record_time
    buffer = array.array("h", [0] * num_samples)
    print("Recording...")
    prev_sample = adc.read_u16() - 32768  # Center around 0
    start_time = utime.ticks_us()

    for i in range(num_samples):
        sample = adc.read_u16() - 32768  # Remove DC offset
        buffer[i] = sample - prev_sample  # Apply simple high-pass filtering
        prev_sample = sample

        while utime.ticks_us() - start_time < (i + 1) * (1000000 // sample_rate):
            pass  # Wait for the next sample time

    print("Recording complete.")
    return buffer


def write_wav(filename, sample_rate, data):
    """Write the recorded audio data to a WAV file.

    Args:
        filename: Name of the output WAV file.
        sample_rate: Sample rate used during recording.
        data: An array.array with 16-bit signed audio samples.
    """
    num_channels = 1
    byte_rate = sample_rate * num_channels * 2  # 16-bit audio
    block_align = num_channels * 2
    subchunk2_size = len(data) * 2  # 2 bytes per sample

    wav_header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",  # ChunkID
        36 + subchunk2_size,  # ChunkSize
        b"WAVE",  # Format
        b"fmt ",  # Subchunk1ID
        16,  # Subchunk1Size (PCM)
        1,  # AudioFormat (PCM)
        num_channels,  # NumChannels
        sample_rate,  # SampleRate
        byte_rate,  # ByteRate
        block_align,  # BlockAlign
        16,  # BitsPerSample
        b"data",  # Subchunk2ID
        subchunk2_size,  # Subchunk2Size
    )

    with open(filename, "wb") as f:
        f.write(wav_header)
        for sample in data:
            f.write(struct.pack("<h", sample))  # Write 16-bit signed sample


def main():
    sample_rate = 2500  # 2500 Hz sample rate
    record_time = 5  # Recording duration in seconds
    adc = setup_adc(26)

    # Record audio and save to file
    audio_data = record_audio(adc, sample_rate, record_time)
    write_wav("audio.wav", sample_rate, audio_data)
    print("Audio saved as 'audio.wav'.")


if __name__ == "__main__":
    main()
