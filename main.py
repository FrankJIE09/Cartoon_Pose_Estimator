import time
import cv2
import mediapipe as mp
import numpy as np
import traceback

# Import the OrbbecCamera class and functions from orbbec_camera.py
from orbbec_camera import OrbbecCamera, get_serial_numbers, frame_to_bgr_image  # Ensure utils.py is accessible

ESC_KEY = 27


# Initialize MediaPipe Pose (moved to global scope)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# Cartoonize Function (moved to global scope)
def cartoonize_image(img, ksize=5, sketch_mode=False):
    if img is None or img.size == 0:
        print("Cartoonize Error: Input image is empty.")
        return None

    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY,
                                      blockSize=9,
                                      C=2)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        if sketch_mode:
            return edges

        color = cv2.bilateralFilter(img, d=ksize * 2, sigmaColor=max(10, ksize * 15), sigmaSpace=max(10, ksize * 15))
        cartoon = cv2.bitwise_and(color, edges)

        return cartoon
    except cv2.error as e:
        print(f"Error during cartoonization: {e}")
        print(f"Image shape: {img.shape}, dtype: {img.dtype}")
        return img  # Return original image on error


def main():
    print("Querying device serial numbers...")
    serial_numbers = get_serial_numbers()  # Get serial numbers using the function from orbbec_camera.py
    print(f"Available devices: {serial_numbers}")

    if not serial_numbers:
        print("Error: No Orbbec devices detected. Exiting.")
        return

    # --- Initialize Camera ---
    target_serial = 'CP1Z842000DM'  # Keep your specific serial
    if target_serial not in serial_numbers:
        print(f"Warning: Target serial {target_serial} not found. Using first available device: {serial_numbers[0]}")
        target_serial = serial_numbers[0]

    print(f"Initializing camera: {target_serial}")
    try:
        camera = OrbbecCamera(target_serial)  # Initialize using OrbbecCamera from orbbec_camera.py
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return

    print("Starting main loop...")
    try:
        while True:
            # 1. Get Frames from OrbbecCamera Class
            color_image, depth_image, depth_frame = camera.get_frames()

            # 2. Check if color image is valid
            if color_image is None:
                time.sleep(0.01)
                continue

            # 3. --- Apply MediaPipe Pose and Cartoonization ---
            frame_bgr = color_image.copy()

            # Convert to RGB for MediaPipe
            try:
                image_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            except cv2.error as e:
                print(f"Error converting BGR to RGB: {e}")
                display_frame = frame_bgr
                continue

            # Process pose
            try:
                results = pose.process(image_rgb)
            except Exception as e:
                print(f"Error during MediaPipe pose processing: {e}")
                results = None
                display_frame = frame_bgr

            # Cartoonize the BGR frame
            cartoon_frame = cartoonize_image(frame_bgr, ksize=5)
            if cartoon_frame is None:
                print("Cartoonization failed, displaying original.")
                display_frame = frame_bgr
            else:
                display_frame = cartoon_frame

            # Draw landmarks onto the cartoon frame
            if results and results.pose_landmarks:
                try:
                    mp_drawing.draw_landmarks(
                        image=display_frame,
                        landmark_list=results.pose_landmarks,
                        connections=mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                except Exception as e:
                    print(f"Error drawing landmarks: {e}")

            # 4. Display the final processed frame
            cv2.imshow(f"Camera {camera.get_serial_number()} Cartoon Pose", display_frame)

            # 5. Check for exit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exit key pressed.")
                break

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print(f"An error occurred in the main execution loop: {e}")
        traceback.print_exc()
    finally:
        # Cleanup
        print("Closing cameras and resources...")
        if 'camera' in locals() and camera is not None:
            camera.stop()

        if 'pose' in globals() and pose is not None:
            pose.close()
            print("MediaPipe Pose closed.")

        cv2.destroyAllWindows()
        print("Process finished.")


if __name__ == "__main__":
    main()