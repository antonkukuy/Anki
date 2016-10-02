# -*- coding: utf-8 ; mode: python -*-
# https://ankiweb.net/shared/info/67643234
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# -- MUST HAVE -- Statistics Pack -- 67643234 -- 
# 
from __future__ import division
from __future__ import unicode_literals
import os, sys

if __name__ == "__main__":
    print("This is a some statistics add-on for the Anki program and it can't be run directly.")
    print("Please download Anki 2.0 from http://ankisrs.net/")
    sys.exit()
else:
    pass

if sys.version[0] == '2': # Python 3 is utf8 only already
  if hasattr(sys,'setdefaultencoding'):
    sys.setdefaultencoding('utf8')

import anki
import anki.stats, aqt, math, time, datetime

#####################
# Get language class
import anki.lang
lang = anki.lang.getLang()

# graph color
colYngLrn = "#7c7"  # light green
colMtr = "#070"     # dark green



#####################
# Progress_Graph.py
# Progress graph 
# https://ankiweb.net/shared/info/763339789
#

# -*- coding: utf-8 ; mode: python -*-
#
# Copyright © 2014 Thomas TEMPÉ, <thomas.tempe@alysse.org>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.

# Progress graph for Anki 2
########################################################################
'''
This module draws two stats graphs in Anki's "stats" window, showing the 
number of notes and cards learned over time.
'''

from anki import stats
from anki.hooks import wrap, addHook, runHook
from aqt.utils import showInfo
import time, re, sys

now = time.mktime(time.localtime())

def history(data, chunks=None, chunk_size=1):
    #Compute history
    if not chunks:
        try:
            chunks=max(data)/chunk_size+1 #nb of periods to look back
        except:
            chunks = 1 #This happens if the deck is empty
    histogram = [0]*(chunks+1)
    cumul=[]
    delta=[]
    subtotal=0
    date=-chunks
    #Fill histogram, as a list. d = nb of days in the past (0=today).
    for d in data:
        if d <= chunks*chunk_size:
            histogram[int(d/chunk_size)] += 1
        else:
            subtotal+=1
    #Fill history, as a list of coordinates: [(relative_day, nb_values),...]
    while len(histogram):
        v=histogram.pop()
        subtotal +=v
        cumul.append((date, subtotal))
        delta.append((date, v))
        date+=1
    return cumul, delta

##################################################
def progressGraphs(self, chunks, chunk_size, chunk_name):
    txt=""
    notes = [] #list of 1st-review dates for all your notes
    cards = [] #list of 1st-review dates for all your cards

    #Count notes
    for first_study_date in self.col.db.execute("select min(revlog.id)/1000 as date from cards, revlog where cards.id=revlog.cid and cards.queue>0 and cards.did in %s group by cards.nid;" % self._limit() ):
        relative_time = int((now-first_study_date[0])/86400) #in days
        notes.append(relative_time)
    notesg, notesc = history(notes, chunks, chunk_size)

    #Count cards
    for first_study_date in self.col.db.execute("select min(revlog.id)/1000 as date from cards, revlog where cards.id=revlog.cid and cards.queue>0 and cards.did in %s group by cards.id;" % self._limit() ):
        relative_time = int((now-first_study_date[0])/86400) #in days
        cards.append(relative_time)
    cardsg, cardsc = history(cards, chunks, chunk_size)
    #Draw graph
    txt += self._title(
        u"Движение вперёд" if lang=='ru' else _("Progress"), # Progress graph
        u"Количество карточек и записей,<br> которые вы разучили с течением времени" if lang=='ru' else _("The number of Anki cards & notes you have learned over time"))

    data = [
#        dict(data=cardsg, color=7, yaxis=1, bars={'show':False}, lines={"show":True }, stack=False, label=_("Cards")), #Putting cards and notes on the same graph extends the scale and makes the graph unreadable
        dict(data=notesg, color=colMtr, yaxis=1, bars={'show':False}, lines={"show":True }, stack=False, label=u"Уже известные записи" if lang=='ru' else _("Known notes")), # color=8
        dict(data=[], stack=False), #Workaround for some weird graph staking issue
        dict(data=cardsc, color=3, yaxis=2, bars={'show': True}, lines={"show":False}, stack=False, label=u"Новые карточки</br> из уже известных записей" if lang=='ru' else _("New cards from known notes")), 
        dict(data=[], stack=False),
        dict(data=notesc, color=7, yaxis=2, bars={'show': True}, lines={"show":False}, stack=False, label=u"Новые записи" if lang=='ru' else _("New notes")),
        ]
    txt += self._graph(id="progress_graph", data=data,
           ylabel = (u"Новые карточки" if lang=='ru' else (_("New cards per ")+_(chunk_name))), 
           ylabel2= (u"Сумма записей" if lang=='ru' else _("Cummulative notes")), 
           conf=dict( xaxis=dict(tickDecimals=0), yaxes=[dict(
                      tickDecimals=0, position="right")]))
    txt += (u"Всего стали известны на сегодня:<br> <b>%d</b> карточек и <b>%d</b> записей." if lang=='ru' else "<div>Total known today: <b>%d cards, %d notes</b></div>") %(len(cards), len(notes))
    return txt

