# coding=utf8
"""Tests for message parsing"""
from __future__ import unicode_literals

import re
import pytest

from sopel.test_tools import MockConfig
from sopel.trigger import PreTrigger, Trigger
from sopel.tools import Identifier


@pytest.fixture
def nick():
    return Identifier('Sopel')


def test_basic_pretrigger(nick):
    line = ':Foo!foo@example.com PRIVMSG #Sopel :Hello, world'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {}
    assert pretrigger.hostmask == 'Foo!foo@example.com'
    assert pretrigger.line == line
    assert pretrigger.args == ['#Sopel', 'Hello, world']
    assert pretrigger.event == 'PRIVMSG'
    assert pretrigger.nick == Identifier('Foo')
    assert pretrigger.user == 'foo'
    assert pretrigger.host == 'example.com'
    assert pretrigger.sender == '#Sopel'


def test_pm_pretrigger(nick):
    line = ':Foo!foo@example.com PRIVMSG Sopel :Hello, world'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {}
    assert pretrigger.hostmask == 'Foo!foo@example.com'
    assert pretrigger.line == line
    assert pretrigger.args == ['Sopel', 'Hello, world']
    assert pretrigger.event == 'PRIVMSG'
    assert pretrigger.nick == Identifier('Foo')
    assert pretrigger.user == 'foo'
    assert pretrigger.host == 'example.com'
    assert pretrigger.sender == Identifier('Foo')


def test_tags_pretrigger(nick):
    line = '@foo=bar;baz;sopel.chat/special=value :Foo!foo@example.com PRIVMSG #Sopel :Hello, world'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {'baz': None, 
                               'foo': 'bar', 
                               'sopel.chat/special': 'value'}
    assert pretrigger.hostmask == 'Foo!foo@example.com'
    assert pretrigger.line == line
    assert pretrigger.args == ['#Sopel', 'Hello, world']
    assert pretrigger.event == 'PRIVMSG'
    assert pretrigger.nick == Identifier('Foo')
    assert pretrigger.user == 'foo'
    assert pretrigger.host == 'example.com'
    assert pretrigger.sender == '#Sopel'


def test_intents_pretrigger(nick):
    line = '@intent=ACTION :Foo!foo@example.com PRIVMSG #Sopel :Hello, world'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {'intent': 'ACTION'}
    assert pretrigger.hostmask == 'Foo!foo@example.com'
    assert pretrigger.line == line
    assert pretrigger.args == ['#Sopel', 'Hello, world']
    assert pretrigger.event == 'PRIVMSG'
    assert pretrigger.nick == Identifier('Foo')
    assert pretrigger.user == 'foo'
    assert pretrigger.host == 'example.com'
    assert pretrigger.sender == '#Sopel'


def test_unusual_pretrigger(nick):
    line = 'PING'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {}
    assert pretrigger.hostmask == None
    assert pretrigger.line == line
    assert pretrigger.args == []
    assert pretrigger.event == 'PING'


def test_ctcp_intent_pretrigger(nick):
    line = ':Foo!foo@example.com PRIVMSG Sopel :\x01VERSION\x01'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {'intent': 'VERSION'}
    assert pretrigger.hostmask == 'Foo!foo@example.com'
    assert pretrigger.line == line
    assert pretrigger.args == ['Sopel', '']
    assert pretrigger.event == 'PRIVMSG'
    assert pretrigger.nick == Identifier('Foo')
    assert pretrigger.user == 'foo'
    assert pretrigger.host == 'example.com'
    assert pretrigger.sender == Identifier('Foo')


def test_ctcp_data_pretrigger(nick):
    line = ':Foo!foo@example.com PRIVMSG Sopel :\x01PING 1123321\x01'
    pretrigger = PreTrigger(nick, line)
    assert pretrigger.tags == {'intent': 'PING'}
    assert pretrigger.hostmask == 'Foo!foo@example.com'
    assert pretrigger.line == line
    assert pretrigger.args == ['Sopel', '1123321']
    assert pretrigger.event == 'PRIVMSG'
    assert pretrigger.nick == Identifier('Foo')
    assert pretrigger.user == 'foo'
    assert pretrigger.host == 'example.com'
    assert pretrigger.sender == Identifier('Foo')


def test_intents_trigger(nick):
    line = '@intent=ACTION :Foo!foo@example.com PRIVMSG #Sopel :Hello, world'
    pretrigger = PreTrigger(nick, line)

    config = MockConfig()
    config.core.owner = 'Foo'
    config.core.admins = ['Bar']

    fakematch = re.match('.*', line)

    trigger = Trigger(config, pretrigger, fakematch)
    assert trigger.sender == '#Sopel'
    assert trigger.raw == line
    assert trigger.is_privmsg == False
    assert trigger.hostmask == 'Foo!foo@example.com'
    assert trigger.user == 'foo'
    assert trigger.nick == Identifier('Foo')
    assert trigger.host == 'example.com'
    assert trigger.event == 'PRIVMSG'
    assert trigger.match == fakematch
    assert trigger.group == fakematch.group
    assert trigger.groups == fakematch.groups
    assert trigger.args == ['#Sopel', 'Hello, world']
    assert trigger.tags == {'intent': 'ACTION'}
    assert trigger.admin == True
    assert trigger.owner == True


# TODO tags, PRIVMSG to bot, intents
# TODO Trigger tests, for what little actual logic is in there
