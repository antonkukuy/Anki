# -*- coding: utf-8 -*-
# Copyright: Michal Krassowski <krassowski.michal@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
This plugin adds the function of night mode, similar that one implemented in AnkiDroid.

It adds a "view" menu entity (if it doesn't exist) with options like:

    switching night mode
    inverting colors of images or latex formulas
    modifying some of the colors

It provides shortcut ctrl+n to quickly switch mode and color picker to adjust some of color parameters.

After enabling night mode, add-on changes colors of menubar, toolbar, bottombars and content windows.

If you want to contribute visit GitHub page: https://github.com/krassowski/Anki-Night-Mode
Also, feel free to send me bug reports or feature requests.

Copyright: Michal Krassowski <krassowski.michal@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

__addon_name__ = "Night Mode"
__version__ = "1.0.9"

from aqt import mw, dialogs
from aqt.editcurrent import EditCurrent
from aqt.addcards import AddCards
from aqt.editor import Editor, EditorWebView
from aqt.clayout import CardLayout
from aqt.browser import Browser, COLOUR_MARKED, COLOUR_SUSPENDED
from aqt.utils import showWarning

from anki.lang import _
from anki.hooks import addHook
from anki.hooks import wrap

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QKeySequence, QMenu, \
						QColorDialog, QMessageBox, QColor
from PyQt4 import QtCore
from os.path import isfile

try:
	nm_from_utf8 = QtCore.QString.fromUtf8
except AttributeError:
	nm_from_utf8 = lambda s: s

# This declarations are there only to be sure that in case of troubles
# with "profileLoaded" hook everything will work.

nm_state_on = False
nm_enable_in_dialogs = False
nm_invert_image = False
nm_invert_latex = False
nm_profile_loaded = False

nm_menu_iimage = None
nm_menu_ilatex = None

nm_color_b = "#272828"  # background color (customizable from menu)
nm_color_s = "#373838"  # alternative (second) background color (hardcoded)
nm_color_t = "#ffffff"  # text color (customizable from menu)
nm_color_a = "#443477"  # active element color (hardcoded)
nm_color_cc = "#ffffff"  # text color cards and representation cards on the style window
nm_color_cbg = "#272828"  # background color cards and representation cards on the style window
nm_color_font_browse = "#ffffff"  # text color brose
nm_color_backgrond_browse = "#444444"  # background color brose

# Save original values for further use.
nm_default_css_menu = mw.styleSheet()

nm_default_css_top = mw.toolbar._css
nm_default_css_body = mw.reviewer._css
nm_default_css_bottom = mw.reviewer._bottomCSS

nm_default_css_decks = mw.deckBrowser._css
nm_default_css_decks_bottom = mw.deckBrowser.bottom._css

nm_default_css_overview = mw.overview._css
nm_default_css_overview_bottom = mw.overview.bottom._css
# sharedCSS is only used for "Waiting for editing to finish." screen.
nm_default_css_waiting_screen = mw.sharedCSS

DEFLAULT_COLOUR_MARKED = COLOUR_MARKED
DEFLAULT_COLOUR_SUSPENDED = COLOUR_SUSPENDED

def nm_iimage():
	"""
	Toggles image inversion.
	To learn how images are inverted check also nm_append_to_styles().
	"""
	global nm_invert_image
	nm_invert_image = not nm_invert_image
	nm_refresh()


def nm_ilatex():
	"""
	Toggles latex inversion.
	Latex formulas are nothing more than images with class "latex".
	To learn how formulas are inverted check also nm_append_to_styles().
	"""
	global nm_invert_latex
	nm_invert_latex = not nm_invert_latex
	nm_refresh()


def nm_change_color_t():
	"""
	Open color picker and set chosen color to text (in content)
	"""
	global nm_color_t
	nm_qcolor_old = QColor(nm_color_t)
	nm_qcolor = QColorDialog.getColor(nm_qcolor_old)
	if nm_qcolor.isValid():
		nm_color_t = nm_qcolor.name()
		nm_refresh()


def nm_change_color_b():
	"""
	Open color picker and set chosen color to background (of content)
	"""
	global nm_color_b
	nm_qcolor_old = QColor(nm_color_b)
	nm_qcolor = QColorDialog.getColor(nm_qcolor_old)
	if nm_qcolor.isValid():
		nm_color_b = nm_qcolor.name()
		nm_refresh()


def nm_color_reset():
	"""
	Reset colors.
	"""
	global nm_color_b, nm_color_t
	nm_color_b = "#272828"
	nm_color_t = "#ffffff"
	nm_refresh()


def nm_about():
	"""
	Show "about" window.
	"""
	nm_about_box = QMessageBox()
	if nm_state_on:
		nm_about_box.setStyleSheet(nm_message_box_css())
	nm_about_box.setText(__addon_name__ + " " + __version__ + __doc__)
	nm_about_box.setGeometry(300, 300, 250, 150)
	nm_about_box.setWindowTitle("About " + __addon_name__ + " " + __version__)

	nm_about_box.exec_()


def nm_save():
	"""
	Saves configurable variables into profile, so they can
	be used to restore previous state after Anki restart.
	"""
	mw.pm.profile['nm_state_on'] = nm_state_on
	mw.pm.profile['nm_enable_in_dialogs'] = nm_enable_in_dialogs
	mw.pm.profile['nm_invert_image'] = nm_invert_image
	mw.pm.profile['nm_invert_latex'] = nm_invert_latex
	mw.pm.profile['nm_color_b'] = nm_color_b
	mw.pm.profile['nm_color_t'] = nm_color_t


def nm_load():
	"""
	Load configuration from profile, set states of checkable menu objects
	and turn on night mode if it were enabled on previous session.
	"""
	global nm_menu_iimage, nm_menu_ilatex, nm_state_on, \
		nm_invert_image, nm_invert_latex, nm_color_b, nm_color_t, \
		nm_enable_in_dialogs, nm_profile_loaded

	try:
		nm_state_on = mw.pm.profile['nm_state_on']
		nm_invert_image = mw.pm.profile['nm_invert_image']
		nm_invert_latex = mw.pm.profile['nm_invert_latex']
		nm_color_b = mw.pm.profile['nm_color_b']
		nm_color_t = mw.pm.profile['nm_color_t']
	except KeyError:
		nm_state_on = False
		nm_invert_image = False
		nm_invert_latex = False
		nm_color_b = "#272828"
		nm_color_t = "#ffffff"

	# placed in other handler to keep compatibility with current users profiles
	try:
		nm_enable_in_dialogs = mw.pm.profile['nm_enable_in_dialogs']
	except KeyError:
		nm_enable_in_dialogs = False

	nm_profile_loaded = True

	if nm_state_on:
		nm_on()

	if nm_invert_image:
		nm_menu_iimage.setChecked(True)

	if nm_invert_latex:
		nm_menu_ilatex.setChecked(True)

	if nm_enable_in_dialogs:
		nm_menu_endial.setChecked(True)


def nm_style_fields(editor):

	if nm_state_on and nm_enable_in_dialogs:

		l = str(len(editor.note.fields))

		# change colors only if the card is not marked or the bg color is changed in card styles
		javascript = """
		for (var i=0; i < """ + l + """; i++) {
			bg_color = $("#f"+i).css("background-color")
			if (bg_color == "rgb(255, 255, 255)")
			{
				$("#f"+i).css("color", '""" + nm_color_t + """');
				$("#f"+i).css("background-color", '""" + nm_color_b + """');
			}
			else if (bg_color == "rgb(255, 204, 204)")
			{
				$("#f"+i).css("color", "black");
				$("#f"+i).css("background-color", "DarkOrange");
			}
		}
		$("a").css("color", "#00BBFF")
		$(".fname").css("color", '""" + nm_color_t + """')
		"""

		editor.web.eval(javascript)


def nm_set_style_to_objects_inside(layout, style):
	for i in range(layout .count()):
		layout.itemAt(i).widget().setStyleSheet(style)


def nm_editor_init_after(self, mw, widget, parentWindow, addMode=False):

	if nm_state_on and nm_enable_in_dialogs:

		editor_css = nm_dialog_css()

		editor_css += "#" + widget.objectName() + '{' + nm_text_and_background() + '}'

		self.parentWindow.setStyleSheet(editor_css)

		self.tags.completer.popup().setStyleSheet(nm_css_completer)

		widget.setStyleSheet(nm_css_qt_mid_buttons +
							nm_css_qt_buttons(restrict_to="#" + nm_encode_class_name("fields")) +
							nm_css_qt_buttons(restrict_to="#" + nm_encode_class_name("layout")))


def nm_editor_web_view_set_html_after(self, *args, **kwargs):

	css = ""

	if nm_invert_image:
		css += ".field" + nm_css_iimage
	if nm_invert_latex:
		css += ".field" + nm_css_ilatex

	javascript = "var node=document.createElement('style');"
	javascript += "node.innerHTML='" + css.replace("\n", ' ') + "';"
	javascript += "document.body.appendChild(node);"

	self.eval(javascript)


def nm_edit_current_init_after(self, mw):

	if nm_state_on and nm_enable_in_dialogs:
		self.form.buttonBox.setStyleSheet(nm_css_qt_buttons())


def nm_browser_init_after(self, mw):

	if nm_state_on and nm_enable_in_dialogs:

		x = self.styleSheet()
		self.setStyleSheet(x + nm_css_menu + nm_css_browser())
		self.toolbar._css += nm_css_top
		self.toolbar.draw()

		self.form.tableView.setStyleSheet(nm_browser_table_css())
		self.form.tableView.horizontalHeader().setStyleSheet(nm_browser_table_header_css())

		self.form.searchEdit.setStyleSheet(nm_browser_search_box_css())
		self.form.searchButton.setStyleSheet(nm_css_qt_buttons())
		self.form.previewButton.setStyleSheet(nm_css_qt_buttons())


def nm_browser_card_info_after(self, _old):

	rep, cs = _old(self)

	if nm_state_on and nm_enable_in_dialogs:
		rep += """
			<style>
			*
			{
				""" + nm_text_and_background() + """
			}
			div
			{
				border-color: #fff!important
			}
			""" + nm_css_color_replacer + """
			</style>
			"""
	return rep, cs


def nm_add_init_after(self, mw):

	if nm_state_on and nm_enable_in_dialogs:

		self.form.buttonBox.setStyleSheet(nm_css_qt_buttons())
		nm_set_style_to_objects_inside(self.form.horizontalLayout, nm_css_qt_buttons())
		self.form.line.setStyleSheet("#" + nm_from_utf8("line") + "{border: 0px solid #333;}")
		self.form.fieldsArea.setAutoFillBackground(False)


def take_care_of_night_class(web_object=None):

	if not web_object:
		web_object = mw.reviewer.web

	if nm_state_on:
		javascript = """
		current_classes = document.body.className;
		if (current_classes.indexOf("night_mode") == -1)
		{
			document.body.className += " night_mode";
		}
		"""
	else:
		javascript = """
		current_classes = document.body.className;
		if (current_classes.indexOf("night_mode") != -1)
		{
			document.body.className = current_classes.replace("night_mode","");
		}
		"""

	web_object.eval(javascript)


def nm_encode_class_name(string):
	return "ID"+"".join(map(str, map(ord, string)))


def nm_add_button_name(self, name, *args, **kwargs):
	original_function = kwargs.pop('_old')
	button = original_function(self, name, *args, **kwargs)
	if name:
		button.setObjectName(nm_encode_class_name(name))
	return button


def nm_render_preview_after(card_layout):

	take_care_of_night_class(card_layout.tab['pform'].frontWeb)
	take_care_of_night_class(card_layout.tab['pform'].backWeb)


def nm_edit_render_preview_after(browser, cardChanged=False):
	if not browser._previewWindow:
		return
	take_care_of_night_class(browser._previewWeb)


def nm_onload():
	"""
	Add hooks and initialize menu.
	Call to this function is placed on the end of this file.
	"""

	addHook("unloadProfile", nm_save)
	addHook("profileLoaded", nm_load)
	addHook("showQuestion", take_care_of_night_class)
	addHook("showAnswer", take_care_of_night_class)

	nm_setup_menu()

	Browser.__init__ = wrap(Browser.__init__, nm_browser_init_after)
	Editor._addButton = wrap(Editor._addButton, nm_add_button_name, "around")
	Editor.checkValid = wrap(Editor.checkValid, nm_style_fields)
	Editor.__init__ = wrap(Editor.__init__, nm_editor_init_after)
	EditorWebView.setHtml = wrap(EditorWebView.setHtml, nm_editor_web_view_set_html_after)
	Browser._renderPreview = wrap(Browser._renderPreview, nm_edit_render_preview_after)
	Browser._cardInfoData = wrap(Browser._cardInfoData, nm_browser_card_info_after, "around")
	EditCurrent.__init__ = wrap(EditCurrent.__init__, nm_edit_current_init_after)
	AddCards.__init__ = wrap(AddCards.__init__, nm_add_init_after)
	CardLayout.renderPreview = wrap(CardLayout.renderPreview, nm_render_preview_after)



def nm_append_to_styles(bottom='', body='', top='', decks='',
						other_bottoms='', overview='', menu='',
						waiting_screen=''):
	"""
	This function changes CSS style of most objects. In basic use,
	it only reloads original styles and refreshes interface.

	All arguments are expected to be strings with CSS styles.
	"""
	# Invert images and latex if needed
	if nm_invert_image:
		body += nm_css_iimage
	if nm_invert_latex:
		body += nm_css_ilatex

	# Apply styles to Python objects or by Qt functions.

	mw.setStyleSheet(nm_default_css_menu + menu)
	mw.toolbar._css = nm_default_css_top + top
	mw.reviewer._bottomCSS = nm_default_css_bottom + bottom
	mw.reviewer._css = nm_default_css_body + body
	mw.deckBrowser._css = nm_default_css_decks + decks
	mw.deckBrowser.bottom._css = nm_default_css_decks_bottom + other_bottoms
	mw.overview._css = nm_default_css_overview + overview
	mw.overview.bottom._css = nm_default_css_overview_bottom + other_bottoms
	mw.sharedCSS = nm_default_css_waiting_screen + waiting_screen

	# Reload current screen.
	if mw.state == "review":
		mw.reviewer._initWeb()
	if mw.state == "deckBrowser":
		mw.deckBrowser.refresh()
	if mw.state == "overview":
		mw.overview.refresh()

	# Redraw toolbar (should be always visible).
	mw.toolbar.draw()


def nm_on():
	"""
	Turn on night mode.
	"""
	if not nm_profile_loaded:
		showWarning(NM_ERROR_NO_PROFILE)
		return False

	global nm_state_on

	try:
		nm_state_on = True

		import aqt.browser
		aqt.browser.COLOUR_MARKED = "#735083"
		aqt.browser.COLOUR_SUSPENDED = "#777750"

		nm_append_to_styles(nm_css_bottom,
							nm_css_body + nm_card_color_css(),
							nm_css_top,
							nm_css_decks + nm_body_color_css(),
							nm_css_other_bottoms,
							nm_css_overview + nm_body_color_css(),
							nm_css_menu,
							nm_css_buttons + nm_body_color_css())
		nm_menu_switch.setChecked(True)
		return True
	except:
		showWarning(NM_ERROR_SWITCH)
		return False

def nm_off():
	"""
	Turn off night mode.
	"""
	if not nm_profile_loaded:
		showWarning(NM_ERROR_NO_PROFILE)
		return False

	try:
		global nm_state_on
		nm_state_on = False

		import aqt.browser
		aqt.browser.COLOUR_MARKED = DEFLAULT_COLOUR_MARKED
		aqt.browser.COLOUR_SUSPENDED = DEFLAULT_COLOUR_SUSPENDED

		nm_append_to_styles()
		nm_menu_switch.setChecked(False)
		return True
	except:
		showWarning(NM_ERROR_SWITCH)
		return False

def nm_switch():
	"""
	Switch night mode.
	"""

	# Implementation of "setStyleSheet" method in QT is bugged.
	# At some circumstances it causes a seg fault, without throwing any exceptions.
	# So the switch of mode is not allowed when the problematic dialogs are visible.

	is_active_dialog = filter(bool, [x[1] for x in dialogs._dialogs.values()])

	if is_active_dialog:
		info = _("Night mode can not be switched when the dialogs are open")
		showWarning(info)
		print info
	else:
		if nm_state_on:
			nm_off()
		else:
			nm_on()


def nm_endial():
	"""
	Switch for night mode in dialogs
	"""
	global nm_enable_in_dialogs
	if nm_enable_in_dialogs:
		nm_enable_in_dialogs = False
	else:
		nm_enable_in_dialogs = True


def nm_refresh():
	"""
	Refresh display by reenabling night or normal mode.
	"""
	if nm_state_on:
		nm_on()
	else:
		nm_off()


def nm_setup_menu():
	"""
	Initialize menu. If there is an entity "View" in top level menu
	(shared with other plugins, like "Zoom" of R. Sieker) options of
	Night Mode will be putted there. In other case it creates that menu.
	"""
	global nm_menu_switch, nm_menu_iimage, nm_menu_ilatex, nm_menu_endial

	try:
		mw.addon_view_menu
	except AttributeError:
		mw.addon_view_menu = QMenu(_(u"&View"), mw)
		mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(),
									mw.addon_view_menu)

	mw.nm_menu = QMenu(_('&Night Mode'), mw)

	mw.addon_view_menu.addMenu(mw.nm_menu)

	nm_menu_switch = QAction(_('&Enable night mode'), mw, checkable=True)
	nm_menu_iimage = QAction(_('&Invert images'), mw, checkable=True)
	nm_menu_ilatex = QAction(_('Invert &latex'), mw, checkable=True)
	nm_menu_endial = QAction(_('Enable in &dialogs'), mw, checkable=True)
	nm_menu_color_b = QAction(_('Set &background color'), mw)
	nm_menu_color_t = QAction(_('Set &text color'), mw)
	nm_menu_color_r = QAction(_('&Reset colors'), mw)
	nm_menu_about = QAction(_('&About...'), mw)

	mw_toggle_seq = QKeySequence("Ctrl+n")
	nm_menu_switch.setShortcut(mw_toggle_seq)

	mw.nm_menu.addAction(nm_menu_switch)
	mw.nm_menu.addAction(nm_menu_endial)
	mw.nm_menu.addSeparator()
	mw.nm_menu.addAction(nm_menu_iimage)
	mw.nm_menu.addAction(nm_menu_ilatex)
	mw.nm_menu.addSeparator()
	mw.nm_menu.addAction(nm_menu_color_b)
	mw.nm_menu.addAction(nm_menu_color_t)
	mw.nm_menu.addAction(nm_menu_color_r)
	mw.nm_menu.addSeparator()
	mw.nm_menu.addAction(nm_menu_about)

	s = SIGNAL("triggered()")
	mw.connect(nm_menu_endial, s, nm_endial)
	mw.connect(nm_menu_switch, s, nm_switch)
	mw.connect(nm_menu_iimage, s, nm_iimage)
	mw.connect(nm_menu_ilatex, s, nm_ilatex)
	mw.connect(nm_menu_color_b, s, nm_change_color_b)
	mw.connect(nm_menu_color_t, s, nm_change_color_t)
	mw.connect(nm_menu_color_r, s, nm_color_reset)
	mw.connect(nm_menu_about, s, nm_about)


