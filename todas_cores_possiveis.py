import cv2
import pytesseract

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)

    def remove_blur(self):
        # Aplicando desfoque bilateral para remover o borrado
        blurred_image = cv2.bilateralFilter(self.image, 5, 50, 50)

        # Convertendo para escala de cinza para melhorar o reconhecimento de texto
        gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)

        # Aplicando binarização de Sauvola para melhorar a qualidade da imagem
        _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Ajustando os parâmetros de thresholding para destacar o texto abaixo do borrado preto
        _, thresholded_image = cv2.threshold(thresholded_image, 127, 255, cv2.THRESH_BINARY)

        self.image = thresholded_image

    # Restante do seu código (enhance_image, recognize_text, etc.)

def main():
    # Caminho para a sua imagem
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    image_path = r'C:\Users\Misael\Downloads\Telegram Desktop\h0.jpg'
    processor = ImageProcessor(image_path)
    processor.remove_blur()

    # Restante do seu código (enhance_image, recognize_text, etc.)

if __name__ == "__main__":
    main()
