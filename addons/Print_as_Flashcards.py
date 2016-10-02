# -*- coding: utf-8 -*-
#############################################################################
#
# -Goal Oriented Academics LLC <goalorientedacademics@gmail.com>
# -GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# -This addon is a modified version of the basic printing add-on by 
# Damien Elmes.  The file flashcards.html that this version produces will
# print as double-sided flashcards in a 3x3 grid.  The ordering required to
# be properly aligned for a specific printer can be adjusted where indicated
# in the code, but rightnow it is only configured for a Canon MF5900 printing
# from Chrome Browser.
#
##############################################################################

import re, urllib
from aqt.qt import *
from anki.utils import isWin
from anki.hooks import runHook, addHook
from aqt.utils import getBase, openLink, tooltip
from aqt import mw
from anki.utils import ids2str

CARDS_PER_ROW   = 3
ROWS_PER_TABLE  = 3
CARDS_PER_TABLE = CARDS_PER_ROW*ROWS_PER_TABLE

def sortFieldOrderCids(did):
    dids = [did]
    for name, id in mw.col.decks.children(did):
        dids.append(id)
    return mw.col.db.list("""
select c.id from cards c, notes n where did in %s
and c.nid = n.id order by n.sfld""" % ids2str(dids))

def onPrint():
    path = os.path.join(mw.pm.profileFolder(), "flashcards.html")
    ids = sortFieldOrderCids(mw.col.decks.selected())
    def esc(s):
        # strip off the repeated question in answer if exists
        #s = re.sub("(?si)^.*<hr id=answer>\n*", "", s)
        # remove type answer
        s = re.sub("\[\[type:[^]]+\]\]", "", s)
        return s
    def upath(path):
        if isWin:
            prefix = u"file:///"
        else:
            prefix = u"file://"
        return prefix + unicode(
            urllib.quote(path.encode("utf-8")), "utf-8")
    buf = open(path, "w")
    buf.write("<html>" + getBase(mw.col).encode("utf8"))
    buf.write("<meta charset=\'utf-8\'><body>")
    buf.write("""<style>
img   { max-width: 100%; }
td    { border: 1px solid #ccc;
        padding: 0;
        width: 33%; }
table { table-layout: fixed; 
        border-spacing: 0;
	page-break-after: always;
	width: 100%;
	height: 100%; }
.a td { border: none; }
tr    { height: 33%; }
@page { size: landscape; }
</style>""")
    first = True
    ans = []
    que = []
    mw.progress.start(immediate=True)
    for j, cid in enumerate(ids):
        c = mw.col.getCard(cid)
        que.append(esc(c._getQA(True, False)['a']).split('<hr id=answer>')[0])
        ans.append(esc(c._getQA(True, False)['a']).split('<hr id=answer>')[1])
    
    if (len(que)%CARDS_PER_TABLE != 0):
        for i in range(len(que)%CARDS_PER_TABLE):
            que.append("")
            ans.append("")
    
    for i in range((len(que)//CARDS_PER_TABLE)):
        theTable = ["<table>","<table class=\'a\'>"]
        for j in range(ROWS_PER_TABLE):
            theTable[0] += "<tr>"
            theTable[1] += "<tr>"
            for k in range(CARDS_PER_ROW):
                theTable[0] += "<td><center>"+que[9*i+3*j+k]+"</td></center>"
######################################################################################
    #Make edits here to adjust the ordering of the answer cards
    #Currently calibrated for a Canon MF5900 printing from Google Chrome
                theTable[1] += "<td><center>"+ans[9*i+6-3*j+k]+"</td></center>"
######################################################################################
            theTable[0] += "</tr>"
            theTable[1] += "</tr>"
        theTable[0] += "</table>"
        theTable[1] += "</table>"
        buf.write(theTable[0].encode("utf-8"))
        buf.write(theTable[1].encode("utf-8"))
    buf.write("</body></html>")
    mw.progress.finish()
    buf.close()
    tooltip(_("Loading..."), period=1000)
    QDesktopServices.openUrl(QUrl.fromEncoded(upath(path)))

q = QAction(mw)
q.setText("Make Flashcards")
q.setShortcut(QKeySequence("Ctrl+M"))
mw.form.menuTools.addAction(q)
mw.connect(q, SIGNAL("triggered()"), onPrint)
