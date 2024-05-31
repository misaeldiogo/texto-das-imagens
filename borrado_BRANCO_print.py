import cv2
import pytesseract

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)

    def remove_blur(self):
        # Aplicando desfoque bilateral para remover o barrado
        blurred_image = cv2.bilateralFilter(self.image, 5, 50, 50)

        # Convertendo para escala de cinza para melhorar o reconhecimento de texto
        gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)

        # Aplicando binarização de Sauvola para melhorar a qualidade da imagem
        _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        self.image = thresholded_image

    def enhance_image(self):
        # Aplicando equalização de histograma adaptativa para melhorar o contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrasted_image = clahe.apply(self.image)

        # Aplicando equalização de histograma local para melhorar a nitidez
        local_contrast = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced_image = local_contrast.apply(contrasted_image)

        self.image = enhanced_image

    def recognize_text(self):
        # Reconhecendo o texto com Tesseract e retornando as palavras
        words = pytesseract.image_to_string(self.image, config='--psm 11 --oem 3').split()

        # Removendo caracteres especiais e espaços desnecessários
        cleaned_words = []
        for word in words:
            if word.isalnum() or word in ['-', '.', ',', '’', '‘', '“', '”']:
                cleaned_words.append(word)

        return ' '.join(cleaned_words)

def main():
    # Caminho para a sua imagem
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    image_path = r'C:\Users\Misael\Downloads\Telegram Desktop\h0.jpg'
    processor = ImageProcessor(image_path)
    processor.remove_blur()
    processor.enhance_image()

    # Definindo a região de interesse (ROI) ao lado de "Correct Score"
    x, y, w, h = 300, 100, 100, 30  # ajuste esses valores para a sua imagem
    roi = processor.image[y:y+h, x:x+w]

    # Reconhecendo o texto na ROI
    text = pytesseract.image_to_string(roi, config='--psm 11 --oem 3')

    # Imprimindo o texto reconhecido
    print(text)

if __name__ == "__main__":
    main()