# background and color fot cards
def nm_card_color_css():
	"""
	Generate and return CSS style of class "card",
	using global color declarations
	"""
	return (".card {	color:" + nm_color_cc + "!important;" +
			"background-color:" + nm_color_cbg + "!important}")


def nm_body_color_css():
	"""
	Generate and return CSS style of class "card",
	using global color declarations
	"""
	return (" body {	color:" + nm_color_t + "!important;" +
			"background-color:" + nm_color_b + "!important}")


def nm_message_box_css():
	"""
	Generate and return CSS style of class QMessageBox,
	using global color declarations
	"""
	return ("QMessageBox,QLabel {	color:" + nm_color_t + ";" +
			"background-color:" + nm_color_b + "}" + nm_css_qt_buttons() +
			"QPushButton {  min-width: 70px }" )


def nm_css_qt_buttons(restrict_to_parent="", restrict_to=""):
	return """
	""" + restrict_to_parent + """ QPushButton""" + restrict_to + """
	{
		background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #3D4850, stop: 0.04 #313d45, stop: 1 #232B30);
		border-radius: 3px;
		""" + nm_css_button_idle + """
	}
	""" + restrict_to_parent + """ QPushButton""" + restrict_to + """:hover
	{
		""" + nm_css_button_hover + """
		background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #4C5A64, stop: 0.04 #404F5A, stop: 1 #2E3940);
	}
	""" + restrict_to_parent + """ QPushButton""" + restrict_to + """:pressed
	{
		""" + nm_css_button_active + """
		background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #20282D, stop: 0.51 #252E34, stop: 1 #222A30);
	}
	"""


