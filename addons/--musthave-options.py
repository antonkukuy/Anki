# -*- mode: Python ; coding: utf-8 -*-
# Place your Must Have configuration variables here.

deck_browser_standard_zoom = 1.0
overview_standard_zoom = 1.0
reviewer_standard_zoom = 1.0

###################################################################
# If you want to use alternative value
# simply delete first character # (sharp) on the subsequent line.
# Use Delete or Backspace key, to remove does not mean to replace with Space instead.
# Either you can place cursor right after # (sharp)
# and push Enter to split single line on two separate lines.

# ---------------------------------
# Get language class
import anki.lang
lang = anki.lang.getLang()

FROM_LANGUAGE = 'russian'
TO_LANGUAGE   = 'english'

FROM_LNG   = 'rus' # 3 letters language code
TO_LNG     = 'eng'

FROM_LANG   = 'ru' # 2 letters language code
TO_LANG     = 'en'

#BUTTON_LABELS_LANG = [[lang, _('Again'), _('Hard'), _('Good'), _('Easy')]] # in Translation 
#BUTTON_LABELS_LANG = [[lang, 'Again', 'Hard', 'Good', 'Easy']] # in English 
#BUTTON_LABELS_LANG = [[lang, 'Snova', 'Trudno', 'AGA', 'Legko']] # in translit 
#BUTTON_LABELS_LANG = [[lang, u'НЕТ', u'Трудно', u'ДА', u'Легко']] # in Russian anyhow 
#BUTTON_LABELS_LANG = [[lang, u'aw&hellip;', u'huh?', u'nice', u'radical!']] # in lowercase anyway 
#BUTTON_LABELS_LANG = [[lang, u'NO?', u'AH!', u'OK', u'SO&#133;']] # in uppercase anywhere