def myTodayStats(self, _old):
    if self.type == 0:
        chunks = 30; chunk_size = 1; chunk_name="day"
    elif self.type == 1:
        chunks = 52; chunk_size = 7; chunk_name="week"
    else:
        chunks = None; chunk_size = 30; chunk_name="month"
    txt =  _old(self) #+ progressGraphs(self, chunks, chunk_size, chunk_name) 
    return txt

try:
    stats.CollectionStats.todayStats = wrap(stats.CollectionStats.todayStats, myTodayStats, "around") 
except AttributeError:
    #Happens on Anki 2.0.0, fixed at least in 2.0.14
    showInfo("The Progress Graph add-on is incompatible with your version of Anki.<br>Please upgrade to the latest version.<br>If the problem persists, please contact the author (<tt>tools -> add-ons -> Browse&install -> Browse -> Progress Graph -> Info -> Ask a question</tt>).")

##########################
# Learning_Achievements_cumulative_total_for_younglearning_card_and_mature_card.py
# Learning Achievements: cumulative total for young/learning card and mature card
# https://ankiweb.net/shared/info/2093985093
#

# -*- coding: utf-8 -*-
# Name: Achivements
# Version: 0.2
# Author: Hirose S.
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# A graph of learning achivements for Anki:
# This add-on provides a graph which enable you to grasp 
# your learning achievments at a glance.
# 

def achievementsGraph(self, _old):
    if self.type == 0:
        days = 30; chunk = 1
    elif self.type == 1:
        days = 52; chunk = 7
    else:
        days = None; chunk = 30

    # count the number of 3 types of cards each day
    lrn = _learningCards(self, days, chunk) # new learning cards each day
    mtr = _maturedCards(self, days, chunk)  # new mature cards each day
    flr = _failedCards(self, days, chunk)   # failed mature cards each day

    # count the current number of young/learning and mature cards
    curMtr, curYngLrn = _currentCards(self)

    if self.type == 0:
        chunks = 30; chunk_size = 1; chunk_name="day"
    elif self.type == 1:
        chunks = 52; chunk_size = 7; chunk_name="week"
    else:
        chunks = None; chunk_size = 30; chunk_name="month"

    txt = progressGraphs(self, chunks, chunk_size, chunk_name) 

    text = progressDaily(self, chunks, chunk_size, chunk_name)

    return  _old(self) + _plotAchievementsGraph(self, lrn, mtr, flr, curYngLrn, curMtr, days) + txt + text

def _plotAchievementsGraph(self, lrn, mtr, flr, curYngLrn, curMtr, days):
    # add dummy data if necessary
    for cards in (lrn, mtr, flr):
        if not cards:
            cards.append([0, 0])
        if cards[-1][0] != 0:
            cards.append([0,0])

    # number of days to calculate cumulative number of cards
    days2 = max(-mtr[0][0], -flr[0][0], -lrn[0][0]) + 1

    # fill missing data with 0
    for cards in (lrn, mtr, flr):
        for i in range(0, int(days2)):
            x = i+1-days2   # the day
            if cards[i][0] != x:
                cards.insert(i, [x, 0])

    # calculate cumulative number of cards
    cmlMtr = []     # mature cards
    cmlYngLrn = []  # young/learning cards
    for i in range(0, int(days2)):
        # the day
        day = i+1-days2
        # calculate sum of number of cards AFTER the day
        sumMtr = sum(x[1] for x in mtr[i+1:])
        sumFlr = sum(x[1] for x in flr[i+1:])
        sumLrn = sum(x[1] for x in lrn[i+1:])
        # calculate cumulative number of the day
        cMtr = curMtr - sumMtr + sumFlr
        cYngLrn = curYngLrn + sumMtr - sumFlr - sumLrn
        # append 
        cmlMtr.append([day, cMtr])
        cmlYngLrn.append([day, cYngLrn])

    # graph axis
    if days:
        xaxis = dict(max=0.5, min=-days+0.5, tickDecimals=0)
    else:
        xaxis = dict(max=0.5, tickDecimals=0)

    # graph title and subtitle
    title = u"Достижения" if lang=='ru' else "Achievements"
    subtitle = u"Количество <i>Mature</i> и <i>Young + Learn</i> карточек." if lang=='ru' else "The number of young+learn and mature cards."

    # graph label
    ylabel = _("Cards")
    ylabel2 = u"Сумма карточек" if lang=='ru' else "Cumulative Cards"

    # graph data
    data=[dict(data=mtr, color=colMtr, label=_("Mature"), stack=1), 
          dict(data=lrn, color=colYngLrn, label=_("Young")+" + "+_("Learn"), stack=1),
          dict(data=cmlMtr, color=colMtr, yaxis=2, 
                bars={'show': False}, lines=dict(show=True), stack=2),
          dict(data=cmlYngLrn, color=colYngLrn, yaxis=2, 
                bars={'show': False}, lines=dict(show=True), stack=3)]

    # display settings
    conf=dict(xaxis=xaxis, yaxes=[dict(min=0), dict(min=0, position="right")])

    # graph
    txt = self._title(_(title), _(subtitle))
    txt += self._graph(id="Achievements", ylabel=ylabel, ylabel2=ylabel2, 
                       data=data, conf=conf)
    return txt

