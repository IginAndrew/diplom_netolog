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




    def message_send(self, user_id, message=None, attachment=None):
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
                offset = 2 * select_user_int_count(int(info[0]['id']))
                if event.text.lower() in ('привет', 'ghbdtn'):
                    # info = self.tools.get_profile_info(event.user_id)
                    if (str(info[0]['id'])) in select_user_int():
                    # user_int_insert(int(info[0]['id']))
                        self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                    else:
                        user_int_insert(int(info[0]['id']))
                        self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                elif event.text.lower() in ('поиск', 'gjbcr'):
                    if info[0]['relation'] != 4:
                        if (info[0]['sex']) == 2:
                            profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 1, offset)
                            for search in range((len(profiles))):
                                print(str(profiles[search]['id']))
                                if ((str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id'])))) and ((str(info[0]['id'])) not in select_user_int()):
                                    user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                    user_int_insert(int(info[0]['id']))
                                    photos = self.tools.photo_like(profiles[search]['id'])
                                    offset += search
                                    for i in photos:
                                        ower = i['owner_id']
                                        photo_id = i['id']
                                        media = f'photo{ower}_{photo_id}'
                                        print(ower, photo_id)
                                        self.message_send((info[0]['id']), (profiles[search]['name']), attachment=media)
                                elif ((str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id'])))):
                                    print(int(profiles[search]['id']))
                                    user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                    photos = self.tools.photo_like(profiles[search]['id'])
                                    offset += search
                                    for i in photos:
                                        ower = i['owner_id']
                                        photo_id = i['id']
                                        media = f'photo{ower}_{photo_id}'
                                        print(ower, photo_id)
                                        self.message_send((info[0]['id']), (profiles[search]['name']), attachment=media)
                            self.message_send((info[0]['id']), 'для продолжения набери "далее "')
                        elif (info[0]['sex']) == 1:
                            profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 2, offset)
                            for search in range((len(profiles))):
                                print(str(profiles[search]['id']))
                                if ((str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id'])))) and ((str(info[0]['id'])) not in select_user_int()):
                                    user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                    user_int_insert(int(info[0]['id']))
                                    photos = self.tools.photo_like(profiles[search]['id'])
                                    offset += search
                                    for i in photos:
                                        ower = i['owner_id']
                                        photo_id = i['id']
                                        media = f'photo{ower}_{photo_id}'
                                        print(ower, photo_id)
                                        self.message_send((info[0]['id']), (profiles[search]['name']), attachment=media)

                                elif (str(profiles[search]['id'])) not in select_user_int_off((int(info[0]['id']))):
                                    user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                                    photos = self.tools.photo_like(profiles[search]['id'])
                                    offset += search
                                    for i in photos:
                                        ower = i['owner_id']
                                        photo_id = i['id']
                                        media = f'photo{ower}_{photo_id}'
                                        print(ower, photo_id)
                                        self.message_send((info[0]['id']), (profiles[search]['name']), attachment=media)
                            self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                    else:
                        self.message_send((info[0]['id']), 'укажи свое семейное положение')

                elif event.text.lower() in ('далее', 'lfktt'):
                    if (info[0]['sex']) == 2 and info[0]['relation'] != 4:
                        profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 1, offset)
                        for search in range((len(profiles))):
                            offset += search
                            if (str(profiles[search]['id'])) in select_user_int_off((int(info[0]['id']))):

                                continue
                            user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                            photos = self.tools.photo_like(profiles[search]['id'])
                            for i in photos:
                                ower = i['owner_id']
                                photo_id = i['id']
                                media = f'photo{ower}_{photo_id}'
                                self.message_send((info[0]['id']), (profiles[search]['name']), attachment=media)
                        self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                    if (info[0]['sex']) == 1 and info[0]['relation'] != 4:
                        profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 2, offset)
                        for search in range((len(profiles))):
                            offset += search
                            if (str(profiles[search]['id'])) in select_user_int_off((int(info[0]['id']))):

                                continue
                            user_int_off_insert((int(profiles[search]['id'])), (int(info[0]['id'])))
                            photos = self.tools.photo_like(profiles[search]['id'])
                            for i in photos:
                                ower = i['owner_id']
                                photo_id = i['id']
                                media = f'photo{ower}_{photo_id}'
                                self.message_send((info[0]['id']), (profiles[search]['name']), attachment=media)
                        self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                else: 
                    self.message_send(event.user_id, 'неизвестная команда')



if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    bot.handler()




