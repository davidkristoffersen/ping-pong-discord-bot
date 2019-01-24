#!/usr/bin/env python3

import discord
from commands import Commands

class Bot(Commands):
    def __init__(self):
        super().__init__()

        self.response = None

    #   Base cmd parsing
    def run_cmd(self, cmd_class):
        self.cmd_class = cmd_class
        self.cmd_content = cmd_class.content
        if not self.cmd_content or not self.cmd_content.startswith(self.prefix) or len(self.cmd_content) == len(self.prefix):
            return

        self.cmd_content = self.cmd_content[len(self.prefix):]
        self.response = self.parse_cmd()

    def parse_cmd(self):
        cmd_list = self.cmd_content.split(' ')
        self.cmd_base = cmd_list[0]
        if len(cmd_list) > 1:
            self.cmd_args_list = cmd_list[1:]
            self.cmd_args_string = ' '.join(self.cmd_args_list)
        else:
            self.cmd_args_list = ['']
            self.cmd_args_string = ''
        func = self.get_cmd_func(self.cmd_base)
        return func()

    #   Getter methods
    def get_cmd_func(self, cmd):
        try:
            return self.cmds[cmd][0]
        except:
            return self.cmd_default

    @property
    def get_response(self):
        ret = self.response
        self.response = None
        return ret

if __name__ == "__main__":
    TOKEN = 'NTM3NjQzNjA3NTAzNTM2MTI4.Dyoorw.kZYgZa6M5bePpYfrNdwcP6nwk3E'

    client = discord.Client()

    @client.event
    async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        print(message.content)
        bot.run_cmd(message)

        response = bot.get_response
        if not response:
            return 
        await client.send_message(message.channel, response)

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    bot = Bot()
    client.run(TOKEN)
