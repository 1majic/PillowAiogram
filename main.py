import os
from typing import Union

from PIL import Image
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor


from keyboards import markups
import config as cfg
from Pillow.make_image import make_image
from Pillow.TPDNE_generator import makeRequest
from utils.utils import States
import io

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
photo = ''
data = ''


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = markups.start_keyboard()
    await message.answer('Привет!', reply_markup=keyboard)


@dp.message_handler(text='Создать новый документ')
async def AddNewDoc(message: types.Message):
    await States.ADD_NEW_DOC.set()
    await message.answer('Отправьте данные в таком формате\n имя|фамилия|отчество|пол|дата рождения|страна')


@dp.callback_query_handler(state=States.ADD_NEW_DOC, text='reload')
async def reload(callback: types.CallbackQuery, state: FSMContext):
    await GenPhoto(callback, state)


@dp.message_handler(state=States.ADD_NEW_DOC)
async def GenPhoto(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    global photo, data
    keyboard = markups.photo_keyboard()
    photo = makeRequest()
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
    else:
        data = message.text
    await bot.send_photo(message.from_user.id, photo, reply_markup=keyboard)


@dp.callback_query_handler(state=States.ADD_NEW_DOC, text='success')
async def successphoto(callback: types.CallbackQuery, state: FSMContext):
    image = Image.open(io.BytesIO(photo))
    await GenNewDoc(callback.message, image, state)


@dp.message_handler(state=States.ADD_NEW_DOC, content_types=['photo'])
async def getPhoto(message: types.Message, state: FSMContext):
    global data
    data = message.text
    await GenNewDoc(message, message.photo[0].download(destination_file='Pillow/image.jpg'), state)


async def GenNewDoc(message: types.Message, photo, state: FSMContext):
    name, surname, middle_name, sex, date, county = data.split('|')
    image = make_image(photo, name, surname, middle_name, sex, date, county)
    image.save("Pillow/image.jpg", format='JPEG')
    await message.answer_photo(open("Pillow/image.jpg", 'rb'))
    await message.delete()
    os.remove("Pillow/image.jpg")
    await state.finish()


@dp.message_handler()
async def get_image(message: types.Message):
    try:
        photo = make_image(message.text)
        photo.save("Pillow/image.jpg", format='JPEG')
        await message.answer_photo(open("Pillow/image.jpg", 'rb'), caption='Готово!')
        os.remove("Pillow/image.jpg")
    except:
        pass


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_shutdown=shutdown)
