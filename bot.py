
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder


TOKEN = "8615943132:AAHueXzfDkrUJV8ULUBwDrIvHJ4DDRaArRY"

bot = Bot(TOKEN)
dp = Dispatcher()


SHOP = {
    "synthetic": {
        "title": "🧪 Синтетические",
        "description": "меф кокаин",
        "items": [
            ("0.5г", 900, "меф,кокаин 0.5г"),
            ("1.0г", 1600, "меф,кокаин 1.0г"),
            ("2.0г", 3000, "меф,кокаин 2.0г"),
        ]
    },

    "medicines": {
        "title": "💊 Опиоиды",
        "description": "героин 2",
        "items": [
            ("0.5г", 1500, "героин 0.5г"),
            ("1.0г", 2700, "героин 1.0г"),
            ("2.0г", 4700, "героин 2.0г"),
        ]
    },

    "plants": {
        "title": "🌿 Растения",
        "description": "гашиш марихуана 3",
        "items": [
            ("0.5г", 300, "гашиш, марихуана 0.5г"),
            ("1.0г", 500, "гашиш, марихуана 1.0г"),
            ("2.0г", 900, "гашиш, марихуана 2.0г"),
        ]
    }
}


def main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="🐱 Шоп", callback_data="shop")
    builder.button(text="💳 Оплата", callback_data="payment")

    builder.adjust(1)

    return builder.as_markup()

def shop_menu():
    builder = InlineKeyboardBuilder()

    for key, category in SHOP.items():
        builder.button(
            text=category["title"],
            callback_data=f"category:{key}"
        )

    builder.button(text="◀️ Назад", callback_data="back_main")
    builder.adjust(1)

    return builder.as_markup()


def products_menu(category_name):
    builder = InlineKeyboardBuilder()

    items = SHOP[category_name]["items"]

    for index, item in enumerate(items):
        name = item[0]
        price = item[1]

        builder.button(
            text=f"{name} — {price} грн",
            callback_data=f"product:{category_name}:{index}"
        )

    builder.button(
        text="◀️ Назад",
        callback_data="shop"
    )

    builder.adjust(1)

    return builder.as_markup()


def product_menu(category_name, item_index):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🛒 Купить",
        callback_data=f"buy:{category_name}:{item_index}"
    )

    builder.button(
        text="◀️ Назад",
        callback_data=f"category:{category_name}"
    )

    builder.adjust(1)

    return builder.as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🐱 Добро пожаловать!\n\n"
        "Выбери действие:",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "shop")
async def shop(callback: CallbackQuery):
    await callback.message.edit_text(
        "🐱 Шоп\n\n"
        "Выбери категорию:",
        reply_markup=shop_menu()
    )

    await callback.answer()


@dp.callback_query(F.data.startswith("category:"))
async def category(callback: CallbackQuery):
    category_name = callback.data.split(":", 1)[1]
    category_data = SHOP[category_name]

    await callback.message.edit_text(
        f"{category_data['title']}\n\n"
        f"{category_data['description']}\n\n"
        "Выбери товар:",
        reply_markup=products_menu(category_name)
    )

    await callback.answer()


@dp.callback_query(F.data.startswith("product:"))
async def product(callback: CallbackQuery):
    parts = callback.data.split(":")

    category_name = parts[1]
    item_index = int(parts[2])

    item = SHOP[category_name]["items"][item_index]

    name = item[0]
    price = item[1]
    description = item[2]

    await callback.message.edit_text(
        f"🛒 {name}\n\n"
        f"📖 {description}\n\n"
        f"💰 Цена: {price} грн",
        reply_markup=product_menu(category_name, item_index)
    )

    await callback.answer()


@dp.callback_query(F.data.startswith("buy:"))
async def buy(callback: CallbackQuery):
    parts = callback.data.split(":")

    category_name = parts[1]
    item_index = int(parts[2])

    item = SHOP[category_name]["items"][item_index]

    name = item[0]

    await callback.answer(
        f"Выбран товар: {name}",
        show_alert=True
    )


@dp.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад", callback_data="back_main")

    await callback.message.edit_text(
        "💳 Оплата\n\n"
        "Для оплаты пиши:\n"
        "@Bfftvv",
        reply_markup=builder.as_markup()
    )

    await callback.answer()
@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🐱 Главное меню\n\n"
        "Выбери действие:",
        reply_markup=main_menu()
    )

    await callback.answer()


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())