Z = { 

# Tools -> Add-ons -> Browse & Install...
'ADDONS_INSTALL_TOOLTIP': True, # False, # 

# Edit Cards Add field W/O DIV style=font
'ADD_FIELDS_WITHOUT_DIV': True, # False, # 

# not ^D, Control+d excluded, ^F and ^W only.
'ANKI12SHORTCUTS': True, # False, # 

# Show menu icons
'ANKI_MENU_ICONS': True, # False, # 

# if you need to reply on question (FrontSide) directly,
'ANSWER_BYPASS': False, # True, # 

# if you need to open an answer (BackSide) with any answer key
'ANSWER_USING_REPLY_KEYS': False, # True, # 

# in Browse: CurrentDeck or Card1 only
'BROWSER_SEARCH_MODIFIERS': True, # False, # 

# Сheck the startup path for invalid characters
'CHECK_ASCII_PATH': True, # False, # 

# Look for old add-ons
'CHECK_OLD_ISSUES': True, # False, # 

# in Add/Edit: Ctrl+Alt+Space === Ctrl+Alt+Shift+C
'CLOZE_EDITOR_HOTKEYS': True, # False, # 

# Toolbars on cards.
'COLORFUL_TOOLBAR': True, # False, # 

# Customizable Congratulations Message
'CUSTOM_CONGRAT_MSG': True, # False, # 

# Day learning cards always before new.
'DAY_LEARNING': True, # False, # 

# Look for deck's name, profile name, cmd parameters in window title.
'DECK_NAME_IN_TITLE': True, # False, # 

# Disable the delete key in reviews
'DISABLE_DEL': True, # False, # 

# Expand and Collapse Decks
'EXPAND_AND_COLLAPSE_DECKS': True, # False, # 

# F3 == popup window
'F3_CARD_HISTORY': True, # False, # 

# Card Info During Review
#'F3_CARD_INFO_DURING_REVIEW': False, # False, # 
'F3_CARD_INFO_DURING_REVIEW': True, # False, #    error press Space to answer

# View Source HTML (Alt+F3)
'F3_HTML_SOURCE': True, # False, # 

# View Source HTML
'F3_VIEW_SOURCE': True, # False, # 

# Edit card's templates
'F4_EDIT': True, # False, # 

# ^Shift+F6 fast ^Alt+F6 slow ^Alt+Shift+F6 100%
'F6_FAST_SLOW': True, # False, # 

# F6 pause ^F6 stop Alt+F6 back Shift+F6 forward 5 sec.
#'F6_SOUND_KEY_MENU': False, # False, # 
'F6_SOUND_KEY_MENU': True, # False, # 

# Hint-peeking Keyboard Bindings is a way of showing multiple hints increasingly.
'F9_HINT_PEEKING': True, # False, # 

# Push 5 button to open next hint.
'F9_HINT_PEEKING_5': True, # False, # 

# Push H to hint hext.
'F9_HINT_PEEKING_H': True, # False, # 

# Show FrontSide/BackSide
'FLIP_FLOP': True, # False, # 

'FONT': 'Calibri', # '', # 

# Default Font Size for Decks Browser and Deck Overview
'FONTSIZE': 16, # 0, # 

# A more convenient way to mark fields as sticky.
'FROZEN_FIELDS': True, # False, # 

# GroupName::TagName
'HIERARCHICAL_TAGS': True, # False, # 

# To show next card from NumPad.
'KEY0': True, # False, # 

# Apostophe marks note now, too. (tag:marked)
'KEYS_HANDLER': True, # False, # 

# Icon's size on toolbar (pixels) # 48
'KING_SIZE': 32, # 24, # 

# Local CSS and DIY night mode
'LOCAL_CSS_AND_DIY_NIGHT_MODE': True, # False, # 


# Show {{Field with commas}} on the card as UL/OL.
'MAKE_LIST': True, # False, # 

# Maximum images height in card editor (preview)
'MAXHEIGHT': '100px', # False, # 

# Check multiple type with default space bar.
'MULTIPLE_TYPING': False, # False, # error press Space to answer
#'MULTIPLE_TYPING': True, # False, # 

# Numeric Keypad Remapping Use buttons 7 8 9 6 on numeric keyboard to right-handed reply.
'NUMERIC_KEYPAD_REMAPPING': True, # False, # 

# Skip question if BackSide is empty, {{FrontSide}} only or exact CopyPaste of FrontSide.
'ONESIDED_CARDS': True, # False, # 

# Open local Anki folders in file explorer.
'OPEN_FOLDERS': True, # False, # 

# Power Create lists ordered unordered and indented O U In buttons in editor window
'POWER_CREATE_LISTS': True, # False, # 

# Random element from Field with commas.
'RANDOM_ITEM': True, # False, # 

# [sound:...][sound:...][sound:...] just once
'RANDOM_SOUND': True, # False, # 

# Rebuild ALL filtered decks
'REBUILD_THEM_ALL': True, # False, # 

# new line in Tools menu to Remove ALL Empty Note Types and Delete Redundant Configurations at once
'REMOVES_EMPTY': True, # False, # 

# Replay buttons on card # =1 title tooltip on FrontSide without filename
'REPLAY_BUTTONS_ON_CARD': 0, # 0, # 
#'REPLAY_BUTTONS_ON_CARD': 2, # 0, #      don't work web source voice 

# Reset card scheduling information / progress
'RESET_CARD_SCHEDULING': True, # False, # 

# Use buttons J K L ; on main keyboard to right-handed reply.
'RIGHT_HAND_JKL_ANSWER_KEYS_SHORTCUTS': True, # False, # 

# Tatoeba, Google, Yandex, Bing lookup selected on right-click and so on.
'SEARCH_AND_TRANSLATE': True, # False, # 

# Find out selected text in Anki's Browser.
'SEARCH_BROWSER': True, # False, # 

# Search from Editor
'SEARCH_FROM_EDITOR': True, # False, # 

# Search cards based on review time
'SEARCH_TIME': True, # False, # 

# Show card some days later.
'SET_INTERVAL': True, # False, # 

# No minimal width/height on Add/Edit window.
'SMALL_ADD_EDIT_DIALOGS': True, # False, # 

# Swap Front/Back fields' values
'SWAP_FRONT_BACK': True, # False, # 

# Timebox tooltip w/o any askUser.
'TIMEBOX_TOOLTIP': True, # False, # 

# If you want to learn in Full-Sreen, use this.
'TOGGLE_FULL_SCREEN_F11': True, # False, # 

# 0 on question FrontSide == Show Answer 0 on answer BackSide == Answer Good and Show Next Card
'ZERO_KEY_TO_SHOW_ANSWER': True, # False, # 

# ZOOM and Open Hint and Reply with Mouse Wheel
'ZOOM': True, # False, # 

# also ZOOM Images as well as text too
'ZOOM_IMAGES': True, # False, # 

# More Overview Stats # =1
'B00_MORE_OVERVIEW_STATS': 3, # 0, # 

# Gear at the end of line
'B03_GEAR_AT_END_OF_LINE': True, # False, # 

# Hide big numbers
'B04_HIDE_BIG_NUMBER': 999, # 999999, # 

# Don't see the exact number in deck list.
'B04_HIDE_BIG_NUMBERS': False, # True, # 

# Study Deck Button
'B05_STUDY_BUTTON': False, # True, # 

# Bigger Show All Answer Button
'B06_WIDE_BUTTONS': True, # False, # 

# Color Answer Buttons
'B07_COLOR_BUTTONS': True, # False, # 

# Big Button Show Answer and so far.
'B08_BIG_BUTTONS': True, # False, # 

# =1 tooltip all answers
'B10_ANSWER_CONFIRMATION': 2, # 0, # 

# 2C titles (tooltips, baloon tips)
'B11_BUTTON_TITLES': True, # False, # 

# Use the key 7 on the numeric keypad as key 2 synonim (Hard) instead of key 1 (Again) if you answer `Hard` more often than `Again`
'B12_HARD7': False, # True, # 

# Edit and More buttons on Study Screen
'B13_EDIT_MORE': False, # True, # 


}
 # 


