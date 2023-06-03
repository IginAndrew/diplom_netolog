import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from core import *
from config import acces_token, comunity_token
from data_store import *


class BotInterface():
    def __init__(self, token):
        self.tools = VkTools(acces_token)
        self.bot = vk_api.VkApi(token=token)




    def message_send(self, user_id, message=None, message1=None, attachment=None):
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
                offset = 2 * select_user_int_count(con, int(info[0]['id']))
                if event.text.lower() in ('привет'):

                    if (str(info[0]['id'])) in select_user_int(con):

                        self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                    else:
                        user_int_insert(con, int(info[0]['id']))
                        self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                elif event.text.lower() in ('поиск'):
                    # self.message_send(event.user_id, "Укажите минимальный возраст будущей пары!")
                    # min_age = event.text()
                    try:
                        if info[0]['relation'] != 4:
                            profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, self.sex_id(info[0]['sex']), offset)
                            for search in range((len(profiles))):
                                profiles_big = self.tools.get_profile_info(profiles[search]["id"])
                                print(profiles_big) # отладка
                                if ((str(profiles[search]['id'])) not in select_user_int_off(con, (int(info[0]['id'])))) and ((str(info[0]['id'])) not in select_user_int(con)):
                                    user_int_insert(con, int(info[0]['id']))
                                    self.photo_list(profiles, info,search)


                                elif (str(profiles[search]['id'])) not in select_user_int_off(con, (int(info[0]['id']))):
                                    self.photo_list(profiles, info, search)


                            self.message_send((info[0]['id']), 'Для продолжения наберите "далее"')
                    except KeyError:
                        self.message_send((info[0]['id']), 'Укажите свое семейное положение в профиле')

                elif event.text.lower() in ('далее'):

                    profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, self.sex_id(info[0]['sex']), offset)
                    for search in range((len(profiles))):
                        offset += search
                        if (str(profiles[search]['id'])) in select_user_int_off(con, (int(info[0]['id']))):
                            continue
                        self.photo_list(profiles, info, search)

                    self.message_send((info[0]['id']), 'Для продолжения наберите "далее"')
                else: 
                    self.message_send(event.user_id, 'Неизвестная команда!!!')

    def photo_list(self, profiles, info, search):
        user_int_off_insert(con, (int(profiles[search]['id'])), (int(info[0]['id'])))
        photos = self.tools.photo_like(profiles[search]['id'])
        self.message_send((info[0]['id']), (f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
        for photo in photos:
            ower = photo['owner_id']
            photo_id = photo['id']
            media = f'photo{ower}_{photo_id}'
            self.message_send((info[0]['id']), attachment=media)

    def sex_id(self, sex):
        if sex == 2:
            return 1
        else:
            return 2



if __name__ == '__main__':
    # con = get_connection()
    bot = BotInterface(comunity_token)
    bot.handler()