# TODO rewrite redundant code with this function or even better,
# keep in memory generated string and change it only when the colour is changed.

def nm_text_and_background():
	return 'color:' + nm_color_font_browse + ';background-color:' + nm_color_backgrond_browse + ';'


def nm_dialog_css():
	"""
	Generate and return CSS style of AnkiQt Dialogs,
	using global color declarations
	"""
	return """
			QDialog,QLabel,QListWidget,QFontComboBox,QCheckBox,QSpinBox,QRadioButton,QHBoxLayout
			{
			""" + nm_text_and_background() + """
			}
			QFontComboBox::drop-down{border: 0px; border-left: 1px solid #555; width: 30px;}
			QFontComboBox::down-arrow{width:12px; height:8px;
				top: 1px;
				image: url(""" + NM_DOWN_ARROW_ICON_PATH + """);
			}
			QFontComboBox, QSpinBox{border: 1px solid #555;}

			QTabWidget QWidget
			{
				color: """ + nm_color_t + """;
				background-color: #222;
				border-color: #555;
			}
			QTabWidget QLabel {
				position:relative;
			}
			QTabWidget QTabBar
			{
				color: #000
			}
			QTabWidget QTextEdit
			{
				border-color: #555;
			}
			QTabWidget QGroupBox::title
			{
				subcontrol-origin: margin;
				subcontrol-position:top left;
				margin-top:-7px;
			}
			""" + nm_css_qt_buttons("QTabWidget")


