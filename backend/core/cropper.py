from moviepy.editor import VideoFileClip

import cv2
import numpy as np
import os

class VideoCropper:
    def __init__(self):
        # Use OpenCV's built-in Haar Cascade for face detection (lighter than MediaPipe)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_face_x_center(self, frame) -> float:
        """
        Returns the normalized x-center (0.0 to 1.0) of the primary face in the frame.
        Returns 0.5 (center) if no face is found.
        """
        if frame is None:
            return 0.5
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return 0.5

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
        
        # Analyze first few seconds to find the speaker's position (simplification for speed)
        # In a full production app, we would track the face frame-by-frame
        sample_frame = clip.get_frame(1) # Get frame at 1st second
        center_x_rel = self.detect_face_x_center(sample_frame)
        
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
