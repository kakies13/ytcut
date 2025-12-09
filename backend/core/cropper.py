from moviepy.editor import VideoFileClip

import cv2
import numpy as np
import os

class VideoCropper:
    def __init__(self):
        # Use OpenCV's built-in Haar Cascade for face detection (lighter than MediaPipe)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_face_x_center(self, frame) -> float | None:
        """
        Returns the normalized x-center (0.0 to 1.0) of the primary face in the frame.
        Returns None if no face is found.
        """
        if frame is None:
            return None
            
        # MoviePy returns RGB, OpenCV usually expects BGR/Gray
        # Correctly convert RGB to GRAY
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        # minNeighbors=3 is slightly more lenient than 4
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        
        if len(faces) == 0:
            return None

        # Assume the largest face is the speaker
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        center_x = x + (w / 2)
        frame_width = frame.shape[1]
        
        return max(0.0, min(1.0, center_x / frame_width))

    def create_vertical_clip(self, video_path: str, start: int, end: int, output_path: str):
        clip = VideoFileClip(video_path).subclip(start, end)
        
        # Target aspect ratio 9:16
        target_ratio = 9/16
        w, h = clip.size
        target_w = int(h * target_ratio)
        # Ensure width is even for x264 codec
        if target_w % 2 != 0:
            target_w -= 1
        
        # Analyze multiple frames to find the speaker's position
        # We sample 5 frames distributed across the clip
        duration = clip.duration
        sample_counts = 5
        timestamps = [i * duration / sample_counts for i in range(sample_counts)]
        
        centers = []
        for t in timestamps:
            # Ensure we don't go past the end
            t = min(t, duration - 0.1)
            try:
                frame = clip.get_frame(t)
                c = self.detect_face_x_center(frame)
                if c is not None:
                    centers.append(c)
            except Exception as e:
                print(f"Error analyzing frame at {t}: {e}")
                pass
        
        # If we found faces, take the average position
        if centers:
            center_x_rel = sum(centers) / len(centers)
        else:
            center_x_rel = 0.5
        
        # Calculate crop coordinates
        center_x_px = int(center_x_rel * w)
        x1 = max(0, center_x_px - (target_w // 2))
        x2 = x1 + target_w
        
        # Adjust if out of bounds
        if x2 > w:
            x2 = w
            x1 = w - target_w
        if x1 < 0:
            x1 = 0
            x2 = target_w

        # Crop and Resize
        video_cropped = clip.crop(x1=x1, y1=0, x2=x2, y2=h)
        # Resize to standard 1080x1920 (TikTok/Reels) is optional but good for consistency
        # video_resized = video_cropped.resize(height=1920) 
        
        # Force yuv420p for browser compatibility (otherwise might default to yuv444p or others which don't play well)
        video_cropped.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac', 
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True,
            ffmpeg_params=['-pix_fmt', 'yuv420p'],
            logger=None
        )
        clip.close()
        video_cropped.close()
        return output_path
