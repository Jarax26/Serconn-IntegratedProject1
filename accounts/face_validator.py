import cv2
import numpy as np
from PIL import Image
import io

def validate_face_quality(image_file):
    """
    Validación más estricta que también verifica la calidad del rostro detectado.
    (Opcional - usar solo si necesitas validación más rigurosa)
    
    Args:
        image_file: Archivo de imagen (Django UploadedFile)
    
    Returns:
        tuple: (bool, str) - (Es válido, Mensaje de error si no es válido)
    """
    try:
        image_data = image_file.read()
        image_file.seek(0)
        
        pil_image = Image.open(io.BytesIO(image_data))
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' # type: ignore
        )
        
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50),  # Tamaño mínimo más grande para mejor calidad
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) == 0:
            return False, "No se detectó ningún rostro en la imagen. Asegúrate de que tu cara sea claramente visible."
        
        # Verificar que el rostro ocupe un tamaño razonable de la imagen
        img_height, img_width = opencv_image.shape[:2]
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])  # Encontrar el rostro más grande
        face_width = largest_face[2]
        face_height = largest_face[3]
        
        # El rostro debe ocupar al menos 15% del ancho de la imagen
        if face_width < img_width * 0.15:
            return False, "El rostro en la imagen es muy pequeño. Por favor, acércate más a la cámara."
        
        # Detectar si hay múltiples rostros (opcional, puedes remover esto)
        if len(faces) > 1:
            return False, "Se detectaron múltiples rostros en la imagen. Por favor, sube una foto donde aparezcas solo tú."
        
        return True, None
    
    except Exception as e:
        return False, f"Error al procesar la imagen: {str(e)}. Por favor, intenta con otra foto."