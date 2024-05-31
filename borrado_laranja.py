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

    # Convertendo a imagem para o espaço de cores HSV
    lower_orange = (0, 100, 100)  # Limite inferior da cor laranja (ajuste se necessário)
    upper_orange = (20, 255, 255)  # Limite superior da cor laranja (ajuste se necessário)
    hsv_image = cv2.cvtColor(cv2.cvtColor(processor.image, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2HSV)

    # Extraindo texto dos blocos laranja
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Aplicando a máscara na imagem para isolar os blocos laranja
    masked_image = cv2.bitwise_and(processor.image, processor.image, mask=mask)

    # Reconhecendo o texto nos blocos laranja
    orange_text = pytesseract.image_to_string(masked_image, config='--psm 11 --oem 3')

    # Imprimindo o texto reconhecido dos blocos laranja
    print(orange_text)

    # Reconhecendo o texto da imagem completa
    text = processor.recognize_text()
    print(text)

if __name__ == "__main__":
    main()