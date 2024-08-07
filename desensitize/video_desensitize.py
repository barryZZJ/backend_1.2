import os
from pathlib import Path

import cv2


def pixelate_frame(frame, block_size: int = 5):
    height, width, _ = frame.shape
    small_frame = cv2.resize(frame, (width // block_size, height // block_size))
    pixelated_frame = cv2.resize(small_frame, (width, height), interpolation=cv2.INTER_NEAREST)
    return pixelated_frame


def pixelate_frame_region(frame, region_x, region_y, region_w, region_h, block_size: int = 5):
    x, y, w, h = region_x, region_y, region_w, region_h
    region = frame[y:y + h, x:x + w]
    pixelated_region = pixelate_frame(region, block_size)
    frame[y:y + h, x:x + w] = pixelated_region
    return frame


def pixelate_video(input_path, output_path, block_size: int = 5):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = pixelate_frame(frame, block_size)
        out.write(processed_frame)

    cap.release()
    out.release()
    return output_path


def pixelate_video_region(input_path, output_path, region_x, region_y, region_w, region_h, block_size: int = 5):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    output_path_temp = Path(output_path).with_stem(Path(output_path).stem + '_temp')
    out = cv2.VideoWriter(output_path_temp, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = pixelate_frame_region(frame, region_x, region_y, region_w, region_h, block_size)
        out.write(processed_frame)

    cap.release()
    out.release()
    os.system('ffmpeg -y -i %s -vcodec libx264 -acodec aac -strict -2 %s' % (output_path_temp, output_path))
    return output_path


if __name__ == '__main__':
    # Choose parameters for each effect
    pixelize_block_size = 10
    rectangle_range = (300, 100, 500, 500)  # Example rectangle range (x, y, width, height)

    input_video_path = '../src/videos/test.mp4'
    output_video_path = 'path/to/your/output_video.mp4'

    pixelate_region_video_path = '../src/videos/pixelate_region.mp4'

    pixelate_video_region(input_video_path, pixelate_region_video_path, *rectangle_range, block_size=pixelize_block_size)

    # Destroy OpenCV windows
    cv2.destroyAllWindows()
