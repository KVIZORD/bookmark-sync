import vk_api
from vk_api.longpoll import VkLongPoll


def auth_handler():
    key = input("Код авторизации: ")
    remember_device = True

    return key, remember_device


def get_profile_api(login: str, password: str):
    login = login
    password = password

    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    return vk


def get_wall_by_id(session: vk_api.vk_api.VkApiMethod, owner_id: str, post_id: str):
    posts = owner_id + '_' + post_id

    response = session.wall.getById(posts=posts)

    print(response)


def get_longpoll(group_token: str):

    session = vk_api.VkApi(token=group_token)
    longpoll = VkLongPoll(session)

    return longpoll




