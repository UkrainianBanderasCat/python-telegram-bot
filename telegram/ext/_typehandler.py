#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2022
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains the TypeHandler class."""

from typing import Type, TypeVar

from telegram._utils.types import DVInput
from telegram.ext import Handler
from telegram.ext._utils.types import CCT, HandlerCallback
from telegram._utils.defaultvalue import DEFAULT_TRUE

RT = TypeVar('RT')
UT = TypeVar('UT')


class TypeHandler(Handler[UT, CCT]):
    """Handler class to handle updates of custom types.

    Warning:
        When setting ``block`` to :obj:`True`, you cannot rely on adding custom
        attributes to :class:`telegram.ext.CallbackContext`. See its docs for more info.

    Args:
        type (:obj:`type`): The ``type`` of updates this handler should process, as
            determined by ``isinstance``
        callback (:obj:`callable`): The callback function for this handler. Will be called when
            :attr:`check_update` has determined that an update should be processed by this handler.
            Callback signature: ``def callback(update: Update, context: CallbackContext)``

            The return value of the callback is usually ignored except for the special case of
            :class:`telegram.ext.ConversationHandler`.
        strict (:obj:`bool`, optional): Use ``type`` instead of ``isinstance``.
            Default is :obj:`False`
        block (:obj:`bool`): Determines whether the return value of the callback should be
            awaited before processing the next handler in
            :meth:`telegram.ext.Dispatcher.process_update`. Defaults to :obj:`True`.

    Attributes:
        type (:obj:`type`): The ``type`` of updates this handler should process.
        callback (:obj:`callable`): The callback function for this handler.
        strict (:obj:`bool`): Use ``type`` instead of ``isinstance``. Default is :obj:`False`.
        block (:obj:`bool`): Determines whether the return value of the callback should be
            awaited before processing the next handler in
            :meth:`telegram.ext.Dispatcher.process_update`.

    """

    __slots__ = ('type', 'strict')

    def __init__(
        self,
        type: Type[UT],  # pylint: disable=redefined-builtin
        callback: HandlerCallback[UT, CCT, RT],
        strict: bool = False,
        block: DVInput[bool] = DEFAULT_TRUE,
    ):
        super().__init__(callback, block=block)
        self.type = type  # pylint: disable=assigning-non-slot
        self.strict = strict  # pylint: disable=assigning-non-slot

    def check_update(self, update: object) -> bool:
        """Determines whether an update should be passed to this handlers :attr:`callback`.

        Args:
            update (:obj:`object`): Incoming update.

        Returns:
            :obj:`bool`

        """
        if not self.strict:
            return isinstance(update, self.type)
        return type(update) is self.type  # pylint: disable=unidiomatic-typecheck