def nm_browser_table_css():
	return """
		QTableView
		{
			alternate-background-color: """ + nm_color_s + """;
			gridline-color: """ + nm_color_s + """;
			""" + nm_text_and_background() + """
			selection-background-color: """ + nm_color_a + """
		}
		"""


def nm_browser_table_header_css():
	return """
		QHeaderView::section
		{
			""" + nm_text_and_background() + """
			border: 1px solid """ + nm_color_s + """;
		}
		"""


def nm_browser_search_box_css():
	return """
	QComboBox
	{
		border: 1px solid """ + nm_color_s + """;
		border-radius: 3px;
		padding: 0px 4px;
		""" + nm_text_and_background() + """
	}

	QComboBox:!editable
	{
		background: """ + nm_color_a + """
	}

	QComboBox QAbstractItemView
	{
		border: 1px solid #111;
		""" + nm_text_and_background() + """
		background: #444;
	}

	QComboBox::drop-down, QComboBox::drop-down:editable
	{
		""" + nm_text_and_background() + """
		width: 24px;
		border-left: 1px solid #444;
		border-top-right-radius: 3px;
		border-bottom-right-radius: 3px;
		background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #3D4850, stop: 0.04 #313d45, stop: 1 #232B30);
	}

	QComboBox::down-arrow
	{
		top: 1px;
		image: url(""" + NM_DOWN_ARROW_ICON_PATH + """);
	}
	"""


