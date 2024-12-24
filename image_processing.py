from PIL import Image
import cv2

from PIL import Image
import cv2

def extract_image_features(image_path):
    image_pil = Image.open(image_path)
    image_pil = image_pil.convert('L') 
    image_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    edges = cv2.Canny(image_cv, 50, 150) 
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return {
        "pil_image": image_pil,
        "edges": edges,
        "contours": contours
    }

