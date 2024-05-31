import cv2
import pytesseract

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)

    def remove_blur(self):
        # Aplicando desfoque gaussiano para suavizar a imagem
        blurred_image = cv2.GaussianBlur(self.image, (5, 5), 0)

        # Subtraindo a imagem original da imagem borrada para destacar as bordas
        deblurred_image = self.image - blurred_image

        # Convertendo para escala de cinza para melhorar o reconhecimento de texto
        gray_image = cv2.cvtColor(deblurred_image, cv2.COLOR_BGR2GRAY)

        # Aplicando limiarização para binarizar a imagem
        _, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

        # Dilatando a imagem para aumentar a espessura das bordas do texto
        dilated_image = cv2.dilate(thresholded_image, None, iterations=1)

        self.image = dilated_image

    def enhance_image(self):
        # Aumentando o contraste da imagem
        contrasted_image = cv2.equalizeHist(self.image)

        # Aplicando filtro de Sharpen para melhorar a nitidez do texto
        sharpened_image = cv2.filter2D(contrasted_image, -1, cv2.GaussianBlur(contrasted_image, (3, 3), 0))

        self.image = sharpened_image

    def recognize_text(self):
        # Convertendo a imagem para RGB para o Tesseract
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)

        # Reconhecendo o texto com Tesseract e retornando as palavras
        words = pytesseract.image_to_string(rgb_image, config='--psm 10').split()

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
    text = processor.recognize_text()
    print(text)

if __name__ == "__main__":
    main()
