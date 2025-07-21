import ffmpeg
import os

def merge_videos_grid(video1, video2, video3, video4, output="output.mp4"):
    videos = [video1, video2, video3, video4]
    
    # Get metadata for each video
    metadata = [ffmpeg.probe(v)["streams"][0] for v in videos]
    durations = [float(m["duration"]) for m in metadata]
    max_duration = max(durations)
    width = min(int(m["width"]) for m in metadata)
    height = min(int(m["height"]) for m in metadata)

    # Load and scale videos to a consistent width and height
    inputs = [ffmpeg.input(v) for v in videos]
    inputs = [ffmpeg.filter(v, 'scale', width, height) for v in inputs]

    # Pad each video so that its total duration equals max_duration
    padded_inputs = []
    for inp, duration in zip(inputs, durations):
        pad_time = max_duration - duration  # extra time to pad
        # If pad_time is 0, tpad won't change the clip
        padded = ffmpeg.filter(inp, 'tpad', stop_duration=pad_time, stop_mode='clone')
        padded_inputs.append(padded)

    # Arrange the padded videos in a 2x2 grid (explicitly specifying 4 inputs)
    grid = ffmpeg.filter(padded_inputs, 'xstack', inputs=4, layout="0_0|w0_0|0_h0|w0_h0")

    # Force the output video to run at 120 fps
    grid = ffmpeg.filter(grid, 'fps', fps=120)

    # Output the final merged video (adjust vcodec if using GPU acceleration)
    output_stream = ffmpeg.output(grid, output, vcodec='h264_nvenc', pix_fmt='yuv420p', r=120)
    ffmpeg.run(output_stream)

# Example Usage
video1_path = "assets/namo_isaacsim_persp_camera_demo_placeonground.mp4"
video2_path = "assets/namo_isaacsim_forklift_camera_demo_placeonground.mp4"
video3_path = "assets/namo_isaacsim_persp_camera_demo_placeonobject.mp4"
video4_path = "assets/namo_isaacsim_forklift_camera_demo_placeonobject.mp4"
merge_videos_grid(video1_path, video2_path, video3_path, video4_path, "assets/output_grid.mp4")
