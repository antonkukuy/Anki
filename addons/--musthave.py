# -*- mode: Python ; coding: utf-8 -*-
# • Must Have
# https://ankiweb.net/shared/info/67643234
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# -- MUST HAVE -- All-in-1 SuperPack -- 67643234 -- 
# -- ANKI add-on -- highly configurable addon --
# I did my best, let anybody do better.

# actionDownloadSharedPlugin
# main.onGetSharedPlugin -- addons.onGetAddons

from __future__ import division
from __future__ import unicode_literals
import os, sys, urllib, re

if __name__ == "__main__":
    print("This is THE add-on for the Anki program and it can't be run directly.")
    print("Please download Anki 2.0 from http://ankisrs.net/")
    sys.exit()
else:
    # Save a reference to the toolkit onto the mw, preventing garbage collection of PyQT objects
    #if mw: ... # AnkiBelt AnkiLevel
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already.
  if hasattr(sys,'setdefaultencoding'):
    #reload(sys)
    sys.setdefaultencoding('utf8')

##########################################
#
import datetime, time, io, json
from datetime import datetime, timedelta

import copy

from anki.collection import _Collection
from anki.utils import fmtTimeSpan, ids2str

# NB! QKeySequence("Ctrl+PgUp") but Qt.CTRL + Qt.PageUp 
# --  on Mac Meta+SomeKey automatically converted to Ctrl+SomeKey

# Traceback (most recent call last):
#   File "C:\Users\Anki\Documents\Anki2\addons\--Must_Have.py", line 792, in go_edit_layout
#     clayout.CardLayout(mw, ccard.note(), ord=ccard.ord)
# NameError: global name 'clayout' is not defined

from aqt import mw, clayout, browser, editor 
# -- NameError: global name 'clayout' is not defined 
# -- when next line was commented after adding next line with * -- why?
from aqt import * 
# import the main window object (mw) from ankiqt
from aqt.utils import askUser, showInfo, showText, showWarning, showCritical, tooltip, openLink, openFolder, getOnlyText, getText, mungeQA, getBase

import aqt

from aqt.sound import getAudio

__version__ = "2.0.33b"

# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #

from anki.consts import MODEL_STD, MODEL_CLOZE

import difflib, cgi
import unicodedata as ucd
import HTMLParser

import anki.sound
from anki.sound import play
from anki.sound import mplayerQueue, mplayerClear, mplayerEvt
from anki.sound import MplayerMonitor
from anki.sound import playFromText, clearAudioQueue, play

A = {}
B = {}

HIDE_THEM_ALL = False
#HIDE_THEM_ALL = True

A['CHECK_ASCII_PATH'] = [None, True, False, ''' Сheck the startup path for invalid characters ''', \
    """ Проверять путь к программе на наличие в нём символов кириллицы (и прочего юникода) """]

A['ONESIDED_CARDS'] = [None, True, False, ''' Skip question if BackSide is empty, {{FrontSide}} only or exact CopyPaste of FrontSide. ''', """ Поддержка односторонних карточек """]

B['B11_BUTTON_TITLES'] = [None, True, False, ''' 2C titles (tooltips, baloon tips) ''', \
    """ Показывать всплывающие подсказки """]

#####################
# Get language class
# Выбранный пользователем язык программной оболочки
import anki.lang
lang = anki.lang.getLang()

B['B08_BIG_BUTTONS'] = [None, True, False, ''' Big Button Show Answer and so far. ''', \
    """ Большие кнопки Показать и Оценить ответ """]

###################################
#
A['KING_SIZE'] = [None, 32, 24, ''' Icon's size on toolbar (pixels) # 48 ''', \
    """ Размер места под иконку на панелях инструментов (в пикселях) # как вариант """]

MUSTHAVE_COLOR_ICONS = 'musthave_icons'

##########################
# -- lang Again Hard Good Easy
BUTTON_LABELS_LANG = [ 
   ['ru', u'НЕТ <small>1</small>', u'Трудно <small>2</small>', u'ДА <small>3</small>', u'Легко <small>4</small>'], 
   ['en', u'aw&hellip; <small>1</small>', u'huh? <small>2</small>', u'nice <small>3</small>', u'radical! <small>4</small>'],
   #['ru', u'НЕТ <sub>1</sub>', u'Трудно <sub>2</sub>', u'ДА <sub>3</sub>', u'Легко <sub>4</sub>'], 
   #['en', u'aw&hellip; <sub>1</sub>', u'huh? <sub>2</sub>', u'nice <sub>3</sub>', u'radical! <sub>4</sub>'],
   ]

# lang o_O :-( :-| :-) 
BUTTON_LABELS_SMILES = [[lang, u'o_O', u'<b>:-(</b>', u'<b>:-|</b>', u'<b>:-)</b>']]

BUTTON_LABELS = BUTTON_LABELS_LANG

##########################
# -- Force custom font -- 

#A['FONT'] = [None, "Times New Roman", "", ''' Default Font for Decks Browser and Deck Overview ''', """ Шрифт для списка колод и основных показателей колоды """]
#A['FONTSIZE'] = [None, 18, 0, '''  ''', """  """]

A['FONT'] = [None, "Calibri", "", '''  ''', """  """]
A['FONTSIZE'] = [None, 16, 0, ''' Default Font Size for Decks Browser and Deck Overview ''', \
    """ Размер шрифта для списка колод и страницы основных показателей колоды """]

# hide Edit and More button on left and right bottom corners of reviewer screen
# -- Edit More -- Редактирование Ещё -- Редактирование Еще -- 
# не показывать  !!!

B['B13_EDIT_MORE'] = [None, False, True, ''' Edit and More buttons on Study Screen ''', \
    """ На карточках показывать кнопки Редактирование Ещё """]

MORE_EDIT = " td.stat button { display: none; } "
EDIT_MORE = " td\.stat button \{ display\: none\; \} "

A['LOCAL_CSS_AND_DIY_NIGHT_MODE'] = [None, True, False, ''' Local CSS and DIY night mode ''', \
    """ Можно настраивать внешние таблицы стилей под различные пользовательские и встроенные классы """]

extra_classes_list = [
    {'class': u'night',      'display': u'.night { &Ночной режим } ' if lang == 'ru' else '.night { &Night mode } '},
    {'class': u'contrast',   'display': u'.contrast { &Режим высокой контрастности } ' if lang == 'ru' else '.contrast { &High contrast mode } '},
    {'class': u'solarized',  'display': u'.solarized { &Солнечные цвета } ' if lang == 'ru' else '.solarized { &Solarized colors } '},
    {'class': u'rain',       'display': u'.rain { &Дождливый день } ' if lang == 'ru' else '.rain { &Rainy day } '},
    ]

###############################
# -- Replay buttons on card --
#REPLAY_BUTTONS_ON_CARD = 2 # button's tooltip with filename
#REPLAY_BUTTONS_ON_CARD = 1 # button's tooltip without filename on FrontSide
#REPLAY_BUTTONS_ON_CARD = 0 # no buttons at all

A['REPLAY_BUTTONS_ON_CARD'] = [None, 2, 0, \
    ''' Replay buttons on card # =1 title tooltip on FrontSide without filename ''', \
    """ Как показывать кнопки Повтор Аудио на карточках """]

A['CHECK_OLD_ISSUES'] = [None, True, False, ''' Look for old add-ons ''', \
    """ Проверять старые дополнения """]

#################################################################
# -- Show learn count -- 
# Show_learn_count.py by ospalh
# Show the learn count in the deck browser, too.
# 3 numbers vs 2 by default
# New, Learn, Due vs Learn+Due and New
# Show count of unseen and suspended cards in deck browser.

B['B05_STUDY_BUTTON'] = [None, False, True, ''' Study Deck Button ''', \
    """ Кнопка Учить колоду """]

B['B03_GEAR_AT_END_OF_LINE'] = [None, True, False, ''' Gear at the end of line ''', \
    """ Шестерёнка в конце строки """]

# -- Unseen and buried counts --
# https://ankiweb.net/shared/info/161964983
# Show count of unseen and buried cards in deck browser.

# -- More Overview Stats --
# https://ankiweb.net/shared/info/2116130837
# This add-on adds a little more info to the overview statistics.
#  Due today: new + learning + review 
#   Total reviews: total reviews regardless of daily limit (today and tomorrow limitless)
#   Total new cards: total new cards in deck 
#   Total cards: total cards in deck
# -- More Overview Stats 2 --
# Unseen, suspended and buried
# Невиданные, исключённые и отложенные

B['B00_MORE_OVERVIEW_STATS'] = [None, 3, 0, ''' More Overview Stats # =1 ''', \
    """ Дополнительные показатели на странице колоды и на панели колод # =2 """]

B['B04_HIDE_BIG_NUMBER'] = [None, 999, 999999, ''' Hide big numbers ''', \
    """ Спрятать числа больше указанного """]

B['B04_HIDE_BIG_NUMBERS'] = [None, False, True, ''' Don't see the exact number in deck list. ''', \
    """ Прятать большие числа """]

# -- zoom --
A['ZOOM'] = [None, True, False, ''' ZOOM and Open Hint and Reply with Mouse Wheel  ''', \
    """ Масштаб """]

A['ZOOM_IMAGES'] = [None, True, False, ''' also ZOOM Images as well as text too ''', \
    """ Масштабировать и картинки тоже, как и текст """]

# Standard zoom factors for the main views of the central area:
deck_browser_standard_zoom = 1.0
overview_standard_zoom = 1.0
reviewer_standard_zoom = 1.0
# Before you change the reviewer_standard_zoom size, maybe you should
# use larger fonts in your decks.

A['SEARCH_AND_TRANSLATE'] = [None, True, False, ''' Tatoeba, Google, Yandex, Bing lookup selected on right-click and so on. ''', \
    """ Search Google Images for selected words -- Get context sentence for language learning """]

FROM_LANGUAGE = 'russian'
TO_LANGUAGE   = 'english'

FROM_LNG   = 'rus'
TO_LNG     = 'eng'

FROM_LANG   = 'ru'
TO_LANG     = 'en'

A['F3_CARD_INFO_DURING_REVIEW'] = [None, True, False, ''' Card Info During Review ''', \
    """ Shift+C original -> Shift+F3 == builtin window """]

A['F3_CARD_HISTORY'] = [None, True, False, ''' F3 == popup window ''', \
    """ Посмотреть все ответы на данную карточку: когда, долго ли думал и насколько успешно. """]

A['F3_VIEW_SOURCE'] = [None, True, False, ''' View Source HTML ''', \
    """ Посмотреть реально работающий исходный код HTML-страницы """]

A['F3_HTML_SOURCE'] = [None, True, False, ''' View Source HTML (Alt+F3)''', \
    """ Посмотреть реально работающий исходный код HTML-страницы (Alt+F3)"""]

A['EXPAND_AND_COLLAPSE_DECKS'] = [None, True, False, ''' Expand and Collapse Decks ''', \
    """ Свернуть/развернуть всё дерево колод сразу """]

A['MAXHEIGHT'] = [None, '100px', False, ''' Maximum images height in card editor (preview) ''', \
    """ Ограничение картинок по высоте в полях окна добавления/редактирования записей """]

A['SEARCH_FROM_EDITOR'] = [None, True, False, ''' Search from Editor ''', \
    """ Поиск через Обзор Anki выделенного в окне правки текста  """]

A['ADDONS_INSTALL_TOOLTIP'] = [None, True, False, ''' Tools -> Add-ons -> Browse & Install... ''', \
    """ OK notice without OK button now (showInfo 2 tooltip) """]

##############################################################################
# -- Customizable Congratulations Message --
# You can set the message text which is displayed upon completion of the deck:
CUSTOM_CONGRAT_MSG = [
 ['en',u'<b>Congratulations! You have finished this deck for now.</b><br><br>Press <b><code>D</code></b> to go to <br><button onclick="py.link(\'decks\');" id=\"study\">Deck browser.</button>'],
 ['ru',u"<b>На данный момент в этой колоде учить больше нечего.</b><br><br>Нажмите клавишу <b><code>D</code></b> для перехода к списку колод карточек.<br><button onclick=\"py.link(\'decks\');\" id=\"study\">%s</button>" % _(u'Decks')],
 ['it',u'<b>Congratulazioni! Hai completato questo mazzo per adesso.</b><br><br>Premere <b><code>D</code></b> per andare a Mazzi'],
 ]

# Поздравляем! Вы завершили эту колоду на текущий момент.
# Congratulations! You have finished this deck for now.
# Congratulazioni! Hai completato questo mazzo per adesso.

#CUSTOM_CONGRAT_MSG = False

A['CUSTOM_CONGRAT_MSG'] = [None, True, False, ''' Customizable Congratulations Message ''', \
    """ Заголовки на панели колод и пользовательское сообщение о завершении колоды на сегодня """]

###########################################################################
# It is done with the principle of minimal change in buttons functionality.

# This addon maps
# 2 buttons    1 Again    2 Good    3 Good    4 Good
# 3 buttons    1 Again    2 Good    3 Good    4 Easy
# 4 buttons    1 Again    2 Hard    3 Good    4 Easy

# So
# button 1 and 
# button 2 keep their original action anyway;
# button 4 means maximum available easy anyway;
# button 3 means Good anyway 
# (originally it means Easy in 3 buttons set, 
#  it is the only change).

# button 0 (Zero) is bound to Show Answer (on FrontSide)
# button . (Period) is bound to Undo (on FrontSide and BackSide)
# buttons , (Comma) z Z я Я are bound to Undo, too.

# -- Ignore space/enter when answer shown --
# Ignore_spaceenter_when_answer_shown.py
#
# -- Refocus Card when Reviewing --
# Enter keys are blocked on answer (BackSide)
# to prevent pass through many cards at a moment.

# Default button and Space/Enter,
# Alt and Ctrl keys work correctly now.

# -- Hint-peeking Keyboard Bindings --
# button 5 or H peeks multiple hints hint by hint increasingly
# https://ankiweb.net/shared/info/2616209911
# If there is a way of showing multiple hints increasingly, it would be better.

A['F9_HINT_PEEKING'] = [None, True, False, ''' Hint-peeking Keyboard Bindings is a way of showing multiple hints increasingly. ''', \
    """ F9 и Shift+F9 для последовательного/одновременного открытия подсказок с клавиатуры """]

F9_HINT_PEEKED = False

A['KEYS_HANDLER'] = [None, True, False, ''' Apostophe marks note now, too. (tag:marked) ''', \
    """ e, r and o hotkeys now works in uppercase E, R and O, too. """]

# Actually v Replay own voice
# and V (Shift+v) Record own voice
# Caps Lock inverts logic:
# Caps Lock and Shift+V mean Replay own voice
# Caps Lock and V mean v Record own voice

# -- Numeric Keypad Remapping --
# https://ankiweb.net/shared/info/1247735360
# . (dot)key Undo; buttons func. must be untouched(!)
#
# Use buttons 7 8 9 6 on numeric keyboard to right-handed reply.
# Again - Show Answer - Good - Replay
# You can switch it off right now.
#
A['NUMERIC_KEYPAD_REMAPPING'] = [None, True, False, ''' Numeric Keypad Remapping Use buttons 7 8 9 6 on numeric keyboard to right-handed reply. ''', \
    """ Для удобства ответов с цифровой клавиатуры назначены дополнительные клавиши 6 7 8 9 """]

B['B12_HARD7'] = [None, False, True, \
    ''' Use the key 7 on the numeric keypad as key 2 synonim (Hard) instead of key 1 (Again) if you answer `Hard` more often than `Again` ''', \
    """ Удобно тем, кто чаще отвечает Трудно, чем Снова Не знаю. """]

# -- Handy Answer Keys Shortcuts --
A['RIGHT_HAND_JKL_ANSWER_KEYS_SHORTCUTS'] = [None, True, False, \
    ''' Use buttons J K L ; on main keyboard to right-handed reply. ''', \
    """  They work in uppercase, too. You can switch it off right now. """]

# Set up variable ANSWER_BYPASS to True, 
A['ANSWER_BYPASS'] = [None, False, True, ''' if you need to reply on question (FrontSide) directly, ''', \
    """ without looking at answer (BackSide). """]

# Set up variable ANSWER_USING_REPLY_KEYS to True, 
A['ANSWER_USING_REPLY_KEYS'] = [None, False, True, \
    ''' if you need to open an answer (BackSide) with any answer key ''', \
    """ ANSWER_BYPASS take precedence over this one. """]
# NB! To use this mode is not a good practice.

# -- Bigger Show Answer Button --
# https://ankiweb.net/shared/info/???
# Makes the show answer button wide enough to cover all 4 of the review buttons.
# -- Bigger Show All Answer Button --
# https://ankiweb.net/shared/info/1867966335

B['B06_WIDE_BUTTONS'] = [None, True, False, ''' Bigger Show All Answer Button ''', \
    """ Makes the show answer button wide enough to cover all 4 of the review buttons. """]

# -- Button Colours (Good, Again) -- 
# https://ankiweb.net/shared/info/2494384865
# Color buttons are just the same width as in Night Mode
# Good button expands to empty place of absentee buttons Easy and Hard

B['B07_COLOR_BUTTONS'] = [None, True, False, ''' Color Answer Buttons ''', \
    """ Цветные кнопки оценки ответа """]

# -- Packed with: -- 

# -- Toggle Full Screen F11 --
# https://ankiweb.net/shared/info/1703043345
A['TOGGLE_FULL_SCREEN_F11'] = [None, True, False, ''' If you want to learn in Full-Sreen, use this. ''', \
    """ Свернуть/развернуть на весь экран окно Anki """]

# -- Answer Confirmation plugin for Anki 2.0 --
# https://ankiweb.net/shared/info/3882211885
# Show pressed Answer Button as tooltip
# only on pressed key, no tooltip on mouse click.

B['B10_ANSWER_CONFIRMATION'] = [None, 2, 0, ''' =1 tooltip all answers ''', \
    """ Всплывающая подсказка при ответе с клавиатуры. """]

# -- Accept Anki 1.2 shortcuts to list decks, add cards and open browser -- 
# https://ankiweb.net/shared/info/544525276
# Allows you to use the old ctrl+d, ctrl+f and ctrl+w shortcuts.
A['ANKI12SHORTCUTS'] = [None, True, False, ''' not ^D, Control+d excluded, ^F and ^W only. ''', \
    """ На манер Anki 1.2 Обзор Ctrl+F Колоды Ctrl+W но без Добавить Ctrl+D """]

# -- Hierarchical Tags for Anki --
# https://ankiweb.net/shared/info/1089921461
# without any mod.
A['HIERARCHICAL_TAGS'] = [None, True, False, ''' GroupName::TagName ''', \
    """ Иерархические метки """]

# -- Deck name in title -- 
# https://ankiweb.net/shared/info/3895972296
# v1.2.0 there, v1.3.0 here (from addons-ospalh.zip; with filename.exe in title)
A['DECK_NAME_IN_TITLE'] = [None, True, False, \
    ''' Look for deck's name, profile name, cmd parameters in window title. ''', \
    """ Название колоды, профиля, параметры запуска - в заголовоке окна Anki """]

# -- Bigger Show Answer Button -- 
# https://ankiweb.net/shared/info/1867966335
# For people who do their reps with a mouse.
# Makes the show answer button wide enough to cover all 4 of the review buttons. 
# -- CHK_06_WIDE_BUTTONS 

# https://ankiweb.net/shared/info/916405836
# no comments. must have
A['DISABLE_DEL'] = [None, True, False, ''' Disable the delete key in reviews ''', \
    """ Запрос подтверждения удаления записи по клавише Del во время просмотра карточки. """]

# -- Rebuild All -- 
# https://ankiweb.net/shared/info/1639597619
# Menu command Tools - Rebuild All Filtered Decks is available always.
#  Button to the bottom of the main screen, to rebuild all filtered decks at once
#   is available on demand.
#    NB! Some extra <hr> is drawing! 

# -- Strikethrough button in editor window -- 
# https://ankiweb.net/shared/info/999886206
# Strike Through 

# https://ankiweb.net/shared/info/2062818289
A['POWER_CREATE_LISTS'] = [None, True, False, ''' Power Create lists ordered unordered and indented O U In buttons in editor window ''', \
    """ Удобные кнопочки в редакторе для создания списков """]

# -- Deleting Reduant Configurations -- 
# -- Removes Empty Note Types --
# https://ankiweb.net/shared/info/248074683
# https://ankiweb.net/shared/info/3867500866
A['REMOVES_EMPTY'] = [None, True, False, ''' new line in Tools menu to Remove ALL Empty Note Types and Delete Redundant Configurations at once ''', \
    """ Одной командой меню удалить пустые типы записей и группы параметров, а также всячески протестировать базу. """]

#  After some time you pile up a lot of note types that never get deleted? 
#   This plugin takes care of it! After installing,
#    click on Tools -> Remove Empty Note Types. 

# == Warmest Regards and Much Gratitude: ==

# Decks Total
# https://ankiweb.net/shared/info/1421528223
# Shows the total due, learn and new cards from all the decks in the deck browser.

# more_shortcuts 
#  from addons-ospalh.zip
# Keys i (left-handed Dvorak) and 6 (NumPad) to Replay

# Ignore space/enter when answer shown
# https://ankiweb.net/shared/info/2160758119
# Only holding of the Enter key goes through questions so fast.
# There is no need to block the Space key.

# Handy Answer Keys Shortcuts
# https://ankiweb.net/shared/info/2090822731
# elif _answerCard() stru., 3 vs cnt = .answerButtons()
# J K L ; also should work in uppercase. z Z я Я to Undo.

# Answer Key Remap
# https://ankiweb.net/shared/info/1446503737
# Hard is not Again(!), Hard is Good; buttons func. must be untouched(!)

# Answer Key Cascade
# https://ankiweb.net/shared/info/992946134
# 3 and 4 answer max Easy; 3 must be Good always(!)

# 0 (Zero) Key to show answer
# https://ankiweb.net/shared/info/191541298
A['ZERO_KEY_TO_SHOW_ANSWER'] = [None, True, False, ''' 0 on question FrontSide == Show Answer 0 on answer BackSide == Answer Good and Show Next Card ''', \
    """ Открывать ответ/следующую карточку клавишей 0 с цифровой клавиатуры """]

#################################################################################
# Press Gray+ to play next audio file on FrontSide of BackSide. ???
###

# Frozen Fields
# Воробьиные поля навсегда
A['FROZEN_FIELDS'] = [None, True, False, ''' A more convenient way to mark fields as sticky. ''', \
    """ Поля в окне добавления карточек, сохраняющие последнее значение. """]

A['RESET_CARD_SCHEDULING'] = [None, True, False, ''' Reset card scheduling information / progress ''', \
    """ Сбросить расписание """]

A['OPEN_FOLDERS'] = [None, True, False, ''' Open local Anki folders in file explorer. ''', \
    """ Команды меню на открытие служебных папок (директорий, каталогов) Anki в проводнике файловой системы """]

A['FLIP_FLOP'] = [None, True, False, ''' Show FrontSide/BackSide ''', \
    """ Показать лицевую/оборотную сторону карточки """]

A['RANDOM_ITEM'] = [None, True, False, ''' Random element from Field with commas. ''', \
    """ Случайное значение из поля (список через запятую или точку с запятой) """]

A['RANDOM_SOUND'] = [None, True, False, ''' [sound:...][sound:...][sound:...] just once ''', \
    """ Случайная озвучка из поля [sound: могут идти без пробелов """]

A['MAKE_LIST'] = [None, True, False, ''' Show {{Field with commas}} on the card as UL/OL. ''', \
    """ Создать список OL/UL из одно/двухуровневого списка в поле (,,,;,,) """]

A['ADD_FIELDS_WITHOUT_DIV'] = [None, True, False, ''' Edit Cards Add field W/O DIV style=font ''', \
    """ Редактирование Карточки Добавить поле Не заключать поле в тег DIV с указанием шрифта"""]

A['F6_SOUND_KEY_MENU'] = [None, True, False, ''' F6 pause ^F6 stop Alt+F6 back Shift+F6 forward 5 sec. ''', \
    """ Остановка долгой озвучки, промотка вперёд/назад на 5 сек. """]

A['F6_FAST_SLOW'] = [None, True, False, ''' ^Shift+F6 fast ^Alt+F6 slow ^Alt+Shift+F6 100% ''', \
    """ Ctrl+Shift+F6 быст. 10% Ctrl+Alt+F6 медл. 10% Ctrl+Alt+Shift+F6 норм. 100% """]

A['SET_INTERVAL'] = [None, True, False, ''' Show card some days later. ''', \
    """ Установить следующий показ через указанное количество дней/недель/месяцев """]

A['F4_EDIT'] = [None, True, False, ''' Edit card's templates ''', \
    """ Редактирование шаблона карточки """]

A['REBUILD_THEM_ALL'] = [None, True, False, ''' Rebuild ALL filtered decks ''', \
    """ Перестроить ВСЕ фильтр-колоды. """]

A['ANKI_MENU_ICONS'] = [None, True, False, ''' Show menu icons ''', \
    """ Показывать иконки в меню Anki """]

A['KEY0'] = [None, True, False, ''' To show next card from NumPad. ''', \
    """ На лицевой стороне - ничего, на оборотной - показать следующую карточку. """]

A['MULTIPLE_TYPING'] = [None, True, False, ''' Check multiple type with default space bar. ''', \
    """ Проверка ввода в несколько полей. """]

# -- Card Browser Lookup --
# Look up selected word in Anki browser.
#CARD_BROWSER_LOOKUP = True
#CARD_BROWSER_LOOKUP = False

A['SEARCH_BROWSER'] = [None, True, False, ''' Find out selected text in Anki's Browser. ''', \
    """ Поиск выделенного на карточке текста через Обзор Anki. """]

A['SEARCH_TIME'] = [None, True, False, ''' Search cards based on review time ''', \
    """ типа time:5 для карточек со временем ответа 5 сек. """]

A['SMALL_ADD_EDIT_DIALOGS'] = [None, True, False, ''' No minimal width/height on Add/Edit window. ''', \
    """ Снятие ограничений на размер окна добавления/правки записи. """]

A['TIMEBOX_TOOLTIP'] = [None, True, False, ''' Timebox tooltip w/o any askUser. ''', \
    """ Подсказка о количестве карточек за интервал времени уходит сама. """]

##########################################################
## Configuration section --          COLORFUL_TOOLBARS.py
########################

A['COLORFUL_TOOLBAR'] = [None, True, False, ''' Toolbars on cards. ''', \
    """ Панели инструментов по бокам карточек. """]

try:
    MUSTHAVE_COLOR_ICONS = os.path.join(mw.pm.addonFolder(), MUSTHAVE_COLOR_ICONS)
except:
    MUSTHAVE_COLOR_ICONS = ''

# Keep this on False for tool bars on top or bottom or set it to True
# for tool bars at the left an right. The left tool bar wil also get
# smaller icons.
netbook_version = True
#netbook_version = False

## Position of the new toolbar: either starting out above the old tool
## bar and movable, or below the old tool bar. In that case it can't
## be dragged to another position.
qt_toolbar_movable = True
#qt_toolbar_movable = False

## Do or do not show a button that lets this be the last card reviewed.
show_toggle_last = True
#show_toggle_last = False

## Do or do not show a mute button that stops Anki from playing
## sound/videos initially.
## NB. The mute is not absolute. When you push the replay button, the
## sound still gets played.
show_mute_button = True
#show_mute_button = False

## Show the suspend card button
show_suspend_card = True
#show_suspend_card = False

## Show the suspend note button
show_suspend_note = True
#show_suspend_note = False

# Show the tool bars with a gradient background
#
# In my opinion it looks a little bit nicer with gradient. The
# disadvantage is that with the gradient the tool bars don't follow
# color scheme changes untill you restart Anki.
do_gradient = True
#do_gradient = False

GRADIENT_L = 111
GRADIENT_H = 123

################################
# End of configuration section
############################

A['F9_HINT_PEEKING_5'] = [None, True, False, ''' Push 5 button to open next hint. ''', \
    """ Кнопку 5 можно отключить отдельно. """]

A['F9_HINT_PEEKING_H'] = [None, True, False, ''' Push H to hint hext. ''', \
    """ Кнопку h тоже. """]

A['DAY_LEARNING'] = [None, True, False, ''' Day learning cards always before new. ''', \
    """ Изучаемые карточки с интервалом сутки и более - всегда перед новыми. """]

A['SWAP_FRONT_BACK'] = [None, True, False, ''' Swap Front/Back fields' values ''', """ Обмен значениями полей Вопрос и Ответ """]

A['BROWSER_SEARCH_MODIFIERS'] = [None, True, False, ''' in Browse: CurrentDeck or Card1 only ''', \
    """ в Обзоре: только текущая колода или только первая карточка """]

A['CLOZE_EDITOR_HOTKEYS'] = [None, True, False, ''' in Add/Edit: Ctrl+Alt+Space === Ctrl+Alt+Shift+C ''', \
    """ в Редакторе: ^Space для CLOSE как синоним ^Shift+C """]

###########################################
# Setup initial values

for key, value in A.iteritems():
    A[key][0] = A[key][1]
for key, value in B.iteritems():
    B[key][0] = B[key][1]

# -------------------------------------------------------------------
from aqt.reviewer import Reviewer
from aqt.qt import *
import aqt.reviewer
from anki.hooks import addHook, wrap, runHook
from anki.lang import _
from aqt.webview import AnkiWebView
import aqt.stats

from PyQt4.QtGui import *
from PyQt4.QtCore import *

soundtrack_q_number = 0
soundtrack_q_list = []
soundtrack_a_number = 0
soundtrack_a_list = []

###########################
# Load user's variables
###########################

CREATE_MUSTHAVE_OPTIONS = True
#CREATE_MUSTHAVE_OPTIONS = False

READ_MUSTHAVE_OPTIONS = True
#READ_MUSTHAVE_OPTIONS = False

if CREATE_MUSTHAVE_OPTIONS:
   line = ''

   def NextLine( English_remark, Russian_comment, Constant_variable, Init_value, Alt_value ):
    global line
    str = unicode(Constant_variable)
    if len(str)>0:
      if len(English_remark.strip())>0:
          line += u'# '+ unicode(English_remark.strip()) +'\n'
      if len(Russian_comment.strip())>0 and lang=='ru':
          line += u'# '+ unicode(Russian_comment.strip()) +'\n'

      if isinstance(Init_value, basestring):
          if Init_value.find("'")>=0 and Init_value.find('"')>=0:
            line += "'" + str + "': '''" + unicode(Init_value) + "''', " 
          elif Init_value.find("'")>=0:
            line += "'" + str + "': " + '"' + unicode(Init_value) + '", '
          elif Init_value.find('"')>=0:
            line += "'" + str + "': '" + unicode(Init_value) + "', " 
          else:
            line += "'" + str + "': '" + unicode(Init_value) + "', " 
      else:
            line += "'" + str + "': " + unicode(Init_value) + ", "

      if isinstance(Alt_value, basestring):
          if Alt_value.find("'")>=0 and Alt_value.find('"')>=0:
            line += "# '''" + unicode(Alt_value) + "''', # " 
          elif Alt_value.find("'")>=0:
            line += "# " + '"' + unicode(Alt_value) + '", # '
          elif Alt_value.find('"')>=0:
            line += "# '" + unicode(Alt_value) + "', # " 
          else:
            line += "# '" + unicode(Alt_value) + "', # " 
      else:
            line += "# " + unicode(Alt_value) + ', # ' 

      line += '\n\n'

   filo = os.path.join(mw.pm.addonFolder(), "--musthave-options.py")
   if not os.path.exists(filo):
      # filo without absolute path will be placed into `c:\Program Files (x86)\Anki` folder.
      import codecs
      f = codecs.open(filo, 'w', "utf-8")

      line = u'# -*- mode: Python ; coding: utf-8 -*-\n'+\
      u'# Place your Must Have configuration variables here.\n'+\
      (u'# Ваши константы для дополнения Must Have указывайте здесь:\n' if lang=='ru' else '')+'\n'

      """
      line += u"#HIDE_THEM_ALL = "+unicode(HIDE_THEM_ALL)+"\n"
      line += u"#HIDE_THEM_ALL = "+unicode(not HIDE_THEM_ALL)+"\n\n"
      """

      line += u'deck_browser_standard_zoom = '+str(deck_browser_standard_zoom)+'\n'
      line += u'overview_standard_zoom = '+str(overview_standard_zoom)+'\n'
      line += u'reviewer_standard_zoom = '+str(reviewer_standard_zoom)+'\n\n'

      line += u'#'+ '#'*66 +'\n'
      line += u'# If you want to use alternative value' +'\n'
      line += u'# simply delete first character # (sharp) on the subsequent line.' +'\n'
      line += u'# Use Delete or Backspace key, to remove does not mean to replace with Space instead.' +'\n'
      line += u'# Either you can place cursor right after # (sharp)' +'\n'
      line += u'# and push Enter to split single line on two separate lines.' +'\n\n'

      line += u'# '+ '-'*33 +'\n# Get language class\nimport anki.lang\nlang = anki.lang.getLang()\n\n'

      line += u"FROM_LANGUAGE = '" + FROM_LANGUAGE + "'\n"
      line += u"TO_LANGUAGE   = '" + TO_LANGUAGE + "'\n\n"
      line += u"FROM_LNG   = '" + FROM_LNG + "' # 3 letters language code\n"
      line += u"TO_LNG     = '" + TO_LNG + "'\n\n"
      line += u"FROM_LANG   = '" + FROM_LANG + "' # 2 letters language code\n"
      line += u"TO_LANG     = '" + TO_LANG + "'\n\n"

      """
      line += u"#BUTTON_LABELS_LANG = [[lang, u'1', u'2', u'3', u'4']] # hotkeys \n"
      line += u"#BUTTON_LABELS_LANG = [[lang, u'2', u'3', u'4', u'5']] # Russian school marks \n"
      """

      line += u"#BUTTON_LABELS_LANG = [[lang, _('Again'), _('Hard'), _('Good'), _('Easy')]] # in Translation \n"
      line += u"#BUTTON_LABELS_LANG = [[lang, 'Again', 'Hard', 'Good', 'Easy']] # in English \n"
      line += u"#BUTTON_LABELS_LANG = [[lang, 'Snova', 'Trudno', 'AGA', 'Legko']] # in translit \n"
      line += u"#BUTTON_LABELS_LANG = [[lang, u'НЕТ', u'Трудно', u'ДА', u'Легко']] # in Russian anyhow \n"
      line += u"#BUTTON_LABELS_LANG = [[lang, u'aw&hellip;', u'huh?', u'nice', u'radical!']] # in lowercase anyway \n"
      line += u"#BUTTON_LABELS_LANG = [[lang, u'NO?', u'AH!', u'OK', u'SO&#133;']] # in uppercase anywhere\n\n"

      line += u"Z = { \n\n"

      keylist = A.keys()
      keylist.sort()
      if HIDE_THEM_ALL:
        for key in keylist:
          A[key][0] = A[key][2]
          NextLine( A[key][3], A[key][4], key, A[key][2], A[key][1] )
      else:
        for key in keylist:
          A[key][0] = A[key][1]
          NextLine( A[key][3], A[key][4], key, A[key][1], A[key][2] )

      keylist = B.keys()
      keylist.sort()
      if HIDE_THEM_ALL:
        for key in keylist:
          B[key][0] = B[key][2]
          NextLine( B[key][3], B[key][4], key, B[key][2], B[key][1] )
      else:
        for key in keylist:
          B[key][0] = B[key][1]
          NextLine( B[key][3], B[key][4], key, B[key][1], B[key][2] )

      line += u'}\n # \n\n'

      f.write(unicode(line))
      f.close()

if READ_MUSTHAVE_OPTIONS:
    try:
        #from musthave.options import * # works fine, but I need another filename
        module = __import__("--musthave-options",globals(),locals(),['*'],-1)
        for k in dir(module):
            locals()[k] = getattr(module, k)
        # from options import * # does not work (maybe options is Python's reserved name)
        # A = Z
        for key, value in Z.iteritems():
         if len(key): # and hasattr(Z,key):
          try:
           A[key][0] = Z[key]
          except KeyError:
           try:
            B[key][0] = Z[key]
           except KeyError:
            pass
    except ImportError:
        pass

# -------------------------------------------------------------------
# 0 - unknown 
# 1 - switch it off if original was found
# 2 - fully compatible 
# 3 - original works anyway 
# 4 - incompatible 
# 5 - must have ingredients

if A['CHECK_OLD_ISSUES'][0]:

    old_issues = [
    #['', '', '', '',1],
    ['0_Zero_Key_to_show_answer.py', '0 (Zero) Key to show answer', '191541298', '2012-11-29',1],
    ['Accept_Anki_12_shortcuts_to_list_decks_add_cards_and_open_browser.py',
    'Accept Anki 1.2 shortcuts to list decks, add cards and open browser', '544525276', '2012-04-19',1],
    ['Answer_Confirmation.py', 'Answer Confirmation', '3882211885', '2013-02-13',1],
    ['Answer_Key_Cascade.py', 'Answer Key Cascade', '992946134', '2012-08-23',4],
    ['Answer_Key_Remap.py', 'Answer Key Remap', '1446503737', '2013-07-28',4],
    ['Audio_Playback_Speed.py', 'Audio Playback Speed', '234253523', '2015-03-25',1], # !!! 2016-03-06
    ['Adjust_Audio_Speed.py', 'Adjust Audio Speed', '234253523', '2016-03-25',1], # !!!
    ['Bigger_Show_Answer_Button.py', 'Bigger Show Answer Button', '1867966335', '2013-05-19',1],
    ['Bigger_Show_All_Answer_Buttons.py', 'Bigger Show All Answer Buttons', '2034935033', '2015-02-06',1],
    ['Browser_Search_Modifiers.py', 'Browser Search Modifiers', '594622823', '2016-04-18',1],
    ['Button_Colours_Good_Again.py', 'Button Colours (Good, Again)', '2494384865', '2012-11-25',2],
    ['Card_Browser_Lookup.py', 'Card Browser Lookup', '869824347', '2016-02-28',2], 
    # date of renaming to Search browser for selected words; original date is 2015-11-07
    ['Card_Info_During_Review.py', 'Card Info During Review', '2179254157', '2013-12-08',1],
    ['Card_time_forecast.py', 'Card time forecast', '2189699505', '2015-12-05',3],
    ['Clickable_Tags_on_Reviewer.py', 'Clickable Tags on Reviewer', '1321188674', '2016-02-15',2], # 2016-01-26
    ['colorful_toolbars.py', 'Colorful toolbars', '388296573', '2014-04-02',1],
    ['Control_Audio_Playback_Pause_Skip_backwards_Skip_Forwards_Stop_Audio.py',
     'Control Audio Playback (Pause, Skip backwards, Skip Forwards, Stop Audio)', '1591259314', '2014-10-30',1],
    ['Custom_Keyboard_Shortcuts.py', 'Custom Keyboard Shortcuts', '1483821271', '2015-11-25',4],
    ['Customizable_Congratulations_Message.py', 'Customizable Congratulations Message', '', '29.10.2015',3],
    #['', '', '', '',2],
    ['Deck_name_in_title.py', 'Deck name in title', '3895972296', '2013-04-01',3],
    ['Deleting_Reduant_Configurations.py', 'Deleting Reduant Configurations', '3867500866', '2013-03-08',1],
    ['Disable_the_delete_key_in_reviews.py', 'Disable the delete key in reviews', '916405836', '2013-12-17',1],
    ['Expand_and_Collapse_Decks.py', 'Expand and Collapse Decks', '2554066128', '2013-10-24',2],
    ['extra_card_stats_.py', 'extra card stats ×', '1581856587', '2016-03-09',3],
    ['Field_Modifier_Random_Item.py', 'Field Modifier: Random Item', '1484572887', '2015-01-01',1],
    ['Flip_cards_with_shortcut_key_0.py', 'Flip cards with shortcut key "0".', '844452602', '2016-02-11',1],
    ['Force_custom_font.py', 'Force custom font', '2103013902', '2012-08-23',3],
    ['Frozen Fields.py', 'Frozen Fields', '516643804', '2015-10-25',3],
    ['Full_Screen_F11.py', 'Full Screen F11', '', '21.09.2015',1],
    #['', '', '', '',4],
    ['Handy_Answer_Keys_Shortcuts.py', 'Handy Answer Keys Shortcuts', '2090822731', '2013-07-06',3],
    ['Handy_Hint_and_Answer_Keys.py', 'Handy Hint and Answer Keys', '', '22.10.2015',4],
    ['HierarchicalTags.py', 'Hierarchical Tags', '1089921461', '2014-04-29',3],
    ['Hint-peeking_Keyboard_Bindings.py', 'Hint-peeking Keyboard Bindings', '2616209911', '2012-08-20',1],
    ['Ignore_enter_when_answer_shown.py', 'Ignore enter when answer shown', '', '24.10.2015',4],
    ['Ignore_spaceenter_when_answer_shown.py', 'Ignore space/enter when answer shown', '2160758119', '2012-12-20',3],
    ['Local_CSS_and_DIY_night_mode.py', 'Local CSS and DIY night mode', '2587372325', '2013-06-10',1],
    ['Maximum_images_height_in_card_editor.py', 'Maximum images height in card editor', '229181581', '2015-04-13',1],
    ['More_Overview_Stats.py', 'More Overview Stats', '2116130837', '2013-01-03',2],
    ['More_Overview_Stats_2.py', 'More Overview Stats 2', '531984586', '2014-10-25',2],
    ['Multiple_type_fields_on_card.py', 'Multiple type fields on card', '689574440', '2016-01-22',1],
    ['Must_Have_Hint_and_Answer_Keys.py', 'Must Have Hint and Answer Keys', '', '28.12.2015',4],
    ['Numeric_Keypad_Remapping.py', 'Numeric Keypad Remapping', '1247735360', '2014-07-11',4],
    ['onesided_cards.py', 'One sided cards', '', '06.05.2015',1], # work both, standalone and builtin, do just the same.
    ['play_button.py', 'Replay buttons on card', '498789867', '2014-07-31',1],
    ['Power_Create_lists_ordered_unordered_and_indented.py',
     'Power Create lists ordered unordered and indented', '', '08.08.2015',1],
    ['put_ALL_due_learning_cards_first_.py', 'put ALL due "learning" cards first ×', '1810271825', '2016-03-07',3],
    ['Quick_reschedule_in_reviewer.py', 'Quick reschedule in reviewer', '1190809692', '2016-01-30',2],
    #['', '', '', '',3],
    ['Rebuild_All.py', 'Rebuild All', '1639597619', '2015-09-28',2],
    ['Refocus_Card_when_Reviewing.py', 'Refocus Card when Reviewing', '2061394997', '2013-01-27',2],
    ['Remap_Answer_Key.py', 'Remap Answer Key', '', '24.10.2015',4],
    ['Removes_Empty_Note_Types.py', 'Removes Empty Note Types', '248074683', '2016-01-15',1],
    ['Reschedule_as_new_key_shortcut.py', 'Reschedule as new key shortcut', '2124687261', '2015-04-26',2],
    ['reset_card_scheduling.py', 'Reset card(s) scheduling information / progress', '1432861881', '2016-01-28',2], # 2015-07-06
    ['Search_browser_for_selected_words.py', 'Search browser for selected words', '869824347', '2016-02-28',1], 
    ['Search_cards_based_on_review_time.py', 'Search cards based on review time', '', '29.10.2015',1],
    # '3262774902', '2014-01-04',1],
    ['Search_from_Editor.py', 'Search from Editor', '1559436729', '2014-09-16',2],
    ['Search_Google_Images_for_selected_words.py', 'Search Google Images for selected words', '800190862', '2015-03-21',2],
    ['Select_Buttons_Automatically_If_Correct_Answer_Wrong_Answer_or_Nothing.py',
     'Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing', '2074758752', '2014-07-23',1],
    ['Show_answers__default_ease_additional_key_binding.py',
    'Show answers / default ease additional key binding', '730698933', '2013-01-08',1],
    ['show_learn_count.py', 'Show learn count', '', '29.10.2015',1],
    ['Small_add_cards_dialog.py', 'Small add cards dialog', '3285086934', '2012-10-06',1],
    ['strikethrough.py', 'Strikethrough button in editor window', '999886206', '2014-10-06',2],
    ['Toggle_Full_Screen.py', 'Toggle Full Screen', '1703043345', '2015-10-27',1],
    ['Unseen_and_buried_counts.py', 'Unseen and buried counts', '161964983', '2014-11-06',3],
    ['zoom.py', 'Zoom', '1956318463', '2013-06-10',1],
    #['', '', '', '',0],
    ['Clear_all_Editor_Fields.py', 'Clear all Editor Fields', '136533494', '2016-03-21',0],
    ['Progress_Graph.py', 'Progress graph', '763339789', '2014-01-01',0],
    ['Learning_Achievements_cumulative_total_for_younglearning_card_and_mature_card.py',
    'Learning Achievements: cumulative total for young/learning card and mature card', '2093985093', '2014-02-09',0],
    ['Separate_Learn_and_Relearn_in_the_Answer_Buttons_graph.py',
    'Separate Learn and Relearn in the Answer Buttons graph', '1999018922 ', '2015-02-06',0],
    ['Daily_Totals.py', 'Daily Totals', '1075380732', '2015-02-21',0],
    ['Maturing_Cards.py', 'Maturing Cards', '1147586609', '2013-01-12',0],
    ['Failed_Mature_Cards.py', 'Failed Mature Cards', '1314513660', '2013-01-12',0],
    ['Stats_Expected_number_of_cards.py', 'Stats: Expected number of cards', '2464818309', '2013-01-23',0],
    #['', '', '', '',5],
    ['_Again_Hard.py', '• Again Hard', '1996229983', '2016-04-21',5], #2016-04-05 
    ['_Again_Hard_Good_Easy_wide_big_buttons.py', '• Again Hard Good Easy wide big buttons', '1508882486', '2016-04-21',5], #2016-04-09
    ['_Alternative_hotkeys_to_cloze_selected_text_in_Add_or_Editor_window.py', '• Alternative hotkeys to cloze selected text in Add or Editor window', '2074653746', '2016-04-22',5], # 2016-04-11
    ['_Day_learning_cards_always_before_new.py', '• Day learning cards always before new', '1331545236', '2016-04-21',5], #2016-03-18
    ['_Flip-flop.py', '• Flip-flop', '519426347', '2016-04-21',5], #2016-03-02
    ['_Insensitive_case_type_field.py', '• Insensitive case type field', '1616934891', '2016-04-21',5], #1 03.04.2016
    ['_View_HTML_source_with_JavaScript_and_CSS_styles.py', '• View HTML source with JavaScript and CSS styles', '1128123950', '2016-04-21',5], #2016-04-09
    ['_Prompt_and_set_days_interval.py', '• Prompt and set days interval', 2031109761, '2016-04-21',5], 
    ['_Swap.py', '• Swap', '1040866511', '2016-04-21',5], #2016-04-01
    ['_Timebox_tooltip.py', '• Timebox tooltip', '2014169675', '2016-04-21', 5], #2016-03-02
    ['_Young_Mature_Card_Fields.py', '• Young Mature Card Fields ', '1751807495', '2016-04-21',5], # 2016-04-07
    ['_Zooming.py', '• Zooming', '1071179937', '2016-04-21',5], #2016-03-27
    # There is no need to issue delete warning? #
    ['Flip-flop.py', 'Flip-flop', '519426347', ' 21.04.2016. ',5], #2016-03-02 
    ['Timebox_tooltip.py', 'Timebox tooltip', '2014169675', ' 21.04.2016 ', 5], # 2016-03-02
    #['', '', '', '',4],
    #['More_Answer_Buttons_for_New_Cards.py', 'More Answer Buttons for New Cards', '153603893', '2016-04-03',4],
    #['Open_Added_Today_from_Reviewer.py', 'Open 'Added Today' from Reviewer', '861864770', '2016-04-03',4],
    #['Hide_Toolbar_in_Reviewer.py', 'Hide Toolbar in Reviewer', '701296409', '2016-04-03',4],
    #['Deck_Overview_Stats_Tooltip.py', 'Deck Overview Stats Tooltip', '1279297937', '2016-04-03',4],
    #['Browse_Card_Creation.py', 'Browse Card Creation', '2075482801', '2016-04-03',4],
    ]
    # Продолжение да воспоследует.

    # 31.12.2015 packed ~42; total 243 add-ons https://ankiweb.net/shared/addons/
    # 29.02.2016 packed ~61; total 254 add-ons https://ankiweb.net/shared/addons/

"""
Answer_Key_Cascade.py
    a higher ease than possible will answer with the actual highest

Answer_Key_Remap.py
    Again = 1,2             Good = 3,4

Control_Audio_Playback_Pause_Skip_backwards_Skip_Forwards_Stop_Audio.py
    5 6 7 8 n
    pause seek -5 seek +5 stop pause

Custom_Keyboard_Shortcuts.py
    dsabSy dummy

Disable_the_delete_key_in_reviews.py

Handy_Answer_Keys_Shortcuts.py
    JKL; answer 1234 right way: 34 anwer Easy maximum available.
    on FrontSide these keys send answer directly

Hint-peeking_Keyboard_Bindings.py
    SHOW_HINT_KEY=Qt.Key_H
    To show hint, simply click all show hint buttons.

Numeric_Keypad_Remapping.py
    EASE_SHIFT = True
    UNDO_WITH_PERIOD = True
    ANSWER_KEY_CASCADE = True
    SHOW_ANSWER_USING_NUMERICAL_KEYS = True
    ???!!!

Show_answers__default_ease_additional_key_binding.py
    5 self._showAnswerHack(), 
    5 self._answerCard(self._defaultEase())
"""

if A['CHECK_OLD_ISSUES'][0]:

    very_interesting = [
    ['', '', '', '',0],
    ['dt.py', 'Decks Total', '1421528223', '2012-12-15',0], 
    # There is no ru_RU Russian in LANG list of localisation.
    
    ['Get_context_sentence_for_language_learning_-Tatoeba_lookup_on_right-click.py',
     'Get context sentence for language learning -Tatoeba lookup on right-click', '443435286', '2014-08-18',0],
    ['', '', '', '',0],
    ['advanced_browser.py', 'Advanced Browser', '874215009', '2016-02-10',0],
    ['AwesomeTTS.py', 'AwesomeTTS (text-to-speech playback / recording)', '301952613', '2016-01-17',0],
    ['download_audio.py', 'Download audio', '3100585138', '2015-10-28',0],
    ['Ignore_accents_in_browser_search.py', 'Ignore accents in browser search', '1924690148', '2014-09-28',0],
    ['load_balancer.py', 'Load Balancer', '1417170896', '2015-09-11',0],
    ['Night_Mode.py', 'Night Mode', '1496166067', '2016-03-05',0], # 2016-01-30 2015-12-16
    
    ['', '', '', '',0],
    ['Supplementary Buttons Anki.py', 'Power format pack: Markdown, code blocks, lists, tables, syntax highlight & more', '162313389', '2016-02-10',0], 
    # 2016-01-28 

    ['', 'Quick Tagging', '1562438127', '2014-10-11',0],
    ['', 'Wikitext: format text with Creole markup', '960358571', '2015-05-13',0],
    ['', 'Quick Colour Changing', '2491935955', '2012-04-22',0],
    ['', 'AutoDefine - Automatically define vocabulary words with pronunciations and image', '2136497008', '2014-10-18',0],
    ['Multi-column_note_editor.py', 'Multi-column note editor', '3491767031', '2013-11-10',0],
    ['', '', '', '',0],
    #['CSS_formatting.py', 'CSS formatting', '83944088', '2016-02-28',0],
    ['CSS_styles_formatting.py', 'CSS styles formatting', '83944088', '2016-03-17',0],
    ['', 'Don\'t remove mark on export', '909480379', '2014-04-16',0], # 
    ['', 'Change Review Key Shortcuts', '1057034736', '07.11.2012',0],
    ['', 'Quick note and deck buttons', '2181333594', '2015-11-13',0],
    ['', 'Export Cards As Text', '1589071665', '2014-09-14',0],
    ['', 'Create Copy of Selected Cards', '787914845', '2015-06-28',0],
    ['Tag_Toggler.py', 'Tag Toggler', '874498171', '2016-03-31',0], # 2016-02-29
    ['', 'Transfer Deck', '1921587528', '2014-05-14',0],
    ['', '', '', '',0],
    ]
    # To be continued.

# ---------------------------------
#
if A['CHECK_OLD_ISSUES'][0]:
    for idn_issue in range(0, len(old_issues)):
      old_issue = old_issues[idn_issue]
      if len(old_issue[0]) > 0:
        old_filename = os.path.join(mw.pm.addonFolder(), old_issue[0])
        old_issues[idn_issue].append(os.path.exists(old_filename))

    def found(addon_name): 
        for old_issue in old_issues:
            if addon_name == old_issue[0]:
                return old_issue[5]
        else:
            showCritical('''<center><i>&bull; Must Have:</i> &nbsp; Требуется обязательное внесение в список<br> <b>%s</b>
<br>Просто наличия файла в каталоге дополнений недостаточно!!!</center>'''%addon_name)
        return False

    A['DAY_LEARNING'][0] = False if found('_Day_learning_cards_always_before_new.py') else A['DAY_LEARNING'][0]
    A['SWAP_FRONT_BACK'][0] = False if found('_Swap.py') else A['SWAP_FRONT_BACK'][0]
    #
    A['FLIP_FLOP'][0] = False if found('Flip-flop.py') else A['FLIP_FLOP'][0]
    A['FLIP_FLOP'][0] = False if found('_Flip-flop.py') else A['FLIP_FLOP'][0]
    A['FLIP_FLOP'][0] = False if found('0_Zero_Key_to_show_answer.py') else A['FLIP_FLOP'][0]
    A['FLIP_FLOP'][0] = False if found('Flip_cards_with_shortcut_key_0.py') else A['FLIP_FLOP'][0]
    #
    A['CLOZE_EDITOR_HOTKEYS'][0] = False if found('_Alternative_hotkeys_to_cloze_selected_text_in_Add_or_Editor_window.py') else A['CLOZE_EDITOR_HOTKEYS'][0]
    #
    A['COLORFUL_TOOLBAR'][0] = False if found('colorful_toolbars.py') else A['COLORFUL_TOOLBAR'][0]
    B['B13_EDIT_MORE'][0] = False if found('colorful_toolbars.py') else B['B13_EDIT_MORE'][0]
    #
    CUSTOM_CONGRAT_MSG = False if found('Customizable_Congratulations_Message.py') else CUSTOM_CONGRAT_MSG
    A['CUSTOM_CONGRAT_MSG'][0] = False if found('Customizable_Congratulations_Message.py') else A['CUSTOM_CONGRAT_MSG'][0]
    #
    A['BROWSER_SEARCH_MODIFIERS'][0] = False if found('Browser_Search_Modifiers.py') else A['BROWSER_SEARCH_MODIFIERS'][0]
    #
    A['DISABLE_DEL'][0] = False if found('Disable_the_delete_key_in_reviews.py') else A['DISABLE_DEL'][0]
    #
    A['KEY0'][0] = False if found('0_Zero_Key_to_show_answer.py') else A['KEY0'][0]
    A['KEY0'][0] = False if found('Flip_cards_with_shortcut_key_0.py') else A['KEY0'][0]
    #
    A['ANKI12SHORTCUTS'][0] = False if found('Accept_Anki_12_shortcuts_to_list_decks_add_cards_and_open_browser.py') else A['ANKI12SHORTCUTS'][0]
    B['B10_ANSWER_CONFIRMATION'][0] = 0 if found('Answer_Confirmation.py') else B['B10_ANSWER_CONFIRMATION'][0]
    #
    A['F3_CARD_INFO_DURING_REVIEW'][0] = False if found('Card_Info_During_Review.py') else A['F3_CARD_INFO_DURING_REVIEW'][0]
    A['F3_HTML_SOURCE'][0] = False if found('_View_HTML_source_with_JavaScript_and_CSS_styles.py') else A['F3_HTML_SOURCE'][0]
    #
    A['F6_SOUND_KEY_MENU'][0] = False if found('Control_Audio_Playback_Pause_Skip_backwards_Skip_Forwards_Stop_Audio.py') else A['F6_SOUND_KEY_MENU'][0]
    #
    A['F6_FAST_SLOW'][0] = False if found('Audio_Playback_Speed.py') else  A['F6_FAST_SLOW'][0]
    A['F6_FAST_SLOW'][0] = False if found('Adjust_Audio_Speed.py') else  A['F6_FAST_SLOW'][0]
    #
    A['F9_HINT_PEEKING_5'][0] = False if found('Show_answers__default_ease_additional_key_binding.py') or found('Control_Audio_Playback_Pause_Skip_backwards_Skip_Forwards_Stop_Audio.py') else A['F9_HINT_PEEKING_5'][0]
    A['F9_HINT_PEEKING_H'][0] = False if found('Hint-peeking_Keyboard_Bindings.py') else A['F9_HINT_PEEKING_H'][0]
    #
    A['NUMERIC_KEYPAD_REMAPPING'][0] = False if found('Adjust_Audio_Speed.py') else  A['NUMERIC_KEYPAD_REMAPPING'][0]
    A['NUMERIC_KEYPAD_REMAPPING'][0] = False if found('Audio_Playback_Speed.py') else  A['NUMERIC_KEYPAD_REMAPPING'][0]
    # 16.03.2016 Audio_Playback_Speed.py don't use number keys any more.
    A['NUMERIC_KEYPAD_REMAPPING'][0] = False if found('Control_Audio_Playback_Pause_Skip_backwards_Skip_Forwards_Stop_Audio.py') else  A['NUMERIC_KEYPAD_REMAPPING'][0]
    #
    A['RANDOM_ITEM'][0] = False if found('Field_Modifier_Random_Item.py') else A['RANDOM_ITEM'][0]
    #
    A['MAXHEIGHT'][0] = False if found('Maximum_images_height_in_card_editor.py') else A['MAXHEIGHT'][0]
    #
    B['B00_MORE_OVERVIEW_STATS'][0] = 0 if found('show_learn_count.py') else B['B00_MORE_OVERVIEW_STATS'][0]
    #
    A['MULTIPLE_TYPING'][0] = False if found('Multiple_type_fields_on_card.py') else A['MULTIPLE_TYPING'][0]
    A['MULTIPLE_TYPING'][0] = False if found('Select_Buttons_Automatically_If_Correct_Answer_Wrong_Answer_or_Nothing.py') else A['MULTIPLE_TYPING'][0]
    #
    A['ONESIDED_CARDS'][0] = False if found('onesided_cards.py') else A['ONESIDED_CARDS'][0]
    #
    A['REMOVES_EMPTY'][0] = False if found('Deleting_Reduant_Configurations.py') else A['REMOVES_EMPTY'][0]
    A['REMOVES_EMPTY'][0] = False if found('Removes_Empty_Note_Types.py') else A['REMOVES_EMPTY'][0]
    #
    A['REPLAY_BUTTONS_ON_CARD'][0] = 0 if found("play_button.py") else A['REPLAY_BUTTONS_ON_CARD'][0]
    A['MULTIPLE_TYPING'][0] = 0 if found("play_button.py") else A['MULTIPLE_TYPING'][0]
    #
    A['SEARCH_BROWSER'][0] = False if found('Search_browser_for_selected_words.py') else A['SEARCH_BROWSER'][0]
    #
    A['SEARCH_TIME'][0] = False if found('Search_cards_based_on_review_time.py') else A['SEARCH_TIME'][0]
    #
    A['SMALL_ADD_EDIT_DIALOGS'][0] = False if found('Small_add_cards_dialog.py') else A['SMALL_ADD_EDIT_DIALOGS'][0]
    #
    A['SET_INTERVAL'][0] = False if found('_Prompt_and_set_days_interval.py') else A['SET_INTERVAL'][0]
    #
    A['TIMEBOX_TOOLTIP'][0] = False if found('_Timebox_tooltip.py') else A['TIMEBOX_TOOLTIP'][0]
    A['TIMEBOX_TOOLTIP'][0] = False if found('Timebox_tooltip.py') else A['TIMEBOX_TOOLTIP'][0]
    #
    A['TOGGLE_FULL_SCREEN_F11'][0] = False if found('Full_Screen_F11.py') else A['TOGGLE_FULL_SCREEN_F11'][0]
    A['TOGGLE_FULL_SCREEN_F11'][0] = False if found('Toggle_Full_Screen.py') else A['TOGGLE_FULL_SCREEN_F11'][0]
    #
    A['LOCAL_CSS_AND_DIY_NIGHT_MODE'][0] = False if found('Local_CSS_and_DIY_night_mode.py') else A['LOCAL_CSS_AND_DIY_NIGHT_MODE'][0]
    A['POWER_CREATE_LISTS'][0] = False if found('Power_Create_lists_ordered_unordered_and_indented.py') else A['POWER_CREATE_LISTS'][0]
    #
    B['B06_WIDE_BUTTONS'][0] = False if found('Bigger_Show_All_Answer_Buttons.py') or found('Bigger_Show_Answer_Button.py') else B['B06_WIDE_BUTTONS'][0]
    #
    A['ZOOM'][0] = False if found('zoom.py') else A['ZOOM'][0]
    A['ZOOM'][0] = False if found('_Zooming.py') else A['ZOOM'][0]
    #

###########################################
# Setup alternative values

if HIDE_THEM_ALL:

    for key in A.keys():
        A[key][0] = A[key][2]
    for key in B.keys():
        B[key][0] = B[key][2]

    # -- 
    BUTTON_LABELS_LANG = [[lang, _('Again'), _('Hard'), _('Good'), _('Easy')]] # in Translation 
    BUTTON_LABELS = BUTTON_LABELS_LANG
    CUSTOM_CONGRAT_MSG = False
    #"""
    do_gradient = False
    netbook_version = False
    qt_toolbar_movable = False
    show_toggle_last = False
    show_mute_button = False
    show_suspend_card = False
    show_suspend_note = False
    do_gradient = False
    #"""

    pass # in case if each parameter will be commented out

# -------------------------------------------------------------------

if not A['NUMERIC_KEYPAD_REMAPPING'][0]:
    A['ZERO_KEY_TO_SHOW_ANSWER'][0] = False

if B['B00_MORE_OVERVIEW_STATS'][0] > 1 and B['B00_MORE_OVERVIEW_STATS'][0] < 3:
   B['B03_GEAR_AT_END_OF_LINE'][0] = True

# If we do not enhance deck panel's columns then we shouldn't enhance it's font.
if (B['B00_MORE_OVERVIEW_STATS'][0] == 0):
    A['FONT'][0] =  ""
    A['FONTSIZE'][0] =  0

# -- 
def initEditMore(editMore):
  B['B13_EDIT_MORE'][0] = editMore
  if not editMore:
    mw.reviewer._bottomCSS += MORE_EDIT
  else:
    mw.reviewer._bottomCSS = re.sub(EDIT_MORE, "", mw.reviewer._bottomCSS)

initEditMore(B['B13_EDIT_MORE'][0])

def onEditMore():
  B['B13_EDIT_MORE'][0] = edit_more_action.isChecked()
  if not edit_more_action.isChecked():
    mw.reviewer._bottomCSS += MORE_EDIT
  else:
    mw.reviewer._bottomCSS = re.sub(EDIT_MORE, "", mw.reviewer._bottomCSS)

  if mw.state == "review":
     #mw.reviewer._initWeb()
     mw.moveToState("review")

# -- width of Show Answer button, triple, double and single answers buttons in pixels
BEAMS4 = "99%"
BEAMS3 = "74%"
BEAMS2 = "48%"
BEAMS1 = "24%"

# -------------------------------------------------------------------
# TOH
# 

HOTKEY = {      # in mw Main Window (deckBrowser, Overview, Reviewer)
    'F6_pause'  : ["F6", 'Alt+A, P ', "Alt+З, П ", ''' ''', """ """], 
    'F6_stop'   : ["Ctrl+F6", 'Alt+A, S ', "Alt+З, С ", ''' ''', """ """], 
    'F6_forw'   : ["Shift+F6", 'Alt+A, F ', "Alt+З, В ", ''' ''', """ """], 
    'F6_back'   : ["Alt+F6", 'Alt+A, B ', "Alt+З, Н ", ''' ''', """ """], 
    'F6_fast'   : ["Ctrl+Shift+F6", '', "", ''' ''', """ """], 
    'F6_slow'   : ["Ctrl+Alt+F6", '', "", ''' ''', """ """], 
    'F6_init'   : ["Ctrl+Alt+Shift+F6", '', "", ''' ''', """ """], 
    'F2_undo'   : ["F2", '', "Alt+К, О", ''' ''', """ """], 
    'F2_ctrl'   : ["Ctrl+Alt+Space", '', "Alt+К, Ч", ''' ''', """ """],  # ^F2
    'F2_card_reschedule' : ["Shift+Space", '', "Alt+К, А", ''' ''', """ """],  # ~F2
    'F2_note_reschedule' : ["Ctrl+Shift+Space", '', "Alt+К, З", ''' ''', """ """],  # ~F2
    'F3_history'     : ["F3", '', "Alt+К, И", ''' ''', """ """],  # View
    'F3_HTML_source'      : ["Ctrl+F3", '', "", ''' ''', """ """], 
    'F3_Body_source'      : ["Alt+F3", '', "Alt+К, Х", ''' ''', """ """], 
    'F3_card_stats'  : ["Shift+F3", '', "Alt+К, П", ''' ''', """ """], 
    'F3_A'      : ["Ctrl+F4", 'Alt+H, R', "Alt+П, У", ''' Help &rarr; A variables ''', """ Помощь &rArr; Управляющие переменные """], 
    'F4_edit'        : ["F4", '', "Alt+К, Е", ''' ''', """ """], 
    'F4_edit_layout' : ["Shift+F4", '', "Alt+К, К", ''' ''', """ """], 
    'edit_layout'    : ["Shift+E", '', "", ''' ''', """ """], 
    'goto_stats'    : ["S", '', "", ''' ''', """ """], 
    'goto_deck'     : ["Alt+S", '', "", ''' ''', """ """], 
    'delete_them_all'    : ["Ctrl+Alt+Shift+P", '', "", ''' ''', """ """], 
    'E' : ["E", '', "", ''' ''', """ """],  # Edit
    'marked'     : ["Shift+F8", '', "", ''' ''', """ """], 
    'META_Minus' : ["Ctrl+Alt+Shift+-", '', "", ''' ''', """ """], 
    'autoplay'   : ["Ctrl+Alt+Shift+F5", '', "", ''' ''', """ """], 
    'FrontSide'  : ["Ctrl+PgUp", '', "", ''' ''', """ """], 
    'BackSide'   : ["Ctrl+PgDown", '', "", ''' ''', """ """], 
    'F7_FrontSide' : ["F7", '', "", ''' ''', """ """], 
    'F8_BackSide'  : ["F8", '', "", ''' ''', """ """], 
    'FrontPage'    : ["Ctrl+9", '', "", ''' ''', """ """], 
    'BackPage'     : ["Ctrl+3", '', "", ''' ''', """ """], 
    'FrontPack'    : ["Ctrl+Up", '', "", ''' ''', """ """], 
    'BackPack'     : ["Ctrl+Down", '', "", ''' ''', """ """], 
    'FrontUp'      : ["Ctrl+8", '', "", ''' ''', """ """], 
    'BackDown'     : ["Ctrl+2", '', "", ''' ''', """ """], 
    'Editor'     : ["Ctrl+E", '', "", ''' ''', """ """], 
    'Statistics' : ["Shift+S", '', "", ''' ''', """ """], 
    'Rebuild_Them_All' : ["Ctrl+Shift+F", '', "", ''' ''', """ """], 
    'zoom_info'  : ["Alt+0", '', "", ''' ''', """ """], 
    'zoom_in'    : ["Ctrl++", '', "", ''' ''', """ """], 
    'zoom_out'   : ["Ctrl+-", '', "", ''' ''', """ """], 
    'zoom_reset' : ["Ctrl+0", '', "", ''' ''', """ """], 
    'zoom_init'  : ["Ctrl+Alt+0", '', "", ''' ''', """ """], 
    'toggle_last' : ["Ctrl+Space", '', "", ''' ''', """ """], 
    'expand_decks' : ["Ctrl+Shift++", '', "", ''' ''', """ """], 
    'collapse_decks' : ["Ctrl+Shift+-", '', "", ''' ''', """ """], 
    'download_addon' : ["Ctrl+Shift+Insert", '', "", ''' ''', """ """], 
    'download_addons' : ["Ctrl+Alt+Shift+Insert", '', "", ''' ''', """ """], 
    'next_hint' : ["F9", '', "", ''' ''', """ """], 
    'all_hints' : ["Shift+F9", '', "", ''' ''', """ """], 
    'bury_card' : ["-", '', "", ''' ''', """ """], 
    'bury_note' : ["Shift+-", '', "", ''' ''', """ """], 
    'suspend_card' : ["Alt+-", '', "", ''' ''', """ """], 
    'suspend_note' : ["Alt+Shift+-", '', "", ''' ''', """ """], 
    'audio_list'   : ["Alt+F5", '', "", ''' ''', """ """], 
    'replay_next'  : ["Shift+F5", '', "", ''' ''', """ """], 
    'full_screen'  : ["F11", '', "", ''' ''', """ """], 
    'swap'  : ["F12", '', "", ''' ''', """ """], 
}

HOTKEYS = {      # in Editor window
    'Freeze'     : ["F9", '', "", ''' ''', """ """], 
    'Frozen'     : ["Shift+F9", '', "", ''' ''', """ """], 
    'strike'     : ["Ctrl+s", '', "", ''' ''', """ """], 
    'ordered'    : ["Ctrl+Shift+O", '', "", ''' ''', """ """], 
    'unordered'  : ["Ctrl+Shift+U", '', "", ''' ''', """ """], 
    'indent'     : ["Ctrl+Shift+I", '', "", ''' ''', """ """], 
    'FE'         : ["Ctrl+F", '', "", ''' ''', """ """], 
    'nextCloze'  : ["Ctrl+Space", '', "", ''' ''', """ """], 
    'sameCloze'  : ["Ctrl+Alt+Space", '', "", ''' ''', """ """], 
    'showHTML'   : ["F4", '', "", ''' ''', """ """], 
}

HOTKEYZ = {      # Anki's default keyz: for information purpose only
    'Study_deck' : ["Ctrl+Shift+/", 'Alt+T, <br>Enter', "Alt+И, <br>Enter", ''' Tools -> Study deck ''', """ Инструменты -> Учить колоду... """], 
    'Import'     : ["Ctrl+Shift+I", 'Alt+F, I', "Alt+Ф, И", ''' File &rarr; Import...''', """ Файл &rArr; Импортировать... """], 
    'Export'     : ["Ctrl+Shift+E", 'Alt+F, E', "Alt+Ф, Э", ''' File &rarr; Export...''', """ Файл &rArr; Экспортировать... """], 
    'Decks'  : ["Ctrl+D", 'Alt+G, D', "Alt+Е, Д", ''' Go &rarr; Decks ''', """ Переход &rArr; """], 
    'Add'    : ["Ctrl+A", 'Alt+G, A', "Alt+Е, А", ''' Go &rarr; Add ''', """ Переход &rArr; """], 
    'Browse' : ["Ctrl+B", 'Alt+G, B', "Alt+Е, Б", ''' Go &rarr; Browse ''', """ Переход &rArr; """], 
    'Sync'       : ["Ctrl+Y", 'Alt+G, Y', "Alt+Е, Х", ''' Go &rarr; Synchronize with AnkiWeb ''', """ Переход &rArr; Синхронизировать с AnkiWeb """], 
    'Synchro'    : ["Ctrl+Shift+Y", 'Alt+F, Y', "Alt+Ф, Х", ''' File &rarr; Synchronize with AnkiWeb ''', """ Файл &rArr; Синхронизировать с AnkiWeb """], 
    'record_own_voice' : ["Shift+V", 'Alt+A, C', "Alt+З, З", ''' Audio &rarr; ''', """ Звук &rArr; """], 
    'replay_own_voice' : ["V", 'Alt+A, P', "Alt+З, В", ''' Audio &rarr; ''', """ Звук &rArr; """], 
    'options'          : ["O", 'Alt+E, O', "Alt+Р, Н", ''' Edit &rarr; Options ''', """ Редактирование &rArr;  """], 
}

# -------------------------------------------------------------------
# Field_Modifier_Random_Item.py
# Field Modifier: Random Item
# https://ankiweb.net/shared/info/1484572887

# Picks a random item from the field. Useful for images. Usage:
# {{random:Field Name}}
# Items are separated by commas. 

import random

from anki.cards import Card
from anki import hooks

if A['RANDOM_ITEM'][0]:

    def fmod_random(txt, extra, context, tag, fullname):
        return random.choice([x.strip() for x in txt.split(',')])

    addHook('fmod_random', fmod_random)

# -- Cool Idea, would be better if it worked on mobile
# Great idea, but troublesome if you frequently use the app rather than desktop version 
# since the random function doesn't work and you end up with a list separated by commas 

if A['RANDOM_SOUND'][0]:

    def fmod_sound(txt, extra, context, tag, fullname):
        _soundReg = "(\[sound:.*?\])"

        if txt.find('[sound:')>=0:
            #return random.choice(['[sound:'+x.strip() for x in txt.split('[sound:')][1:])
            #так вывозит, только если между звуками ничего нет или лишь пробелы
            return random.choice(re.findall(_soundReg, txt))
        else:
            return txt

    addHook('fmod_sound', fmod_sound)

#_soundReg = "\[sound:(.*?)\]"
#
#def playFromText(text):
#    for match in re.findall(_soundReg, text):
#        play(match)
#
#def stripSounds(text):
#    return re.sub(_soundReg, "", text)
#
#def hasSound(text):
#    return re.search(_soundReg, text) is not None

if A['MAKE_LIST'][0]:

    def fmod_list(txt, extra, context, tag, fullname):
        retv = ''
        if txt.find(';')>=0:
            for x in txt.split(';'):
                xx = x.strip()
                if len(xx)>0:
                    retv += '<li>'+xx+'</li>'
            return ('<ul>'+retv+'</ul>' if len(retv)>0 else '')
        elif txt.find(',')>=0:
            for x in txt.split(','):
                xx = x.strip()
                if len(xx)>0:
                    retv += '<li>'+xx+'</li>'
            return ('<ol>'+retv+'</ol>' if len(retv)>0 else '')
        else:
            return txt

    def fmod_sublist(txt, extra, context, tag, fullname):
        retv = ''
        if txt.find(';')>=0:
            for x in txt.split(';'):
                x = x.strip()
                if x.find(',')>=0:
                    retv += '<li><ul>'
                    for xx in x.split(','):
                        xxx = xx.strip()
                        if len(xxx)>0:
                            retv += '<li>'+xxx+'</li>'
                    retv += '</ul></li>'
                else:
                    if len(x)>0:
                        retv += '<li>'+x+'</li>'
            return ('<ul>'+retv+'</ul>' if len(retv)>0 else '')
        elif txt.find(',')>=0:
            for x in txt.split(','):
                xx = x.strip()
                if len(xx)>0:
                    retv += '<li>'+x.strip()+'</li>'
            return ('<ol>'+retv+'</ol>' if len(retv)>0 else '')
        else:
            return txt

    addHook('fmod_list', fmod_list)
    addHook('fmod_sublist', fmod_sublist)

# -------------------------------------------------------------------
from anki.utils import stripHTML, isMac, json

if True:

  try:
        mw.addon_view_menu
  except AttributeError:
        mw.addon_view_menu = QMenu(_(u"&Вид") if lang == 'ru' else _(u"&View"), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_view_menu)

if A['SET_INTERVAL'][0] or A['F4_EDIT'][0] or B['B00_MORE_OVERVIEW_STATS'][0] or A['COLORFUL_TOOLBAR'][0]:

  try:
        mw.addon_cards_menu
  except AttributeError:
        mw.addon_cards_menu = QMenu(_(u"&Карточки") if lang == 'ru' else _(u"&Cards"), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_cards_menu)

if A['F6_SOUND_KEY_MENU'][0] or A['COLORFUL_TOOLBAR'][0]:
  try:
        mw.addon_audio_menu
  except AttributeError:
        mw.addon_audio_menu = QMenu(_(u"&Звук") if lang == 'ru' else _(u"&Audio"), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_audio_menu)

if A['COLORFUL_TOOLBAR'][0] or A['FLIP_FLOP'][0]:
    try:
        mw.addon_go_menu.addSeparator()
    except AttributeError:
        mw.addon_go_menu = QMenu(u'П&ереход' if lang=='ru' else _(u"&Go"), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_go_menu)

mw_addon_view_menu_exists = hasattr(mw,'addon_view_menu')
mw_addon_cards_menu_exists = hasattr(mw,'addon_cards_menu')
mw_addon_audio_menu_exists = hasattr(mw,'addon_audio_menu')
mw_addon_go_menu_exists = hasattr(mw,'addon_go_menu')

# -- _______ /// _______ --

audio_speed = 1.0

if A['F6_SOUND_KEY_MENU'][0]:

    pause_auction = QAction(mw)
    pause_auction.setText(u'&Пауза' if lang=='ru' else _(u"&Pause"))
    if A['COLORFUL_TOOLBAR'][0]:
        pause_auction.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'player_pause.png')))
    pause_auction.setShortcut(QKeySequence(HOTKEY['F6_pause'][0]))
    mw.connect(pause_auction, SIGNAL("triggered()"), \
        lambda: anki.sound.mplayerManager.mplayer.stdin.write("pause\n") )

    pause_action = QAction(mw)
    pause_action.setText(u'&Пауза' if lang=='ru' else _(u"&Pause"))
    if A['ANKI_MENU_ICONS'][0]:
        pause_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'player_pause.png')))
    pause_action.setShortcut(QKeySequence(HOTKEY['F6_pause'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        pause_action.setEnabled(False)
    mw.connect(pause_action, SIGNAL("triggered()"), \
        lambda: anki.sound.mplayerManager.mplayer.stdin.write("pause\n") )

    stop_action = QAction(mw)
    stop_action.setText(u'&Стоп' if lang=='ru' else _(u"&Stop"))
    if A['ANKI_MENU_ICONS'][0]:
        stop_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'player_stop.png')))
    stop_action.setShortcut(QKeySequence(HOTKEY['F6_stop'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        stop_action.setEnabled(False)
    mw.connect(stop_action, SIGNAL("triggered()"), \
        lambda: anki.sound.mplayerManager.mplayer.stdin.write("stop\n") )

    forward_action = QAction(mw)
    forward_action.setText(u'&Вперёд 5 сек.' if lang=='ru' else _(u"&Forward 5 sec."))
    if A['ANKI_MENU_ICONS'][0]:
        forward_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'player_fwd.png')))
    forward_action.setShortcut(QKeySequence(HOTKEY['F6_forw'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        forward_action.setEnabled(False)
    mw.connect(forward_action, SIGNAL("triggered()"), \
        lambda: anki.sound.mplayerManager.mplayer.stdin.write("seek 5 0 \n") )

    backward_action = QAction(mw)
    backward_action.setText(u'&Назад 5 сек.' if lang=='ru' else _(u"&Backward 5 sec."))
    if A['ANKI_MENU_ICONS'][0]:
        backward_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'player_rew.png')))
    backward_action.setShortcut(QKeySequence(HOTKEY['F6_back'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        backward_action.setEnabled(False)
    mw.connect(backward_action, SIGNAL("triggered()"), \
        lambda: anki.sound.mplayerManager.mplayer.stdin.write("seek -5 0 \n") )

if A['F6_SOUND_KEY_MENU'][0] and A['F6_FAST_SLOW'][0]:

    def audio_play(speed):
        global audio_speed
        if speed:
            audio_speed = speed
        if anki.sound.mplayerManager is not None:
            if anki.sound.mplayerManager.mplayer is not None:
                anki.sound.mplayerManager.mplayer.stdin.write("af_add scaletempo=stride=10:overlap=0.8\n")
                anki.sound.mplayerManager.mplayer.stdin.write("speed_set %f \n"%audio_speed)

    fast_action = QAction(mw)
    fast_action.setText(u'&Быстрее на 10% (до 4.0)' if lang=='ru' else _(u"&Faster by 10% (max 4.0)"))
    if A['ANKI_MENU_ICONS'][0]:
        fast_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'audio-fast.png')))
    fast_action.setShortcut(QKeySequence(HOTKEY['F6_fast'][0]))
    #if A['COLORFUL_TOOLBAR'][0]:
    #    fast_action.setEnabled(False)
    mw.connect(fast_action, SIGNAL("triggered()"), \
        lambda: audio_play(min(4.0, audio_speed + 0.1)) )

    slow_action = QAction(mw)
    slow_action.setText(u'&Медленнее на 10% (до 0.1)' if lang=='ru' else _(u"&Slower by 10% (min 0.1)"))
    if A['ANKI_MENU_ICONS'][0]:
        slow_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'audio-slow.png')))
    slow_action.setShortcut(QKeySequence(HOTKEY['F6_slow'][0]))
    #if A['COLORFUL_TOOLBAR'][0]:
    #    slow_action.setEnabled(False)
    mw.connect(slow_action, SIGNAL("triggered()"), \
        lambda: audio_play(max(0.1, audio_speed - 0.1)) )

    init_action = QAction(mw)
    init_action.setText(u'&С нормальной скоростью 100%' if lang=='ru' else _(u"&Initial speed 100%"))
    if A['ANKI_MENU_ICONS'][0]:
        init_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'audio-play.png')))
    init_action.setShortcut(QKeySequence(HOTKEY['F6_init'][0]))
    #if A['COLORFUL_TOOLBAR'][0]:
    #    init_action.setEnabled(False)
    mw.connect(init_action, SIGNAL("triggered()"), \
        lambda: audio_play(1.0) )

    def my_runHandler(self):
        _self = anki.sound.mplayerManager
        global mplayerClear
        _self.mplayer = None
        _self.deadPlayers = []
        while 1:
            anki.sound.mplayerEvt.wait()
            anki.sound.mplayerEvt.clear()
            
            # clearing queue?
            if anki.sound.mplayerClear and _self.mplayer:
                try:
                    _self.mplayer.stdin.write("stop\n")
                except:
                    # mplayer quit by user (likely video)
                    _self.deadPlayers.append(_self.mplayer)
                    _self.mplayer = None

            # loop through files to play
            while anki.sound.mplayerQueue:
                # ensure started
                if not _self.mplayer:
                    _self.startProcess()
                # pop a file
                try:
                    item = anki.sound.mplayerQueue.pop(0)
                    _self.mplayer.stdin.write("stop\n")
                except IndexError:
                    # queue was cleared by main thread
                    continue
                if anki.sound.mplayerClear:
                    anki.sound.mplayerClear = False
                    extra = ""
                else:
                    extra = " 1"
                cmd = 'loadfile "%s"%s\n' % (item, extra)
                
                try:
                    _self.mplayer.stdin.write(cmd)
                except:
                    # mplayer has quit and needs restarting
                    _self.deadPlayers.append(_self.mplayer)
                    _self.mplayer = None
                    _self.startProcess()
                    _self.mplayer.stdin.write(cmd)
                
                if abs(audio_speed - 1.0) > 0.01:
                    _self.mplayer.stdin.write("af_add scaletempo=stride=10:overlap=0.8\n")
                    _self.mplayer.stdin.write("speed_set %f \n" % audio_speed)
                    _self.mplayer.stdin.write("seek 0 1\n")
                
                # if we feed mplayer too fast it loses files
                time.sleep(1)
            # wait() on finished processes. we don't want to block on the
            # wait, so we keep trying each time we're reactivated
            def clean(pl):
                if pl.poll() is not None:
                    pl.wait()
                    return False
                else:
                    return True
            _self.deadPlayers = [pl for pl in _self.deadPlayers if clean(pl)]

    def store_file(regex_string):
        global audio_file
        audio_file = regex_string.group(1)
        
    def audio_filter(qa_html, qa_type, dummy_fields, dummy_model, dummy_data, dummy_col):
        re.sub(sound_re, store_file, qa_html)
        return qa_html

    MplayerMonitor.run = my_runHandler
    addHook("mungeQA", audio_filter)

# -- _______ /// _______ --

def go_edit_current():
    """Edit the current card when there is one."""
    try:
        mw.onEditCurrent()
    except AttributeError:
        pass

def go_edit_layout():
    """Edit the current card's note's layout if there is one."""
    try:
        ccard = mw.reviewer.card
        clayout.CardLayout(mw, ccard.note(), ord=ccard.ord)
        #go_study()
    except AttributeError:
        return

if mw_addon_cards_menu_exists: 

    undo_action = QAction(mw)
    undo_action.setText(u'&Обратно' if lang=='ru' else _(u"&Go back"))
    if A['ANKI_MENU_ICONS'][0]:
        undo_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'undo.png')))
    undo_action.setShortcut(QKeySequence(HOTKEY['F2_undo'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        undo_action.setEnabled(False)
    mw.connect(undo_action, SIGNAL("triggered()"), mw.onUndo)

    mw.addon_cards_menu.addAction(undo_action)

###################################################################
# Reschedule_as_new_key_shortcut.py

if A['RESET_CARD_SCHEDULING'][0]:

  def onForgetCard(self):
   if askUser(u"Сбросить расписание для данной карточки?" if lang=="ru" else "Reschedule as new card?"):
    self.mw.checkpoint(_("Forget Card"))

    self.mw.col.sched.removeLrn(   [ self.card.id ] )
    self.mw.col.sched.remFromDyn(  [ self.card.id ] )
    self.mw.col.sched.resetCards(  [ self.card.id ] )

    tooltip(u"Карточка поставлена в конец очереди новых карточек." if lang=="ru" else _("Card rescheduled as new"))
    self.mw.reset()

  def onForgetNote(self):
   if askUser(u"Сбросить расписание для всех карточек данной записи?" if lang=="ru" else "Reschedule all cards of current note?"):
    self.mw.checkpoint(_("Forget Note"))

    self.mw.col.sched.removeLrn(   sorted([ c.id for c in self.card.note().cards() ]) )
    self.mw.col.sched.remFromDyn(  sorted([ c.id for c in self.card.note().cards() ]) )
    self.mw.col.sched.resetCards(  sorted([ c.id for c in self.card.note().cards() ]) )

    tooltip(u"Карточки записи поставлены в конец очереди новых карточек." if lang=="ru" else _("Cards of note are rescheduled as new"))
    self.mw.reset()

if A['F4_EDIT'][0]:

    F4_edit_current_action = QAction(mw)
    F4_edit_current_action.setText(u'Р&едактирование...' if lang=='ru' else _(u"&Edit..."))
    if A['ANKI_MENU_ICONS'][0]:
        F4_edit_current_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_current.png')))
    F4_edit_current_action.setShortcut(QKeySequence(HOTKEY['F4_edit'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        F4_edit_current_action.setEnabled(False)
    mw.connect(F4_edit_current_action, SIGNAL("triggered()"), go_edit_current)

    F4_edit_layout_action = QAction(mw)
    F4_edit_layout_action.setText(u'&Карточки...' if lang=='ru' else _(u"&Cards..."))
    if A['ANKI_MENU_ICONS'][0]:
        F4_edit_layout_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_layout.png')))
    F4_edit_layout_action.setShortcut(QKeySequence(HOTKEY['F4_edit_layout'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        F4_edit_layout_action.setEnabled(False)
    mw.connect(F4_edit_layout_action, SIGNAL("triggered()"), go_edit_layout)

    if mw_addon_cards_menu_exists:
        mw.addon_cards_menu.addSeparator()
        mw.addon_cards_menu.addAction(F4_edit_current_action)
        mw.addon_cards_menu.addAction(F4_edit_layout_action)
        mw.addon_cards_menu.addSeparator()

if A['RESET_CARD_SCHEDULING'][0]:

    #Reviewer.onForget = onForget
    F2_FORGET_ME_NOT_action = QAction(mw)
    F2_FORGET_ME_NOT_action.setText(u"Только эту к&арточку - в конец очереди новых..." if lang=="ru" else "Reschedule Card as &New...")
    if A['ANKI_MENU_ICONS'][0]:
        F2_FORGET_ME_NOT_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'new.png')))
    F2_FORGET_ME_NOT_action.setShortcut(QKeySequence(HOTKEY['F2_card_reschedule'][0]))
    mw.connect(F2_FORGET_ME_NOT_action, SIGNAL("triggered()"), lambda self=mw.reviewer: onForgetCard(self)) #mw.reviewer.onForget)

    F2_FORGET_ME_NOTE_action = QAction(mw)
    F2_FORGET_ME_NOTE_action.setText(u"Все карточки &записи - в конец очереди новых карточек..." if lang=="ru" else "Reschedule Note as &New Cards...")
    if A['ANKI_MENU_ICONS'][0]:
        F2_FORGET_ME_NOTE_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'queue.png')))
    F2_FORGET_ME_NOTE_action.setShortcut(QKeySequence(HOTKEY['F2_note_reschedule'][0]))
    mw.connect(F2_FORGET_ME_NOTE_action, SIGNAL("triggered()"), lambda self=mw.reviewer: onForgetNote(self)) #mw.reviewer.onForget)

    if mw_addon_cards_menu_exists:
        mw.addon_cards_menu.addSeparator()
        mw.addon_cards_menu.addAction(F2_FORGET_ME_NOT_action)
        mw.addon_cards_menu.addAction(F2_FORGET_ME_NOTE_action)

# Date:     January 27, 2016
# Author:   Benjamin Gray
# File:     Quick_Reschedule.py
# Purpose:  Quickly reschedule cards in anki to a user specified interval using sched.reschedCards()

import random

# prompt for new interval, and set it
def promptNewInterval():
    if mw.state == 'review':
        if True:
            days = unicode(mw.reviewer.card.ivl+1)
            dayString = getText((u"Дней до следующего просмотра карточки (текущий интервал + 1 = %s ):" \
                if lang=='ru' else \
                "Number of days until next review (current interval + 1 = %s ):") % (days), default=days)
            if dayString[1]:
                dayString0 = dayString[0].strip().lower()
                dayStringM = False
                dayStringW = False
                dayStringI = False
                if dayString0.endswith('m') or dayString0.endswith(u'м'):
                    dayString0 = dayString0[:-1].strip()
                    dayStringM = True
                if dayString0.endswith('w') or dayString0.endswith(u'н'):
                    dayString0 = dayString0[:-1].strip()
                    dayStringW = True
                if len(dayString0)==0:
                    dayString0 = '1'

                try:
                    days = int(dayString0)
                    dayz = float(0)
                    if dayStringM:
                        dayz = abs(float(days))
                        days = 0
                    if dayStringW:
                        dayz = float(0)
                        days = abs(days) * 7
                    if days < 0:
                        dayStringI = True
                except ValueError:
                    days = mw.reviewer.card.ivl+1
                    try:
                        dayz = abs(float(dayString0))
                        if 0<dayz and dayz<1:
                            days = int(dayz*10) * 7
                            dayz = 0
                            dayStringW = True
                        else:
                            days = 0
                            dayStringM = True
                    except ValueError:
                        dayz = float(0)

                if dayz > 0: # 3.1 or 1.2 is monthes
                    days = int(31*dayz)+random.randrange(-15, 15+1, 1)
                elif dayStringW: # .2 is two weeks
                    days = abs(days)+random.randrange(-3, 3+1, 1)
                elif days > 10:
                    days = days + random.randrange(-1, 1+1, 1)
                elif days > 0: # from 1 to 9 setup exact number of day
                    pass # days = days 
                elif days <= 0:
                    days = mw.reviewer.card.ivl+1
                    #days = days * 60 # num<0 == interval in seconds

                #showWarning(unicode(dayString)+' '+str(dayz)+' '+str(days))

                mw.checkpoint(_("Reschedule card"))
                mw.col.sched.reschedCards( [mw.reviewer.card.id], days-1 if days>1 else 1, days+1 )
                days_mod = (days % 10) if ( (days%100) < 11 or (days%100) > 14) else (days % 100)
                tooltip( (u"Запланирован просмотр через <b>%s</b> "+("день" if days_mod==1 else ("дня" if days_mod>=2 and days_mod<=4 else "дней")) if lang=='ru' else \
                    'Rescheduled for review in <b>%s</b> days') % (days) )
                mw.reset()
    else:
        tooltip("Задавать дни до следующего просмотра можно только при просмотре карточек!" if lang=='ru' else \
            'Prompt for new interval available only on answer side (BackSide) of card\'s reviewer.')

if A['SET_INTERVAL'][0]:
    set_new_int_action = QAction(mw)
    set_new_int_action.setText(u'&Через ... дней' if lang=='ru' else _(u"&Prompt and Set ... days interval"))
    if A['ANKI_MENU_ICONS'][0]:
        set_new_int_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'schedule.png')))
    set_new_int_action.setShortcut(QKeySequence(HOTKEY['F2_ctrl'][0]))
    if A['COLORFUL_TOOLBAR'][0]:
        set_new_int_action.setEnabled(False)
    mw.connect(set_new_int_action, SIGNAL("triggered()"), promptNewInterval)
    if mw_addon_cards_menu_exists:
        mw.addon_cards_menu.addAction(set_new_int_action)
        mw.addon_cards_menu.addSeparator()

# ----------------------------------------------------------------------------
BUTTON_LABEL = [None, _("Again"), _("Hard"), _("Good"), _("Easy")]

# Button_Colours_Good_Again.py
# This add-on makes "Good" green and "Again" red. It's a little like Anki 1 or AnkiDroid.

# Author: Calumks <calumks@gmail.com>
# Get reviewer class -- Monkey patching

dflt = '#000'

def color_buttons():
    global dflt, btn_Later, btn_Again, btn_Hard, btn_Good, btn_Easy
    for lbls in BUTTON_LABELS:
       if lbls[0] == lang:
           BUTTON_LABEL[0] = lang
           BUTTON_LABEL[1] = lbls[1]
           BUTTON_LABEL[2] = lbls[2]
           BUTTON_LABEL[3] = lbls[3]
           BUTTON_LABEL[4] = lbls[4]
           break
    if B['B08_BIG_BUTTONS'][0]:
        dflt = '#666'
    else:
        dflt = '#333' # 'default'
    if B['B07_COLOR_BUTTONS'][0]:
       btn_Again = ['#c33', BUTTON_LABEL[1]]
       btn_Hard = ['#c90', BUTTON_LABEL[2]] 
       btn_Good = ['#3c3', BUTTON_LABEL[3]] 
       btn_Easy = ['#69f', BUTTON_LABEL[4]] 
    else:
       btn_Again = [dflt, BUTTON_LABEL[1]]
       btn_Hard = [dflt, BUTTON_LABEL[2]] 
       btn_Good = [dflt, BUTTON_LABEL[3]] 
       btn_Easy = [dflt, BUTTON_LABEL[4]] 
color_buttons()

##################################################################
# Card Info During Review
# https://ankiweb.net/shared/info/2179254157

# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Show statistics about the current and previous card while reviewing.
# Activate from the tools menu.
#
# Card stats
##########################################################################

from anki.stats import CardStats

if A['F3_CARD_INFO_DURING_REVIEW'][0]:

  # 1300 is the minimum ease, the card may actually be harder.
  lowest_ease_possible = 1300

  def percFromBaseToExtreme(value, base, extreme):
    """Shows, in %, where value is on the way from base to extreme.

    Used for coloring numbers.
    """
    # Examples:
    # base = 2500, extreme = 1300; 2500 - 1300 = 1200.
    # value 1300: (2500 - 1300) / 1200 = 100%
    # value 1900: (2500 - 1900 = 600) / 1200 = 50%
    # value 2500: (2500 - 2500) / whatever = 0%
    # base = 2500, extreme = 3560, 2500 - 3560 = -1060
    # value 2600: (2500 - 2600 = -100) / 1060 = 9%
    if base == extreme:
        perc = 100
    else:
        perc = int(round( 100 * (base - value) / (base - extreme), 0 ))
        if perc > 100:
            perc = 100

    return perc

  def reps_for_total_ivl(ivl, FACTOR, max_total_ivl):
    """Repetitions required to retain during max_total_ivl from now."""

    if ivl == 0:
        return 0

    for (reps, total_ivl) in total_ivls(ivl, FACTOR / 1000.0):

        if total_ivl >= max_total_ivl:
            return reps

  def total_ivls(ivl, ease):
    """The total sum of intervals for each number of repetitions.

    >>> total_ivls(20, 2.50)[:2]
    [(1, 50), (2, 175), (3, 525)]

    """

    total_ivl = 0

    for reps in range(1, 999):

        ivl *= ease
        total_ivl += ivl

        yield (reps, total_ivl)

  def get_time_avg(all_times):
    """Takes duration of almost every review and returns average.
    Skips the oldest reviews if there is enough.

    Durations are in seconds.
    """

    if len(all_times) < 7:
        timeList = all_times
    else:
        oldest_count = len(all_times) // 5
        timeList = all_times[oldest_count - 1:]

    time_avg = sum(timeList) / float(len(timeList))  # much faster than numpy.mean

    return time_avg

  def repstime(days, time_avg, ivl, FACTOR):
    """Returns time needed to know this card for days days since next
    answer (for Review cards only).
    """
    if days <= 0:   # forecast requested for before the due date
        return 0
    else:
        reps = repsForIvlFactorAndMaximum(ivl=ivl, FACTOR=FACTOR, days=days)
        return reps * time_avg

  def repstime_s(days, FACTOR, time_avg, ivl, cardStatsObject):
    """Returns time as "1m 30s"
    """
    time_num = repstime(days=days, time_avg=time_avg, ivl=ivl, FACTOR=FACTOR)
    timestr = cardStatsObject.time(time_num)
    if FACTOR <= lowest_ease_possible:
        fmt_time = '>=%s' % timestr
    else:
        fmt_time = '%s' % timestr

    # To make forecast times red if they are big.
    foretime_base = 60
    foretime_max = 330
    foretime_red_perc = foretime_green_perc = 0

    if (days > (365 * 3) and time_num < 10):
        foretime_green_perc = 50
    elif days > (365 * 40):
        fmt_time = '<small>%s</small>' % fmt_time
    elif time_num > foretime_base:
        foretime_red_perc = percFromBaseToExtreme(
                time_num, foretime_base, foretime_max)

    if time_num >= 120:
        fmt_time = '<i>%s</i>' % fmt_time

    fmt_time = u'<span style="font-style:italic;font-weight:bold;color: rgb({0}%, {1}%, 0%)">{2}</span>'.format(
            foretime_red_perc, foretime_green_perc, fmt_time)

    return fmt_time

  def repsForIvlFactorAndMaximum(ivl, FACTOR, days):
    # I guess this is currently just a proxy because I wanted to adapt it
    # for cards due in the future.  Then it will subtract the "due in"
    # time from the "days".  Note that getForecast does it now.
    return reps_for_total_ivl(ivl=ivl, FACTOR=FACTOR, max_total_ivl=days)

  # The following 2 functions are used in other add-ons only.

  def getForecastText(self, c, forecast_days):
    # Returns text forecast for card c in seconds, with "s" added.
    f = getForecast(self, c, forecast_days)
    if f:
        return (str(int(f)) + ' s')
    else:
        return ''

  # Copyright: Aleksej
  # Based on anki.stats from Anki 2.0.15 (the report function by Damien Elmes
  # <anki@ichi2.net>).
  # License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

  def getForecast(self, c, forecast_days):
    # Returns forecast for card c in seconds.
        if not (c.ivl > 0):
            return  # in-learning cards not supported

        all_times = self.col.db.list(
            "select time/1000 from revlog where cid = :id",
            id=c.id)

        cnt = len(all_times)

        if cnt:

            time_avg = get_time_avg(all_times)

            def repstime_this(days):
                return repstime(days=days, time_avg=time_avg, ivl=c.ivl,
                                FACTOR=c.factor)

            if c.queue in (2,3):
                if c.due > self.col.sched.today:
                    forecast_days -= (c.due - self.col.sched.today)

            forecast = repstime_this(forecast_days)
            if forecast:
                return forecast
            else:
                return None

  """
https://ankiweb.net/shared/info/2189699505

Card time forecast
0.01MB. Updated 2015-12-05.

Description

In the card-specific statistics table (which I use with Damien's "Card Info During Review", see below),

* shows how much review time may be needed to retain the memory for 5, 10, 15 years, assuming the "Good" button is pressed every time;
** it does not consider forgetting index (which is assumed to be about 90%); calculating with it directly every time would be slow (if it affects the relative numbers, maybe the effect could be approximated differently?);
** as of 2013-06-18, it uses only the mean average of the recent ≈5 review times; it used also the median in the past, but now the functions are used in add-ons for multi-card forecasts, which need speed (calculating a median with NumPy is almost 10 times slower than calculating a mean manually);
* highlights low ease with red, considering its distance from the first ease (only for cards with at least 4 ratings).  Also highlights high ease with green, change opt_use_green_for_ease in the code to disable that.
* highlights forecast time with red, considering its distance from 60s, with #FF red at 330s+ (5.5m).

* I haven't considered Interval modifier; using it may make this add-on show incorrect forecasts and highlights.
* The add-on replaces CardStats.report, so if that is updated or replaced by a different add-on, something about card info output might break (but probably no dataloss).

System requirements:
* Recommended: "Card Info During Review" (to show the info in a sidebar).

Links
* Source code repository (GitHub): github.com/aleksejrs/anki-2.0-card-time-forecast;
* Old repository location (Gitorious): gitorious.org/anki-2-0-card-time-forecast-and-ease-warner;
* another Ease-related add-on: Suggest Starting Ease for the deck's options group.
* another forecast add-on (depends on this one): Study screen time forecast.
* You may be wondering if there is a way to show a forecast for each card in the browser.  I have an add-on for that, which is a module for an old alpha version of Advanced Browser. I've renamed the files, so it works alongside current version of AB.

Ideas

I am not a programmer, so these are ideas, not plans.
* Return to using mean for single-card calculation when NumPy is installed?
* Younger cards have longer forecasts, so they look harder, and their forecast is colored red.
** When coloring, consider total time of the reviews.
*** Alone, that will confuse cards whose learning has been restarted (after editing, or acquiring the knowledge necessary to memorize them).
* Make the configurability of the medium ease more prominent (currently it's the Starting ease).

Feedback?
If you want me to notice your feedback soon, please use either:
* the TenderApp discussion area (mention the add-on name in the message title);

* GitHub issue tracker.

Changelog (by date of upload)
* 2015-10-16: increased the max number of reviews in a forecast from about 998 to about 99999. I hope it does not affect performance (haven't tested).
* (2015-03-25: source code moved to GitHub, because Gitorious will be closed in May)
* 2014-12-25: for coloring, use the card's first ease, not the average of it and 250.
* 2013-10-23: from Anki 2.0.15: add Note ID and Card ID to the info table.
* 2013-06-17: stop using Numpy and calculating median, use average only. It is one dependency less for this add-on, and at least 1.5 times faster for multi-card forecast by other add-ons which will depend on this one (also added two functions for them).  This made my forecast times about 10% bigger.  A problem this has is for cards which have accidentally been left for a minute.  However, that is good if you consider cards that have been left for a minute 2 of 5 times not by an accident.  For filtered decks, the source deck is also shown now.
* 2013-04-04: colors forecast times over 60s with red (gradient with upper value of 330s); removed my deck-specific tweaks and 1-year forecast; fixed a bug (probably division by zero)
* 2013-03-27: added an option to disable green colouring of Ease numbers.
* 2013-03-06: first version published here. Unlike the really first version, it highlights ease and has a better code structure.
  """

if A['F3_CARD_INFO_DURING_REVIEW'][0] or A['F3_CARD_HISTORY'][0]:

  def addRLine(self, k, v):
    """Add a line with right-aligned caption to a CardStats object"""
    self.txt += "<tr><td align=right style='padding:.1em .25em;'><b>%s</b></td><td style='padding:.1em .5em;'>%s</td></tr>" % (k, v)

  def glocal_revlogDatum(self, crd):
    entries = mw.col.db.all(
        "select id/1000.0, ease, ivl, FACTOR, time/1000.0, type "
        "from revlog where cid = ? order by id desc limit 1", crd.id)
    if not entries:
        return ""
    s = ""
    for (date, ease, ivl, FACTOR, taken, type) in reversed(entries):
        #tstr = [_("Learn"), _("Review"), _("Relearn"), _("Filtered"), _("Resched")][type]
        import anki.stats as st
        fmt = "<span style='color:%s'>%s</span>"
        if ease == 1:
            retv = fmt % (st.colRelearn, _("Again"))
        else:
            if type==0 or type==3:
                easy = ["", _("Again"),_("Good"),_("Easy"), "", ""]
            elif type==2:
                easy = ["", _("Again"),_("Good"), "", "", ""]
            else:
                easy = ["", _("Again"),_("Hard"),_("Good"),_("Easy"), ""]
            retv = easy[ease]
            if retv == "":
                retv = easy[ease-1]
                if retv == "":
                    retv = easy[ease-2]
    self.addLine(("Последний ответ" if lang=="ru" else _('Last answer'))+":", "<span style='color:#666;'>" + unicode(retv) + 
        "</span> &nbsp; <span style=font-weight:400;>(" + str(ease) + ") <sub>%d</sub> </span>" % type)
    self.addLine(("Текущий интервал" if lang=="ru" else _('Current interval'))+":", " &nbsp; <span style=font-weight:700;>" + str(ivl) + " </span>")

# by Anki user rjgoif
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# https://ankiweb.net/shared/info/1581856587
# extra card stats ×

# This addon displays the original due date and intervals for cards in filtered decks.
# For all decks (filtered and normal), it also adds another statistic:
# if the card is not due today, it also displays the days early or days overdue
#	and the percent early/late compared to the current interval.
# I made this to assist in the development of my other add-ons, but additionally
#	I just like having that information available when I am studying. 

###################### VERSION 0004 ######################### 2016-03-09

"""
A simple add-on that lists a few more stats to your cards, including if you have the add-on that displays stats while you review (which can be found <a href="https://ankiweb.net/shared/info/2179254157" rel="nofollow">here</a>. 

Stats added:
- home deck and home deck (original) due date when studying filtered decks
- days overdue in regular and filtered decks
- days early in filtered decks
- relative lateness/earliness when the card being studied is either early (filtered decks) or late (regular or filtered).

Change log:
<b>v0004</b>
- fixed date formatting bug for lapsed cards

<b>v0003</b>
- fixed divide-by-zero bug.

<b>v0002</b>
- fixed bug caused by preview-ahead cards being considered as part of the "new" queue (bug an artifact of developing the add-on with some other unreleased add-ons active. Whoops.)
- correctly removed the (Home) Due line from card stats when they are not in a filtered deck.
"""

if A['F3_CARD_INFO_DURING_REVIEW'][0]:
  
  #class CardStat(object):
  #    def __init__(self, col, card):
  #        self.col = col
  #        self.card = card
  #    def report(self):
  def aleksejCardStatsReportForForecast(self):
        
        # Make Ease number green for easy cards.  Low ease numbers are marked
        # red, so you may want to disable this if it is difficult for you to
        # distinguish red and green.
        opt_use_green_for_ease = True

        c = self.card
        fmt = lambda x, **kwargs: fmtTimeSpan(x, short=True, **kwargs)
        self.txt = "<!--style>.cs tr:nth-child(2n){background-color:#eee;}</style--><table class=cs width=100% style='border-collapse:collapse;' cellspacing=0>"

        self.glocal_revlogDatum(c)

        if c.note().tags:
            Tags = ""
            for tag in c.note().tags:
                Tags += " " + tag 
            self.addLine(_("Tags"), '<span style="font-weight:bold;color:Chocolate;">'+Tags+'</span>')

        first = self.col.db.scalar(
            "select min(id) from revlog where cid = ?", c.id)
        last = self.col.db.scalar(
            "select max(id) from revlog where cid = ?", c.id)

        frctOverdue = None
        frctOverdueStr = ""
        if c.type in (1,2):
            if c.odid or c.queue < 0:
                next = None
                overdue = None
            else:
                if c.queue in (2,3) or (c.queue == 0 and c.type == 2):
                    #next = time.time()+((c.due - self.col.sched.today)*86400)
                    if c.odue:
                        next = time.time()+((c.odue - self.col.sched.today)*86400)
                        overdue = self.col.sched.today - c.odue
                    else:
                        next = time.time()+((c.due - self.col.sched.today)*86400)
                        overdue = self.col.sched.today - c.due
                    if c.ivl > 0:
                        frctOverdue = abs(overdue / c.ivl)
                        if round(frctOverdue,3) >= 0.1:
                            frctOverdueStr = " (%.0f%%)" % (frctOverdue*100)
                        elif round(frctOverdue,3) >= 0.001:
                            frctOverdueStr = " (%.1f%%)" % (frctOverdue*100)
                        else:
                            frctOverdueStr = " (<0.1%)"
                else:
                    next = c.due
                    overdue = None
                next = self.date(next)
            if next and last and next != self.date(last/1000):
              self.addLine(_("(Home) Due") if c.odue else _("Due"), '<span style="color:blue;">'+next+'</span>')

        if c.lapses > 0:
            self.addLine(_("Lapses"), "<span style=color:red;>%d</span>" % c.lapses)

        if c.reps > 0:
            self.addLine(_("Reviews"), "%d" % c.reps)

        if c.type in (1,2):
            if c.queue == 2 or (c.queue == 0 and c.type == 2):
                if overdue > 0 and frctOverdue:
                    self.addLine(_("Overdue"), fmt(overdue * 86400) + frctOverdueStr)
                elif overdue < 0 and frctOverdue:
                    self.addLine(_("Early"), fmt(-overdue * 86400) + frctOverdueStr)
                self.addLine("<span style = color:green;>" + _("Interval") + "</span>", "<span style = color:green;>" + fmt(c.ivl * 86400) + "</span>")
                #self.addLine(_("Ease"), "%d%%" % (c.factor/10.0))

                ##

                ease_str = '%d%%' % (c.factor / 10.0)
                if c.factor <= lowest_ease_possible:
                    ease_str = '<i>%s</i>' % ease_str

                all_times = self.col.db.list(
                    "select time/1000 from revlog where cid = :id",
                    id=c.id)

                cnt = len(all_times)

                ease_green_perc = ease_red_perc = 0
                # Making the Ease number red or green.
                if cnt > 4:
                    first_factor = self.col.db.list(
                        "select FACTOR from revlog where cid = :id and FACTOR <> 0 limit 1",
                        id=c.id)

                    # Account for a custom Starting Ease at the first review.
                    if len(first_factor) > 0:
                        medium_ease = first_factor[0]
                    else:
                        medium_ease = 2500

                    if c.factor < medium_ease:
                        ease_green_perc = 0
                        ease_red_perc = percFromBaseToExtreme(
                                    c.factor, medium_ease, lowest_ease_possible)
                    # If the card is easy, make the number green.
                    # XXX: This is not very useful, and may be bad for
                    # accessibility (color blindness).  To disable it, change
                    # opt_use_green_for_ease above to False.
                    elif c.factor > medium_ease and opt_use_green_for_ease:
                        # Precision is probably not important here.
                        highest_ease_possible = 3560
                        ease_red_perc = 0
                        ease_green_perc = percFromBaseToExtreme(
                                    c.factor, medium_ease, highest_ease_possible)

                ease_rgb = '<span style="color:rgb({0}%,{1}%,0%);cursor:help;"'+\
                    (' title=" color:rgb({0}%,{1}%,0%); "' if B['B11_BUTTON_TITLES'][0] else '')+'>'.format(
                            ease_red_perc, ease_green_perc)

                self.addLine(ease_rgb + _("Ease") + "</span>", ease_rgb + ease_str + "</span>")

                ##

            (cnt, total) = self.col.db.first(
                "select count(), sum(time)/1000 from revlog where cid = :id",
                id=c.id)

            if cnt:
                self.addLine(_(u"Time") if c.reps==1 else _("Average Time"), "<span style = color:blueviolet; >" + unicode(self.time(total / float(cnt))) + "</span>")
                if c.reps>1:
                    self.addLine(_("Total Time"), "<span style = color:indigo; >" + unicode(self.timer(total)) + "</span>")

                ##

            if c.queue==2 and cnt:
                time_avg = get_time_avg(all_times)

                def repstime_this(days):
                    return repstime(days=days, time_avg=time_avg,
                                ivl=c.ivl, FACTOR=c.factor)

                def addCardForecast(caption, days):
                    if not (c.ivl > 0):
                        return  # in-learning cards not supported
#                    caption = fmt(days * 86400)

#                    time_num = repstime(
#                        days=days, time_avg=time_avg,
#                        ivl=c.ivl, FACTOR=c.factor)
                    time_str = repstime_s(days=days, FACTOR=c.factor,
                            time_avg=time_avg,
                            ivl=c.ivl, cardStatsObject=self)

                    years = days / 365.0

                    if years == 15:
                        caption = ('<span style="color: green">%s</span>' %
                                caption)
                    elif years == 40:
                        caption = '<small>%s</small>' % caption

                    addRLine(self, caption, time_str)

                if cnt >= 3 or (cnt >= 2 and c.ivl > 100):
                    # Account for cards due in the future -- consider the
                    # due date the date of the next answer.
                    subtract_from_forecast_days = 0
                    if c.queue in (2,3) and c.due > self.col.sched.today:
                        subtract_from_forecast_days = (c.due - self.col.sched.today)

#                   forecast_list = [('1 Y', 365 * 1),
                    forecast_list = [('5 Y', 365 * 5),
                                     ('10 Y', 365 * 10),
                                     ('15 Y', 365 * 15)]
#                                     ('40 Y', 365 * 40)]

                    forecast_captions, forecast_days = zip(*forecast_list)
                    forecast_captions, forecast_days = list(forecast_captions), list(forecast_days)
                    forecast_days.append(365 * 100)

                    for i in range(len(forecast_list)):
                        # Show no more than one forecast of 8 seconds or less.
                        nextIsNotVerySmall = repstime_this(forecast_days[i + 1] - subtract_from_forecast_days) > 8
                        # Skip the forecast if the next one is the same.
                        nextIsBigger = (repstime_this(forecast_days[i] - subtract_from_forecast_days) <
                                        repstime_this(forecast_days[i + 1] - subtract_from_forecast_days))

                        if nextIsNotVerySmall and nextIsBigger:
                            addCardForecast(forecast_captions[i], forecast_days[i] -
                                            subtract_from_forecast_days)

                ##

        elif c.queue == 0:
            self.addLine(_("Position"), c.due)

        if not first or first and self.date(c.id/1000) != self.date(last/1000):
            self.addLine(_("Added"), '<span style="color:cornflowerblue;">'+self.date(c.id/1000)+'</span>')
        if first and self.date(c.note().mod) != self.date(c.id/1000):
            self.addLine(_("Edited"), '<span style="color:royalblue;">'+self.date(c.note().mod)+'</span>')
        #if first and self.date(c.mod) != self.date(last/1000):
        #    self.addLine(_("Changed"), '<span style="color:cornflowerblue;">'+self.date(c.mod)+'</span>')

        if first and last and self.date(first/1000) != self.date(last/1000):
            self.addLine(_("First Review"), '<span style="color:cornflowerblue;">'+self.date(first/1000)+'</span>')
            self.addLine(_("Latest Review"), '<span style="color:royalblue;">'+self.date(last/1000)+'</span>')
        elif first and last and self.date(first/1000)==self.date(last/1000):
            self.addLine(_("Review"), '<span style="color:royalblue;">'+self.date(first/1000)+'</span>')

        self.addLine(_("Card Type")+' '+str(c.ord+1), '<div style="color:cornflowerblue;">'+c.template()['name']+'</div>')

        d = c.model()['name']
        if d != c.template()['name']:
            self.addLine(_("Note Type"), "<div style='color:#333;'>"+d+"</div>")

        def ddd(d,t):
          if d != c.model()['name']:
            dixis = d.split('::')
            dd = ''
            i = 0
            for dixie in dixis:
                dd += "<br>" if i > 0 else ""
                dd += "&ndash;&nbsp;" if i==1 else "&mdash;&nbsp;" if i>0 else "" #*i
                i += 1
                dd += dixie # (dixie[:20]+"&hellip;") if len(dixie) > 20 else dixie
            self.addLine(t, "<div"+\
                (" title=' "+d.replace('::','\n')+" '" if B['B11_BUTTON_TITLES'][0] else "")+\
                " style='cursor:help;color:gray;'>"+dd+"</div>")

        if c.odid:
            ddd( self.col.decks.name(c.odid), "Исходная колода" if lang=="ru" else _("(Home) Deck") )
        ddd( self.col.decks.name(c.did), _("Deck") )

        self.addLine(_("Card ID"), '<span style="font-weight:400;color:cornflowerblue;">'+str(c.id)+'</span>')
        self.addLine(_("Note ID"), '<span style="font-weight:400;color:royalblue;">'+str(c.nid)+'</span>')
        self.addLine(u"ID колоды" if lang=="ru" else _("Deck ID"), '<span style="font-weight:400;color:cornflowerblue;">'+str(c.did)+'</span>')

        if c:
          self.addLine(
            "model queue type", 
            (_("Cloze") if c.model()['type'] == MODEL_CLOZE else _("Basic")) + 
            ' ' + ('<big style=font-style:italic;color:red;>' if c.queue  !=  c.type else '') +
            " " + ("<b style=color:red;>" if not c.queue in (-2, -1, 0, 1, 2, 3) else "") + str(c.queue) + ("</b>" if not c.queue in (-2, -1, 0, 1, 2, 3) else "") + 
            ' ' + ("<b style=color:red;>" if not c.type in (0, 1, 2) else "") + str(c.type) + ("</b>" if not c.type in (0, 1, 2) else "") +
            " " + ('</big>' if c.queue  !=  c.type else '') 
            )

        self.txt += "</table>"
        return self.txt

  glocal_i = False
  def glocal_addLine(self, k, v):
        global glocal_i
        self.txt += "<tr style='"+('background-color:#eee;' if glocal_i else '')+"'><td style='white-space:nowrap;padding:.1em .5em;'>%s</td><td style='padding:.25em .5em;'><b>%s</b></td></tr>" % (k, v)
        glocal_i = not glocal_i

  def glocal_timer(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

  def glocal_time(self, tm):
        str = ""
        if tm >= 60:
            str = fmtTimeSpan((tm/60)*60, short=True, point=-1, unit=1)
        str += " "
        if tm%60 != 0 or not str:
            str += fmtTimeSpan(round(tm%60,0), point=2 if not str else -1, short=True)
        return str

  if True:
    #CardStats.report = aleksejCardStatsReportForForecast
    CardStats.report = wrap( CardStats.report, aleksejCardStatsReportForForecast )
    CardStats.addLine = glocal_addLine
    CardStats.addRLine = addRLine
    CardStats.glocal_revlogDatum = glocal_revlogDatum
    CardStats.time = glocal_time
    CardStats.timer = glocal_timer

  class glocal_CardStats(object):
    def __init__(self, mw):
        self.mw = mw
        self.shown = False
        addHook("showQuestion", self._update)
        addHook("deckClosing", self.hide)
        addHook("reviewCleanup", self.hide)

    def _addDockable(self, title, w):
        class DockableWithClose(QDockWidget):
            def closeEvent(self, evt):
                self.emit(SIGNAL("closed"))
                QDockWidget.closeEvent(self, evt)
        dock = DockableWithClose(title, mw)
        dock.setObjectName(title)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetClosable)
        dock.setWidget(w)
        if mw.width() < 1000: # 1024x768 min
            mw.resize(QSize(1000, (740 if mw.height() < 740 else mw.height()) ))
        mw.addDockWidget(Qt.RightDockWidgetArea, dock)
        return dock

    def _remDockable(self, dock):
        mw.removeDockWidget(dock)

    def show(self):
        if not self.shown:
            class ThinAnkiWebView(AnkiWebView):
                def sizeHint(self):
                    return QSize(305, 305)
            self.web = ThinAnkiWebView()
            self.shown = self._addDockable(_("Card Info"), self.web)
            self.shown.connect(self.shown, SIGNAL("closed"),
                               self._onClosed)
        self._update()

    def hide(self):
        if self.shown:
            self._remDockable(self.shown)
            self.shown = None
            #actionself.mw.form.actionCstats.setChecked(False)

    def toggle(self):
        if self.shown:
            self.hide()
        else:
            self.show()

    def _onClosed(self):
        # schedule removal for after evt has finished
        self.mw.progress.timer(100, self.hide, False)

    def _update(self):
        if not self.shown:
            return
        txt = ""

        r = self.mw.reviewer
        d = self.mw.col
        if r.card:
            txt += "<h3>" + (u"Текущая карточка" if lang=="ru" else _("Current Card")) + \
                ("" if (B['B00_MORE_OVERVIEW_STATS'][0] == 1) else " &nbsp; " + mw.reviewer._remaining()) + "</h3><hr>"
            txt += d.cardStats(r.card)
        lc = r.lastCard()
        if lc:
            txt += "<h3>" + (u"Предыдущая карточка" if lang=="ru" else _("Last Card")) + "</h3>"
            txt += d.cardStats(lc)
        if not txt:
            txt = _("No current card or last card.")
        self.web.setHtml("""
<html><head>
</head><body><center>%s</center></body></html>
"""% txt)

  _cs = glocal_CardStats(mw)

  def cardStats(): #(on):
    _cs.toggle()

def glocal_revlogData(self, crd, cs):
    entries = self.mw.col.db.all(
        "select id/1000.0, ease, ivl, FACTOR, time/1000.0, type "
        "from revlog where cid = ?", crd.id)
    if not entries:
        return ""
    s = "<table width=100%%><tr><th align=left>%s</th>" % _("Date")
    s += ("<th align=right>%s</th>" * 5) % (
        _("Type"), _("Rating"), _("Interval"), _("Ease"), _("Time"))
    cnt = 0
    for (date, ease, ivl, FACTOR, taken, type) in reversed(entries):
        cnt += 1
        s += "<tr><td>%s</td>" % time.strftime(_("<b>%Y-%m-%d</b> @ %H:%M"),
                                               time.localtime(date))
        tstr = [_("Learn"), _("Review"), _("Relearn"), _("Filtered"),
                _("Resched")][type]
        import anki.stats as st
        fmt = "<span style='color:%s'>%s</span>"
        if type == 0:
            tstr = fmt % (st.colLearn, tstr)
        elif type == 1:
            tstr = fmt % (st.colMature, tstr)
        elif type == 2:
            tstr = fmt % (st.colRelearn, tstr)
        elif type == 3:
            tstr = fmt % (st.colCram, tstr)
        else:
            tstr = fmt % ("#000", tstr)
        if ease == 1:
            ease = fmt % (st.colRelearn, ease)
        if ivl == 0:
            ivl = _("0d")
        elif ivl > 0:
            ivl = fmtTimeSpan(ivl*86400, short=True)
        else:
            ivl = cs.time(-ivl)
        s += ("<td align=right>%s</td>" * 5) % (
            tstr,
            ease, ivl,
            "%d%%" % (FACTOR/10) if FACTOR else "",
            cs.time(taken)) + "</tr>"
    s += "</table>"
    if cnt < crd.reps:
        s += _("""\
Note: Some of the history is missing. For more information, \
please see the browser documentation.""")
    return s + "<hr>"

def showTextik(txt, parent=None, type="text", run=True, geomKey=None, minW=555,minH=666,title=""):
    if not parent:
        parent = aqt.mw.app.activeWindow() or aqt.mw
    diag = QDialog(parent)
    diag.setWindowTitle("Anki "+title)
    layout = QVBoxLayout(diag)
    diag.setLayout(layout)
    text = QTextEdit()
    text.setReadOnly(True)
    if type == "text":
        text.setPlainText(txt)
    else:
        text.setHtml(txt)
    layout.addWidget(text)
    box = QDialogButtonBox(QDialogButtonBox.Close)
    layout.addWidget(box)
    def onReject():
        if geomKey:
            saveGeom(diag, geomKey)
        QDialog.reject(diag)
    diag.connect(box, SIGNAL("rejected()"), onReject)
    diag.setMinimumWidth(minW) # !!!
    diag.setMinimumHeight(minH) # !!!
    if geomKey:
        restoreGeom(diag, geomKey)
    if run:
        diag.exec_()
    else:
        return diag, box

######################
#
if mw_addon_view_menu_exists:
    mw.addon_view_menu.addSeparator()
if mw_addon_cards_menu_exists:
    mw.addon_cards_menu.addSeparator()

def showBodyClasses(): 
    return "<div style='white-space: pre-wrap;'>" + mw.reviewer.web.page().mainFrame().evaluateJavaScript("""
        (function(){ 
          var ret = document.documentElement.classList.toString().trim();
           ret = "/* html */<br>." + ret.replace(/(\s+)/g,' {  } <br>.') + " {  } <br>";
          var retv = document.body.classList.toString().trim();
           retv = "/* body */<br>." + retv.replace(/(\s+)/g,' {  } <br>.') + " {  } <br>";
          return ret + retv; 
         }())
     """) + "</div>"

def onStats():
    if not mw.reviewer.card:
        return
    cs = CardStats(mw.col, mw.reviewer.card)
    retv = cs.report()
    retw = glocal_revlogData(mw.reviewer, mw.reviewer.card, cs)

    lc = mw.reviewer.lastCard()
    if lc:
        lcs = CardStats(mw.col, mw.reviewer.lastCard())
        retx = lcs.report()
        rety = glocal_revlogData(mw.reviewer, mw.reviewer.lastCard(), lcs)
    else:
        lcs = retx = rety = ""

    # -- выбрасывает showText со стандартным заголовком 
    #    Проверьте базу данных, не помогло - скопируйте на форум
    #sys.stderr.write("...\n")

    showTextik( '' +
        'audio_speed = %1.1f<br>\n'%audio_speed +
        'Replay Q <b>'+ unicode(soundtrack_q_number)+ '</b> '+ unicode(len(soundtrack_q_list))+ ' '+ unicode(soundtrack_q_list) + '<br>\n' +
        'Replay A <b>'+ unicode(soundtrack_a_number)+ '</b> '+ unicode(len(soundtrack_a_list))+ ' '+ unicode(soundtrack_a_list) + '<br>\n<br>' +
        "deck_browser_standard_zoom = <b>"+str(deck_browser_current_zoom)+"</b><br>\n"+\
        "overview_standard_zoom = <b>"+str(overview_current_zoom)+"</b><br>\n"+\
        "reviewer_standard_zoom = <b>"+str(reviewer_current_zoom)+"</b>\n"+
        "<h3>" + (u"Текущая карточка" if lang=="ru" else _("Current Card")) + \
        ("" if (B['B00_MORE_OVERVIEW_STATS'][0] == 1) else " &nbsp; " + mw.reviewer._remaining()) + "</h3><hr>" +
        showBodyClasses()+"<hr>"+ 
        retv+"<hr>"+retw+
        ("<h3>" + (u"Предыдущая карточка" if lang=="ru" else _("Last Card")) + "</h3><hr>" +
        retx+"<hr>" if lc else "")+
        rety+"<p>&nbsp;",type="html")

def qViewSource():
    if not mw.reviewer.card:
        return
    c = mw.reviewer.card
    showTextik( _('Question') + ':\n----------\n' + c.q(),type="text",title="HTML+CSS insertion into Body " + _("Question") +" c.q() ",minW=666)

def aViewSource():
    if not mw.reviewer.card:
        return
    c = mw.reviewer.card
    showTextik( _('Answer')   + ':\n----------\n' + c.a(),type="text",title="HTML+CSS insertion into Body " + _("Answer") +" c.a() ",minW=666) 

def cssViewSource():
    if not mw.reviewer.card:
        return
    c = mw.reviewer.card
    showTextik( _('CSS')   + ':\n----------\n' + c.css(),type="text",title="CSS+ insertion into Body " + _("Styling (shared between cards)") +" c.css() ",minW=666) 

def q_ViewSource():
    if not mw.reviewer.card:
        return
    c = mw.reviewer.card
    q = c.q()
    showTextik( _('Question') + ':\n----------\n\n' + c._getQA()['q'],type="text",title="HTML insertion into Body " + _("Question") +" c._getQA()['q'] ",minW=666) # c._getQA()['q']

def a_ViewSource():
    if not mw.reviewer.card:
        return
    c = mw.reviewer.card
    a = c.a()
    showTextik( _('Answer')   + ':\n----------\n\n' + c._getQA()['a'],type="text",title="HTML insertion into Body " + _("Answer") +" c._getQA()['a'] ",minW=666) # c._getQA()['a']

def css_ViewSource(self):
    if not self.mw.reviewer.card:
        return
    c = self.mw.reviewer.card
    showTextik( _('CSS')   + ':\n----------\n\n' + c.model()['css'],type="text",title="CSS insertion into Body " + _("Styling (shared between cards)") +" c.model()['css'] ",minW=666) 

if A['F3_CARD_HISTORY'][0]:
    F3_CARD_HISTORY_action = QAction(mw)
    F3_CARD_HISTORY_action.setText(u"&История карточки" if lang=="ru" else "Card &Revlog")
    F3_CARD_HISTORY_action.setShortcut(HOTKEY['F3_history'][0])
    if A['ANKI_MENU_ICONS'][0]:
        F3_CARD_HISTORY_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'view.png')))
    mw.connect(F3_CARD_HISTORY_action, SIGNAL("triggered()"), onStats)
    if mw_addon_cards_menu_exists:
        mw.addon_cards_menu.addAction(F3_CARD_HISTORY_action)
        if not A['F3_CARD_INFO_DURING_REVIEW'][0]:
            mw.addon_cards_menu.addSeparator()

if A['F3_CARD_INFO_DURING_REVIEW'][0]:
    F3_CARD_INFO_DURING_REVIEW_action = QAction(mw)
    F3_CARD_INFO_DURING_REVIEW_action.setText("Основные &Показатели Карточек" if lang == 'ru' else "Card &Stats")
    if A['ANKI_MENU_ICONS'][0]:
        F3_CARD_INFO_DURING_REVIEW_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'sidebar.png')))
    F3_CARD_INFO_DURING_REVIEW_action.setShortcut(QKeySequence(HOTKEY['F3_card_stats'][0]))
    mw.connect(F3_CARD_INFO_DURING_REVIEW_action, SIGNAL("triggered()"), cardStats)
    if mw_addon_cards_menu_exists:
        mw.addon_cards_menu.addAction(F3_CARD_INFO_DURING_REVIEW_action)
        mw.addon_cards_menu.addSeparator()

def _getSourceHTML():
    """To look at sourcne HTML+CSS code."""
    html = mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.documentElement.outerHTML
         }())
    """)
    showTextik(html,minW=999,title="HTML5+CSS3+JavaScript + jQuery 1.5 Source Code")

def _getSourceBody():
    """To look at sourcne HTML+CSS code."""
    html = '<html class="' +\
        unicode(mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.documentElement.className
         }())
    """)) + '">\n<head>\n' +\
        unicode(mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.getElementsByTagName('head')[0].getElementsByTagName('style')[0].outerHTML
         }())
    """)) + "\n</head>\n" +\
        unicode(mw.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             return document.body.outerHTML
         }())
    """)) + "\n</html>\n"
    showTextik(html,minW=999,title="HTML5+CSS3+JavaScript + jQuery 1.5 Source Code")

menu_titles = []

def _getA():
    """To look at A list."""
    html = "<html><head><style>"
    html += "h1 { color: dodgerblue; }"
    html += "table { border: solid 1px gray; }"
    html += "td { padding:5px 15px; }"
    html += "</style></head><body><table align=center><tbody><tr><td>"

    def _nextA(AZ,ttl,color):
        html = ''
        html += "<h1 align=center>"+ttl+"</h1><p>&nbsp;"
        html += "<table cellspacing=0 align=center><tbody>"
        i = False
        #for key, value in AZ.iteritems():
        keylist = AZ.keys()
        keylist.sort()
        for key in keylist:
          value = AZ[key]
          if key:
            html += "<tr style='"+('background-color:#eee;' if i else '')+"'>"
            if value[0] != value[1] and value[0] != value[2]:
                html += "<td style='color:"+color+";'><b>"+key+"</b></td><td><b style=color:red;><big>"+str(value[0])+"</big></b></td>"
            elif value[0] != value[1]:
                html += "<td style='color:"+color+";'><b>"+key+"</b></td><td><b><big>"+str(value[0])+"</big></b></td>"
            else:
                html += "<td style='color:"+color+";'>"+key+"</td><td>"+str(value[0])+"</td>"
            html += "</tr>"
          i = not i
        html += "</tbody></table>"
        return html

    def _nextK(AZ,ttl,color):
        html = ''
        html += "<h1 align=center>"+ttl+"</h1><p>&nbsp;"
        html += "<table cellspacing=0 align=center><tbody>"
        i = False
        #for key, value in AZ.iteritems():
        keylist = AZ.keys()
        def sortBy(inputStr):
            return AZ[inputStr][2]+" "+inputStr
        keylist.sort(key=sortBy)
        for key in keylist:
          value = AZ[key]
          if key:
            html += "<tr style='"+('background-color:#eee;' if i else '')+"'>"
            html += "<td>"+key+"</td><td style='color:"+color+";'>"+str(value[0])+"</td>"
            html += "<td style=color:#369;white-space:nowrap;>"+value[1]+"</td>"
            html += "<td style=color:gray;white-space:nowrap;>"+value[2]+"</td>"
            html += "</tr>"
          i = not i
        html += "</tbody></table><p>&nbsp;"
        return html

    def _nextZ(AZ,ttl,color):
        html = ''
        html += "<h1 align=center>"+ttl+"</h1><p>&nbsp;"
        html += "<table cellspacing=0 align=center><tbody>"
        i = False
        for value in AZ:
            html += "<tr style='"+('background-color:#eee;' if i else '')+"'>"
            html += "<td style='color:"+color+";'><BIG>"+str(value)+"</BIG></td>"
            html += "</tr>"
            i = not i
        html += "</tbody></table><p>&nbsp;"
        return html

    html += '' + \
    _nextK(HOTKEY,"HOTKEY list","darkviolet") + \
    _nextK(HOTKEYS,"HOTKEYS list","green") + \
    _nextK(HOTKEYZ,"HOTKEYZ list","darkred") + '</td><td>' + \
    _nextZ(menu_titles,"addons list","purple") + \
    _nextA(A,"A list","OliveDrab ") + \
    _nextA(B,"B list","Olive ") + \
    "</tr></tbody></table><p>&nbsp;"

    #html += "<p><code>"+unicode( sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()]) )+"</code>"

    html += "<p>&nbsp;</body></html>"
    showTextik(html,minW=888,title="A list",type="HTML")

if A['F3_VIEW_SOURCE'][0]:

    if A['F3_HTML_SOURCE'][0]:

        get_Body_Source_action = QAction(mw)
        get_Body_Source_action.setText("Показать Ис&ходник HTML Body" if lang == 'ru' else "View Source code &Body")
        if A['ANKI_MENU_ICONS'][0]:
            get_Body_Source_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'xhtml.png')))
        get_Body_Source_action.setShortcut(QKeySequence(HOTKEY['F3_Body_source'][0]))
        mw.connect(get_Body_Source_action, SIGNAL("triggered()"), _getSourceBody)

        get_HTML_Source_action = QAction(mw)
        get_HTML_Source_action.setText("Показать И&сходник HTML" if lang == 'ru' else "&View Source code")
        if A['ANKI_MENU_ICONS'][0]:
            get_HTML_Source_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'html.png')))
        get_HTML_Source_action.setShortcut(QKeySequence(HOTKEY['F3_HTML_source'][0]))
        mw.connect(get_HTML_Source_action, SIGNAL("triggered()"), _getSourceHTML)

        if hasattr(mw,'addon_cards_menu'):
            mw.addon_cards_menu.addAction(get_Body_Source_action)
            mw.addon_cards_menu.addAction(get_HTML_Source_action)

    mw.debug_submenu = QMenu('О&тладка' if lang == 'ru' else "&"+_(u"Debug"), mw)
    if A['ANKI_MENU_ICONS'][0]:
        mw.debug_submenu.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'source.png')))

    debug_console_action = QAction(mw)
    debug_console_action.setText( "Python REPL &" + _("Debug Console") ) # Read-Eval-Print Loop
    if A['ANKI_MENU_ICONS'][0]:
        debug_console_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'terminal.png')))
    debug_console_action.setShortcut(QKeySequence("Ctrl+Shift+:"))
    mw.connect(debug_console_action, SIGNAL("triggered()"), mw.onDebug)

    View_Question_action = QAction(mw)
    View_Question_action.setText( "HTML+CSS Body &" + _("Question") )
    View_Question_action.setShortcut(QKeySequence("Alt+Shift+F3"))
    mw.connect(View_Question_action, SIGNAL("triggered()"), qViewSource)

    View_Answer_action = QAction(mw)
    View_Answer_action.setText( "HTML+CSS Body &" + _("Answer") )
    View_Answer_action.setShortcut(QKeySequence("Ctrl+Shift+F3")) # Ctrl+Alt+F3 does not work
    mw.connect(View_Answer_action, SIGNAL("triggered()"), aViewSource)

    View_Ans_action = QAction(mw)
    View_Ans_action.setText( "CSS &" + _("Card") )
    View_Ans_action.setShortcut(QKeySequence("Ctrl+Alt+Shift+F3")) 
    mw.connect(View_Ans_action, SIGNAL("triggered()"), cssViewSource)

    View_Quest_action = QAction(mw)
    View_Quest_action.setText( "HTML Body &" + _("Question") )
    View_Quest_action.setShortcut(QKeySequence("Alt+Shift+F4"))
    mw.connect(View_Quest_action, SIGNAL("triggered()"), q_ViewSource)

    View_Answ_action = QAction(mw)
    View_Answ_action.setText( "HTML Body &" + _("Answer") )
    View_Answ_action.setShortcut(QKeySequence("Ctrl+Shift+F4")) 
    mw.connect(View_Answ_action, SIGNAL("triggered()"), a_ViewSource)

    View_Answr_action = QAction(mw)
    View_Answr_action.setText( "CSS only &" + _("Card") )
    View_Answr_action.setShortcut(QKeySequence("Ctrl+Alt+Shift+F4")) 
    mw.connect(View_Answr_action, SIGNAL("triggered()"), lambda: css_ViewSource(mw.reviewer))

    if mw_addon_cards_menu_exists:
        mw.addon_cards_menu.addMenu(mw.debug_submenu)

        mw.debug_submenu.addAction(debug_console_action)
        mw.debug_submenu.addSeparator()
        mw.debug_submenu.addAction(View_Question_action)
        mw.debug_submenu.addAction(View_Answer_action)
        mw.debug_submenu.addAction(View_Ans_action)
        mw.debug_submenu.addSeparator()
        mw.debug_submenu.addAction(View_Quest_action)
        mw.debug_submenu.addAction(View_Answ_action)
        mw.debug_submenu.addAction(View_Answr_action)
        mw.debug_submenu.addSeparator()

##############################

if True: #B['B00_MORE_OVERVIEW_STATS'][0]: #CHECKERS:

    def on_musthave_study():
        global A, B
        B['B05_STUDY_BUTTON'][0] = musthave_study_action.isChecked()
        if mw.state == "deckBrowser":
            mw.moveToState("deckBrowser")

    def on_gear_at_end_of_line():
        global A, B
        B['B03_GEAR_AT_END_OF_LINE'][0] = gear_at_end_of_line_action.isChecked()
        if mw.state == "deckBrowser":
            mw.moveToState("deckBrowser")

    def on_hide_big_numbers():
        global A, B
        B['B04_HIDE_BIG_NUMBERS'][0] = hide_big_numbers_action.isChecked()
        if mw.state == "deckBrowser":
            mw.moveToState("deckBrowser")
        if mw.state == "overview":
            mw.moveToState("overview")

    def Unseen_and_buried_counts():
        global A, B
        if  B['B00_MORE_OVERVIEW_STATS'][0] == 0:
            return

        if  B['B00_MORE_OVERVIEW_STATS'][0] == 3:
            B['B00_MORE_OVERVIEW_STATS'][0] = 2
        else:
            B['B00_MORE_OVERVIEW_STATS'][0] = 3

        musthave_setup_menu(3)
        overview_init()
        initDeckBro()

        if mw.state == "deckBrowser":
            mw.moveToState("deckBrowser")
        if mw.state == "overview":
            mw.moveToState("overview")

    def on_checkers():
        global A, B 
        if checkers_action.isChecked():
          #if new_and_due_action.isChecked():
          #  if unseen_and_suspended_action.isChecked():
          #      B['B00_MORE_OVERVIEW_STATS'][0] = 3
          #  else:
          #      B['B00_MORE_OVERVIEW_STATS'][0] = 2
          #else:
          #  B['B00_MORE_OVERVIEW_STATS'][0] = 1
          B['B00_MORE_OVERVIEW_STATS'][0] = 3
        else:
            B['B00_MORE_OVERVIEW_STATS'][0] = 0

        musthave_setup_menu(4)
        overview_init()
        initDeckBro()

        if mw.state == "deckBrowser":
            mw.moveToState("deckBrowser")
        if mw.state == "overview":
            mw.moveToState("overview")

    def new_and_due_counts():
        global A, B 
        if  B['B00_MORE_OVERVIEW_STATS'][0] == 0:
            return

        if  B['B00_MORE_OVERVIEW_STATS'][0] > 1:
            B['B00_MORE_OVERVIEW_STATS'][0] = 1
        else:
            if unseen_and_suspended_action.isChecked():
                B['B00_MORE_OVERVIEW_STATS'][0] = 3
            else:
                B['B00_MORE_OVERVIEW_STATS'][0] = 2

        musthave_setup_menu(5)
        overview_init()
        initDeckBro()

        if mw.state == "deckBrowser":
            mw.moveToState("deckBrowser")
        if mw.state == "overview":
            mw.moveToState("overview")

    def show_them_all():
        global F9_HINT_PEEKED
        color_buttons()
        if mw.state == 'review':
            if mw.reviewer.state == 'question':
               anki.sound.stopMplayer()
               F9_HINT_PEEKED = False
               mw.reviewer._initWeb() # _showQuestion()
            if mw.reviewer.state == 'answer':
               anki.sound.stopMplayer()
               mw.reviewer._showAnswer()

    def on_color_buttons():
        global A, B
        B['B07_COLOR_BUTTONS'][0] = color_buttons_action.isChecked()
        show_them_all()

    def on_big_buttons():
        global A, B, F9_HINT_PEEKED
        B['B08_BIG_BUTTONS'][0] = big_buttons_action.isChecked()
        if mw.state == 'review':
            if mw.reviewer.state == 'question':
               anki.sound.stopMplayer()
               F9_HINT_PEEKED = False
               mw.reviewer._initWeb() # _showQuestion()
            if mw.reviewer.state == 'answer':
               anki.sound.stopMplayer()
               mw.reviewer._showAnswer()

    def on_just_smiles():
        global BUTTON_LABELS, F9_HINT_PEEKED
        if just_smiles_action.isChecked():
            BUTTON_LABELS = BUTTON_LABELS_SMILES
        else:
            BUTTON_LABELS = BUTTON_LABELS_LANG
        color_buttons()
        if mw.state == "review":
            if mw.reviewer.state == 'question':
               anki.sound.stopMplayer()
               F9_HINT_PEEKED = False
               mw.reviewer._initWeb() # _showQuestion()
            if mw.reviewer.state == "answer":
               anki.sound.stopMplayer()
               mw.reviewer._showAnswer()

    def myAnswerButtons(self,_old):
      global A, B
      if B['B06_WIDE_BUTTONS'][0]:
        times = []
        default = self._defaultEase()
        def but(i, label, beam):
            if i == default:
                extra = "id=defease"
            else:
                extra = ""
            due = self._buttonTime(i)
            return '''
    <td align=center style="width:%s;">%s<button %s %s onclick='py.link("ease%d");'>\
    %s</button></td>''' % (beam, due, extra, \
            ((" title=' "+(_("Shortcut key: %s") % i)+" '") if B['B11_BUTTON_TITLES'][0] else ""), i, label)
        buf = "<table cellpading=0 cellspacing=0 width=100%%><tr>"
        for ease, lbl, beams in answerButtonList(self):
            buf += but(ease, lbl, beams)
        buf += "</tr></table>"
        script = """
        <style>table tr td button { width: 100%; } </style>
    <script>$(function () { $("#defease").focus(); });</script>"""
        return buf + script
      else:
        return _old(self)

    """
    # Bigger Show Answer Button
    For people who do their reps with a mouse. 
    Makes the show answer button wide enough to cover all 4 of the review buttons. 
    """

    def myShowAnswerButton(self,_old):
      global A, B
      if B['B06_WIDE_BUTTONS'][0]:
        self._bottomReady = True
        if not self.typeCorrect:
            self.bottom.web.setFocus()
        middle = '''
    <span class=stattxt>%s</span><br>
    <button %s id=ansbut style="display:inline-block;width:%s;%s" onclick='py.link(\"ans\");'>%s</button>
        </script>
    ''' % (
        self._remaining(), \
            ((" title=' "+(_("Shortcut key: %s") % _("Space"))+" '") if B['B11_BUTTON_TITLES'][0] else ""),
            BEAMS4, "font-size:x-large;color:"+dflt if B['B08_BIG_BUTTONS'][0] else "", _("Show Answer"))
        # place it in a table so it has the same top margin as the ease buttons
        #middle = "<table cellpadding=0><tr><td class=stat2 align=center>%s</td></tr></table>" % middle
        middle = "<div class=stat2 align=center style='width:%s!important;'>%s</div>" % (BEAMS4, middle)
        if self.card.shouldShowTimer():
            maxTime = self.card.timeLimit() / 1000
        else:
            maxTime = 0
        self.bottom.web.eval("showQuestion(%s,%d);" % (
            json.dumps(middle), maxTime))
        return True
      else:
        return _old(self)

    def wide_buttons_init():
        if B['B06_WIDE_BUTTONS'][0]:
           if A['COLORFUL_TOOLBAR'][0]:
               color_buttons_action.setEnabled(True)
               big_buttons_action.setEnabled(True)
               just_smiles_action.setEnabled(True)
        else:
           if A['COLORFUL_TOOLBAR'][0]:
               color_buttons_action.setEnabled(False)
               big_buttons_action.setEnabled(False)
               just_smiles_action.setEnabled(False)

    def on_wide_buttons():
        global A, B
        B['B06_WIDE_BUTTONS'][0] = wide_buttons_action.isChecked()
        wide_buttons_init()
        show_them_all()

    def refresh_reviewer():
      global F9_HINT_PEEKED
      if mw.state == 'review':
        if mw.reviewer.state == 'question':
           anki.sound.stopMplayer()
           F9_HINT_PEEKED = False
           mw.reviewer._initWeb() # _showQuestion()
        if mw.reviewer.state == 'answer':
           anki.sound.stopMplayer()
           mw.reviewer._showAnswer()

    def on_Answer_Confirmation():
        global A, B
        if A['KEYS_HANDLER'][0]:
            B['B10_ANSWER_CONFIRMATION'][0] = 2 if answer_confirmation_action.isChecked() else 0
        refresh_reviewer()

    def on_Titles():
        global A, B
        B['B11_BUTTON_TITLES'][0] = titles_action.isChecked()
        refresh_reviewer()

    def on_hard7():
        global A, B
        B['B12_HARD7'][0] = hard7_action.isChecked()
        refresh_reviewer()

    mw.musthave_submenu = QMenu('&Настройки панели колод и кнопок ответа' if lang == 'ru' else _(u"Decks and Answers &Options"), mw)
    if A['ANKI_MENU_ICONS'][0]:
        mw.musthave_submenu.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'Right_Arrow.png')))

    unseen_and_suspended_action = QAction('&Невиданные, исключённые и отложенные' if lang == 'ru' else _('&Unseen, suspended and buried'), mw)
    mw.connect(unseen_and_suspended_action, SIGNAL("triggered()"), Unseen_and_buried_counts)
    unseen_and_suspended_action.setCheckable(True)

    gear_at_end_of_line_action = QAction('&Шестерёнка в конце строки' if lang == 'ru' else _('&Gear at the end of line'), mw)
    mw.connect(gear_at_end_of_line_action, SIGNAL("triggered()"), on_gear_at_end_of_line)
    gear_at_end_of_line_action.setCheckable(True)

    musthave_study_action = QAction('&Кнопка Учить колоду' if lang == 'ru' else _('&Study Deck Button'), mw)
    mw.connect(musthave_study_action, SIGNAL("triggered()"), on_musthave_study)
    musthave_study_action.setCheckable(True)

    hide_big_numbers_action = QAction( ('&Спрятать числа больше %d' % (B['B04_HIDE_BIG_NUMBER'][0]) ) if lang == 'ru' else _('&Hide big numbers')+(' ( > %s )' % (B['B04_HIDE_BIG_NUMBER'][0]) ), mw)
    mw.connect(hide_big_numbers_action, SIGNAL("triggered()"), on_hide_big_numbers)
    hide_big_numbers_action.setCheckable(True)

    checkers_action = QAction("Настроить панель колод и показатели колоды" if lang=="ru" else "Setup Decks panel and Overview deck", mw)
    mw.connect(checkers_action, SIGNAL("triggered()"), on_checkers)
    checkers_action.setCheckable(True)

    new_and_due_action = QAction("%s, %s, %s, %s"%(_('New'),_('Learn'),_('To Review'),_('Due')), mw)
    mw.connect(new_and_due_action, SIGNAL("triggered()"), new_and_due_counts)
    new_and_due_action.setCheckable(True)

    if mw_addon_view_menu_exists:
        mw.addon_view_menu.addSeparator()
        mw.addon_view_menu.addMenu(mw.musthave_submenu)
        mw.musthave_submenu.addAction(checkers_action)
        mw.musthave_submenu.addSeparator()
        mw.musthave_submenu.addAction(new_and_due_action)
        mw.musthave_submenu.addAction(unseen_and_suspended_action)
        mw.musthave_submenu.addAction(gear_at_end_of_line_action)
        mw.musthave_submenu.addAction(hide_big_numbers_action)
        mw.musthave_submenu.addSeparator()
        mw.musthave_submenu.addAction(musthave_study_action)
        mw.musthave_submenu.addSeparator()

    #CHK_07_COLOR_BUTTONS
    color_buttons_action = QAction('&Цветные кнопки оценки' if lang == 'ru' else _('&Color Answer Buttons'), mw)
    mw.connect(color_buttons_action, SIGNAL("triggered()"), on_color_buttons)
    color_buttons_action.setCheckable(True)

    #CHK_08_BIG_BUTTONS
    big_buttons_action = QAction('&Большие буквы на кнопках' if lang == 'ru' else _('&Big Letters on Buttons'), mw)
    mw.connect(big_buttons_action, SIGNAL("triggered()"), on_big_buttons)
    big_buttons_action.setCheckable(True)

    #JUST_SMILES
    just_smiles_action = QAction('&Смайлы по асе' if lang == 'ru' else _('&Just smiles'), mw)
    mw.connect(just_smiles_action, SIGNAL("triggered()"), on_just_smiles)
    just_smiles_action.setCheckable(True)

    # -- Now it's a history. --
    #CHK_06_WIDE_BUTTONS_answerButtons = Reviewer._answerButtons
    #CHK_06_WIDE_BUTTONS_showAnswerButton = Reviewer._showAnswerButton
    #if CHK_06_WIDE_BUTTONS:
       #Reviewer._answerButtons = myAnswerButtons
       #Reviewer._showAnswerButton = myShowAnswerButton
    Reviewer._answerButtons = wrap(Reviewer._answerButtons, myAnswerButtons, "around")
    Reviewer._showAnswerButton = wrap(Reviewer._showAnswerButton, myShowAnswerButton, "around")

    #CHK_06_WIDE_BUTTONS
    wide_buttons_action = QAction('&Широкие кнопки оценки ответа' if lang == 'ru' else _('&Wide Answer Buttons'), mw)
    mw.connect(wide_buttons_action, SIGNAL("triggered()"), on_wide_buttons)
    wide_buttons_action.setCheckable(True)

    if not B['B06_WIDE_BUTTONS'][0] and A['COLORFUL_TOOLBAR'][0]:
       color_buttons_action.setEnabled(False)
       big_buttons_action.setEnabled(False)
       just_smiles_action.setEnabled(False)

    # ANSWER_CONFIRMATION
    answer_confirmation_action = QAction('&Всплывающая подсказка при ответе с клавиатуры' if lang == 'ru' else _('&Answer_Confirmation'), mw)
    mw.connect(answer_confirmation_action, SIGNAL("triggered()"), on_Answer_Confirmation)
    answer_confirmation_action.setCheckable(True)

    # BUTTON_TITLES
    titles_action = QAction('&Всплывающие подсказки над кнопками ответа' if lang == 'ru' else _('&Reply buttons hotkey tooltips '), mw)
    mw.connect(titles_action, SIGNAL("triggered()"), on_Titles)
    titles_action.setCheckable(True)

    # HARD7
    hard7_action = QAction('&Чаще отвечать Трудно, чем Снова Не знаю' if lang == 'ru' else _('&Often Reply Hard than Again'), mw)
    mw.connect(hard7_action, SIGNAL("triggered()"), on_hard7)
    hard7_action.setCheckable(True)

    # EDIT_MORE
    edit_more_action = QAction('Кнопки &Редактирование Ещё' if lang == 'ru' else _('&Edit More Buttons'), mw)
    mw.connect(edit_more_action, SIGNAL("triggered()"), onEditMore)
    edit_more_action.setCheckable(True)
    edit_more_action.setChecked(B['B13_EDIT_MORE'][0])

    if mw_addon_view_menu_exists:
        mw.musthave_submenu.addAction(wide_buttons_action)
        mw.musthave_submenu.addAction(color_buttons_action)
        mw.musthave_submenu.addAction(big_buttons_action)
        mw.musthave_submenu.addAction(just_smiles_action)
        mw.musthave_submenu.addSeparator()
        mw.musthave_submenu.addAction(answer_confirmation_action)
        mw.musthave_submenu.addAction(titles_action)
        mw.musthave_submenu.addAction(hard7_action)
        mw.musthave_submenu.addAction(edit_more_action)

    def musthave_setup_menu(num):

        checkers_action.setChecked(B['B00_MORE_OVERVIEW_STATS'][0] > 0)

        unseen_and_suspended_action.setChecked(B['B00_MORE_OVERVIEW_STATS'][0] > 2)
        unseen_and_suspended_action.setEnabled(B['B00_MORE_OVERVIEW_STATS'][0] > 1)

        musthave_study_action.setChecked(B['B05_STUDY_BUTTON'][0])
        musthave_study_action.setEnabled(B['B00_MORE_OVERVIEW_STATS'][0] > 0)

        hide_big_numbers_action.setChecked(B['B04_HIDE_BIG_NUMBERS'][0])
        hide_big_numbers_action.setEnabled(B['B00_MORE_OVERVIEW_STATS'][0] > 1)

        new_and_due_action.setChecked(B['B00_MORE_OVERVIEW_STATS'][0] > 1)
        new_and_due_action.setEnabled(B['B00_MORE_OVERVIEW_STATS'][0] > 0)

        gear_at_end_of_line_action.setChecked(B['B03_GEAR_AT_END_OF_LINE'][0])
        gear_at_end_of_line_action.setEnabled(B['B00_MORE_OVERVIEW_STATS'][0] > 2)

        color_buttons_action.setChecked(B['B07_COLOR_BUTTONS'][0])
        big_buttons_action.setChecked(B['B08_BIG_BUTTONS'][0])
        color_buttons()

        wide_buttons_action.setChecked(B['B06_WIDE_BUTTONS'][0])
        wide_buttons_init()

        just_smiles_action.setChecked(BUTTON_LABELS_SMILES == BUTTON_LABELS)

        answer_confirmation_action.setChecked(B['B10_ANSWER_CONFIRMATION'][0]>0)
        titles_action.setChecked(B['B11_BUTTON_TITLES'][0])
        hard7_action.setChecked(B['B12_HARD7'][0])
        edit_more_action.setChecked(B['B13_EDIT_MORE'][0])

    musthave_setup_menu(1)

if A['COLORFUL_TOOLBAR'][0]:

    def toggle_text_tool_bar():
        #"""Switch the original toolbar on or off."""
        if show_text_tool_bar_action.isChecked():
            mw.toolbar.web.show()
        else:
            mw.toolbar.web.hide()

    def toggle_qt_tool_bar():
        #"""Switch the new upper tool bar on or off."""
        if show_qt_tool_bar_action.isChecked():
            mw.qt_tool_bar.show()
        else:
            mw.qt_tool_bar.hide()

    def toggle_more_tool_bar():
        #"""Switch the new lower tool bar on or off."""
        # No real need to check if we are in review. Only then should we
        # be able to activate the action.
        if show_more_tool_bar_action.isChecked():
            mw.reviewer.more_tool_bar.show()
        else:
            mw.reviewer.more_tool_bar.hide()

    ## Actions to show and hide the different tool bars.
    show_text_tool_bar_action = QAction(mw)
    show_text_tool_bar_action.setText(u"Показать Колоды Добавить Обзор" if lang=="ru" else _(u"Show text tool bar"))
    show_text_tool_bar_action.setCheckable(True)
    mw.connect(show_text_tool_bar_action, SIGNAL("triggered()"),
               toggle_text_tool_bar)

    show_qt_tool_bar_action = QAction(mw)
    show_qt_tool_bar_action.setText(u"Показать панель переходов" if lang=="ru" else _(u"Show icon bar"))
    show_qt_tool_bar_action.setCheckable(True)
    show_qt_tool_bar_action.setChecked(True)
    mw.connect(show_qt_tool_bar_action, SIGNAL("triggered()"), 
               toggle_qt_tool_bar)

    show_more_tool_bar_action = QAction(mw)
    show_more_tool_bar_action.setText(u"Показать панель редактирования" if lang=="ru" else _(u"Show more tool bar"))
    show_more_tool_bar_action.setCheckable(True)
    show_more_tool_bar_action.setChecked(True)
    show_more_tool_bar_action.setEnabled(False)
    mw.connect(show_more_tool_bar_action, SIGNAL("triggered()"),
               toggle_more_tool_bar)

    if mw_addon_view_menu_exists:
        mw.addon_view_menu.addAction(show_qt_tool_bar_action)
        mw.addon_view_menu.addAction(show_text_tool_bar_action)
        mw.addon_view_menu.addAction(show_more_tool_bar_action)
        mw.addon_view_menu.addSeparator()

# -------------------------------------------------------------------
Keys = {}

Keys['Undo'] = [Qt.Key_Period, Qt.Key_Z, Qt.Key_Comma] # Undo - NumPad dot = period in English and comma in Russian
Keys['R'] = [Qt.Key_R] # Replay Audio
#KeysV = [Qt.Key_V] # Record Voice
#KeysG = [Qt.Key_G] # Replay Voice
#KeysO = [Qt.Key_O] # Options
Keys['A'] = [Qt.Key_A] # Add
Keys['B'] = [Qt.Key_B] # Browse
Keys['D'] = [Qt.Key_D] # Deck
Keys['Y'] = [Qt.Key_Y] # Sync
Keys['Plus'] = [Qt.Key_Plus] # Replay Next Audio

Keys['0'] = []
if A['ZERO_KEY_TO_SHOW_ANSWER'][0]:
   Keys['0'] = [Qt.Key_0] # Show Answer

Keys['1'] = [Qt.Key_1]
Keys['2'] = [Qt.Key_2]
Keys['3'] = [Qt.Key_3]
Keys['4'] = [Qt.Key_4]
Keys['5'] = [] # hint
Keys['Aster'] = [Qt.Key_Asterisk] # marked

if A['RIGHT_HAND_JKL_ANSWER_KEYS_SHORTCUTS'][0]: 
    Keys['1'].append(Qt.Key_J) # again
    Keys['2'].append(Qt.Key_K) # hard
    Keys['3'].append(Qt.Key_L) # good
    Keys['4'].append(Qt.Key_Semicolon) # easy
    if A['F9_HINT_PEEKING'][0] and A['F9_HINT_PEEKING_H'][0]:
        Keys['5'].append(Qt.Key_H) # hint
    Keys['Aster'].append(Qt.Key_Apostrophe) # marked

Keys8 = []
if A['NUMERIC_KEYPAD_REMAPPING'][0]:
    if B['B12_HARD7'][0]: 
      Keys['2'].append(Qt.Key_7)
    else:
      Keys['1'].append(Qt.Key_7)
    Keys8.append(Qt.Key_8)
    if A['F9_HINT_PEEKING'][0] and A['F9_HINT_PEEKING_5'][0]:
        Keys['5'].append(Qt.Key_5) # hint
    Keys['3'].append(Qt.Key_9)
    Keys['R'].append(Qt.Key_6)

'''
if lang == 'ru':
    # Russian Edition
    Text1 = [ u'о', u'О' ] # again
    Text2 = [ u'л', u'Л' ] # hard
    Text3 = [ u'д', u'Д' ] # good
    Text4 = [ u'ж', u'Ж' ] # easy
    Text5 = [ u'р', u'Р' ] # hint
    TextUndo = [ u'я', u'Я' ] # Undo
    # End of Russian Edition
else:
    Text1 = []
    Text2 = []
    Text3 = []
    Text4 = []
    Text5 = []
    TextUndo = []
'''

if lang == 'ru':
    # Russian Edition
    SHOW_HIDE_MARKED_STAR_KEYs = [ u'э', u'Э' ] # marked

    REPLAY_BUTTONs   = [ u'к', u'К' ] # Replay Audio
    RECORD_BUTTONs   = [ u'м', u'М' ] # Record Voice
    RECORDED_BUTTONs = [ u'п', u'П' ] # Replay Voice
    OPTIONS_BUTTONs  = [ u'щ', u'Щ' ] # Options
    ADD_BUTTONs      = [ u'ф', u'Ф' ] # a
    BROWSE_BUTTONs   = [ u'и', u'И' ] # b
    DECK_BUTTONs     = [ u'в', u'В' ] # d
    SYNC_BUTTONs     = [ u'н', u'Н' ] # y
    # End of Russian Edition
else:
    SHOW_HIDE_MARKED_STAR_KEYs = []
    REPLAY_BUTTONs = []
    RECORD_BUTTONs = []
    RECORDED_BUTTONs = []
    OPTIONS_BUTTONs = []
    ADD_BUTTONs = []
    BROWSE_BUTTONs = []
    DECK_BUTTONs = []
    SYNC_BUTTONs = []

# Author:  Ben Lickly <blickly at berkeley dot edu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#   Hint-peeking add-on
# This add-on allows peeking at some of the fields in a flashcard
# before seeing the answer. This can be used to peek at word context,
# example sentences, word pronunciation (especially useful for
# Chinese/Japanese/Korean), and much more.

def _showHint(self): # self == mw.reviewer
    """To show next hint, simply click 5 or H key."""
    global F9_HINT_PEEKED
    F9_HINT_PEEKED = True
    return self.web.page().mainFrame().evaluateJavaScript("""
        (function(){
             var customEvent = document.createEvent('MouseEvents');
             customEvent.initEvent('click', false, true);
             var arr = document.getElementsByClassName('hint'); //.getElementsByTagName('a');
             if (arr.length>0) {
              for (var i=0; i<arr.length; i++) {
               var l=arr[i]; //alert(l.outerHTML);
               if (l.nodeName.toUpperCase() == 'A') {
                if (l.href.charAt(l.href.length-1) === '#' & l.style.display != 'none') {
                 l.dispatchEvent(customEvent);
                 var ll = arr[i+1]; 
                 var btn = ll.getElementsByClassName('replaybutton'); 
                 if (btn.length>0) {
                  for (var i=0; i<btn.length; i++) {
                   var lll=btn[i]; 
                   if (lll.nodeName.toUpperCase() == 'A') {
                    var gustomEvent = document.createEvent('MouseEvents');
                    gustomEvent.initEvent('click', false, true);
                    lll.dispatchEvent(gustomEvent); //alert(lll.href); //alert(lll.innerHTML);
                   }
                  }
                 }
                 return true; // break;
                }
               }
              } // for
             }
             return false;
         }())
     """)

def _doHint(self): # self == mw.reviewer
    global F9_HINT_PEEKED
    if not _showHint(self):
        if self.state == "question":
           self._showAnswer() # ._showAnswerHack()
        elif self.state == "answer":
           F9_HINT_PEEKED = False
           self._initWeb() # ._initWeb() # _showQuestion()
        #pass

def _showAllHints():
    """To show hints, simply click all show hint buttons."""
    global F9_HINT_PEEKED
    F9_HINT_PEEKED = True
    mw.reviewer.web.eval("""
        (function(){
             var customEvent = document.createEvent('MouseEvents');
             customEvent.initEvent('click', false, true);
             var arr = document.getElementsByClassName('hint'); //.getElementsByTagName('a');
             if (arr.length===0) return false;
             for (var i=0; i<arr.length; i++) {
               var l=arr[i];
              if (l.nodeName.toUpperCase() == 'A') {
               if (l.href.charAt(l.href.length-1) === '#' & l.style.display != 'none') {
                 l.dispatchEvent(customEvent);
                 var ll = arr[i+1]; //alert(ll.innerHTML);
                     var btn = ll.getElementsByClassName('replaybutton'); 
                     if (btn.length===0) continue;
                     for (var i=0; i<btn.length; i++) {
                      var lll=btn[i]; 
                      if (lll.nodeName.toUpperCase() == 'A') {
                       var gustomEvent = document.createEvent('MouseEvents');
                        gustomEvent.initEvent('click', false, true);
                          lll.dispatchEvent(gustomEvent); //alert(lll.href); //alert(lll.innerHTML);
                      }
                     }
               }
              }
             }
         }())
     """)

def on_showHint():
      _doHint(mw.reviewer)

def on_showAllHints():
    _showAllHints()

# Copyright © 2013–2014  Roland Sieker <ospalh@gmail.com>
# -- from COLORFUL_TOOLBARS.py
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

def ask_delete():
    #"""Delete a note after asking the user."""
    if askUser(u"Удалить запись?" if lang=='ru' else _(u'Delete note?'), defaultno=True):
        mw.reviewer.onDelete()

# Name: Disable the delete key in reviews
if A['DISABLE_DEL'][0]:
   aqt.mw.disconnect(aqt.mw.reviewer.delShortcut, aqt.qt.SIGNAL("activated()"), aqt.mw.reviewer.onDelete)
   aqt.mw.connect(aqt.mw.reviewer.delShortcut, aqt.qt.SIGNAL("activated()"), ask_delete)

def go_deck_browse():
    """Open the deck browser."""
    mw.moveToState("deckBrowser")

def go_study():
    """Start studying cards."""
    mw.col.reset()
    mw.col.startTimebox()
    mw.moveToState("review")

def go_options():
    """Options group..."""
    try:
        mw.reviewer.onOptions()
    except AttributeError:
        pass

def overeview():
    if mw.state == "overview":
        mw.col.startTimebox()
        mw.moveToState("review")
        if mw.state == "overview":
            mw.moveToState("deckBrowser")
    else:
        mw.moveToState("overview")

##

def new_replayq(self, card, previewer=None):
    s = previewer if previewer else self
    if not s.card:
        return true # false
    else:
        return s.mw.col.decks.confForDid(
            s.card.odid or s.card.did).get('replayq', True)

Reviewer._replayq = new_replayq # What is it? This is for Replay Audio.

##

# -- Answer Confirmation plugin for Anki 2.0 --
# https://ankiweb.net/shared/info/3882211885

# Author:  Albert Lyubarsky
# Email: albert.lyubarsky@gmail.com
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Very simple add-on. 
# Show pressed Answer Button as tooltip
# only on pressed key, no tooltip on mouse click.

# Useful when answering by pressing shortcut keys 
# e.i.: 1,2,3,4 or default answer button e.i.: enter or space

answerCard_LA = ''

# -- if ANSWER_CONFIRMATION: --
def answerCard_before(self, ease) :
    global answerCard_LA
    la = self._answerButtonList()
    al = [item for item in la if item[0] == ease]
    if len(al) > 0 and ( B['B10_ANSWER_CONFIRMATION'][0] > 1 and ( ease<=1 or ease > 1 and ( ease != self._defaultEase() or ( self.mw.col.sched.answerButtons(self.card) <4 and B['B10_ANSWER_CONFIRMATION'][0] and ease==1 or self.mw.col.sched.answerButtons(self.card) == 4 and B['B10_ANSWER_CONFIRMATION'][0] and ease<3) ) ) ):
        tooltip(al[0][1], period=1500)
        answerCard_LA = al[0][1]
    else:
        answerCard_LA = ''

"""
Name: Answer Key Cascade
Filename: Answer_Key_Cascade.py
Version: 0.5
Author: Kenishi
Desc:    By default Anki 2 now reduces the button count depending on card age.
        Cards can now have anywhere from 2 to 4 buttons max depending on age.
        Answering a card with 2 buttons requires you to press 1 or 2 if you are using hotkeys.
        This can interfere with review speed if you don't realize its 2 buttons and answer 3/4.
        This addon makes it so answering with a higher ease than possible will answer with the actual highest.

        *Example* 3 Button card: You press "4", the addon answers with "3".
        Thanks go to ospalh(https://github.com/ospalh) for simpler implementation (should also eliminate state bugs)

        Report bugs to https://github.com/Kenishi/Answer-Key-Cascade
"""

# --------------------------
# key handler for any window
# --------------------------

"""
    def keyPressEvent(self, evt):
        # do we have a delegate?
        if self.keyHandler:
            # did it eat the key?
            if self.keyHandler(evt):
                return
        # run standard handler
        QMainWindow.keyPressEvent(self, evt)
        # check global keys
        key = unicode(evt.text())
        if key == "d":
            self.moveToState("deckBrowser")
        elif key == "s":
            if self.state == "overview":
                self.col.startTimebox()
                self.moveToState("review")
            else:
                self.moveToState("overview")
        elif key == "a":
            self.onAddCard()
        elif key == "b":
            self.onBrowse()
        elif key == "S":
            self.onStats()
        elif key == "y":
            self.onSync()
"""

def keyPressedEvent(evt):
    key = evt.key()
    text = unicode(evt.text())

    if (key in [Qt.Key_Escape] and mw.state in ['review','overview']):
        mw.moveToState("deckBrowser")

    if key in [Qt.Key_Space, Qt.Key_Return] and mw.state == 'deckBrowser':
            mw.col.startTimebox()
            mw.moveToState("review")
            return 

    if (key in Keys['D'] or (text in DECK_BUTTONs)): # key == "d":
        if mw.state == "review":
            mw.moveToState("deckBrowser")
        elif mw.state == "overview":
            mw.moveToState("deckBrowser")
        elif mw.state == "deckBrowser":
            mw.col.startTimebox()
            mw.moveToState("review")

    # DABSY dab sy -> stats on Shift+S
    elif (key in Keys['A'] or text in ADD_BUTTONs): # key == "a":
        mw.onAddCard()
    elif (key in Keys['B'] or text in BROWSE_BUTTONs): # key == "b":
        mw.onBrowse()
    elif (key in Keys['Y'] or text in SYNC_BUTTONs): # key == "y":
        mw.onSync()
    else:
        origKeyPressEvent(evt)

"""
Name: Answer Key Remap
Filename: Answer_Key_Remap.py
Version: 0.2
Author: fisheggs
Desc:   By default Anki 2 now reduces the button count depending on card age.
        Cards can now have anywhere from 2 to 4 buttons max depending on age.
        Answering a card with 2 buttons requires you to press 1 or 2 if you are using hotkeys.
        This can interfere with review speed if you don't realize its 2 buttons and answer 3/4.

        This maps
        2 button        Again = 1,2             Good = 3,4
        3 button        Again = 1,2             Good = 3    Easy = 4
        4 button        Again = 1   Hard = 2    Good = 3    Easy = 4

        So 
            1 is always Again
            2 is always harder than Good (either Again or Hard)
            3 is always Good
            4 is always easier than (or equal to) Good
        Thanks to Kenishi for Answer_Key_Cascade from which this code was modified.

v0.2 203-07-19 -- buttet proof lookup incase extra buttons are added
"""

def onKeyPlus():
    global soundtrack_q_number, soundtrack_a_number
    if mw.state == 'review':
        if mw.reviewer.state == 'question':
            if soundtrack_q_number >= len(soundtrack_q_list):
               soundtrack_q_number = 0
            if soundtrack_q_number < len(soundtrack_q_list):
                play(soundtrack_q_list[soundtrack_q_number])
            soundtrack_q_number += 1
        else:
            if soundtrack_a_number >= len(soundtrack_a_list):
               soundtrack_a_number = 0
            if soundtrack_a_number < len(soundtrack_a_list):
                play(soundtrack_a_list[soundtrack_a_number])
            soundtrack_a_number += 1

def onAudioList():
    if len(soundtrack_q_list)+len(soundtrack_a_list)>0:
        showInfo('' +
        'Replay Q <b>'+ unicode(soundtrack_q_number)+ '</b> '+ unicode(len(soundtrack_q_list))+ ' '+ unicode(soundtrack_q_list) + '<br>\n<br>' +
        'Replay A <b>'+ unicode(soundtrack_a_number)+ '</b> '+ unicode(len(soundtrack_a_list))+ ' '+ unicode(soundtrack_a_list) + '<br>\n<br>' +
        '')
    else:
        showInfo(u"Звуковых файлов на этой карте нет." if lang=='ru' else 'There is no any sound on this card.')

# Name: Handy Answer Keys Shortcuts
# Copyright: Vitalie Spinu 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Bind 'j', 'k', 'l', ';' to card answering actions.  This allows answering with
# right hand, keeping your thumb on SPC (default action) and other fingers on
# 'j', 'k', 'l', ';'. If the number of buttons is less than 4, 'l' and ';' will
# do the right thing - choose the maximal ease level.
#
# If you are in the "question" state (no answer is yet visible) these keys
# bypass the display of the answer and automatically set the ease level.  So if
# you press ';', the note is automatically marked with the highest ease level
# (last button in answer state), if you press 'k' or 'l', the note is marked by
# the default ease level ("good"), if you press 'j', the note is marked as hard
# (first button).
# As a bonus 'z' is bound to undo.

# -------------------------------
# key handler for reviewer window
# -------------------------------
def newKeyHandler(self, evt):
    key = evt.key()
    #text = unicode(evt.text())

    """Show hint when the hint peeking key is pressed."""
    if (self.state == "question" or self.state == "answer"):
      if (A['F9_HINT_PEEKING'][0] and (key in Keys['5'])):# or text in Text5)):
          _doHint(mw.reviewer)
          return True
    else:
          return _old(self, evt)

    isq = self.state == "question"
    if isq: 
       if A['ANSWER_BYPASS'][0] and \
          ( key in Keys['1'] or \
          key in Keys['2'] or \
          key in Keys['3'] or \
          key in Keys['4'] ):
          self._showAnswer() #._showAnswerHack()
       elif A['ANSWER_USING_REPLY_KEYS'][0] and \
          ( key in Keys['1'] or \
          key in Keys['2'] or \
          key in Keys['3'] or \
          key in Keys['4'] ):
           """
          ((key in Keys['1'] or text in Text1) or \
          (key in Keys['2'] or text in Text2) or \
          (key in Keys['3'] or text in Text3) or \
          (key in Keys['4'] or text in Text4)):
           """
           self._showAnswer()
           return

    cnt = mw.col.sched.answerButtons(mw.reviewer.card) # Get button count
    rst = mw.reviewer.state # self.state

# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Ignore_spaceenter_when_answer_shown.ppy
# Set focus to middle area when answer shown, so space does not trigger the answer buttons.

# Number key 0 shows answer
# by Madman Pierre, petere@madmanpierre.com

    if (rst == "question" or rst == "answer") and (key in Keys['Undo']):# or text in TextUndo):
      try: # throws an error on undo -> do -> undo pattern,  otherwise works fine
         mw.onUndo()
      except:
            pass

    elif rst == "answer" and key in [Qt.Key_Return, Qt.Key_Enter]:
        return True # to prevent pass through multiple cards
    elif (key in [Qt.Key_Space]):# or text == " "):
        if self.state == "question":
           self._showAnswer() #._showAnswerHack()
        elif self.state == "answer":
           if B['B10_ANSWER_CONFIRMATION'][0]:
              answerCard_before(self, self._defaultEase())
           self._answerCard(self._defaultEase())
    elif rst == "question" and key in Keys8:
         self._showAnswer() #._showAnswerHack()
    elif rst == "question" and key in Keys['0'] and A['KEY0'][0]:
         #self._showAnswer() #._showAnswerHack()
         return True
    elif rst == "answer" and key in Keys['0'] and A['KEY0'][0]:
           if B['B10_ANSWER_CONFIRMATION'][0]:
              answerCard_before(self, self._defaultEase())
           self._answerCard(self._defaultEase())

    elif rst == "answer" and (key in Keys['1']):# or text in Text1):
         if B['B10_ANSWER_CONFIRMATION'][0]:
            answerCard_before(self, 1)
         self._answerCard(1)
    elif rst == "answer" and (key in Keys['2']):# or text in Text2):
         if B['B10_ANSWER_CONFIRMATION'][0]:
            answerCard_before(self, 2)
         self._answerCard(2)
    elif rst == "answer" and (key in Keys['3']):# or text in Text3):
        if cnt == 2 or cnt == 3: 
           if B['B10_ANSWER_CONFIRMATION'][0]:
              answerCard_before(self, 2)
           self._answerCard(2)
        else: # 4
           if B['B10_ANSWER_CONFIRMATION'][0]:
              answerCard_before(self, 3)
           self._answerCard(3)
    elif rst == "answer" and (key in Keys['4']):# or text in Text4):
         if B['B10_ANSWER_CONFIRMATION'][0]:
            answerCard_before(self, cnt)
         self._answerCard(cnt)

    elif (key in Keys['Aster']):# or text in SHOW_HIDE_MARKED_STAR_KEYs):
        self.onMark()
    elif (key in Keys['Plus']): # Replay Next Audio
        onKeyPlus()
    #elif (key in Keys['R']):# or text in REPLAY_BUTTONs):
    #    self.replayAudio()
    #    return True

    #elif (key in KeysO or text in OPTIONS_BUTTONs):
    #    self.onOptions()

    #elif (key in KeysG or text in RECORDED_BUTTONs): # key == "V":
    #    self.onReplayRecorded()
    #elif (key in KeysV or text in RECORD_BUTTONs): # key == "v":
    #    self.onRecordVoice()

    #elif (key == Qt.CTRL+Qt.Key_PageUp and self.state == "answer"):
    #    go_study()
    # The keys codes come, but not in sum, just separately, one by one.

    #elif (key == Qt.CTRL+Qt.Key_PageDown and self.state == "question"):
    #    self._showAnswer() #._showAnswerHack()
    # приходить-то коды приходят, но делают это по отдельности

    else:
         origKeyHandler(self, evt)

# -- Refocus Card when Reviewing --
# Refocus_Card_when_Reviewing.py
# Copyright: Edgar Simo-Serra <bobbens@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# def interface_refocus():
#     mw.web.setFocus()
# addHook( "showQuestion", interface_refocus )
# addHook( "showAnswer",   interface_refocus )

# Set focus to middle area when answer shown, 
# so enter does not trigger the answer buttons.

def noAnswer():
    mw.web.setFocus() # mw.reviewer.web.setFocus()

#############################################################################################

if A['KEYS_HANDLER'][0]:

   #addHook("showQuestion", noAnswer) # with this hook space don't stop passing through multiple cards at once
   addHook("showAnswer", noAnswer)

   origKeyHandler = Reviewer._keyHandler
   Reviewer._keyHandler = newKeyHandler

   origKeyPressEvent = mw.keyPressEvent
   mw.keyPressEvent = keyPressedEvent

# -- Toggle Full Screen F11 --
# https://ankiweb.net/shared/info/1703043345

# Copyright: Jannick Drolf; ported  from Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# This plugin adds the ability to toggle full screen mode. 
# It adds an item to the tools menu.

def onFullScreen():
    mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)

mw.form.menuTools.addSeparator() # WTF?!

if A['TOGGLE_FULL_SCREEN_F11'][0]:
   F11_action = QAction(mw)
   F11_action.setText("Полно&экранный режим" if lang == 'ru' else "&Toggle Full Screen")
   if A['ANKI_MENU_ICONS'][0]:
        F11_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'full_screen.png')))
   F11_action.setShortcut(HOTKEY['full_screen'][0])
   mw.connect(F11_action, SIGNAL("triggered()"), onFullScreen)
   if mw_addon_view_menu_exists:
       mw.addon_view_menu.addSeparator()
       mw.addon_view_menu.addAction(F11_action) # mw.form.menuTools

#################################################################################################
# hotkeys does not work on context menu
# for information purpose only (exploratory testing is anticipated)

opts = [
    [_("Mark Note"), "*", mw.reviewer.onMark],
    None,
    [_("Bury Card"), "-", mw.reviewer.onBuryCard],
    [_("Bury Note"), "=", mw.reviewer.onBuryNote],
    [_("Suspend Card"), "@", mw.reviewer.onSuspendCard],
    [_("Suspend Note"), "!", mw.reviewer.onSuspend],
    [_("Delete Note"), "Delete", ask_delete], # mw.reviewer.onDelete],
    None,
    [_("Options"), "O", mw.reviewer.onOptions],
]

opts.extend([
    None,
    [_("Replay Audio"), "R", mw.reviewer.replayAudio],
    [u"Проиграть следующее аудио" if lang=="ru" else _("Replay Next Audio"), "+", onKeyPlus],
    None,
])

opts.append(
    [_("Record Own Voice"), HOTKEYZ['record_own_voice'][0], mw.reviewer.onRecordVoice],
)
opts.append(
    [_("Replay Own Voice"), HOTKEYZ['replay_own_voice'][0], mw.reviewer.onReplayRecorded],
)

def go_lambda(adres):
    openLink(adres)

def go_writing():
    openLink("http://ankisrs.net/docs/addons.html")

def go_AnkiTest():
    openLink("http://finpapa.ucoz.ru/index.html")

def go_official():
    openLink("http://ankisrs.net/")

def go_AnkiSRS():
    openLink("http://ankisrs.net/#download")

def go_AnkiWeb():
    openLink("https://ankiweb.net/")

def go_AnkiWeb_decks():
    openLink("https://ankiweb.net/shared/decks/")

def go_AnkiWeb_addons():
    openLink("https://ankiweb.net/shared/addons/")

def go_media_folder():
    d = os.path.join(mw.pm.profileFolder(), "collection.media")
    openFolder(d)

def go_backups_folder():
    d = os.path.join(mw.pm.profileFolder(), "backups")
    openFolder(d)

def go_addons_folder():
    openFolder(mw.addonManager.addonsFolder())

def go_data_folder():
    openFolder(os.path.join(mw.addonManager.addonsFolder(), '..'))

def go_profile_folder():
    openFolder(mw.pm.profileFolder())

def go_answer():
    if mw.state == 'review':
        if mw.reviewer.state == 'question':
            anki.sound.stopMplayer()
            mw.reviewer._showAnswer() # _showAnswerHack()
    # mw.reviewer notwithstanding 'review' !!! ,Однако

def go_question():
    global F9_HINT_PEEKED
    if mw.state == 'review':
        if mw.reviewer.state == 'answer' or mw.reviewer.state == 'question': # refresh FrontSide on PgUp
            anki.sound.stopMplayer()
            F9_HINT_PEEKED = True
            mw.reviewer._initWeb() # _showQuestion()

############
# --

sync_aktion = QAction(mw)
sync_aktion.setText(u"Син&хронизировать с AnkiWeb" if lang=="ru" else _(u"S&ynchronize with AnkiWeb"))
if A['ANKI_MENU_ICONS'][0]:
    sync_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'sync.png')))
sync_aktion.setShortcut(QKeySequence(HOTKEYZ['Synchro'][0]))
mw.connect(sync_aktion, SIGNAL("triggered()"), mw.onSync)

sync_action = QAction(mw)
sync_action.setText(u"Син&хронизировать с AnkiWeb" if lang=="ru" else _(u"S&ynchronize with AnkiWeb"))
sync_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'sync.png')))
sync_action.setShortcut(QKeySequence(HOTKEYZ['Sync'][0]))
mw.connect(sync_action, SIGNAL("triggered()"), mw.onSync)

edit_layout_action = QAction(mw) # TODO !!!
edit_layout_action.setText(u'&Карточки...' if lang=='ru' else _(u"&Cards..."))
edit_layout_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_layout.png')))
edit_layout_action.setShortcut(QKeySequence(HOTKEY['edit_layout'][0]))
mw.connect(edit_layout_action, SIGNAL("triggered()"), go_edit_layout)

if A['COLORFUL_TOOLBAR'][0]:
    # DAB

    decks_action = QAction(mw)
    decks_action.setText(u'Коло&ды' if lang=='ru' else _("&Decks"))
    decks_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'deck_browser.png')))
    if A['ANKI12SHORTCUTS'][0]:
        decks_action.setShortcut(QKeySequence(HOTKEYZ['Decks'][0]))
    mw.connect(decks_action, SIGNAL("triggered()"), go_deck_browse)

    add_notes_action = QAction(mw)
    add_notes_action.setText(u'Доб&авить' if lang=='ru' else _("&Add"))
    add_notes_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'add.png')))
    add_notes_action.setShortcut(QKeySequence(HOTKEYZ['Add'][0]))
    mw.connect(add_notes_action, SIGNAL("triggered()"), mw.onAddCard)

    browse_cards_action = QAction(mw)
    browse_cards_action.setText(u'О&бзор' if lang=='ru' else _("&Browse"))
    browse_cards_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'browse.png')))
    browse_cards_action.setShortcut(QKeySequence(HOTKEYZ['Browse'][0]))
    mw.connect(browse_cards_action, SIGNAL("triggered()"), mw.onBrowse)

    decks_aktion = QAction(mw)
    decks_aktion.setText(u'Коло&ды' if lang=='ru' else _("&Decks"))
    decks_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-deck_browser.png')))
    mw.connect(decks_aktion, SIGNAL("triggered()"), go_deck_browse)

    add_notes_aktion = QAction(mw)
    add_notes_aktion.setText(u'Доб&авить' if lang=='ru' else _("&Add"))
    add_notes_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-add.png')))
    mw.connect(add_notes_aktion, SIGNAL("triggered()"), mw.onAddCard)

    mw.form.actionImport.setShortcut(QKeySequence(HOTKEYZ['Import'][0]))
    mw.form.actionExport.setShortcut(QKeySequence(HOTKEYZ['Export'][0]))

    eddit_current_action = QAction(mw)
    eddit_current_action.setText(u'Р&едактирование...' if lang=='ru' else _(u"&Edit..."))
    eddit_current_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_current.png')))
    eddit_current_action.setShortcut(QKeySequence(HOTKEY['Editor'][0]))
    mw.connect(eddit_current_action, SIGNAL("triggered()"), go_edit_current)

    options_aktion = QAction(mw)
    options_aktion.setText(u'&Настройки...' if lang=='ru' else _(u"&Options..."))
    options_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-options.png')))
    mw.connect(options_aktion, SIGNAL("triggered()"), go_options)

    statistics_action = QAction(mw)
    statistics_action.setText(u'&Статистика' if lang=='ru' else _(u"&Statistics"))
    statistics_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'statistics.png')))
    statistics_action.setShortcut(QKeySequence(HOTKEY['Statistics'][0]))
    mw.connect(statistics_action, SIGNAL("triggered()"), mw.onStats)

    statistics_aktion = QAction(mw)
    statistics_aktion.setText(u'&Статистика' if lang=='ru' else _(u"&Statistics"))
    statistics_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-statistics.png')))
    mw.connect(statistics_aktion, SIGNAL("triggered()"), mw.onStats)

    overeview_action = QAction(mw)
    overeview_action.setText(u'Обзор колод&ы' if lang=='ru' else _(u"&Overview Deck"))
    overeview_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'study_options.png')))
    overeview_action.setShortcut(QKeySequence(HOTKEY['goto_stats'][0])) 
    mw.connect(overeview_action, SIGNAL("triggered()"), overeview)

    study_action = QAction(mw)
    study_action.setText(u'&Учить колоду' if lang=='ru' else _(u"S&tudy deck"))
    study_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'study.png')))
    study_action.setShortcut(QKeySequence(HOTKEY['goto_deck'][0])) 
    mw.connect(study_action, SIGNAL("triggered()"), go_study)

    study_aktion = QAction(mw)
    study_aktion.setText(u'&Учить колоду' if lang=='ru' else _(u"S&tudy deck"))
    study_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-study.png')))
    mw.connect(study_aktion, SIGNAL("triggered()"), go_study)

    def onRollback():
        if mw.state == "review":
            if mw.reviewer.state == "answer":
                mw.reviewer._initWeb()
            else:
                mw.onUndo()
        else:
            mw.onUndo()

    undo_onF2_action = QAction(mw)
    undo_onF2_action.setText(u'&Откат' if lang=='ru' else _(u"&Rollback"))
    undo_onF2_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'undo.png')))
    #undo_onF2_action.setShortcut(QKeySequence(QKeySequence.Undo)) # ^Z only
    if A['COLORFUL_TOOLBAR'][0]:
        undo_onF2_action.setEnabled(False)
    mw.connect(undo_onF2_action, SIGNAL("triggered()"), mw.onUndo)

    # monkey patch
    def maybeF2EnableUndo():
      if hasattr(mw,'col'):
        if mw.col and mw.col.undoName():
            mw.form.actionUndo.setText(_("Undo")+(" %s"%mw.col.undoName()))
            if A['COLORFUL_TOOLBAR'][0]:
                mw.form.actionUndo.setEnabled(True)
                undo_action.setEnabled(True)
            runHook("undoState", True)
        else:
            mw.form.actionUndo.setText(_("Undo"))
            if A['COLORFUL_TOOLBAR'][0]:
                mw.form.actionUndo.setEnabled(False)
                undo_action.setEnabled(False)
            runHook("undoState", False)

    mw.maybeEnableUndo = maybeF2EnableUndo

###############################################################################
#
    if mw_addon_go_menu_exists:
        mw.addon_go_menu.addAction(undo_onF2_action)
        mw.addon_go_menu.addSeparator()
        mw.addon_go_menu.addAction(eddit_current_action)
        mw.addon_go_menu.addAction(edit_layout_action)
        mw.addon_go_menu.addSeparator()
        # Add DABSY to the new go menu
        mw.addon_go_menu.addAction(decks_action)
        mw.addon_go_menu.addAction(add_notes_action)
        mw.addon_go_menu.addAction(browse_cards_action)
        mw.addon_go_menu.addSeparator()
        mw.addon_go_menu.addAction(statistics_action)
        mw.addon_go_menu.addAction(sync_action)
        mw.addon_go_menu.addSeparator()
        mw.addon_go_menu.addAction(overeview_action)
        mw.addon_go_menu.addAction(study_action)

#####################################################
#
download_addon_action = QAction(mw)
download_addon_action.setText(u'Открыть сайт Anki&Web с дополнениями' if lang=='ru' else _(u"Open &AnkiWeb shared add-ons site"))
mw.connect(download_addon_action, SIGNAL("triggered()"), go_AnkiWeb_addons)
mw.form.menuPlugins.insertAction(mw.form.actionOpenPluginFolder, download_addon_action) 

if A['OPEN_FOLDERS'][0]:

    writing_action = QAction(mw)
    writing_action.setText(u"&Написание дополнений" if lang=="ru" else u"&Writing add-ons")
    mw.connect(writing_action, SIGNAL("triggered()"), go_writing)

    # Открыть сайт Самоучитель Anki 2.0 Tutorial

    helpful_action = QAction(mw)
    helpful_action.setText(u'Открыть &сайт "Cправочник по Anki 2.0"' if lang=='ru' else _(u"&Open Anki 2.0 HandBook"))
    if A['ANKI_MENU_ICONS'][0]:
        helpful_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'green_tick_16.png')))
    mw.connect(helpful_action, SIGNAL("triggered()"), go_AnkiTest)

    def myCreateDeck():
        deck = getOnlyText(_("Name for deck:"))
        if deck:
            mw.col.decks.id(deck)
            mw.deckBrowser.refresh()
            mw.onAddCard()

    create_deck_action = QAction(mw)
    create_deck_action.setText(u'Со&здать колоду' if lang=='ru' else _(u"&Create Deck"))
    create_deck_action.setToolTip(_(u"Create ParentDeck::ChildSubDeck."))
    mw.connect(create_deck_action, SIGNAL("triggered()"), myCreateDeck)

    download_deck_action = QAction(mw)
    download_deck_action.setText(u'Ска&чать колоды с сайта AnkiWeb' if lang=='ru' else _(u"Down&load AnkiWeb Decks"))
    download_deck_action.setToolTip(_(u"Open AnkiWeb decks site."))
    mw.connect(download_deck_action, SIGNAL("triggered()"), go_AnkiWeb_decks)

    go_ankisrs_action = QAction(mw)
    go_ankisrs_action.setText(u'&Открыть сайт AnkiSRS' if lang=='ru' else _(u"Open AnkiS&RS site"))
    mw.connect(go_ankisrs_action, SIGNAL("triggered()"), go_AnkiSRS)

    go_official_action = QAction(mw)
    go_official_action.setText(u'О&ткрыть официальный сайт Anki' if lang=='ru' else _(u"&Official Anki site"))
    mw.connect(go_official_action, SIGNAL("triggered()"), go_official)

    go_ankiweb_action = QAction(mw)
    go_ankiweb_action.setText(u'Открыть с&айт AnkiWeb' if lang=='ru' else _(u"Open Anki&Web site"))
    mw.connect(go_ankiweb_action, SIGNAL("triggered()"), go_AnkiWeb)

    go_media_action = QAction(mw)
    go_media_action.setText(u'Открыть папку с &медиа-файлами коллекции' if lang=='ru' else _(u"Open &collection.media folder"))
    mw.connect(go_media_action, SIGNAL("triggered()"), go_media_folder)

    go_backups_action = QAction(mw)
    go_backups_action.setText(u'Открыть папку с &резервными копиями профиля' if lang=='ru' else _(u"Open &backups  folder"))
    mw.connect(go_backups_action, SIGNAL("triggered()"), go_backups_folder)

    go_addons_action = QAction(mw)
    go_addons_action.setText(u'Открыть папку с &дополнениями' if lang=='ru' else _(u"Open add&ons folder"))
    mw.connect(go_addons_action, SIGNAL("triggered()"), go_addons_folder)

    go_profile_action = QAction(mw)
    go_profile_action.setText(u'Открыть папку &профиля' if lang=='ru' else _(u"Open &profile folder"))
    mw.connect(go_profile_action, SIGNAL("triggered()"), go_profile_folder)

    go_data_action = QAction(mw)
    go_data_action.setText(u'Открыть папку с да&нными всех профилей' if lang=='ru' else _(u"Open da&ta folder"))
    mw.connect(go_data_action, SIGNAL("triggered()"), go_data_folder)

    def go_pgm_folder():
        fldr = os.path.abspath(sys.argv[0])
        try:
            if fldr.index('\/'):
                fldr = '\/'.join(fldr.split('\/')[:-1])
        except ValueError:
            pass
        try:
            if fldr.index('\\'):
                fldr = '\\'.join(fldr.split('\\')[:-1])
        except ValueError:
            pass
        openFolder(fldr)

    go_pgm_action = QAction(mw)
    go_pgm_action.setText(u'Открыть папку про&граммы' if lang=='ru' else _(u"Open progra&m folder"))
    mw.connect(go_pgm_action, SIGNAL("triggered()"), go_pgm_folder)

    mw.form.menuCol.insertAction(mw.form.actionExit, create_deck_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, download_deck_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, sync_aktion)

    mw.form.menuCol.insertAction(mw.form.actionExit, go_ankisrs_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, go_ankiweb_action)
    mw.form.menuCol.insertSeparator(mw.form.actionExit)

    mw.form.menuCol.insertAction(mw.form.actionExit, go_media_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, go_backups_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, go_profile_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, go_addons_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, go_data_action)
    mw.form.menuCol.insertAction(mw.form.actionExit, go_pgm_action)
    mw.form.menuCol.insertSeparator(mw.form.actionExit)

    mw.form.menuHelp.insertAction(mw.form.actionDonate, go_official_action)
    if not os.path.exists(os.path.join(mw.pm.addonFolder(), "--handbook.py")):
        mw.form.menuHelp.addAction(writing_action)
        if lang=='ru':
            mw.form.menuHelp.addSeparator()
            mw.form.menuHelp.addAction(helpful_action)

    download_decks_action = QAction(mw)
    download_decks_action.setText(u'Открыть са&йт AnkiWeb с колодами' if lang=='ru' else _(u"Open AnkiWeb shared &Decks"))
    mw.connect(download_decks_action, SIGNAL("triggered()"), go_AnkiWeb_decks)

    download_addons_action = QAction(mw)
    download_addons_action.setText(u'Открыть сай&т AnkiWeb с дополнениями' if lang=='ru' else _(u"Open AnkiWeb shared &Add-ons"))
    mw.connect(download_addons_action, SIGNAL("triggered()"), go_AnkiWeb_addons)

    lambda_action = QAction(mw)
    lambda_action.setText(u'Anki’s Tender. This is the home of all support for Anki')
    mw.connect(lambda_action, SIGNAL("triggered()"), lambda: go_lambda('https://anki.tenderapp.com/'))

    lambda2_action = QAction(mw)
    lambda2_action.setText(u'reddit.com r Anki. This is a forum about the Anki flashcard program')
    mw.connect(lambda2_action, SIGNAL("triggered()"), lambda: go_lambda('https://www.reddit.com/r/Anki/'))

    mw.form.menuHelp.addSeparator()
    mw.form.menuHelp.addAction(download_decks_action)
    mw.form.menuHelp.addAction(download_addons_action)
    mw.form.menuHelp.addAction(lambda_action)
    mw.form.menuHelp.addAction(lambda2_action)
    mw.form.menuHelp.addSeparator()

##############################
#
get_A_list_action = QAction(mw)
get_A_list_action.setText("&Управляющие переменные" if lang == 'ru' else "A va&riables")
if A['ANKI_MENU_ICONS'][0]:
    get_A_list_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'sheet.png')))
get_A_list_action.setShortcut(QKeySequence(HOTKEY['F3_A'][0]))
mw.connect(get_A_list_action, SIGNAL("triggered()"), _getA)

#mw.addon_cards_menu.addSeparator()
mw.addon_cards_menu.addAction(get_A_list_action)
mw.addon_cards_menu.addSeparator()

##############################
#
# -- Accept Anki 1.2 shortcuts to list decks, add cards and open browser -- 
# https://ankiweb.net/shared/info/544525276

# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Emulate some Anki 1.2 shortcuts.
# Allows you to use the old ctrl+d, ctrl+f and ctrl+w shortcuts.

if A['ANKI12SHORTCUTS'][0]:

    mw.otherDeck = QShortcut(QKeySequence("Ctrl+w"), mw) # old Deck
    #mw.otherAdd = QShortcut(QKeySequence("Ctrl+d"), mw) # old Add hinders to new Decks
    mw.otherBrowse = QShortcut(QKeySequence("Ctrl+f"), mw) # old Browse

    mw.connect(
    mw.otherDeck, SIGNAL("activated()"), lambda: mw.moveToState("deckBrowser"))
    #mw.connect(
    #  mw.otherAdd, SIGNAL("activated()"), lambda: mw.onAddCard())
    mw.connect(
    mw.otherBrowse, SIGNAL("activated()"), lambda: mw.onBrowse())

"""
Nice, but should have more shortcuts.
Posted on 2013-01-30

I loved getting my CTRL+F open browser shortcut back, 
but I'd also like to have the CTRL+E to edit the current card 
(or to close the editing screen and get back to review screen). 
Currently it's a shortcut to "export deck", 
which is totally stupid (who needs a shortcut for that...).

Having customizable shortcuts for more actions would be awesome. 
"""

# ----- ******** ############## ******** -----

"""
 Super helpful, but I have a suggested feature.
Posted on 2013-11-04

No complaints whatsoever about this plugin, it does just as advertised.

One suggested feature though, when I'm doing reviews and a card only has one potential pass interval 
(i.e., "Good") it'd be great if the "Good" button was larger too. 
What I picture is the "Again" button being small and taking up a portion of the space 
previously occupied by the "Show Answer" button, and then the larger "Good" button taking up that remaining space.

Likewise when there are only two intervals available, it'd be awesome 
if the "Good" and "Easy" buttons took up the space that the aforementioned, 
larger "Good" button would take up, but this is less important than getting a large "Good" button. 
It'd be a nice additional touch though.

This'd be an awesome addition to make those difficult or new cards less frustrating than they already are. 
"""

# Replace _answerButtonList method
def answerButtonList(self):
    l = ((1, "<style>" + ("button span{font-size:x-large;}" if B['B08_BIG_BUTTONS'][0] else "") + \
    " button small { color:#999;font-weight:400;padding-left:.35em;font-size: small; } " + \
    "</style>" + "<span style='color:" + btn_Again[0] + ";'>" + btn_Again[1] + "</span>", BEAMS1),)
    cnt = self.mw.col.sched.answerButtons(self.card)
    if cnt == 2:
        return l + ((2, "<span style='color:" + btn_Good[0] + ";font-weight:bold;'>" + btn_Good[1] + "</span>", BEAMS3),)
        # the comma at the end is mandatory, a subtle bug occurs without it
    elif cnt == 3:
        return l + ((2, "<span style='color:" + btn_Good[0] + ";font-weight:bold;'>" + btn_Good[1] + "</span>", BEAMS2), 
                    (3, "<span style='color:" + btn_Easy[0] + ";'>" + btn_Easy[1] + "</span>", BEAMS1))
    else:
        return l + ((2, "<span style='color:" + btn_Hard[0] + ";'>" + btn_Hard[1] + "</span>", BEAMS1), 
                    (3, "<span style='color:" + btn_Good[0] + ";font-weight:bold;'>" + btn_Good[1] + "</span>", BEAMS1),
                    (4, "<span style='color:" + btn_Easy[0] + ";'>" + btn_Easy[1] + "</span>", BEAMS1))
# all buttons are with coloured text
# and have an equal width with buttons in Night Mode

# _____ ------ ========== *********** ========== -------- ______

if A['CUSTOM_CONGRAT_MSG'][0] and lang == 'ru':
   th_Unseen = u"<small style='color:#DA70D6;'>Неви-<br>данные</small>" # Не&nbsp;про-<br>смотрено</small>"
   th_Suspended = u'<small style="color:#c90;">Исклю-<br>чённые</small>'
   th_Buried    = u'<small style="color:#960;">Отло-<br>женные</small>'
   _Buried = u'Отложенные' # поскольку у Дамьена не предложено это слово для перевода
elif A['CUSTOM_CONGRAT_MSG'][0] and lang == 'en':
   th_Unseen = u"<small style='color:#DA70D6;'>Unseen</small>"
   th_Suspended = u'<small style="color:#c90;">Sus-<br>pen-<br>ded&nbsp;</small>'
   th_Buried    = u'<small style="color:#960;">Buried</small>'
   _Buried = u'Buried' 
else:
   th_Unseen = u"<span style='color:#DA70D6;'>" + _("Unseen") + "</span>"
   th_Suspended = u"<span style='color:#c90;'>" + _("Suspended") + "</span>"
   th_Buried    = u"<span style='color:#960;'>" + _("Buried") + "</span>"
   _Buried = _("Buried") # у Дамьена переводятся только Suspended и Suspended+Buried

#################################################################################################

# Copyright © 2012–2014 Roland Sieker <ospalh@gmail.com>
#   Show_learn_count.py
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/licenses/agpl.html

"""
Anki-2 add-on to show the learn count in the deck browser proper way
"""

from aqt.deckbrowser import DeckBrowser

def my_studyDeck(self, did):
    self.scrollPos =  self.web.page().mainFrame().scrollPosition()
    self.mw.col.decks.select(did)
    self.mw.col.startTimebox()
    self.mw.moveToState("review")
    if self.mw.state == "overview":
        more_tool_bar_off()
        tooltip(_("No cards are due yet."))

# Event handlers
# Monkey patching

def my_studyHandler(self, url):
    if ":" in url:
        (cmd, arg) = url.split(":")
    else:
        cmd = url
        arg = ''
    if cmd == "study":
        my_studyDeck(self, arg)

DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler, my_studyHandler) # , 'before')  

################################################################
def nonzeroColour(acnt, colour, did):
    if not acnt:
       colour = "silver"
    achk = B['B04_HIDE_BIG_NUMBERS'][0] and acnt > B['B04_HIDE_BIG_NUMBER'][0]
    if achk:
        cnt = "%s+" % (B['B04_HIDE_BIG_NUMBER'][0])
    else:
        cnt = str(acnt)
    return ("""<a href="study:{}" style="text-decoration:none;cursor:pointer;color:{};" {} onmouseover="this.style.textDecoration='underline';" onmouseout="this.style.textDecoration='none';">&nbsp;{}&nbsp;</a>""".format(did, colour, \
    ((' title=" '+ _('Study') + ' %s "'%(acnt if achk else '')) if B['B11_BUTTON_TITLES'][0] else ''), cnt) \
    if did and acnt else \
    """<span style="color:{};{}>&nbsp;{}&nbsp;</span>""".format(colour, \
    (('%s" title="%s"'%(('cursor:help;' if achk else ''),(acnt if achk else ''))) if B['B11_BUTTON_TITLES'][0] else '"'), \
    cnt)) if acnt > 0 else """<span style="color:{};">&nbsp;{}&nbsp;</span>""".format(colour, cnt)

################################################################
def deck_browser_render_deck_tree(deck_browser, nodes, depth=0):
    if not nodes:
        return ""

    if depth == 0:
       buf = """\n<tr>\n<th colspan=3 style='padding-right:.25em;color:default;'>%s</th>""" \
        % ( "<div style = padding-bottom:.25em; "+\
            (" title = Профиль " if B['B11_BUTTON_TITLES'][0] else "")+\
            ">" + (mw.pm.name if len(mw.pm.profiles()) > 1 and mw.pm.name else "") +\
            "</div><div style = font-weight:400;><i>" + _("Decks") + ":</i></div>" +\
            "</th>\n<td style='text-align:right;'>%s</td>" %\
            ("<i>"+_("Cards")+":</i>" if B['B00_MORE_OVERVIEW_STATS'][0] > 1 else "") )

       if B['B00_MORE_OVERVIEW_STATS'][0] > 1:
          buf += """\n
<td class=count style='padding-right:.25em;color:#33f;width:4em;'>%s</td>\
<td class=count style='padding-right:.25em;color:#c33;width:4em;'>%s</td>\
<td class=count style='color:#090;padding-right:.25em;width:4em;'>%s</td>\
<td class=count style='color:#999;padding-right:1em;width:4em;'>%s</td>\
\n""" % ( _("New"), "<small>Из-<br>учить</small>" if A['CUSTOM_CONGRAT_MSG'][0] and lang == 'ru' else _('Learn'), "<small>Про-<br>верить</small>" if A['CUSTOM_CONGRAT_MSG'][0] and lang == 'ru' else _('To Review'), _("Due") )

       if B['B00_MORE_OVERVIEW_STATS'][0] > 2:
          if not B['B03_GEAR_AT_END_OF_LINE'][0]:
             buf += "<td></td>"
          buf += """\n
<td style="padding-right:.25em;text-align:right;width:4em !important;">%s</td>\
<td style="padding-right:.25em;color:#c90;text-align:right;width:3em;">%s</td>\
<td style="padding-right:.25em;color:#960;text-align:right;width:3em;">%s</td>\
""" % ( th_Unseen, th_Suspended, th_Buried )

       buf += "\n</tr>\n" + deck_browser._topLevelDragRow()
    else:
        buf = ""
    for node in nodes:
        buf += deck_browser_deck_row(deck_browser, node, depth, len(nodes))
    if depth == 0:
        buf += deck_browser._topLevelDragRow()

        # Get due and new cards
        due = 0
        new = 0
        lrn = 0

        for tree in deck_browser.mw.col.sched.deckDueTree():
#        due += tree[2] + tree[3]
            due += tree[2]
            lrn += tree[3]
            new += tree[4]

        if B['B00_MORE_OVERVIEW_STATS'][0] > 1:

           buf += """\n
<tr style="vertical-align:top;">\
<th style="color:gray;text-align:left;">%s</th>\
<th align=left>%s</th><th align=left>%s</th>\
<th style='color:gray;text-align:right;'>%s:</th>\
<th class=count style='width:4em;'>%s</th>\
<th class=count style='width:4em;'>%s</th>\
<th class=count style='color:gray;width:4em;'>&nbsp;+&nbsp;%s</th>\
<th class=count style='color:gray;width:4em;padding-right:1em;'>&nbsp;=&nbsp;%s</th>\
\n""" % ( lang, _("Total"), \
                nonzeroColour( mw.col.cardCount(), "default", False ), \
                nonzeroColour(new+lrn+due, "gray", False), \
                nonzeroColour(new, "#33f", False), \
                nonzeroColour(lrn, "#c33", False), \
                nonzeroColour(due, "#090", False), \
                nonzeroColour(lrn+due, "#999", False) )

        # options
        if not B['B03_GEAR_AT_END_OF_LINE'][0] and B['B00_MORE_OVERVIEW_STATS'][0] > 2:
          buf += "<td>&nbsp;</td>\n"

        if B['B00_MORE_OVERVIEW_STATS'][0] > 2:
           unseen = deck_browser.mw.col.db.scalar("select count(*) from cards where queue=0")
           suspended = deck_browser.mw.col.db.scalar("select count(*) from cards where queue = -1")
           buried    = deck_browser.mw.col.db.scalar("select count(*) from cards where queue = -2")

           buf += """\
<td style="padding-right:.25em;width:4em !important;" align=right>%s&nbsp;</td>\
<td style="padding-right:.25em;width:3em;" align=right>%s&nbsp;</td>\
<td style="padding-right:.5em;width:3em;" align=right>%s&nbsp;</td>\
""" % (
            nonzeroColour(unseen, "#DA70D6", False),
            nonzeroColour(suspended, "#c90", False),
            nonzeroColour(buried, "#960", False)) # "#555500"))

        buf += "\n</tr>\n"

    return buf

################################################################
def deck_browser_deck_row(deck_browser, node, depth, cnt):
    name, did, due, lrn, new, children = node
    deck = deck_browser.mw.col.decks.get(did)

    if B['B00_MORE_OVERVIEW_STATS'][0] > 2:
       unseen = deck_browser.mw.col.db.scalar("select count(*) from cards where did = %i and queue=0" % did)
       suspended = deck_browser.mw.col.db.scalar("select count(*) from cards where did = %i and queue = -1" % did)
       buried    = deck_browser.mw.col.db.scalar("select count(*) from cards where did = %i and queue = -2" % did)

    if did == 1 and cnt > 1 and not children:
        # if the default deck is empty, hide it
        if not deck_browser.mw.col.db.scalar(
                "select 1 from cards where did = 1"):
            return ""

    # parent toggled for collapsing
    for parent in deck_browser.mw.col.decks.parents(did):
        if parent['collapsed']:
            buff = ""
            return buff
    prefix = "<big><b>&minus;</b></big>"
    if deck_browser.mw.col.decks.get(did)['collapsed']:
        prefix = "<big><b>&plus;</b></big>"

#    due += lrn

    def indent():
        return "&nbsp;"*6*depth

    if did == deck_browser.mw.col.conf['curDeck']:
        klass = 'deck current'
    else:
        klass = 'deck'

    buf = "\n<tr class='%s' id='%d' " % (klass, did) 
    #buf += """_onmouseover="this.style.backgroundColor='#ddd';this.style.backgroundImage='-webkit-linear-gradient(bottom,#ddd,#eee ,#ddd)';" """
    #buf += """_onmouseout="this.style.backgroundColor='';this.style.backgroundImage='';" """
    # указание колоды под курсором сбивается при вызове контекстного меню под шестерёнкой

    if B['B11_BUTTON_TITLES'][0]:
        buf += (' title = " ' + _('Today') + ': %s "') % (new+lrn+due)
    buf += '>'

    # deck link
    if children:
        collapse = """<a class=collapse href=# onclick='py.link("collapse:%d");return false;' \
        style="padding-left:.5em;padding-right:.1em;margin-right:.2em; \
        border:solid 1px transparent;border-radius:5px;display:inline-block;" \
        onmouseover="this.style.border='solid 1px silver';" \
        onmouseout="this.style.border='solid 1px transparent';" \
        title="%s">%s</a>""" % (
            did, (u' title=" Свернуть/развернуть вложенные колоды "' if lang=='ru' else ' title=" '+_(' Collapse/Downfall ')+' "') if B['B11_BUTTON_TITLES'][0] else '', prefix)
    else:
        collapse = "<span class=collapse></span>"
    if deck['dyn']:
        extraclass = "filtered"
    else:
        extraclass = ""

    studydid = ('''onclick="py.link('study:%d');"''' % did) if (new+lrn+due)>0 else ""
    cursorPointer = ('''cursor:pointer''') if (new+lrn+due)>0 else ""

    buf += """
    <td class=decktd colspan=4 %s style="%s;">%s%s<a class="deck %s" href=%s %s>%s</a>\
</td>""" % ( studydid, cursorPointer, \
    indent(), collapse, extraclass, \
    #(''' onclick="py.link('open:%d');return false;"''' % did) if (new+lrn+due)>0 else ("open:%d" % did), \
    # In such case KHTML doesn't recognize tag as anchor link, processes it as tag span.
    ('''# onclick="py.link('open:%d');return false;"''' % did) if (new+lrn+due)>0 else ("open:%d" % did), \
    (" title=' "+_('Study')+" '") if B['B11_BUTTON_TITLES'][0] else '', "<b>"+name+"</b>" if new+lrn+due > 0 else name)

    if B['B00_MORE_OVERVIEW_STATS'][0] > 1:
       buf += """\n\
<td align=right %s style="%s;">%s</td>\
<td align=right %s style="%s;">%s</td>\
<td align=right %s style="%s;">%s</td>\
<td align=right %s style="%s;padding-right:1em;">%s</td>\
\n""" % ( studydid, cursorPointer, nonzeroColour(new, "#33f", did),
          studydid, cursorPointer, nonzeroColour(lrn, "#c33", did),
          studydid, cursorPointer, nonzeroColour(due, "#090", did),
          studydid, cursorPointer, nonzeroColour(lrn+due, "#999", did)) 

    # options
    if not B['B03_GEAR_AT_END_OF_LINE'][0] and B['B00_MORE_OVERVIEW_STATS'][0] > 2:
      buf += "<td align=right class=opts style='width:1.5em!important;' onclick='return false;'>&nbsp;%s</td>" % deck_browser.mw.button(
        link="opts:%d" % did,
        name="<img src='qrc:/icons/gears.png'>&#9662;")

    if B['B00_MORE_OVERVIEW_STATS'][0] > 2:
       buf += """\
<td %s style="%s;padding-right:.25em;width:3em!important;" align=right>%s&nbsp;</td>\
<td %s style="%s;padding-right:.25em;" align=right>%s&nbsp;</td>\
<td %s style="%s;padding-right:.5em;" align=right>%s&nbsp;</td>\
""" % ( studydid, cursorPointer, nonzeroColour(unseen, "#DA70D6", did),
        studydid, cursorPointer, nonzeroColour(suspended, "#c90", did),
        studydid, cursorPointer, nonzeroColour(buried, "#960", did)) # "#555500"))

    # options
    if B['B03_GEAR_AT_END_OF_LINE'][0] or B['B00_MORE_OVERVIEW_STATS'][0] < 3:
      buf += "\n<td align=right class=opts style='width:1.5em!important;' onclick='return false;'>&nbsp;%s</td>" % deck_browser.mw.button(
        link="opts:%d" % did,
        name="<img _valign=bottom src='qrc:/icons/gears.png'>&#9662;")

    if B['B05_STUDY_BUTTON'][0]:
       buf += """\n<td align=right style="font-size:smaller;">&nbsp;%s</td>""" % deck_browser.mw.button(
        link="study:%d" % did, name="<small style = color:dodgerblue; >&#9658;</small>")

    buf += "\n</tr>\n"
    # children
    buf += deck_browser_render_deck_tree(deck_browser, children, depth+1)
    return buf

# Copyright: Juda Kaleta <juda.kaleta@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#  Unseen and buried counts
# https://ankiweb.net/shared/info/161964983
# Show count of unseen and buried cards in deck browser.

org_DeckBrowser_renderDeckTree = DeckBrowser._renderDeckTree
org_DeckBrowser_deckRow = DeckBrowser._deckRow

def initDeckBro():
 if B['B00_MORE_OVERVIEW_STATS'][0]:
    DeckBrowser._renderDeckTree = deck_browser_render_deck_tree
    DeckBrowser._deckRow = deck_browser_deck_row
 else:
    DeckBrowser._renderDeckTree = org_DeckBrowser_renderDeckTree
    DeckBrowser._deckRow = org_DeckBrowser_deckRow

initDeckBro()

##############################################################################

"""
Hierarchical Tags for Anki
==========================

This addon adds hierarchical tags to the browser in [Anki][]. The addon is
[published on Ankiweb](https://ankiweb.net/shared/info/1089921461).

To create hierarchies use double-colons in the tag names, for example
"learning::anki" or "language::japanese".

This addon is licensed under the same license as Anki itself (GNU Affero
General Public License 3).

## Known Issues

When clicking on a tag in the hierarchy, an asterisk is added to the search
term. The effect of that is that all notes with that tag and all subtags are
searched for.

But a side-effect is, that all tags with the same prefix are matched. For
example if you have a tag ``it`` and a tag ``italian``, clicking on the tag
``it`` would also show content from ``italian``. Let me know if this affects
you and I'll try to work around this.

## Support

The add-on was written by [Patrice Neff][]. I try to monitor threads in the
[Anki Support forum][]. To be safe you may also want to open a ticket on the
plugin's [GitHub issues][] page.

[Anki]: http://ankisrs.net/
[Patrice Neff]: http://patrice.ch/
[Anki support forum]: https://anki.tenderapp.com/discussions/add-ons
[GitHub issues]: https://github.com/pneff/anki-hierarchical-tags/issues 
"""

# -- Just to reduce the load time of the add-ons. -- without any mod. --
# https://ankiweb.net/shared/info/1089921461
from aqt.browser import Browser

# Separator used between hierarchies
SEPARATOR = '::'

def myTagTree(self, root, _old):
    tags = sorted(self.col.tags.all())
    tags_tree = {}

    for t in tags:
        if t.lower() == "marked" or t.lower() == "leech":
            continue

        components = t.split(SEPARATOR)
        for idx, c in enumerate(components):
            partial_tag = SEPARATOR.join(components[0:idx + 1])
            if not tags_tree.get(partial_tag):
                if idx == 0:
                    parent = root
                else:
                    parent_tag = SEPARATOR.join(components[0:idx])
                    parent = tags_tree[parent_tag]

                item = self.CallbackItem(
                    parent, c,
                    lambda partial_tag=partial_tag: self.setFilter("tag", partial_tag + '*'))
                item.setIcon(0, QIcon(":/icons/anki-tag.png"))

                tags_tree[partial_tag] = item

# Simple, nice, and easy.

#  Very neat! Thanks! 
#   If you like the new collapsible decks, you may want to try this. 
#    The separator can be changed in the file “hierarchical_tags.py”. (I use a hyphen.)

#     This changed a lot the way I use tags.
#      Only it cannot change me. ;-) 
#       So it's a pity that there is no way 
#        to change multiple tags at once like we can change cards in the Browser.
#         Here is a patch to ignore case in the tags (works better with ASCII tags than non-ASCII ones): 
#          https://github.com/pneff/anki-hierarchical-tags/pull/2/files 

if A['HIERARCHICAL_TAGS'][0]:
   Browser._userTagTree = wrap(Browser._userTagTree, myTagTree, 'around')  

######################################################################
# • Swap 
# https://ankiweb.net/shared/info/1040866511
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/

if A['SWAP_FRONT_BACK'][0]:
    CASE_SENSITIVE = False # True # 

    fldlst = [
        ['En','Ru'],
        ['Eng','Rus'],
        ['English','Russian'],
        ['по-английски','по-русски'],
        ['Q','A'],
        ['Question','Answer'],
        [_('Question'),_('Answer')],
        ['Front','Back'],
        [_('Front'),_('Back')], # Вопрос, Ответ
        ]

    fld1st = _('Front') # Вопрос
    fld2nd = _('Back') # Ответ

    def JustSwapIt(note):
      global fld1st, fld2nd
      if not (mw.reviewer.state == 'question' or mw.reviewer.state == 'answer'):
        showCritical("Обмен в списке колод или в окне колоды невозможен,<br>только при просмотре (заучивании) карточек." if lang=='ru' else 'Swap is available only for cards,<br>not for decks panel nor deck overview as well.')
      else:
       if not hasattr(mw.reviewer.card,'model'):
        showCritical("Извините, конечно, но пока делать просто нечего!" if lang=='ru' else 'Oops, <s>I did it again!</s> there is <b>nothing to do</b> yet!')
       else:
        c = mw.reviewer.card
        if c.model()['type'] == MODEL_CLOZE:
            showCritical("<center>Обмен полей для типа записей <b>с пропусками</b><br> не поддерживается. Только вручную.</center>" if lang=='ru' else """<div style="text-align:center;">It's unable to swap fields of CLOZE note type automatically.<br>Please, do it manually by yourself.</div>""") 
            # Unfortunately, style="text-align:center;" does not work here. But <center> works.
        elif c.model()['type'] == MODEL_STD:
            fldn = note.model()['flds']
            fldl = len(note.fields)

            audioSound = False
            for fld in fldn:
                if fld['name'].lower()=='audio' or fld['name'].lower()=='sound':
                   audioSound = True
                   break

            fnd1st = False
            for fld in fldn:
              for lst in fldlst:
                if CASE_SENSITIVE:
                    found = fld['name']==lst[0]
                else:
                    found = fld['name'].lower()==lst[0].lower()
                if found:
                   fnd1st = True
                   fld1st = fld['name']
                   break
              else:
                continue
              break

            fnd2nd = False
            for fld in fldn:
              for lst in fldlst:
                if CASE_SENSITIVE:
                    found = fld['name']==lst[1] and lst[0]==fld1st
                else:
                    found = fld['name'].lower()==lst[1].lower() and lst[0].lower()==fld1st.lower()
                if found:
                   fnd2nd = True
                   fld2nd = fld['name']
                   break
              else:
                continue
              break

            if fldl<2:
                showCritical("У данной записи одно-единственное поле,<br> его просто не с чем обменивать." if lang=='ru' else 'It is unable to swap a note with a single field in it.')
                return

            elif fldl==2: # There are two fields only? Swap it anyway.
                fld1st = fldn[0]['name']
                fld2nd = fldn[1]['name']
                swap_fld = note[fld1st]
                note[fld1st] = note[fld2nd]
                note[fld2nd] = swap_fld

            elif fldl==3 and audioSound: # There are three fields only? With Audio or Sound? Swap other two anyway.
                fld1st = ''
                fld2nd = ''
                for fld in fldn:
                    if fld['name'].lower()!='audio' and fld['name'].lower()!='sound' and fld1st=='':
                        fld1st = fld['name']
                    if fld['name'].lower()!='audio' and fld['name'].lower()!='sound' and fld2nd=='' and fld['name']!=fld1st:
                        fld2nd = fld['name']
                if fld1st!='' and fld2nd!='':
                    showInfo(unicode(fld1st)+' '+unicode(fld2nd))
                    swap_fld = note[fld1st]
                    note[fld1st] = note[fld2nd]
                    note[fld2nd] = swap_fld
                else:
                    showCritical('3 поля, но есть и Audio, и Sound. Что с чем обменивать-то тогда?')
                    return 

            # There are 3 (w/o Audio/Sound) or 4 or more fields?
            elif fnd1st and fnd2nd:
                # Swap by name if names are found in list. 
                swap_fld = note[fld1st]
                note[fld1st] = note[fld2nd]
                note[fld2nd] = swap_fld

            else:
                # Otherwise swap two first anyway.
                fld1st = fldn[0]['name']
                fld2nd = fldn[1]['name']
                swap_fld = note[fld1st]
                note[fld1st] = note[fld2nd]
                note[fld2nd] = swap_fld

            note.flush()  # never forget to flush
            tooltip(("Выполнен обмен значений между полями <b>%s</b> и <b>%s</b>." if lang=='ru' else '<b>%s</b> and <b>%s</b> swapped.')%(fld1st,fld2nd))

    def JustSwapItYourself():
        rst = mw.reviewer.state 
        NB = mw.reviewer.card.note()
        JustSwapIt(NB)
        mw.reset()  # refresh gui
        if rst == 'answer':
            mw.reviewer._showAnswer() # ._showAnswerHack()

    def TryItYourself(edit):
        JustSwapIt(edit.note)
        mw.reset()  # refresh gui
        # focus field so it's saved
        edit.web.setFocus()
        edit.web.eval("focusField(%d);" % edit.currentField)

    swap_action = QAction(('О&бмен полей %s и %s' if lang == 'ru' else _('S&wap %s and %s fields'))%(fld1st,fld2nd), mw)
    swap_action.setShortcut(QKeySequence(HOTKEY['swap'][0]))
    swap_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'swap.png')))
    mw.connect(swap_action, SIGNAL("triggered()"), JustSwapItYourself)

    def swap_off():
        swap_action.setEnabled(False)

    def swap_on():
        swap_action.setEnabled(True)

    def setup_buttons(editor):
        """Add the buttons to the editor."""
        editor._addButton("swap_fields", lambda edito=editor: TryItYourself(edito) , HOTKEY['swap'][0],
                           text="Sw", tip="Swap fields (" + HOTKEY['swap'][0] +")")

    mw.deckBrowser.show = wrap(mw.deckBrowser.show, swap_off)
    mw.overview.show = wrap(mw.overview.show, swap_off)
    mw.reviewer.show = wrap(mw.reviewer.show, swap_on)

    # register callback function that gets executed after setupEditorButtons has run. 
    # See Editor.setupEditorButtons for details
    addHook("setupEditorButtons", setup_buttons)


#######################################################################################
# To make ANKI working correct with images, sounds and videos
# start dir must contain only digits, spaces and basic English chars, maybe parentheses

check_prog_path = [
    ['en',u'The path to the program folder \n\n %s \n\n should contain only ASCII characters (32-127) [0-9A-Za-z \()]'],
    ['ru',u'Путь к программе не должен содержать кириллицы \n\n %s \n\n только латиницу из диапазона ASCII (32-127) [0-9A-Za-z \()]'],
]
#check_prog_path = False

def get_prog_path():
    """Return either "Anki" org argv[0]"""
    argv0 = sys.argv[0]
    if A['CHECK_ASCII_PATH'][0] and argv0:
        start_dir = os.path.abspath(argv0)
        score = len([char for char in start_dir if ord(char)>127])
        # show a message box
        if score > 0:
           showInfo(custom_msg % unicode(start_dir, errors='replace'), type="critical")

if check_prog_path:
   custom_msg = check_prog_path[0][1]
   for msgs in check_prog_path:
    if msgs[0] == lang:
       custom_msg = msgs[1]
       #break
   get_prog_path()

###################################################################################
# Deck name in title

# -- Just to reduce the load time of the add-ons. -- without any mod. --
# https://ankiweb.net/shared/info/3895972296
# v1.2.0 there, v1.3.0 here (from addons-ospalh.zip)

# © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

## Several separators between the current ‘activity’ (file, directory,
## web page) and the program name seem common. Pick one to taste:
title_separator = u' — '
# title_separator = u' – '
# title_separator = u' - ' # —–-
# title_separator = u' : '

## Show the sub-deck the current card belongs to
show_subdeck = True
# show_subdeck = False

# How to separate the clicked-on deck from the subdeck.
subdeck_format = u'{parent} || {child}'
#subdeck_format = u'{parent}:–:{child}'
# subdeck_format = u'{parent}(::{child})'  # Old style

## Use either "Anki" 
#use_argv_0 = False
## or the program file name.
use_argv_0 = True

def get_prog_name():
    """Return either "Anki" org argv[0]"""
    argv0 = sys.argv[0]
    if use_argv_0 and argv0:
        return os.path.basename(argv0)
    return u'Anki'

def str_sys_argv():
    retv = ''
    for nextel in sys.argv[1:]:
        retv += ' ' + unicode(nextel)
    return retv

class DeckNamer(object):
    """Functions to set the title to the deck name in Anki2 """

    def __init__(self):
        self.prog_name = get_prog_name()
        self.profile_string = u''
        self.deck_name = u''
        self.subdeck_name = u''

    def get_deck_name(self):
        """Return the deck name"""
        try:
            self.deck_name = mw.col.decks.current()['name']
        except AttributeError:
            self.deck_name = u''
        self.deck_name = self.deck_name.replace('::',' | ')
        self.subdeck_name = self.deck_name
        return self.deck_name

    def get_profile_string(self):
        """
        Return the profile name.

        When there is more than one profile, return that name,
        together with the title separator.
        """
        if len(mw.pm.profiles()) > 1 and mw.pm.name:
            self.profile_string = mw.pm.name
        else:
            self.profile_string = u''
        return self.profile_string

    def deck_browser_title(self):
        """Set the window title when we are in the deck browser."""
        mw.setWindowTitle(unicode(self.get_profile_string()) + 
            title_separator + 
            unicode(self.prog_name) + 
            unicode(str_sys_argv()) +
            '')

    def overview_title(self):
        """Set the window title when we are at the overview."""
        mw.setWindowTitle(
                          unicode(self.profile_string) + 
                          title_separator +
                          unicode(self.get_deck_name()) + 
                          '')

    def card_title(self):
        """Set the window title when we are reviewing."""
        self.overview_title()
        old_subdeck_name = self.subdeck_name
        self.subdeck_name = ""
        if hasattr(mw.reviewer.card,'did'): # AttributeError: 'NoneType' object has no attribute 'did'
            self.subdeck_name = mw.col.decks.get(mw.reviewer.card.did)['name']
            # in case there are no new or due cards, queue == 1 or 3 only (learning or day-learning) 
        self.subdeck_name = self.subdeck_name.replace('::',' | ')
        #showInfo(old_subdeck_name + ' $$ ' + self.subdeck_name)
        #if old_subdeck_name == self.subdeck_name:
        #    return
        
        #showWarning(self.deck_name + ' ;; ' + self.subdeck_name)
        # в колодах от Анки 1.2 имя подколоды не приходит!!!

        tags_list = ''
        for next_tag in mw.reviewer.card.note().tags:
            tags_list += ' %s'%next_tag
        tags_list = tags_list.strip()
        if len(tags_list):
            tags_list = ' { '+tags_list+' } '

        #if self.subdeck_name == self.deck_name:
        #    self.overview_title()
        #    return
        sd = self.subdeck_name[(len(self.deck_name) + 2):]
        tmp = unicode(_("Cloze") if mw.reviewer.card.model()['type'] == MODEL_CLOZE else _("Basic"))
        temp = unicode(mw.reviewer.card.model()['name'])
        tempo = (tmp +' | '+ temp) if tmp!=temp else tmp
        tmpl = unicode(mw.reviewer.card.template()['name'])
        mess = '' +\
            unicode(self.profile_string) +\
            unicode(title_separator) +\
            unicode( subdeck_format.format(\
                parent=self.deck_name,\
                child=sd) if len(sd) else unicode(self.get_deck_name()) ) +\
            ' ('+ tempo +') ' +\
            (tmpl if not (tmpl == tempo or tmpl == temp or tmpl == tmp) else '') +\
            tags_list
        mw.setWindowTitle(mess)

if A['DECK_NAME_IN_TITLE'][0]:
    deck_namer = DeckNamer()

    mw.deckBrowser.show = wrap(mw.deckBrowser.show, deck_namer.deck_browser_title)
    mw.overview.show = wrap(mw.overview.show, deck_namer.overview_title)
    #mw.reviewer.show = wrap(mw.reviewer.show, deck_namer.card_title)
    addHook("showQuestion", deck_namer.card_title)

    #if show_subdeck:
    #   addHook('showQuestion', deck_namer.card_title)

#################################################################################################

# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-rebuild-all

def rebuildAllDecks():
    dynDeckIds = [ d["id"] for d in mw.col.decks.all() if d["dyn"] ]
    mw.checkpoint("rebuild {0} decks".format(len(dynDeckIds)))
    mw.progress.start()
    [ mw.col.sched.rebuildDyn(did) for did in dynDeckIds ]
    mw.progress.finish()
    #showInfo('<i>Rebuild All Filtered Decks</i> done.')
    mw.reset()

def _addButton(self):
    # There's no clean way to add a button, so hack it in. :(
    button = "<button "+(" title=' Rebuild All '" if B['B11_BUTTON_TITLES'][0] else "")+" onclick='py.link(\"rebuild\");'>" + _(u'Rebuild All') + "</button>"
    html = self.bottom.web.page().mainFrame().toHtml()
    html = re.sub("</button></td>", u"</button>{0}</td>".format(button), html)
    self.bottom.draw(html)

if A['REBUILD_THEM_ALL'][0]:
    rebuild_all_action = QAction(mw)
    rebuild_all_action.setText("Перестроить &ВСЕ фильтр-колоды" if lang == 'ru' else "&Rebuild All Filtered Decks")
    rebuild_all_action.setShortcut(QKeySequence(HOTKEY['Rebuild_Them_All'][0]))
    if A['ANKI_MENU_ICONS'][0]:
        rebuild_all_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'rebuild_all.png')))
    mw.connect(rebuild_all_action, SIGNAL("triggered()"), rebuildAllDecks)
    #mw.form.menuTools.addAction(rebuild_all_action)
    mw.form.menuTools.insertAction(mw.form.actionCreateFiltered, rebuild_all_action)

#################################################################################################

# Copyright 2013 Thomas TEMPE <thomas.tempe@alysse.org>
#  strikethrough.py
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from aqt.editor import Editor

def toggleStrike(self):
    self.web.eval("setFormat('strikethrough');")

# Power Create lists ordered unordered and indented
# Written by Daniel Mankarios in 2013 <daniel.mankarios@uqconnect.edu.au>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

def toggleOList(self):
    self.web.eval("document.execCommand('insertOrderedList', false, %s);"
                % json.dumps(self.web.selectedText()))

def toggleUList(self):
    self.web.eval("document.execCommand('insertUnorderedList', false, %s);"
                % json.dumps(self.web.selectedText()))

def indentList(self):
    self.web.eval("document.execCommand('indent', false, %s);"
                % json.dumps(self.web.selectedText()))

def myButtons(self):
    self._addButton("mybutton", lambda s=self: toggleStrike(self),
                    text=u"s\u0336", tip="Зачёркивание ("+HOTKEYS['strike'][0]+")" if lang == 'ru' else "Strikethrough ("+HOTKEYS['strike'][0]+")", key=HOTKEYS['strike'][0])

    self._addButton(
        "OlistButton", lambda s=self: toggleOList(self),
        text=u"O", tip="Упорядоченный список ("+HOTKEYS['ordered'][0]+")" if lang == 'ru' else "Ordered List ("+HOTKEYS['ordered'][0]+")", key=HOTKEYS['ordered'][0])

    self._addButton(
        "UlistButton", lambda s=self: toggleUList(self),
        text=u"U", tip="Неупорядоченный список ("+HOTKEYS['unordered'][0]+")" if lang == 'ru' else "Unordered List ("+HOTKEYS['unordered'][0]+")", key=HOTKEYS['unordered'][0])

    self._addButton(
        "indentButton", lambda s=self: indentList(self),
        text=u"In", tip="Отступ списка ("+HOTKEYS['indent'][0]+")" if lang == 'ru' else "Indent List ("+HOTKEYS['indent'][0]+")", key=HOTKEYS['indent'][0])

if A['POWER_CREATE_LISTS'][0]:
   Editor.toggleStrike = toggleStrike

   Editor.toggleOList = toggleOList
   Editor.toggleUList = toggleUList
   Editor.indentList = indentList

   Editor.setupButtons = wrap(Editor.setupButtons, myButtons)

# • Alternative hotkeys to cloze selected text in Add or Editor window
# https://ankiweb.net/shared/info/2074653746
# _Alternative_hotkeys_to_cloze_selected_text_in_Add_or_Editor_window.py

akita_CtrlSpace     = HOTKEYS["nextCloze"][0] #"Ctrl+Space"     # Ctrl+Shift+C
akita_CtrlAltSpace  = HOTKEYS["sameCloze"][0] #"Ctrl+Alt+Space" # Ctrl+Alt+Shift+C
akita_CtrlShiftX    = HOTKEYS["showHTML"][0]  #"F4"             # Ctrl+Shift+X

#from aqt.editor import *

def akita_setupButtonz(self):
    s = QShortcut(
        QKeySequence(akita_CtrlSpace), self.parentWindow)
    s.connect(s, SIGNAL("activated()"), self.onCloze)

    s = QShortcut(
        QKeySequence(akita_CtrlAltSpace), self.parentWindow)
    s.connect(s, SIGNAL("activated()"), self.onCloze)

    s = QShortcut(
        QKeySequence(akita_CtrlShiftX), self.widget)
    s.connect(s, SIGNAL("activated()"), self.onHtmlEdit)

if A['CLOZE_EDITOR_HOTKEYS'][0]:
    aqt.editor.Editor.setupButtons = wrap(aqt.editor.Editor.setupButtons, akita_setupButtonz)

#################################################################################################
# Customizable Congratulations Message
# https://ankiweb.net/shared/info/856960187
#
# This plugin is provided as-is without any additional support. 
#
# To customize, edit the CUSTOM_CONGRAT_MSG line in Custom_Congrats_Message.py with html. 
# This can be done by Tools->Add-ons->Customizable_Congratulations_Message->Edit
# Umlaute 
# Hey - cool gimmick!
# would be nice, if it would support Umlaute äöü etc.
# thx. cheers. 
# How to use Unicode characters
# Does what it says.
# To the reviewer who said they wanted to use umlauts (or any other non-Latin characters), 
#    you can do this as well, you just have to make two changes:
# 1. At the very top of the file, add the line
#    #-*- coding: utf-8 -*-
# 2. In the line with the string to modify, add a letter 'u' in front of the opening quotation mark, like so:
#    CUSTOM_CONGRAT_MSG = u"This is my ĉöngrátulatiǒns message" 
from anki.sched import Scheduler

def customMsg(self):
    return ( custom_msg + "<br><br>" + self._nextDueMsg())

if A['CUSTOM_CONGRAT_MSG'][0]:
   for lbls in CUSTOM_CONGRAT_MSG:
    if lbls[0] == lang:
       custom_msg = lbls[1]
       Scheduler.finishedMsg = customMsg

######################################################################################################
# CHK_00_MORE_OVERVIEW_STATS.py
# Author: Calumks <calumks@gmail.com>
# 2013-01-02 The card count does not include the cards in subdecks. -- 02/01/2013 Fixed card count bug

# Get Overview class
from aqt.overview import Overview

# Replace _table method
def table(self):
    cardsUnseen = self.mw.col.db.first("""
select
sum(case when queue=0 then 1 else 0 end) -- new
from cards where did in %s""" % self.mw.col.sched._deckLimit())

    cardsSuspended = self.mw.col.db.first("""
select
sum(case when queue = -1 then 1 else 0 end) -- new
from cards where did in %s""" % self.mw.col.sched._deckLimit())

    cardsBuried = self.mw.col.db.first("""
select
sum(case when queue = -2 then 1 else 0 end) -- new
from cards where did in %s""" % self.mw.col.sched._deckLimit())

    cardsTotal = self.mw.col.db.first("""
select count(id) from cards
where did in %s """ % self.mw.col.sched._deckLimit())

    cardsTotalReviews = self.mw.col.db.scalar("""
select count() from cards where did in %s and queue > 0
and due < ?""" % self.mw.col.sched._deckLimit(), self.mw.col.sched.today+1)

    counts = list(self.mw.col.sched.counts())
    finished = not sum(counts)
    for n in range(len(counts)):
        if B['B04_HIDE_BIG_NUMBERS'][0] and counts[n] > B['B04_HIDE_BIG_NUMBER'][0]: # counts[n] == 1000:
            counts[n] = "%s+" % (B['B04_HIDE_BIG_NUMBER'][0]) # "1000+" 
    but = self.mw.button
    if finished:
        return '<div style="white-space: pre-wrap;">%s</div>' % (
            self.mw.col.sched.finishedMsg())
    else:
        line1 = '''
    <table width=300 cellpadding=5>
    <tr><td align=center valign=top>
    <table cellspacing=5>'''
        if B['B00_MORE_OVERVIEW_STATS'][0] == 1:
           line2 = "" # "<tr><td></td><td></td></tr>"
           #line2 = '''<tr><td>%s:</td><td align=right style="font-weight:bold;color:silver;white-space:nowrap;"><font color=#33f>%s</font> + <font color=#c33>%s</font> + <font color=#090>%s</font></td></tr>''' % ( _('Today'), counts[0], counts[1], counts[2] ) # _("Due today")
        else:
           line2 = '''
    <tr><td style="white-space:nowrap;">%s:</td><td align=right style="color:#33f;font-weight:bold;">&nbsp;%s</td></tr>
    <tr><td style="white-space:nowrap;">%s:</td><td align=right style="color:#c33;font-weight:bold;">&nbsp;%s</td></tr>
    <tr><td style="white-space:nowrap;">%s:</td><td align=right style="color:#090;font-weight:bold;">&nbsp;%s</td></tr>''' % (
   _('New'), counts[0], 
   _('Learning'), counts[1], 
   _('To Review'), counts[2] )
        if (B['B00_MORE_OVERVIEW_STATS'][0] == 1):
            line3 = ""
        else:
            line3 = '''
    <tr><td colspan=2><hr></td></tr>
    <tr><td style="white-space:nowrap;">%s:</td><td align=right style="color:#DA70D6;">&nbsp;%s</td></tr>
    <tr><td style="white-space:nowrap;">%s:</td><td align=right style="color:#c90;">&nbsp;%s</td></tr>
    <tr><td style="white-space:nowrap;">%s:</td><td align=right style="color:#960;">&nbsp;%s</td></tr>
    <tr><td colspan=2><hr></td></tr>
    <tr><td style="white-space:nowrap;">%s:</td><th align=right>&nbsp;%s</font></th></tr>''' % ( 
    _("Unseen"), cardsUnseen[0] if cardsUnseen[0] <= B['B04_HIDE_BIG_NUMBER'][0] \
     or ((cardsUnseen[0] > B['B04_HIDE_BIG_NUMBER'][0]) and not B['B04_HIDE_BIG_NUMBERS'][0]) else "%s+" % (B['B04_HIDE_BIG_NUMBER'][0]),
    _("Suspended"), cardsSuspended[0] if cardsSuspended[0] <= B['B04_HIDE_BIG_NUMBER'][0] \
     or ((cardsSuspended[0] > B['B04_HIDE_BIG_NUMBER'][0]) and not B['B04_HIDE_BIG_NUMBERS'][0]) else "%s+" % (B['B04_HIDE_BIG_NUMBER'][0]),
    _Buried, cardsBuried[0] if cardsBuried[0] <= B['B04_HIDE_BIG_NUMBER'][0] \
     or ((cardsBuried[0] > B['B04_HIDE_BIG_NUMBER'][0]) and not B['B04_HIDE_BIG_NUMBERS'][0]) else "%s+" % (B['B04_HIDE_BIG_NUMBER'][0]),
    _("Total cards"), cardsTotal[0] if cardsTotal[0] <= B['B04_HIDE_BIG_NUMBER'][0] \
     or ((cardsTotal[0] > B['B04_HIDE_BIG_NUMBER'][0]) and not B['B04_HIDE_BIG_NUMBERS'][0]) else "%s+" % (B['B04_HIDE_BIG_NUMBER'][0]) )
        line3 += ''' </table>
    </td><td align=center>%s</td></tr></table>''' % ( but("study", _("Study Now"), id="study") )
        return line1 + line2 + line3

# Total reviews == Due

original_table = Overview._table

if B['B00_MORE_OVERVIEW_STATS'][0] > 0 and B['B00_MORE_OVERVIEW_STATS'][0] < 3:
   Overview._table = table

#######################################################################
# https://ankiweb.net/shared/info/531984586
# More Overview Stats 2
# This is god-tier. 

"""

Statistics add-on for Anki v1.9. 
It's based on the nice "More Overview Stats" add-on by Calumks but shows more (and different) values. 
You can find a description of hidden options and the change log at the beginning of the source code. 
For bugs or comments, feel free to contact me. 

Note: this add-on may cause the overview page to display more slowly on large decks and/or slower computers.

More Overview Stats 2
=====================
Statistics add-on for Anki -- based on "More Overview Stats" by
Calumks <calumks@gmail.com>

Copyright (c) 2014 Martin Zuther (http://www.mzuther.de/)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Thank you for using free software!

USAGE
=====
This statistics add-on for Anki is based on the nice "More Overview
Stats" add-on by Calumks but shows more (and different) values.

To change the behaviour of this add-on, create a JSON file called
'More_Overview_Stats_2.json' in your profile folder.  When you edit
this file, please make sure you save the JSON file using a compatible
encoding such as UTF-8.

In case you don't like to see the stats on finished decks, copy the
following lines to your JSON file:

   {
      "options": {
         "show_table_for_finished_decks": false
      }
   }

There is another (advanced) option: I use Anki to learn vocabulary,
and some of my decks have one card per note, while others have two
cards per note.  To watch my progress, I want to know the (somewhat
virtual) number of *notes* instead of the cards.

To achieve this, edit the JSON file along these lines:

   {
      "options": {
         "show_table_for_finished_decks": true
      },
      "note_correction_factors": {
         "Spanisch": 2,
         "Türkisch": 2,
         "Türkisch::Word Pool": 1
      }
   }

If everything works fine, this add-on will compare the current deck
name with the entries and use the FACTOR given for the longest match.

For the example above, all Spanish and Turkish decks will divide the
card numbers by 2, while the subdeck "Türkisch::Word Pool" will show
the original card numbers.  Please note that the card numbers for new,
learning and review will NOT be modified so that you can still monitor
your learning progress.

Enjoy!

HISTORY
=======
version 1.9:
* now works correctly with empty decks (thanks to Jonte!)
version 1.8:
* changed displayed values (unseen / suspended)
* format display using CSS
version 1.7:
* move hidden variable from source code to JSON file
version 1.6:
* correct note numbers by deck-specific factors
version 1.5:
* hide new/learning/review block when deck is finished
version 1.4:
* changed displayed values (learned)
version 1.3:
* support Unicode in localisations
version 1.2:
* align table regardless of font
version 1.1:
* show table even if deck is finished
version 1.0:
* initial commit
"""

# from datetime import date, datetime, time, timedelta 

def dd4():
    if mw.col.crt:
        startHour = datetime.fromtimestamp(mw.col.crt).hour
    else:
        startHour = 4
    d0 = datetime.now() 
    d4 = datetime(d0.year, d0.month, d0.day, startHour, 0, 0)
    d4 += timedelta(days=(1 if d0.hour >= startHour else 0))
    return (d4 - datetime(1970,1,1)).total_seconds()

def overview_table(self):
    json_file = os.path.join(self.mw.pm.profileFolder(),
                             'More_Overview_Stats_2.json')

    if os.path.isfile(json_file):
        with open(json_file, mode='r') as f:
            settings = json.load(f)
    else:
        settings = {}

    current_deck_name = self.mw.col.decks.current()['name']

    correction_for_notes = 1
    last_match_length = 0

    if 'note_correction_factors' in settings:
        for fragment, FACTOR in settings['note_correction_factors'].items():
            if current_deck_name.startswith(fragment):
                if len(fragment) > last_match_length:
                    correction_for_notes = int(FACTOR)
                    last_match_length = len(fragment)

        # prevent division by zero and negative results
        if correction_for_notes <= 0:
            correction_for_notes = 1

    total, mature, young, unseen, suspended, buried, lrn, lrn1, lrn4, due = self.mw.col.db.first( 
        '''
          select
          -- total
          count(id),
          -- mature
          sum(case when queue = 2 and ivl >= 21
                   then 1 else 0 end),
          -- young / learning
          sum(case when queue in (1, 3) or (queue = 2 and ivl < 21)
                   then 1 else 0 end),
          -- unseen
          sum(case when queue = 0
                   then 1 else 0 end),
          -- suspended
          sum(case when queue = -1
                   then 1 else 0 end),
          -- buried
          sum(case when queue = -2
                   then 1 else 0 end),
          -- lrn
          sum(case when (queue = 1 or queue = 3) and due <= {1}
                   then round(left / 1000) else 0 end),
          -- lrn1 # mw.col.conf['collapseTime'] mins * 60 secs
          sum(case when (queue = 1 or queue = 3) and due <= {1}
                   then 1 else 0 end),
          -- lrn4
          sum(case when (queue = 1 or queue = 3) and due <= {3}
                   then 1 else 0 end),
          -- due
          sum(case when queue = 2 and due < {2}
                   then 1 else 0 end)
          from cards where did in {0:s}
        '''.format( self.mw.col.sched._deckLimit(), round(time.time() + mw.col.conf['collapseTime']*60), \
        self.mw.col.sched.today+1, round(dd4() + mw.col.conf['collapseTime']*60) ) )

    if not total:
        return u'<p>No cards found.</p>'

    scheduled_counts = list(self.mw.col.sched.counts())
    deck_is_finished = not sum(scheduled_counts)

    cards = {}

    cards['mature'] = mature / int(correction_for_notes)
    cards['young'] = young / int(correction_for_notes)
    cards['unseen'] = unseen / int(correction_for_notes)
    cards['suspended'] = suspended / int(correction_for_notes)
    cards['buried'] = buried / int(correction_for_notes)

    cards['total'] = total / int(correction_for_notes)
    cards['learned'] = cards['mature'] + cards['young']

    cards['new'] = scheduled_counts[0]
    cards['learn'] = lrn
    cards['lrn1'] = lrn1 # str(lrn1)
    cards['learning'] = scheduled_counts[1]
    cards['lrn4'] = lrn4 # str(lrn4)
    cards['review'] = scheduled_counts[2]
    cards['due'] = cards['learn'] + cards['review'] # due

    cards_percent = {}

    cards_percent['mature'] = cards['mature'] * 1.0 / cards['total']
    cards_percent['young'] = cards['young'] * 1.0 / cards['total']
    cards_percent['unseen'] = cards['unseen'] * 1.0 / cards['total']
    cards_percent['suspended'] = cards['suspended'] * 1.0 / cards['total']
    cards_percent['buried'] = cards['buried'] * 1.0 / cards['total']

    cards_percent['total'] = 1.0
    cards_percent['learned'] = cards['learned'] * 1.0 / cards['total']

    cards_percent['new'] = cards['new'] * 1.0 / cards['total']
    cards_percent['learning'] = cards['learning'] * 1.0 / cards['total']
    cards_percent['learn'] = cards['learn'] * 1.0 / cards['total']
    cards_percent['review'] = cards['review'] * 1.0 / cards['total']
    cards_percent['due'] = cards['due'] * 1.0 / cards['total']

    for card in cards:
        cards[card] = int(cards[card])
    cardz={}

    # percents are calculated from correct values
    for key, value in cards.iteritems(): # for Python2 only, Python3 does it another way.
        #if B['B04_HIDE_BIG_NUMBERS'][0] and value > B['B04_HIDE_BIG_NUMBER'][0]:
        #    cards[key] = str(B['B04_HIDE_BIG_NUMBER'][0])+"+"
        #else:
        #    cards[key] = str(value)
        cardz[key] = nonzeroColour(cards[key],"default",False)

    labels = {}

    labels['new'] = _('New')
    labels['learning'] = _('Learning') # + ' ' + str(round(dd4()))
    labels['learn'] = _('Learn') # + ' ' + str(round(time.time()))
    labels['review'] = _('To Review')
    labels['due'] = _('Due')

    labels['unseen'] = _('Unseen')
    labels['suspended'] = _('Suspended')
    labels['buried'] = _Buried

    labels['mature'] = _('Mature')
    labels['young'] = _('Young')
    labels['learned'] = _('Mature') + ' + ' + _('Young') # _('Learned')

    labels['total'] = _('Total')

    for key in labels:
        labels[key] = u'{:s}:'.format(labels[key])

    button = self.mw.button

    output_table = '''
      <style type="text/css">
        hr {
            height: 1px;
            border: none;
            border-top: 1px solid #aaa;
        }
        td {
            vertical-align: top;
        }
        td.row1, td.hr {
            text-align: left;
            padding-left: 1.2em;
        }
        td.row2 {
            text-align: right;
            padding-left: 1.2em;
            padding-right: .2em;
        }
        td.row3, td.row4 {
            text-align: right;
        }
        td.row4, td.hr {
            padding-right:1.2em;
        }
        td.new {
            font-weight: bold;
            color: #33f; /* #00a; */
        }
        td.learning {
            color: #c33; /* #a00; */
        }
        td.learn {
            font-weight: bold;
            color: #c33; /* #a00; */
        }
        td.review {
            font-weight: bold;
            color: #090; /* #080; */
        }
        td.percent {
            font-weight: normal;
            color: #888;
        }
        td.mature {
            font-weight: normal;
            color: #080; 
        }
        td.young {
            font-weight: normal;
            color: #3c3; 
        }
        td.learned {
            font-weight: normal;
            color: #0a0; 
        }
        td.due {
            font-weight: normal;
            color: #999; 
        }
        td.unseen {
            font-weight: normal;
            color: #DA70D6; /* #a00; */
        }
        td.suspended {
            font-weight: normal;
            color: #c90; /* #a70; */
        }
        td.buried {
            font-weight: normal;
            color: #960; /* #a70; */
        }
        td.total {
            font-weight: bold;
            color: default; /* #000; */
        }
        .G { background-color: #e6e6e6; } 
        .night .G { background-color:  #444; }
        table { 
            border-spacing: 0px; 
        }
      </style>
    '''

    if cards['learning']==cards['learn']:
       output_table += ''' <style> .L { display: none; } </style> '''

    output_table += '''
      <table cellspacing="2">
    '''

    if not deck_is_finished:
        output_table += '''
            <tr>
              <td class="row1">{label[new]:s}</td>
              <td class="row2 new">{cards[new]:s}</td>
              <td></td>
              <td class="row4 percent">{percent[new]:.0%}</td>
            </tr>
            <tr class="L">
              <td class="row1">{label[learning]:s}</td>
              <td class="row2 learning">{cards[learning]:s}</td>
              <td class="learning" style="text-align:left;"><sub>{cards[lrn4]}</sub></td>
              <td class="row4 percent">{percent[learning]:.0%}</td>
            </tr>
            <tr class="G">
              <td class="row1" style="color:#999;">{label[learn]:s}</td>
              <td class="row2 learn">{cards[learn]:s}</td>
              <td class="learn" style="text-align:left;"><sub>{cards[lrn1]}</sub></td>
              <td class="row4 percent">{percent[learn]:.0%}</td>
            </tr>
            <tr>
              <td class="row1">{label[review]:s}</td>
              <td class="row2 review">{cards[review]:s}</td>
              <td></td>
              <td class="row4 percent">{percent[review]:.0%}</td>
            </tr>
            <tr>
              <td class="row1">{label[due]:s}</td>
              <td class="row2 due">{cards[due]:s}</td>
              <td></td>
              <td class="row4 percent">{percent[due]:.0%}</td>
            </tr>
        '''.format(label=labels,
                   cards=cardz,
                   percent=cards_percent)

    if (cards['unseen'] + cards['suspended'] + cards['buried']):
      output_table += '''
            <tr>
              <td colspan="4" class="hr"><hr /></td>
            </tr>
        <tr>
          <td class="row1">{label[unseen]:s}</td>
          <td class="row2 unseen">{cards[unseen]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[unseen]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[suspended]:s}</td>
          <td class="row2 suspended">{cards[suspended]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[suspended]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[buried]:s}</td>
          <td class="row2 buried">{cards[buried]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[buried]:.0%}</td>
        </tr>
      '''.format(label=labels,
               cards=cardz,
               percent=cards_percent)

    output_table += '''
        <tr>
          <td colspan="4" class="hr"><hr /></td>
        </tr>
        <tr>
          <td class="row1">{label[mature]:s}</td>
          <td class="row2 mature">{cards[mature]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[mature]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[young]:s}</td>
          <td class="row2 young">{cards[young]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[young]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[learned]:s}</td>
          <td class="row2 learned">{cards[learned]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[learned]:.0%}</td>
        </tr>
        <tr>
          <td colspan="4" class="hr"><hr /></td>
        </tr>
        <tr>
          <td class="row1">{label[total]:s}</td>
          <td class="row2 total">{cards[total]:s}</td>
              <td></td>
          <td class="row4 percent">{percent[total]:.0%}</td>
        </tr>
    '''.format(label=labels,
               cards=cardz,
               percent=cards_percent)

    output = ''

    if deck_is_finished:
        if (not 'options' in settings) or (settings['options'].get(
                'show_table_for_finished_decks', True)):
            output += output_table
            output += '''
              </table>
              <hr style="margin: 1.5em 0; border-top: 1px dotted #888;" />
            '''

        output += '''
          <div style="white-space: pre-wrap;">{:s}</div>
        '''.format(self.mw.col.sched.finishedMsg())
    else:
        suma = cards['new']+cards['learn']+cards['review']
        summa = cards['new']+cards['learning']+cards['review']
        #showWarning(str(suma)+' '+unicode(summa))
        #output += (output_table if suma==0 else "") + '''
        if suma>0:
          output += '''
            <tr>
              <td colspan="4" style="text-align: center; padding-top: 0.6em;">{button:s}</td>
            </tr>
          '''.format(button=(button('study', _('Study Now'), id='study') if summa>0 else button('decks', _('Decks'), id='study'))) 
        #                                                                                                          id='study' to get focus
        if summa > 0:
            output += (output_table if summa > 0 else "") + '''
            <tr>
              <td colspan="4" style="text-align: center; padding-top: 0.6em;">{button:s}</td>
            </tr>
        '''.format(button=(button('decks', '<small>'+_('Decks')+'</small>', id='study'))) 
        output += "</table>"

    return output

# replace _table method
if B['B00_MORE_OVERVIEW_STATS'][0] == 3:
   Overview._table = overview_table

def overview_init():
    if B['B00_MORE_OVERVIEW_STATS'][0] > 0 and B['B00_MORE_OVERVIEW_STATS'][0] < 3:
       Overview._table = table
    elif B['B00_MORE_OVERVIEW_STATS'][0] == 0:
       Overview._table = original_table
    else:
       Overview._table = overview_table

# -- 

#self.reviewer._css = 
'''
hr { color: maroon; background-color:#def; margin: .5em 2.5em;  }
body { margin:1.5em; padding: 2em; border: solid 1px lime; }
img { max-width: 95%; max-height: 95%; }
.marked { position:fixed; right: 7px; top: 7px; display: none; }
#typeans { width: 100%; }
.typeGood { background: #0f0; }
.typeBad { background: #f00; }
.typeMissed { background: #ccc; }'''

# -- 

#######################################################################
# https://ankiweb.net/shared/info/248074683
# Removes Empty Note Types
#  After some time you pile up a lot of note types that never get deleted? 
#   This plugin takes care of it! After installing,
#    click on Tools -> Remove Empty Note Types. 
#     This might take a few seconds.

##########################################################################
# https://ankiweb.net/shared/info/3867500866
# Deleting Reduant Configurations -- Redundant, BTW
#  Delete all configurations inside the collections,
#   except the one used by decks and the original one.
# Written by Sara Jakša sarajaksa@gmail.com

if A['REMOVES_EMPTY'][0]:
  from aqt.deckconf import DeckConf

  class ConfigurationDeletions():

    def __init__(self):
        self.mw = mw
        self.allDecks = mw.col.decks.all()
        self.allConf = mw.col.decks.allConf()

    def countGroup(self, conf4Del):
        counter = 0
        for conf in conf4Del:
            conf = self.findConfigurationFromId(conf)
            if not conf['id'] == 1:
                counter += 1
        return counter

    #Odstrani configuracije
    def remGroup(self, conf4Del):
        counter = 0
        #deck = self.findDeckFromConfiguration(self.findConfigurationFromId(1))
        #configuration = DeckConf(mw, deck)
        for conf in conf4Del:
            conf = self.findConfigurationFromId(conf)
            if not conf['id'] == 1:
                counter += 1
                mw.col.decks.remConf(conf['id'])
                #configuration.loadConfs()
        return counter

    def findDeckFromConfiguration(self, conf):
        for deck in self.allDecks:
            if deck[u'conf'] == conf:
                return deck

    #Finds the ID of all configurations
    def findIdConfigurations(self):
        confId = set()
        for conf in self.allConf:
            confId.add(conf[u'id'])
        return confId

    #Find if it is a filter deck
    def filterDeck(self, deck):
        if deck[u'dyn']:
            return True
        return False

    #Finds all the decks and their's configurations
    def findDeckIdConfiguration(self):
        deckConfId = set()
        for deck in self.allDecks:
            if self.filterDeck(deck):
                return None
            deckConfId.add(deck['conf'])
        return deckConfId

    #finds all configuration, with no deck
    def ophranConfigurations(self, confId, deckId):
        conf4Del = []
        for ID in confId:
            if ID not in deckId:
                conf4Del.append(ID)
        return conf4Del

    #From confId find configuration
    def findConfigurationFromId(self, Id):
        for conf in self.allConf:
            if conf['id'] == Id:
                return conf

  def remDupes():
    counter = 0
    mw.window().checkpoint(_("Delete Empty Note Types"))
    for model in mw.col.models.all():
        if mw.col.models.useCount(model) == 0:
            if len(mw.col.models.all())>1:
                counter += 1
                mw.col.models.rem(model)
    #mw.window().requireReset()
    return counter

  def countDupes():
    counter = 0
    for model in mw.col.models.all():
        if mw.col.models.useCount(model) == 0:
            counter += 1
    return counter

  def confStart():
    deletion = ConfigurationDeletions()
    cntDel = deletion.countGroup(deletion.ophranConfigurations(deletion.findIdConfigurations(), deletion.findDeckIdConfiguration()))
    cntDup = countDupes()
    if (cntDel+cntDup):
        if askUser((u" Будут удалены: \n пустые типы записей - {} \n пустые группы настроек колод - {} "
            if lang == 'ru' else "Would be deleted \n empty note types - {}  \n options groups - {} ").format(cntDup,cntDel), defaultno = True): # true - global name not found

            cntDel = deletion.remGroup(deletion.ophranConfigurations(deletion.findIdConfigurations(), deletion.findDeckIdConfiguration()))
            cntDup = remDupes()
            if cntDup + cntDel:
                if lang == 'ru':
                    tooltip(u" Удалены пустые \n типы записей - %d \n группы настроек колод - %d " % (cntDup, cntDel) )
                else: # showInfo showWarning showCritical
                    tooltip(" %d empty note types deleted.\n %d empty options groups deleted." % (cntDup, cntDel) )
    else:
        tooltip(u'Пустые типы записей или группы настроек колод не найдены.' 
            if lang == 'ru' else "There are no empty note types or options groups to delete.")

    if mw.onCheckDB():
       mw.onCheckMediaDB()
       mw.onEmptyCards()

if A['REMOVES_EMPTY'][0]:
    remove_action = QAction(u"&Удалить пустые типы записей, метки и группы настроек колод" if lang == 'ru' else "&Delete Empty Options Groups, Tags and Notes Types", mw)
    if A['ANKI_MENU_ICONS'][0]:
        remove_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'warning.png')))
    remove_action.setShortcut(HOTKEY['delete_them_all'][0]) 
    mw.connect(remove_action, SIGNAL("triggered()"), confStart)

    #mw.form.menuTools.addAction(remove_action)
    mw.form.menuTools.insertAction(mw.form.actionFullDatabaseCheck,remove_action)

##########################################################################
# Clickable Tags on Reviewer
# https://ankiweb.net/shared/info/1321188674
# Clickable_Tags_on_Reviewer.py
# 28.01.2016

"""
Clickable_Tags add-on 0.1 alpha release- inspired by Dybamic_Tags add-on
The styles used here are from Power format pack add-on
Copyright: Abdolmahdi Saravi, 2013 <amsaravi@yahoo.com>
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
This add-on Displays the Cards Tag in style of keyboard keys that has the 
ability to click on them witch opens the anki browser and lists the cards that match clicked tag.
You can change the style of tags by editing the code.
You can also use {{Tags}} in card template to position the tags on the card. by default if you don't use the
{{Tags}} in your Cards the add-on puts the tags before any content of the card. you can change this behavior
by setting the variable TAG_IN_ALL_CARDS to False
Also you can use this add-on as a global css injector. css styles that is defined here are visible on all note types
if you Double Click on a tag within viewer the related Tags within current Deck will be showed
Good Luck
https://bitbucket.org/amsaravi/ankiaddons
"""

from aqt import DialogManager  # we need it to fix the anki behavior not to deal with minimized state of window
from anki.template import Template

"""
    -webkit-user-select: none !important; /* to prevent selecting text on dblclick */
    user-select: none !important;
    -khtml-user-select: none !important;
    -webkit-touch-callout: none !important; /* all these styles doesn't work in Anki */
"""

kbd_css = """
kbd {
    box-shadow: inset 0px 1px 0px 0px #ffffff;
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0.05, #f9f9f9), color-stop(1, #e9e9e9) );
    background-color: #f9f9f9; color: #333;
    border-radius: 4px;
    border: 1px solid #dcdcdc;
    display: inline-block;
    font-size:15px;
    height: 15px;
    line-height: 15px;
    padding:4px 4px 6px;
    margin:5px;
    text-align: center;
    text-shadow: 1px 1px 0px #999;
    cursor: pointer; cursor: hand; 
} #Tags {
    position: fixed; bottom: .1em; left: 1em; right: 1em; max-height: 3.3em; overflow: auto;
} body {
    #padding-bottom: 4em !important;
}
"""

java_script = """
<script type="text/javascript">
var timer = 0;
var delay = 200;
var prevent = false;
function click_func(tags) {
    timer = setTimeout(function() {
        if (!prevent) {
            py.link(tags);
        }
        prevent = false;
    }, delay);
}

function dblclick_func(tags_deck) {
    clearTimeout(timer);
    prevent = true;
    py.link(tags_deck);
}

</script>
"""

TAG_MARK = "{{info:Tags}}"
FRNT_SIDE = "{{FrontSide}}"

TAG_IN_ALL_CARDS = False    #uncomment and put the fields in your cards manually
#TAG_IN_ALL_CARDS = True    #uncomment to put tags automatically in the beginning of each card

def tagClicklinkHandler(self, url):
    browser = None

    if url.startswith("tagclick_"):             # click
        tag = url.split("tagclick_")[-1]
        browser = aqt.dialogs.open("Browser", self.mw)
        browser.setFilter("tag:\"%s\" " % tag)
    elif url.startswith("_tagdbl_"):            # Ctrl+click
        dec, tag = url.split("_tagdbl_")[1:]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" card:\"%s\" " % (tag, dec))
    elif url.startswith("_tag_"):               # Shift+click
        dec, tag = url.split("_tag_")[1:]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" note:\"%s\" " % (tag, dec))
    elif url.startswith("_tagctrlshift_"):      # Ctrl+Shift+click
        dec, tag, nop = url.split("_tagctrlshift_")[1:]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" card:\"%s\" note:\"%s\" " % (tag, dec, nop))

    elif url.startswith("_tagdblclick_"):       # context
        tag = url.split("_tagdblclick_")[-1]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" deck:current " % (tag))
        #dec, tag = url.split("_tagdblclick_")[1:]
        #browser = aqt.dialogs.open("Browser", self.mw)       
        #browser.setFilter("tag:%s \"deck:%s\"" % (tag, dec))
        browser.setWindowState(browser.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    elif url.startswith("_tagctrl_"):           # Ctrl+context
        dec, tag = url.split("_tagctrl_")[1:]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" deck:current card:\"%s\" " % (tag, dec))
    elif url.startswith("_tagshift_"):          # Shift+context
        dec, tag = url.split("_tagshift_")[1:]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" deck:current note:\"%s\" " % (tag, dec))
    elif url.startswith("_tagshiftctrl_"):      # Ctrl+Shift+context
        dec, tag, nop = url.split("_tagshiftctrl_")[1:]
        browser = aqt.dialogs.open("Browser", self.mw)       
        browser.setFilter("tag:\"%s\" deck:current card:\"%s\" note:\"%s\" " % (tag, dec, nop))
    #else:
    #    oldLinkHandler(reviewer, url)

    if browser:
        browser.setWindowState(browser.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

    # Play the sound or call the original link handler.
    if url.startswith("ankiplay"):
        play(url[8:])

    if url == "rebuild":
        rebuildAllDecks()

    if ":" in url:
        (cmd, arg) = url.split(":", 1)
    else:
        cmd = url
        arg = ''

    if cmd == "study":
        my_studyDeck(self, arg)
    elif url.startswith("typeans:"):
        self.typedAnswers.append(unicode(arg))


def new_render(self, template=None, context=None, encoding=None):
    template = template or self.template
    context = context or self.context
    if context is not None:
        deck = context['Deck']
        card = context['Card']
        note = context['Type']
        tags = context['Tags'].split()
        tagStr = " ".join([ 
            ( """<kbd oncontextmenu="if(!event.ctrlKey){if (!event.shiftKey){py.link('_tagdblclick_%s')}else{py.link('_tagshift_%s_tagshift_%s')}}else{if(event.shiftKey){py.link('_tagshiftctrl_%s_tagshiftctrl_%s_tagshiftctrl_%s')}else{py.link('_tagctrl_%s_tagctrl_%s')}};return false;" """
            % (tag, note, tag, card, tag, note, card, tag) ) + 
            ( """ onclick="if (!event.ctrlKey){if (!event.shiftKey){py.link('tagclick_%s');}else{py.link('_tag_%s_tag_%s')}}else{if(event.shiftKey){py.link('_tagctrlshift_%s_tagctrlshift_%s_tagctrlshift_%s')}else{py.link('_tagdbl_%s_tagdbl_%s')}}return false;">%s</kbd>"""
            % (tag, note, tag, card, tag, note, card, tag, tag) ) for tag in tags])
        tagStr += java_script
        template, n = re.subn(TAG_MARK, tagStr, template)
        if (not n) and (template.rfind(FRNT_SIDE) == -1) and (TAG_IN_ALL_CARDS):
            template = tagStr + template    
    return old_render(self, template, context, encoding)

def kbdTags_new_css(card):
    return kbdTags_old_css(card) + "\n<style>\n%s\n</style>\n\n" % kbd_css

kbdTags_old_css = Card.css
Card.css = kbdTags_new_css

old_render = Template.render
Template.render = new_render

#function to change anki behavior of opening  minimized windows that anki doesn't deals with it
def unminimize(dlgmngr, name, *args):
    instance=old_open(dlgmngr,name, *args)
    if instance:
        instance.setWindowState(instance.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    return instance

old_open= DialogManager.open
DialogManager.open =  unminimize

def new_renderPreview(self, cardChanged=False,_old=None):    
    _old(self,cardChanged)
    if self._previewWindow:
        self._previewWeb._linkHandler=lambda url: tagClicklinkHandler(self,url)
        self._previewWeb.setLinkHandler(self._previewWeb._linkHandler)

Browser._renderPreview=wrap(Browser._renderPreview, new_renderPreview, "around")

# -- click in Preview doesn't work

#################################################################################################
# Replay buttons on card
# https://ankiweb.net/shared/info/498789867
#
# Small add-on to add replay buttons on the card itself, the way AnkiDroid does it.
# This is mostly useful when you have more than one audio file on a card;
# with this you can replay individual files. Although there isn’t that much more to say, 
# there is a manual page. Report further problems at the support site or at github.
#
# http://ospalh.github.io/anki-addons/Play%20button.html
# https://anki.tenderapp.com/discussions/add-ons
# https://github.com/ospalh/anki-addons/issues?state=open
#
# Copyright © 2013–14 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to add AnkiDroid-style replay buttons."""

import shutil

from BeautifulSoup import BeautifulSoup

from aqt.browser import DataModel
from aqt.clayout import CardLayout

sound_re = ur"\[sound:(.*?)\]"

image_re = ur'\<img src="(.*?)" \/\>'

original_arrow_name = 'replay.png'
collection_arrow_name = '_inline_replay_button.png'
hide_class_name = u'browserhide'

# Filter the questions and answers to add play buttons.
#
def play_button_filter(
        qa_html, qa_type, dummy_fields, dummy_model, dummy_data, dummy_col):
    #showTextik(qa_html,title=qa_type)

    global soundtrack_q_number, soundtrack_q_list
    global soundtrack_a_number, soundtrack_a_list
    if qa_type == 'q':
        soundtrack_q_number = 0
        soundtrack_q_list = []
    else:
        soundtrack_a_number = 0
        soundtrack_a_list = []

    #   no matches = no call
    def add_button(sound):
        """
        Add img link after the match.

        Add an img link after the match to replay the audio. 
        The title is set to "Replay" on the question side 
        to hide information or to the file name on the answer.
        """

        if not sound.group(1):
            return ""

        if not os.path.isfile(os.path.join(mw.pm.profileFolder(), "collection.media", sound.group(1))):
            return ""

        if 'q' == qa_type:
            title = _(u"Replay") + ((' &#91;sound:' + sound.group(1) + '&#93;') if A['REPLAY_BUTTONS_ON_CARD'][0] > 1 else '')
        else:
            title = sound.group(1)

        global soundtrack_q_list
        global soundtrack_a_list
        if 'q' == qa_type:
            soundtrack_q_list.append( sound.group(1) )
        else:
            soundtrack_a_list.append( sound.group(1) )
        #onAudioList()

        # -- It's return !!! --
        return """{orig}<a href='javascript:py.link("ankiplay{fn}");' \
{ttl} class="replaybutton browserhide"><span><img \
alt="play" src="{ip}" style="max-width: 32px; max-height: 1em; min-height:8px;" />\
</span></a><span style="display: none;">&#91;sound:{fn}&#93;</span>""".format(
            orig=sound.group(0), fn=sound.group(1), ip=collection_arrow_name,
            ttl=((' title=" ' + title + ' "') if B['B11_BUTTON_TITLES'][0] else '') )
        # The &#91; &#93; are the square brackets that we want to
        # appear as brackets and not trigger the playing of the
        # sound. The span inside the a around the img is to bring this
        # closer in line with AnkiDroid.

    retv = re.sub(sound_re, add_button, qa_html)
    #   no matches = no call

    if qa_type == 'q':
        if A['COLORFUL_TOOLBAR'][0]:
            replay_action.setEnabled(False)
            replay_all_audio_action.setEnabled(False)
            replay_audio_action.setEnabled(False)

        if A['F6_SOUND_KEY_MENU'][0]:
            pause_action.setEnabled(False)
            stop_action.setEnabled(False)
            forward_action.setEnabled(False)
            backward_action.setEnabled(False)
            if A['F6_FAST_SLOW'][0]:
                fast_action.setEnabled(False)
                slow_action.setEnabled(False)
                init_action.setEnabled(False)

    if qa_type == 'a':
        if len(soundtrack_q_list)+len(soundtrack_a_list)>0: 
         if A['COLORFUL_TOOLBAR'][0]:
            replay_action.setEnabled(True)
            replay_all_audio_action.setEnabled(True)
            replay_audio_action.setEnabled(True)

         if A['F6_SOUND_KEY_MENU'][0]:
            pause_action.setEnabled(True)
            stop_action.setEnabled(True)
            forward_action.setEnabled(True)
            backward_action.setEnabled(True)
            if A['F6_FAST_SLOW'][0]:
                fast_action.setEnabled(True)
                slow_action.setEnabled(True)
                init_action.setEnabled(True)

    #onAudioList()
    return retv

# Filter the questions and answers to remove absentee (missing, not found, unavailable) images.

def images_filter(
        qa_html, qa_type, dummy_fields, dummy_model, dummy_data, dummy_col):

    #   no matches = no call
    def remove_img(picture):
        """
        Remove <img tag, if there is no such file in collection.media folder.
        """
        pic = os.path.join(mw.pm.profileFolder(), "collection.media", picture.group(1))
        if not os.path.isfile(pic):
            return ""

        return picture.group(0)

    return re.sub(image_re, remove_img, qa_html)
    #   no matches = no call


def simple_link_handler(url):
    # Play the file.
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        QDesktopServices.openUrl(QUrl(url))

def add_clayout_link_handler(clayout, dummy_t):
    # Make sure we play the files from the card layout window.
    clayout.forms[-1]['pform'].frontWeb.setLinkHandler(simple_link_handler)
    clayout.forms[-1]['pform'].backWeb.setLinkHandler(simple_link_handler)

def add_preview_link_handler(browser):
    # Make sure we play the files from the preview window.
    browser._previewWeb.setLinkHandler(simple_link_handler)

def reduce_format_qa(self, text):
    # Remove elements with a given class before displaying.
    soup = BeautifulSoup(text)
    for hide in soup.findAll(True, {'class': re.compile(
            '\\b' + hide_class_name + '\\b')}):
        hide.extract()
    return original_format_qa(self, unicode(soup))

def copy_arrow():
    # Copy the image file to the collection.
    if not os.path.exists(os.path.join(
            mw.col.media.dir(), collection_arrow_name)):
        shutil.copy(
            os.path.join(mw.pm.addonFolder(), MUSTHAVE_COLOR_ICONS,
                         original_arrow_name),
            collection_arrow_name)

if A['REPLAY_BUTTONS_ON_CARD'][0]:
   #oldLinkHandler = Reviewer._linkHandler
   #Reviewer._linkHandler = tagClicklinkHandler
   Reviewer._linkHandler = wrap(Reviewer._linkHandler, tagClicklinkHandler)

   original_format_qa = DataModel.formatQA
   DataModel.formatQA = reduce_format_qa

   addHook("mungeQA", images_filter) # after play_button_filter replay images also had been deleted!
   addHook("mungeQA", play_button_filter) 
   # file exists in collection.media folder
   # but not found cause of <img src=... alt=... style=... 
   # alt and style were interpreted by re as part of src value.
   # after changing to <img alt=... src=... style=... it's Ok now,
   # images_filter and play_button_filter can be called in any order.

   Browser._openPreview = wrap(Browser._openPreview, add_preview_link_handler)
   CardLayout.addTab = wrap(CardLayout.addTab, add_clayout_link_handler)
   addHook("profileLoaded", copy_arrow)

##################################################################
# ZOOM 
# https://ankiweb.net/shared/info/1956318463

deck_browser_current_zoom = deck_browser_standard_zoom
overview_current_zoom = overview_standard_zoom
reviewer_current_zoom = reviewer_standard_zoom

# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""Add-on for Anki 2 to zoom in or out."""

def reset_current_zoom():
    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    deck_browser_current_zoom = deck_browser_standard_zoom
    overview_current_zoom = overview_standard_zoom
    reviewer_current_zoom = reviewer_standard_zoom

# How much to increase or decrease the zoom FACTOR with each step. The
# a little odd looking number is the fourth root of two. That means
# with four clicks you double or half the size, as precisely as
# possible.
zoom_step = .1 # 1.1 # min 0.5 after 1.9 next 2.1 # 1.5**.15 min 0.8 # 2.0**0.25

def zoom_in(step=None):
    # Increase the text size.
    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    if not step:
        step = zoom_step

    if 'deckBrowser' == mw.state:
        #deck_browser_current_zoom = round(deck_browser_current_zoom * zoom_step, 1)
        deck_browser_current_zoom = round(deck_browser_current_zoom + zoom_step, 1)
        current_zoom = deck_browser_current_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        overview_current_zoom = round(overview_current_zoom + zoom_step, 1)
        current_zoom = overview_current_zoom
    if 'review' == mw.state:
        reviewer_current_zoom = round(reviewer_current_zoom + zoom_step, 1)
        current_zoom = reviewer_current_zoom

    if A['ZOOM_IMAGES'][0]:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)

def zoom_out(step=None):
    # Decrease the text size.
    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    if not step:
        step = zoom_step

    if 'deckBrowser' == mw.state:
        #deck_browser_current_zoom = round(deck_browser_current_zoom / zoom_step, 1)
        deck_browser_current_zoom = max(.1,round(deck_browser_current_zoom - zoom_step, 1))
        current_zoom = deck_browser_current_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        overview_current_zoom = max(.1,round(overview_current_zoom - zoom_step, 1))
        current_zoom = overview_current_zoom
    if 'review' == mw.state:
        reviewer_current_zoom = max(.1,round(reviewer_current_zoom - zoom_step, 1))
        current_zoom = reviewer_current_zoom

    if A['ZOOM_IMAGES'][0]:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)

def zoom_init(state=None, *args):
    # Reset the text size.
    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    current_zoom = 1.0

    deck_browser_current_zoom = 1.0
    overview_current_zoom = 1.0
    reviewer_current_zoom = 1.0

    if A['ZOOM_IMAGES'][0]:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)

def zoom_reset(state=None, *args):
    # Reset the text size.
    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    current_zoom = 1.0

    if 'deckBrowser' == mw.state:
        current_zoom = deck_browser_standard_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        current_zoom = overview_standard_zoom
    if 'review' == mw.state:
        current_zoom = reviewer_standard_zoom
    reset_current_zoom()

    if A['ZOOM_IMAGES'][0]:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)

def current_reset_zoom(state=None, *args):
    # Reset the text size.
    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    current_zoom = 1

    if 'deckBrowser' == mw.state:
        current_zoom = deck_browser_current_zoom
    if 'overview' == mw.state or 'requestRequired' == mw.state:
        current_zoom = overview_current_zoom
    if 'review' == mw.state:
        current_zoom = reviewer_current_zoom

    if A['ZOOM_IMAGES'][0]:
        mw.web.setZoomFactor(current_zoom)
    else:
        mw.web.setTextSizeMultiplier(current_zoom)

def zoom_info():
    showTextik("<big>deck_browser_standard_zoom = <b>"+str(deck_browser_current_zoom)+"</b><br>\n"+\
        "overview_standard_zoom = <b>"+str(overview_current_zoom)+"</b><br>\n"+\
        "reviewer_standard_zoom = <b>"+str(reviewer_current_zoom)+"</b></big>\n",\
        minW=222, minH=66, type="HTML", title="Zoom")

def zoom_setup_menu():
    # Set up the zoom menu.
    mw.zoom_submenu = QMenu('Мас&штаб' if lang == 'ru' else _(u"&Zoom"), mw)
    if A['ANKI_MENU_ICONS'][0]:
        mw.zoom_submenu.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom.png')))

    zoom_info_action = QAction('Масштаб &показать' if lang == 'ru' else _('Zoom &Info'), mw)
    zoom_info_action.setShortcut(QKeySequence(HOTKEY['zoom_info'][0])) # Ctrl+Shift+0 doesn't work on NumPad
    mw.connect(zoom_info_action, SIGNAL("triggered()"), zoom_info)

    zoom_in_action = QAction('Масштаб у&величить' if lang == 'ru' else _('Zoom &In'), mw)
    zoom_in_action.setShortcut(QKeySequence(HOTKEY['zoom_in'][0]))
    if A['ANKI_MENU_ICONS'][0]:
        zoom_in_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom_in.png')))
    mw.connect(zoom_in_action, SIGNAL("triggered()"), zoom_in)

    zoom_out_action = QAction('Масштаб у&меньшить' if lang == 'ru' else _('Zoom &Out'), mw)
    zoom_out_action.setShortcut(QKeySequence(HOTKEY['zoom_out'][0]))
    if A['ANKI_MENU_ICONS'][0]:
        zoom_out_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'zoom_out.png')))
    mw.connect(zoom_out_action, SIGNAL("triggered()"), zoom_out)

    reset_zoom_action = QAction('Масштаб на&чальный ( ='+str(deck_browser_standard_zoom)+' ='+str(overview_standard_zoom)+' ='+str(reviewer_standard_zoom)+' )' if lang == 'ru' else _('&Reset Initial ')+u'( ='+str(deck_browser_standard_zoom)+' ='+str(overview_standard_zoom)+' ='+str(reviewer_standard_zoom)+' )', mw)
    reset_zoom_action.setShortcut(QKeySequence(HOTKEY['zoom_reset'][0])) # Shift+0 does not work on NumPad
    mw.connect(reset_zoom_action, SIGNAL("triggered()"), zoom_reset)

    reset_zoom_init_action = QAction('Мас&штаб 1:1 100% ( =1.0 =1.0 =1.0 )' if lang == 'ru' else _('&Reset 1:1 100% ( =1.0 =1.0 =1.0 )'), mw)
    reset_zoom_init_action.setShortcut(QKeySequence(HOTKEY['zoom_init'][0]))
    mw.connect(reset_zoom_init_action, SIGNAL("triggered()"), zoom_init)

    if mw_addon_view_menu_exists:
        mw.addon_view_menu.addMenu(mw.zoom_submenu)
        mw.zoom_submenu.addAction(zoom_info_action)
        mw.zoom_submenu.addSeparator()
        mw.zoom_submenu.addAction(zoom_in_action)
        mw.zoom_submenu.addAction(zoom_out_action)
        mw.zoom_submenu.addSeparator()
        if deck_browser_standard_zoom != 1.0 or overview_standard_zoom != 1.0 or reviewer_standard_zoom != 1.0:
            mw.zoom_submenu.addAction(reset_zoom_action)
        mw.zoom_submenu.addAction(reset_zoom_init_action)

################################
#
toBeerOrNot2Beer = False

def handle_wheel_event(event):
    """Zoom on mouse wheel events with Ctrl.

    Zoom in our out on mouse wheel events when Ctrl is pressed.  
    A standard mouse wheel click is 120/8 degree. 
    ZOOM by one step for that amount.
    """
    global F9_HINT_PEEKED

    if event.modifiers() & Qt.ControlModifier:
        step = event.delta() / 120 * zoom_step
        if step < 0:
            zoom_in(-step)
        else:
            zoom_out(step)

    elif bool(event.modifiers() & Qt.AltModifier) and bool(event.modifiers() & Qt.ShiftModifier) or (altMW_action.isChecked() and shiftMW_action.isChecked()):

        step = event.delta() / 12000 * zoom_step
        if step > 0:
            if mw.state == "review":
                if mw.reviewer.state == 'answer':
                    if (not A['ONESIDED_CARDS'][0]) or (not toBeerOrNot2Beer):
                       anki.sound.stopMplayer()
                       F9_HINT_PEEKED = False
                       mw.reviewer._initWeb() # _showQuestion()
                    elif mw.form.actionUndo.isEnabled():
                       anki.sound.stopMplayer()
                       mw.onUndo()
                elif mw.reviewer.state == 'question':
                   if mw.form.actionUndo.isEnabled():
                       anki.sound.stopMplayer()
                       mw.onUndo()
        else:
            if mw.state == "review":
              if not _showHint(mw.reviewer):
                if mw.reviewer.state == 'question':
                   mw.reviewer._showAnswer() # ._showAnswerHack()
                elif mw.reviewer.state == 'answer':
                   F9_HINT_PEEKED = False
                   # self._initWeb() # ._initWeb() # _showQuestion() 
                   #mw.reviewer._answerCard(mw.reviewer._defaultEase())
                   mw.reviewer.onBuryCard()

    elif bool(event.modifiers() & Qt.AltModifier) or altMW_action.isChecked(): 

        step = event.delta() / 12000 * zoom_step
        if step > 0:
           if mw.state == "review":
                if mw.reviewer.state == 'answer':
                    if (not A['ONESIDED_CARDS'][0]) or (not toBeerOrNot2Beer):
                       anki.sound.stopMplayer()
                       F9_HINT_PEEKED = False
                       mw.reviewer._initWeb() # _showQuestion()
                    elif mw.form.actionUndo.isEnabled():
                       anki.sound.stopMplayer()
                       mw.onUndo()
                elif mw.reviewer.state == 'question':
                    if mw.form.actionUndo.isEnabled():
                        mw.onUndo()
        else:
           if mw.state == "review":
              if not _showHint(mw.reviewer):
                if mw.reviewer.state == 'question':
                   mw.reviewer._showAnswer() # ._showAnswerHack()
                elif mw.reviewer.state == 'answer':
                   F9_HINT_PEEKED = False
                   # self._initWeb() # ._initWeb() # _showQuestion() 
                   mw.reviewer._answerCard(mw.reviewer._defaultEase())

    elif bool(event.modifiers() & Qt.ShiftModifier) or shiftMW_action.isChecked():

        step = event.delta() / 12000 * zoom_step
        if step > 0:
            if mw.state == "review":
                if mw.reviewer.state == 'answer':
                    if (not A['ONESIDED_CARDS'][0]) or (not toBeerOrNot2Beer):
                       anki.sound.stopMplayer()
                       F9_HINT_PEEKED = False
                       mw.reviewer._initWeb() # _showQuestion()
                    elif mw.form.actionUndo.isEnabled():
                       anki.sound.stopMplayer()
                       mw.onUndo()
                elif mw.reviewer.state == 'question':
                   if mw.form.actionUndo.isEnabled():
                       anki.sound.stopMplayer()
                       mw.onUndo()
        else:
            if mw.state == "review":
                if mw.reviewer.state == 'question':
                   anki.sound.stopMplayer()
                   mw.reviewer._showAnswer()
                elif mw.reviewer.state == 'answer':
                   anki.sound.stopMplayer()
                   mw.reviewer._answerCard(mw.reviewer._defaultEase())

    else:
        original_mw_web_wheelEvent(event)

def run_move_to_state_hook(state, *args):
    """Run a hook whenever we have changed the state."""
    runHook("movedToState", state)

if A['ZOOM'][0]:

    mw.moveToState = wrap(mw.moveToState, run_move_to_state_hook)
    addHook("movedToState", current_reset_zoom)
    original_mw_web_wheelEvent = mw.web.wheelEvent
    mw.web.wheelEvent = handle_wheel_event
    zoom_setup_menu()

    shiftMW_action = QAction(mw)
    shiftMW_action.setText(u'(Shift+колесо мыши): ответы по умолч.' if lang=='ru' else u'Shift + Mouse Wheel')
    shiftMW_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'shift.png')))
    shiftMW_action.setCheckable(True)
    shiftMW_action.setChecked(False)

    altMW_action = QAction(mw)
    altMW_action.setText(u'(Alt+колесо мыши): ещё и подсказки' if lang=='ru' else u'Alt + Mouse Wheel')
    altMW_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'alt.png')))
    altMW_action.setCheckable(True)
    altMW_action.setChecked(False)

    if mw_addon_go_menu_exists:
        mw.addon_go_menu.addSeparator()
        mw.addon_go_menu.addAction(shiftMW_action)
        mw.addon_go_menu.addAction(altMW_action)
        mw.addon_go_menu.addSeparator()

####################################################################################
toolbar_gradient_form = """QToolBar:top, QToolBar:bottom {{
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {bg}, stop:1 {bgg});
}}
QToolBar:left, QToolBar:right {{
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {bg}, stop:1 {bgg});
}}
QToolBar:top {{border-bottom: 1px solid {bgl};}}
QToolBar:bottom {{border-top: 1px solid {bgl};}}
QToolBar:left {{border-right: 1px solid {bgl};}}
QToolBar:right {{border-left: 1px solid {bgl};}}""" # """

# Change below this at your own risk/only when you know what you are doing.

# Make all the actions top level, so we can use them for the menu and
# the tool bar.

# Most of the icons are part of the standard version, but as they are
# not currently used by the standard version, they may disappear when
# dae gets around to doing some clean up. So bring them along, anyway.

if A['COLORFUL_TOOLBAR'][0]: # or not B['B13_EDIT_MORE'][0]:

    edit_current_action = QAction(mw)
    edit_current_action.setText(u'Р&едактирование...' if lang=='ru' else _(u"&Edit..."))
    edit_current_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'edit_current.png')))
    edit_current_action.setShortcut(QKeySequence(HOTKEY['E'][0])) 
    mw.connect(edit_current_action, SIGNAL("triggered()"), go_edit_current)

    toggle_mark_action = QAction(mw)
    toggle_mark_action.setText(_(u"Mark Note"))
    toggle_mark_action.setCheckable(True)

    toggle_mark_icon = QIcon()
    toggle_mark_icon.addFile(os.path.join(MUSTHAVE_COLOR_ICONS, 'mark_off.png'))
    toggle_mark_icon.addFile(os.path.join(MUSTHAVE_COLOR_ICONS, 'mark_on.png'), 
                             QSize(), QIcon.Normal, QIcon.On)
    if A['COLORFUL_TOOLBAR'][0]:
        toggle_mark_action.setIcon(toggle_mark_icon)

    toggle_mark_action.setShortcut(QKeySequence(HOTKEY['marked'][0])) 
    # Alt+Space opens main menu.
    # Shift+Space doesn't work inside of type:Field
    mw.connect(toggle_mark_action, SIGNAL("triggered()"), mw.reviewer.onMark)

    toggle_last_card_action = QAction(mw)
    toggle_last_card_action.setText(u"Прекратить просмотр после этой карточки" if lang=="ru" else _(u"Last card"))
    toggle_last_card_action.setToolTip(u"После этой карточки просмотр колоды будет прекращён" if lang=="ru" else _(u"Last card"))
    toggle_last_card_action.setShortcut(HOTKEY['toggle_last'][0])
    toggle_last_card_action.setCheckable(True)
    toggle_last_card_action.setChecked(False)

    toggle_last_card_icon = QIcon()
    toggle_last_card_icon.addFile(os.path.join(MUSTHAVE_COLOR_ICONS, 'last_card_off.png'))
    toggle_last_card_icon.addFile(os.path.join(MUSTHAVE_COLOR_ICONS, 'last_card_on.png'),
                                  QSize(), QIcon.Normal, QIcon.On)
    if A['COLORFUL_TOOLBAR'][0]:
        toggle_last_card_action.setIcon(toggle_last_card_icon)

    bury_card_action = QAction(mw)
    bury_card_action.setText(_(u"Bury Card"))
    #bury_note_action.setShortcut("-") # This hotkey is used somewhere else. But it works as intended.
    if A['ANKI_MENU_ICONS'][0]:
        bury_card_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'bury-card.png')))
    mw.connect(bury_card_action, SIGNAL("triggered()"), mw.reviewer.onBuryCard)

    bury_note_action = QAction(mw)
    bury_note_action.setText(_(u"Bury Note"))
    bury_note_action.setShortcut(HOTKEY['bury_note'][0])
    if A['ANKI_MENU_ICONS'][0]:
        bury_note_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'bury.png')))
    mw.connect(bury_note_action, SIGNAL("triggered()"), mw.reviewer.onBuryNote)

    suspend_card_action = QAction(mw)
    suspend_card_action.setText(_(u"Suspend Card"))
    suspend_card_action.setShortcut(HOTKEY['suspend_card'][0])
    if A['ANKI_MENU_ICONS'][0]:
        suspend_card_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'suspend_card.png')))
    mw.connect(
        suspend_card_action, SIGNAL("triggered()"), mw.reviewer.onSuspendCard)

    suspend_note_action = QAction(mw)
    suspend_note_action.setText(_(u"Suspend Note"))
    suspend_note_action.setShortcut(HOTKEY['suspend_note'][0])
    if A['ANKI_MENU_ICONS'][0]:
        suspend_note_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'suspend.png')))
    mw.connect(suspend_note_action, SIGNAL("triggered()"), mw.reviewer.onSuspend)

    delete_action = QAction(mw)
    delete_action.setText(_(u"Delete Note"))
    if A['ANKI_MENU_ICONS'][0]:
        delete_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'delete.png')))
    #delete_action.setShortcut(Qt.META + Qt.Key_Minus) 
    # on Mac it is converted to Ctrl+- but it is zoom in already
    delete_action.setShortcut(HOTKEY['META_Minus'][0]) 
    mw.connect(delete_action, SIGNAL("triggered()"), ask_delete)

    options_action = QAction(mw)
    options_action.setText(u'&Настройки...' if lang=='ru' else _(u"&Options..."))
    if A['ANKI_MENU_ICONS'][0]:
        options_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'options.png')))
    options_action.setShortcut(HOTKEYZ['options'][0]) 
    mw.connect(options_action, SIGNAL("triggered()"), go_options)

mute_action = QAction(mw)
mute_action.setText(_(u"Automatically play audio"))
mute_action.setShortcut(QKeySequence(HOTKEY['autoplay'][0]))
mute_action.setCheckable(True)
mute_action.setChecked(True)
mute_icon = QIcon()
mute_icon.addFile(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-mute.png'))
mute_icon.addFile(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-unmute.png'), QSize(), QIcon.Normal, QIcon.On)
mute_action.setIcon(mute_icon)

if A['COLORFUL_TOOLBAR'][0]:

    bury_card_aktion = QAction(mw)
    bury_card_aktion.setText(_(u"Bury Card"))
    bury_card_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'bury-card.png')))
    mw.connect(bury_card_aktion, SIGNAL("triggered()"), mw.reviewer.onBuryCard)

    bury_note_aktion = QAction(mw)
    bury_note_aktion.setText(_(u"Bury Note"))
    bury_note_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'bury.png')))
    mw.connect(bury_note_aktion, SIGNAL("triggered()"), mw.reviewer.onBuryNote)

    suspend_card_aktion = QAction(mw)
    suspend_card_aktion.setText(_(u"Suspend Card"))
    suspend_card_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-suspend_card.png')))
    mw.connect(
        suspend_card_aktion, SIGNAL("triggered()"), mw.reviewer.onSuspendCard)

    suspend_note_aktion = QAction(mw)
    suspend_note_aktion.setText(_(u"Suspend Note"))
    suspend_note_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-suspend.png')))
    mw.connect(suspend_note_aktion, SIGNAL("triggered()"), mw.reviewer.onSuspend)

    delete_aktion = QAction(mw)
    delete_aktion.setText(_(u"Delete Note"))
    delete_aktion.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-delete.png')))
    mw.connect(delete_aktion, SIGNAL("triggered()"), ask_delete)

    replay_action = QAction(mw)
    replay_action.setText(u"Проиграть все &аудио-файлы (F5)" if lang=='ru' else _(u"&Replay Audio"))
    replay_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'replay.png')))
    mw.connect(replay_action, SIGNAL("triggered()"), mw.reviewer.replayAudio)

    replay_audio_action = QAction(mw)
    replay_audio_action.setText("Прои&грать следующее аудио" if lang == 'ru' else "Replay &Next Audio")
    replay_audio_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'play_next.png')))
    replay_audio_action.setShortcut(HOTKEY['replay_next'][0])
    mw.connect(replay_audio_action, SIGNAL("triggered()"), onKeyPlus)

    list_audio_action = QAction(mw)
    list_audio_action.setText("Показать &список аудио" if lang == 'ru' else "Show Audio &List")
    list_audio_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'list.png')))
    list_audio_action.setShortcut(HOTKEY['audio_list'][0])
    mw.connect(list_audio_action, SIGNAL("triggered()"), onAudioList)

    record_own_action = QAction(mw)
    record_own_action.setText(u"&Записать свой голос" if lang=='ru' else _(u"Re&cord own voice"))
    record_own_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'blue_mic.png')))
    record_own_action.setShortcut(HOTKEYZ['record_own_voice'][0])
    mw.connect(record_own_action, SIGNAL("triggered()"), mw.reviewer.onRecordVoice)

    replay_own_action = QAction(mw)
    replay_own_action.setText(u"&Воспроизвести свой голос" if lang=='ru' else _(u"Re&play own voice"))
    replay_own_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'g-play_green.png')))
    replay_own_action.setShortcut(HOTKEYZ['replay_own_voice'][0])
    mw.connect(replay_own_action, SIGNAL("triggered()"),
               mw.reviewer.onReplayRecorded)

    replay_all_audio_action = QAction(mw)
    replay_all_audio_action.setText("Про&играть все аудио (F5|R)" if lang == 'ru' else "&Replay All Audio (F5|R)")
    replay_all_audio_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'replay.png')))
    mw.connect(replay_all_audio_action, SIGNAL("triggered()"), mw.reviewer.replayAudio)

    # Add a Qt tool bar to Anki2.

    # This is a more Anki-1-ish Qt tool bar with a number of rather big,
    # colorful icons to replace the Anki 2 DSAB toolbar.

    mw.qt_tool_bar = QToolBar()
    # mw.qt_tool_bar.setAccessibleName('secondary tool bar')
    mw.qt_tool_bar.setObjectName('qt tool bar')
    if netbook_version:
        mw.qt_tool_bar.setIconSize(QSize(A['KING_SIZE'][0], A['KING_SIZE'][0]))
    else:
        mw.qt_tool_bar.setIconSize(QSize(32, 32))
    # Conditional setup
    if netbook_version or qt_toolbar_movable:
        mw.qt_tool_bar.setFloatable(True)
        mw.qt_tool_bar.setMovable(True)
        if netbook_version:
            mw.addToolBar(Qt.LeftToolBarArea, mw.qt_tool_bar)
        else:
            mw.addToolBar(Qt.TopToolBarArea, mw.qt_tool_bar)
    else:
        mw.qt_tool_bar.setFloatable(False)
        mw.qt_tool_bar.setMovable(False)
        mw.mainLayout.insertWidget(1, mw.qt_tool_bar)
    if do_gradient:
        palette = mw.qt_tool_bar.palette()
        fg = palette.color(QPalette.ButtonText)
        bg = palette.color(QPalette.Button)

        if bg.lightnessF() > fg.lightnessF():
            bgg = bg.lighter(GRADIENT_L)
            bgl = bg.darker(GRADIENT_H)
        else:
            bgl = bg.lighter(GRADIENT_L)
            bgg = bg.darker(GRADIENT_H)

        mw.qt_tool_bar.setStyleSheet(
            toolbar_gradient_form.format(
                bg=bg.name(), bgg=bgg.name(), bgl=bgl.name()))

    mw.qt_tool_bar.addAction(mw.form.actionUndo)
    mw.qt_tool_bar.addSeparator()
    mw.qt_tool_bar.addAction(edit_current_action)
    mw.qt_tool_bar.addAction(edit_layout_action)
    mw.qt_tool_bar.addSeparator()
    mw.qt_tool_bar.addAction(decks_aktion)
    mw.qt_tool_bar.addAction(add_notes_aktion)
    mw.qt_tool_bar.addAction(browse_cards_action)
    mw.qt_tool_bar.addSeparator()
    mw.qt_tool_bar.addAction(statistics_aktion)
    mw.qt_tool_bar.addAction(sync_action)
    mw.qt_tool_bar.addSeparator()
    mw.qt_tool_bar.addAction(overeview_action)
    mw.qt_tool_bar.addAction(study_aktion)
    if A['ZOOM'][0]:
        mw.qt_tool_bar.addSeparator()
        mw.qt_tool_bar.addAction(shiftMW_action)
        mw.qt_tool_bar.addAction(altMW_action)
        #mw.qt_tool_bar.addSeparator()

    def more_tool_bar_off():
        #"""Hide the more tool bar."""
        global show_more_tool_bar_action, edit_layout_action, bury_note_action, toggle_mark_action, suspend_card_action, suspend_note_action, delete_action, bury_card_action

        show_more_tool_bar_action.setEnabled(False)

        toggle_mark_action.setEnabled(False)

        bury_card_action.setEnabled(False)
        bury_note_action.setEnabled(False)
        suspend_card_action.setEnabled(False)
        suspend_note_action.setEnabled(False)
        delete_action.setEnabled(False)

        replay_action.setEnabled(False)
        replay_audio_action.setEnabled(False)
        replay_all_audio_action.setEnabled(False)
        list_audio_action.setEnabled(False)
        mute_action.setEnabled(False)

        if A['F6_SOUND_KEY_MENU'][0]:
            pause_action.setEnabled(False)
            stop_action.setEnabled(False)
            forward_action.setEnabled(False)
            backward_action.setEnabled(False)
            if A['F6_FAST_SLOW'][0]:
                fast_action.setEnabled(False)
                slow_action.setEnabled(False)
                init_action.setEnabled(False)

        try:
            mw.reviewer.more_tool_bar.hide()
        except AttributeError:
            pass

    def add_more_tool_bar():
        # Add a tool bar at the bottom.

        #This provieds colorful command buttons for the functions usually
        #hidden in the "More" button at the bottom.

        try:
            mw.reviewer.more_tool_bar = QToolBar()
        except AttributeError:
            return
        # mw.reviewer.more_tool_bar.setAccessibleName('secondary tool bar')
        mw.reviewer.more_tool_bar.setObjectName('more options tool bar')
        mw.reviewer.more_tool_bar.setIconSize(QSize(A['KING_SIZE'][0], A['KING_SIZE'][0]))
        if netbook_version:
            mw.reviewer.more_tool_bar.setFloatable(True)
            mw.reviewer.more_tool_bar.setMovable(True)
            mw.addToolBar(Qt.RightToolBarArea, mw.reviewer.more_tool_bar)
        else:
            mw.reviewer.more_tool_bar.setFloatable(False)
            mw.reviewer.more_tool_bar.setMovable(False)
            mw.mainLayout.insertWidget(2, mw.reviewer.more_tool_bar)
        if do_gradient:
            palette = mw.reviewer.more_tool_bar.palette()
            fg = palette.color(QPalette.ButtonText)
            bg = palette.color(QPalette.Button)

            if bg.lightnessF() > fg.lightnessF():
                bgg = bg.lighter(GRADIENT_L)
                bgl = bg.darker(GRADIENT_H)
            else:
                bgl = bg.lighter(GRADIENT_L)
                bgg = bg.darker(GRADIENT_H)

            mw.reviewer.more_tool_bar.setStyleSheet(
                toolbar_gradient_form.format(
                    bg=bg.name(), bgg=bgg.name(), bgl=bgl.name()))
        # Add the actions here
        mw.reviewer.more_tool_bar.addAction(mw.form.actionUndo)
        mw.reviewer.more_tool_bar.addSeparator()
        mw.reviewer.more_tool_bar.addAction(edit_current_action)
        mw.reviewer.more_tool_bar.addAction(edit_layout_action)

        mw.reviewer.more_tool_bar.addSeparator()
        mw.reviewer.more_tool_bar.addAction(toggle_mark_action)

        if show_toggle_last:
            mw.reviewer.more_tool_bar.addAction(toggle_last_card_action)

        mw.reviewer.more_tool_bar.addSeparator()
        mw.reviewer.more_tool_bar.addAction(bury_card_aktion)
        mw.reviewer.more_tool_bar.addAction(bury_note_aktion)
        if show_suspend_card:
            mw.reviewer.more_tool_bar.addAction(suspend_card_aktion)
        if show_suspend_note:
            mw.reviewer.more_tool_bar.addAction(suspend_note_aktion)
        mw.reviewer.more_tool_bar.addAction(delete_aktion)

        mw.reviewer.more_tool_bar.addSeparator()
        mw.reviewer.more_tool_bar.addAction(options_aktion)

        mw.reviewer.more_tool_bar.addSeparator()
        if show_mute_button:
            mw.reviewer.more_tool_bar.addAction(mute_action)
        mw.reviewer.more_tool_bar.addAction(replay_action)
        if A['REPLAY_BUTTONS_ON_CARD'][0]:
            mw.reviewer.more_tool_bar.addAction(replay_audio_action)

        mw.reviewer.more_tool_bar.addSeparator()
        mw.reviewer.more_tool_bar.addAction(record_own_action)
        mw.reviewer.more_tool_bar.addAction(replay_own_action)

        if A['F6_SOUND_KEY_MENU'][0]:
            mw.reviewer.more_tool_bar.addSeparator()
            mw.reviewer.more_tool_bar.addAction(pause_auction)
            mw.reviewer.more_tool_bar.addSeparator()

    add_more_tool_bar()
    more_tool_bar_off()

if A['COLORFUL_TOOLBAR'][0]: # or not B['B13_EDIT_MORE'][0]:
    # Add a number of items to menus.

    # Put the functions of the DASB old-style tool bar links into
    # menus. Sync to the file menu, stats to the tools menu, the DASB,
    # together with a study-withouts-overview item to a new go
    # menu. Also add items to, d'uh, edit stuff to the edit menu.

    # Add sync to the file memu. It was there in Anki 1.
    #mw.form.menuCol.insertAction(mw.form.actionImport, sync_action)
    # Make a new top level menu and insert it.

    # Add DSAB to the new go menu
    if mw_addon_view_menu_exists:
        mw.addon_view_menu.addSeparator()
    # Stats. Maybe this should go to help. Seems somewhat help-ish to me, but not too much.

    # Add to the edit menu. The undo looked a bit forlorn.
    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addAction(edit_current_action)
    mw.form.menuEdit.addAction(edit_layout_action)
    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addAction(toggle_mark_action)
    mw.form.menuEdit.addAction(toggle_last_card_action)
    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addAction(bury_card_action)
    mw.form.menuEdit.addAction(bury_note_action)
    mw.form.menuEdit.addAction(suspend_card_action)
    mw.form.menuEdit.addAction(suspend_note_action)
    mw.form.menuEdit.addAction(delete_action)
    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addAction(options_action)
    mw.form.menuEdit.addSeparator()

if A['FLIP_FLOP'][0] or A['COLORFUL_TOOLBAR'][0]:  

    PageUp_icon = QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'PageUp.png'))
    PageDown_icon = QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'PageDown.png'))

if A['FLIP_FLOP'][0]: #TODO

    show_question_auction = QAction(mw)
    show_question_auction.setText(u'&Лицевая Сторона' if lang=='ru' else _(u"Card's &FrontSide"))
    show_question_auction.setShortcut(QKeySequence(HOTKEY['F7_FrontSide'][0]))
    if A['ANKI_MENU_ICONS'][0]:
        show_question_auction.setIcon(PageUp_icon)
    mw.connect(show_question_auction, SIGNAL("triggered()"), go_question)

    show_answer_auction = QAction(mw)
    show_answer_auction.setText(u'&Оборотная Сторона' if lang=='ru' else _(u"Card's &BackSide"))
    show_answer_auction.setShortcut(QKeySequence(HOTKEY['F8_BackSide'][0])) 
    if A['ANKI_MENU_ICONS'][0]:
        show_answer_auction.setIcon(PageDown_icon)
    mw.connect(show_answer_auction, SIGNAL("triggered()"), go_answer)

    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addAction(show_question_auction)
    #edit_menu.addAction(onesided_action) 
    # U can't do menu twice (or more) with the same action
    # -- on additional icons panel it's OK --
    mw.form.menuEdit.addAction(show_answer_auction)
    mw.form.menuEdit.addSeparator()

if A['SWAP_FRONT_BACK'][0]:
    mw.form.menuEdit.addAction(swap_action)
    mw.form.menuEdit.addSeparator()

#########################################################
#
if mw_addon_view_menu_exists and A['F9_HINT_PEEKING'][0]:

    F9_HINT_PEEKING_action = QAction(mw)
    F9_HINT_PEEKING_action.setText("Пока&зать следующую подсказку" if lang == 'ru' else "Show Next Hint")
    if A['ANKI_MENU_ICONS'][0]:
        F9_HINT_PEEKING_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'hint.png')))
    F9_HINT_PEEKING_action.setShortcut(HOTKEY['next_hint'][0]) # Ctrl+H,F9 press ^H then F9 voila # Control+H OK
    mw.connect(F9_HINT_PEEKING_action, SIGNAL("triggered()"), on_showHint)

    show_all_hints_action = QAction(mw)
    show_all_hints_action.setText("Показать &все подсказки" if lang == 'ru' else "Show All Hints")
    if A['ANKI_MENU_ICONS'][0]:
        show_all_hints_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'envelope.png')))
    show_all_hints_action.setShortcut(HOTKEY['all_hints'][0]) # Ctrl+Shift+H does not work anymore
    mw.connect(show_all_hints_action, SIGNAL("triggered()"), on_showAllHints)

    mw.addon_view_menu.addSeparator() 
    mw.addon_view_menu.addAction(F9_HINT_PEEKING_action) 
    mw.addon_view_menu.addAction(show_all_hints_action) 
    mw.addon_view_menu.addSeparator() 

######################################################################
# Expand and Collapse Decks
# https://ankiweb.net/shared/info/2554066128
# Creates two options in the Tools menu to expand and collapse all the decks in the main window
# Obviously it must be placed in view menu, not tools.

def toggleDecksCollapsed(collapsed):
    "Toggles all decks to be either expanded or collapsed, based upon the boolean parameter passed in "
    # get all the decks and set them collapsed/expanded
    deckids = mw.col.decks.allIds()
    for deckid in deckids:
        deck = mw.col.decks.get(deckid)
        deck['collapsed'] = collapsed
        mw.col.decks.save(deck)

    # Refresh the browser to show the changes
    mw.deckBrowser.refresh()

def expandAllDecks():
    toggleDecksCollapsed(False)

def collapseAllDecks():
    toggleDecksCollapsed(True)

if A['EXPAND_AND_COLLAPSE_DECKS'][0]:

   expandAction = QAction("&Развернуть все колоды" if lang == 'ru' else "Expand &All Decks", mw)
   expandAction.setShortcut(QKeySequence(HOTKEY['expand_decks'][0]))
   if A['ANKI_MENU_ICONS'][0]:
      expandAction.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'plus.png')))
   mw.connect(expandAction, SIGNAL("triggered()"), expandAllDecks)
   #mw.form.menuTools.addAction(expandAction)

   collapseAction = QAction("&Свернуть все колоды" if lang == 'ru' else "Collapse All &Decks", mw)
   collapseAction.setShortcut(QKeySequence(HOTKEY['collapse_decks'][0]))
   if A['ANKI_MENU_ICONS'][0]:
      collapseAction.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'minus.png')))
   mw.connect(collapseAction, SIGNAL("triggered()"), collapseAllDecks)
   #mw.form.menuTools.addAction(collapseAction)

   if mw_addon_view_menu_exists:
       mw.addon_view_menu.addSeparator()
       mw.addon_view_menu.addAction(expandAction)
       mw.addon_view_menu.addAction(collapseAction)
       mw.addon_view_menu.addSeparator()

#####################################################
#
if A['ONESIDED_CARDS'][0]:

    onesided_action = QAction(mw)
    onesided_action.setText(u'Показывать &Только Оборотные Стороны' if lang=='ru' else _(u"Show BackSides &Only"))
    onesided_action.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'onesided.png')))
    onesided_action.setCheckable(True)
    onesided_action.setChecked(False)

if A['FLIP_FLOP'][0]: 

    show_question_aukcion = QAction(mw)
    show_question_aukcion.setText(u'Перейти на &Лицевую Сторону' if lang=='ru' else _(u"Show &FrontSide"))
    show_question_aukcion.setIcon(PageUp_icon)
    #show_question_aukcion.setVisible(True)
    mw.connect(show_question_aukcion, SIGNAL("triggered()"), go_question)

    show_answer_aukcion = QAction(mw)
    show_answer_aukcion.setText(u'Перейти на &Оборотную Сторону' if lang=='ru' else _(u"Show &BackSide"))
    show_answer_aukcion.setIcon(PageDown_icon)
    mw.connect(show_answer_aukcion, SIGNAL("triggered()"), go_answer)

    show_question_action = QAction(mw)
    show_question_action.setText(u'Перейти на &Лицевую Сторону' if lang=='ru' else _(u"Show &FrontSide"))
    show_question_action.setShortcut(HOTKEY['FrontPack'][0])
    show_question_action.setIcon(PageUp_icon)
    #show_question_action.setVisible(True)
    mw.connect(show_question_action, SIGNAL("triggered()"), go_question)

    show_answer_action = QAction(mw)
    show_answer_action.setText(u'Перейти на &Оборотную Сторону' if lang=='ru' else _(u"Show &BackSide"))
    show_answer_action.setShortcut(HOTKEY['BackPack'][0]) 
    show_answer_action.setIcon(PageDown_icon)
    mw.connect(show_answer_action, SIGNAL("triggered()"), go_answer)

    if mw_addon_view_menu_exists:

      if A['NUMERIC_KEYPAD_REMAPPING'][0]:
        show_question_aktion = QAction(mw)
        show_question_aktion.setText(u'Показать &Лицевую Сторону' if lang=='ru' else _(u"Show &FrontSide"))
        show_question_aktion.setShortcut(HOTKEY['FrontPage'][0])
        if A['ANKI_MENU_ICONS'][0]:
            show_question_aktion.setIcon(PageUp_icon)
        mw.connect(show_question_aktion, SIGNAL("triggered()"), go_question)

        show_answer_aktion = QAction(mw)
        show_answer_aktion.setText(u'Показать &Оборотную Сторону' if lang=='ru' else _(u"Show &BackSide"))
        show_answer_aktion.setShortcut(HOTKEY['BackPage'][0])
        if A['ANKI_MENU_ICONS'][0]:
            show_answer_aktion.setIcon(PageDown_icon)
        mw.connect(show_answer_aktion, SIGNAL("triggered()"), go_answer)

        mw.addon_view_menu.addSeparator()
        mw.addon_view_menu.addAction(show_question_aktion)
        mw.addon_view_menu.addAction(show_answer_aktion)
        mw.addon_view_menu.addSeparator()

if A['FLIP_FLOP'][0]: 

    show_question_auktion = QAction(mw)
    show_question_auktion.setText(u'&Лицевая Сторона карточки' if lang=='ru' else _(u"Show &FrontSide"))
    show_question_auktion.setShortcut(HOTKEY['FrontSide'][0])
    if A['ANKI_MENU_ICONS'][0]:
        show_question_auktion.setIcon(PageUp_icon)
    mw.connect(show_question_auktion, SIGNAL("triggered()"), go_question)

    show_answer_auktion = QAction(mw)
    show_answer_auktion.setText(u'&Оборотная Сторона карточки' if lang=='ru' else _(u"Show &BackSide"))
    show_answer_auktion.setShortcut(HOTKEY['BackSide'][0])
    if A['ANKI_MENU_ICONS'][0]:
        show_answer_auktion.setIcon(PageDown_icon)
    mw.connect(show_answer_auktion, SIGNAL("triggered()"), go_answer)

if A['COLORFUL_TOOLBAR'][0]: 

    show_question_aukcion = QAction(mw)
    show_question_aukcion.setText(u'&Лицевая Сторона карточки' if lang=='ru' else _(u"Show &FrontSide"))
    show_question_aukcion.setIcon(PageUp_icon)
    mw.connect(show_question_aukcion, SIGNAL("triggered()"), go_question)

    show_answer_aukcion = QAction(mw)
    show_answer_aukcion.setText(u'&Оборотная Сторона карточки' if lang=='ru' else _(u"Show &BackSide"))
    show_answer_aukcion.setIcon(PageDown_icon)
    mw.connect(show_answer_aukcion, SIGNAL("triggered()"), go_answer)

if A['FLIP_FLOP'][0] and A['COLORFUL_TOOLBAR'][0] and mw_addon_cards_menu_exists: 

    mw.addon_cards_menu.addSeparator()
    mw.addon_cards_menu.addAction(show_question_auktion)
    mw.addon_cards_menu.addAction(show_answer_auktion)
    mw.addon_cards_menu.addSeparator()

if (A['FLIP_FLOP'][0] or A['ONESIDED_CARDS'][0]) and A['COLORFUL_TOOLBAR'][0]:

    mw.qt_tool_bar.addSeparator()
    if A['FLIP_FLOP'][0]:
        mw.qt_tool_bar.addAction(show_question_aukcion)
    if A['ONESIDED_CARDS'][0]:
        mw.qt_tool_bar.addAction(onesided_action)
    if A['FLIP_FLOP'][0]:
        mw.qt_tool_bar.addAction(show_answer_aukcion)
    mw.qt_tool_bar.addSeparator()

if mw_addon_go_menu_exists and (A['FLIP_FLOP'][0] or A['ONESIDED_CARDS'][0]):
    mw.addon_go_menu.addSeparator()
    if A['FLIP_FLOP'][0]:
        mw.addon_go_menu.addAction(show_question_action)
    if A['ONESIDED_CARDS'][0]:
        mw.addon_go_menu.addAction(onesided_action)
    if A['FLIP_FLOP'][0]:
        mw.addon_go_menu.addAction(show_answer_action)
    mw.addon_go_menu.addSeparator()

#################################
#
mw.form.menuTools.addSeparator() 

##########################################################################
# Card Browser Lookup
# https://ankiweb.net/shared/info/869824347

"""
Simple addon to quickly look up words in Anki's Browser

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)
Based on 'OSX Dictionary Lookup' by Eddie Blundell <eblundell@gmail.com>:
https://gist.github.com/eddie/ff3d820fb267ae26ca0e

License: The MIT License (MIT)
"""

class BrowserLookup:

  def get_selected(self, view):
    """Copy selected text"""
    return view.page().selectedText()

  def lookup_action(self, view):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    browser.form.searchEdit.lineEdit().setText(self.get_selected(view))
    browser.onSearch()

  def add_action(self, view, menu, action):
    """Add 'lookup' action to context menu."""
    if self.get_selected(view):
      action = menu.addAction(action)
      action.connect(action, SIGNAL('triggered()'),
        lambda view=view: self.lookup_action(view))

  def context_lookup_action(self, view, menu):

    edit_current_action = menu.addAction(u'Редактирование' if lang=='ru' else _(u"Edit"))
    edit_current_action.connect(edit_current_action, SIGNAL("triggered()"), go_edit_current)

    more_menu = QMenu(u'Ещё' if lang=='ru' else _(u"More"),menu)
    menu.addMenu(more_menu)

    for row in opts:
        if not row:
            more_menu.addSeparator()
            continue
        label, scut, func = row
        a = more_menu.addAction(label)
        a.setShortcut(QKeySequence(scut))
        a.connect(a, SIGNAL("triggered()"), func)

    """Browser Lookup action"""
    if A['SEARCH_BROWSER'][0]:
        #menu.addSeparator()
        self.add_action(view,menu,(u'Поиск в Обозревателе Anki: %s...' if lang == 'ru' else 'Search Anki Browser for %s...')%self.get_selected(view)[:20])

# Add lookup actions to context menu
if not B['B13_EDIT_MORE'][0] or A['SEARCH_BROWSER'][0]:
   browser_lookup = BrowserLookup()
   addHook("AnkiWebView.contextMenuEvent", browser_lookup.context_lookup_action)

##################################################################
# Search Google Images for selected words
# https://ankiweb.net/shared/info/800190862

"""
Adds Search For Selected Text to the Reviewer Window's context/popup menu

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Note: AnkiWebView.contextMenuEvent is replaced, but only to add a hook
which should make it easy to maintain.

Support: Use at your own risk. If you do find a problem please email me
or use one the following forums, however there are certain periods
throughout the year when I will not have time to do any work on
these addons.

Github page:  https://github.com/steveaw/anki_addons
Anki addons: https://groups.google.com/forum/?hl=en#!forum/anki-addons
"""

SEARCH_URL = 'https://www.google.com/search?tbm=isch&q=%s'

def selected_text_as_query(web_view):
    sel = web_view.page().selectedText()
    return " ".join(sel.split())

def on_search_for_selection_GOOGLE(web_view):
    sel_encode = selected_text_as_query(web_view).encode('utf8', 'ignore')
    #need to do this the long way around to avoid double % encoding
    url = QUrl.fromEncoded(SEARCH_URL % (urllib.quote(sel_encode)))
    #openLink(SEARCH_URL + sel_encode)
    QDesktopServices.openUrl(url)

def contextMenuEvent(self, evt):
    # lazy: only run in reviewer
    if aqt.mw.state != "review":
        return
    m = QMenu(self)
    a = m.addAction(_("Copy"))
    a.connect(a, SIGNAL("triggered()"),
          lambda: self.triggerPageAction(QWebPage.Copy))
    #Only change is the following statement
    runHook("AnkiWebView.contextMenuEvent",self,m)
    m.popup(QCursor.pos())

def insert_search_menu_action(anki_web_view,m):
    selected = selected_text_as_query(anki_web_view)
    if len(selected)>0:
        truncated = (selected[:40] + '...') if len(selected) > 40 else selected
        m.addSeparator()
        a = m.addAction(('Искать картинки "%s" в %s ' if lang == 'ru' else 'Search images of "%s" on %s ') \
            % (truncated, 'Google Images'))
        a.connect(a, SIGNAL("triggered()"),
            lambda wv=anki_web_view: on_search_for_selection_GOOGLE(wv))

##################################################################
# Get context sentence for language learning -Tatoeba lookup on right-click
# https://ankiweb.net/shared/info/800190862

# Stupid hack by me, to mimic https://ankiweb.net/shared/info/798922495 
# in order to show German -> English sentences (to provide more context for a given word/phrase).
# Defaults are setup to look for German->English sentences. 
# You could open the SEARCH_TATOEBA_for_selected_text_in_Reviewer python file 
# in your Anki addons folder and modify FROM_LNG and TO_LNG 
# in order to get any languages supported for the look up. 
# FROM_LNG = 'deu' 
# TO_LNG = 'eng'

"""
Adds Search For Selected Text to the Reviewer Window's context/popup menu

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
Changed to work with Tatoeba: <tatoeba_addon@chthonic.co.za>

Note: AnkiWebView.contextMenuEvent is replaced, but only to add a hook
which should make it easy to maintain.

Support: Use at your own risk. If you do find a problem please email me
or use one the following forums, however there are certain periods
throughout the year when I will not have time to do any work on
these addons.

Github page:  https://github.com/steveaw/anki_addons
Anki addons: https://groups.google.com/forum/?hl=en#!forum/anki-addons
"""

def on_search_for_selection_TATOEBA(web_view, vw):
    url = QUrl.fromEncoded(vw)
    QDesktopServices.openUrl(url)

def search_menu_action(anki_web_view,m,selected,server,search_url):
    truncated = (selected[:40] + '...') if len(selected) > 40 else selected
    if len(selected)>0:
      a = m.addAction(('Искать "%s" на %s ' if lang == 'ru' else 'Search for "%s" on %s ') % (truncated, server))
      a.connect(a, SIGNAL("triggered()"),
         lambda wv=anki_web_view: on_search_for_selection_TATOEBA(wv, search_url % (urllib.quote(selected_text_as_query(wv).encode('utf8', 'ignore')))))

def wiki_menu_action(anki_web_view,m,selected,server,search_url,lng):
    truncated = (selected[:40] + '...') if len(selected) > 40 else selected
    if len(selected)>0:
      a = m.addAction(('Найти "%s" на %s (%s) ' if lang == 'ru' else 'Look up for "%s" on %s (%s)') % (truncated, server, lng))
      a.connect(a, SIGNAL("triggered()"),
         lambda wv=anki_web_view: on_search_for_selection_TATOEBA(wv, search_url % (lng, urllib.quote(selected_text_as_query(wv).encode('utf8', 'ignore')))))

# yandex.com
def yandex_menu_action(anki_web_view,m,selected,server,search_url,lng,lng2):
    truncated = (selected[:40] + '...') if len(selected) > 40 else selected
    if len(selected)>0:
      a = m.addAction(('Заглянуть в %s в поисках "%s" (%s-%s) ' if lang == 'ru' else 'Look up on %s for "%s" (%s-%s)') % (server, truncated, lng, lng2))
      a.connect(a, SIGNAL("triggered()"),
         lambda wv=anki_web_view: on_search_for_selection_TATOEBA(wv, search_url % ( urllib.quote(selected_text_as_query(wv).encode('utf8', 'ignore')),lng,lng2)))

def translate_menu_action(anki_web_view,m,selected,server,search_url,from_lng,to_lng,dir=""):
    truncated = (selected[:40] + '...') if len(selected) > 40 else selected
    if len(selected)>0:
      if dir=="" or dir=="FROM":
        a = m.addAction(('Перевод "%s" на %s (%s->%s) ' if lang == 'ru' else 'Translate for "%s" on %s (%s->%s) ') % (truncated, server, from_lng, to_lng))
        a.connect(a, SIGNAL("triggered()"),
         lambda wv=anki_web_view: on_search_for_selection_TATOEBA(wv, search_url % (from_lng,to_lng,urllib.quote(selected_text_as_query(wv).encode('utf8', 'ignore')))))
      if dir=="" or dir=="TO":
        a = m.addAction(('Перевести "%s" на %s (%s->%s) ' if lang == 'ru' else 'Translation for "%s" on %s (%s->%s) ') % (truncated, server, to_lng, from_lng))
        a.connect(a, SIGNAL("triggered()"),
         lambda wv=anki_web_view: on_search_for_selection_TATOEBA(wv, search_url % (to_lng,from_lng,urllib.quote(selected_text_as_query(wv).encode('utf8', 'ignore')))))

def insert_search_menu_action_TATOEBA(anki_web_view, m):
    selected = selected_text_as_query(anki_web_view)
    if len(selected)>0:
        trans_menu = QMenu(u'Словари на сайтах' if lang=='ru' else u'Dictionaries online',m)
        m.addMenu(trans_menu)

        #translate_menu_action(anki_web_view, trans_menu, selected, 'Lingvo', 'http://www.lingvo.ua/ru/Translate/%s-%s/%s', FROM_LANG, TO_LANG) http://www.lingvo-online.ru/ru/Translate/en-ru/appliance
        
        # 'https://slovari.yandex.ru/%s/%s/'
        yandex_menu_action(anki_web_view, trans_menu, selected, 'Яндекс.Словари', 'https://slovari.yandex.ru/%s/%s-%s', TO_LANG, FROM_LANG) 
        trans_menu.addSeparator()

        translate_menu_action(anki_web_view, trans_menu, selected, 'Lingvo', 'http://www.lingvo-online.ru/ru/Translate/%s-%s/%s', FROM_LANG, TO_LANG) 
        trans_menu.addSeparator()

        wiki_menu_action(anki_web_view, trans_menu, selected, 'OLD', 'http://www.oxfordlearnersdictionaries.com/definition/%s/%s', FROM_LANGUAGE)
        wiki_menu_action(anki_web_view, trans_menu, selected, 'Oxford', 'http://www.oxfordlearnersdictionaries.com/definition/%s/%s', TO_LANGUAGE)
        trans_menu.addSeparator()

        search_menu_action(anki_web_view, trans_menu, selected, 'LDOCE', 'http://www.ldoceonline.com/search/?q=%s')
        search_menu_action(anki_web_view, trans_menu, selected, 'MW', 'http://www.merriam-webster.com/dictionary/%s')
        trans_menu.addSeparator()

        wiki_menu_action(anki_web_view, trans_menu, selected, 'CDO', 'http://dictionary.cambridge.org/dictionary/%s/%s', TO_LANGUAGE)
        translate_menu_action(anki_web_view, trans_menu, selected, 'CDO', 'http://dictionary.cambridge.org/dictionary/%s-%s/%s', FROM_LANGUAGE, TO_LANGUAGE) 

        search_menu_action(anki_web_view, m, selected, 'Google', 'https://www.google.com/search?q=%s')

        triad_menu = QMenu(u'Триада: Искать Перевод Татоэба' if lang=='ru' else _(u"Triad: Search Translation Tatoeba"),m)
        m.addMenu(triad_menu)

        search_menu_action(anki_web_view, triad_menu,    selected, 'Google', 'https://www.google.co.uk/search?q=%s')
        translate_menu_action(anki_web_view, triad_menu, selected, 'Google', 'https://translate.google.com/?sl=%s&tl=%s&q=%s', FROM_LANG, TO_LANG)
        triad_menu.addSeparator()
        search_menu_action(anki_web_view, triad_menu,    selected, 'Yandex', 'https://yandex.ru/yandsearch?text=%s')
        translate_menu_action(anki_web_view, triad_menu, selected, 'Yandex', 'https://translate.yandex.ru/?lang=%s-%s&text=%s', FROM_LANG, TO_LANG)
        triad_menu.addSeparator()
        search_menu_action(anki_web_view, triad_menu,    selected, 'Bing', 'https://www.bing.com/search?q=%s')
        translate_menu_action(anki_web_view, triad_menu, selected, 'Bing', 'https://www.bing.com/translator/?from=%s&to=%s&text=%s', FROM_LANG, TO_LANG)
        triad_menu.addSeparator()
        translate_menu_action(anki_web_view, triad_menu, selected, 'TATOEBA', 
            'http://tatoeba.org/eng/sentences/search?from=%s&to=%s&query=%s', FROM_LNG, TO_LNG)
        triad_menu.addSeparator()

        trans_menu.addSeparator()
        wiki_menu_action(anki_web_view, trans_menu, selected, 'The FREE Dictionary', 'http://%s.thefreedictionary.com/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, trans_menu, selected, 'The FREE Dictionary', 'http://%s.thefreedictionary.com/%s', TO_LANG)

        translate_menu_action(anki_web_view, m, selected, 'Yandex', 'https://translate.yandex.ru/?lang=%s-%s&text=%s', FROM_LANG, TO_LANG, dir="TO")

        wiki_main_menu = QMenu(u"Поиск по любой вики..." if lang=="ru" else u"Search any wiki...", m)
        m.addMenu(wiki_main_menu)

        wiki_menu_action(anki_web_view, wiki_main_menu, selected, 'Википедия', 'https://%s.wikipedia.org/wiki/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_main_menu, selected, 'Wikipedia', 'https://%s.wikipedia.org/wiki/%s', TO_LANG)

        wiki_menu = QMenu((u'Поиск по остальным вики (%s)' % FROM_LANG) if lang=='ru' else (u"Search wiki sites (%s)" % FROM_LANG), wiki_main_menu)
        wiki_main_menu.addMenu(wiki_menu)

        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wiktionary', 'https://%s.wiktionary.org/wiki/Special:Search/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wikibooks', 'https://%s.wikibooks.org/wiki/Special:Search/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wikiquote', 'https://%s.wikiquote.org/wiki/Special:Search/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wikisource', 'https://%s.wikisource.org/wiki/Special:Search/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wikiversity', 'https://%s.wikiversity.org/wiki/Special:Search/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wikivoyage', 'https://%s.wikivoyage.org/wiki/Special:Search/%s', FROM_LANG)
        wiki_menu_action(anki_web_view, wiki_menu, selected, 'wikinews', 'https://%s.wikinews.org/wiki/Special:Search/%s', FROM_LANG)

        viki_menu = QMenu(u"Search wiki sites (%s)" % TO_LANG, wiki_main_menu)
        wiki_main_menu.addMenu(viki_menu)

        wiki_menu_action(anki_web_view, viki_menu, selected, 'wiktionary', 'https://%s.wiktionary.org/wiki/Special:Search/%s', TO_LANG)
        wiki_menu_action(anki_web_view, viki_menu, selected, 'wikibooks', 'https://%s.wikibooks.org/wiki/Special:Search/%s', TO_LANG)
        wiki_menu_action(anki_web_view, viki_menu, selected, 'wikiquote', 'https://%s.wikiquote.org/wiki/Special:Search/%s', TO_LANG)
        wiki_menu_action(anki_web_view, viki_menu, selected, 'wikisource', 'https://%s.wikisource.org/wiki/Special:Search/%s', TO_LANG)
        wiki_menu_action(anki_web_view, viki_menu, selected, 'wikiversity', 'https://%s.wikiversity.org/wiki/Special:Search/%s', TO_LANG)
        wiki_menu_action(anki_web_view, viki_menu, selected, 'wikivoyage', 'https://%s.wikivoyage.org/wiki/Special:Search/%s', TO_LANG)
        wiki_menu_action(anki_web_view, viki_menu, selected, 'wikinews', 'https://%s.wikinews.org/wiki/Special:Search/%s', TO_LANG)

        wiki_menu_action(anki_web_view, wiki_main_menu, selected, 'wikidata', 'https://%s.wikidata.org/wiki/Special:Search/%s', 'www')
        wiki_menu_action(anki_web_view, wiki_main_menu, selected, 'wikimedia', 'https://%s.wikimedia.org/wiki/Special:Search/%s', 'commons')

        m.addSeparator()

if A['SEARCH_AND_TRANSLATE'][0]:
   AnkiWebView.contextMenuEvent = contextMenuEvent
   addHook("AnkiWebView.contextMenuEvent", insert_search_menu_action)
   AnkiWebView.contextMenuEvent = contextMenuEvent
   addHook("AnkiWebView.contextMenuEvent", insert_search_menu_action_TATOEBA)

#########################################################################
# Maximum images height in card editor
# https://ankiweb.net/shared/info/229181581

# Copyright (C) 2015 by Simone Gaiarin <simgunz@gmail.com>              #
#                                                                       #
# This program is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, see <http://www.gnu.org/licenses/>.  #

if A['MAXHEIGHT'][0]: #  = '200px'
    oldImgStyle = "img { max-width: 90%%; }"
    newImgStyle = "img { max-width: 90%%%%; max-height: %s; }" % A['MAXHEIGHT'][0]
    editor._html = editor._html.replace(oldImgStyle, newImgStyle)

##################################################################
# Search from Editor
# https://ankiweb.net/shared/info/1559436729

# Copyright: itraveller, 2014
# License: GNU AGPL v.3 or later

'''
This script is an add-on for Anki 2.0.28

Synopsis:
=========
This add-on is designed to search directly from the editor area, that is
particularly useful to quickly find:
1) duplicates of the added note
2) synonyms and homonyms of the added word

After installing you will find the 'S' button in the editor tool bar. When you
press it the entire contents of the active field (or its highlighted part) will
be sent to search box of the Anki browser. The search query looks like:
1) "<field name:><field content or its highlighted part>"
2) "<field name:>*<highlighted part>*"

Push the button while holding the 'Shift' if you want to search without
specifying the field name.
'''

import aqt.forms

def search_FE(self):
    '''Send the field content into the search box of the browser'''
    # check status of 'shift' key
    shift_key = QApplication.keyboardModifiers() == Qt.ShiftModifier
    # prepare search query
    selection = self.web.selectedText()
    fields = self.note.items()
    field_name, field_value = fields[self.currentField]
    content = '*' + selection + '*' if selection else field_value
    tag = '' if shift_key else field_name + ':'
    query = '"' + tag + content + '"'
    # invoke browser
    browser = aqt.dialogs.open("Browser", self.mw)
    browser.form.searchEdit.lineEdit().setText(query)
    browser.onSearch()

def button_FE(self):
    '''Create the 'S' button in the editor tool bar.'''
    self._addButton("mybutton", lambda s = self: search_FE(self), \
                    text = u"F", tip = "Искать в Обозревателе Anki ("+HOTKEYS['FE'][0]+")" if lang == 'ru' else "Find in Anki browser ("+HOTKEYS['FE'][0]+")", key = HOTKEYS['FE'][0])

if A['SEARCH_FROM_EDITOR'][0]:
   Editor.search = search_FE
   addHook("setupEditorButtons", button_FE)

##################################################################
# Reset card scheduling information / progress
# https://ankiweb.net/shared/info/1432861881

# Copyright: Jeffrey Baitis <jeff@baitis.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Col is a collection of cards, cids are the ids of the cards to reset.
if A['RESET_CARD_SCHEDULING'][0]:

  def resetSelectedCardScheduling(self):
    """ Resets statistics for selected cards, and removes them from learning queues. """
    cids = self.selectedCards()
    if not cids:
        return
    # Allow undo
    self.mw.checkpoint(_("Reset scheduling and learning on selected cards"))
    self.mw.progress.start(immediate=True)
    # Not sure if beginReset is required
    self.model.beginReset()

    # Removes card from learning queues
    self.col.sched.removeLrn(cids) # removeLrn call forgetCards by itself
    # Removes card from dynamic deck?
    self.col.sched.remFromDyn(cids)
    # Resets selected cards in current collection
    self.col.sched.resetCards(cids)

    self.model.endReset()
    self.mw.progress.finish()
    # Update the main UI window to reflect changes in card status
    self.mw.reset()

  def addMenuItem(self):
    """ Adds hook to the Edit menu in the note browser """
    action = QAction("Сброс расписания и просмотров выбранных карточек" if lang == 'ru' else "Reset scheduling and learning on selected cards", self)
    self.resetSelectedCardScheduling = resetSelectedCardScheduling
    self.connect(action, SIGNAL("triggered()"), lambda s=self: resetSelectedCardScheduling(self))
    self.form.menuEdit.addAction(action)

  # Add-in hook; called by the AQT Browser object when it is ready for the add-on to modify the menus
  addHook('browser.setupMenus', addMenuItem)

  # TODO: Eventually, this add-on should be able to be invoked from the deck browser
  # addHook('deckbrowser.setupOptions', addOptionsItem)

##################################################################
# anki-master\aqt\addons.py
#  Monkey Patching
#   showInfo -> tooltip

from aqt.addons import AddonManager, GetAddons
from aqt.downloader import download

if A['ADDONS_INSTALL_TOOLTIP'][0]:

  def _accept1(self):
    #go_AnkiWeb_addons() # This way starts after dialog window were closed, not before.
    QDialog.accept(self)
    # create downloader thread
    ret = download(self.mw, self.form.code.text())
    if not ret:
        return
    data, fname = ret
    self.mw.addonManager.install(data, fname)
    self.mw.progress.finish()
    tooltip(_("Download successful. Please restart Anki."),period=6000)
    #aqt.addons.AddonManager.onGetAddons(self.mw.addonManager) # TODO

  def _accepts(self):
      _accept1(self)
      aqt.addons.AddonManager.onGetAddons(self.mw.addonManager)

  aqt.addons.GetAddons.accept = _accept1

##################################################################
# Force custom font
# https://ankiweb.net/shared/info/2103013902

# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

def changeFont():
    f = QFontInfo(QFont(A['FONT'][0]))
    ws = QWebSettings.globalSettings()
    mw.fontHeight = A['FONTSIZE'][0] if A['FONTSIZE'][0] else f.pixelSize()
    mw.fontFamily = f.family()
    mw.fontHeightDelta = max(0, mw.fontHeight - 13)
    ws.setFontFamily(QWebSettings.StandardFont, mw.fontFamily)
    ws.setFontSize(QWebSettings.DefaultFontSize, mw.fontHeight)
    mw.reset()

if A['FONT'][0]:
   changeFont()

##################################################################
# ONESIDED_CARDS.py
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# monkey patch

def maybe_skip_question(self): 
    model = mw.reviewer.card.model()
    #if model['type'] != MODEL_STD:
    if model['type'] == MODEL_CLOZE:
        morda = 0
    else:
        morda = mw.reviewer.card.ord
    front = model['tmpls'][morda]['qfmt'].strip()
    back = model['tmpls'][morda]['afmt'].strip()

    global toBeerOrNot2Beer
    toBeerOrNot2Beer = onesided_action.isChecked() or \
        back in ['','{{FrontSide}}'] or front == back 

    self._reps += 1
    self.state = "question"
    self.typedAnswer = None
    self.typedAnswers = []
    c = self.card
    # grab the question and play audio
    if c.isEmpty():
        q = _("""\
The front of this card is empty. Please run Tools>Empty Cards.""")
    else:
        q = c.q()

    if not A['ONESIDED_CARDS'][0] or (A['ONESIDED_CARDS'][0] and not toBeerOrNot2Beer):
      if self.autoplay(c):
        playFromText(q)

    # render & update bottom
    q = self._mungeQA(q)
    klass = "card card%d" % (c.ord+1)
    self.web.eval("_updateQA(%s, false, '%s');" % (json.dumps(q), klass))
    self._toggleStar()
    if self._bottomReady:
        self._showAnswerButton()
    # if we have a type answer field, focus main web
    if self.typeCorrect:
        self.mw.web.setFocus()
    # user hook

    #if back == '': # permanently forever replace empty BackSide with {{FrontSide}} 
    #   mw.reviewer.card.model()['tmpls'][morda]['afmt'] = '{{FrontSide}}'
    #   # but for the current card empty answer still will be shown
    #   # -- avoid side effects! --

    runHook('showQuestion')

    if toBeerOrNot2Beer:
        try:
            # Currently, this seems to be the right thing to do.
            mw.reviewer.bottom.web.eval("py.link('ansHack');")
        except NameError:
            #mw.reviewer._showAnswer()
            try:
                mw.reviewer._showAnswer() #._showAnswerHack()
            except NameError:
                # Maybe next week we need this again.
                mw.reviewer._showAnswer()

def maybe_showAnswer(self):
        if self.mw.state != "review":
            # showing resetRequired screen; ignore space
            return
        self.state = "answer"
        c = self.card
        a = c.a()
        a = a.strip()

        model = mw.reviewer.card.model()
        if model['type'] == MODEL_CLOZE:
            morda = 0
        else:
            morda = mw.reviewer.card.ord
        if model['tmpls'][morda]['afmt'].strip() in ["",'{{FrontSide}}'] :
            a = c.q()
            a = a.strip()

        # play audio?
        if self.autoplay(c):
            playFromText(a)

        # render and update bottom
        a = self._mungeQA(a)
        self.web.eval("_updateQA(%s, true);" % json.dumps(a))
        self._showEaseButtons()
        # user hook
        runHook('showAnswer')

if A['ONESIDED_CARDS'][0]:
    Reviewer._showQuestion = maybe_skip_question
    Reviewer._showAnswer = maybe_showAnswer

#########################################################################################
#
# Copyright © 2013–2014  Roland Sieker <ospalh@gmail.com>
# --          COLORFUL_TOOLBARS.py
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Images:
#
# most icons from Anki1
#
# Exceptions:
# study.png,
# Found at http://www.vectorarts.net/vector-icons/free-study-book-icons/ ,
# "Free for Personal and Commercial Use"
#
# A few others, notably the 'bury', 'suspend', 'options', 'record' and
# 'play recorded' icons were found at openclipart.org:
# Free: http://creativecommons.org/publicdomain/zero/1.0/
#
# Others from other “public domain” images libraries.
# __version__ = "1.5.0"

"""
Add standard tool bars to Anki2.

This Anki2 addon adds standard tool bars (QtToolBar) to the Anki
main window. By default a few buttons (QActions) are added, more can
be added by the user.
"""

def edit_actions_off():
    """Switch off the edit actions."""
    global F9_HINT_PEEKED

    try:
        global edit_current_action, edit_layout_action, bury_note_action, toggle_mark_action, suspend_card_action, suspend_note_action, delete_action, show_more_tool_bar_action, bury_card_action

        edit_current_action.setEnabled(False)
        edit_layout_action.setEnabled(False)
        if A['F4_EDIT'][0]:
            F4_edit_current_action.setEnabled(False)
            F4_edit_layout_action.setEnabled(False)
        if A['FLIP_FLOP'][0]:
            show_question_action.setEnabled(False)
            show_answer_action.setEnabled(False)
            show_question_auktion.setEnabled(False)
            show_answer_auktion.setEnabled(False)
        toggle_last_card_action.setEnabled(False)
        if A['F3_CARD_INFO_DURING_REVIEW'][0]:
            F3_CARD_INFO_DURING_REVIEW_action.setEnabled(False)
        if A['F3_CARD_HISTORY'][0]:
            F3_CARD_HISTORY_action.setEnabled(False)
        if A['F9_HINT_PEEKING'][0]:
            show_all_hints_action.setEnabled(False)
            F9_HINT_PEEKING_action.setEnabled(False)
        eddit_current_action.setEnabled(False)
        if A['RESET_CARD_SCHEDULING'][0]:
            F2_FORGET_ME_NOT_action.setEnabled(False)
            F2_FORGET_ME_NOTE_action.setEnabled(False)
        if A['SET_INTERVAL'][0]:
            set_new_int_action.setEnabled(False)

        record_own_action.setEnabled(False)
        replay_own_action.setEnabled(False)

        toggle_last_card_action.setEnabled(False)

        if A['REBUILD_THEM_ALL'][0]:
            rebuild_all_action.setEnabled(True)
        if A['EXPAND_AND_COLLAPSE_DECKS'][0]:
            expandAction.setEnabled(True)
            collapseAction.setEnabled(True)

        toggle_mark_action.setEnabled(False)

        bury_card_action.setEnabled(False)
        bury_note_action.setEnabled(False)
        suspend_card_action.setEnabled(False)
        suspend_note_action.setEnabled(False)
        delete_action.setEnabled(False)

        replay_action.setEnabled(False)
        replay_audio_action.setEnabled(False)
        replay_all_audio_action.setEnabled(False)
        list_audio_action.setEnabled(False)
        mute_action.setEnabled(False)

        if A['F6_SOUND_KEY_MENU'][0]:
            pause_action.setEnabled(False)
            stop_action.setEnabled(False)
            forward_action.setEnabled(False)
            backward_action.setEnabled(False)
            if A['F6_FAST_SLOW'][0]:
                fast_action.setEnabled(False)
                slow_action.setEnabled(False)
                init_action.setEnabled(False)

    except AttributeError:
        pass

def edit_actions_on():
    #"""Switch on the edit actions."""
    try:
        global edit_current_action, edit_layout_action

        if A['REBUILD_THEM_ALL'][0]:
            rebuild_all_action.setEnabled(False)
        if A['EXPAND_AND_COLLAPSE_DECKS'][0]:
            expandAction.setEnabled(False)
            collapseAction.setEnabled(False)

    except AttributeError:
        pass

def maybe_more_tool_bar_on():
    #"""Show the more tool bar when we should."""
    global show_more_tool_bar_action, edit_layout_action, bury_note_action, toggle_mark_action, suspend_card_action, suspend_note_action, delete_action, bury_card_action

    show_more_tool_bar_action.setEnabled(True)

    toggle_mark_action.setEnabled(True)

    bury_card_action.setEnabled(True)
    bury_note_action.setEnabled(True)
    suspend_card_action.setEnabled(True)
    suspend_note_action.setEnabled(True)
    delete_action.setEnabled(True)

    edit_current_action.setEnabled(True)
    edit_layout_action.setEnabled(True)
    if A['F4_EDIT'][0]:
        F4_edit_current_action.setEnabled(True)
        F4_edit_layout_action.setEnabled(True)
    if A['FLIP_FLOP'][0]:
        show_question_action.setEnabled(True)
        show_answer_action.setEnabled(True)
        show_question_auktion.setEnabled(True)
        show_answer_auktion.setEnabled(True)

    if A['F3_CARD_INFO_DURING_REVIEW'][0]:
        F3_CARD_INFO_DURING_REVIEW_action.setEnabled(True)
    if A['F3_CARD_HISTORY'][0]:
        F3_CARD_HISTORY_action.setEnabled(True)
    if A['F9_HINT_PEEKING'][0]:
        show_all_hints_action.setEnabled(True)
        F9_HINT_PEEKING_action.setEnabled(True)
    eddit_current_action.setEnabled(True)
    if A['RESET_CARD_SCHEDULING'][0]:
        F2_FORGET_ME_NOT_action.setEnabled(True)
        F2_FORGET_ME_NOTE_action.setEnabled(True)
    if A['SET_INTERVAL'][0]:
        set_new_int_action.setEnabled(True)

    record_own_action.setEnabled(True)
    replay_own_action.setEnabled(True)

    if len(soundtrack_q_list)+len(soundtrack_a_list)>0:
        replay_action.setEnabled(True)
        replay_all_audio_action.setEnabled(True)
        replay_audio_action.setEnabled(True)
        list_audio_action.setEnabled(True)

        if A['F6_SOUND_KEY_MENU'][0]:
            pause_action.setEnabled(True)
            stop_action.setEnabled(True)
            forward_action.setEnabled(True)
            backward_action.setEnabled(True)
            if A['F6_FAST_SLOW'][0]:
                fast_action.setEnabled(True)
                slow_action.setEnabled(True)
                init_action.setEnabled(True)

    mute_action.setEnabled(True)

    toggle_last_card_action.setEnabled(True)

    if show_more_tool_bar_action.isChecked():
        try:
            mw.reviewer.more_tool_bar.show()
        except AttributeError:
            pass

def save_toolbars_visible():
    #"""Save if we should show the tool bars in the profile."""
    mw.pm.profile['ctb_show_toolbar'] = show_text_tool_bar_action.isChecked()
    mw.pm.profile['ctb_show_qt_toolbar'] = show_qt_tool_bar_action.isChecked()
    mw.pm.profile['ctb_show_more_toolbar'] = show_more_tool_bar_action.isChecked()

def save_toolbarz_visible():
    if A['ZOOM'][0]:
        mw.pm.profile['ctb_deck_browser_zoom'] = deck_browser_current_zoom
        mw.pm.profile['ctb_overview_zoom'] = overview_current_zoom
        mw.pm.profile['ctb_reviewer_zoom'] = reviewer_current_zoom

    mw.pm.profile['ctb_more_overview_stats'] = B['B00_MORE_OVERVIEW_STATS'][0]
    #
    mw.pm.profile['ctb_new_and_due'] = (B['B00_MORE_OVERVIEW_STATS'][0] > 1)
    mw.pm.profile['ctb_unseen_and_suspended'] = (B['B00_MORE_OVERVIEW_STATS'][0] > 2)
    mw.pm.profile['ctb_hide_big_numbers'] = B['B04_HIDE_BIG_NUMBERS'][0]
    mw.pm.profile['ctb_gear_at_end_of_line'] = B['B03_GEAR_AT_END_OF_LINE'][0]
    #
    mw.pm.profile['ctb_musthave_study'] = B['B05_STUDY_BUTTON'][0]
    #
    mw.pm.profile['ctb_wide_buttons'] = B['B06_WIDE_BUTTONS'][0]
    mw.pm.profile['ctb_color_buttons'] = B['B07_COLOR_BUTTONS'][0]
    mw.pm.profile['ctb_big_buttons'] = B['B08_BIG_BUTTONS'][0]
    mw.pm.profile['ctb_just_smiles'] = (BUTTON_LABELS_SMILES == BUTTON_LABELS)
    #
    mw.pm.profile['ctb_answer_confirmation'] = B['B10_ANSWER_CONFIRMATION'][0]
    mw.pm.profile['ctb_titles'] = B['B11_BUTTON_TITLES'][0]
    mw.pm.profile['ctb_hard7'] = B['B12_HARD7'][0]
    mw.pm.profile['ctb_edit_more'] = B['B13_EDIT_MORE'][0]

def load_toolbars_visible():
    # Show the right tool bars.

    # Get the state if we should show the tool bars from the profile or
    # use default values. Then show or do not show those tool bars.

    try:
        ttb_on = mw.pm.profile['ctb_show_toolbar']
    except KeyError:
        ttb_on = False
    show_text_tool_bar_action.setChecked(ttb_on)
    toggle_text_tool_bar()

    try:
        qtb_on = mw.pm.profile['ctb_show_qt_toolbar']
    except KeyError:
        qtb_on = True
    show_qt_tool_bar_action.setChecked(qtb_on)
    toggle_qt_tool_bar()

    try:
        mtb_on = mw.pm.profile['ctb_show_more_toolbar']
    except KeyError:
        mtb_on = True
    show_more_tool_bar_action.setChecked(mtb_on)

    # Don't toggle the more tool bar yet. It would be shown on the
    # deck browser screen
    # toggle_more_tool_bar()

def load_toolbarz_visible():

    global deck_browser_current_zoom, overview_current_zoom, reviewer_current_zoom
    global A, B, BUTTON_LABELS

    try:
        key_value = mw.pm.profile['ctb_deck_browser_zoom']
        if A['ZOOM'][0]:
            deck_browser_current_zoom = key_value
    except KeyError:
        pass
    #    deck_browser_current_zoom = deck_browser_standard_zoom

    try:
        key_value = mw.pm.profile['ctb_overview_zoom']
        if A['ZOOM'][0]:
            overview_current_zoom = key_value
    except KeyError:
        pass
    #   overview_current_zoom = overview_standard_zoom

    try:
        key_value = mw.pm.profile['ctb_reviewer_zoom']
        if A['ZOOM'][0]:
            reviewer_current_zoom = key_value
    except KeyError:
        pass
    #   reviewer_current_zoom = reviewer_standard_zoom

    current_reset_zoom()

    # -- IEWL

    try:
        next_key1 = mw.pm.profile['ctb_more_overview_stats']
    except KeyError:
        next_key1 = 0
    if next_key1:
        B['B00_MORE_OVERVIEW_STATS'][0] = 3
    else:
        B['B00_MORE_OVERVIEW_STATS'][0] = 0

    if B['B00_MORE_OVERVIEW_STATS'][0]:
     try:
        next_key2 = mw.pm.profile['ctb_unseen_and_suspended']
     except KeyError:
        next_key2 = True
     if next_key2:
        B['B00_MORE_OVERVIEW_STATS'][0] = 3
     else:
        B['B00_MORE_OVERVIEW_STATS'][0] = 2

     try:
        next_key = mw.pm.profile['ctb_new_and_due']
     except KeyError:
        next_key = True
     if next_key:
        if next_key2:
            B['B00_MORE_OVERVIEW_STATS'][0] = 3
        else:
            B['B00_MORE_OVERVIEW_STATS'][0] = 2
     else:
        B['B00_MORE_OVERVIEW_STATS'][0] = 1

    try:
        key_value = mw.pm.profile['ctb_hide_big_numbers']
        B['B04_HIDE_BIG_NUMBERS'][0] = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['ctb_gear_at_end_of_line']
        B['B03_GEAR_AT_END_OF_LINE'][0] = key_value
    except KeyError:
        pass

    # -- 

    try:
        key_value = mw.pm.profile['ctb_musthave_study']
        B['B05_STUDY_BUTTON'][0] = key_value
    except KeyError:
        pass

    # -- 

    try:
        key_value = mw.pm.profile['ctb_wide_buttons']
        B['B06_WIDE_BUTTONS'][0] = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['ctb_color_buttons']
        B['B07_COLOR_BUTTONS'][0] = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['ctb_big_buttons']
        B['B08_BIG_BUTTONS'][0] = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['ctb_just_smiles']
    except KeyError:
        key_value = (BUTTON_LABELS_SMILES == BUTTON_LABELS)
    #
    if key_value:
            BUTTON_LABELS = BUTTON_LABELS_SMILES
    else:
            BUTTON_LABELS = BUTTON_LABELS_LANG

    # -- 
    try:
        key_value = mw.pm.profile['ctb_answer_confirmation']
        B['B10_ANSWER_CONFIRMATION'][0] = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['ctb_titles']
        B['B11_BUTTON_TITLES'][0] = key_value
    except KeyError:
        pass

    try:
        key_value = mw.pm.profile['ctb_hard7']
        B['B12_HARD7'][0] = key_value
    except KeyError:
        pass
    
    try:
        key_value = mw.pm.profile['ctb_edit_more']
        B['B13_EDIT_MORE'][0] = key_value
        initEditMore(B['B13_EDIT_MORE'][0])
    except KeyError:
        pass
    
    #if B['B00_MORE_OVERVIEW_STATS'][0]:
    musthave_setup_menu(2)
    overview_init()
    initDeckBro()

    if mw.state == "deckBrowser":
        mw.moveToState("deckBrowser")
    if mw.state == "overview":
        mw.moveToState("overview")
    if mw.state == "review":
        mw.moveToState("review")

# -- 

def update_mark_action():
    """Set the state of the mark action to the marked state of the note."""
    toggle_mark_action.setChecked(mw.reviewer.card.note().hasTag("marked"))

def next_card_toggle_off():
    """Switch the next card action off."""
    toggle_last_card_action.setChecked(False)

def maybe_autoplay(reviewer, card):
    """Return whether we should play the sound on card flips."""

    # Return False when we have swiched on mute, the standard autoplay state otherwise.
    if not mute_action.isChecked():
        return False
    return reviewer.mw.col.decks.confForDid(card.odid or card.did)['autoplay']

if A['ANKI_MENU_ICONS'][0] or A['COLORFUL_TOOLBAR'][0]: 
    mw.form.actionUndo.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'undo.png')))

if A['ANKI_MENU_ICONS'][0]: 
    ## Add images to actions we already have. I skip a few where no icon really fits.
    mw.form.actionDocumentation.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'help.png')))
    mw.form.actionDonate.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'donate.png')))
    mw.form.actionAbout.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'anki.png')))

    mw.form.actionSwitchProfile.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'switch-profile.png')))
    mw.form.actionImport.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'import.png')))
    mw.form.actionExport.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'export.png')))
    mw.form.actionExit.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'exit.png')))

    mw.form.actionDownloadSharedPlugin.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'download-addon.png')))
    mw.form.actionDownloadSharedPlugin.setShortcut(QKeySequence(HOTKEY['download_addon'][0]))

    mw.form.actionFullDatabaseCheck.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'check-db.png')))
    mw.form.actionPreferences.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'preferences.png')))

    mw.form.actionStudyDeck.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'decks.png')))
    mw.form.actionStudyDeck.setShortcut(HOTKEYZ['Study_deck'][0])

    mw.form.actionCreateFiltered.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'filter.png')))
    mw.form.actionCheckMediaDatabase.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'media.png')))
    mw.form.actionEmptyCards.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'empty.png')))
    mw.form.actionNoteTypes.setIcon(QIcon(os.path.join(MUSTHAVE_COLOR_ICONS, 'bug.png')))

# Wrapper to not show a next card.
Reviewer.autoplay = maybe_autoplay

#if B['B00_MORE_OVERVIEW_STATS'][0]:
if not HIDE_THEM_ALL:
    addHook("unloadProfile", save_toolbarz_visible)
    addHook("profileLoaded", load_toolbarz_visible)

if A['COLORFUL_TOOLBAR'][0]:

    mw.deckBrowser.show = wrap(mw.deckBrowser.show, edit_actions_off)
    mw.overview.show = wrap(mw.overview.show, edit_actions_on)
    mw.reviewer.show = wrap(mw.reviewer.show, edit_actions_on)
    mw.reviewer.show = wrap(mw.reviewer.show, maybe_more_tool_bar_on)
    mw.overview.show = wrap(mw.overview.show, more_tool_bar_off)
    mw.reviewer._toggleStar = wrap(mw.reviewer._toggleStar, update_mark_action)
    mw.deckBrowser.show = wrap(mw.deckBrowser.show, more_tool_bar_off)

    # Make sure we don't leave a stale last card button switched on
    addHook("reviewCleanup", next_card_toggle_off)

    addHook("unloadProfile", save_toolbars_visible)
    addHook("profileLoaded", load_toolbars_visible)

    if mw_addon_audio_menu_exists:
        mw.addon_audio_menu.addAction(mute_action)

        if A['REPLAY_BUTTONS_ON_CARD'][0]:
            mw.addon_audio_menu.addAction(replay_all_audio_action) 
            mw.addon_audio_menu.addAction(replay_audio_action) 
            mw.addon_audio_menu.addAction(list_audio_action) 

        mw.addon_audio_menu.addSeparator() 
        mw.addon_audio_menu.addAction(record_own_action)
        mw.addon_audio_menu.addAction(replay_own_action)
        mw.addon_audio_menu.addSeparator()

if A['F6_SOUND_KEY_MENU'][0]:
    mw.addon_audio_menu.addSeparator() 
    mw.addon_audio_menu.addAction(pause_action)
    mw.addon_audio_menu.addAction(stop_action)
    mw.addon_audio_menu.addAction(forward_action)
    mw.addon_audio_menu.addAction(backward_action)
    mw.addon_audio_menu.addSeparator() 
    if A['F6_FAST_SLOW'][0]:
        mw.addon_audio_menu.addAction(fast_action)
        mw.addon_audio_menu.addAction(slow_action)
        mw.addon_audio_menu.addAction(init_action)
        mw.addon_audio_menu.addSeparator() 

######################################################
#
if A['FLIP_FLOP'][0]: 
    if mw_addon_audio_menu_exists:
      if A['NUMERIC_KEYPAD_REMAPPING'][0]:

        snow_question_aktion = QAction(mw)
        snow_question_aktion.setText(u'На &Лицевую Сторону' if lang=='ru' else _(u"Show &FrontSide"))
        snow_question_aktion.setShortcut(HOTKEY['FrontUp'][0])
        if A['ANKI_MENU_ICONS'][0]:
            snow_question_aktion.setIcon(PageUp_icon)
        mw.connect(snow_question_aktion, SIGNAL("triggered()"), go_question)

        snow_answer_aktion = QAction(mw)
        snow_answer_aktion.setText(u'На &Оборотную Сторону' if lang=='ru' else _(u"Show &BackSide"))
        snow_answer_aktion.setShortcut(HOTKEY['BackDown'][0])
        if A['ANKI_MENU_ICONS'][0]:
            snow_answer_aktion.setIcon(PageDown_icon)
        mw.connect(snow_answer_aktion, SIGNAL("triggered()"), go_answer)

        mw.addon_audio_menu.addSeparator()
        mw.addon_audio_menu.addAction(snow_question_aktion)
        mw.addon_audio_menu.addAction(snow_answer_aktion)
        mw.addon_audio_menu.addSeparator()

#############################################################################################################
# Local CSS and DIY night mode
# https://ankiweb.net/shared/info/2587372325

# © copyright 2012 Roland Sieker <ospalh@gmail.com>
# Contains snippets of code from anki proper,
# written by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
# Insipired by CSS Modify Style-Sheet input by DAThomas

"""
Load local CSS and add it to the cards.

This is an add-on for Anki 2 SRS.
Load the file 'user_style.css' from the user’s profile folder
(e.g. "~/Anki/User 1/user_style.css") and add it to the cards, before
the style from the template.
"""

user_css_name = 'user_style.css'
"""File name of the user's CSS"""
css_encoding = 'utf-8'
"""Encoding of the user's CSS file"""
local_class = 'loc'
"""Class added to all cards"""

user_css = u'\n .G { color: gray; }\n .H { visibility: hidden; }\n .B { font-weight: bold; }\n .I { font-style: italic; }\n .reviewerhide, .n { display: none; } .s { font-size: smaller; } \n '
extra_class = None

def fix_body_class():
    # Add classes to body.

    # Add classes to the html body, so the local CSS mechanism works
    # together with CSS definitions for web review. Use
    # ".loc.card"—without space—for the card and ".loc .classNN"—with a
    # space—for sub-elements in you user_style.css.

    # Gather all the A-Za-z0-9_ characters from the template and model
    # names and add those as class.
    model = mw.reviewer.card.model()
    if model['type'] == MODEL_STD:
        template_nr = mw.reviewer.card.ord
    else:
        template_nr = 0

    template_class = re.sub(ur'[\W_]+', u'', model['tmpls'][template_nr]['name']).lower()
    model_class = re.sub(ur'[\W_]+', u'', model['name']).lower()

    stencil = ur'[~\"\'\`\,\.\@\:\;\#\!\?\$\%\^\&\*\(\)\+\=\/\\\|\{\}\<\>\[\]]+' # 
    stenc = ur'[\s]+'

    template_klass = re.sub(stencil, u'', model['tmpls'][template_nr]['name']) 
    template_klass = re.sub(stenc, u'_', template_klass) 
    model_klass = re.sub(stencil, u'', model['name']) 
    model_klass = re.sub(stenc, u'_', model_klass) 

    deck_klass = re.sub(SEPARATOR, '_', mw.col.decks.current()['name']) 
    deck_klass = re.sub(stencil, u'', deck_klass) 
    deck_klass = re.sub(stenc, u'_', deck_klass) 

    body_class = ur'{0} card card{1} template_{2} model_{3} card_{4} type_{5} deck_{6}'.format(
        local_class, mw.reviewer.card.ord + 1,
        template_class, model_class, template_klass, model_klass, deck_klass)

    try:
        body_class += ' ' + extra_class 
    except TypeError:
        pass

    htm_class = ' ' + \
     ( " queue_New" if mw.reviewer.card.queue == 0 else "" ) + \
     ( " queue_Reps" if mw.reviewer.card.reps > 0 else "" ) + \
     ( " queue_Lapses" if mw.reviewer.card.lapses > 0 else "" ) + \
     ( " queue_Learn" if mw.reviewer.card.queue == 1 and mw.reviewer.card.type == 1 else "" ) + \
     ( " queue_Relearn" if mw.reviewer.card.queue == 1 and mw.reviewer.card.type == 2 else "" ) + \
     ( " queue_Filtered" if mw.reviewer.card.queue == 0 and mw.reviewer.card.type == 2 else "" ) + \
     ( " queue_NextdayLearn" if mw.reviewer.card.queue == 3 and mw.reviewer.card.type == 1 else "" ) + \
     ( " queue_Review" if mw.reviewer.card.queue == 2 else "" ) + \
     ( " queue_Young" if mw.reviewer.card.queue == 2 and mw.reviewer.card.ivl < 21 else "" ) + \
     ( " queue_Mature" if mw.reviewer.card.queue == 2 and mw.reviewer.card.ivl > 20 else "" ) 
    if lang != 'en':
       htm_class += ' ' + \
        ( " "+_('queue')+"_"+_("New") if mw.reviewer.card.queue == 0 else "" ) +  \
        ( " "+_('queue')+"_"+_("Lapses") if mw.reviewer.card.lapses > 0 else "" ) + \
        ( " "+_('queue')+"_"+_("Learn") if mw.reviewer.card.queue == 1 and mw.reviewer.card.type == 1 else "" ) +  \
        ( " "+_('queue')+"_"+_("Relearn") if mw.reviewer.card.queue == 1 and mw.reviewer.card.type == 2 else "" ) +  \
        ( " "+_('queue')+"_"+_("Filtered") if mw.reviewer.card.queue == 0 and mw.reviewer.card.type == 2 else "" ) +  \
        ( " "+_('queue')+"_"+_("Review") if mw.reviewer.card.queue == 2 else "" ) + \
        ( " "+_('queue')+"_"+_("Young") if mw.reviewer.card.queue == 2 and mw.reviewer.card.ivl < 21 else "" ) + \
        ( " "+_('queue')+"_"+_("Mature") if mw.reviewer.card.queue == 2 and mw.reviewer.card.ivl > 20 else "" )
    #mw.web.eval(u"(function(){var d=document.documentElement.className;if(d.indexOf('%s')<0){document.documentElement.className+=' %s';}/*alert(document.documentElement.className);*/}())" % (htm_class,htm_class))
    # Anki keeps the only <html class=""> between cards.
    # It means it's not easy to use card's individual classes on html tag.
    # U must delete old classes each time before an assignment of a new one.

    deck_klass = ''
    decks_klass = 'deck'
    deck_klasses =  mw.col.decks.current()['name'].split(u'::')
    deck_ind = 0
    if len(deck_klasses) > 1:
        for next_klass in deck_klasses:
            deck_ind += 1
            next_klass = re.sub(stencil, u'', unicode(next_klass)) 
            next_klass = re.sub(stenc, u'_', next_klass) 
            if deck_ind < len(deck_klasses):
               decks_klass += '_' + next_klass
            deck_klass += 'deck_' + next_klass + ' '
            if deck_ind > 1 and deck_ind < len(deck_klasses):
               deck_klass += decks_klass + ' '
    deck_klass = deck_klass.strip()
    if len(deck_klass) > 0:
        deck_klass = ' ' + deck_klass

    tags_klass = ''
    for next_klass in mw.reviewer.card.note().tags:
        tag_klass = re.sub(SEPARATOR, '_', next_klass)
        tag_klass = re.sub(stencil, u'', tag_klass) 
        tag_klass = re.sub(stenc, u'_', tag_klass) 
        tag_klass = 'tag_' + tag_klass + ' '
        if tags_klass.find(tag_klass) == -1:
            tags_klass += tag_klass
        while next_klass.rfind(SEPARATOR)>-1:
            last_klass = next_klass.split(SEPARATOR)[-1]
            tag_klass = re.sub(SEPARATOR, '_', last_klass)
            tag_klass = re.sub(stencil, u'', tag_klass) 
            tag_klass = re.sub(stenc, u'_', tag_klass) 
            tag_klass = 'tag_' + tag_klass + ' '
            if tags_klass.find(tag_klass) == -1:
                tags_klass += tag_klass
            next_klass = SEPARATOR.join(next_klass.split(SEPARATOR)[:-1])
            tag_klass = re.sub(SEPARATOR, '_', next_klass)
            tag_klass = re.sub(stencil, u'', tag_klass) 
            tag_klass = re.sub(stenc, u'_', tag_klass) 
            tag_klass = 'tag_' + tag_klass + ' '
            if tags_klass.find(tag_klass) == -1:
                tags_klass += tag_klass
    tags_klass = tags_klass[:-1]

    frontSide = mw.reviewer.card.model()['tmpls'][0 if mw.reviewer.card.model()['type'] == MODEL_CLOZE else mw.reviewer.card.ord]['qfmt'].strip()
    backSide  = mw.reviewer.card.model()['tmpls'][0 if mw.reviewer.card.model()['type'] == MODEL_CLOZE else mw.reviewer.card.ord]['afmt'].strip()

    mw.web.eval(u"document.body.className = '{0} {1} {2} {3} {4} {5} {6}'.replace(/\s+/g,' ');".format(body_class, htm_class, deck_klass, tags_klass,
       (" onesided_card" + (" Односторонняя" if lang=='ru' else "")) if backSide == '{{FrontSide}}' or backSide == '' or backSide == frontSide or onesided_action.isChecked() else "",
       ( " note_Basic" if mw.reviewer.card.model()['type'] == MODEL_STD else " note_Cloze" ) +
       ( "" if lang == 'en' else ( " note_"+_("Cloze") if mw.reviewer.card.model()['type'] == MODEL_CLOZE else " note_"+_("Basic") ) ),
       "lang_" + lang
       ))

# loc card card1 
# template_oxfordpicturedictionaryinteractivem4r4m
# model_oxfordpicturedictionaryinteractivem4r4m
# card_OxfordPictureDictionary_Interactive-M4R4M
# note_Oxford_PictureDictionaryInteractive-M4R4M
# note: Oxford_Picture Dictionary Interactive. -M4R4M
# card: @Ox!f#o$r%d "P^ic&t*u(r)e" 'D+i=c:t;i,o|n/a\r?y_I[n]t{e}ra`c<t>ive'. -M4R4M

def get_user_css():
    """
    Load the user's CSS data from disk.
    """
    global user_css

    css_path = os.path.join(mw.pm.profileFolder(), "../addons/" + user_css_name)
    try:
        with open(css_path, 'r') as f:
            user_css += unicode(f.read(), css_encoding)
    except IOError:
        pass

    css_path = os.path.join(mw.pm.profileFolder(), "../" + user_css_name)
    try:
        with open(css_path, 'r') as f:
            user_css += unicode(f.read(), css_encoding)
    except IOError:
        pass

    css_path = os.path.join(mw.pm.profileFolder(), user_css_name)
    try:
        with open(css_path, 'r') as f:
            user_css += unicode(f.read(), css_encoding)
    except IOError:
        pass

def localized_card_css(self):
    """Set the css for a card"""
    return_css = u''
    if user_css:
        return_css = '\n<style>\n%s\n</style>' % user_css
    a = old_css(self)
    a = a.replace('</style>','\n</style>')
    return return_css + a.replace('<style>','\n<style>\n\n')

def set_extra_class(new_extra_class):
    """Set the varible so the extra class is used on the next card."""
    global extra_class
    extra_class = new_extra_class

def setup_menu():
    # Add a submenu to a view menu.

    # Add a submenu that lists the available extra classes to the view
    # menu, creating that menu when neccessary

    if extra_classes_list:
        mw.extra_class_submenu = QMenu(u'&Местные стили' if lang == 'ru' else '&Local CSS', mw) 
        # u"Mode (e&xtra class)", mw)

        if mw_addon_view_menu_exists:
            mw.addon_view_menu.addSeparator()
            mw.addon_view_menu.addMenu(mw.extra_class_submenu)

        action_group = QActionGroup(mw, exclusive=True)
        no_class_action = action_group.addAction(
            QAction('н&е использовать' if lang == 'ru' else '(n&one/standard)', mw, checkable=True))
        no_class_action.setChecked(True)
        mw.extra_class_submenu.addAction(no_class_action)
        mw.connect(no_class_action, SIGNAL("triggered()"),
                   lambda: set_extra_class(None))
        mw.extra_class_submenu.addSeparator()
        for ecd in extra_classes_list:
            nn_class_action = action_group.addAction(
                QAction(ecd['display'], mw, checkable=True))
            mw.extra_class_submenu.addAction(nn_class_action)
            mw.connect(nn_class_action, SIGNAL("triggered()"),
                       lambda ec=ecd['class']: set_extra_class(ec))

if A['LOCAL_CSS_AND_DIY_NIGHT_MODE'][0]:
   old_css = Card.css
   Card.css = localized_card_css
   hooks.addHook("showQuestion", fix_body_class)
   hooks.addHook("profileLoaded", get_user_css)
   setup_menu()

#####################################################################
# Frozen Fields add-on for Anki
# Original author: tmbb (https://github.com/tmbb)
# with changes by: Glutanimate (https://github.com/Glutanimate)
#
# Modifications:
# 2015-10-25 - added hotkeys for various actions

# A more convenient way to mark fields as sticky.
# Documentation and further info here:
# -- http://tmbb.bitbucket.org/frozen-fields/index.html
# Author Contact: tmbb@campus.ul.pt

# Snowflake Icon
icon_name = "flake"
icon_min_width = "24"

## Uncomment to use the Kubuntu icon instead of the snowflake icon
#icon_name = "frozen_26x28"
#icon_min_width = "28"

def addons_folder(): return mw.pm.addonFolder()

def icon_color(icon, ext="png"):
    return "'" + os.path.join(addons_folder(),
                              MUSTHAVE_COLOR_ICONS,
                              (icon + "_color." + ext)).replace("\\","/") + "'"

def icon_grayscale(icon, ext="png"):
    return "'" + os.path.join(addons_folder(),
                              MUSTHAVE_COLOR_ICONS,
                              (icon + "_grayscale." + ext)).replace("\\","/") + "'"

icon_js_code = """
function onFrozen(elem) {
    currentField = elem;
    py.run("frozen:" + currentField.id.substring(1));
}

function setFrozenFields(fields, frozen, focusTo) {
    var txt = "";
    for (var i=0; i<fields.length; i++) {
        var n = fields[i][0];
        var f = fields[i][1];
        if (!f) {
            f = "<br>";
        }
        txt += "<tr><td style='min-width:""" + icon_min_width + """'></td><td class=fname>{0}</td></tr><tr>".format(n);
        if (frozen[i]) {
            txt += "<td style='min-width:""" + icon_min_width + """'><div id=i{0} onclick='onFrozen(this);'><img src=""" + icon_color(icon_name) + """/></div></td>".format(i);
        }
        else {
            txt += "<td style='min-width:"""  + icon_min_width + """'><div id=i{0} onclick='onFrozen(this);'><img src=""" + icon_grayscale(icon_name) + """/></div></td>".format(i);
        }
        txt += "<td width=100%%>"
        txt += "<div id=f{0} onkeydown='onKey();' onmouseup='onKey();'".format(i);
        txt += " onfocus='onFocus(this);' onblur='onBlur();' class=field ";
        txt += "ondragover='onDragOver(this);' ";
        txt += "contentEditable=true class=field>{0}</div>".format(f);
        txt += "</td>"
        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100%%>"+txt+"</table>");
    if (!focusTo) {
        focusTo = 0;
    }
    if (focusTo >= 0) {
        $("#f"+focusTo).focus();
    }
};
"""

def myLoadNote(self):
    self.web.eval(icon_js_code)
    if self.stealFocus:
        field = self.currentField
    else:
        field = -1
    if not self._loaded:
        # will be loaded when page is ready
        return
    data = []
    for fld, val in self.note.items():
        data.append((fld, self.mw.col.media.escapeImages(val)))
    ###########################################################
    sticky = []
    model = self.note.model()
    for fld in model['flds']:
        sticky.append(fld['sticky'])
    ###########################################################
    self.web.eval("setFrozenFields(%s, %s, %d);" % (
        json.dumps(data), json.dumps(sticky), field))
    self.web.eval("setFonts(%s);" % (
        json.dumps(self.fonts())))
    self.checkValid()
    self.widget.show()
    if self.stealFocus:
        self.web.setFocus()

def myBridge(self, str):
    if str.startswith("frozen"):
        (cmd, txt) = str.split(":", 1)
        field_nr = int(txt)
        model = self.note.model()
        is_sticky = model['flds'][field_nr]['sticky']
        model['flds'][field_nr]['sticky'] = not is_sticky
        self.loadNote()

def resetFrozen(editor):
    myField = editor.currentField
    flds = editor.note.model()['flds']
    for n in range(len(editor.note.fields)):
        try:
            if  flds[n]['sticky']:
                flds[n]['sticky'] = not flds[n]['sticky']
        except IndexError:
            break
    editor.loadNote()
    editor.web.eval("focusField(%d);" % myField)

def toggleFrozen(editor):
    # myField = editor.currentField
    # flds = editor.note.model()['flds']
    # flds[myField]['sticky'] = not flds[myField]['sticky']
    myField = editor.currentField
    editor.web.eval("""py.run("frozen:%d");""" % myField)
    editor.loadNote()
    editor.web.eval("focusField(%d);" % myField)

def onSetupButtons(editor):
    # insert custom key sequences here:
    # e.g. QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_F) for Alt+Shift+F
    s = QShortcut(QKeySequence(HOTKEYS['Freeze'][0]), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleFrozen(editor))
    t = QShortcut(QKeySequence(HOTKEYS['Frozen'][0]), editor.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : resetFrozen(editor))

if A['FROZEN_FIELDS'][0]:
    addHook("setupEditorButtons", onSetupButtons)
    editor.Editor.loadNote = myLoadNote
    editor.Editor.bridge = wrap(editor.Editor.bridge, myBridge, 'before')

import aqt.editor

#############################################################
# Search cards based on review time
# https://ankiweb.net/shared/info/3262774902
# by: muflax <mail@muflax.com>, 2014

# Search for cards based on their review time.
#
# Use 'time' to search for cards based on their last review time, 'timeavg' for their average review time and 'timetotal' for their total review time. Time is in seconds, and it accepts comparisons like 'prop'.
#
# Examples:
#   'time:3' finds cards that took up to 3 seconds during the last review, i.e. very easy cards.
#   'timeavg:<=4.2' finds cards with less than 4.2 seconds review average.
#   'timetotal:>60' finds cards that took more than 1 minute to study over their lifetime.

def findTime(command, (interval, args)):
    query = interval

    # extract argument
    m = re.match("^(<=|>=|!=|=|<|>)?(\d+)$", query)
    if not m:
        # invalid input, ignore it
        return
    comparison, interval = m.groups()

    if not comparison:
        comparison = "<="

    # is interval a valid millisecond value?
    try:
        interval = int(float(interval) * 1000)
    except ValueError:
        return

    # query
    q = []
    # only valid for review/daily learning
    q.append("(c.queue in (2,3))")

    if command == "last":
        # get latest review of each card
        group = "select cid, max(id) as maxId  from revlog group by cid"
        cids = "select r.cid from revlog r inner join (%s) groupedr on r.id = groupedr.maxId" % group
        q.append("c.id in (%s where r.time %s %s)" % (cids, comparison, interval))
    elif command == "avg":
        # get average times
        group = "select cid, sum(time)/count() as avg from revlog group by cid"
        q.append("c.id in (select cid from (%s) where avg %s %s)" % (group, comparison, interval))
    elif command == "total":
        # get total times
        group = "select cid, sum(time) as total from revlog group by cid"
        q.append("c.id in (select cid from (%s) where total %s %s)" % (group, comparison, interval))
    else:
        # invalid command
        return

    return " and ".join(q)

def addFindTime(search):
    search["time"]      = lambda x: findTime("last", x)
    search["timelast"]  = lambda x: findTime("last", x)
    search["timeavg"]   = lambda x: findTime("avg", x)
    search["timetotal"] = lambda x: findTime("total", x)

if A['SEARCH_TIME'][0]:
    addHook("search", addFindTime)

##################################################################
# Small add cards dialog
# Small add carts dialog
# https://ankiweb.net/shared/info/3285086934
# Small_add_cards_dialog.py
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
# Just a quick hack. Remove the minimum size for the add card dialog. (Requested in the Anki Users group.)
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
# __version__ = '1.0.0'
# See the notes in the progress function

if A['SMALL_ADD_EDIT_DIALOGS'][0]:

    from aqt.addcards import AddCards

    def reset_min_size(self):
        """
        Undo the setting of the minimun size.
        """
        self.setMinimumWidth(100) # 400x300 addcards.py
        self.setMinimumHeight(50) # 500x400 editcurrent.py

    AddCards.setupEditor = wrap(AddCards.setupEditor, reset_min_size)

    # Should be default behavior.
    # Why a window would require a minimum size is beyond me.
    # I should be able to resize anything to whatever size I wish.
    # Thanks. --  ¡иɯʎdʞ ин ʞɐʞ 'ɐнɔɐdʞǝdu qнεиЖ 

    from aqt.editcurrent import EditCurrent

    EditCurrent.show = wrap(EditCurrent.show, reset_min_size, "before")

##################################################################
# Update Profile on first run

"""
if UPDATE_PROFILE and not mw.col.conf.get('musthaveInit',False):
    mw.col.conf['musthaveInit'] = True
    mw.col.conf['numBackups'] = 10
    mw.col.conf['compressBackups'] = False
    mw.col.conf['collapseTime'] = 0
    mw.col.setMod()
"""

##################################################################
# from AZERTY French keys support

AZERTY = [
    ['--handbook',"Справочник по Anki 2.0"],
    ['--musthave',"Must Have"],
    ['--musthave-options',"Must Have "+("— настройки" if lang=="ru" else _("Options"))],
    ['--musthave-stats',"Must Have "+("— статистика" if lang=="ru" else _("Statistics"))],
    ['dt', "Пора: ... повторений, ... новых карточек (Decks Total, dt) " if lang=="ru" else "Decks Total (dt)"],
]

# Prettier menu entry
def AZERTYrebuildAddonsMenu(self):
    global menu_titles
    for menu in self._menus:
        for QWERTY in AZERTY:
            if QWERTY[0] == menu.title():
                menu.setTitle(QWERTY[1])
                break
        else:
            menu.setTitle( menu.title().replace('_',' ') )
            menu_titles.append( menu.title().replace('_',' ') )

AddonManager.rebuildAddonsMenu = wrap(AddonManager.rebuildAddonsMenu,AZERTYrebuildAddonsMenu)

# --------------
# no <div style=font...>{{Field}}</div>
# in Edit Cards... by Add Field button
# only {{Field}}

if A['ADD_FIELDS_WITHOUT_DIV'][0]:
    def maddField(self, widg, field, font, size):
        t = widg.toPlainText()
        t +="\n{{%s}}\n" % (field)
        widg.setPlainText(t)
        self.saveCard()
    CardLayout._addField = maddField

###########################################################################################
# Multiple type fields on card
# https://ankiweb.net/shared/info/689574440
# This addon allows the user to specify multiple independent {{type:}} fields on one card.

# ==== Reviewer ====
#we only have to wrap init, since we can overwrite the assignment
def myInit(self, mw):
    oldInit(self, mw)
    self.typeCorrect = []


#This is only a constant attached to the reviewer which makes it easy to replace
myRevHtml = """
<img src="qrc:/icons/rating.png" id=star class=marked>
<div id=qa></div>
<script>
var ankiPlatform = "desktop";
var typetxts;
function _updateQA (q, answerMode, klass) {
    $("#qa").html(q);
    typetxts = document.getElementsByName("typetxt");
    if (typetxts.length > 0 && typetxts[0]) {
        typetxts[0].focus();
    }
    if (answerMode) {
        var e = $("#answer");
        if (e[0]) { e[0].scrollIntoView(); }
    } else {
        window.scrollTo(0, 0);
    }
    if (klass) {
        document.body.className = klass;
    }
    // don't allow drags of images, which cause them to be deleted
    $("img").attr("draggable", false);
};
function _toggleStar (show) {
    if (show) {
        $(".marked").show();
    } else {
        $(".marked").hide();
    }
};
function _getTypedText (num) {
    if (typetxts.length > num && typetxts[num]) {
        py.link("typeans:"+typetxts[num].value);
    }
};
function _typeAnsPress() {
    if (window.event.keyCode === 13) {
        py.link("ansHack");
    }
};
function _blurInput() {
    for (var i = 0; i < typetxts.length; ++i) {
        typetxts[i].blur();
    }
};
</script>
"""

#Sadly we cannot use the original code in the functions below this
def myTypeAnsFilter(self, buf):
    if self.state == "question":
        self.typeCorrect = []
        return self.typeAnsQuestionFilter(buf)
    else:
        return self.typeAnsAnswerFilter(buf, 0)


def myTypeAnsQuestionFilter(self, buf):
    clozeIdx = None
    m = re.search(self.typeAnsPat, buf)
    if not m:
        return buf
    fld = m.group(1)
    # if it's a cloze, extract data
    if fld.startswith("cloze:"):
        # get field and cloze position
        clozeIdx = self.card.ord + 1
        fld = fld.split(":")[1]
    # loop through fields for a match
    for f in self.card.model()['flds']:
        if f['name'] == fld:
            typeCorrect = self.card.note()[f['name']]
            if clozeIdx:
                # narrow to cloze
                typeCorrect = self._contentForCloze(
                    typeCorrect, clozeIdx)
            self.typeFont = f['font']
            self.typeSize = f['size']
            break
    if not typeCorrect:
        #append none, so AnsAnswer indices don't missmatch
        self.typeCorrect.append(None)
        if typeCorrect is None:
            if clozeIdx:
                warn = _("""\
Please run Tools>Empty Cards""")
            else:
                warn = _("Type answer: unknown field %s") % fld
            return re.sub(self.typeAnsPat, warn, buf)
        else:
            # empty field, remove type answer pattern
            return re.sub(self.typeAnsPat, "", buf)
    buf = re.sub(self.typeAnsPat, """
<center>
<input type=text id=typeans name=typetxt onkeypress="_typeAnsPress();"
style="font-family: '%s'; font-size: %spx;">
</center>
""" % (self.typeFont, self.typeSize), buf, 1)
    self.typeCorrect.append(typeCorrect)
    return self.typeAnsQuestionFilter(buf)

def myTypeAnsAnswerFilter(self, buf, i):
    if i >= len(self.typeCorrect):
        return re.sub(self.typeAnsPat, "", buf)
    # tell webview to call us back with the input content
    self.web.eval("_getTypedText(%d);" % i)
    origSize = len(buf)
    buf = buf.replace("<hr id=answer>", "")
    hadHR = len(buf) != origSize
    # munge correct value
    parser = HTMLParser.HTMLParser()
    cor = stripHTML(self.mw.col.media.strip(self.typeCorrect[i]))
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(" ", "&nbsp;")
    cor = parser.unescape(cor)
    cor = cor.replace(u"\xa0", " ")
    given = self.typedAnswer
    # compare with typed answer
    #res = self.correct(given.strip().lower(), cor.strip().lower(), showBad=False)
    res = self.correct(given.strip(), cor.strip(), showBad=False)
    # and update the type answer area
    def repl(match):
        # can't pass a string in directly, and can't use re.escape as it
        # escapes too much
        s = """
<span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
            self.typeFont, self.typeSize, res)
        if hadHR:
            # a hack to ensure the q/a separator falls before the answer
            # comparison when user is using {{FrontSide}}
            s = "<hr id=answer>" + s
        return s
    buf = re.sub(self.typeAnsPat, repl, buf, 1)
    return self.typeAnsAnswerFilter(buf, i + 1)

def myCatchEsc(self, evt):
   if evt.key() == Qt.Key_Escape:
      self.web.eval("_blurInput();")
      return True

# ==== CLayout ====
def myMaybeTextInput(self, txt, type='q'):
    ret = oldMaybeTextInput(self, txt, type)
    if type == 'q':
        ret = re.sub("id='typeans'", "id='typeans' name='typetxt'", ret)
    return ret

if A['MULTIPLE_TYPING'][0]:

    # old style wrap
    oldInit = Reviewer.__init__
    Reviewer.__init__ = myInit

    # monkey patch
    Reviewer._revHtml = myRevHtml
    Reviewer.typeAnsFilter = myTypeAnsFilter
    Reviewer.typeAnsQuestionFilter = myTypeAnsQuestionFilter
    Reviewer.typeAnsAnswerFilter = myTypeAnsAnswerFilter
    Reviewer._catchEsc = myCatchEsc

    oldMaybeTextInput = CardLayout.maybeTextInput
    CardLayout.maybeTextInput = myMaybeTextInput


##################################################################
# Select_Buttons_Automatically_If_Correct_Answer_Wrong_Answer_or_Nothing.py
# https://ankiweb.net/shared/info/2074758752
# Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing

def JustDoIt(parm):
    try:
        arg = stripHTML(mw.col.media.strip(unicode(parm)))
        arg = parm.replace(" ", "&nbsp;")
    except UnicodeDecodeError:
        arg = ''
    # ensure we don't chomp multiple whitespace
    arg = HTMLParser.HTMLParser().unescape(arg) 
    return arg #unicode(arg.replace(u"\xa0", " ")) #arg

def myDefaultEase(self, _old):
  #if self.mw.reviewer.state == 'question': # на стороне вопроса не делать ничего - там данные от прошлой карточки
  #    return _old(self)
  #tooltip(self.mw.reviewer.state) # it's always called on answer side, but three times

  given = ''
  if hasattr(self, 'typedAnswer'):
   if hasattr(self, 'typeCorrect'):
    if self.typeCorrect: # not None
     if hasattr(self, 'typedAnswers'):

        self.typedAnswer = JustDoIt(unicode(self.typedAnswer))
        if not len(self.typedAnswers):
            gvn = [self.typedAnswer]
        else:
          for i in range(len(self.typedAnswers)): 
            self.typedAnswers[i] = JustDoIt(unicode(self.typedAnswers[i]))
          gvn = self.typedAnswers

        if not type(self.typeCorrect) is list:
            self.typeCorrect = JustDoIt(unicode(self.typeCorrect).encode('utf-8'))
            cor = [self.typeCorrect] 
            # in native Anki it is a string
        else:
          for i in range(len(self.typeCorrect)): 
            # <div>Indiana</div> It happens very often after unexpected pushing Enter key.
            self.typeCorrect[i] = JustDoIt(stripHTML(unicode(self.typeCorrect[i]).encode('utf-8')))
          cor = self.typeCorrect
          # with Multiple_type_fields_on_card.py it becomes a list of strings

        """
        tmp = '' +\
            unicode(self.typedAnswers) + '<br>' +\
            unicode(self.typeCorrect) + '<br>' +\
            unicode(str(self.typedAnswers)) + '<br>' +\
            unicode(str(self.typeCorrect)) + '<br>' +\
            unicode(unicode(self.typedAnswers)) + '<br>' +\
            unicode(unicode(self.typeCorrect)) + '<br>' +\
            unicode(gvn) + '<br>' +\
            unicode(cor) + '<br>'
        if len(gvn)>0:
            tmp += '' +\
            unicode(gvn[len(gvn)-1]) + '<br>' +\
            unicode(cor[len(cor)-1]) + '<br>' +\
            unicode(len(gvn[len(gvn)-1])) + '<br>' +\
            unicode(len(cor[len(cor)-1])) + '<br>' +\
            unicode(str(gvn[len(gvn)-1]==cor[len(cor)-1])) + '<br>' 
        showInfo(self.typedAnswer + '<br>' + tmp)
        """

        if (len(gvn)==0): 
            res = False
        else:
            if (len(gvn)>1 and len(gvn) != len(cor)): # something went wrong
                res = False
            else:
                if (len(gvn)==1):
                    #res = gvn[len(gvn)-1].strip().lower()==cor[len(cor)-1].strip().lower()
                    res = gvn[len(gvn)-1].strip()==cor[len(cor)-1].strip()
                else:
                    res = True
                    for i in range(0,len(cor)):
                        gvn[i] = gvn[i].strip() #.lower()
                        cor[i] = cor[i].strip() #.lower()
                        #gvn[i] = JustDoIt(gvn[i])
                        #cor[i] = JustDoIt(cor[i])
                        if (gvn[i]  !=  "" and gvn[i]  !=  cor[i]):
                            res = False
                        if (gvn[i]  !=  ""):
                            given += gvn[i]

        if not F9_HINT_PEEKED and ( res or \
            given == '' and ( toBeerOrNot2Beer or altMW_action.isChecked() or shiftMW_action.isChecked() ) ):
            #tooltip ('F9_HINT_PEEKED 32...')
            if self.mw.col.sched.answerButtons(self.card) == 4:
                retv = 3
            else:
                retv = 2
        else:
            #showWarning('F9_HINT_PEEKED 21... %s, %s, %s, %s, %s, %s ' % ( F9_HINT_PEEKED,res,given,toBeerOrNot2Beer,altMW_action.isChecked(),shiftMW_action.isChecked() ))
            if self.mw.col.sched.answerButtons(self.card) == 4 and B['B12_HARD7'][0]:
                retv = 2
            else:
                retv = 1

     else:
         #tooltip ('No typedAnswers')
         retv = _old(self)
    else:
        #tooltip ('typeCorrect is None')
        retv = _old(self)
   else:
       #tooltip ('No typeCorrect')
       retv = _old(self)
  else:
      #tooltip ('No typedAnswer')
      retv = _old(self)

  #showCritical('retv = '+unicode(retv))
  return retv

if A['MULTIPLE_TYPING'][0]:
    Reviewer._defaultEase = wrap(Reviewer._defaultEase, myDefaultEase, "around")

##################################################################
# Timebox tooltip
# https://ankiweb.net/shared/info/2014169675

from aqt.reviewer import Reviewer
from aqt.utils import tooltip 
from anki.sound import playFromText, clearAudioQueue, play

if A['TIMEBOX_TOOLTIP'][0]:

  # anki/collection.py
  """
    def timeboxReached(self):
        "Return (elapsedTime, reps) if timebox reached, or False."
        if not self.conf['timeLim']:
            # timeboxing disabled
            return False
        elapsed = time.time() - self._startTime
        if elapsed > self.conf['timeLim']:
            return (self.conf['timeLim'], self.sched.reps - self._startReps)
  """

  # aqt/reviewer.py Monkey Patch
  def maNextCard(self,_old):
    global F9_HINT_PEEKED

    if A['COLORFUL_TOOLBAR'][0]:
     if toggle_last_card_action.isChecked():
        clearAudioQueue()
        toggle_last_card_action.setChecked(False)
        self.mw.moveToState("overview")
        return True

    elapsed = self.mw.col.timeboxReached()
    if elapsed:
        part1 = ngettext("%d card studied in", "%d cards studied in", elapsed[1]) % elapsed[1]
        mins = int(round(elapsed[0]/60))
        part2 = ngettext("%s minute.", "%s minutes.", mins) % mins
        tooltip("<b style=font-size:larger;color:blue;font-weight:bold;> %s <span style=color:red>%s</span> </b><br><br> %s" % ( part1, part2, answerCard_LA if B['B10_ANSWER_CONFIRMATION'][0] else '' ), period=6000) 
        self.mw.col.startTimebox()
    if self.cardQueue:
        # undone/edited cards to show
        c = self.cardQueue.pop()
        c.startTimer()
        self.hadCardQueue = True
    else:
        if self.hadCardQueue:
            # the undone/edited cards may be sitting in the regular queue;
            # need to reset
            self.mw.col.reset()
            self.hadCardQueue = False
        c = self.mw.col.sched.getCard()

    self.card = c
    clearAudioQueue()
    if not c:
        self.mw.moveToState("overview")
        return

    if self._reps is None or self._reps % 100 == 0:
        # we recycle the webview periodically so webkit can free memory
        F9_HINT_PEEKED = False
        self._initWeb()
    else:
        F9_HINT_PEEKED = False
        self._showQuestion() #._initWeb() # 

  Reviewer.nextCard = wrap( Reviewer.nextCard, maNextCard, "around" )

# Bottom area
######################################################################

def my_renderBottom(self):
    links = [
        ["O", "opts", _("Options")],
    ]
    if self.mw.col.decks.current()['dyn']:
        links.append(["R", "refresh", _("Rebuild")])
        links.append(["E", "empty", _("Empty")])
    else:
        links.append(["C", "studymore", _("Custom Study")])
        #links.append(["F", "cram", _("Filter/Cram")])
    if self.mw.col.sched.haveBuried():
        links.append(["U", "unbury", _("Unbury")])
    buf = ""
    for b in links:
        if b[0]:
            b[0] = _("Shortcut key: %s") % shortcut(b[0])
        buf += """
<button title="%s" onclick='py.link(\"%s\");'>%s</button>""" % tuple(b)
    self.bottom.draw(buf)
    if isMac:
        size = 28
    else:
        size = 36 + self.mw.fontHeightDelta*3
    self.bottom.web.setFixedHeight(size)
    self.bottom.web.setLinkHandler(self._linkHandler)

# Studying more
######################################################################

def ma_haveBuried(self, did):
    sdids = ids2str(did)
    cnt = self.mw.col.db.scalar(
        "select 1 from cards where queue = -2 and did in %s limit 1" % sdids)
    return not not cnt

def my_onUnbury(self,did):
    import aqt.customstudy
    self.mw.col.decks.select(did) #self.col.decks.id(ret.name))
    self.mw.moveToState("overview")
    self.mw.col.sched.unburyCardsForDeck()
    self.mw.reset()

def my_onStudyMore(self,did):
    import aqt.customstudy
    self.mw.col.decks.select(did) #self.col.decks.id(ret.name))
    self.mw.moveToState("overview")
    aqt.customstudy.CustomStudy(self.mw)
    self.mw.reset()

def my_onRebuild(self,did):
    self.mw.col.decks.select(did) 
    self.mw.moveToState("overview")
    self.mw.col.sched.rebuildDyn()
    self.mw.reset()

def my_onEmpty(self,did):
    self.mw.col.decks.select(did)
    #self.mw.moveToState("overview")
    self.mw.col.sched.emptyDyn(self.mw.col.decks.selected())
    self.mw.reset()

def my_onRescheduleDeck(self,did):
  if askUser(u"Сбросить расписание для всех карточек данной колоды?" if lang=="ru" else "Reschedule all cards of current deck?"):
    self.mw.checkpoint(_("Forget"))

    self.mw.col.decks.select(did)
    self.mw.moveToState("overview")

    self.mw.col.sched.removeLrn(   sorted(self.mw.col.decks.cids(did, children=True)) )
    self.mw.col.sched.remFromDyn(  sorted(self.mw.col.decks.cids(did, children=True)) )
    self.mw.col.sched.resetCards(  sorted(self.mw.col.decks.cids(did, children=True)) )

    tooltip(u"Карточки колоды поставлены в конец очереди новых карточек." if lang=="ru" else _("Cards of deck are rescheduled as new"))
    self.mw.reset()

# Options
##########################################################################

def my_showOptions(self, did):
    m = QMenu(self.mw)
    a = m.addAction(_("Study"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: my_studyDeck(self, did))
    if self.mw.col.decks.get(did)['dyn']:
        a = m.addAction(_("Rebuild"))
        a.connect(a, SIGNAL("triggered()"), lambda did=did: my_onRebuild(self, did))
        a = m.addAction(_("Empty"))
        a.connect(a, SIGNAL("triggered()"), lambda did=did: my_onEmpty(self, did))
        pass
    else:
        a = m.addAction(_("Custom Study"))
        a.connect(a, SIGNAL("triggered()"), lambda did=did: my_onStudyMore(self, did)) #self._rename(did))
        if ma_haveBuried(self, [did]):
            a = m.addAction(_("Unbury"))
            a.connect(a, SIGNAL("triggered()"), lambda did=did: my_onUnbury(self, did)) 
    a = m.addSeparator()
    #
    a = m.addAction(_("Rename"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._rename(did))
    a = m.addAction(_("Options"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._options(did))
    a = m.addAction(_("Export"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._export(did))
    a = m.addAction(_("Delete"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._delete(did))
    #
    if A['RESET_CARD_SCHEDULING'][0]:
        a = m.addSeparator() 
        a = m.addAction((u"Сбросить расписание" if lang=="ru" else "Reschedule all cards"))
        a.connect(a, SIGNAL("triggered()"), lambda did=did: my_onRescheduleDeck(self, did))
    #
    m.exec_(QCursor.pos())

DeckBrowser._showOptions = my_showOptions

##################################################################
# • day learning cards always before new

# By default Anki do so:
#  learning; new if before; due; day learning; new if after
# With this add-on card will be displayed in the following order:
#  learning; (day learning; new) if before; due; (day learning; new) if after

# Normally these cards go after due, but I want them to go before new. 

# If Tools -> Preferences... -> Basic -> Show new cards before reviews
#    learning; day learning; new; due
# If Tools -> Preferences... -> Basic -> Show new cards after reviews
#    learning; due; day learning; new

# inspired by Anki user rjgoif
# https://ankiweb.net/shared/info/1810271825
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# put ALL due "learning" cards first ×
# ####################################################################
# That is a simple add-on that inserts the daily-learning cards, i.e.
# cards in the learning queue with intervals that crossed the day turnover,
# before starting other reviews (new cards, review cards). Normally these cards
# go last, but I want them to go first. 
# ####################################################################

# This is a simple monkey patch add-on that inserts day learning cards
# (learning cards with intervals that crossed the day turnover)
# always before new cards without depending due reviews. 

# by Anki user ankitest
# • day learning cards always before new
# https://ankiweb.net/shared/info/1331545236

if A['DAY_LEARNING'][0]:
  import anki.sched

  def _getCardReordered(self):
    "Return the next due card id, or None."

    # learning card due?
    c = self._getLrnCard()
    if c:
        return c

    # new first, or time for one?
    if self._timeForNewCard():

        # day learning card due?
        c = self._getLrnDayCard()
        if c:
            return c

        c = self._getNewCard()
        if c:
            return c

    # card due for review?
    c = self._getRevCard()
    if c:
        return c

    # day learning card due?
    c = self._getLrnDayCard()
    if c:
        return c

    # new cards left?
    c = self._getNewCard()
    if c:
        return c

    # collapse or finish
    return self._getLrnCard(collapse=True)

  anki.sched.Scheduler._getCard = _getCardReordered

####################################################
# Copyright 2016 Mirco Kraenz <contact@kraenz.eu>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# https://ankiweb.net/shared/info/136533494
# Tested on Anki Version 2.0.33, Qt 4.8.4, PyQt 4.10

"""
Adds new button to Ankis Editor (the window when you click "Add"). By clicking the button or pressing shortcut Alt + D: Clear all the text from the text fields and jump back to topmost text field. example with below image: Click Button. Then the text field with "foo" and the other one with "bar" will be empty. note: Shortcut is customizable by editing the constant atop the code. Repository on GitHub https://github.com/proSingularity/anki2-addons
"""

SHORTCUT_AltD = "Alt+D"
    
def clear_all_editor_fields(editor):
    '''Remove text from fields in editor. '''
    note = editor.note
    # enumerate all fieldNames of the current note
    for c, field_name in enumerate(mw.col.models.fieldNames(note.model())):
        note[field_name] = ''
    note.flush()  # never forget to flush
    mw.reset()  # refresh gui
    
def setup_clear_buttons(editor):
    """Add the buttons to the editor."""
    editor._addButton("clear_fields1", lambda edito=editor: clear_all_editor_fields(edito), _(SHORTCUT_AltD),
                       text=u"C", tip="Clear field entries (" + SHORTCUT_AltD +")")

# register callback function that gets executed after setupEditorButtons has run. 
# See Editor.setupEditorButtons for details
addHook("setupEditorButtons", setup_clear_buttons)


########################################################
# Browser Search Modifiers
# inspired by https://ankiweb.net/shared/info/594622823
# and https://anki.tenderapp.com/discussions/ankidesktop/17918-add-on-or-anki-feature-suggestion-show-only-front-card-in-browser-checkbox

"""
Anki Add-on: Browser search modifiers

Adds two checkboxes to the browser search form that, when toggled, modify
searches in the following way:

Deck (Hotkey: Alt+D): Limit results to current deck
Card (Hotkey: Alt+C): Limit results to first card of each note

Based on the following add-ons:

- "Limit searches to current deck" by Damien Elmes
   (https://github.com/dae/ankiplugins/blob/master/searchdeck.py)
- "Ignore accents in browser search" by Houssam Salem
   (https://github.com/hssm/anki-addons)

Original idea by Keven on Anki tenderapp

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from aqt.forms.browser import Ui_Dialog

default_checkbox_conf = {'deck_check_checked': False,
                         'card_check_checked': False}

deckChanged = False
cardChanged = False

def onSearch(self, reset=True):
    """Modify search entry."""

    global deckChanged, cardChanged

    txt = unicode(self.form.searchEdit.lineEdit().text()).strip()

    if self.form.cardToggleButton.isChecked():
        if "card:" in txt:
            pass
        elif _("<type here to search; hit enter to show current deck>") in txt:
            pass
        elif "is:current" in txt:
            pass
        else:
            txt = "card:1 " + txt
    elif cardChanged:
        txt = txt.replace("card:1","")
    cardChanged = False

    txt = txt.strip()

    if self.form.deckToggleButton.isChecked():
        if "deck:" in txt:
            pass
        elif _("<type here to search; hit enter to show current deck>") in txt:
            pass
        elif "is:current" in txt:
            pass
        elif txt == "" or txt == 'deck:current' or txt == 'card:1' or txt == 'card:1 deck:current':
            pass
        #elif not txt.strip():
        #    txt = "deck:*"
        else:
            txt = "deck:current " + txt
    elif deckChanged:
        if txt != 'deck:current' and txt != 'card:1 deck:current':
            txt = txt.replace("deck:current","")
    deckChanged = False

    self.form.searchEdit.lineEdit().setText(txt)


def onDeckChecked(state):
    '''Save the checked state in Anki's configuration.'''
    global deckChanged
    mw.col.conf['browser_checkbox_conf']['deck_check_checked'] = state
    deckChanged = True

def onCardChecked(state):
    global cardChanged
    mw.col.conf['browser_checkbox_conf']['card_check_checked'] = state
    cardChanged = True

def mySetupUI(self, mw):
    """Add new items to the browser UI to allow toggling the add-on."""

    # Our UI stuff
    self.deckToggleButton = QCheckBox(_("Deck"), self.widget)
    self.cardToggleButton = QCheckBox(_("Card"), self.widget)
    self.deckToggleButton.setToolTip("Limit results to current deck")
    self.cardToggleButton.setToolTip("Limit results to first card of each note")

    # Restore checked state
    if not 'browser_checkbox_conf' in mw.col.conf:
        mw.col.conf['browser_checkbox_conf'] = default_checkbox_conf
    self.deckToggleButton.setCheckState(
        mw.col.conf['browser_checkbox_conf']['deck_check_checked'])
    self.cardToggleButton.setCheckState(
        mw.col.conf['browser_checkbox_conf']['card_check_checked'])

    # Save state on toggle
    mw.connect(self.deckToggleButton, SIGNAL("stateChanged(int)"), onDeckChecked)
    mw.connect(self.cardToggleButton, SIGNAL("stateChanged(int)"), onCardChecked)
    
    # Add our items to the right of the search box. We do this by moving
    # every widget out of the gridlayout and into a new list. We simply
    # add our stuff in the new list in the right place before moving them
    # back to gridlayout.
    n_items = self.gridLayout.count()
    items= []
    for i in range(0, n_items):
        item = self.gridLayout.itemAt(i).widget()
        items.append(item)
        if item == self.searchEdit:
            items.append(self.deckToggleButton)
            items.append(self.cardToggleButton)
    
    for i, item in enumerate(items):
        self.gridLayout.addWidget(item, 0, i, 1, 1)

def onSetupMenus(self):
    '''Toggle state via key bindings.'''
    self.a = QShortcut(QKeySequence("Alt+C"), self)
    self.connect(self.a, SIGNAL("activated()"), lambda c=self: c.form.cardToggleButton.toggle())
    self.a = QShortcut(QKeySequence("Alt+D"), self)
    self.connect(self.a, SIGNAL("activated()"), lambda c=self: c.form.deckToggleButton.toggle())

    # execute search when toggling checkmarks
    self.connect(self.form.deckToggleButton,
                 SIGNAL("stateChanged(int)"),
                 self.onReset)
    self.connect(self.form.cardToggleButton,
                 SIGNAL("stateChanged(int)"),
                 self.onReset)

if A['BROWSER_SEARCH_MODIFIERS'][0]:
    Ui_Dialog.setupUi = wrap(Ui_Dialog.setupUi, mySetupUI)
    Browser.onSearch = wrap(Browser.onSearch, onSearch, "before")
    addHook("browser.setupMenus", onSetupMenus)


##################################################################
# New filename 2016: Must_Have.py --musthave.py

if A['CHECK_OLD_ISSUES'][0]:
  old_filename = os.path.join(mw.pm.addonFolder(), "Must_Have_Hint_and_Answer_Keys.py")
  if os.path.exists(old_filename):
       showCritical( u'Найдена предыдущая версия дополнения <b>Must Have</b> <br><br>%s<br><br><b>Must_Have_Hint_and_Answer_Keys &nbsp; <big>&#9654;</big></b><br><br> Она несовместима с новой версией.<br> &nbsp; Для нормальной работы:<br> &nbsp;  &nbsp; - удалите старое дополнение<br>  &nbsp; &nbsp; &nbsp; - перезапустите Anki.' % (old_filename) if lang == 'ru' else 'The previous version of the <b>Must Have</b> add-on <br><br>%s<br><br> is incompatible with new edition. <br> Please, remove old file and restart Anki.'  % (old_filename) )
       # отсюда удалить нельзя, Anki слетит из-за неожиданной потери дополнения в процессе их загрузки
       # It's impossible to remove file right now - Anki will be confused.

  old_issues2delete = ''
  for old_issue in old_issues:
     if len(old_issue[0]) > 0:
        old_filename = os.path.join(mw.pm.addonFolder(), old_issue[0])
        if os.path.exists(old_filename) and (old_issue[4]<1 or old_issue[4]==4 or old_issue[4]>5): 
           old_issues2delete += old_issue[0][:-3] + ' \n'

  if old_issues2delete != '':
      if lang == 'ru':
       showText('В каталоге\n\n '+mw.pm.addonFolder()+'\n\nнайдены дополнения, которые уже включены в дополнение `Must Have`,\nи поэтому будут конфликтовать с ним.\n\n' + old_issues2delete + '\nУдалите эти дополнения и перезапустите Anki.')
      else:
       showText('There are some add-ons in the folder \n\n '+mw.pm.addonFolder()+'\n\nThey are already part of `Must Have` addon,\n\n' + old_issues2delete + '\nPlease, delete them and restart Anki.')
  else:
   # mw.addonManager.addonsFolder() is not available here, because of what?
   #tmp = os.path.join(mw.addonManager.addonsFolder(), "musthave_addons")
   tmp = os.path.join(mw.pm.addonFolder(), "musthave_addons")
   if os.path.exists(tmp): # os.path.isdir(tmp)

    def openAddons():
        mw.reviewer.web.page().mainFrame().evaluateJavaScript(\
            'location.assign("https://ankiweb.net/shared/addons/");')

    def openAir():
        maName = os.path.join(mw.addonManager.addonsFolder(), 'musthave_addons.html') #  'musthave-addons.html')
        QDesktopServices.openUrl(QUrl("file:///"+maName))

    def filez():
        return [f for f in os.listdir(os.path.join(mw.addonManager.addonsFolder(), "musthave_addons"))
                    if f.endswith(".py")]

    def checkAddons():

        mustHaveAddons = os.path.join(mw.pm.addonFolder(), "musthave_addons")
        if os.path.exists(mustHaveAddons):

            old_issues2save = ''
            for old_issue in old_issues:
              if len(old_issue[0]) > 0:
                old_filename = os.path.join(mustHaveAddons, old_issue[0])
                if not os.path.exists(old_filename):
                   old_issues2save += old_issue[0][:-3] + ' \n'

            if old_issues2save  !=  '':
               showText('В каталоге\n\n '+mustHaveAddons+'\n\nне найдены дополнения, которые уже включены в дополнение `Must Have`,\nи поэтому, возможно, следует загрузить их и скопировать туда.\n\n' + old_issues2save + '\nНайди эти дополнения и сохрани для дальнейших разборок!')

            old_issues2list = ''
            for old_filename in filez():
              for old_issue in old_issues:
               if old_issue[0]==old_filename:
                   break
              else:
               old_issues2list += old_filename[:-3] + ' \n'

            if old_issues2list  !=  '':
               showText('В каталоге\n\n '+mustHaveAddons+'\n\nнайдены дополнения, которые ещё не включены в список `old_issues`,\nи поэтому, возможно, следует занести их туда.\n\n' + old_issues2list + '\nНайди эти дополнения и реши вопрос!')

        listAddons = mw.reviewer.web.page().mainFrame().evaluateJavaScript(\
            '(function(){return JSON.stringify(shared.files)}())')
        try:
            listAddons = json.loads(listAddons)
        except TypeError:
            tooltip(' &nbsp;<big> Select <i style=color:red;>&nbsp;<b> Load Addons </b>&nbsp;</i> First! </big>&nbsp; ')
            return

        nextlines = []
        for nextline in listAddons:
            nextlines.append(['',nextline[1],str(nextline[0]),time.strftime("%Y-%m-%d", time.localtime(nextline[4]))])

        maName = os.path.join(mw.addonManager.addonsFolder(), 'musthave_addons.html')

        f = open(maName, 'w') 
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<title>musthave</title><meta charset=utf-8>\n')
        f.write('<style>body{text-align:center;font-family:Calibri;}table{margin:auto;border-spacing:0px;border:solid silver 1px;} table:last-of-type { border-bottom: solid 1px black; } tr:nth-child(2n-1){background-color:rgba(233,233,233,.75);}td,th{line-height:1.5em;padding:.1em 1em;text-align:left;}a{text-decoration:none;}a:active,a:hover{text-decoration:underline;}</style>\n')
        f.write('</head>\n<body><h1>musthave <small style = color:green; >'+ unicode(datetime.today().date()) +' <small style = color:blue; >'+ datetime.strftime(datetime.now(),"%H:%M") +'</small></small></h1><p><a href="https://ankiweb.net/shared/addons/">AnkiWeb add-ons list</a></p>\n') 

        def mayDoIt(old_issues):
            oldie = 0
            ff = open(os.path.join(mw.addonManager.addonsFolder(), 'musthave-addons.html'), 'w')
            ff.write(u'<pre>\n')
            for old_issue in old_issues:
                if oldie != old_issue[4]:
                    oldie = old_issue[4]
                    ff.write('\n')
                    ff.writelines('')
                if not old_issue[2] == '':
                    ff.write(u'<a href="https://ankiweb.net/shared/info/%s" rel="nofollow">%s</a>\n' % (old_issue[2], old_issue[1]))
            ff.write(u'</pre>\n')
            ff.close()

        mayDoIt( sorted(old_issues, key=lambda issue: issue[4]) )

        def canDoIt(old_issues, h2, fl, i4):
            f = u'<h4>%s</h4>\n<table style=min-width:50em;><tbody>\n' % (h2)
            i = 0
            j = 0
            for old_issue in old_issues: 
              if old_issue[4] == i4:
                if not old_issue[2] == '':
                    i += 1
                    f += u'<tr><td style=padding-right:1em;text-align:right;font-size:smaller;>' +str(i)+ '.</td><td><a href="https://ankiweb.net/shared/info/%s">%s</a></td><td>%s</td><td style="font-size:smaller;">%s</td></tr>\n' \
                    % (old_issue[2], "<b>%s</b>"%(old_issue[1]) if (old_issue[4]<1) and fl else "<i>%s</i>"%(old_issue[1]) if (old_issue[4]>3) and fl else old_issue[1], old_issue[3], old_issue[2])
                else:
                    if not old_issue[1] == '':
                        j += 1
                        f += '<tr><td style=padding-right:1em;text-align:right;color:dodgerblue;>' +str(j)+ '<small>)</small></td>'
                    else:
                        f += '<tr><td>&nbsp;</td>'

                    f += '<td>%s</td><td>%s</td><td>&nbsp;</td></tr>\n' % ( ("<b>%s</b>"%(old_issue[0]) if (old_issue[4]<1) and fl else "<i>%s</i>"%(old_issue[0]) if (old_issue[4]>3) and fl else old_issue[0]), old_issue[3])

            f += '</tbody></table>\n'
            return f

        def doThemAll(old_issues):
            for old_issue in old_issues:
                not_found = True
                for nextline in nextlines:
                    if old_issue[2]==nextline[2] or old_issue[1].lower() == nextline[1].lower():
                        #"""
                        old_issue[3] = old_issue[3].strip()
                        if old_issue[3][-1:]=='.':
                           old_issue[3] = old_issue[3][:-1]
                        try:
                          mydate = datetime.strptime( old_issue[3], \
                            "%Y-%m-%d" if '-' in old_issue[3] else "%d.%m.%Y" )
                        except ValueError:
                          mydate = ''
                        try:
                          madate = datetime.strptime( nextline[3], \
                            "%d.%m.%Y" if '.' in nextline[3] else "%Y-%m-%d" )
                        except ValueError:
                          madate = ''
                        #"""
                        if not mydate == madate:
                            f.write('<tr><th style="text-align:left;"><a href="https://ankiweb.net/shared/info/%s">%s</a></th><th>' \
                                % (old_issue[2], old_issue[1]) + nextline[3] + '</th><td>' \
                                + old_issue[3] + '</td></tr>\n')
                        not_found = False
                        break
                if not_found and not old_issue[2]=='':
                    f.write('<tr><td><i>' + old_issue[1] + \
                        '</i></td><td colspan="2" style="text-align:center;">not found in add-ons list.</td></tr>')

        f.write('<h2 style="color:red;">Обновления</h2>')
        f.write('<table><tbody>')
        doThemAll(very_interesting)
        f.write('</tbody></table>'+canDoIt(very_interesting, 'Very Necessary', False, 0)+' ')

        f.write('<h2 style="color:red;">New Issues</h2>')
        f.write('<table><tbody>')
        doThemAll(old_issues)
        f.write('</tbody></table>'+canDoIt(old_issues, 'unknown', True, 0)+\
            canDoIt(old_issues, 'disabled if original was found', True, 1)+\
            canDoIt(old_issues, 'fully compatible', True, 2)+\
            canDoIt(old_issues, 'original works anyway', True, 3)+\
            canDoIt(old_issues, 'incompatible', True, 4)+\
            canDoIt(old_issues, 'the add-ons are mine', True, 5)+\
            ' ')

        # 0 - unknown 
        # 1 - switch it off if original was found
        # 2 - fully compatible 
        # 3 - original works anyway 
        # 4 - incompatible 
        # 5 - original does not work

        f.write('<p>&bull;&nbsp;</p></body></html>')
        f.close()

        QDesktopServices.openUrl(QUrl("file:///"+maName))

    open_addons_action = QAction(mw)
    open_addons_action.setText(u'&Load addons')
    mw.connect(open_addons_action, SIGNAL("triggered()"), openAddons)

    check_addons_action = QAction(mw)
    check_addons_action.setText(u'&Check addons')
    mw.connect(check_addons_action, SIGNAL("triggered()"), checkAddons)

    view_addons_action = QAction(mw)
    view_addons_action.setText(u'&View last Check addons results')
    mw.connect(view_addons_action, SIGNAL("triggered()"), openAir)

    mw.form.menuHelp.addSeparator()
    mw.form.menuHelp.addAction(open_addons_action)
    mw.form.menuHelp.addAction(check_addons_action)
    mw.form.menuHelp.addAction(view_addons_action)
    mw.form.menuHelp.addAction(download_addon_action) 
    mw.form.menuHelp.addSeparator()

    dt = datetime.now() # Текущие дата и время. # Current date and time.
    tooltip('<i style="color:blue;">Must Have:</i> &nbsp; it is &nbsp; <b style="color:red;">%s</b> &nbsp; now.' % dt.strftime('%d.%m.%Y %H:%M'))

## eof
