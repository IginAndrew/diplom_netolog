import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from core import *
from config import acces_token, comunity_token



class BotInterface():
    def __init__(self, token):
        self.tools = VkTools(acces_token)
        self.bot = vk_api.VkApi(token=token)




    def message_send(self, user_id, message=None, attachment=None):
        name = self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                        }
                        )

        return name


    def handler(self):
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день! Для поиска пары наберите слово "поиск"')
                elif event.text.lower() in ('поиск', 'далее'):
                    info = self.tools.get_profile_info(event.user_id)
                    if info[0]['relation'] != 4:
                        if (info[0]['sex']) == 2:
                            profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 1)
                            for search in range(len(profiles)):
                                photos = self.tools.photos_get(profiles[search]['id'])
                                for i in photos:
                                    ower = i['owner_id']
                                    photo_id = i['id']
                                    media = f'photo{ower}_{photo_id}'
                                    print(ower, photo_id)
                                    self.message_send((info[0]['id']), 'фото', attachment=media)
                                # media = f'photo{ower}_{photo_id}'
                                # self.message_send((info[0]['id']),'фото', attachment=media)
                            self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                        elif (info[0]['sex']) == 1:
                            profiles = self.tools.user_serch((info[0]['city']['id']), 20, 40, 2)
                            for search in range(len(profiles)):
                                photos = self.tools.photos_get(profiles[search]['id'])
                                for i in photos:
                                    ower = i['owner_id']
                                    photo_id = i['id']
                                    media = f'photo{ower}_{photo_id}'
                                    print(ower, photo_id)
                                    self.message_send((info[0]['id']), 'фото', attachment=media)
                            self.message_send((info[0]['id']), 'для продолжения набери "далее"')
                elif event.text.lower() == 'далее':
                    pass
                else: 
                    self.message_send(event.user_id, 'неизвестная команда')



if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    bot.handler()




