from app.core.config import settings
import qrcode
import os


QR_FOLDER = "static/qr"


def generate_qr(order_id: int, total_amount: int):
    os.makedirs(QR_FOLDER, exist_ok=True)
    content = f"upi://pay?pa={settings.UPI_ID}&am={total_amount}&tn=Order{order_id}"

    qr = qrcode.QRCode()
    qr.add_data(content)
    qr.make(fit=True)
    image = qr.make_image()
    file_path = f"{QR_FOLDER}/{order_id}.png"
    image.save(file_path)

    return file_path