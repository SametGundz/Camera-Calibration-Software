# Camera Calibration Software

## Project Description

This software calculates the intrinsic and distortion parameters of a camera using checkerboard images. It performs camera calibration, outputs reprojection errors, and saves the calibration results, including intrinsic matrix, distortion coefficients, extrinsic matrix, and correlation coefficients. The results are saved in a format that can be easily integrated into C++ applications.

## Table of Contents

- [Usage](#usage)
- [Prerequisites](#prerequisites)
- [Running the Software](#running-the-software)
- [Example Input](#example-input)
- [Example Output](#example-output)
- [Unit Tests](#unit-tests)
- [Development Environment](#development-environment)
- [Architecture](#architecture)
- [Checkerboard Shot Tips](#checkerboard-shot-tips)
- [Contributing](#contributing)
- [License](#license)

## Usage

### Prerequisites

- Python 3.9+
- OpenCV
- NumPy
- PyYAML

### Running the Software

1. Clone the repository:
   ```bash
   git clone https://github.com/SametGundz/Camera-Calibration-Software.git

2. Build the Docker image:
   ```bash
   docker build -t camera-calibrator .

3. Run the Docker container:
   ```bash
   docker run camera-calibrator

The software automatically detects checkerboard corners in images, calibrates the camera, and logs the results.

### Example Input

Checkerboard images (e.g., a 9x6 grid) should be stored in the `data/input` folder as defined in the `config.yaml`.

### Example Output

#### Intrinsic Matrix:
   ```bash
   [[3.02104779e+03 0.00000000e+00 1.05585692e+03]
 [0.00000000e+00 3.01540312e+03 1.91533035e+03]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
```

#### Distortion Coefficients:
   ```bash
   [ 0.20947133 -1.09068132 -0.00310036 -0.00471262 2.85036049]
```

#### Reprojection Error:
   ```bash
   Image 1: 0.0986
   Image 2: 0.0916
   Image 3: 0.0650
   Image 4: 0.1004
   Image 5: 0.0893
   Image 6: 0.1287
   Image 7: 0.0717
   Image 8: 0.0800
   Image 9: 0.0806
   Average: 0.0895
```

#### Extrinsic Matrix and Correlation Coefficients:
These will be saved in YAML format in the same folder as the input images, with a timestamp in the filename for session identification.

### Unit Tests
You can run the provided unit tests with:
   ```bash
   python unit_tests.py
```

### Development Environment

### Python Setup
Install Python dependencies by running:
   ```bash
   pip install -r requirements.txt
```

### Docker Setup
Alternatively, build and run the project using Docker for a consistent environment:
- Build the Docker image:
   ```bash
   docker build -t camera-calibrator .

- Run the Docker container:
   ```bash
   docker run camera-calibrator

## Archiecture

### Folder Structure
   ```bash
   camera-calibrator/
   │
   ├── data/
   │   ├── input/                 # Checkerboard images
   │   └── output/                # Calibration output
   │
   ├── calibrateCamera.py         # Main calibration script
   ├── config.yaml                # Configuration file
   ├── logger.py                  # Logger module for tracking
   ├── Dockerfile                 # Docker setup
   ├── README.md                  # Project documentation
   ├── requirements.txt           # Python dependencies
   └── calibration.log            # Log file for calibration process
```

### Main Components
1. **Image Loading**: 
   - The software reads images from the input folder specified in the `config.yaml` file. The folder contains the checkerboard images required for calibration.
2. **Corner Detection**: 
   - The software uses OpenCV's `findChessboardCorners` to detect the corners of the checkerboard pattern. It further refines the detected corners for improved accuracy.
3. **Camera Calibration**: 
   - The `calibrateCamera` function from OpenCV is used to calculate the camera's intrinsic parameters (such as focal length and optical center) and distortion coefficients.
4. **Error Calculation**: 
   - For each image, the software computes and logs the reprojection error, which indicates the accuracy of the calibration by measuring the difference between the projected points and the detected points.
5. **Saving Results**: 
   - The calibration results, including the intrinsic and extrinsic matrices, distortion coefficients, and reprojection errors, are saved in a format that is compatible with C++ applications.

## Checkerboard Shot Tips

- **Checkerboard Size**: Ensure the correct number of rows and columns as configured in the `config.yaml`.
- **Angles**: Capture images from various angles for more accurate calibration.
- **Lighting**: Avoid shadows and reflections for better corner detection.
- **Focus**: Ensure sharp focus on the checkerboard corners.
- **Distance**: Vary the distance between the camera and the checkerboard.




