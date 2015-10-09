# coding=utf8
"""Tests for message formatting"""
from __future__ import unicode_literals

import pytest

from sopel.test_tools import MockSopel
from sopel import logger

@pytest.fixture
def bot():
    bot = MockSopel('Sopel')
    bot.config.core.logging_channel = '#Sopel'
    return bot


def test_sopel_logging(bot):
    logger.setup_logging(bot)
    log = logger.get_logger()
    log.info('Sopel')
    log = logger.get_logger(__name__)
    log.warn('Sopel')
    log.error('Sopel')
