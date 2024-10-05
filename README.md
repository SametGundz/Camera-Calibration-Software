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
   git clone <repo-link>

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
[[1000. 0. 640.]
 [0. 1000. 360.]
 [0. 0. 1.]]
 
 