def nm_css_browser():
	return """
	QSplitter::handle
	{
		background:#000000
	}
	#""" + nm_from_utf8("widget") + """, QTreeView
	{
		""" + nm_text_and_background() + """
	}
	QTreeView::item:selected:active, QTreeView::branch:selected:active
	{
		background: """ + nm_color_a + """
	}
	QTreeView::item:selected:!active, QTreeView::branch:selected:!active
	{
		background: """ + nm_color_a + """
	}
	"""

#
# GLOBAL CSS STYLES SECTION
#

# Thanks to http://devgrow.com/dark-button-navigation-using-css3/
nm_css_button_idle = """
	color: #AFB9C1;
	margin-top: 0;
	position:relative;
	top: 0;
	outline: 0;
	padding: 3px 8px;
	border: 1px solid #3E474D;
	border-top-color: #1c252b;
	border-left-color: #2d363c;
"""

nm_css_button_hover = """
	color: #fff;
"""

nm_css_button_active = """
	color: #fff;
"""

nm_css_buttons = """
button
{
	""" + nm_css_button_idle + """
	text-shadow: 1px 1px #1f272b;
	display: inline-block;
	background: -webkit-gradient(linear, left top, left bottom, color-stop(3%,#3D4850), color-stop(4%,#313d45), color-stop(100%,#232B30));
	-webkit-box-shadow: 1px 1px 1px rgba(0,0,0,0.1);
	-webkit-border-radius: 3px;
}
button:hover
{
	""" + nm_css_button_hover + """
	background: -webkit-gradient(linear, left top, left bottom, color-stop(3%,#4C5A64), color-stop(4%,#404F5A), color-stop(100%,#2E3940));
}
button:active
{
	""" + nm_css_button_active + """
	background: -webkit-gradient(linear, left top, left bottom, color-stop(3%,#20282D), color-stop(51%,#252E34), color-stop(100%,#222A30));
	-webkit-box-shadow: 1px 1px 1px rgba(255,255,255,0.1);
}
"""

