import yaml
from slackclient import SlackClient

paramsFile = open('parameters.yml')
params = yaml.load(paramsFile, Loader=yaml.Loader)

SLACK_BOT_TOKEN = params['slack-bot-token']
BOT_USERNAME = params['bot-username']

slack_client = SlackClient(SLACK_BOT_TOKEN)


def get_user_id(users_dict, username):

    """
    Gets the user's id from the name
    :param users_dict: dict
    :param username: string
    :return: the slack user id
    :rtype string
    """
    for user in users_dict:
        if 'name' in user and user.get('name') == username:
            return user.get('id')


def get_users():

    """
    Fetches the users list
    :return:
    """
    users_list = slack_client.api_call("users.list")
    if users_list.get('ok'):
        return users_list.get('members')
    else:
        raise Exception("Unable to retrieve users")


if __name__ == "__main__":

    users = get_users()
    bot_id = get_user_id(users, BOT_USERNAME)
    if bot_id is None:
        raise Exception("Unable to find bot id")



