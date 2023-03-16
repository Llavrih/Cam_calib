import cv2
import numpy as np

# Set the number of calibration images and the size of the calibration object
num_images = 47
calibration_object_size = 24.7 # in millimeters

# Define the calibration object
x_squares = 10
y_squares = 7
calibration_object = np.zeros((x_squares * y_squares, 3), np.float32)
calibration_object[:, :2] = np.mgrid[0:x_squares, 0:y_squares].T.reshape(-1, 2) * calibration_object_size

# Initialize the arrays to store the calibration points and the images
calibration_points = []
image_points_1 = []
image_points_2 = []

# Loop over the images and detect the calibration points

for image_idx in range(17,num_images):
    # Capture an image from each camera
    image_1 = cv2.imread(f'camera_1_{image_idx}.jpg')
    image_2 = cv2.imread(f'camera_2_{image_idx}.jpg')
    
    # Find the calibration points in both images
    gray_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
    
    ret_1, corners_1 = cv2.findChessboardCorners(gray_1, (x_squares, y_squares), None)
    ret_2, corners_2 = cv2.findChessboardCorners(gray_2, (x_squares, y_squares), None)
    
    

    # If the calibration points are found in both images, add them to the arrays
    if ret_1 == True and ret_2 == True:
        calibration_points.append(calibration_object)
        
                # Refine the calibration points to subpixel accuracy
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 1000000, 1e-10)
        corners_1 = cv2.cornerSubPix(gray_1, corners_1, (11, 11), (-1, -1), criteria)
        corners_2 = cv2.cornerSubPix(gray_2, corners_2, (11, 11), (-1, -1), criteria)

        # Add the refined calibration points to the image points arrays
        image_points_1.append(corners_1.reshape(-1, 2))
        image_points_2.append(corners_2.reshape(-1, 2))

        # Draw the detected chessboard corners onto the images
        cv2.drawChessboardCorners(image_1, (10, 7), corners_1, ret_1)
        cv2.drawChessboardCorners(image_2, (10, 7), corners_2, ret_2)
        print(image_idx)
        # Display the images with the detected corners and points
        # cv2.imshow(f'Camera 1 Image {image_idx}', image_1)
        # cv2.imshow(f'Camera 2 Image {image_idx}', image_2)
        # cv2.waitKey(0)

# Calibrate the cameras and obtain the intrinsic parameters
ret_1, camera_matrix_1, distortion_coeffs_1, rvecs_1, tvecs_1 = cv2.calibrateCamera(calibration_points, image_points_1, gray_1.shape[::-1], None, None)
ret_2, camera_matrix_2, distortion_coeffs_2, rvecs_2, tvecs_2 = cv2.calibrateCamera(calibration_points, image_points_2, gray_2.shape[::-1], None, None)

# Set the initial values of the extrinsic parameters
R = np.array([[1, 0, 0],
              [0, 0.5, -0.5],
              [0, 0.5, 0.5]])

T = np.array([[-12.5],
              [-670],
              [0]])

# Apply stereo calibration
flags = cv2.CALIB_FIX_INTRINSIC
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 1000000, 1e-100)
ret, camera_matrix_1, distortion_coeffs_1, camera_matrix_2, distortion_coeffs_2, R, T, E, F = cv2.stereoCalibrate(
    calibration_points, image_points_1, image_points_2, camera_matrix_1, distortion_coeffs_1, camera_matrix_2, distortion_coeffs_2, gray_1.shape[::-1],
    criteria=criteria, flags=flags, R=R, T=T)


# Print the extrinsic parameters
print('Rotation matrix:')
print(R)
print('Translation vector:')
print(T)
print(np.sqrt(np.power(T[0],2)+np.power(T[1],2)+np.power(T[2],2)))
print(np.arccos(R[1,1])*57.2957795)
print(np.arcsin(R[1,2])*57.2957795)


