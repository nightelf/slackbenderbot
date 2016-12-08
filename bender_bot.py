import yaml, pprint, time, dialogue, os
from slackclient import SlackClient
from dialogue.comment import Comment
from dialogue.matcher import DialogueMatcher
from dialogue.synonym import SynonymIndex
from dialogue.response import ResponseIndex

paramsFile = open('parameters.yml')
params = yaml.load(paramsFile, Loader=yaml.Loader)

SLACK_BOT_TOKEN = params['slack-bot-token']
BOT_USERNAME = params['bot-username']

MESSAGE_TYPE_HELLO = 'hello'
MESSAGE_TYPE_PRESENCE = 'presence_change'
MESSAGE_TYPE_MESSAGE = 'message'
MESSAGE_TYPE_USER_TYPING = 'user_typing'

PRESENCE_AWAY = 'away'
PRESENCE_ACTIVE = 'active'

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
    users_response = slack_client.api_call("users.list")
    if users_response.get('ok'):
        return users_response.get('members')
    else:
        raise Exception("Unable to retrieve users")


def format_user_id(user_id):
    return '<@' + user_id + '>'


if __name__ == "__main__":

    users = get_users()
    bot_id = get_user_id(users, BOT_USERNAME)
    if bot_id is None:
        raise Exception("Unable to find bot id")

    synonym_index = SynonymIndex()
    response_index = ResponseIndex(synonym_index=synonym_index)
    matcher = DialogueMatcher(synonym_index=synonym_index, response_index=response_index)

    if slack_client.rtm_connect():
        print("Bender running")
        while True:
            messages = slack_client.rtm_read()
            for message in messages:
                response = None
                if message and message['type'] == MESSAGE_TYPE_MESSAGE:
                    comment = Comment(message['text'])
                    kwargs = {'commentee_name': format_user_id(bot_id), 'commenter_name': format_user_id(message['user'])}
                    response = matcher.match(comment=comment, **kwargs)

                if response is not None:
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text=response,
                        as_user=True)
            time.sleep(1)



