from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callback.data import FoodData
from db import Repo
from db.models import User
from keyboards import user as kb

router = Router()

#@router.message()
#async def aaa(message: Message):
    #print(message)


@router.message(CommandStart())
async def start_com(message: Message, state: FSMContext, repo: Repo, user: User):
    await state.clear()
    if not user:
        await repo.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer_photo(photo="AgACAgIAAxkBAAIFGGRVIfnBhy1FunOCcM3rOZN4C506AAIyxjEb_0ipSlAg64UAAVEr7wEAAwIAA3kAAy8E", caption=f"Привіт, <b>{message.from_user.full_name}</b>!", reply_markup=kb.start())


@router.callback_query(F.data == "back")
async def main_menu(query: CallbackQuery):
    try:
        await query.message.edit_text("Ви в головному меню:", reply_markup=kb.start())
    except TelegramBadRequest:
        await query.message.delete()
        await query.message.answer("Ви в головному меню:", reply_markup=kb.start())


@router.callback_query(F.data == "veg")
async def vegetables(query: CallbackQuery):
    try:
        await query.message.edit_text("Оберіть фрукт: ", reply_markup=kb.veg())
    except TelegramBadRequest:
        await query.message.delete()
        await query.message.answer("Оберіть фрукт: ", reply_markup=kb.veg())


@router.callback_query(F.data == "junk")
async def junk_food(query: CallbackQuery):
    try:
        await query.message.edit_text("Оберіть фастфуд: ", reply_markup=kb.junk())
    except TelegramBadRequest:
        await query.message.delete()
        await query.message.answer("Оберіть фастфуд: ", reply_markup=kb.junk())


@router.callback_query(FoodData.filter())
async def add_food(query: CallbackQuery, repo: Repo, callback_data: FoodData, user: User):
    next_time = (datetime.now() + timedelta(hours=callback_data.cooldown)).strftime("%d/%m/%Y, %H:%M:%S")
    try:
        if datetime.strptime(user.history[callback_data.name], "%d/%m/%Y, %H:%M:%S") < datetime.now():
            user.inventory[callback_data.name] += 1
            user.history[callback_data.name] = next_time
            await repo.commit(user)
            try:
                await query.message.edit_text(
                    f"Ви отримали <b>{callback_data.name}</b>, тепер у Вас їх <b>{user.inventory[callback_data.name]}</b>.\n\n"
                    f"Через <b>{callback_data.cooldown} год. [{next_time}]</b> Ви зможете отримати ще раз.", reply_markup=query.message.reply_markup)
            except TelegramBadRequest:
                await query.message.delete()
                await query.message.answer(
                    f"Ви отримали <b>{callback_data.name}</b>, тепер у Вас їх <b>{user.inventory[callback_data.name]}</b>.\n\n"
                    f"Через <b>{callback_data.cooldown} год. [{next_time}]</b> Ви зможете отримати ще раз.", reply_markup=query.message.reply_markup)
        else:
            try:
                await query.message.edit_text(f"Ви вже отримали <b>{callback_data.name}</b>. Наступна можливість <b>{user.history[callback_data.name]}</b>.", reply_markup=query.message.reply_markup)
            except TelegramBadRequest:
                await query.message.delete()
                await query.message.answer(f"Ви вже отримали <b>{callback_data.name}</b>. Наступна можливість <b>{user.history[callback_data.name]}</b>.", reply_markup=query.message.reply_markup)
    except KeyError:
        user.inventory[callback_data.name], user.history[callback_data.name] = 1, next_time
        await repo.commit(user)
        try:
            await query.message.edit_text(
                f"Ви отримали <b>{callback_data.name}</b>, тепер у Вас їх <b>{user.inventory[callback_data.name]}</b>.\n\n"
                f"Через <b>{callback_data.cooldown} год. [{next_time}]</b> Ви зможете отримати ще раз.", reply_markup=query.message.reply_markup)
        except TelegramBadRequest:
            await query.message.delete()
            await query.message.answer(f"Ви отримали <b>{callback_data.name}</b>, тепер у Вас їх <b>{user.inventory[callback_data.name]}</b>.\n\n"
                f"Через <b>{callback_data.cooldown} год. [{next_time}]</b> Ви зможете отримати ще раз.", reply_markup=query.message.reply_markup)


@router.callback_query(F.data == "profile")
async def user_stats(query: CallbackQuery, user: User):
    try:
        await query.message.edit_text(f"ID:  <code>{user.id}</code>\n"
                                  f'Реєстрація:  <b>{user.creation_date.strftime("%d/%m/%Y, %H:%M:%S")}</b>\n' + ''.join(f'{name}:  <b>{user.inventory[name]}\n</b>' for name in sorted(user.inventory.keys())), reply_markup=kb.back())
    except Exception:
        await query.message.delete()
        await query.message.answer(f"ID:  <code>{user.id}</code>\n"
                                  f'Реєстрація:  <b>{user.creation_date.strftime("%d/%m/%Y, %H:%M:%S")}</b>\n' + ''.join(f'{name}:  <b>{user.inventory[name]}\n</b>' for name in sorted(user.inventory.keys())), reply_markup=kb.back())