# TODO
nm_css_completer = """
	background-color:black;
	border-color:#444;
	color:#eee;
"""

nm_css_qt_mid_buttons = """
QLineEdit
{
""" + nm_css_completer + """
}

/*
QPushButton
{
	background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #8E99AA, stop: 0.04 #828E96, stop: 1 #747C8A);
	border-radius: 3px;
	""" + nm_css_button_idle + """
	color: #000;
}
QPushButton:hover
{
	""" + nm_css_button_hover + """
	background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #9CAAB4, stop: 0.04 #909FAA, stop: 1 #7E8990);
}
QPushButton:pressed
{
	""" + nm_css_button_active + """
	background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #70787D, stop: 0.51 #757E84, stop: 1 #727A80);
}
*/
"""

nm_css_color_replacer = """
font[color="#007700"], span[style="color:#070"]
{
	color:#00CC00!important
}
font[color="#000099"], span[style="color:#00F"]
{
	color:#00BBFF!important
}
font[color="#C35617"], span[style="color:#c00"]
{
	color:#D46728!important
}
font[color="#00a"]
{
	color:#00BBFF
}
"""

nm_css_bottom = nm_css_buttons + nm_css_color_replacer + """
body
{
	background: -webkit-gradient(linear, left top, left bottom, from(#333), to(#222));
	border-top-color: #000;
}
button
{
	min-width: 70px;
}
.hitem
{
	margin-top: -20px;
}
.stat
{
	padding-top: 0;
}
.stat2
{
	padding-top: 0;
}
.stattxt
{
	height: 6px;
	display:block;
}
.stattxt
{
	color:#ccc
}
.nobold
{
	display: block;
	padding-top: 0;
	height: 7px;
	color:#ddd
}
.spacer
{
	position:relative;
	top:-8px;
}
.spacer2
{
	position:relative;
	top:-8px;
}
button
{
	top:-6px
}
button:active
{
	top:-7px
}
"""

