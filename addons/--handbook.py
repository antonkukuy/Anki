# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/handbook.html
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# -- Справочник 2.0
#
from __future__ import division
from __future__ import unicode_literals
import os, urllib, re

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from aqt import mw
from aqt.utils import *

icons_dir = os.path.join(mw.pm.addonFolder(), 'handbook')


######################
# Activation
#
JustDoIt = True
#JustDoIt = False

######################
# Get language class
#
import anki.lang
lang = anki.lang.getLang()

if lang in ['ru','en']:
   bells_and_whistles = True
#   bells_and_whistles = False
# Turn it off if you don't need it anyway; even if you start with this language.
else:
   bells_and_whistles = False

def go_writing():
    openLink("http://ankisrs.net/docs/addons.html")

def go_AnkiTest():
    openLink("http://finpapa.ucoz.ru/index.html")

def go_HandBook():
    if QDesktopServices.openUrl(QUrl("file:///"+os.path.join(mw.pm.addonFolder(),'handbook',lang if lang in ['ru','en'] else "","index.htm"))):
        tooltip('Запускается в браузере...')
        return True
    else:
        tooltip('Упс, что-то пошло не так.<br><br> &nbsp; <i>Факир был пьян и фокус не удался.</i>') # \n don't work here
        return False
    

######################
# Just Do It! 
# [ʤʌst duː ɪt]
# Просто Добавь Воды!
#
if JustDoIt:
    writing_action = QAction(mw)
    writing_action.setText(u"&Написание дополнений" if lang=="ru" else u"&Writing add-ons")
    mw.connect(writing_action, SIGNAL("triggered()"), go_writing)
    mw.form.menuHelp.addAction(writing_action)

    if bells_and_whistles and lang=='ru':
        local_help_action = QAction(mw)
        local_help_action.setText(u'Открыть &локальный Справочник по Anki 2.0 на диске' if lang=='ru' 
            else _(u"Open &local Anki 2.0 HandBook"))
        local_help_action.setIcon(QIcon(os.path.join(icons_dir, 'handbook.png')))
        mw.connect(local_help_action, SIGNAL("triggered()"), go_HandBook)

        mw.form.menuHelp.addSeparator()
        mw.form.menuHelp.addAction(local_help_action)

        helpful_action = QAction(mw)
        helpful_action.setText(u'Открыть &сайт Справочника по Anki 2.0' if lang=='ru' else _(u"&Open Anki 2.0 HandBook"))
        helpful_action.setIcon(QIcon(os.path.join(icons_dir, 'green_tick_16.png')))
        mw.connect(helpful_action, SIGNAL("triggered()"), go_AnkiTest)
        mw.form.menuHelp.addAction(helpful_action)


