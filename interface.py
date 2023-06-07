import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from core import *
from config import acces_token, comunity_token
from data_store import *
from datetime import date

class BotInterface():
    def __init__(self, token):
        self.tools = VkTools(acces_token)
        self.bot = vk_api.VkApi(token=token)




    def message_send(self, user_id, message=None,  attachment=None):
        name = self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment,
                        }
                        )

        return name


    def handler(self):
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                info = self.tools.get_profile_info(event.user_id)
                print(f'В бот зашел {info}')

                age = (info[0]['bdate'])
                age_my = self.calculate_age(int(age[-4:]))

                offset = 2 * select_user_int_count(int(info[0]['id']))
                if event.text.lower() in ('привет'):

                    if (str(info[0]['id'])) in select_user_int():

                        self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                    else:
                        user_int_insert(int(info[0]['id']))
                        self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                elif event.text.lower() in ('поиск'):

                    try:
                        if info[0]['relation'] != 4:
                            profiles = self.tools.user_serch((info[0]['city']['id']), age_my-5, age_my+5, self.sex_id(info[0]['sex']), offset)
                            for search in range((len(profiles))):
                                profiles_big = self.tools.get_profile_info(profiles[search]["id"])
                                print(profiles_big) # отладка
                                if ((str(profiles[search]['id'])) not in select_user_int_off(int(info[0]['id']))) and ((str(info[0]['id'])) not in select_user_int()) :
                                    user_int_insert(int(info[0]['id']))
                                    self.photo_list(profiles, info,search)


                                elif (str(profiles[search]['id'])) not in select_user_int_off(int(info[0]['id'])):
                                    self.photo_list(profiles, info, search)


                            self.message_send((info[0]['id']), 'Для продолжения наберите "далее"')
                    except KeyError:
                        self.message_send((info[0]['id']), 'Укажите свое семейное положение в профиле')

                elif event.text.lower() in ('далее'):

                    profiles = self.tools.user_serch((info[0]['city']['id']), age_my-5, age_my+5, self.sex_id(info[0]['sex']), offset)
                    for search in range((len(profiles))):
                        offset += search
                        if (str(profiles[search]['id'])) in select_user_int_off(int(info[0]['id'])):
                            continue
                        self.photo_list(profiles, info, search)

                    self.message_send((info[0]['id']), 'Для продолжения наберите "далее"')
                else: 
                    self.message_send(event.user_id, 'Неизвестная команда!!!')

    def photo_list(self, profiles, info, search):
        user_int_off_insert(int(profiles[search]['id']), (int(info[0]['id'])))
        photos = self.tools.photo_like(profiles[search]['id'])
        media_box = ''
        for photo in photos:
            ower = photo['owner_id']
            photo_id = photo['id']
            media = f'photo{ower}_{photo_id},'
            media_box += media
        print(media_box)
        self.message_send((info[0]['id']), (f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'), attachment=media_box)




    def sex_id(self, sex):
        if sex == 2:
            return 1
        else:
            return 2

    def calculate_age(self, year):
        today = date.today()
        return today.year - year



if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    bot.handler()




