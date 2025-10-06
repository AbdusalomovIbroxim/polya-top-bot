from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
import requests
from config import API_BASE_URL
router = Router()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    # или ok=False, error_message="Извините, товар закончился"

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    booking_payload = message.successful_payment.invoice_payload
    amount = message.successful_payment.total_amount
    # дергаем API бекенда и подтверждаем оплату
    requests.post(API_BASE_URL+"api/bookings/confirm_payment/", json={
        "payload": booking_payload,
        "amount": amount,
        "telegram_charge_id": message.successful_payment.telegram_payment_charge_id,
    })
    await message.answer("✅ Оплата прошла успешно! Ваша бронь подтверждена.")


from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message):
    user_id = message.from_user.id

    try:
        response = requests.post(
            API_BASE_URL+"api/users/check_admin_access/",
            json={"telegram_id": user_id},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        if data.get("allowed"):
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text="Открыть админку",
                        web_app=WebAppInfo(url=API_BASE_URL + "admin/")
                    )
                ]]
            )
            await message.answer("✅ Доступ подтверждён. Нажмите кнопку ниже:", reply_markup=keyboard)
        else:
            await message.answer("❌ У вас нет доступа к админке.")
    except requests.RequestException as e:
        await message.answer("⚠️ Не удалось проверить доступ. Попробуйте позже.")
        print(f"[ERROR] Admin command: {e}")
