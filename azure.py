import cv2
import openai
import os
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

# OPEN CAMERA and then make the edges in the white project and then make the open then the function will make sure it returns the fram in same time 
class AIVisionAnalyzer:
    def __init__(self):
        load_dotenv()
        self.setup_openai()
        self.setup_camera()
        self.output_dir = "captured_images"
        os.makedirs(self.output_dir, exist_ok=True)

    def setup_openai(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        # Configure for Azure OpenAI if needed
        
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Could not open camera")
        
        # Optimize for MacOS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
    def save_frame(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/capture_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        return filename

    def analyze_frame(self, frame):
        filename = self.save_frame(frame)
        try:
            # Add your OpenAI analysis code here
            result = "Image analyzed successfully"
            return result
        except Exception as e:
            return f"Analysis error: {str(e)}"

    def run(self):
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                # Add some basic OpenCV processing
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                
                # Show both original and processed frames
                cv2.imshow('Original', frame)
                cv2.imshow('Edges', edges)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    filename = self.save_frame(frame)
                    print(f"Saved frame to {filename}")
                elif key == ord('a'):
                    analysis = self.analyze_frame(frame)
                    print(analysis)

        finally:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzer = AIVisionAnalyzer()
    analyzer.run()