def _maturedCards(self, num=7, chunk=1):
    lims = []
    if num is not None:
        lims.append("id > %d" % (
            (self.col.sched.dayCutoff-(num*chunk*86400))*1000))
    lim = self._revlogLimit()
    if lim:
        lims.append(lim)
    if lims:
        lim = "where " + " and ".join(lims)
    else:
        lim = ""
    if self.type == 0:
        tf = 60.0 # minutes
    else:
        tf = 3600.0 # hours
    if lim:
        return self.col.db.all("""
select
(cast((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
count(*) as count
from revlog %s and ivl >= 21 and lastivl < 21
group by day order by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)
    else:
        return self.col.db.all("""
select
(cast((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
count(*) as count
from revlog %s where ivl >= 21 and lastivl < 21
group by day order by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)

def _failedCards(self, num=7, chunk=1):
    lims = []
    if num is not None:
        lims.append("id > %d" % (
            (self.col.sched.dayCutoff-(num*chunk*86400))*1000))
    lim = self._revlogLimit()
    
    if lim:
        lims.append(lim)
    if lims:
        lim = "where " + " and ".join(lims)
    else:
        lim = ""
    if self.type == 0:
        tf = 60.0 # minutes
    else:
        tf = 3600.0 # hours
    
    if lim:
        return self.col.db.all("""
select
(cast((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
count(*) as count
from revlog %s and (ivl < lastivl and lastivl >= 21)
group by day order by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)
    else:
        return self.col.db.all("""
select
(cast((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
count(*) as count
from revlog %s where (ivl < lastivl and lastivl >= 21)
group by day order by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)        

def _learningCards(self, num=7, chunk=1):
    notes = [] 
    cards = []
    now = time.mktime(time.localtime())

    if self.type == 0:
        chunks = 30; chunk_size = 1; chunk_name="day"
    elif self.type == 1:
        chunks = 52; chunk_size = 7; chunk_name="week"
    else:
        chunks = None; chunk_size = 30; chunk_name="month"

    first_study_dates = self.col.db.execute("""
select
min(revlog.id)/1000 as date 
from cards, revlog where cards.id=revlog.cid and cards.queue>0 and cards.did in %s 
group by cards.id;""" % self._limit())
    for first_study_date in first_study_dates:
        relative_time = int((now-first_study_date[0])/86400)
        cards.append(relative_time)
    lrn = _learningCards2(cards, chunks, chunk_size)

    for i in range(0, len(lrn)):
        if lrn[i][1] != 0 or i == (len(lrn)-1):
            del lrn[0:i]
            break

    return lrn

def _learningCards2(data, chunks=None, chunk_size=1):
    if not chunks:
        try:
            chunks=max(data)/chunk_size+1 
        except:
            chunks = 1
        chunks = chunks + 1
    #showInfo(unicode(chunks))
    histogram = [0]*int(chunks)
    delta=[]
    date=-(chunks-1)
    for d in data:
        if d <= (chunks-1)*chunk_size:
            histogram[int(d/chunk_size)] += 1
    while len(histogram):
        v=histogram.pop()
        delta.append((date, v))
        date+=1
    return delta
 
def _currentCards(self):
    curMtr, curYngLrn = self.col.db.first("""
select
sum(case when queue=2 and ivl>= 21 then 1 else 0 end), 
sum(case when queue in (1,3) or (queue=2 and ivl < 21) then 1 else 0 end) 
from cards where did in %s""" % self._limit())
    if not curMtr: curMtr = 0
    if not curYngLrn: curYngLrn = 0
    return curMtr, curYngLrn

anki.stats.CollectionStats.cardGraph = wrap(anki.stats.CollectionStats.cardGraph, achievementsGraph, pos="")



##############################################
# 

# -*- coding: utf-8 ; mode: python -*-
#
# Copyright © 2014 Thomas TEMPÉ, <thomas.tempe@alysse.org>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.

###########################
# Daily_Totals.py
# Daily Totals
# https://ankiweb.net/shared/info/1075380732
#

# Progress graph for Anki 2
########################################################################
'''
This module draws two stats graphs in Anki's "stats" window, showing the 
number of notes and cards learned over time.
'''

from anki import stats
import time, re, sys, math

ltime = time.localtime();
now = time.time() - ltime[3]*3600 - ltime[4]*60 - ltime[5] + 86400 + 4*3600;

def history(data, chunks=None, chunk_size=1):
    #Compute history
    if not chunks:
        try:
            chunks=max(data)/chunk_size+1 #nb of periods to look back
        except:
            chunks = 1 #This happens if the deck is empty
    histogram = [0]*int(chunks+1)
    cumul=[]
    delta=[]
    subtotal=0
    date=-chunks
    #Fill histogram, as a list. d = nb of days in the past (0=today).
    for d in data:
        if d <= chunks*chunk_size:
            histogram[int(math.floor(d/chunk_size))] += 1
        else:
            subtotal+=1
    #Fill history, as a list of coordinates: [(relative_day, nb_values),...]
    while len(histogram):
        v=histogram.pop()
        subtotal +=v
        cumul.append((date, subtotal))
        delta.append((date, v))
        
        #delta.append((date, 2))
        #cumul.append((date, 1))
        date+=1
    return cumul, delta

def historyV2(db, query_sql, chunks=None, chunk_size=1):
    #Compute history
    if not chunks:
        try:
            chunks=max(data)/chunk_size+1 #nb of periods to look back
        except:
            tmp_query = "SELECT min(revlog.id) FROM revlog";
            min_revlog = 0
            for temp_arr in db.execute( tmp_query):
                min_revlog = temp_arr[0]
            if min_revlog == 0:
                chunks = 1
            else:
                chunks = math.ceil((now*1000-min_revlog)/(chunk_size*24*3600*1000))
            chunks = int(chunks)
    histogram = [0]*(chunks+1)
    delta=[]
    date=-chunks
    #Fill histogram, as a list. d = nb of days in the past (0=today).
    for temp_arr in db.execute( query_sql):
        relative_days_i = temp_arr[0]
        count_i = temp_arr[1]
        if relative_days_i <= chunks*chunk_size:
            histogram[int(math.floor(relative_days_i/chunk_size))] += count_i
    #Fill history, as a list of coordinates: [(relative_day, nb_values),...]
    while len(histogram):
        v=histogram.pop()
        delta.append((date, v/chunk_size))
        
        #delta.append((date, 2))
        #cumul.append((date, 1))
        date+=1
    return delta

##################################################
def progressDaily(self, chunks, chunk_size, chunk_name):
    #a = "%s "  % chunks
    #tmp_query = "SELECT min(revlog.id) FROM revlog"
    #min_revlog = 0
    #for temp_arr in self.col.db.execute( tmp_query):
    #    min_revlog = temp_arr[0]
    #if min_revlog == 0:
    #    chunks = 1
    #else:
    #    chunks = math.ceil((now*1000-min_revlog)/(chunk_size*24*3600*1000))
    #chunks = int(chunks)
    #a += "%s" %chunks
    #return a;
    txt=""
    totalCards = [] #list of 1st-review dates for all your notes
    reviewCards = [] #list of 1st-review dates for all your cards
    newCards = [] #list of 1st-review dates for all your cards
    
    #offset = time.gmtime() - time.localtime();
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset = - (time.altzone if is_dst else time.timezone)
    
    
    #total_query = "select cast(((%s - revlog.id/1000)/86400) as int) as date,cards.nid from cards,revlog WHERE ((revlog.ease > 1 AND revlog.lastIvl != -60) OR revlog.ease > 2) AND cards.id=revlog.cid and cards.did in %s group by cards.nid,date ORDER BY revlog.id ASC" % (now, self._limit())
    #debug_txt = ""
    #cardsSeen=[]
    ##TOTAL CARDS
    #for temp_arr in self.col.db.execute( total_query):
    #    relativeDays = temp_arr[0]
    #    cardId = temp_arr[1]
    #    totalCards.append(relativeDays)
    #    isSeen = 0;
    #    for card_id_i in cardsSeen:
    #        if card_id_i == cardId:
    #            isSeen = 1
    #    x = 1;
    #    if isSeen == 0:
    #        newCards.append(relativeDays)
    #    else:
    #        reviewCards.append(temp_arr[0])
    #    cardsSeen.append(cardId)
    #
    
    now_str = "%s" % now
    limit = self._limit();
    total_query = "SELECT `date`,count() FROM (select cast((("+now_str+" - revlog.id/1000)/86400) as int) as date,cards.nid from cards,revlog WHERE ((revlog.ease > 1 AND revlog.lastIvl != -60) OR revlog.ease > 2) AND cards.id=revlog.cid and cards.did in "+limit+" group by cards.nid,date ORDER BY revlog.id ASC) as r GROUP BY `date`";
    base_query = "SELECT `date`,count() FROM (SELECT r. `date`,r.nid,r2.max,r2.min FROM (select cast((("+now_str+" - revlog.id/1000)/86400) as int) as date,cards.nid from cards,revlog WHERE ((revlog.ease > 1 AND revlog.lastIvl != -60) OR revlog.ease > 2) AND cards.id=revlog.cid and cards.did in "+limit+" group by cards.nid,date ORDER BY revlog.id ASC) as r,(SELECT nid,max(date) as `max`,min(date) as min FROM (select cast((("+now_str+" - revlog.id/1000)/86400) as int) as date,cards.nid from cards,revlog WHERE ((revlog.ease > 1 AND revlog.lastIvl != -60) OR revlog.ease > 2) AND cards.id=revlog.cid and cards.did in "+limit+" group by cards.nid,date ORDER BY revlog.id ASC) as b GROUP BY nid) as r2 WHERE r.nid=r2.nid AND ====) as r GROUP BY `date`";
    review_query   = base_query.replace("====","r2.max!=r2.min") 
    newcards_query = base_query.replace("====","r2.max==r2.min")     
    
    
    db = self.col.db
    totalnotesc = historyV2(db, total_query, chunks, chunk_size)
    reviewcardsc = historyV2(db, review_query, chunks, chunk_size)
    newcardsc = historyV2(db, newcards_query, chunks, chunk_size)
    #totalnotesg, totalnotesc = history(totalCards, chunks, chunk_size)
    #reviewcardsg, reviewcardsc = history(reviewCards, chunks, chunk_size)
    #newcardsg, newcardsc = history(newCards, chunks, chunk_size)
    
    #Draw graph
    txt += self._title(
        _("Daily Totals"),
        _("The number of Anki cards reviewed in one "+chunk_name))

    data_total = [
        dict(data=totalnotesc, color=8, yaxis=1, bars={'show':False}, lines={"show":True }, stack=False),
        dict(data=[], stack=False), #Workaround for some weird graph staking issue
        ]
    txt += self._graph(id="unique_total_cards_graph", data=data_total,
                       conf=dict(
            xaxis=dict(tickDecimals=0), yaxes=[dict(
                    tickDecimals=0, position="right")]))
    txt += self._title(
        _("Unique Review Cards"),
        _("The number of unique Anki \"review cards\" reviewed in one "+chunk_name))

    data_review = [
        dict(data=reviewcardsc, color=8, yaxis=1, bars={'show':False}, lines={"show":True }, stack=False),
        dict(data=[], stack=False), #Workaround for some weird graph staking issue
        ]
    txt += self._graph(id="unique_review_cards_graph", data=data_review,
                       conf=dict(
            xaxis=dict(tickDecimals=0), yaxes=[dict(
                    tickDecimals=0, position="right")]))
    txt += self._title(
        _("Unique New Cards"),
        _("The number of unique Anki \"new cards\" reviewed in one "+chunk_name))

    data_new = [
        dict(data=newcardsc, color=8, yaxis=1, bars={'show':False}, lines={"show":True }, stack=False),
        dict(data=[], stack=False), #Workaround for some weird graph staking issue
        ]
    txt += self._graph(id="unique_new_cards_graph", data=data_new,
                       conf=dict(
            xaxis=dict(tickDecimals=0), yaxes=[dict(
                    tickDecimals=0, position="right")]))
    
    #final totals
    today_total = 0;
    today_review = 0;
    today_new    = 0;
    
    yesterday_total = 0;
    yesterday_review = 0;
    yesterday_new    = 0;
    
    if len(totalnotesc) > 0:
        today_total = totalnotesc.pop()[1];
    if len(reviewcardsc) > 0:
        today_review = reviewcardsc.pop()[1];
    if len(newcardsc) >0:
        today_new = newcardsc.pop()[1];
        
        
    if len(totalnotesc) > 0:
        yesterday_total = totalnotesc.pop()[1];
    if len(reviewcardsc) > 0:
        yesterday_review = reviewcardsc.pop()[1];
    if len(newcardsc) >0:
        yesterday_new = newcardsc.pop()[1];
    
    
    
    #txt += "%d"%utc_offset
    if chunk_size == 1:
      if lang == 'ru':
        txt += "<style>"
        txt += "#maTable { border-collapse:collapse; margin-top: 1em; margin-bottom: .5em; }"
        txt += "#maTable thead { border:dashed 1px black; }"
        txt += "#maTable tbody { border:dashed 1px black; }"
        txt += "#maTable tr:nth-child(2n) { background-color: #e3e3e3; }"
        txt += "#maTable td { padding: .25em 1.25em .25em 1.5em; }"
        txt += "#maTable td b { font-weight: bold; color: dodgerblue; }"
        txt += "#maTable td s { text-decoration: none; color: dodgerblue; }"
        txt += "#maTable thead tr:first-child td, #maTable tbody tr:first-child td { padding-top: .5em; }"
        txt += "#maTable thead tr:last-of-type td, #maTable tbody tr:last-of-type td { padding-bottom: .5em; }"
        txt += "</style>"
        txt += "<table id=maTable><thead>"
        txt += u"<tr><td>Всего уникальных <i>карточек</i> <b>сегодня</b>: </td><td style='text-align:right;'><b>%d</b></td></tr>" %today_total;
        txt += u"<tr><td>В том числе <s>повторяемых</s>: </td><td style='text-align:right;'><b>%d</b></td></tr>" %today_review;
        txt += u"<tr><td>И <s>новых</s>: </td><td style='text-align:right;'><b>%d</b></td></tr>" %today_new;
        txt += '</thead><tbody>';
        txt += u"<tr><td>Всего уникальных <i>карточек</i> <b>вчера</b>: </td><td style='text-align:right;'><b>%d</b></td></tr>" %yesterday_total;
        txt += u"<tr><td>В том числе <s>повторяемых</s>: </td><td style='text-align:right;'><b>%d</b></td></tr>" %yesterday_review;
        txt += u"<tr><td>И <s>новых</s>: </td><td style='text-align:right;'><b>%d</b></td></tr>" %yesterday_new;
        txt += "</tbody></table>"
      else:
        txt += "<div>Total unique cards today: <b>%d cards</b></div>" %today_total;
        txt += "<div>Total unique review cards today: <b>%d cards</b></div>" %today_review;
        txt += "<div>Total unique new cards today: <b>%d cards</b></div>" %today_new;
        txt += '<br />';
        txt += "<div>Total unique cards yesterday: <b>%d cards</b></div>" %yesterday_total;
        txt += "<div>Total unique review cards yesterday: <b>%d cards</b></div>" %yesterday_review;
        txt += "<div>Total unique new cards yesterday: <b>%d cards</b></div>" %yesterday_new;
    #txt += "<br /><br /><br /><br />NOW: %s" % now;
    #txt += " <br />Total Query:<br />" + total_query+"<br /><br /><br />"
    return txt

def maTodayStats(self, _old):
    if self.type == 0:
        chunks = 30; chunk_size = 1; chunk_name="day"
    elif self.type == 1:
        chunks = 52; chunk_size = 7; chunk_name="week"
    else:
        chunks = None; chunk_size = 30; chunk_name="month"
    txt = _old(self)
    txt+= progressDaily(self, chunks, chunk_size, chunk_name)
    return txt

#try:
#    stats.CollectionStats.todayStats = wrap(stats.CollectionStats.todayStats, maTodayStats, "around")
#except AttributeError:
#    #Happens on Anki 2.0.0, fixed at least in 2.0.14
#    showInfo("The Progress Graph add-on is incompatible with your version of Anki.<br>Please upgrade to the latest version.<br>If the problem persists, please contact the author (<tt>tools -> add-ons -> Browse&install -> Browse -> Progress Graph -> Info -> Ask a question</tt>).")
#    pass




############################################################
# Separate_Learn_and_Relearn_in_the_Answer_Buttons_graph.py
# Separate Learn and Relearn in the Answer Buttons graph
# https://ankiweb.net/shared/info/1999018922
#

# -*- coding: utf-8 -*-
# Relearn Stats 1.0, an Anki addon to separate Learn and Relearn in the Answer Buttons graph
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Modified from Anki source code (2.0.31 and possibly earlier versions) in 2014-2015 by Teemu Pudas
# Anki is Copyright: Damien Elmes <anki@ichi2.net> 
# (I include his email address because that's how it is in the original copyright notice in the Anki source code.
# Don't contact him about bugs in this addon (they're not his fault), use http://anki.tenderapp.com/discussions/add-ons instead)

from anki.db import DB
from anki.stats import *

def myExecute(self, sql, *a, **kw):
    
    # _eases() - add a fourth category for relearn
    if "(case when type in (0,2) and ease = 4 then 3 else ease end), count() from revlog" in sql:
        sql = sql.replace("when type in (0,2) then 0", """
when type = 0 then 0
when type = 2 then 3
""", 1)

    return oldExecute(self, sql, *a, **kw)


def easeGraph(self):
    # 3 + 4 + 4 + 4 + spaces on sides and middle = 18
    # yng starts at 3+1 = 4
    # mtr starts at 4+4+1 = 9
    # rel starts at 9+4+1 = 14
    d = {'lrn':[], 'yng':[], 'mtr':[], 'rel': []}
    types = ("lrn", "yng", "mtr", "rel")
    eases = self._eases()
    nonzero = False
    for (type, ease, cnt) in eases:
        if type == 1:
            ease += 4
        elif type == 2:
            ease += 9
        elif type == 3:
            ease += 14
        n = types[type]
        if cnt > 0:
            nonzero = True
        d[n].append((ease, cnt))
    if not nonzero:
        return ""
    ticks = [[1,1],[2,2],[3,3],
             [5,1],[6,2],[7,3],[8,4],
             [10, 1],[11,2],[12,3],[13,4],
             [15, 1],[16,2],[17,3]]
    txt = self._title(_("Answer Buttons"),
                      _("The number of times you have pressed each button."))
    txt += self._graph(id="ease", data=[
        dict(data=d['lrn'], color=colLearn, label=_("Learning")),
        dict(data=d['yng'], color=colYoung, label=_("Young")),
        dict(data=d['mtr'], color=colMature, label=_("Mature")),
        dict(data=d['rel'], color=colRelearn, label=_("Relearn")),
        ], type="barsLine", conf=dict(
            xaxis=dict(ticks=ticks, min=0, max=18)),
        ylabel=_("Answers"))
    txt += self._easeInfo(eases)
    return txt

def _easeInfo(self, eases):
    types = {0: [0, 0], 1: [0, 0], 2: [0,0], 3: [0, 0]}
    for (type, ease, cnt) in eases:
        if ease == 1:
            types[type][0] += cnt
        else:
            types[type][1] += cnt
    i = []
    for type in range(4):
        (bad, good) = types[type]
        tot = bad + good
        try:
            pct = good / float(tot) * 100
        except:
            pct = 0
        i.append(_(
            "Correct: <b>%(pct)0.2f%%</b><br>(%(good)d of %(tot)d)") % dict(
            pct=pct, good=good, tot=tot))
    return ("""
<center><table width=%dpx><tr><td width=50></td><td align=center>""" % self.width +
            "</td><td align=center>".join(i) +
            "</td></tr></table></center>")

oldExecute = DB.execute
DB.execute = myExecute

CollectionStats._easeInfo = _easeInfo
CollectionStats.easeGraph = easeGraph


##################################################
# Maturing_Cards.py
# Maturing Cards
# https://ankiweb.net/shared/info/1147586609
#

"""
Name: Maturing Cards
Filename: Maturing Cards.py
Version: 0.3
Author: Kenishi
Desc:    Generates a new graph that shows the number of cards that are maturing in a time frame
        
        Report bugs to https://github.com/Kenishi/Maturing-Cards
"""

###Constants###
DEBUG = False
debugOut = None

# Graph Bar Color
reviewMatureC = "#007700" # "#72a5d9"

def log(str):
    ##USAGE: Debug logging, make sure a <deck name>.media folder exists in deck's root directory for log to be created
    ##RETURNS: Nothing
    global debugOut
    
    if DEBUG:
        if not debugOut:
            debugOut = open("""D:\mr_debug.txt""", mode="a")
        debugOut.write(repr(str))
        debugOut.close()


def maturingGraph(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']  ### Reference back to cardGraph()
    
    if self.type == 0:
        days = 30; chunk = 1
    elif self.type == 1:
        days = 52; chunk = 7
    else:
        days = None; chunk = 30
    return old(self) + _plotMaturingGraph(self, _maturedCardz(self,days,chunk),
                            days,
                            u"Созревание карт" if lang=='ru' else _("Maturing Cards"))

# data=[dict(data=mtr, color=reviewMatureC, label=_("Mature"), stack=1)]

def _plotMaturingGraph(self, data, days, title):
    if not data:
        return ""
    max_yaxis=0
    for (x,y) in data: # Unzip the data
        if y > max_yaxis:
            test = int(round((float(y)/10))*10)
            if test < y:
                max_yaxis = test + 10
            else:
                max_yaxis = test
                
    txt = self._title(u"Развитые карты" if lang=='ru' else _("Maturing Cards"),
                      u"Количество <i>Mature</i> карточек, у которых<br> интервал до следующего показа уже превысил 20 дней,<br> а предыдущий интервал был меньше 21 дня." if lang=='ru' else _("Number of cards matured."))
    txt += self._graph(id="maturing", data=[dict(data=data, label=_("Mature"), color=reviewMatureC)], conf=dict(xaxis=dict(max=0.5),yaxis=dict(min=0,max=max_yaxis)))

    return txt


def _maturedCardz(self, num=7, chunk=1):
    lims = []
    if num is not None:
        lims.append("id > %d" % (
            (self.col.sched.dayCutoff-(num*chunk*86400))*1000))
    lim = self._revlogLimit()
    if lim:
        lims.append(lim)
    if lims:
        lim = "where " + " and ".join(lims)
    else:
        lim = ""
    if self.type == 0:
        tf = 60.0 # minutes
    else:
        tf = 3600.0 # hours
    if lim:
        return self.col.db.all("""
SELECT
(CAST((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
COUNT(*) as count
FROM revlog %s and ivl >= 21 and lastIvl < 21
GROUP BY day ORDER by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)
    else:
        return self.col.db.all("""
SELECT
(CAST((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
COUNT(*) as count
FROM revlog %s WHERE ivl >= 21 and lastIvl < 21
GROUP BY day ORDER by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)

anki.stats.CollectionStats.cardGraph = wrap(anki.stats.CollectionStats.cardGraph, maturingGraph, pos="")


#################################################################
# Failed_Mature_Cards.py
# Failed Mature Cards
# https://ankiweb.net/shared/info/1314513660
#

"""
Name: Failed Mature Cards
Filename: Failed Mature Cards.py
Version: 0.4
Author: Kenishi
Desc:	Generates a new graph that shows the number of mature cards that were failed over a time period
		
		Report bugs to https://github.com/Kenishi/Failed-Mature-Cards
"""

def failingGraph(*args, **kwargs):
	self = args[0]
	old = kwargs['_old']  ### Reference back to cardGraph()
	
	if self.type == 0:
		days = 30; chunk = 1
	elif self.type == 1:
		days = 52; chunk = 7
	else:
		days = None; chunk = 30
	return old(self) + _pilotFailingGraph(self, _failingCardes(self,days,chunk),
							days,
							_("Failing Mature Cards"))

def _pilotFailingGraph(self,data, days, title):
	if not data:
		return ""
	max_yaxis=0
	for (x,y) in data: # Unzip the data
		if y > max_yaxis:
			test = int(round((float(y)/10))*10)
			if test < y:
				max_yaxis = test + 10
			else:
				max_yaxis = test
				
	txt = self._title(_("Failed Mature Cards"),
					  _("Number of matured cards failed."))
	txt += self._graph(id="failing", data=[dict(data=data, color="#DE8073")], conf=dict(xaxis=dict(max=0.5),yaxis=dict(min=0,max=max_yaxis)))

	return txt

def _failingCardes(self, num=7, chunk=1):
	lims = []
	if num is not None:
		lims.append("id > %d" % (
			(self.col.sched.dayCutoff-(num*chunk*86400))*1000))
	lim = self._revlogLimit()
	
	if lim:
		lims.append(lim)
	if lims:
		lim = "where " + " and ".join(lims)
	else:
		lim = ""
	if self.type == 0:
		tf = 60.0 # minutes
	else:
		tf = 3600.0 # hours
	
	if lim:
		return self.col.db.all("""
SELECT
(CAST((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
COUNT(*) as count
FROM revlog %s and (ivl < lastIvl and lastIvl >= 21)
GROUP BY day ORDER by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)
	else:
		return self.col.db.all("""
SELECT
(CAST((id/1000 - :cut) / 86400.0 as int))/:chunk as day,
COUNT(*) as count
FROM revlog %s WHERE (ivl < lastIvl and lastIvl >= 21)
GROUP BY day ORDER by day""" % lim, cut=self.col.sched.dayCutoff, tf=tf, chunk=chunk)		

anki.stats.CollectionStats.cardGraph = wrap(anki.stats.CollectionStats.cardGraph, failingGraph, pos="")	




#################################################################
# Stats_Expected_number_of_cards.py
# Stats: Expected number of cards
# https://ankiweb.net/shared/info/2464818309
#

# -*- coding: utf-8 -*-
# Copyright: Fabien  S H U M - K I N G
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Displays in the stats for each deck (or the current one) the number
# of expected cards per day, according to their frequency.
# For example, a card with a frequency of 3 days count as 1/3 card per day

# version: 0.2

# save previous graph func
fsk_old_cardGraph = anki.stats.CollectionStats.todayStats

def fskNewGraph(self):
	out = self._title(u"<span style=font-size:smaller;>Среднее количество<br> <span style=font-weight:400;>ожидаемых карточек <i>в день</i></span></span>" if lang=='ru' else _("Average expected cards"),"")
	deck_stats = []
	# for each of the decks or the current deck (according to stats option)
	for deck in self.col.decks.all() if self.wholeCollection else (self.col.decks.current(),):
		# get sum 
		res = self.col.db.scalar(
		"select round(sum(1./ivl),2) from cards where did=? and ivl>0 and queue!=-1",
		deck['id'])
		if res>0:
			deck_stats.append((deck["name"], res))
	# decreasing count sort
	deck_stats.sort(lambda x, y: -cmp(x[1], y[1]))
	
	# add sum if many decks stats
	if len(deck_stats)>1:
		deck_stats.append((_("Total"), sum(map(lambda x: x[1], deck_stats))))

	# create lines
	lines = []
	for st in deck_stats:
		self._line(lines, "<span style=white-space:nowrap;>"+st[0].replace('::','<br>&mdash;&nbsp;')+"</span>", ("&nbsp; <big style=color:dodgerblue;>{0}</big> "+("" if lang=='ru' else _("cards per day"))).format(st[1]))
		
	out += self._lineTbl(lines)
	return fsk_old_cardGraph(self) + out

# replace graph func
anki.stats.CollectionStats.todayStats = fskNewGraph


