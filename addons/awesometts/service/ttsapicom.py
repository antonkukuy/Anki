# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
#
# Copyright (C) 2014       Anki AwesomeTTS Development Team
# Copyright (C) 2014       Dave Shifflett
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Service implementation for TTS-API.com
"""

__all__ = ['TTSAPICom']

from .base import Service
from .common import Trait


class TTSAPICom(Service):
    """
    Provides a Service-compliant implementation for TTS-API.com.
    """

    __slots__ = [
    ]

    NAME = "TTS-API.com"

    TRAITS = [Trait.INTERNET]

    def desc(self):
        """
        Returns a short, static description.
        """

        return "TTS-API.com (English only)"

    def options(self):
        """
        Provides access to voice only -- sort of -- only English is
        supported, so the user does not have much choice in the matter.
        """

        return [
            dict(
                key='voice',
                label="Voice",
                values=[
                    ('en', "English (en)"),
                ],
                transform=lambda value: (
                    'en' if self.normalize(value).startswith('en')
                    else value
                ),
                default='en',
            ),
        ]

    def run(self, text, options, path):
        """
        Downloads from TTS-API.com directly to an MP3.
        """

        assert options['voice'] == 'en', "Only English is supported"

        self.net_download(
            path,
            [
                ('http://tts-api.com/tts.mp3', dict(
                    q=subtext,
                ))

                # n.b. safe limit of 750, but actual limit is higher
                for subtext in self.util_split(text, 750)
            ],
            require=dict(mime='audio/mpeg', size=256),
        )
