import vk_api
from config import acces_token
from vk_api.exceptions import ApiError


class VkTools():
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)


    def get_profile_info(self, user_id):

        try:
            info = self.ext_api.method('users.get',
                                    {'user_id': user_id,
                                    'fields': 'bdate,city,sex,relation'
                                    }
                                    )
        except ApiError:
            return
        return info



    
    def user_serch(self, city_id, age_from, age_to, sex, offset = None):
    
        try:
            profiles = self.ext_api.method('users.search',
                                       {'city_id': city_id,
                                        'age_from': age_from,
                                        'age_to': age_to,
                                        'sex': sex,
                                        'count': 8,
                                        'offset': offset
                                        })

        except ApiError:
            return 

        profiles = profiles['items']
        
        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                              'id': profile['id']
                              })
                
        return result
    
    def photos_get(self, user_id):
        photos = self.ext_api.method('photos.get',
                                     {'album_id': 'profile',
                                      'owner_id': user_id,
                                      'extended': 1
                                     }
                                     )
        try:
            photos = photos['items']
        except KeyError:
            return

        result = []
        for num, photo in enumerate(photos):
            result.append({'owner_id': photo['owner_id'],
                           'id': photo['id'],
                           'extended': photo['likes']
                           })
            if num == 10:
                break

        return result

    def photo_like(self, id):
        total = []
        max_ = []
        photo = []
        ph = (self.photos_get(id))
        for i in ph:
            total.append(i)
        for j in total:
            max_.append(j['extended']['count'])
        arr = (sorted(max_, reverse=True)[:3])
        for i in range(len(total)):
            if total[i]['extended']['count'] in arr:
                photo.append(total[i])
        return photo



if __name__ == '__main__':
    tools = VkTools(acces_token)
    print(tools.photo_like(18078352))
    # ph = (tools.photos_get(18078352))
    # if ph:
    #     print(ph[0]['extended']['count'])
    #     for i in ph:
    #         print(i['extended']['count'])
    #

    # info = tools.get_profile_info(767605949)
    # if info:
    #     print(tools.get_profile_info(767605949))
    #     for i in info[0]:
    #         print (i)

    # else:
    #     print('Error')
    # profiles = tools.user_serch(4644, 20, 40, 1)
    # # print(profiles)
    # print(tools.user_serch(4644,20,40,2))

    # #
   



