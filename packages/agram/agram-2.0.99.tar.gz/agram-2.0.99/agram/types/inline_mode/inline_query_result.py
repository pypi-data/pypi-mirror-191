#  agram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of agram.
#
#  agram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  agram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with agram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import agram
from agram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~agram.types.InlineQueryResultCachedAudio`
    - :obj:`~agram.types.InlineQueryResultCachedDocument`
    - :obj:`~agram.types.InlineQueryResultCachedAnimation`
    - :obj:`~agram.types.InlineQueryResultCachedPhoto`
    - :obj:`~agram.types.InlineQueryResultCachedSticker`
    - :obj:`~agram.types.InlineQueryResultCachedVideo`
    - :obj:`~agram.types.InlineQueryResultCachedVoice`
    - :obj:`~agram.types.InlineQueryResultArticle`
    - :obj:`~agram.types.InlineQueryResultAudio`
    - :obj:`~agram.types.InlineQueryResultContact`
    - :obj:`~agram.types.InlineQueryResultDocument`
    - :obj:`~agram.types.InlineQueryResultAnimation`
    - :obj:`~agram.types.InlineQueryResultLocation`
    - :obj:`~agram.types.InlineQueryResultPhoto`
    - :obj:`~agram.types.InlineQueryResultVenue`
    - :obj:`~agram.types.InlineQueryResultVideo`
    - :obj:`~agram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "agram.Client"):
        pass
