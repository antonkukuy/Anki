# -*- coding: utf-8 -*-
# Author:  Ben Lickly <blickly at berkeley dot edu>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   Hint-peeking add-on
#
# This add-on allows peeking at some of the fields in a flashcard
# before seeing the answer. This can be used to peek at word context,
# example sentences, word pronunciation (especially useful for
# Chinese/Japanese/Korean), and much more.

from PyQt4.QtCore import Qt

########################### Settings #######################################
# The following settings can be changed to suit your needs. Lines
# starting with a pound sign (#) are comments and are ignored.

# SHOW_HINT_KEY defines the key that will reveal the hint fields.
# A list of possible key values can be found at:
#       http://opendocs.net/pyqt/pyqt4/html/qt.html#Key-enum
SHOW_HINT_KEY=Qt.Key_H

######################### End of Settings ##################################

from anki.hooks import wrap
from aqt.reviewer import Reviewer

def newKeyHandler(self, evt, _old):
    """Show hint when the SHOW_HINT_KEY is pressed."""
    if (self.state == "question"
            and evt.key() == SHOW_HINT_KEY):
        self._showHint()
    else:
        return _old(self, evt)

def _showHint(self):
    """To show hint, simply click all show hint buttons."""
    self.web.eval("""
     var customEvent = document.createEvent('MouseEvents');
     customEvent.initEvent('click', false, true);
     var arr = document.getElementsByTagName('a');
     for (var i=0; i<arr.length; i++) {
       var l=arr[i];
       if (l.href.charAt(l.href.length-1) === '#') {
         l.dispatchEvent(customEvent);
       }
     }
     """)

Reviewer._showHint = _showHint
Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "around")