nm_css_top = """
html
{
	background: -webkit-gradient(linear, left top, left bottom, from(#333), to(#444));
	color:#eee;
}
body
{
	border-bottom-color:#111;
}
.hitem
{
	color: #ddd;
}
"""

nm_css_ilatex = """
.latex
{
	-webkit-filter: invert(100%);
}
"""

nm_css_iimage = """
img
{
	-webkit-filter: invert(100%);
}
"""


nm_css_body = """
'''
.card input
{
	background-color:black!important;
	border-color:#444!important;
	color:#eee!important;
}
.typeGood
{
	color:black;
	background:#57a957;
}
.typeBad
{
	color:black;
	background:#c43c35;
}
.typeMissed
{
	color:black;
	background:#ccc;
}
#answer
{
	height: 0;
	border: 0;
	border-bottom: 2px solid #333;
	border-top: 2px solid black;
}
img#star
{
	-webkit-filter: invert(0%)!important;
}
.cloze
{
	color: #33CC33!important;
}
'''
"""


nm_css_decks = nm_css_buttons + nm_css_color_replacer + """
.current
{
	background-color: rgba(0,0,0,0.5);
}
a.deck
{
	color: #efe
}
tr.deck td
{
	height:35px;
	border-bottom-color:#333
}
tr.deck button img
{
	-webkit-filter: invert(20%);
}
tr.deck font[color="#007700"]
{
	color:#00CC00
}
tr.deck font[color="#000099"]
{
	color:#00BBFF
}
"""

