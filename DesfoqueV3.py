import os
import cv2
import pytesseract
from telethon import TelegramClient, events
import asyncio

# Configurações do Telegram
api_id = "SEU_API_ID_AQUI"
api_hash = "SEU_API_HASH_AQUI"
phone_number = "+SEU_TELEFONE_AQUI"
group_name = "-100SEU_GRUPO_ID_AQUI"

# Configurações do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

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
        _, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Aplicando detecção de bordas para preservar as bordas dos textos
        edges = cv2.Canny(thresholded_image, 100, 200)

        # Dilatando a imagem para aumentar a espessura das bordas do texto
        dilated_image = cv2.dilate(edges, None, iterations=1)

        self.image = dilated_image

    def enhance_image(self):
        # Aplicando equalização de histograma adaptativa para melhorar o contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrasted_image = clahe.apply(cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)[:,:,0])
        contrasted_image = cv2.merge([contrasted_image]*3)

        # Aplicando equalização de histograma local para melhorar a nitidez
        local_contrast = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced_image = local_contrast.apply(contrasted_image)

        self.image = enhanced_image

    def recognize_text(self):
        # Convertendo a imagem para RGB para o Tesseract
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)

        # Reconhecendo o texto com Tesseract e retornando as palavras
        words = pytesseract.image_to_string(rgb_image, config='--psm 11 --oem 3').split()

        # Removendo caracteres especiais e espaços desnecessários
        cleaned_words = []
        for word in words:
            if word.isalnum() or word in ['-', '.', ',', '’', '‘', '“', '”']:
                cleaned_words.append(word)

        return ' '.join(cleaned_words)

async def get_group_messages():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter the code: '))

    group = await client.get_entity(group_name)
    date_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = date_today - timedelta(days=5)

    messages = []
    async for message in client.iter_messages(group, min_id=1):
        print(message.date, yesterday)
        if str(message.date) < str(yesterday):
            break
        messages.append(message)

    for message in messages:
        if message.media:
            file_id = message.media.photo.id
            file_info = await client.get_file(file_id)
            file_path = file_info.file_path
            file_name = re.sub(r'\W+', '_', message.text) + '.jpg'
            image_path = os.path.join('imagens', file_name)

            await client.download_file(file_path, image_path)

            processor = ImageProcessor(image_path)
            processor.remove_blur()
            processor.enhance_image()
            text = processor.recognize_text()
            print(f'Texto reconhecido: {text}')

asyncio.run(get_group_messages())