from botcity.plugins.discord import BotDiscordPlugin, EmbeddedMessage, Author, Footer, Field, Color

import time


def test_send_message(bot: BotDiscordPlugin):
    res = bot.send_message(content='Hello')
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204

def test_send_message_with_file(bot: BotDiscordPlugin, tmp_file: str,):
    res = bot.send_message(content='Hello!', files=[tmp_file] )
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204

def test_send_message_with_file_in_bytes(bot: BotDiscordPlugin, tmp_file_in_bytes: str):
    res = bot.send_message(content='Hello!', files={"test": tmp_file_in_bytes})
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204

def test_send_complex_message(bot: BotDiscordPlugin):
    msg = EmbeddedMessage(title='Title Embedded', description='Long Description.', color=Color.ORANGE)

    msg.author = Author(
        name='Botcity',
        url='https://github.com/botcity-dev',
        icon_url='https://avatars.githubusercontent.com/u/72993825?s=200&v=4'
    )

    msg.footer = Footer(
        text='Footer text example',
        icon_url='https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png'  
    )

    msg.fields = [Field(name='Field 1', value='Value 1'), Field(name='Field 2', value='Value 2')]

    msg.thumbnail = 'https://pbs.twimg.com/profile_images/1374747222353575944/7kS6IhZb_400x400.jpg'

    msg.image = 'https://cdn-icons-png.flaticon.com/512/2111/2111370.png'  

    res = bot.send_embedded_message(msg)
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204


def test_send_complex_message_with_color_and_timestamp_as_none(bot: BotDiscordPlugin):
    msg = EmbeddedMessage(title='Title Embedded', description='Long Description.', color=None, timestamp=None)
    res = bot.send_embedded_message(msg)
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204


def test_send_complex_message_with_file(bot: BotDiscordPlugin, tmp_file: str):
    msg = EmbeddedMessage(title='Title Embedded', description='Long Description.', color=Color.ORANGE, files=[tmp_file])
    res = bot.send_embedded_message(msg)
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204

def test_send_complex_message_with_file_in_bytes(bot: BotDiscordPlugin, tmp_file_in_bytes: str):
    msg = EmbeddedMessage(title='Title Embedded', description='Long Description.', color=Color.ORANGE, files={"test": tmp_file_in_bytes})
    res = bot.send_embedded_message(msg)
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204

def test_edit_message(bot: BotDiscordPlugin):
    first_message_response = bot.send_message(content='Hello!')
    updated_message_response = bot.edit_message(first_message_response, 'New content.')
    res_delete = bot.delete_message_edited(updated_message_response)
    assert updated_message_response.status_code == 200 or 204
    assert res_delete.status_code == 200 or 204


def test_send_file(bot: BotDiscordPlugin, tmp_file: str):
    res = bot.send_file(files=[tmp_file])
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204

def test_delete_message_and_file(bot: BotDiscordPlugin):
    res = bot.send_message(content='Hello!')
    time.sleep(5)
    res_delete = bot.delete_message(res)
    assert res.status_code == 200
    assert res_delete.status_code == 200 or 204
