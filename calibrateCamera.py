import cv2 as cv
import numpy as np
import glob
import os
import yaml
import time
from logger import setup_logger

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
image_folder = config['paths']['image_folder']
output_folder = config['paths']['output_folder']

# setting up logger module
logger = setup_logger()

# checkerboard size (row and collumn size)
checkerboard_rows = config['checkerboard']['rows']
checkerboard_columns = config['checkerboard']['columns']
checkerboard_size = (checkerboard_rows, checkerboard_columns)

# termination criteria (max iteration and min reprojection error)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# preparing 3d object points
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)

# lists for store up 3d and 2d points
objpoints = []  # 3D noktalar 
imgpoints = []  # 2D noktalar 

reprojection_errors = []

# uploading checkerboard images
images = glob.glob(os.path.join(image_folder, '*.jpg'))
counter = 0 

logger.info(f'{len(images)} images found. Starting processing...')

for image in images:
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # finding checkerboard corners
    ret, corners = cv.findChessboardCorners(gray, checkerboard_size, None)

    if ret == True:
        logger.info(f"Corners found: {image}")
        # optimizing corners using sub-pixel accuracy
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # store up 3d object points and corners of checkerboard
        objpoints.append(objp)
        imgpoints.append(corners2)

        # draw the detected corners and display the image
        cv.drawChessboardCorners(img, checkerboard_size, corners2, ret)

        output_path = os.path.join(output_folder, f'img{counter}.jpg')
        cv.imwrite(output_path, img)
    else:
        logger.warning(f"Corners not found: {image}")
    counter += 1

# show this logger message if there is no any checkerboard
if not objpoints or not imgpoints:
    logger.error("No checkerboard corners found. Terminating the program.")
    exit()

# calibrating camera
logger.info("Starting camera calibration...")
ret, intrinsic_matrix, distortion_coeff, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

logger.info("Camera calibration completed.")

# calculating reprojection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], intrinsic_matrix, distortion_coeff)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    reprojection_errors.append(error)
    logger.info(f'Reprojection Error for image {i+1}: {error}')

mean_error = np.mean(reprojection_errors)
logger.info(f"Average Reprojection Error: {mean_error}")
logger.info(f"Intrinsic Matrix:\n {intrinsic_matrix}")
logger.info(f"Distortion Coefficients:\n {distortion_coeff}")

# saving the extrinsic and intrinsic values
extrinsic_data = {
    'rvecs': [rvec.tolist() for rvec in rvecs],
    'tvecs': [tvec.tolist() for tvec in tvecs],
    'intrinsic_matrix': intrinsic_matrix.tolist(),
    'distortion_coefficients': distortion_coeff.tolist(),
    'reprojection_errors': reprojection_errors
}

# creating file with a time stamps
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_filename = f"calibration_{timestamp}.yaml"
output_path = os.path.join(output_folder, output_filename)

# writing on YAML file
with open(output_path, 'w') as file:
    yaml.dump(extrinsic_data, file)

logger.info(f"Extrinsic and intrinsic values saved to the file {output_path}.")