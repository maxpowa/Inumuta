# coding=utf8
"""
blame.py - Don't blame $nickname :V
Copyright 2014 Max Gurela

Licensed under the Eiffel Forum License 2.
"""

from willie.module import rule

@rule('#blame$nickname')
def blame(bot, trigger):
    bot.action('dies a little inside')