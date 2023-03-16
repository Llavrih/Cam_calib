import pyrealsense2 as rs
import numpy as np
import cv2
import time

# Configure the RealSense cameras
pipeline_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device('233622079610')  # replace with the serial number of the first camera
config_1.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

pipeline_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device('233622074753')  # replace with the serial number of the second camera
config_2.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

# Start the RealSense cameras
pipeline_1.start(config_1)
pipeline_2.start(config_2)

try:
    # Wait for 5 seconds
    print("Waiting for 2 seconds...")
    time.sleep(2)

    # Capture images
    index = 0
    while True:
        # Wait for a coherent pair of frames from both cameras
        frames_1 = pipeline_1.wait_for_frames()
        frames_2 = pipeline_2.wait_for_frames()

        color_frame_1 = frames_1.get_color_frame()
        color_frame_2 = frames_2.get_color_frame()

        # Convert the frames to numpy arrays
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        color_image_2 = np.asanyarray(color_frame_2.get_data())

        # Display the images
        cv2.imshow('Camera 1', color_image_1)
        cv2.imshow('Camera 2', color_image_2)

        key = cv2.waitKey(1)
        if key == ord('p'):
            cv2.imwrite(f'camera_1_{index}.jpg', color_image_1)
            cv2.imwrite(f'camera_2_{index}.jpg', color_image_2)
            index += 1

        elif key == ord('q'):
            break

finally:
    # Stop the RealSense cameras
    pipeline_1.stop()
    pipeline_2.stop
