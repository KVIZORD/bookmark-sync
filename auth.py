import vk_api


def auth_handler():
    key = input("Код авторизации: ")
    remember_device = True

    return key, remember_device


def get_vk_api(login: str, password: str):
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

