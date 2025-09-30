from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message
import requests

router = Router()

# Хендлер pre_checkout_query
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    # или ok=False, error_message="Извините, товар закончился"

# Хендлер successful_payment
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    booking_payload = message.successful_payment.invoice_payload
    amount = message.successful_payment.total_amount
    # дергаем API бекенда и подтверждаем оплату
    requests.post("https://polya.top/api/bookings/confirm_payment/", json={
        "payload": booking_payload,
        "amount": amount,
        "telegram_charge_id": message.successful_payment.telegram_payment_charge_id,
    })
    await message.answer("✅ Оплата прошла успешно! Ваша бронь подтверждена.")
