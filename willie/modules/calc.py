# coding=utf8
"""
calc.py - Willie Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://willie.dfbta.net
"""
from __future__ import unicode_literals

import re
from willie import web
from willie.module import commands, example
from willie.tools import eval_equation
from socket import timeout
import sys
if sys.version_info.major < 3:
    import HTMLParser
else:
    import html.parser as HTMLParser


@commands('c', 'calc')
@example('.c 5 + 3', '8')
@example('.c 0.9*10', '9')
@example('.c 10*0.9', '9')
@example('.c 2*(1+2)*3', '18')
@example('.c 2**10', '1024')
@example('.c 5 // 2', '2')
@example('.c 5 / 2', '2.5')
def c(bot, trigger):
    """Evaluate some calculation."""
    if not trigger.group(2):
        return bot.reply("Nothing to calculate.")
    # Account for the silly non-Anglophones and their silly radix point.
    eqn = trigger.group(2).replace(',', '.')
    try:
        result = eval_equation(eqn)
        result = "{:.10g}".format(result)
    except ZeroDivisionError:
        result = "Division by zero is not supported in this universe."
    except Exception as e:
        result = "{error}: {msg}".format(error=type(e), msg=e)
    bot.reply(result)


@commands('py')
@example('.py len([1,2,3])', '3')
def py(bot, trigger):
    """Evaluate a Python expression."""
    if not trigger.group(2):
        return bot.say("Need an expression to evaluate")

    query = trigger.group(2)
    uri = 'http://tumbolia.appspot.com/py/'
    answer = web.get(uri + web.quote(query))
    if answer:
        bot.say(answer)
    else:
        bot.reply('Sorry, no result.')


if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