nm_css_other_bottoms = nm_css_buttons + """
#header
{
	color:#ccc!important;
	background: -webkit-gradient(linear, left top, left bottom, from(#333), to(#222));
	border-top-color: #000;
	height:40px;
}
"""

nm_css_overview = nm_css_buttons + nm_css_color_replacer

nm_css_menu = """
QMenuBar,QMenu
{
	background-color: #444!important;
	color: #eee!important;
}
QMenuBar::item
{
	background-color: transparent;
}
QMenuBar::item:selected
{
	background-color: """ + nm_color_a + """!important;
	border-top-left-radius: 6px;
	border-top-right-radius: 6px;
}
QMenu
{
	border: 1px solid #111;
}
QMenu::item::selected
{
	background-color: """ + nm_color_a + """;
}
QMenu::item
{
	padding: 3px 25px 3px 25px;
	border: 1px solid transparent;
}
"""

NM_ERROR_NO_PROFILE = """Switching night mode failed: The profile is not loaded yet.
Probably it's a bug of Anki or you tried to switch mode to quickly."""

NM_ERROR_SWITCH = """Switching night mode failed: Something went really really wrong.
Contact add-on author to get help."""


where_to_look_for_arrow_icon = [
	'/usr/share/icons/Adwaita/scalable/actions/pan-down-symbolic.svg',
	'/usr/share/icons/gnome/scalable/actions/go-down-symbolic.svg',
	'/usr/share/icons/ubuntu-mobile/actions/scalable/dropdown-menu.svg',
	'/usr/share/icons/Humanity/actions/16/down.svg',
	'/usr/share/icons/Humanity/actions/16/go-down.svg',
	'/usr/share/icons/Humanity/actions/16/stock_down.svg',
	'/usr/share/icons/nuvola/16x16/actions/arrow-down.png',
	'/usr/share/icons/default.kde4/16x16/actions/arrow-down.png'
	]

# It's not an arrow icon,
# but on windows systems it's better to have this, than nothing.
NM_DOWN_ARROW_ICON_PATH = ':/icons/gears.png'

for path in where_to_look_for_arrow_icon:
	if isfile(path):
		NM_DOWN_ARROW_ICON_PATH = path
		break

#
# ONLOAD SECTION
#

nm_onload()
