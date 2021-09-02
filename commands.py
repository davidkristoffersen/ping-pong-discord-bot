from random import randint
import requests
import json
import html
from urllib import parse

underline = lambda x: '__' + x + '__'
bold = lambda x: '**' + x + '**'
italic = lambda x: '*' + x + '*'

#
#   All available commands
#
class Commands():
    def __init__(self):
        self.cmds = {
            'help': (self.help, ''),
            'test': (self.test, ''),
            'cmds': (self.cmds, ''),
            'print': (self.print_msg, '[some text]'),
            'prefix': (self.change_prefix, '[new prefix]'),
            'torstein': (self.torstein, ''),
            'david': (self.david, ''),
            'roll': (self.roll, ''),
            'color': (self.color, '[color] [some text]'),
            'yay_nay': (self.yay_nay, ''),
            'calc': (self.calc, '[math expression]'),
            'qa': (self.qa, ''),
            'even': (self.even, ''),
        }

        self.prefix = "p!"
        self.cmd_class = None
        self.cmd_content = None
        self.cmd_base = None
        self.cmd_args_list = None
        self.cmd_args_string = None

    # Help menu listing bot functionality
    def help(self):
        resp = "I am your personal Ping Pong bot!\n\n"
        resp += "Here is a list of all the things I can do\n\n"

        resp += 'Prefix: `' + self.prefix + '`\n\n'
        resp += 'Available commands:\n'
        resp += '- ' + '\n- '.join(['`' + key + '` ' + val[1] for key, val in self.cmds.items()])
        return resp

    def cmds(self):
        resp = '- `' + '`\n- `'.join(self.cmds.keys()) + '`'
        return resp

    # DEFAULT COMMANDS

    def cmd_default(self):
        return 'No such command: `' + self.cmd_base + '`'

    def test(self):
        return "This is a test response change"

    def color(self):
        try:
            colors = {
                        'pre': '```',
                        'red': 'excel\n',
                        'green': 'css\n',
                        'blue': 'elm\n',
                        'yellow': 'http\n',
                        'orange': 'arm\n',
                        'cyan': 'yaml\n',
                        'brown': 'fix\n',
                        'post': '```'
                     }
            col = self.cmd_args_list[0]
            msg = ' '.join(self.cmd_args_list[1:])
            return "Test of coloring: " + colors['pre'] + colors[col] + msg + colors['post']
        except:
            return 'Invalid color: `' + self.cmd_args_string + '`'

    # COMMANDS START HERE

    def print_msg(self):
        return self.cmd_args_string

    def change_prefix(self):
        if self.cmd_args_string == None:
            return '`' + self.prefix + "prefix [new prefix]`"

        new = self.cmd_args_list[0]
        self.prefix = new
        return "The prefix is now: `" + new + "`"

    def torstein(self):
        return "e slem :("

    def david(self):
        return "e deprimert..."

    def even(self):
        return "e trøtt \"_\""

    def roll(self):
        return randint(0, 100)

    def yay_nay(self):
        return ['Yay! :)', 'Nay :('][randint(0,1)]

    def calc(self):
        ops = self.cmd_args_list[1::2]
        vals = self.cmd_args_list[0::2]
        for op in ops:
            if not op in ['+', '-', '*', '**', '/']:
                return 'Invalid operand: `' + op + '`'
        for val in vals:
            try:
                int(val)
            except:
                try:
                    float(val)
                except:
                    return 'Invalid value: `' + val + '`'
        return eval(self.cmd_args_string)

    def qa(self):
        query = self.cmd_args_string
        try:
            ret = ''
            url = 'https://api.stackexchange.com/2.2/search/advanced?pagesize=1&order=desc&sort=activity&site=stackoverflow&filter=!2)zABJ)ZvP_ub7H(QhxI5&q=' + parse.quote_plus(query)
            question_data = json.loads(requests.get(url).text)
            quota_remaining = question_data['quota_remaining']
            question_data = question_data['items'][0]

            ret += underline(bold(question_data['title'])) + '\n'
            ret += question_data['link'] + '\n'

            answer_id = question_data['accepted_answer_id']

            url = 'https://api.stackexchange.com/2.2/answers/' + str(answer_id) + '?order=desc&sort=activity&site=stackoverflow&filter=!WXiXcHJ.E8QbM5nB9O-ckRJ6Qj.)-FZuxrzlSGf'
            answer_data = json.loads(requests.get(url).text)['items'][0]
            answer_owner = answer_data['owner']

            ret += italic(answer_owner['display_name'] + ' with reputation ' + str(answer_owner['reputation']) + ' wrote this answer with score ' + str(answer_data['score']) + ':' + '\n' + '\n')
            body = html.unescape(answer_data['body_markdown'])
            ret += body
            ret += 'Number of requests left: ' + bold(str(quota_remaining))
            return ret
        except:
            return 'No result or maybe the bot is broken'
