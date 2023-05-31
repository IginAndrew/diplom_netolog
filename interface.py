import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from core import *
from config import acces_token, comunity_token
from data_store import user_int_insert, user_int_off_insert, select_user_int, select_user_int_off, select_user_int_count


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
                            if (info[0]['sex']) == 2:
                                profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 1, offset)

                                for search in range((len(profiles))):
                                    profiles_big = self.tools.get_profile_info(profiles[search]["id"])
                                    print(profiles_big) # отладка
                                    if ((str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id'])))) and ((str(info[0]['id'])) not in select_user_int()):
                                        user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                        user_int_insert(int(info[0]['id']))
                                        photos = self.tools.photo_like(profiles[search]['id'])
                                        offset += search


                                        self.message_send((info[0]['id']),(f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
                                        for photo in photos:
                                            ower = photo['owner_id']
                                            photo_id = photo['id']
                                            media = f'photo{ower}_{photo_id}'


                                            self.message_send((info[0]['id']),  attachment=media)


                                    elif ((str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id'])))):

                                        user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                        photos = self.tools.photo_like(profiles[search]['id'])
                                        offset += search

                                        self.message_send((info[0]['id']), (f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
                                        for photo in photos:
                                            ower = photo['owner_id']
                                            photo_id = photo['id']
                                            media = f'photo{ower}_{photo_id}'

                                            self.message_send((info[0]['id']),  attachment=media)


                                self.message_send((info[0]['id']), 'для продолжения набери "далее "')
                            elif (info[0]['sex']) == 1:
                                profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 2, offset)
                                for search in range((len(profiles))):

                                    if ((str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id'])))) and ((str(info[0]['id'])) not in select_user_int()):
                                        user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                        user_int_insert(int(info[0]['id']))
                                        photos = self.tools.photo_like(profiles[search]['id'])
                                        offset += search

                                        self.message_send((info[0]['id']), (f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
                                        for photo in photos:
                                            ower = photo['owner_id']
                                            photo_id = photo['id']
                                            media = f'photo{ower}_{photo_id}'

                                            self.message_send((info[0]['id']), attachment=media)

                                    elif (str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id']))):
                                        user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                        photos = self.tools.photo_like(profiles[search]['id'])
                                        offset += search


                                        self.message_send((info[0]['id']),(f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
                                        for photo in photos:
                                            ower = photo['owner_id']
                                            photo_id = photo['id']
                                            media = f'photo{ower}_{photo_id}'

                                            self.message_send((info[0]['id']),attachment=media)


                                self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                    except KeyError:
                        self.message_send((info[0]['id']), 'укажи свое семейное положение в профиле')

                elif event.text.lower() in ('далее'):
                    if (info[0]['sex']) == 2 and info[0]['relation'] != 4:
                        profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 1, offset)
                        for search in range((len(profiles))):
                            offset += search
                            if (str(profiles[search]['id'])) in select_user_int_off((int(info[0]['id']))):

                                continue
                            user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                            photos = self.tools.photo_like(profiles[search]['id'])

                            self.message_send((info[0]['id']), (f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
                            for photo in photos:
                                ower = photo['owner_id']
                                photo_id = photo['id']
                                media = f'photo{ower}_{photo_id}'
                                self.message_send((info[0]['id']), attachment=media)


                        self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                    if (info[0]['sex']) == 1 and info[0]['relation'] != 4:
                        profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 2, offset)
                        for search in range((len(profiles))):
                            offset += search
                            if (str(profiles[search]['id'])) in select_user_int_off((int(info[0]['id']))):

                                continue
                            user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                            photos = self.tools.photo_like(profiles[search]['id'])

                            self.message_send((info[0]['id']), (f'{profiles[search]["name"]}, https://vk.com/id{profiles[search]["id"]}'))
                            for photo in photos:
                                ower = photo['owner_id']
                                photo_id = photo['id']
                                media = f'photo{ower}_{photo_id}'
                                self.message_send((info[0]['id']), attachment=media)


                        self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                else: 
                    self.message_send(event.user_id, 'неизвестная команда')



if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    bot.handler()




