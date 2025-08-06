import pathlib

import database.models


async def convert_payment_receipt_to_receipt_data(
    receipt: database.models.PaymentReceipt,
) -> dict:
    file_path = pathlib.Path(receipt.file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    file_bytes = file_path.read_bytes()
    encoded_file = file_bytes.decode("latin1")
    return {
        "filename": receipt.filename,
        "filebytes": encoded_file,
    }
