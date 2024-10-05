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

# Logger modülünü kur
logger = setup_logger()

# Checkerboard boyutları (satır sayısı ve sütun sayısı)
checkerboard_rows = config['checkerboard']['rows']
checkerboard_columns = config['checkerboard']['columns']
checkerboard_size = (checkerboard_rows, checkerboard_columns)

# termination criteria (sonlandırma kriteri)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D dünya noktalarını hazırlama
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)

# 3D ve 2D noktaları depolamak için listeler
objpoints = []  # 3D noktalar 
imgpoints = []  # 2D noktalar 

reprojection_errors = []

# Checkerboard görüntülerini yükleme 
images = glob.glob(os.path.join(image_folder, '*.jpg'))
counter = 0 

logger.info(f'{len(images)} adet resim bulundu. İşleme başlıyor...')

for image in images:
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Checkerboard köşelerini bulma
    ret, corners = cv.findChessboardCorners(gray, checkerboard_size, None)

    if ret == True:
        logger.info(f"Köşeler bulundu: {image}")
        # Köşeleri sub-pixel doğruluğunda iyileştir
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # 3D dünya noktaları ve görüntüdeki köşe noktalarını depola
        objpoints.append(objp)
        imgpoints.append(corners2)

        # Bulunan köşeleri çiz ve göster
        cv.drawChessboardCorners(img, checkerboard_size, corners2, ret)

        output_path = os.path.join(output_folder, f'img{counter}.jpg')
        cv.imwrite(output_path, img)
    else:
        logger.warning(f"Köşeler bulunamadı: {image}")
    counter += 1

# Eğer hiç checkerboard bulunmadıysa, hata mesajı ver
if not objpoints or not imgpoints:
    logger.error("Hiçbir checkerboard köşesi bulunamadı. Program sonlandırılıyor.")
    exit()

# Kamerayı kalibre etme
logger.info("Kamera kalibrasyonu başlatılıyor...")
ret, intrinsic_matrix, distortion_coeff, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

logger.info("Kamera kalibrasyonu tamamlandı")

# Reprojection Error Hesaplama
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], intrinsic_matrix, distortion_coeff)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    reprojection_errors.append(error)
    logger.info(f'Reprojection Error for image {i+1}: {error}')

mean_error = np.mean(reprojection_errors)
logger.info(f"Ortalama Reprojection Error: {mean_error}")
logger.info(f"Intrinsic Matrix:\n {intrinsic_matrix}")
logger.info(f"Distortion Coefficients:\n {distortion_coeff}")

# Extrinsic ve intrinsic parametreleri kaydetme
extrinsic_data = {
    'rvecs': [rvec.tolist() for rvec in rvecs],
    'tvecs': [tvec.tolist() for tvec in tvecs],
    'intrinsic_matrix': intrinsic_matrix.tolist(),
    'distortion_coefficients': distortion_coeff.tolist(),
    'reprojection_errors': reprojection_errors
}

# Zaman damgası ile dosya adı oluşturuluyor
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_filename = f"calibration_{timestamp}.yaml"
output_path = os.path.join(output_folder, output_filename)

# YAML dosyasına yazma işlemi
with open(output_path, 'w') as file:
    yaml.dump(extrinsic_data, file)

logger.info(f"Extrinsic ve intrinsic değerler {output_path} dosyasına kaydedildi.")
