import vk_api
import configparser


def auth_handler() -> tuple:
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

    profile_api = vk_session.get_api()

    return profile_api


def get_post_by_id(session: vk_api.vk_api.VkApiMethod, posts: str):
    response = session.wall.getById(posts=posts)
    return response


def get_group_api(group_token: str):
    token = group_token
    session = vk_api.VkApi(token=token)
    group_api = session.get_api()

    return group_api


def get_count_unread_messages(session: vk_api.vk_api.VkApiMethod, dialog_id: str):
    dialog_list = session.messages.getConversations()
    unread_count = 0

    for dialog in dialog_list['items']:
        if str(dialog['conversation']['peer']['id']) == dialog_id:
            if 'unread_count' in dialog_list['items'][0]['conversation']:
                unread_count = dialog_list['items'][0]['conversation']['unread_count']

    return unread_count


def get_filtered_messages(session: vk_api.vk_api.VkApiMethod, filters: list, count: int, dialog_id: str):
    """Функция возвращает все сообщения, содержащие одну из подстрок filter. Отмечает их, как прочитанные"""

    filtered_messages = []
    message_history = session.messages.getHistory(count=count, user_id=dialog_id)
    read_messages_id = []
    for message in message_history['items']:
        read_messages_id.append(message['id'])
        for filter in filters:
            if filter in message['text'].lower():
                filtered_messages.append(message)

    session.messages.markAsRead(peer_id=215916167, start_message_id=read_messages_id[0])

    return filtered_messages


def test():
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get('auth_data', 'vk_group_token')
    group_api = get_group_api(token)
    user_id = config.get('auth_data', 'vk_id')
    count = get_count_unread_messages(group_api, user_id)
    if count != 0:
        for i in get_filtered_messages(group_api, ['-з', '-p'], count, user_id):
            print(i)
    else:
        print('Новых закладок не обнаружено')


test()
