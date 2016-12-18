# -*- coding: utf-8 -*-
#import lxml.html  	# hier für Konvertierungen - Funktionen von Plex nicht akzeptiert
#import requests	# u.a. Einlesen HTML-Seite, Methode außerhalb Plex-Framework 
import string
import urllib		# urllib.quote()
import os, subprocess 	# u.a. Behandlung von Pfadnamen
import re			# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import time
import datetime
import json			# json -> Textstrings

import locale

import updater


# +++++ ARD Mediathek 2016 Plugin for Plex +++++

VERSION =  '2.6.3'		
VDATE = '18.12.2016'

# 
#	


# (c) 2016 by Roland Scholz, rols1@gmx.de
#	GUI by Arauco (Plex-Forum) from V1.5.1
# 
#     Testing Enviroment -> README.md
# 
# Licensed under the GPL, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  
#    http://www.gnu.org/licenses/gpl-3.0-standalone.html
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Artwork (folder 'Resources'): (c) ARD

####################################################################################################

NAME = 'ARD Mediathek 2016'
PREFIX = '/video/ardmediathek2016'			
												
PLAYLIST = 'livesenderTV.xml'				# TV-Sender-Logos erstellt von: Arauco (Plex-Forum). 											
PLAYLIST_Radio = 'livesenderRadio.xml'		# Liste der RadioAnstalten. Einzelne Sender und Links werden 
											# 	vom Plugin ermittelt
											# Radio-Sender-Logos erstellt von: Arauco (Plex-Forum). 

ART = 'art.png'								# ARD 
ICON = 'icon.png'							# ARD
ICON_SEARCH = 'ard-suche.png'						
ICON_ZDF_SEARCH = 'zdf-suche.png'						

ICON_MAIN_ARD = 'ard-mediathek.png'			
ICON_MAIN_ZDF = 'zdf-mediathek.png'			
ICON_MAIN_TVLIVE = 'tv-livestreams.png'		
ICON_MAIN_RADIOLIVE = 'radio-livestreams.png' 	
ICON_MAIN_UPDATER = 'plugin-update.png'		
ICON_UPDATER_NEW = 'plugin-update-new.png'
ICON_PREFS = 'plugin-preferences.png'


ICON_ARD_AZ = 'ard-sendungen-az.png' 			
ICON_ARD_VERP = 'ard-sendung-verpasst.png'			
ICON_ARD_RUBRIKEN = 'ard-rubriken.png' 			
ICON_ARD_Themen = 'ard-themen.png'	 			
ICON_ARD_Filme = 'ard-ausgewaehlte-filme.png' 	
ICON_ARD_FilmeAll = 'ard-alle-filme.png' 		
ICON_ARD_Dokus = 'ard-ausgewaehlte-dokus.png'			
ICON_ARD_DokusAll = 'ard-alle-dokus.png'		
ICON_ARD_Serien = 'ard-serien.png'				
ICON_ARD_MEIST = 'ard-meist-gesehen.png' 	
ICON_ARD_NEUESTE = 'ard-neueste-videos.png' 	
ICON_ARD_BEST = 'ard-am-besten-bewertet.png' 	

ICON_ZDF_AZ = 'zdf-sendungen-az.png' 		
ICON_ZDF_VERP = 'zdf-sendung-verpasst.png'	
ICON_ZDF_RUBRIKEN = 'zdf-rubriken.png' 		
ICON_ZDF_Themen = 'zdf-themen.png'			
ICON_ZDF_MEIST = 'zdf-meist-gesehen.png' 	
ICON_ZDF_BARRIEREARM = 'zdf-barrierearm.png' 
ICON_ZDF_HOERFASSUNGEN = 'zdf-hoerfassungen.png' 
ICON_ZDF_UNTERTITEL = 'zdf-untertitel.png'
ICON_ZDF_INFOS = 'zdf-infos.png'
ICON_ZDF_BILDERSERIEN = 'zdf-bilderserien.png'

ICON_OK = "icon-ok.png"
ICON_WARNING = "icon-warning.png"
ICON_NEXT = "icon-next.png"
ICON_CANCEL = "icon-error.png"
ICON_MEHR = "icon-mehr.png"
ICON_SAVE = "icon-save.png"
ICON_DELETE = "icon-delete.png"


BASE_URL = 'http://www.ardmediathek.de'
ARD_VERPASST = '/tv/sendungVerpasst?tag='		# ergänzt mit 0, 1, 2 usw.
ARD_AZ = '/tv/sendungen-a-z?buchstabe='			# ergänzt mit 0-9, A, B, usw.
ARD_Suche = '/tv/suche?searchText='				# ergänzt mit Suchbegriff
ARD_Live = '/tv/live'

# Aktualisierung der ARD-ID's in Update_ARD_Path
ARD_Rubriken = 'http://www.ardmediathek.de/tv/Rubriken/mehr?documentId=21282550'
ARD_Themen = 'http://www.ardmediathek.de/tv/Themen/mehr?documentId=21301810'
ARD_Serien = 'http://www.ardmediathek.de/tv/Serien/mehr?documentId=26402940'
ARD_Dokus = 'http://www.ardmediathek.de/tv/Ausgew%C3%A4hlte-Dokus/mehr?documentId=33649086'
ARD_DokusAll = 'http://www.ardmediathek.de/tv/Alle-Dokus-Reportagen/mehr?documentId=29897594'
ARD_Filme = 'http://www.ardmediathek.de/tv/Ausgew%C3%A4hlte-Filme/mehr?documentId=33649088'
ARD_FilmeAll = 'http://www.ardmediathek.de/tv/Alle-Filme/mehr?documentId=31610076'
ARD_Meist = 'http://www.ardmediathek.de/tv/Meistabgerufene-Videos/mehr?documentId=23644244'
ARD_Neu = 'http://www.ardmediathek.de/tv/Neueste-Videos/mehr?documentId=21282466'
ARD_Best = 'http://www.ardmediathek.de/tv/Am-besten-bewertet/mehr?documentId=21282468'
ARD_RadioAll = 'http://www.ardmediathek.de/radio/live?genre=Alle+Genres&kanal=Alle'


# Relaunch der Mediathek beim ZDF ab 28.10.2016: xml-Service abgeschaltet
ZDF_BASE				= 'https://www.zdf.de'
# ZDF_Search_PATH: siehe ZDF_Search, ganze Sendungen, sortiert nach Datum, bei Bilderserien ohne ganze Sendungen
ZDF_SENDUNG_VERPASST 	= 'https://www.zdf.de/sendung-verpasst?airtimeDate=%s'  # Datumformat 2016-10-31
ZDF_SENDUNGEN_AZ		= 'https://www.zdf.de/sendungen-a-z?group=%s'			# group-Format: a,b, ... 0-9: group=0+-+9
ZDF_SENDUNGEN_MEIST		= 'https://www.zdf.de/meist-gesehen'
ZDF_BARRIEREARM		= 'https://www.zdf.de/barrierefreiheit-im-zdf'

REPO_NAME = 'Plex-Plugin-ARDMediathek2016'
GITHUB_REPOSITORY = 'rols1/' + REPO_NAME
myhost = 'http://127.0.0.1:32400'


''' 
####################################################################################################
TV-Live-Sender der Mediathek: | ARD-Alpha | BR |Das Erste | HR | MDR | NDR | RBB | SR | SWR | 
	WDR | tagesschau24 |  | KIKA | PHOENIX | Deutsche Welle
	zusätzlich: Tagesschau | NDR Fernsehen Hamburg, Mecklenburg-Vorpommern, Niedersachsen, Schleswig-Holstein |
	RBB Berlin, Brandenburg | MDR Sachsen-Anhalt, Sachsen, Thüringen

TV-Live-Sender des ZDF: ZDF | ZDFneo | ZDFinfo | 3Sat | ARTE (Sonderbehandlung im Code für ARTE 
	wegen relativer Links in den m3u8-Dateien)

TV-Live-Sender Sonstige: NRW.TV | Joiz | DAF | N24 | n-tv

Radio-Live-Streams der ARD: alle Radiosender von Bayern, HR, mdr, NDR, Radio Bremen, RBB, SR, SWR, WDR, 
	Deutschlandfunk. Insgesamt 10 Stationen, 63 Sender

Versions-Historie: siehe Datei HISTORY
####################################################################################################
'''

def Start():
	#Log.Debug()  	# definiert in Info.plist
	# Problem Voreinstellung Plakate/Details/Liste:
	#	https://forums.plex.tv/discussion/211755/how-do-i-make-my-objectcontainer-display-as-a-gallery-of-thumbnails
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	#ObjectContainer.art        = R(ART)
	ObjectContainer.art        = R(ICON)  # gefällt mir als Hintergrund besser
	ObjectContainer.title1     = NAME
	#ObjectContainer.view_group = "InfoList"

	HTTP.CacheTime = CACHE_1HOUR # Debugging: falls Logdaten ausbleiben, Browserdaten löschen

#----------------------------------------------------------------
# handler bindet an das bundle
@route(PREFIX)
@handler(PREFIX, NAME, art = ART, thumb = ICON)
def Main():
	Log('Funktion Main'); Log(PREFIX); Log(VERSION); Log(VDATE)
	Log('Client: '); Log(Client.Platform)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	# Plex akzeptiert nur InfoList + List, keine
																			# Auswirkung auf Wiedergabe im Webplayer
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ARD, name="ARD Mediathek"), title="ARD Mediathek",
		summary='', tagline='TV', thumb=R(ICON_MAIN_ARD)))
		
	oc.add(DirectoryObject(key=Callback(Main_ZDF, name="ZDF Mediathek"), title="ZDF Mediathek", 
		summary='', tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		
	oc.add(DirectoryObject(key=Callback(SenderLiveListePre, title='TV-Livestreams'), title='TV-Livestreams',
		summary='', tagline='TV', thumb=R(ICON_MAIN_TVLIVE)))
	oc.add(DirectoryObject(key=Callback(RadioLiveListe, path=ARD_RadioAll, title='Radio-Livestreams'), 
		title='Radio-Livestreams', summary='', tagline='Radio', thumb=R(ICON_MAIN_RADIOLIVE)))

	repo_url = 'https://github.com/{0}/releases/'.format(GITHUB_REPOSITORY)
	oc.add(DirectoryObject(key=Callback(SearchUpdate, title='Plugin-Update'), 
		title='Plugin-Update | akt. Version: ' + VERSION + ' vom ' + VDATE,
		summary='Suche nach neuen Updates starten', tagline='Bezugsquelle: ' + repo_url, thumb=R(ICON_MAIN_UPDATER)))
		
	oc.add(DirectoryObject(key = Callback(Main_Options, title='Einstellungen'), title = 'Einstellungen', 
		summary = 'Live-TV-Sender: EPG-Daten verwenden, verfuegbare Bandbreiten anzeigen', 
		thumb = R(ICON_PREFS)))
	return oc
	
#----------------------------------------------------------------
@route(PREFIX + '/Main_ARD')
def Main_ARD(name):
	Log('Funktion Main_ARD'); Log(PREFIX); Log(VERSION); Log(VDATE)	
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	
	oc = home(cont=oc, ID=NAME)							# Home-Button	
	
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ARD, name=name),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(Search,  channel='ARD', s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))
		
	title = 'Sendung Verpasst (1 Woche)'
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name), title=title,
		summary=title, tagline='TV', thumb=R(ICON_ARD_VERP)))
	title = 'Sendungen A-Z'
	oc.add(DirectoryObject(key=Callback(SendungenAZ, name='Sendungen 0-9 | A-Z'), title='Sendungen A-Z',
		summary=title, tagline='TV', thumb=R(ICON_ARD_AZ)))
						
		
	title = 'Ausgewählte Filme'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Filme, next_cbKey='SingleSendung'),
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_Filme)))
	title = 'Alle Filme'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_FilmeAll, next_cbKey='SingleSendung'),
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_FilmeAll)))
	title = 'Ausgewählte Dokus'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Dokus, next_cbKey='SingleSendung'), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_Dokus)))
	title = 'Alle Dokus'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_DokusAll, next_cbKey='SingleSendung'),
		title=title,summary=title, tagline='TV', thumb=R(ICON_ARD_DokusAll)))
	title = 'Themen'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Themen, next_cbKey='SinglePage'),
		 title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_Themen)))
	title = 'Serien'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Serien, next_cbKey='SinglePage'), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_Serien)))
	title = 'Rubriken'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Rubriken, next_cbKey='SinglePage'),
		 title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_RUBRIKEN)))
	title = 'Meist Gesehen'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Meist, next_cbKey='SingleSendung'), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_MEIST)))
	title = 'neueste Videos'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Neu, next_cbKey='SingleSendung'), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_NEUESTE)))
	title = 'am besten bewertet'
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title, morepath=ARD_Best, next_cbKey='SingleSendung'),
		 title=title, summary=title, tagline='TV', thumb=R(ICON_ARD_BEST)))
	return oc	
	
#---------------------------------------------------------------- 
@route(PREFIX + '/Main_ZDF')
def Main_ZDF(name):
	Log('Funktion Main_ZDF'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art, title1=name)	
	oc = home(cont=oc, ID=NAME)								# Home-Button	
	
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ZDF, name=name),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_ZDF_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(ZDF_Search, s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_ZDF_SEARCH)))
		
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name), title="Sendung Verpasst (1 Woche)",
		thumb=R(ICON_ZDF_VERP)))
	oc.add(DirectoryObject(key=Callback(ZDFSendungenAZ, name="Sendungen A-Z"), title="Sendungen A-Z",
		thumb=R(ICON_ZDF_AZ)))
	oc.add(DirectoryObject(key=Callback(Rubriken, name="Rubriken"), title="Rubriken", 
		thumb=R(ICON_ZDF_RUBRIKEN))) 
	oc.add(DirectoryObject(key=Callback(MeistGesehen, name="Meist gesehen"), title="Meist gesehen (1 Woche)", 
		thumb=R(ICON_ZDF_MEIST))) 
	oc.add(DirectoryObject(key=Callback(BarriereArm, name="Barrierearm"), title="Barrierearm", 
		thumb=R(ICON_ZDF_BARRIEREARM))) 
		
	oc.add(DirectoryObject(key=Callback(ZDF_Search, s_type='Bilderserien', title="Bilderserien", query="Bilderserien"), 
		title="Bilderserien", thumb=R(ICON_ZDF_BILDERSERIEN))) 
	return oc	
	
#----------------------------------------------------------------
def home(cont, ID):												# Home-Button, Aufruf: oc = home(cont=oc)	
	title = 'Zurück zum Hauptmenü ' + ID
	title = title.decode(encoding="utf-8", errors="ignore")
	summary = title
	
	if ID == NAME:
		cont.add(DirectoryObject(key=Callback(Main),title=title, summary=summary, tagline=NAME, thumb=R('home.png')))
	if ID == 'ARD':
		name = "ARD Mediathek"
		cont.add(DirectoryObject(key=Callback(Main_ARD, name=name),title=title, summary=summary, tagline=name, 
			thumb=R('home.png')))
	if ID == 'ZDF':
		name = "ZDF Mediathek"
		cont.add(DirectoryObject(key=Callback(Main_ZDF,name=name),title=title, summary=summary, tagline=name, 
			thumb=R('home.png')))

	return cont
	
####################################################################################################
@route(PREFIX + '/Main_Options')
# DumbTools (https://github.com/coder-alpha/DumbTools-for-Plex) getestet, aber nicht verwendet - wiederholte 
#	Aussetzer bei Aufrufen nach längeren Pausen (mit + ohne secure-Funktion)
#	Framework: code/preferences.py

def Main_Options(title):
	Log('Funktion Main_Options')	
	Log(Prefs['pref_use_epg']); Log(Prefs['pref_tvlive_allbandwith']);
	
	# hier zeigt Plex die Einstellungen (Entwicklervorgabe in DefaultPrefs.json):
	# 	http://127.0.0.1:32400/:/plugins/com.plexapp.plugins.ardmediathek2016/prefs
	#	geänderte Daten legt Plex persistent ab (nicht in DefaultPrefs.json) - Löschen nur 
	#	möglich mit Löschen des Caches (Entfernen ../Caches/com.plexapp.plugins.ardmediathek2016)
	myplugin = Plugin.Identifier
	data = HTTP.Request("%s/:/plugins/%s/prefs" % (myhost, myplugin), # als Text, nicht als HTML-Element
						immediate=True).content 
	
	# Zeilenaufbau
	#	1. Zeile "<?xml version='1.0' encoding='utf-8'?>"
	#	2. Zeile (..identifier="com.plexapp.plugins.ardmediathek2016"..) 
	#   ab 3.Zeile Daten
	# Log(data)
	myprefs = data.splitlines() 
	Log(myprefs)
	myprefs = myprefs[2:-1]		# letzte Zeile + Zeilen 1-2 entfernen 
		
	oc = ObjectContainer(no_cache=True, view_group="InfoList", title1='Einstellungen')
	oc = home(cont=oc, ID=NAME)				# Home-Button - in den Untermenüs Rücksprung hierher zu Einstellungen 
	for i in range (len(myprefs)):
		do = DirectoryObject()
		element = myprefs[i]		# Muster: <Setting secure="false" default="true" value="true" label=...
		Log(element)
		secure = stringextract('secure=\"', '\"', element)		# nicht verwendet
		default = stringextract('default=\"', '\"', element)	# Vorgabe
		id = stringextract('id=\"', '\"', element)
		value = stringextract('value=\"', '\"', element)		# akt. Wert (hier nach dem Setzen nicht mehr aktuell)
		pref_value = Prefs[id]									# akt. Wert via Prefs - OK
		label = stringextract('label=\"', '\"', element)
		values = stringextract('values=\"', '\"', element)
		mytype = stringextract('type=\"', '\"', element)
		Log(secure);Log(default);Log(label);Log(values);Log(mytype); Log(id);
		Log(pref_value);
		if mytype == 'bool':										# lesbare Anzeige (statt bool, true, false)
			#oc_type = '| JA / NEIN | aktuell: '
			if str(pref_value).lower() == 'true':
				oc_wert = 'JA'
				oc_type = '| für NEIN  klicken | aktuell: '
			else:
				oc_wert = 'NEIN'
				oc_type = '| für JA  klicken | aktuell: '
		if mytype == 'enum':
			#oc_type = '|  Aufzählung | aktuell: '
			oc_type = '|  für Liste klicken | aktuell: '
			oc_wert = pref_value
		if mytype == 'text':
			oc_type = '| Texteingabe | aktuell: '
			oc_wert = pref_value
		title = u'%s  %s  %s' % (label, oc_type, oc_wert)
		title = title.decode(encoding="utf-8", errors="ignore")
		Log(title); Log(mytype)

		if mytype == 'bool':
			Log('mytype == bool')	
			do.key = Callback(Set, key=id, value=not Prefs[id], oc_wert=not Prefs[id]) 	# Wert direkt setzen (groß/klein egal)		
		if mytype == 'enum':
			do.key = Callback(ListEnum, id=id, label=label, values=values)			# Werte auflisten
		elif mytype == 'text':														# Eingabefeld für neuen Wert (Player-abhängig)
			oc = home(cont=oc, ID=NAME)							# Home-Button	
			oc.add(InputDirectoryObject(key=Callback(SetText, id=id), title=title), title=title)
			continue
			
		do.title = title
		oc.add(do)			
		
	return oc
#------------
@route(PREFIX + '/ListEnum')
def ListEnum(id, label, values):
	Log(ListEnum); Log(id); 
	label = label.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(no_cache=True, view_group="InfoList", title1=label)	
	title = 'zurück zu den Einstellungen'.decode(encoding="utf-8", errors="ignore")		# statt Home-Button	
	oc.add(DirectoryObject(key = Callback(Main_Options, title=title), title = title, 
		summary = title, 
		thumb = R(ICON_PREFS)))
	values = values.split('|') 
	Log(values);
	for i in range(len(values)):
		pref = values[i]
		oc_wert = pref
		Log('value: ' + str(i) + ' Wert: ' + oc_wert)
		oc.add(DirectoryObject(key=Callback(Set, key=id, value=i, oc_wert=oc_wert), title = u'%s' % (pref)))				
	return oc
#------------
@route(PREFIX + '/SetText')
def SetText(query, id):
	return Set(key=id, value=query, oc_wert=oc_wert)
#------------
@route(PREFIX + '/Set')
def Set(key, value, oc_wert):
	Log('Set: key, value ' + key + ', ' + value); 
	#oc_wert = value
	if str(value).lower() == 'true':
		oc_wert = 'JA'
	if str(value).lower() == 'false':
		oc_wert = 'NEIN'

	oc = ObjectContainer(no_cache=True, view_group="InfoList", title1='eingestellt auf: ' + oc_wert)	
	title = 'zurück zu den Einstellungen'.decode(encoding="utf-8", errors="ignore")		# statt Home-Button	
	oc.add(DirectoryObject(key = Callback(Main_Options, title=title), title = title, 
		summary = title, 
		thumb = R(ICON_PREFS)))
	
	# Bsp.: http://127.0.0.1:32400/:/plugins/com.plexapp.plugins.ardmediathek2016/prefs/set?pref_use_epg=True
	HTTP.Request("%s/:/plugins/%s/prefs/set?%s=%s" % (myhost, Plugin.Identifier, key, value), immediate=True)
	#return ObjectContainer()
	return oc
#--------------------------------
def ValidatePrefs():
	Log('ValidatePrefs')
	#Dict.Save()	# n.b. - Plex speichert in Funktion Set, benötigt trotzdem Funktion ValidatePrefs im Plugin
	return
	
####################################################################################################
@route(PREFIX + '/SearchUpdate')
def SearchUpdate(title):		#
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	

	ret = updater.update_available(VERSION)
	int_lv = ret[0]			# Version Github
	int_lc = ret[1]			# Version aktuell
	latest_version = ret[2]	# Version Github, Format 1.4.1
	summ = ret[3]			# Plugin-Name
	tag = ret[4]			# History (last change) )

	url = 'https://github.com/{0}/releases/download/{1}/{2}.bundle.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
	Log(latest_version); Log(int_lv); Log(int_lc); Log(url); 
	
	if int_lv > int_lc:		# zum Testen drehen (akt. Plugin vorher sichern!)
		oc.add(DirectoryObject(
			key = Callback(updater.update, url=url , ver=latest_version), 
			title = 'Update vorhanden - jetzt installieren',
			summary = 'Plugin aktuell: ' + VERSION + ', neu auf Github: ' + latest_version,
			tagline = summ,
			thumb = R(ICON_UPDATER_NEW)))
			
		oc.add(DirectoryObject(
			key = Callback(Main), 
			title = 'Update abbrechen',
			summary = 'weiter im aktuellen Plugin',
			thumb = R(ICON_UPDATER_NEW)))
	else:	
		oc.add(DirectoryObject(
			#key = Callback(updater.menu, title='Update Plugin'), 
			key = Callback(Main), 
			title = 'Plugin ist aktuell', 
			summary = 'Plugin Version ' + VERSION + ' ist aktuell (kein Update vorhanden)',
			tagline = 'weiter zum aktuellen Plugin',
			thumb = R(ICON_OK)))
			
	return oc
	
####################################################################################################
@route(PREFIX + '/SendungenAZ')
def SendungenAZ(name):		# Auflistung 0-9 (1 Eintrag), A-Z (einzeln) 
	Log('SendungenAZ: ' + name)
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	oc = home(cont=oc, ID='ARD')							# Home-Button
	
	azlist = list(string.ascii_uppercase)					# A - Z, 0-9
	azlist.append('0-9')
	
	next_cbKey = 'PageControl'	# SinglePage zeigt die Sendereihen, PageControl dann die weiteren Seiten
	
	path = azPath = BASE_URL + ARD_AZ + 'A'		# A-Seite laden für Prüfung auf inaktive Buchstaben
	Log(path)
	page = HTTP.Request(path).content
	Log(len(page))
	try:										# inaktive Buchstaben?
		inactive_range = stringextract('Aktuelle TV Auswahl:', 'subressort collapsed', page)
		inactive_list = blockextract('class=\"inactive\"', inactive_range)
		Log(inactive_list)		
	except:
		inactive_list = ""

	inactive_char = ""
	if inactive_list:							# inaktive Buchstaben -> 1 String
		for element in inactive_list:
			char = stringextract('<a>', '</a>', element)
			char = char.strip()
			inactive_char =  inactive_char + char
	Log(inactive_char)							# z.B. XYXY
	
	for element in azlist:	
		Log(element)
		azPath = BASE_URL + ARD_AZ + element
		button = element
		title = "Sendungen mit " + button
		if inactive_char.find(button) >= 0:		# inaktiver Buchstabe?
			title = "Sendungen mit " + button + ': keine gefunden'
			oc.add(DirectoryObject(key=Callback(SendungenAZ, name = 'zuletzt: ' + button), 
					title=title, thumb=R(ICON_WARNING)))
		else:
			oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=azPath, next_cbKey=next_cbKey, 
				mode='Sendereihen'), title=title,  thumb=R(ICON_ARD_AZ)))
	return oc
   
####################################################################################################
@route(PREFIX + '/Search')	# Suche - Verarbeitung der Eingabe
	# Hinweis zur Suche in der Mediathek: miserabler unscharfer Algorithmus - findet alles mögliche
def Search(query=None, title=L('Search'), s_type='video', offset=0, **kwargs):
	Log('Search'); Log(query)
	
	name = 'Suchergebnis zu: ' + query
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
			
	path =  BASE_URL +  ARD_Suche + query 
	Log(path) 
	page = HTTP.Request(path).content
	Log(len(page))
	
	err = test_fault(page, path)
	if err:
		return err		
		
	i = page.find('<strong>keine Treffer</strong')
	Log(i)
	if i > 0:
		msg_notfound = 'Leider kein Treffer.'
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		summary = 'zurück zu ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ARD, name=NAME), title=msg_notfound, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ARD)))
		return oc
	else:
		oc = PageControl(title=name, path=path, cbKey=next_cbKey, mode='Suche') 	# wir springen direkt
	 
	return oc
 
#-----------------------
def test_fault(page, path):	# testet ARD-Seite auf ARD-spezif. Error-Test
 	error_txt = '<title>Leider liegt eine Störung vor | ARD Mediathek</title>'
	if page.find(error_txt) >= 0:
		error_txt = 'Leider liegt eine Störung vor | ARD Mediathek | interne Serverprobleme'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header=msgH, message=msg)	
	else:
		return ''
#-----------------------
def get_page(path):		# holt kontrolliert raw-Content
	try:
		page = HTTP.Request(path).content
		err = ''
	except:
		page = ''
		
	if page == '':	
		error_txt = 'Seite nicht erreichbar'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		err = ObjectContainer(header=msgH, message=msg)

	return page, err	

####################################################################################################
@route(PREFIX + '/VerpasstWoche')	# Liste der Wochentage
	# Ablauf (ARD): 	
	#		2. PageControl: Liste der Rubriken des gewählten Tages
	#		3. SinglePage: Sendungen der ausgewählten Rubrik mit Bildern (mehrere Sendungen pro Rubrik möglich)
	#		4. Parseplaylist: Auswertung m3u8-Datei (verschiedene Auflösungen)
	#		5. CreateVideoClipObject: einzelnes Video-Objekt erzeugen mit Bild + Laufzeit + Beschreibung
def VerpasstWoche(name):	# Wochenliste zeigen
	Log('VerpasstWoche: ' + name)
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	oc = home(cont=oc, ID='ARD')						# Home-Button	
		
	wlist = range(0,6)
	now = datetime.datetime.now()

	for nr in wlist:
		iPath = BASE_URL + ARD_VERPASST + str(nr)
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")		# Formate s. man strftime (3)
		zdfDate = rdate.strftime("%Y-%m-%d")		
		iWeekday =  rdate.strftime("%A")
		punkte = '.'
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		iWeekday = transl_wtag(iWeekday)
		Log(iPath); Log(iDate); Log(iWeekday);
		#title = ("%10s ..... %10s"% (iWeekday, iDate))	 # Formatierung in Plex ohne Wirkung
		title =	"%s | %s" % (iDate, iWeekday)
		cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
		if name.find('ARD') == 0 :
			oc.add(DirectoryObject(key=Callback(PageControl, title=title, path=iPath, cbKey='SinglePage', 
				mode='Verpasst'), title=title, thumb=R(ICON_ARD_VERP)))				
		else:
			oc.add(DirectoryObject(key=Callback(ZDF_Verpasst, title=title, zdfDate=zdfDate),	  
				title=title, thumb=R(ICON_ZDF_VERP)))
	return oc
#------------
def transl_wtag(tag):	# Wochentage engl./deutsch wg. Problemen mit locale-Setting 
	wt_engl = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	wt_deutsch = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
	
	wt_ret = tag
	for i in range (len(wt_engl)):
		el = wt_engl[i]
		if el == tag:
			wt_ret = wt_deutsch[i]
			break
	return wt_ret
		
####################################################################################################
@route(PREFIX + '/ARDMore')	# Seiten die nur 1 Beitrag pro Eintrag enhalten
def ARDMore(title, morepath, next_cbKey):	# next_cbKey: Vorgabe für nächsten Callback in SinglePage
	Log('ARDMore'); Log(morepath)
	title2=title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc, ID='ARD')							# Home-Button
					 
	path = Update_ARD_Path(morepath)			# Pfad aktualisieren
	page = HTTP.Request(morepath).content
	err = test_fault(page, morepath)
	if err:
		return err		
							
	pagenr_path =  re.findall("=page.(\d+)", page) # Mehrfachseiten?
	Log(pagenr_path)
	if pagenr_path:
		del pagenr_path[-1]						# letzten Eintrag entfernen (Doppel) - OK
	Log(pagenr_path)	
	
	mode = 'Sendereihen'						# steuert Ausschnittbildung in SinglePage 
	if pagenr_path:	 							# bei Mehrfachseiten Liste Weiter bauen, beginnend mit 1. Seite
		title = 'Weiter zu Seite 1'
		path = morepath + '&' + 'mcontent=page.1'  # 1. Seite, morepath würde auch reichen
		Log(path)
		oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey, mode=mode), 
			title=title, tagline='', summary='', thumb='', art=ICON))			
		
		for page_nr in pagenr_path:
			path = morepath + '&' + 'mcontent=page.' + page_nr
			title = 'Weiter zu Seite ' + page_nr
			Log(path)
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey, 
				mode=mode), title=title, tagline='', summary='', thumb='', art=ICON))			
	else:										# bei nur 1 Seite springen wir direkt, z.Z. bei Rubriken
		oc = SinglePage(path=path, title=title, next_cbKey=next_cbKey, mode='Sendereihen')
		
	return oc

#------------------------	
def Update_ARD_Path(path):		# aktualisiert den Zugriffspfad fallls mötig, z.B. für "Alle Filme"
	try:
		Log('Update_ARD_Path old: ' + path)	
		search_path = stringextract(BASE_URL, '?', path) 	# Base + documentId abschneiden
		#Log(search_path)
		page = HTTP.Request(BASE_URL).content
		pos = page.find(search_path)
		if pos >= 0:	# Pfad (einschl. http://) + Länge documentId (20) + 10 Reserve:
			new_path = page[pos-6:pos + len(search_path) + 30]	
			#Log(new_path)	
			new_path =  stringextract('\"', '\"',  new_path)
			#Log(new_path)	
			new_path = BASE_URL + new_path
			#Log(new_path)	
			if new_path == path:
				Log('Update_ARD_Path new=old: ' + path)	
				return path
			else:
				Log('Update_ARD_Path new: ' + path)	
				return new_path
			
	except:						# bei Zugriffsproblemen mit altem Pfad arbeiten
		Log('Update_ARD_Path: Zugriffsproblem')	
		return path
	
####################################################################################################
@route(PREFIX + '/PageControl')	# kontrolliert auf Folgeseiten. Mehrfache Verwendung.
	# Wir laden beim 1. Zugriff alle Seitenverweise in eine Liste. Bei den Folgezugriffen können die Seiten-
	# verweise entfallen - der Rückschritt zur Liste ist dem Anwender nach jedem Listenelement  möglich.
	# Dagegen wird in der Mediathek geblättert.
def PageControl(cbKey, title, path, mode, offset=0):  # 
	Log('PageControl'); Log('cbKey: ' + cbKey); Log(path)
	title1='Folgeseiten: ' + title.decode(encoding="utf-8", errors="ignore")
	Log('mode: ' + mode)

	oc = ObjectContainer(view_group="InfoList", title1=title1, title2=title1, art = ObjectContainer.art)
	oc = home(cont=oc, ID='ARD')							# Home-Button
	
	page = HTTP.Request(path).content
	path_page1 = path							# Pfad der ersten Seite sichern, sonst gehts mit Seite 2 weiter	

	pagenr_suche = re.findall("mresults=page", page)   
	pagenr_andere = re.findall("mcontents=page", page)  
	pagenr_einslike = re.findall("mcontent=page", page)  	# auch in ARDThemen
	Log(pagenr_suche); Log(pagenr_andere); Log(pagenr_einslike)
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike):
		Log('PageControl: Mehrfach-Seite mit Folgeseiten')
	else:												# keine Folgeseiten -> SinglePage
		Log('PageControl: Einzelseite, keine Folgeseiten'); Log(cbKey); Log(path); Log(title)
		oc = SinglePage(title=title, path=path, next_cbKey='SingleSendung', mode=mode ) # wir springen direkt, 
		return oc																# erspart dem Anwender 1 Klick

	# pagenr_path =  re.findall("&mresults{0,1}=page.(\d+)", page) # lange Form funktioniert nicht
	pagenr_path =  re.findall("=page.(\d+)", page) # 
	Log(pagenr_path)
	if pagenr_path:
		# pagenr_path = repl_dop(pagenr_path) 	# Doppel entfernen (z.B. Zif. 2) - Plex verweigert, warum?
		del pagenr_path[-1]						# letzten Eintrag entfernen - OK
	Log(pagenr_path)
	pagenr_path = pagenr_path[0]	# 1. Seitennummer in der Seite - brauchen wir nicht , wir beginnen bei 1 s.u.
	Log(pagenr_path)		
	
	# ab hier Liste der Folgeseiten. Letzten Eintrag entfernen (Mediathek: Rückverweis auf vorige Seite)
	list = blockextract('class=\"entry\"', page)  # sowohl in A-Z, als auch in Verpasst, 1. Element
	del list[-1]				# letzten Eintrag entfernen - wie in pagenr_path
	Log(len(list))


	first_site = True								# falls 1. Aufruf ohne Seitennr.: im Pfad ergänzen für Liste		
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike) :		# re.findall s.o.  		
		if path_page1.find('mcontents=page') == -1: 
			path_page1 = path_page1 + 'mcontents=page.1'
		if path_page1.find('mresults=page') == -1:
			path_page1 = path_page1 + '&mresults=page.1'
		if path_page1.find('searchText=') >= 0:			#  kommt direkt von Suche
			path_page1 = path + '&source=tv&mresults=page.1'
		if path_page1.find('mcontent=page') >= 0:			#  einslike oder Themen
			path_page1 = path_page1 + 'mcontent=page.1'
	else:
		first_site = False
		
	Log(first_site)
	if  first_site == True:										
		path_page1 = path
		title = 'Weiter zu Seite 1'
		next_cbKey = 'SingleSendung'
			
		Log(first_site); Log(path_page1); Log(next_cbKey)
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=path_page1, next_cbKey=next_cbKey, mode=mode), 
				title=title, thumb=ICON))
	else:	# Folgeseite einer Mehrfachseite - keine Liste mehr notwendig
		Log(first_site)													# wir springen wieder direkt:
		oc = SinglePage(title=title, path=path, next_cbKey='SingleSendung', mode=mode) 
	for element in list:	# [@class='entry'] 
		pagenr_suche = ''; pagenr_andere = ''; title = ''; href = ''
		href = stringextract(' href=\"', '\"', element)
		href = unescape(href)
		if href == '': 
			continue							# Satz verwerfen
			
		# Log(element); 	# Log(s)  # class="entry" - nur bei Bedarf
		pagenr =  re.findall("=page.(\d+)", element) 	# einzelne Nummer aus dem Pfad s ziehen	
		Log(pagenr); 
					
		if (pagenr):							# fehlt manchmal, z.B. bei Suche
			if href.find('=page.') >=0:
				title = 'Weiter zu Seite ' + pagenr[0]
				href = BASE_URL + href
			else:				
				continue						# Satz verwerfen
		else:
			continue							# Satz verwerfen
			
		Log('href: ' + href); Log('title: ' + title)
		next_cbKey = 'SingleSendung'
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=href, next_cbKey=next_cbKey, mode=mode), 
				title=title, thumb=ICON))
	    
	Log(len(oc))
	return oc
  
####################################################################################################
@route(PREFIX + '/SinglePage')	# Liste der Sendungen eines Tages / einer Suche 
								# durchgehend angezeigt (im Original collapsed)
def SinglePage(title, path, next_cbKey, mode, offset=0):	# path komplett
	Log('Funktion SinglePage: ' + path)
	Log('mode: ' + mode); Log('next_cbKey. ' + next_cbKey); 
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc, ID='ARD')					# Home-Button
	
	func_path = path								# für Vergleich sichern
					
	page = HTTP.Request(path).content
	sendungen = ''
	
	if mode == 'Suche':									# relevanten Inhalt ausschneiden, Blöcke bilden
		page = stringextract('data-ctrl-scorefilterloadableLoader-source', 'class=\"socialMedia\"', page)	
		sendungen = blockextract('class=\"teaser\"', page) 
	if mode == 'Verpasst':								
		page = stringextract('"boxCon isCollapsible', 'class=\"socialMedia\"', page)	
		sendungen = blockextract('<h3 class="headline"', page) 
	if mode == 'Sendereihen':							# auch A-Z, 
		page = stringextract('data-ctrl-layoutable', 'class=\"socialMedia\"', page)	
		sendungen = blockextract('class=\"teaser\"', page) 
		
		
	if len(sendungen) == 0:								# Fallback 	
		sendungen = blockextract('class=\"entry\"', page) 
				
	Log(len(sendungen))
	send_arr = get_sendungen(oc, sendungen)	# send_arr enthält pro Satz 8 Listen 
	# Rückgabe send_arr = (send_path, send_headline, send_img_src, send_millsec_duration)
	#Log(send_arr); Log('Länge send_arr: ' + str(len(send_arr)))
	send_path = send_arr[0]; send_headline = send_arr[1]; send_subtitel = send_arr[2];
	send_img_src = send_arr[3]; send_img_alt = send_arr[4]; send_millsec_duration = send_arr[5]
	send_dachzeile = send_arr[6]; send_sid = send_arr[7]
	#Log(send_path); Log(send_arr)
	Log(len(send_path));
	for i in range(len(send_path)):	
		path = send_path[i]
		headline = send_headline[i]
		headline = unescape(headline)				# HTML-Escapezeichen  im Titel	
		subtitel = send_subtitel[i]
		img_src = send_img_src[i]
		img_alt = send_img_alt[i]
		img_alt = unescape(img_alt)
		millsec_duration = send_millsec_duration[i]
		if not millsec_duration:
			millsec_duration = "leer"
		dachzeile = send_dachzeile[i]
		Log(dachzeile)
		sid = send_sid[i]
		summary = ''
		if dachzeile != "":
			summary = dachzeile 
		if  subtitel != "":
			summary = subtitel
			if  dachzeile != "":
				summary = dachzeile + ' | ' + subtitel
		summary = unescape(summary)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		summary = cleanhtml(summary)
		subtitel = subtitel.decode(encoding="utf-8", errors="ignore")
		subtitel = cleanhtml(subtitel)
		Log(subtitel); Log(dachzeile)
		
		Log('neuer Satz'); Log('path: ' + path); Log(title); Log(headline); Log(img_src); Log(millsec_duration);
		Log('next_cbKey: ' + next_cbKey); Log('summary: ' + summary);
		if next_cbKey == 'SingleSendung':		# Callback verweigert den Funktionsnamen als Variable
			Log('path: ' + path); Log('func_path: ' + func_path); Log('subtitel: ' + subtitel); Log(sid)
			if func_path == BASE_URL + path: 	# überspringen - in ThemenARD erscheint der Dachdatensatz nochmal
				Log('BASE_URL + path == func_path | Satz überspringen');
				continue
			if subtitel == '':	# ohne subtitel verm. keine EinzelSendung, sondern Verweis auf Serie o.ä.
				continue
			if subtitel == summary or subtitel == '':
				subtitel = img_alt.decode(encoding="utf-8", errors="ignore")
			
			path = BASE_URL + '/play/media/' + sid			# -> *.mp4 (Quali.-Stufen) + master.m3u8-Datei (Textform)
			oc.add(DirectoryObject(key=Callback(SingleSendung, path=path, title=headline, thumb=img_src, 
				duration=millsec_duration), title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
		if next_cbKey == 'SinglePage':						# mit neuem path nochmal durchlaufen
			path = BASE_URL + path
			Log('path: ' + path);
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=headline, next_cbKey='SingleSendung', 
				mode=mode), title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
		if next_cbKey == 'PageControl':		
			path = BASE_URL + path
			Log('path: ' + path);
			Log('next_cbKey: PageControl in SinglePage')
			oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=headline, cbKey='SingleSendung', 
				mode='Sendereihen'), title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))

	Log(len(oc))	# Anzahl Einträge
						
	return oc
####################################################################################################
@route(PREFIX + '/SingleSendung')	# einzelne Sendung, path in neuer Mediathekführt zur 
# Quellenseite (verschiedene Formate -> 
#	1. Text-Seite mit Verweis auf .m3u8-Datei und / oder href_quality_ Angaben zu mp4-videos -
#		im Listenformat, nicht m3u8-Format, die verlinkte master.m3u8 ist aber im 3u8-Format
#	2. Text-Seite mit rtmp-Streams (Listenformat ähnlich Zif. 1, rtmp-Pfade müssen zusammengesetzt
#		werden
#  
def SingleSendung(path, title, thumb, duration, offset=0):	# -> CreateVideoClipObject
	title = title.decode(encoding="utf-8", errors="ignore")	# ohne: Exception All strings must be XML compatible
	title_org = title	# Backup 

	Log('SingleSendung path: ' + path)					# z.B. http://www.ardmediathek.de/play/media/11177770
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc, ID='ARD')						# Home-Button
	# Log(path)
	page = HTTP.Request(path).content  # als Text, nicht als HTML-Element

	link_path,link_img, m3u8_master = parseLinks_Mp4_Rtmp(page)	# link_img kommt bereits mit thumb,  hier auf Vorrat						
	Log(link_img); Log(m3u8_master); # Log(link_path);  

 	if link_path == []:	      		# keine Videos gefunden		
		Log('link_path == []') 		 
		msgH = 'keine Videoquelle gefunden - Abbruch'; msg = '.keine Videoquelle gefunden - Abbruch. Seite: ' + path;
		return ObjectContainer(header=msgH, message=msg)
  
	# *.m3u8-Datei vorhanden -> auswerten, falls ladefähig. die Alternative 'Client wählt selbst' (master.m3u8)
	# stellen wir voran (WDTV-Live OK, VLC-Player auf Nexus7 'schwerwiegenden Fehler'), MXPlayer läuft dagegen
	if m3u8_master:	  		  								# nicht bei rtmp-Links (ohne master wie m3u8)
		title = 'Bandbreite und Auflösung automatisch'			# master.m3u8
		Codecs = ''
		oc.add(CreateVideoStreamObject(url=m3u8_master, title=title, rtmp_live='nein',
			summary='automatische Auflösung | Auswahl durch den Player', tagline=title, meta=Codecs, thumb=thumb, 
			resolution=''))			
		cont = Parseplaylist(oc, m3u8_master, thumb)	# Liste der zusätzlichen einzelnen Auflösungen 
		#del link_path[0]								# master.m3u8 entfernen, Rest bei m3u8_master: mp4-Links
		Log(cont)  										
	 
	# ab hier Auswertung der restlichen mp4-Links bzw. rtmp-Links (aus parseLinks_Mp4_Rtmp)
	# Format: 0|http://mvideos.daserste.de/videoportal/Film/c_610000/611560/format706220.mp4
	# 	oder: rtmp://vod.daserste.de/ardfs/mp4:videoportal/mediathek/...
	href_quality_S 	= ''; href_quality_M 	= ''; href_quality_L 	= ''; href_quality_XL 	= ''
	for i in range(len(link_path)):
		s = link_path[i]
		#Log(s)
		if s[0:4] == "auto":	# m3u8_master bereits entfernt. Bsp. hier: 	
			# http://tagesschau-lh.akamaihd.net/z/tagesschau_1@119231/manifest.f4m?b=608,1152,1992,3776 
			#	Platzhalter für künftige Sendungen, z.B. Tagesschau (Meldung in Original-Mediathek:
			# 	'dieser Livestream ist noch nicht verfügbar!'
			href_quality_Auto = s[2:]	
			title = 'Qualität AUTO'
			url = href_quality_Auto
			resolution = ''
		if s[0:1] == "0":			
			href_quality_S = s[2:]
			title = 'Qualität SMALL'
			url = href_quality_S
			resolution = 240
		if s[0:1] == "1":			
			href_quality_M = s[2:]
			title = 'Qualität MEDIUM'
			url = href_quality_M
			resolution = 480
		if s[0:1] == "2":			
			href_quality_L = s[2:]
			title = 'Qualität LARGE'
			url = href_quality_L
			resolution = 540
		if s[0:1] == "3":			
			href_quality_XL = s[2:]
			title = 'Qualität EXTRALARGE'
			url = href_quality_XL
			resolution = 720
		
		Log('url ' + title + ': ' + url); 	
		if url:
			if url.find('.m3u8') >= 9:
				del link_path[i]			# 1. master.m3u8 entfernen, oben bereits abgehandelt
				continue
						
			if url.find('rtmp://') >= 0:	# 2. rtmp-Links:	
				summary='Video-Format: RTMP-Stream'	
				oc.add(CreateVideoStreamObject(url=url, title=title, 
					summary=summary, tagline=title, meta=path, thumb=thumb, duration=duration, rtmp_live='nein', 
					resolution=''))					
			else:
				download_url = url			# letzte (höchste Qualität) = Url für Download 
				summary='Video-Format: MP4'	# 3. mp4-Links:	
				oc.add(CreateVideoClipObject(url=url, title=title, 
					summary=summary, meta=path, thumb=thumb, tagline='', duration=duration, resolution=''))
					
	Log(Prefs['pref_use_downloads']) 							# Voreinstellung: False 
	if Prefs['pref_use_downloads'] == True:
		if download_url.find('.m3u8') == -1 and download_url.find('rtmp://') == -1:
			now = datetime.datetime.now()
			mydate = now.strftime("%Y-%m-%d_%H:%M:%S")				
			dfname = 'Download_' + mydate + '.mp4'   			# Bsp.: Download_2016-12-18_09:15:45.mp4
			tagline = 'Hinweis: Download läuft bei Timeout weiter!'
			title = 'Download Video: ' + title_org + ' --> ' + dfname
			dest_path = Core.bundle_path + '/Contents/Downloads/'
			summary = 'Ablage: ' + dest_path
			summary=summary.decode(encoding="utf-8", errors="ignore")
			tagline=tagline.decode(encoding="utf-8", errors="ignore")
			title=title.decode(encoding="utf-8", errors="ignore")
			oc.add(DirectoryObject(key=Callback(Download, url=download_url, title=title, dest_path=dest_path,
				dfname=dfname), title=title, summary=summary, thumb=R(ICON_SAVE), tagline=tagline))

			title = 'Downloadverzeichnis löschen'
			tagline = 'Löschen erfolgt ohne Rückfrage!'
			tagline=tagline.decode(encoding="utf-8", errors="ignore")
			title=title.decode(encoding="utf-8", errors="ignore")			
			summary = 'alle Dateien aus dem Downloadverzeichnis entfernen'
			oc.add(DirectoryObject(key=Callback(DownloadsDelete, url=dest_path),
				title=title, summary=summary, thumb=R(ICON_DELETE), tagline=tagline))
			
	return oc

####################################################################################################
@route(PREFIX + '/Download')	# einzelne Sendung, path in neuer Mediathek führt zur 
# s.a. https://forums.plex.tv/discussion/34771/nameerror-global-name-core-is-not-defined
# Code intern: ../Framework/components/storage.py
# Speicherort ohne Pfadangabe (hier n.b.):
# 	../Plex Media Server/Plug-in Support/Data/com.plexapp.plugins.ardmediathek2016
# Verwendung von curl verworfen (zusätzl. Aufwand, wenig Nutzen)
# 		 		
def Download(url, title, dest_path, dfname):
	Log('Download: ' + title + ' -> ' + dfname)
	Log(url); 

	data, err = get_page(path=url)				# Absicherung gegen Connect-Probleme
	if err:
		return err	

	try:										# läuft nach HTTP-Timeout weiter
		fullpath = os.path.join(dest_path, dfname)
		Log(fullpath)
		Core.storage.save(fullpath, data)
		error_txt = dfname + ' erfolgreich gespeichert'			 			 	 
		msgH = 'Hinweis'; msg = error_txt + ' | ' + fullpath
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header=msgH, message=msg)
	except Exception as exception:
		error_txt = 'Download fehlgeschlagen | ' + str(exception)			 			 	 
		msgH = 'Fehler'; msg = error_txt
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		Log(msg)
		return ObjectContainer(header=msgH, message=msg)

#---------------------------
@route(PREFIX + '/DownloadsDelete')	# 			# Downloadverzeichnis leeren / löschen / neu anlegen
def DownloadsDelete(url):
	Log('DownloadsDelete: ' + url)
	try:
		for i in os.listdir(url):		# Verz. leeren
			fullpath = os.path.join(url, i)
			os.remove(fullpath)
		os.rmdir(url)					# entfernen
		os.makedirs(url)			# neu anlegen
		error_txt = 'Downloadverzeichnis geleert'			 			 	 
		msgH = 'Hinweis'; msg = error_txt + ' | Downloadverzeichnis: ' + url
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header=msgH, message=msg)
	except Exception as exception:
		error_txt = 'Downloadverzeichnis konnte nicht gelöscht werden | ' + str(exception)			 			 	 
		msgH = 'Fehler'; msg = error_txt
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		Log(msg)
		return ObjectContainer(header=msgH, message=msg)

####################################################################################################
def parseLinks_Mp4_Rtmp(page):		# extrahiert aus Textseite .mp4- und rtmp-Links (Aufrufer SingleSendung)
									# akt. Bsp. rtmp: http://www.ardmediathek.de/play/media/35771780
	Log('parseLinks_Mp4_Rtmp')		# akt. Bsp. m3u8: 
	#Log('parseLinks_Mp4_Rtmp: ' + page)		# bei Bedarf
	
	if page.find('http://www.ardmediathek.de/image') >= 0:
		#link_img = teilstring(page, 'http://www.ardmediathek.de/image', '\",\"_subtitleUrl')
		link_img = stringextract('_previewImage\":\"', '\",\"_subtitle', page)
	else:
		link_img = ""

	link_path = []							# Liste nimmt Pfade und Quali.-Markierung auf
	m3u8_master = ''						# nimmt master.m3u8 zusätzlich auf
	
	if page.find('\"_quality\":') >= 0:
		s = page.split('\"_quality\":')	
		# Log(s)							# nur bei Bedarf
		del s[0]							# 1. Teil entfernen - enthält img-Quelle (s.o.)
		
		for i in range(len(s)):
			s1 =  s[i]
			s2 = ''
			Log(s1)
				
			if s1.find('rtmp://') >= 0: # rtmp-Stream 
				Log('s1: ' + s1)
				t1 = stringextract('server\":\"', '\",\"_cdn\"', s1) 
				t2 = stringextract( '\"_stream\":\"', '\"}', s1) 
				s2 = t1 + t2	# beide rtmp-Teile verbinden
				#Log(s2)				# nur bei Bedarf
			
			if s1.find('http://') >= 0: # http: master.m3u8 + mp4
				if s1.find('master.m3u8') >= 0 :
					s2 = teilstring(s1, 'http://','master.m3u8' )
					m3u8_master = s2
					#Log(s2)				# nur bei Bedarf
				elif s1.find('.mp4')  >= 0:
					s2 = teilstring(s1, 'http://','.mp4' )
					#Log(s2)
				elif s1.find('master.m3u8') == -1 and s1.find('.mp4') == -1: # Video-Urls ohne Extension
					#s2 = stringextract('_stream\":\"', '\"}]}]', s1) 
					s2 = stringextract('_stream\":\"', '\"}]', s1) 
					#Log(s2)				# nur bei Bedarf
					
			#Log(s2); Log(len(s2))				# nur bei Bedarf
			
			if len(s2) > 9:						# schon url gefunden? Dann Markierung ermitteln
				if s1.find('auto') >= 0:
					mark = 'auto' + '|'					
				else:
					m = s1[0:1] 				# entweder Ziffern 0,1,2,3 
					mark = m + '|' 	
								
				link = mark + s2				# Qualität voranstellen			
				link_path.append(link)
				Log(mark); Log(s2); Log(link); # Log(link_path)
			
	#Log(link_path)				
	link_path = list(set(link_path))			# Doppel entfernen (gesehen: 0, 1, 2 doppelt)
	link_path.sort()							# Sortierung - Original Bsp.: 0,1,2,0,1,2,3
	Log(link_path); Log(len(link_path))					
		
	return link_path, link_img, m3u8_master				 		
		
####################################################################################################
def get_sendungen(container, sendungen): # Sendungen ausgeschnitten mit class='teaser', aus Verpasst + A-Z,
	# 										Suche, Einslike
	# Headline + Subtitel sind nicht via xpath erreichbar, daher Stringsuche:
	# ohne linklist + Subtitel weiter (teaser Seitenfang od. Verweis auf Serie, bei A-Z teaser-Satz fast identisch,
	#	nur linklist fehlt )
	# Die Rückgabe-Liste send_arr nimmt die Datensätze auf (path, headline usw.)
	
	Log('get_sendungen'); 
	# send_arr nimmt die folgenden Listen auf (je 1 Datensatz pro Sendung)
	send_path = []; send_headline = []; send_subtitel = []; send_img_src = [];
	send_img_alt = []; send_millsec_duration = []; send_dachzeile = []; send_sid = []; 
	arr_ind = 0
	for s in sendungen:	
		# Log(s)				# bei Bedarf
		found_sendung = False
		if s.find('<div class="linklist">') == -1:
			if  s.find('subtitle') >= 0: 
				found_sendung = True
			if  s.find('dachzeile') >= 0: # subtitle in ARDThemen nicht vorhanden
				found_sendung = True
			if  s.find('<h4 class=\"headline\">') >= 0:  # in Rubriken weder subtitle noch dachzeile vorhanden
				found_sendung = True
				
		Log(found_sendung)
		if found_sendung:				
			dachzeile = re.search("<p class=\"dachzeile\">(.*?)</p>\s+?", s)  # Bsp. <p class="dachzeile">Weltspiegel</p>
			if dachzeile:									# fehlt komplett bei ARD_SENDUNG_VERPASST
				dachzeile = dachzeile.group(1)
			else:
				dachzeile = ''
			headline = stringextract('<h4 class=\"headline\">', '</h4>', s)
			if headline == '':
				continue
		
			#if headline.find('- Hörfassung') >= 0:			# nicht unterdrücken - keine reine Hörfassung gesehen 
			#	continue
			if headline.find('Diese Seite benötigt') >= 0:	# Vorspann - irrelevant
				continue
			headline = headline .decode('utf-8')			# tagline-Attribute verlangt Unicode
			hupper = headline.upper()
			if hupper.find(str.upper('Livestream')) >= 0:			# Livestream hier unterdrücken (mehrfach in Rubriken)
				continue
			if s.find('subtitle') >= 0:	# nicht in ARDThemen
				subtitel = re.search("<p class=\"subtitle\">(.*?)</p>\s+?", s)	# Bsp. <p class="subtitle">25 Min.</p>
				subtitel = subtitel.group(1)
				subtitel = subtitel.replace('<br>', ' | ')				
			else:
				subtitel =""
								
			Log(headline)
			send_duration = subtitel						
			send_date = stringextract('class=\"date\">', '</span>', s) # auch Uhrzeit möglich
			Log(subtitel)
			Log(send_date)
			if send_date and subtitel:
				subtitel = send_date + ' Uhr | ' + subtitel				
				
			if send_duration.find('Min.') >= 0:			# Bsp. 20 Min. | UT
				send_duration = send_duration.split('Min.')[0]
				duration = send_duration.split('Min.')[0]
				#Log(duration)
				if duration.find('|') >= 0:			# Bsp. 17.03.2016 | 29 Min. | UT 
						duration = duration.split('|')[1]
				#Log(duration)
				millsec_duration = CalculateDuration(duration)
			else:
				millsec_duration = ''
			
			try:
				extr_path = stringextract('class=\"media mediaA\"', '/noscript', s)
				id_path = stringextract('href=\"', '\"', extr_path)
				# Log(extr_path); Log(id_path)
				sid = ""
				if id_path.find('documentId=') >= 0:		# documentId
					sid = id_path.split('documentId=')[1]
				Log(sid)
				path = id_path	# korrigiert in SinglePage für Einzelsendungen in  '/play/media/' + sid
				# Log(path)							
			except:
				Log('xpath-Fehler in Liste class=teaserbox, sendung: ' + s )	# Satz überspringen
				continue
				
			pos = s.find('urlScheme')						# Bild ermitteln, versteckt im img-Knoten
			if  pos >= 0:									
				text = stringextract('urlScheme', '/noscript', s)
				img_src, img_alt = img_urlScheme(text, 320)
			else:
				img_src=''; img_alt=''				
				
		
			Log('neuer Satz')
			Log(sid); Log(id_path); Log(path); Log(img_src); Log(img_alt); Log(headline);  
			Log(subtitel); Log(send_duration); Log(millsec_duration); Log(dachzeile); 

			send_path.append(path)			# erst die Listen füllen
			send_headline.append(headline)
			send_subtitel.append(subtitel)
			send_img_src.append(img_src)
			send_img_alt.append(img_alt)
			send_millsec_duration.append(millsec_duration)
			send_dachzeile.append(dachzeile)		
			send_sid.append(sid)	
			
											# dann der komplette Listen-Satz ins Array		
	send_arr = [send_path, send_headline, send_subtitel, send_img_src, send_img_alt, send_millsec_duration, 
		send_dachzeile, send_sid]
	# Log(send_arr)					# umfangreich - nur bei Bedarf
	return send_arr
#-------------------
# def img_urlScheme: img-Url ermitteln für get_sendungen, ARDRubriken. text = string, dim = Dimension
def img_urlScheme(text, dim):
	Log('img_urlScheme: ' + text[0:40])
	Log(dim)
	pos = text.find('class=\"mediaCon\">')				# img erst danach
	if pos >= 0:
		text = text[pos:]
		img_src = stringextract("urlScheme':'", '##width', text)
	else:
		img_src = stringextract(':&#039;', '##width', text)
		
	img_alt = stringextract('title=\"', '\"', text)
	if img_alt == '':
		img_alt = stringextract('alt=\"', '\"', text)
	img_alt = img_alt.replace('- Standbild', '')
	img_alt = 'Bild: ' + img_alt
	
		
	if img_src and img_alt:
		img_src = BASE_URL + img_src + str(dim)			# dim getestet: 160,265,320,640
		Log('img_urlScheme: ' + img_src)
		img_alt = img_alt.decode(encoding="utf-8", errors="ignore")	 # kommt vor:  utf8-decode-error bate 0xc3
		Log('img_urlScheme: ' + img_alt[0:40])
		return img_src, img_alt
	else:
		Log('img_urlScheme: leer')
		return '', ''		
	
####################################################################################################
@route(PREFIX + '/CreateVideoClipObject')	# <- SingleSendung Qualitätsstufen
	# Plex-Warnung: Media part has no streams - attempting to synthesize | keine Auswirkung
	# **kwargs erforderlich bei Fehler: CreateVideoClipObject() got an unexpected keyword argument 'checkFiles'
	#	beobachtet bei Firefox (Suse Leap) + Chrome (Windows7)
	#	s.a. https://github.com/sander1/channelpear.bundle/tree/8605fc778a2d46243bb0378b0ab40a205c408da4
def CreateVideoClipObject(url, title, summary, tagline, meta, thumb, duration, resolution, include_container=False, **kwargs):
	#title = title.encode("utf-8")		# ev. für alle ausgelesenen Details erforderlich
	Log('CreateVideoClipObject')
	Log(url); Log(duration); Log(tagline)
	Log(Client.Platform)
	# resolution = ''					# leer - Clients skalieren besser selbst
	resolution=[720, 540, 480]			# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich

 
	videoclip_obj = VideoClipObject(
	key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, tagline=tagline,
		meta=meta, thumb=thumb, duration=duration, resolution=resolution, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		tagline = tagline,
		thumb = thumb,
		items = [
			MediaObject(
				parts = [
					# PartObject(key=url)						# reicht für Webplayer
					PartObject(key=Callback(PlayVideo, url=url)) 
				],
				container = Container.MP4,  	# weitere Video-Details für Chrome nicht erf., aber Firefox 
				video_codec = VideoCodec.H264,	# benötigt VideoCodec + AudioCodec zur Audiowiedergabe
				audio_codec = AudioCodec.AAC,	# 
				
			)  									# for resolution in [720, 540, 480, 240] # (in PlayVideo übergeben), s.o.
	])

	if include_container:						# Abfrage anscheinend verzichtbar, schadet aber auch nicht 
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj
	
#####################################################################################################
@route(PREFIX + '/SenderLiveListePre')	# LiveListe Vorauswahl - verwendet lokale Playlist
def SenderLiveListePre(title, offset=0):	# Vorauswahl: Überregional, Regional, Privat
	Log.Debug('SenderLiveListePre')
	playlist = Resource.Load(PLAYLIST)	# lokale XML-Datei (Pluginverz./Resources)
	#Log(playlist)		# nur bei Bedarf

	oc = ObjectContainer(view_group="InfoList", title1='TV-Livestreams', title2=title, art = ICON)	
	oc = home(cont=oc, ID=NAME)				# Home-Button	
		
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>	
	liste = doc.xpath('//channels/channel')
	Log(liste)
	
	for element in liste:
		element_str = HTML.StringFromElement(element)
		name = stringextract('<name>', '</name>', element_str)
		name = name.decode(encoding="utf-8", errors="ignore")	
		img = stringextract('<thumbnail>', '</thumbnail>', element_str) # channel-thumbnail in playlist
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
		Log(name); Log(img); # Log(element_str);  # nur bei Bedarf	
		oc.add(DirectoryObject(key=Callback(SenderLiveListe, title=name, listname=name),
			title='Live-Sender: ' + name, thumb=img, tagline=''))
			
	return oc
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/SenderLiveListe')	# LiveListe - verwendet lokale Playlist
def SenderLiveListe(title, listname, offset=0):	# 

	# SenderLiveListe -> SenderLiveResolution (reicht nur durch) -> Parseplaylist (Ausw. m3u8)
	#	-> CreateVideoStreamObject 
	Log.Debug('SenderLiveListe')

	title2 = 'Live-Sender ' + title
	title2 = title2.decode(encoding="utf-8", errors="ignore")	
	oc = ObjectContainer(view_group="InfoList", title1='Live-Sender', title2=title2, art = ICON)
	oc = home(cont=oc, ID=NAME)				# Home-Button
			
	playlist = Resource.Load(PLAYLIST)	# muss neu geladen werden, das 'listelement' ist hier sonst nutzlos und die
	#Log(playlist)						# Übergabe als String kann zu groß  werden (max. URL-Länge beim MIE 2083)
	
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>	
	liste = doc.xpath('//channels/channel')
	Log(liste)
	
	for element in liste:
		element_str = HTML.StringFromElement(element)
		name = stringextract('<name>', '</name>', element_str)
		if name == listname:			# Listenauswahl gefunden
			break
	
	liste = element.xpath('./items/item')
	Log(name); Log(liste); # Log(element_str)  # 1 Channel  der Playlist - nur bei Bedarf

	# Besonderheit: die Senderliste wird lokal geladen (s.o.). Über den link wird die URL zur  
	#	*.m3u8 geholt. Nach Anwahl eines Live-Senders erfolgt in SenderLiveResolution die Listung
	#	der Auflösungsstufen.
	#

	for element in liste:							# EPG-Daten für einzelnen Sender holen 	
		#title = element.xpath("./title/text()")	# xpath arbeitet fehlerhaft bei Sonderzeichen (z.B. in URL)
		element_str = HTML.StringFromElement(element)
		#Log(element_str)		# bei Bedarf			
		link = stringextract('<link>', '<thumbnail>', element_str) 	# HTML.StringFromElement unterschlägt </link>
		link = link.strip()							# \r + Leerz. am Ende entfernen
		link = unescape(link)						# amp; entfernen! Herkunft: HTML.ElementFromString bei &-Zeichen
		Log(link);
		
		# Bei link zu lokaler m3u8-Datei (Resources) reagieren SenderLiveResolution und ParsePlayList entsprechend:
		#	der erste Eintrag (automatisch) entfällt, da für die lokale Reource kein HTTP-Request durchge-
		#	führt werden kann. In ParsePlayList werden die enthaltenen Einträge wie üblich aufbereitet
		#	 
									
		title = stringextract('<title>', '</title>', element_str)
		epg_schema=''; epg_url=''
		epg_date=''; epg_title=''; epg_text=''; summary=''; tagline='' 
		Log(Prefs['pref_use_epg']) 					# Voreinstellung: EPG nutzen? - nur mit Schema nutzbar 
		if Prefs['pref_use_epg'] == True:
			epg_schema = stringextract('<epg_schema>', '</epg_schema>', element_str)	# bisher nur ARD, ZDF
			epg_url = stringextract('<epg_url>', '</epg_url>', element_str)				# Link auf Seite mit Info zur Sendung
			epg_url = unescape(epg_url)						# amp; entfernen! Herkunft: HTML.ElementFromString bei &-Zeichen
			Log('--')		# Suchmarke 
			Log(epg_url)
			
			now = datetime.datetime.now()		# akt. Zeit, Parameter für epg_url nach ARD-Schema
			myDate = now.strftime("%d.%m.%Y")	
			
			if epg_schema == 'ARD':						# EPG-Daten ARD holen 
				epg_url = epg_url % myDate
				epg_date, epg_title, epg_text = get_epg_ARD(epg_url, listname)			
					
			if epg_schema == 'ZDF':						# EPG-Daten  ZDF holen	
				epgname = stringextract('<epgname>', '</epgname>', element_str)		
				epg_date, epg_title, epg_text = get_epg_ZDF(epg_url, epgname)	
																		
			if epg_schema == 'DW':					# EPG-Daten  Deutsche Welle holen	
				epgname = stringextract('<epgname>', '</epgname>', element_str)		
				epg_date, epg_title, epg_text = get_epg_DW(epg_url, epgname)	
								
		Log(epg_schema); Log(epg_url); 
		# Log(epg_title); Log(epg_date); Log(epg_text[0:40]);	# bei Bedarf	
		if epg_date and epg_title:
			summary = epg_date + ' | ' + epg_title
		if epg_text:								# kann fehlen
			tagline = epg_text
			
		title = title.decode(encoding="utf-8", errors="ignore")	
		summary = summary.decode(encoding="utf-8", errors="ignore")			
		tagline = tagline.decode(encoding="utf-8", errors="ignore")	
						
		img = stringextract('<thumbnail>', '</thumbnail>', element_str) 
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
			
		Log(link); Log(img); Log(summary); Log(tagline[0:80]);
		Resolution = ""; Codecs = ""; duration = ""
	
		#if link.find('rtmp') == 0:				# rtmp-Streaming s. CreateVideoStreamObject
		# Link zu master.m3u8 erst auf Folgeseite? - SenderLiveResolution reicht an  Parseplaylist durch  
		oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=link, title=title, thumb=img),
			title=title, summary=summary,  tagline=tagline, thumb=img))

	Log(len(oc))
	return oc
#----------------------
def get_epg_ARD(epg_url, listname):					# EPG-Daten ermitteln für SenderLiveListe, ARD
	Log('get_epg_ARD: ' + listname)
	epg_date = ''; epg_title=''; epg_text=''

	# 	Abruf ohne Cachebeschränkung - Seiten enthalten Tagesdaten
	page = HTTP.Request(epg_url, timeout=float(3)).content # ohne xpath, Timeout max. 3 sec
	# Log(page)		# nur bei Bedarf		
	liste = blockextract('class=\"sendungslink\"', page)  
	Log(len(liste));	# bei Bedarf
	if len(liste) == 0: # Sicherung
		return '','','Keine EPG-Daten gefunden'
	
	now = datetime.datetime.now()		# akt. Zeit
	nowtime = now.strftime("%H:%M")		# ARD: <span class="date"> \r 00:15 \r <div class="icons">
	
	for i in range (len(liste)):		# ältere Sendungen enthalten - daher Schleife + Zeitabgleich	
		starttime = stringextract('<span class=\"date\">', '<', liste[i]) # aktuelle Sendezeit
		starttime = mystrip(starttime)
		try:
			endtime = stringextract('<span class=\"date\">', '<', liste[i+1])		# nächste Sendezeit		
			endtime = mystrip(endtime)
		except:
			endtime = '23:59'			# Listenende

		#Log('starttime ' + starttime); Log('endtime ' + endtime); Log('nowtime ' + nowtime);	# bei Bedarf
		epg_date = ''
		if nowtime >= starttime and nowtime < endtime:
			epg_date = stringextract('<span class=\"date\">', '<', liste[i])
			epg_date = mystrip(epg_date) + ' - ' + endtime
			
			epg_title = stringextract('<span class=\"titel\">', '<',  liste[i])
			epg_title = mystrip(epg_title)
			epg_title = unescape(epg_title)			
					
			epg_text = stringextract('<span class=\"subtitel\">', '<',  liste[i])
			epg_text = mystrip(epg_text)
			epg_text = unescape(epg_text)
			
			# weitere Details via eventid z.Z. nicht verfügbar - beim Abruf klemmt Plex ohne Fehlermeldung:
			#eventid = stringextract('data-eventid=\"', '\"', liste[i])	# Bsp. 	2872518888223822
			#details_url = "http://programm.ard.de/?sendung=" + eventid
			#page = HTTP.Request(details_url, cacheTime=1, timeout=float(10)).content # ohne xpath, Cache max. 1 sec
			#epg_details = stringextract('name=\"description\" content="', '\" />', page)
			#epg_text = unescape(epg_text[0:80])
			
			break
	
	if epg_date == '':					# Sicherung
		return '','','Problem mit EPG-Daten'	
			
	epg_text = epg_text.decode(encoding="utf-8", errors="ignore") # möglich: UnicodeDecodeError: 'utf8' codec can't decode byte 0xc3 ...
	Log(epg_date); Log(epg_title); Log(epg_text[0:80]); 	
	return epg_date, epg_title, epg_text
#----------------------
def get_epg_ZDF(epg_url, epgname):					# EPG-Daten ermitteln für SenderLiveListe, ZDF
	Log('get_epg_ZDF: ' + epgname)					#	neu nach ZDF-Relaunch 28.10.2016
	#Log(epgname)

	page = HTTP.Request(epg_url).content 	# ohne Cachebeschränkung - Seiten enthalten Tagesdaten
	epgZDF =  blockextract('class="b-epg-timeline timeline-', page)	# Datensätze für ZDF, ZDFinfo, ZDFneo
	# Log(epgZDF); 				# bei Bedarf
	for epg_rec in epgZDF:
		mark = 'timeline-' + epgname
		if epg_rec.find(mark) >= 0:		# Name hinter timeline-, Bsp.: timeline-ZDFneo
			break
	# Log(epg_rec)		# bei Bedarf
	rec_liste = blockextract('class=\"overlay-link-title\"', epg_rec)	# Datensätze für epgname
	# Log(rec_liste)	# bei Bedarf
	
	now = datetime.datetime.now()
	nowtime = now.strftime("%H:%M")		  	# ZDF-Format, Bsp.: 05:50
	epg_date = ''; epg_title = ''; epg_text = '';
	
	for rec in rec_liste:				# schön: Zeitangabe enthält Anfang + Ende, Bsp.: 05:50 - 06:35
		# Log(rec)	# bei Bedarf
		sendtime = 	stringextract('class=\"time\">', '</span>', rec)	
		starttime = sendtime[0:4]
		endtime = sendtime[8:]					
		# Log('starttime ' + starttime); Log('endtime ' + endtime); Log('nowtime ' + nowtime);	# bei Bedarf
		
		if nowtime >= starttime and nowtime < endtime:
			#  	Beschreib.: h3, (h5), (p, p). h3= titel, h5= Untertitel, p=Herkunft/Jahr 
			epg_date = sendtime	
			epg_cat = 	stringextract('link-category\">', '<span', rec)		
			epg_title = stringextract('</span></span>', '</a>', rec)
			epg_title = mystrip(epg_title)		# mit Zeilenumbruch	
			# etext = stringextract('</span></span>', '</h5>', rec)  # weitere Infos fehlen, ev. in plusbar?
			if epg_cat:
				epg_title = epg_cat + ' | ' + epg_title				# Kat. + Titel zusammenfassen
			Log(epg_date); Log(epg_title); # Log(etext); 
			epg_title = unescape(epg_title); 	epg_text = unescape(epg_text)			
			break												# fertig mit 'Jetzt'
						
	epg_text = epg_text.decode(encoding="utf-8", errors="ignore")	
	Log(epg_date); Log(epg_title); Log(epg_text[0:40]);  
	return epg_date, epg_title, epg_text
#----------------------
#	Aktuell : http://www.dw.com/de/media-center/live-tv/s-100817 - mitnunter morgens leer
def get_epg_DW(epg_url, epgname):					# EPG-Daten ermitteln für SenderLiveListe, Deutsche Welle
	Log('get_epg_DW: ' + epgname)	
	#page = HTML.ElementFromURL(epg_url, cacheTime=1)
	page = HTTP.Request(epg_url, timeout=float(1)).content #  nur Stringsuche
	
	# xpath n.m., da <td class="time"> auch ohne Zeitangabe vorh., Zeitangaben + Sprachen überschneiden sich
	# liste =  re.findall("td class=\"time\">(.*?)</td>\s+?", page)	# falsche Ergebnisse wg. o.g. Überschneidung 
	
	page = stringextract('<table data-channel-id=\"5\"', '</table>', page)	# Filterung deutscher Inhalte
	# Log(page)			# bei Bedarf
	liste = blockextract('<tr class=\"langDE', page)  	# einschl. <tr class="langDE highlight">			
	Log(len(liste));	# bei Bedarf
	if len(liste) == 0: # Sicherung
		return '','','Problem mit EPG-Daten'
	
	now = datetime.datetime.now()		# akt. Zeit
	nowtime = now.strftime("%H:%M")		# DW: <td class="time">00:15</td>
	
	for i in range (len(liste)):
		# starttime =stringextract('class=\"time\">', '</td>', liste[i]) # aktuelle Sendezeit UTC-Zeit (minus 2 Std)
		starttime =stringextract('data-time=\"', '\"></td>', liste[i]) # aktuelle Sendezeit
		starttime = starttime[0:10]			# 13-stel, auf 10 Stellen kürzen für Operationen mittels datetime.fromtimestamp
		starttime = datetime.datetime.fromtimestamp(int(starttime))
		starttime =  starttime.strftime("%H:%M")	
		try:
			endtime = stringextract('data-time=\"', '\"></td>', liste[i+1])		# nächste Sendezeit		
			endtime = endtime[0:10]			# 13-stel, auf 10 Stellen kürzen für Operationen mittels datetime.fromtimestamp
			endtime = datetime.datetime.fromtimestamp(int(endtime))
			endtime =  endtime.strftime("%H:%M")	
		except:
			endtime = '23:59'			# Listenende

		#Log('starttime ' + starttime); Log('endtime ' + endtime); Log('nowtime ' + nowtime);	# bei Bedarf
		epg_date = ''
		if nowtime >= starttime and nowtime < endtime:
			epg_date = starttime
			epg_title = stringextract('<h2>', '</h2>', liste[i])
			epg_text = stringextract('nofollow\">', '</a', liste[i])
			label = stringextract('label\">', '</span', liste[i])		# Sprachlabel
			epg_text = label + ' | ' + epg_text
			epg_text = unescape(epg_text)				# HTML-Escapezeichen  im Teasertext	
			Log(liste[i][0:40])
			break
	if epg_date == '':					# Sicherung
		return '','','Problem mit EPG-Daten'
		
 	Log(epg_date); Log(epg_title); Log(epg_text[0:80]);  
	return epg_date, epg_title, epg_text
		
###################################################################################################
@route(PREFIX + '/SenderLiveResolution')	# Auswahl der Auflösungstufen des Livesenders
	#	Die URL der gewählten Auflösung führt zu weiterer m3u8-Datei (*.m3u8), die Links zu den 
	#	Videosegmenten (.ts-Files enthält). Diese  verarbeitet der Plexserver im Videoobject. 
def SenderLiveResolution(path, title, thumb, include_container=False):
	#page = HTML.ElementFromURL(path)
	url_m3u8 = path
	Log(title); Log(url_m3u8);

	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=title + ' Live', art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button
	
	Codecs = 'H.264'	# dummy-Vorgabe für PHT (darf nicht leer sein)										
	if title.find('Arte') >= 0:
		Log('Arte-Stream gefunden')			
		oc = Arteplaylist(oc, url_m3u8, title, thumb)	# Auswertung Arte-Parameter rtmp- + hls-streaming
		Log(len(oc))
		return oc
		
	if url_m3u8.find('rtmp') == 0:		# rtmp, summary darf für PHT nicht leer sein
		oc.add(CreateVideoStreamObject(url=url_m3u8, title=title, 
			summary='rtmp-Stream', tagline=title, meta=Codecs, thumb=thumb, rtmp_live='ja', resolution=''))
		return oc
		
	# alle übrigen (i.d.R. http-Links)
	if url_m3u8.find('.m3u8') >= 0:					# häufigstes Format
		Log(url_m3u8)
		if url_m3u8.find('http') == 0:		# URL (auch https) oder lokale Datei? (lokal entfällt Eintrag "autom.")			
			oc.add(CreateVideoStreamObject(url=url_m3u8, title=title + ' | Bandbreite und Auflösung automatisch', 
				summary='automatische Auflösung | Auswahl durch den Player', tagline=title,
				meta=Codecs, thumb=thumb, rtmp_live='nein', resolution=''))
			if Prefs['pref_tvlive_allbandwith'] == False:	# nur 1. Eintrag zeigen
				Log(Prefs['pref_tvlive_allbandwith'])		# Plex-Forum plex-plugin-ardmediathek2016/p5
				return oc
		# hier weiter mit Auswertung der m3u8-Datei (lokal oder extern, Berücksichtigung pref_tvlive_allbandwith)
		oc = Parseplaylist(oc, url_m3u8, thumb)	# Auswertung *.m3u8-Datei, Auffüllung Container mit Auflösungen
		return oc							# (-> CreateVideoStreamObject pro Auflösungstufe)
	else:	# keine oder unbekannte Extension - Format unbekannt
		return ObjectContainer(header='SenderLiveResolution: ', message='unbekanntes Format in ' + url_m3u8)
				
####################################################################################################
@route(PREFIX + '/Arteplaylist')	# Auswertung Arte-Parameter rtmp- + hls-streaming
	# Die unter  https://api.arte.tv/api/player/v1/livestream/de?autostart=1 ausgelieferte Textdatei
	# 	enthält je 2 rtmp-Url und 2 hls-Url
	# 27.09.2016: Format + Sender URL's geändert - json, 2 x .f4m, 2 x .m3u8 (jeweils deutsch/französisch)
	#	wir verwenden nur die beiden .m3u8-Versionen. 
	#	Sender artelive-lh.akamaihd.net statt delive.artestras.cshls.lldns.net
def Arteplaylist(oc, url, title, thumb):
	Log('Arteplaylist')
	playlist = HTTP.Request(url).content  # als Text, nicht als HTML-Element

	HLS_SQ_1 = stringextract('\"HLS_SQ_1\": {', '}', playlist)	# .m3u8 deutsch
	HLS_SQ_2 = stringextract('\"HLS_SQ_2\": {', '}', playlist)  # .m3u8 französisch
	# Log(HLS_SQ_1); Log(HLS_SQ_2);  # bei Bedarf
	
	r1 = stringextract('\"url\": \"', '\",',  HLS_SQ_1)  # hls-Url 
	r2 = stringextract('\"url\": \"', '\",',  HLS_SQ_2)  # 
	hls1_url = repl_char('\\', r1)	# Quotierung für Slashes entfernen
	hls2_url = repl_char('\\', r2)	
	Log(hls1_url);Log(hls2_url);
		
	title1=title;title2=title;
	notfound = 	'Problem: URL nicht gefunden! '
	if hls1_url == '':		# Sicherung bzw. Info im Titel bei leeren Links
		title1 = notfound + title1
	if hls2_url == '':		
		title2 = notfound + title2
	
	oc.add(CreateVideoStreamObject(url=hls1_url, title=title1 + ' (de) | http', 
		summary='HLS-Streaming deutsch', tagline=title, meta='', thumb=thumb, rtmp_live='nein', resolution=''))
	oc.add(CreateVideoStreamObject(url=hls2_url, title=title2 + ' (fr) | http', 
		summary='HLS-Streaming französisch', tagline=title, meta='', thumb=thumb, rtmp_live='nein', resolution=''))
	
	Log(len(oc))
	return oc

####################################################################################################
@route(PREFIX + '/CreateVideoStreamObject')	# <- LiveListe, SingleSendung (nur m3u8-Dateien)
											# **kwargs - s. CreateVideoClipObject
def CreateVideoStreamObject(url, title, summary, tagline, meta, thumb, rtmp_live, resolution, include_container=False, **kwargs):
  # Zum Problem HTTP Live Streaming (HLS): Redirecting des Video-Callbacks in einen HTTPLiveStreamURL
  # s.https://forums.plex.tv/index.php/topic/40532-bug-http-live-streaming-doesnt-work-when-redirected/
  # s.a. https://forums.plex.tv/discussion/88056/httplivestreamurl
  # HTTPLiveStreamURL takes the url for an m3u8 playlist as the key argument
  # Ablauf: videoclip_obj -> MediaObject -> PlayVideo
  # HTTPLiveStreamURL: für m3u8-Links, Metadaten (container, codec,..) werden nicht gesetzt
  # ab 03.04.2016: ohne Redirect - die vorh. Infos reichen bei der Mediathek, auch bei den Live-Sendern
  #		Redirect wurde von manchen Playern kommentarlos verweigert bzw. führte zum Crash (Logfiles Otto Kerner)  
  
  # Einstellung im Plex-Web-Client: Direkte Wiedergabe, Direct Stream (Experimenteller Player auf Wunsch)
  #		andernfalls Fehler: HTTP Error 503: Service Unavailable
  #		Aber: keine Auswirkung auf andere Player im Netz
  
  #	resolution = [720, 540, 480] # Parameter bei HTTPLivestream nicht akzeptiert +  auch nicht nötig
  #				bisherige Erfahrung: Clients skalieren besser selbst. Anders bei rtmp!
  # rtmp_live: Steuerung via False/True nicht möglich. Bei zweiten Durchlauf gehen Bool-Parameter verloren
  #				DAF (auch anderes Streams?) benötigt mindestens 1 resolution-Parameter - sonst Fehler.
  #				resolution ohne Auswirkung auf Player-Einstellungen
  #				Die CRITICAL Meldung CreateVideoStreamObject() takes at least 7 arguments (7 given) führt
  #				nicht zum Abbruch des Streams.
  
	url = url.replace('%40', '@')	# Url kann Zeichen @ enthalten
	Log('CreateVideoStreamObject: '); Log(url); Log(rtmp_live) 
	Log('include_container: '); Log(include_container)
	Log(Client.Platform)

	if url.find('rtmp:') >= 0:	# rtmp = Protokoll für flash, Quellen: rtmpdump, shark, Chrome/Entw.-Tools
		if rtmp_live == 'ja':
			Log('rtmp_live: '); Log(rtmp_live) 
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url,live=True))]) # live=True nur Streaming
			rating_key = title
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, tagline=tagline,
				meta=meta, thumb=thumb, rtmp_live='ja', resolution=[720, 540, 480], include_container=True), 
				rating_key=title,
				title=title,
				summary=summary,
				tagline=tagline,
				thumb=thumb,)  
		else:
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url))])
			rating_key = title
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,  tagline=tagline,
				meta=meta, thumb=thumb, rtmp_live='nein', resolution='', include_container=True), 
				rating_key=title,
				title=title,
				summary=summary,
				tagline=tagline,
				thumb=thumb,) 			 

	else:
		# Auslösungsstufen weglassen? (bei relativen Pfaden nutzlos) 
		# Auflösungsstufen - s. SenderLiveResolution -> Parseplaylist
		resolution=[720, 540, 480]		# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich
		meta=url						# leer (None) im Webplayer OK, mit PHT:  Server: Had trouble breaking meta
		mo = MediaObject(parts=[PartObject(key=HTTPLiveStreamURL(url=url))]) 
		rating_key = title
		videoclip_obj = VideoClipObject(					# Parameter wie MovieObject
			key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,  tagline=tagline,
			meta=meta, thumb=thumb, rtmp_live='nein', resolution=resolution, include_container=True), 
			rating_key=title,
			title=title,
			summary=summary,
			tagline=tagline,
			thumb=thumb,)
			
	videoclip_obj.add(mo)

	Log(url); Log(title); Log(summary); Log(tagline);
	Log(meta); Log(thumb); Log(rating_key); 
	
	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

	return oc
#-----------------------------
# PlayVideo: .m3u8 wurde in Route als fehlend bemängelt, wird aber als Attribut der Funktion nicht 
#	akzeptiert - Ursache nicht gefunden. 
#	Routine ab 03.04.2016 entbehrlich - s.o. (ohne Redirect)
# 
@route(PREFIX + '/PlayVideo')  
#def PlayVideo(url, resolution, **kwargs):	# resolution übergeben, falls im  videoclip_obj verwendet
def PlayVideo(url, **kwargs):	# resolution übergeben, falls im  videoclip_obj verwendet
	Log('PlayVideo: ' + url); 		# Log('PlayVideo: ' + resolution)
	HTTP.Request(url).content
	return Redirect(url)

####################################################################################################
@route(PREFIX + '/RadioLiveListe')  
def RadioLiveListe(path, title):
	Log('RadioLiveListe');
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc, ID=NAME)					# Home-Button
	
	#page = HTML.ElementFromURL(path)
	#Log(page)
	playlist = Resource.Load(PLAYLIST_Radio) 
	#Log(playlist)					
	
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>	
	liste = doc.xpath('//item')					# z.Z. nur 1 Channel (ARD). Bei Bedarf Schleife erweitern
	Log(liste)
	
	# Unterschied zur TV-Playlist livesenderTV.xml: Liste  der Radioanstalten mit Links zu den Webseiten.
	#	Die Liste der Sender im Feld <sender> muss exakt den Benennungen in den jew. Webseiten entsprechen.
	#	Nach Auswahl durch den Nutzer werden in RadioAnstalten die einzelnen Sender der Station
	#	ermittelt. Die Icons werden durch Zuordnung Name in Webseite -> Feld <sender> -> Feld <thumblist>
	#		 ermittelt (Index identisch).
	#	Nach Auswahl einer Station wird in RadioLiveSender der Audiostream-Link ermittelt und
	#	in CreateTrackObject endverarbeitet.
	#

	for element in liste:
		s = HTML.StringFromElement(element) 		# Ergebnis wie XMML.StringFromElement
		# Log(s)					# bei Bedarf
		title = stringextract('<title>', '</title>', s)
		title = title.decode(encoding="utf-8", errors="ignore")
		link = stringextract('<link>', '<thumbnail>', s) 	# HTML.StringFromElement unterschlägt </link>
		link = link.strip()							# \r + Leerz. am Ende entfernen
		link = repl_char('amp;',link)				# amp; entfernen! Herkunft: HTML.ElementFromString bei &-Zeichen
		img = stringextract('<thumbnail>', '</thumbnail>', s) 
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
			
		sender = stringextract('<sender>', '</sender>', s)			# Auswertung sender + thumbs in RadioAnstalten
		thumbs = stringextract('<thumblist>', '</thumblist>', s)	
			
		Log(title); Log(link); Log(img); 												
		oc.add(DirectoryObject(key=Callback(RadioAnstalten, path=link, title=title, sender=sender, thumbs=thumbs), 
			title=title, summary='einzelne Sender', tagline='Radio', thumb=img))
	return oc
#-----------------------------
@route(PREFIX + '/RadioAnstalten')  
def RadioAnstalten(path, title,sender,thumbs):
	Log('RadioAnstalten');
	entry_path = path	# sichern
	oc = ObjectContainer(view_group="InfoList",  title1='Radiosender von ' + title, art=ICON)
	Log(Client.Platform)
	client = Client.Platform
	if client == None:
		client = ''
	if client.find ('Plex Home Theater'): 
		oc = home(cont=oc, ID=NAME)							# Home-Button macht bei PHT die Trackliste unbrauchbar 
				
	page, err = get_page(path=path)				# Absicherung gegen Connect-Probleme
	if err:
		return err	
	entries = blockextract('class=\"teaser\"', page)	
	
	del entries[0:2]								# "Javascript-Fehler" überspringen (2 Elemente)
	Log(len(entries))

	for element in entries:
		pos = element.find('class=\"socialMedia\"')			# begrenzen
		if pos >= 0:
			element = element[0:pos]
		# Log(element[0:80])						#  nur bei Bedarf)	
		
		img_src = ""						# img_src = Sender-Icon, thumbs = lokale Icons
		if element.find('urlScheme') >= 0:					# Bildaddresse versteckt im img-Knoten
			img_src = img_urlScheme(element,320)				# ausgelagert - s.u.
			
		headline = ''; subtitel = ''		# nicht immer beide enthalten
		if element.find('headline') >= 0:			# h4 class="headline" enthält den Sendernamen
			headline = stringextract('\"headline\">', '</h4>', element)
			headline = headline .decode('utf-8')		# tagline-Attribute verlangt Unicode
		if element.find('subtitle') >= 0:	
			subtitel = stringextract('\"subtitle\">', '</p>', element)
		Log(headline); Log(subtitel);				
			
		href = stringextract('<a href=\"', '\"', element)
		sid = href.split('documentId=')[1]
		
		path = BASE_URL + '/play/media/' + sid + '?devicetype=pc&features=flash'	# -> Textdatei mit Streamlink
		path_content = HTTP.Request(path).content
		Log(path_content[0:80])			# enthält nochmal Bildquelle + Auflistung Streams (_quality)
										# Streamlinks mit .m3u-Ext. führen zu weiterer Textdatei - Auswert. folgt 
		#slink = stringextract('_stream\":\"', '\"}', path_content) 		# nur 1 Streamlink? nicht mehr aktuell
		link_path,link_img, m3u8_master = parseLinks_Mp4_Rtmp(path_content)	# mehrere Streamlinks auswerten	
		
		if sender and thumbs:				# Zuordnung zu lokalen Icons, Quelle livesenderRadio.xml
			senderlist = sender.split('|')
			thumblist = thumbs.split('|')
			Log(senderlist); Log(thumblist); 	# bei Bedarf
			for i in range (len(senderlist)):
				sname = ''; img = ''
				try:								# try gegen Schreibfehler in  livesenderRadio.xml
					sname =  mystrip(senderlist[i]) # mystrip wg. Zeilenumbrüchen in livesenderRadio.xml
					img = mystrip(thumblist[i])
				except:
					break					# dann bleibt es bei img_src (Fallback)
				if sname == headline:
					if img:
						img_src = img
					Log(img_src); 			# bei Bedarf
					break

		Log(link_path); Log(link_img); Log(img_src);Log(m3u8_master);  		
		for i in range(len(link_path)):
			s = link_path[i]
			Log(s)
			mark = s[0]
			slink = s[2:]
			Log(s); Log(mark); Log(slink); 
			if slink.find('.m3u') > 9:		# der .m3u-Link führt zu weiterer Textdatei, die den Streamlink enthält
				try:						# Request kann fehlschlagen, z.B. bei RBB, SR, SWR
					#slink_content = HTTP.Request(slink).content	# 
					slink_content = HTTP.Request(slink,timeout=float(1)).content	# timeout 0,5 für RBB + SR zu klein
					z = slink_content.split()
					Log(z)
					slink = z[-1]				# Link in letzter Zeile
				except:
					slink = ""
			
			Log(img_src); Log(headline); Log(subtitel); Log(sid); Log(slink);	# Bildquelle: z.Z. verwenden wir nur img_src
			if subtitel == '':		# OpenPHT parsing Error, wenn leer
				subtitel = headline
			headline = headline.decode(encoding="utf-8", errors="ignore")		
			subtitel = subtitel.decode(encoding="utf-8", errors="ignore")	
				
			if slink:						# normaler Link oder Link über .m3u ermittelt
				# msg = ', Stream ' + str(i + 1) + ': OK'		# Log in parseLinks_Mp4_Rtmp ausreichend
				msg = ''
				if img_src.find('http') >= 0:	# Bildquelle Web
					oc.add(CreateTrackObject(url=slink, title=headline + msg, summary=subtitel,
						 thumb=img_src, fmt='mp3'))				# funktioniert hier auch mit aac
				else:							# Bildquelle lokal
					# OpenPHT scheitert, falls hier CreateTrackObject direkt angesteuert wird und sich in der
					#	Liste andere als Trackobjekte befinden (z.B. Homebutton) Webplayer dagegen OK
					oc.add(CreateTrackObject(url=slink, title=headline, summary=subtitel, thumb=R(img_src), fmt='mp3',))							 	
			else:
				msg = ' Stream ' + str(i + 1) + ': nicht verfügbar'	# einzelnen nicht zeigen - verwirrt nur
				#oc.add(DirectoryObject(key=Callback(RadioAnstalten, path=entry_path, title=msg), 
				#	title=headline + msg, summary='', tagline='', thumb=img_src))				
	
	if len(oc) < 1:	      		# keine Radiostreams gefunden		
		Log('oc = 0, keine Radiostreams gefunden') 		 
		msgHg = 'keine Radiostreams bei ' + title + ' gefunden/verfuegbar' 
		msg =  'keine Radiostreams bei ' + title + ' gefunden/verfuegbar, ' + 'Seite: ' + path
		return ObjectContainer(header=msgH, message=msg)	# bricht Auswertung für Anstalt komplett ab							
				
	return oc
	
#-----------------------------
# Umleitung, falls PHT in RadioAnstalten scheitert (1 Klick mehr erforderlich, keine Liste), z.Z. nicht benötigt
@route(PREFIX + '/RadioEinzel')  
def RadioEinzel(url, title, summary, fmt, thumb,):
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc.add(CreateTrackObject(url=url, title=title, summary=summary, fmt='mp3', thumb=thumb))	
	return oc
	
#-----------------------------
@route(PREFIX + '/CreateTrackObject')
# @route('/music/ardmediathek2016/CreateTrackObject')  # funktioniert nicht, dto. in PlayAudio
#	 **kwargs als Parameter für PHT nicht geeignet
def CreateTrackObject(url, title, summary, fmt, thumb, include_container=False):
	Log('CreateTrackObject: ' + url); Log(include_container)

	if fmt == 'mp3':
		container = Container.MP3
		audio_codec = AudioCodec.MP3
	elif fmt == 'aac':
		container = Container.MP4
		audio_codec = AudioCodec.AAC
	elif fmt == 'hls':
		protocol = 'hls'
		container = 'mpegts'
		audio_codec = AudioCodec.AAC	

	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, title=title, summary=summary, fmt=fmt, thumb=thumb, include_container=True),
        # key=Callback(CreateTrackObject, url=url, title=title, fmt=fmt, thumb=thumb, include_container=True),
		rating_key = url,	
		title = title,
		summary = summary,
		thumb=thumb,
		items = [
			MediaObject(
				parts = [
					PartObject(key=Callback(PlayAudio, url=url, ext=fmt)) # runtime- Aufruf PlayAudio.mp3
				],
				container = container,
				audio_codec = audio_codec,
				# bitrate = 128,		# bitrate entbehrlich
				audio_channels = 2		# audio_channels entbehrlich
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object

#-----------------------------
@route(PREFIX + '/PlayAudio') 
def PlayAudio(url):				# runtime- Aufruf PlayAudio.mp3
	Log('PlayAudio: ' + url)	
	return Redirect(url)
		
####################################################################################################
#									ZDF-Funktionen
#
@route(PREFIX + '/ZDF_Search')	# Suche - Verarbeitung der Eingabe. Neu ab 28.10.2016 (nach ZDF-Relaunch)
	# 	Voreinstellungen: alle DF-Sender, ganze Sendungen, sortiert nach Datum
	#	Anzahl Suchergebnisse: 25 - nicht beeinflussbar
def ZDF_Search(query=None, title=L('Search'), s_type=None, pagenr='', **kwargs):
	# query = urllib.quote(query)
	query = query.replace(' ', '+')		# Leer-Trennung bei ZDF-Suche mit +
	Log('ZDF_Search'); Log(query); Log(pagenr); Log(s_type)

	ID='Search'
	ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&from=&to=&sender=alle+Sender&attrs=&contentTypes=episode&sortBy=date&page=%s'
	if s_type == 'Bilderserien':	# 'ganze Sendungen' aus Suchpfad entfernt:
		ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&from=&to=&sender=alle+Sender&attrs=&contentTypes=&sortBy=date&page=%s'
		ID=s_type
	
	path = ZDF_Search_PATH % (query, pagenr) 
	Log(path)	
	# page = HTTP.Request(path, cacheTime=1).content 		# Debug: cacheTime=1 
	page = HTTP.Request(path).content 
	
	# Log(page)	# bei Bedarf		
	searchResult = stringextract('data-loadmore-result-count=\"', '\"', page)
	Log(searchResult);
	
	if pagenr == '':		# erster Aufruf muss '' sein
		pagenr = 1
	NAME = 'ZDF Mediathek'
	name = 'Suchergebnisse zu: %s (Gesamt: %s), Seite %s'  % (urllib.unquote(query), searchResult, pagenr)
	name = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	oc = home(cont=oc, ID='ZDF')							# Home-Button	
			
	oc = ZDF_get_content(oc=oc, page=page, ref_path=path, ID=ID)
	
	# auf mehr prüfen (Folgeseite auf content-link = Ausschlusskriterum prüfen):
	pagenr = int(pagenr) + 1
	path = ZDF_Search_PATH % (query, pagenr)
	Log(pagenr); Log(path)
	page = HTTP.Request(path).content
	pos =  page.find('\"content-link\"')
	if pos >= 0: 
		title = "Weitere Beiträge".decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(ZDF_Search, query=query, s_type=s_type, pagenr=pagenr), 
			title=title, thumb=R(ICON_MEHR), summary=''))	
 
	return oc
	
#-------------------------
@route(PREFIX + '/ZDF_Verpasst')
def ZDF_Verpasst(title, zdfDate):
	Log('ZDF_Verpasst'); Log(title); Log(zdfDate)
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	path = ZDF_SENDUNG_VERPASST % zdfDate
	page = HTTP.Request(path).content 
	Log(path);	# Log(page)	# bei Bedarf

	oc = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='VERPASST')
	
	return oc
	
####################################################################################################
@route(PREFIX + '/ZDFSendungenAZ')
def ZDFSendungenAZ(name):
	Log('ZDFSendungenAZ')
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	azlist = list(string.ascii_uppercase)
	azlist.append('0-9')
	title = "Sendungen A-Z"

	# Menü A to Z
	for element in azlist:
		oc.add(DirectoryObject(key=Callback(SendungenAZList, title=title, element=element), 
			title='Sendungen mit ' + element, thumb=R(ICON_ZDF_AZ)))

	return oc

####################################################################################################
@route(PREFIX + '/SendungenAZList')
def SendungenAZList(title, element):	# Sendungen zm gewählten Buchstaben
	Log('SendungenAZList')
	title2='Sendungen mit ' + element
	oc = ObjectContainer(title2=title2, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	group = element	
	if element == '0-9':
		group = '0+-+9'		# ZDF-Vorgabe
	azPath = ZDF_SENDUNGEN_AZ % group
	page = HTTP.Request(azPath).content 
	Log(azPath);	

	oc = ZDF_get_content(oc=oc, page=page, ref_path=azPath, ID='DEFAULT')
	  
	if len(oc) == 1:	# home berücksichtigen
		return NotFound('Leer - keine Sendung(en), die mit  >' + element + '< starten')

	return oc
	
####################################################################################################
# 	wrapper für Mehrfachseiten aus ZDF_get_content (multi=True). Dort ist kein rekursiver Aufruf
#	möglich (Übergabe Objectcontainer in Callback nicht möglich - kommt als String an)
@route(PREFIX + '/ZDF_Sendungen')	
def ZDF_Sendungen(url, title, ID):
	Log('ZDFSendungen')
	
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')						# Home-Button
	
	try:												# Sicherung, s.a. 
		page = HTTP.Request(url).content 				# https://www.zdf.de/zdfunternehmen/drei-stufen-test-100.html
	except:
		page = ''
	if page == '':
			msg = 'Seite kann nicht geladen werden. URL:\r'
			msg = msg + url
			return ObjectContainer(message=msg)	  # header=... ohne Wirkung	(?)	
					
	oc = ZDF_get_content(oc=oc, page=page, ref_path=url, ID=ID)

	return oc
  
####################################################################################################
@route(PREFIX + '/Rubriken')
def Rubriken(name):
	Log('Rubriken')
	oc = ObjectContainer(title2='ZDF: ' + name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button

	# zuerst holen wir uns die Rubriken von einer der Rubrikseiten:
	path = 'https://www.zdf.de/doku-wissen'
	page = HTTP.Request(path).content 

	listblock =  stringextract('<li class=\"dropdown-block x-left\">', 'link js-track-click icon-104_live-tv', page)
	rubriken =  blockextract('class=\"dropdown-item', listblock)
	
	for rec in rubriken:											# leider keine thumbs enthalten
		path = stringextract('href=\"', '\"', rec)
		path = ZDF_BASE + path
		title = stringextract('class=\"link-text\">', '</span>', rec)
		title = mystrip(title)
		if title == "Sendungen A-Z":	# Rest nicht mehr relevant
			break
		oc.add(DirectoryObject(key=Callback(RubrikSingle, title=title, path=path), 
			title=title, thumb=R(ICON_ARD_RUBRIKEN)))	
	
	return oc
#-------------------------
@route(PREFIX + '/RubrikSingle')
def RubrikSingle(title, path):
	Log('RubrikSingle'); 
	oc = ObjectContainer(title2=title, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	page = HTTP.Request(path).content 			
	oc = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='DEFAULT')	
	
	return oc
	
####################################################################################################
@route(PREFIX + '/MeistGesehen')
def MeistGesehen(name):
	Log('MeistGesehen'); 
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc, ID='ZDF')							# Home-Button
	
	path = ZDF_SENDUNGEN_MEIST
	page = HTTP.Request(path).content 			
	oc = ZDF_get_content(oc=oc, page=page, ref_path=path, ID='DEFAULT')	
	
	return oc
		
####################################################################################################
@route(PREFIX + '/BarriereArm')		# z.Z. nur Hörfassungen, Rest ausgeblendet, da UT in Plex-Channels n.m.
def BarriereArm(name):				# Vorauswahl: 1. Infos, 2. Hörfassungen, 3. Videos mit Untertitel
	Log('BarriereArm')
	oc = ObjectContainer(title2='ZDF: ' + name, view_group="List")
	oc = home(cont=oc, ID='ZDF')								# Home-Button

#	title='Barrierefreie Angebote'							# freischalten, falls UT in Plex verfügbar
#	title=title.decode(encoding="utf-8", errors="ignore")
#	oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID='Infos'), 
#		title=title, summary='Infos zu den barrierefreie Angeboten', thumb=R(ICON_ZDF_INFOS)))	
		
	title='Hörfassungen'
	title=title.decode(encoding="utf-8", errors="ignore")
	summary='verfügbare Videos mit reinen Hörfassugen'
	summary=summary.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID='Voice'), 
		title=title, summary=summary, thumb=R(ICON_ZDF_HOERFASSUNGEN)))	
		
#	title='Untertitel'										# freischalten, falls UT in Plex verfügbar
#	title=title.decode(encoding="utf-8", errors="ignore")
#	# summary='Verfügbare Videos mit Untertitel'
#	summary='in Plex noch nicht verfügbar'
#	summary=summary.decode(encoding="utf-8", errors="ignore")
#	oc.add(DirectoryObject(key=Callback(BarriereArmSingle, title=title, ID='UT'), 
#		title=title, summary=summary, thumb=R(ICON_ZDF_UNTERTITEL)))		
		
	return oc
	
#-------------------------
@route(PREFIX + '/BarriereArmSingle')
def BarriereArmSingle(title, ID):			# Aufruf: 1. Infos, 2. Hörfassungen, 3. Videos mit Untertitel
	Log('BarriereArmSingle')
	
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2='ZDF: ' + title, view_group="List")
	oc = home(cont=oc, ID='ZDF')								# Home-Button

	path = ZDF_BARRIEREARM
	page = HTTP.Request(path).content 
	
	# Dreiteilung: 1. Infos, 2. Hörfassungen, 3. Videos mit Untertitel
	cont1 =  stringextract('title\" >Barrierefreie Angebote', 'itemprop=\"name\">Verfügbare Hörfassungen', page)
	cont2 =  stringextract('\"name\">Verfügbare Hörfassungen', '\"name\">Verfügbare Videos mit Untertitel', page)
	pos = page.find('Verfügbare Videos mit Untertitel</h2>')   # nur 1 x vorh, bis Rest
	cont3 = page[pos:]
	Log(len(cont3))
	
	if ID == 'Infos':
		oc = ZDF_get_content(oc=oc, page=cont1, ref_path=path, ID='DEFAULT')	
	if ID == 'Voice':
		oc = ZDF_get_content(oc=oc, page=cont2, ref_path=path, ID='DEFAULT')	
	if ID == 'UT':
		oc = ZDF_get_content(oc=oc, page=cont3, ref_path=path, ID='DEFAULT')	
	
	return oc
	
####################################################################################################
# @route(PREFIX + '/ZDF_get_content')	# Auswertung aller ZDF-Seiten
#	Die Erkennung von Mehrfachseiten (multi=true) ist leider nicht allen Fällen möglich. Bsp.:
#	Liveticker, Bilderserien usw. werden ohne bes. Kennung hier angezeigt. Bis auf Weiteres werden
#	die Folgeseiten mit Fehlermeldung abgefangen (nach Test auf Videos) 

def ZDF_get_content(oc, page, ref_path, ID=None):	# ID='Search' od. 'VERPASST' - Abweichungen zu Rubriken + A-Z
	Log('ZDF_get_content'); Log(ID); Log(ref_path)
	
	img_alt = teilstring(page, 'class=\"m-desktop', '</picture>') # Bildsätze für b-playerbox
	
	if page.find('class=\"content-box gallery-slider-box') >= 0:  # Bildgalerie (hier aus Folgeseiten)
		title = stringextract('\"big-headline\"  itemprop=\"name\" >', '</h1>', page)
		title = unescape(title)
		Log(title)
		oc = ZDF_Bildgalerie(oc=oc, page=page, mode='is_gallery', title=title)
		return oc
	if page.find('name headline mainEntityOfPage') >= 0:  # spez. Bildgalerie, hier Bares für Rares
		headline = stringextract('name headline mainEntityOfPage\" >', '</h1>', page)
		if headline[0:7] == 'Objekte':		# Bsp.: Objekte vom 6. Dezember 2016
			oc = ZDF_Bildgalerie(oc=oc, page=page, mode='pics_in_accordion-panels', title=headline)
			return oc 
		 	
		
	pos = page.find('class=\"content-box\"')					# ab hier verwertbare Inhalte 
	if pos >= 0:
		page = page[pos:]
				
				
	#if ID == 'Search' or ID == 'VERPASST':						# Unterscheidung ab 22.11.16 nicht mehr nötig
	#	content =  blockextract('class=\"content-link\"', page)																			
	content =  blockextract('class=\"artdirect\"', page)			
	Log(len(page)); Log(len(content));
	
	if len(content) == 0:										# kein Ergebnis oder allg. Fehler
		msg_notfound = 'Leider keine Inhalte' 					# z.B. bei A-Z für best. Buchstaben 
			
		s = 'Es ist leider ein Fehler aufgetreten.'				# ZDF-Meldung Server-Problem
		if page.find('\"title\">' + s) >= 0:
			msg_notfound = s + ' Bitte versuchen Sie es später noch einmal.'
						
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")					
		summary = 'zurück zur ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=NAME), title=title, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		return oc
		
		
	if page.find('class=\"b-playerbox') > 0 and page.find('class=\"item-caption') > 0:  # Video gesamte Sendung?
		first_rec = img_alt +  stringextract('class=\"item-caption', 'data-tracking=', page) # mit img_alt
		content.insert(0, first_rec)		# an den Anfang der Liste
		# Log(content[0]) # bei Bedarf
		
	for rec in content:	
		pos = rec.find('</article>')		# Satz begrenzen - bis nächsten Satz nicht verwertbare Inhalte möglich
		if pos > 0:
			rec = rec[0:pos]
			#Log(rec)  # bei Bedarf
			
		teaser_cat=''; actionDetail=''; genre=''; summary=''; duration='';  title=''; airing=''; 
		tagline=''; thumb =''; vid_content=''; video_datum=''; video_duration=''; other_teaser_label='';
		multi = False			# steuert Mehrfachergebnisse 
		
		meta_image = stringextract('<meta itemprop=\"image\"', '>', rec)
		#Log('meta_image: ' + meta_image)
		# thumb  = stringextract('class=\"m-8-9\"  data-srcset=\"', ' ', rec)    # 1. Bild im Satz m-8-9 (groß)
		thumb_set = stringextract('class=\"m-8-9\"  data-srcset=\"', '/>', rec) 
		thumb_set = thumb_set.split(' ')		
		
		for thumb in thumb_set:				# kleine Ausgabe 240x270 suchen
			if thumb.find('240x270') >= 0:
				break		
		# Log(thumb_set); Log(thumb)

		if thumb == '':											# 1. Fallback thumb	
			thumb  = stringextract('class=\"b-plus-button m-small', '\"', meta_image)
		if thumb == '':											# 2. Fallback thumb (1. Bild aus img_alt)
			thumb = stringextract('data-srcset=\"', ' ', img_alt) 	# img_alt s.o.	
		Log(thumb)
			
		if thumb.find('https://') == -1:	 # Bsp.: "./img/bgs/zdf-typical-fallback-314x314.jpg?cb=0.18.1787"
				thumb = ZDF_BASE + thumb[1:] # 	Fallback-Image  ohne Host
			
		# python-Problem beim stringextract des gesamten plusbar-Blocks. Beschränkung auf einzelne strings			
		path =  stringextract('plusbar-url=\"', '\"', rec)	# plusbar nicht vorh.? - sollte nicht vorkommen
		if path == '' or path == ref_path:					# kein Pfad oder Selbstreferenz
			continue
		plusbar_title = stringextract('plusbar-title=\"', '\"', rec)	# Bereichs-, nicht Einzeltitel, nachrangig
		plusbar_path = stringextract('plusbar-path=\"', '\"', rec)

		# multi- und Teaser-Behandlung:	
		teaser_label = stringextract('class=\"teaser-label\"', '</div>', rec)
		teaser_typ =  stringextract('<strong>', '</strong>', teaser_label)
		if 	teaser_label:
			dt1 =  stringextract('</span>', '<strong>', teaser_label)   
			dt2 =  stringextract('<strong>', '</strong>', teaser_label)
			# Log(teaser_label);Log(teaser_typ);
			Log(dt1); Log(dt2);
			
		if teaser_typ == 'Beiträge':		# Mehrfachergebnisse ohne Datum + Uhrzeit
			multi = True
			summary = dt1 + teaser_typ 		# Anzahl Beiträge
		#Log('teaser_typ: ' + teaser_typ)			
			
		if 	teaser_label.find('class=\"icon-301_clock') >= 0:							# Wochentag + Uhrzeit
			airing = dt1 + ' | ' + dt2 + ' Uhr'
		if 	teaser_label.find('class=\"icon-302_countdown') >= 0:						# Countdown
			other_teaser_label = dt1 + ' ' + dt2			
		#Log(airing); Log(other_teaser_label);
			
		subscription = stringextract('is-subscription=\"', '\"', rec)	# aus plusbar-Block	
		Log(subscription)
		if subscription == 'true':						
			multi = True
			teaser_count = stringextract('</span>', '<strong>', teaser_label)	# bei Beiträgen
			stage_title = stringextract('class=\"stage-title\"', '</h1>', rec)  
			summary = teaser_count + ' ' + teaser_typ 

		# Auswertung Datum + Uhrzeit
		if rec.find('class=\"vid-content\"') >= 0:		# Bsp: <dd class="video-duration m-border">55 min</dd>
			if rec.find('<time datetime=') > 0:	# airing ersetzt airing aus teaser_label 
				airing_string = stringextract('<time datetime=\"', '\"', rec)
				Log(airing_string)
				airing = get_airing(airing_string)		# Bsp. airing_list 2016-11-12T21:45:00.000+01:00
				Log(airing)	
			video_datum = stringextract('video-airing\">', '<', rec)		# Video-Datum, kann fehlen	
			video_duration = stringextract('video-duration', '/dd', rec)	# Video-Länge,  "      "	
			duration = stringextract('>', '<', video_duration)
			if video_datum:
				vid_content = video_datum
			if airing:		# aus teaser_label oder vid-content, so.o.
				vid_content = airing 		# Wochentag + Uhrzeit aus teaser_label
			if duration:
				if vid_content == '':
					vid_content = duration
				else:
					vid_content = vid_content + ' | ' + duration
		Log(airing); Log(video_datum); Log(video_duration); Log(duration);  

		# teaser_cat. div. Bezeichner + Textformate,  Bsp.: <span class="teaser-cat" itemprop="genre">
		teaser_cat = stringextract('class=\"teaser-cat\"', '</span>', rec)
		teaser_cat = teaser_cat.replace('>', "")
		teaser_cat = teaser_cat.replace('itemprop=\"genre\"', "")	
		teaser_cat = teaser_cat.strip()
		if teaser_cat.find('|') > 0:  	# häufig über 3 Zeilen verteilt
			tclist = teaser_cat.split('|')
			teaser_cat = str.strip(tclist[0]) + ' | ' + str.strip(tclist[1])			# zusammenführen
		#Log('teaser_cat: ' + teaser_cat)	
			
		href_title = stringextract('<a href=\"', '>', rec)		# href-link hinter teaser-cat kann Titel enthalten
		href_title = stringextract('title="', '\"', href_title)
		href_title = unescape(href_title)
		#Log(href_title)
		genre = stringextract('itemprop=\"genre\">', '</span>', rec)
		genre = mystrip(genre)
		if genre.find('|') > 0:  	# häufig über 3 Zeilen verteilt
			tclist = genre.split('|')
			genre = str.strip(tclist[0]) + ' | ' + str.strip(tclist[1])			# zusammenführen
			
		description = stringextract('itemprop=\"description\">', '</p>', rec)	# 
		if description == '':
			description = stringextract('class=\"item-description\">', '<', rec) 	# Bsp. Satz b-playerbox
		description = description.strip()	
		description = unescape(description)
		
		# Titel + Beschreibung (einschl. Datum + Zeit) zusammenstellen
		if teaser_cat:
			title = teaser_cat
		if href_title:				
			title = title + ' | ' + href_title		
		if title == '':				
			title = plusbar_title	# nachrangig, z.B. Zeitbereich: Morgens 5:30 - 12:00
		
		if description:
			summary = description

		if multi == True:			
			tagline = 'Folgeseiten'
		else:							# Videos prüfen + Titel kennzeichnen
			if rec.find('title-icon icon-502_play') > 0 or  rec.find('icon-301_clock icon') > 0:
				title = 'Video' + ' | ' + title 
				tagline = plusbar_title
				if vid_content:
					title = title  +  ' | ' + vid_content
					tagline = plusbar_title 
			else:	
				Log('icon-502_play und icon-301_clock nicht gefunden')
				if ID == 'Bilderserien': 	# aber Bilderserien aufnehmen
					Log('Bilderserien')
				if plusbar_title.find(' in Zahlen') > 0:	# Statistik-Seite, voraus. ohne Galeriebilder 
					continue
				if plusbar_title.find('Liveticker') > 0:	#   Liveticker und Ergebnisse
					continue
				if plusbar_path.find('-livestream-') > 0:	#   Verweis Livestreamseite
					continue
					
				multi = True		# weitere Folgeseiten mit unbekanntem Inhalt, ev. auch Videos
				tagline = 'Folgeseiten'
		
		if title[1] == '|':			# Fehlerkorrektur
			title = title[2:]
		title = title.strip()
		title = unescape(title)
		summary = unescape(summary)
		summary = cleanhtml(summary)
		tagline = unescape(tagline)
		tagline = cleanhtml(tagline)
		Log(Client.Platform)									# für PHT: Austausch Titel / Tagline
		if  Client.Platform == 'Plex Home Theater':
			title, tagline = tagline, title
			
		Log('neuer Satz')
		Log(teaser_cat);Log(actionDetail);Log(genre);Log(description);			
		Log(thumb);Log(path);Log(title);Log(summary);Log(tagline);Log(multi);
		title = title.decode(encoding="utf-8", errors="ignore")
		summary = summary.decode(encoding="utf-8", errors="ignore")
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		
		if multi == True:
			oc.add(DirectoryObject(key=Callback(ZDF_Sendungen, url=path, title=title, ID=ID), 
				title=title, thumb=thumb, summary=summary, tagline=tagline))
		else:							
			oc.add(DirectoryObject(key=Callback(GetZDFVideoSources, title=title, url=path, tagline=tagline, thumb=thumb), 
					title=title, thumb=thumb, summary=summary, tagline=tagline))					

	# Bildstrecken am Fuß des Dokuments anhängen (ZDF-Korrespondenten, -Mitarbeiter,...):
	segment_start='<article class=\"b-group-persons\">'; segment_end = 'class="b-footer">'
	if page.find(segment_start) > 0:  
		rec = stringextract(segment_start, segment_end, page)
		path = ref_path													# aktuelle Seite, Auswertung in Bildgalerie
		title = stringextract('class="big-headline">', '</h2>', rec)	# 1. Titel
		title = unescape(title)
		thumb = stringextract('data-src=\"', '\"', rec)					# 1. Bild
		summary = stringextract('class=\"desc-text\">', '</p>', rec)	# 1. Beschr.
		summary = unescape(summary)
		summary = cleanhtml(summary)
		tagline = 'Bilder und Infos'
		title = title.decode(encoding="utf-8", errors="ignore")
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		summary = summary.decode(encoding="utf-8", errors="ignore")
		Log('Bildstrecke Footer');Log(thumb);Log(path);
		oc.add(DirectoryObject(key=Callback(GetZDFVideoSources, title=title, url=path, tagline=tagline, thumb=thumb,
			segment_start=segment_start, segment_end=segment_end),  title=title, thumb=thumb, summary=summary,
			tagline=tagline))	

	return oc
#-------------
def get_airing(airing_string):		# Datum + Uhrzeit, Bsp. airing_string 2016-11-12T21:45:00.000+01:00
	# Log(airing_string)
	airing = ''
	
	airing_date = airing_string.split('T')[0]	# 2016-11-12
	airing_time = airing_string.split('T')[1]
	
	airing_date = airing_date[8:10] + '.' + airing_date[5:7] +  '.' + airing_date[0:4]  # 12.11.2016
	airing_time = airing_time[0:5]  # 21:45
	
	if airing_date and airing_time:
		airing = airing_date + ', ' + airing_time + ' Uhr'
	
	return airing
	
#-------------

####################################################################################################
# Subtitles: im Kopf der videodat-Datei enthalten (Endung .vtt). Leider z.Z. keine Möglichkeit
#	bekannt, diese einzubinden
@route(PREFIX + '/GetZDFVideoSources')			# 4 Requests bis zu den Quellen erforderlich!				
def GetZDFVideoSources(url, title, thumb, tagline, segment_start=None, segment_end=None):	
	Log('GetVideoSources'); Log(url); Log(tagline); 
	title = title.decode(encoding="utf-8", errors="ignore")					
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	urlSource = url 	# für ZDFotherSources

	page = HTTP.Request(url).content 											# 1. player-Konfig. ermitteln
	#headers = HTTP.Request(url).headers	# etag entfällt ab 20.11.2016  
	#headers = str(headers)
	# Log(headers); # Log(page)    # bei Bedarf
	#etag = stringextract('etag\': ', ',', headers)  # Bsp: 'etag': 'W/"07e11176a095329b326b128fd3528f916"',
	#etag = stringextract('\'', '\'', etag)			# Verwendung in header von profile_url
	#Log(etag)
	
	# Start Vorauswertungen: Bildgalerie u.ä. 
	if segment_start and segment_end:						# Vorgabe Ausschnitt durch ZDF_get_content 
		pos1 = page.find(segment_start); pos2 = page.find(segment_end);  # bisher: b-group-persons
		Log(pos1);Log(pos2);
		page = page[pos1:pos2]
		oc = ZDF_Bildgalerie(oc=oc, page=page, mode=segment_start, title=title)
		return oc

	if page.find('data-module=\"zdfplayer\"') == -1:		# Vorprüfung auf Videos
		if page.find('class=\"b-group-contentbox\"') > 0:	# keine Bildgalerie, aber ähnlicher Inhalt
			oc = ZDF_Bildgalerie(oc=oc, page=page, mode='pics_in_accordion-panels', title=title)		
			return oc		
		if page.find('class=\"content-box gallery-slider-box') >= 0:		# Bildgalerie
			oc = ZDF_Bildgalerie(oc=oc, page=page, mode='is_gallery', title=title)
			return oc
			
	# Ende Vorauswertungen: 
			
	oc = home(cont=oc, ID='ZDF')	# Home-Button - nach Bildgalerie (PhotoObject darf keine weiteren Medienobjekte enth.)
	
	zdfplayer = stringextract('data-module=\"zdfplayer\"', 'autoplay', page)			
	player_id =  stringextract('data-zdfplayer-id=\"', '\"', zdfplayer)		
	config_url = stringextract('\"config\": \"', '\"', zdfplayer)	
	profile_url = stringextract('\"content\": \"', '\"', zdfplayer)
	# config_url: /ZDFplayer/configs/zdf/zdf2016/configuration.json	- enth. Sender-ID's u.a., auch apiToken	
	# profile_url Bsp.:  "https://api.zdf.de/content/documents/heute-show-vom-21-10-2016-102.json?profile=player"
	# Log(zdfplayer); Log(player_id); Log(config_url); 
	Log(profile_url)
	if zdfplayer == '':										# Nachprüfung auf Videos
		msgH='kein Video gefunden. Seite:\r' 
		alt_msg = 'Video leider nicht mehr verf&uuml;gbar'
		if page.find(alt_msg) > 0:
			msgH = alt_msg + ' Seite:\r'
		msg = msgH + url
		return ObjectContainer(message=msg)	  # header=... ohne Wirkung	(?)
	
	config_url = ZDF_BASE + config_url 											# 2. apiToken ermitteln - immer identisch?
	page = HTTP.Request(config_url).content 									# 	ev. nicht außerhalb Deutschlands?
	apiToken = stringextract('\"apiToken\": \"', '\"', page)
	Log(apiToken)	
	
	# zu headers s. ZDF_Video_Quellen.txt + ZDF_Video_HAR_gesamt.txt
	#	Abruf mit curl + Header-Option OK (z,Z, reicht apiToken)
	#   headers = {'Api-Auth':"Bearer d2726b6c8c655e42b68b0db26131b15b22bd1a32", 'Host':"api.zdf.de", ... 
	#   Bearer = apiToken aus https://www.zdf.de/ZDFplayer/configs/zdf/zdf2016/configuration.json 
	#	nur Api-Auth + Host erforderlich, Rest entbehrlich
	#headers = {'Api-Auth':"Bearer d2726b6c8c655e42b68b0db26131b15b22bd1a32", 'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	#headers = {'Api-Auth':"Bearer %s" % apiToken, 'If-None-Match':"%s" % etag} 
	#headers = {'Host':"api.zdf.de", 'Api-Auth': "Bearer %s" % apiToken}
	#headers = {'Api-Auth': "Bearer %s" % apiToken}
	headers = {'Api-Auth': "Bearer %s" % apiToken, 'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	# Log(headers)		# bei Bedarf
	
	request = JSON.ObjectFromURL(profile_url, headers=headers)					# 3. Playerdaten ermitteln
	request = json.dumps(request, sort_keys=True, indent=2, separators=(',', ': '))  # sortierte Ausgabe
	# Log(request)
	request = str(request)				# json=dict erlaubt keine Stringsuche, json.dumps klappt hier nicht
	request = request.decode('utf-8', 'ignore')		
	
	pos = request.rfind('mainVideoContent')				# 'mainVideoContent' am Ende suchen
	request_part = request[pos:]
	# Log(request_part)			# bei Bedarf
	old_videodat = stringextract('http://zdf.de/rels/streams/ptmd\": \"', '\",', request_part)	
	# Bsp.: /tmd/2/portal/vod/ptmd/mediathek/161021_hsh_hsh'
	# Log(videodat)	
	old_videodat_url = 'https://api.zdf.de' + old_videodat							# 4. Videodaten ermitteln
	# neu ab 20.1.2016: uurl-Pfad statt ptmd-Pfad ( ptmd-Pfad fehlt bei Teilvideos)
	videodat = stringextract('\"uurl\": \"', '\"', request_part)	# Bsp.: 161118_clip_5_hsh
	videodat_url = 'https://api.zdf.de/tmd/2/portal/vod/ptmd/mediathek/' + videodat
	Log('ptmd: ' + old_videodat_url); Log('uurl: ' + videodat); Log('videodat_url: ' + videodat_url)	
	
	
	# Bsp.: https://api.zdf.de/tmd/2/portal/vod/ptmd/mediathek/161021_hsh_hsh'
	# 	zweite Variante mit {player} = ngplayer_2_3 : identische Datei
	# headers = {'Api-Auth':"Bearer d2726b6c8c655e42b68b0db26131b15b22bd1a32", 'Origin':"https://www.zdf.de", 
	#		'Host':"api.zdf.de", 'Accept-Encoding':"de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4", 
	#		'Accept':"application/vnd.de.zdf.v1.0+json"}
	#
	# Fehler "crossdomain access denied" bei .m3u8-Dateien: Ursache https-Verbindung - konkrete Wechselwirkung n.b.
	#	div. Versuche mit Änderungen der crossdomain.xml in Plex erfolglos,
	#	dto. Eintrag des Servers zdfvodnone-vh.akamaihd.net in der hosts-Datei.
	#	Abhilfe: https -> http, klappt bei allen angebotenen Formaten
	#	
	page = JSON.ObjectFromURL(videodat_url)	 # json=dict erlaubt keine Stringsuche, Sortierung nötig (not in order!)				
	page = 	json.dumps(page, sort_keys=True, indent=2, separators=(',', ': '))
	# Log(page)	
	
	subtitles = stringextract('\"captions\"', '\"documentVersion\"', page)	# Untertitel ermitteln, bisher in Plex-
	subtitles = blockextract('\"class\"', subtitles)						# Channels nicht verwendbar
	#Log(subtitles)
	if len(subtitles) == 2:
		sub_xml = subtitles[0]
		sub_vtt = subtitles[1]
		#Log(sub_xml);Log(sub_vtt);
		sub_xml_path = stringextract('\"uri\": \"', '\"', sub_xml)
		sub_vtt_path = stringextract('\"uri\": \"', '\"', sub_vtt)
		Log('Untertitel xml + vtt:');Log(sub_xml_path);Log(sub_vtt_path);
	
	formitaeten = blockextract('\"formitaeten\":', page)		# Video-URL's ermitteln
	# Log(formitaeten)
	title_call = title
	i = 0 	# Titel-Zähler für mehrere Objekte mit dem selben Titel (manche Clients verwerfen solche)
	for rec in formitaeten:							# Datensätze gesamt
		# Log(rec)		# bei Bedarf
		typ = stringextract('\"type\": \"', '\"', rec)
		facets = stringextract('\"facets\": ', ',', rec)	# Bsp.: "facets": ["progressive"]
		facets = facets.replace('\"', '').replace('\n', '').replace(' ', '')  
		Log('typ: ' + typ); Log('facets: ' + facets)
		if typ == "h264_aac_ts_http_m3u8_http":			# hier nur m3u8-Dateien			
			audio = blockextract('\"audio\":', rec)		# Datensätze je Typ
			# Log(audio)	# bei Bedarf
			for audiorec in audio:		
				url = stringextract('\"uri\": \"',  '\"', audiorec)			# URL
				url = url.replace('https', 'http')		# im Plugin kein Zugang mit https!
				quality = stringextract('\"quality\": \"',  '\"', audiorec)
				Log(url); Log(quality);
				if quality == 'high':					# high bisher identisch mit auto 
					continue
				i = i +1
				if url:
					if url.find('master.m3u8') > 0:		# 
						title=str(i) + '. ' + title_call + ' | ' + quality + ' [m3u8]'
						summary = 'Qualität: ' + quality + ' | Typ: ' + typ + ' [m3u8-Streaming]'	
						summary = summary.decode(encoding="utf-8", errors="ignore")
						oc.add(CreateVideoStreamObject(url=url, title=title, rtmp_live='nein', summary=summary, 
							tagline=tagline, meta= Plugin.Identifier + str(i), thumb=thumb, resolution='unbekannt'))	
	
	# oc = Parseplaylist(oc, videoURL, thumb)	# hier nicht benötigt - das ZDF bietet bereits 3 Auflösungsbereiche
	oc.add(DirectoryObject(key=Callback(ZDFotherSources, url=urlSource, title=title_call, tagline=tagline, thumb=thumb),
		title='weitere Video-Formate', summary='', thumb=R(ICON_MEHR)))

	return oc	
	
#-------------------------
@route(PREFIX + '/ZDFotherSources')		# weitere Videoquellen - Quellen werden erneut geladen
def ZDFotherSources(url, title, tagline, thumb):
	Log('OtherSources:' + url); 

	title = title.decode(encoding="utf-8", errors="ignore")					
	oc = ObjectContainer(title2=title, view_group="InfoList")
	oc = home(cont=oc, ID='ZDF')						# Home-Button

	page = HTTP.Request(url).content 					# player-Konfig. ermitteln		
	# Log(page)    # bei Bedarf
		
	zdfplayer = stringextract('data-module=\"zdfplayer\"', 'autoplay', page)			
	player_id =  stringextract('data-zdfplayer-id=\"', '\"', zdfplayer)		
	config_url = stringextract('\"config\": \"', '\"', zdfplayer)		
	profile_url = stringextract('\"content\": \"', '\"', zdfplayer)	
	#Log(zdfplayer); Log(player_id); Log(config_url); Log(profile_url)
	
	config_url = ZDF_BASE + config_url 											# 2. apiToken ermitteln - immer identisch?
	page = HTTP.Request(config_url).content 									# 	ev. nicht außerhalb Deutschlands?
	apiToken = stringextract('\"apiToken\": \"', '\"', page)
	Log(apiToken)	
	
	headers = {'Api-Auth': "Bearer %s" % apiToken, 'Host':"api.zdf.de", 'Accept-Encoding':"gzip, deflate, sdch, br", 'Accept':"application/vnd.de.zdf.v1.0+json"}
	# Log(headers)		# bei Bedarf

	request = JSON.ObjectFromURL(profile_url, headers=headers)					# 3. Playerdaten ermitteln
	request = json.dumps(request, sort_keys=True, indent=2, separators=(',', ': '))  # sortierte Ausgabe
	# Log(request)
	request = str(request)				# json=dict erlaubt keine Stringsuche, json.dumps klappt hier nicht
	request = request.decode('utf-8', 'ignore')		
		
	pos = request.rfind('mainVideoContent')				# 'mainVideoContent' am Ende suchen
	request_part = request[pos:]
	# Log(request_part)			# bei Bedarf
	old_videodat = stringextract('http://zdf.de/rels/streams/ptmd\": \"', '\",', request_part)	
	# Bsp.: /tmd/2/portal/vod/ptmd/mediathek/161021_hsh_hsh'
	# Log(videodat)	
	old_videodat_url = 'https://api.zdf.de' + old_videodat							# 4. Videodaten ermitteln
	# neu ab 20.1.2016: uurl-Pfad statt ptmd-Pfad ( ptmd-Pfad fehlt bei Teilvideos)
	videodat = stringextract('\"uurl\": \"', '\"', request_part)	# Bsp.: 161118_clip_5_hsh
	videodat_url = 'https://api.zdf.de/tmd/2/portal/vod/ptmd/mediathek/' + videodat
	Log('ptmd: ' + old_videodat_url); Log('uurl: ' + videodat); Log('videodat_url: ' + videodat_url)	
	
	page = JSON.ObjectFromURL(videodat_url)	 # json=dict erlaubt keine Stringsuche, Sortierung nötig (not in order!)				
	page = 	json.dumps(page, sort_keys=True, indent=2, separators=(',', ': '))
	# Log(page)	
	
	formitaeten = blockextract('\"formitaeten\":', page)		# Video-URL's ermitteln
	# Log(formitaeten)
	i = 0 	# Titel-Zähler für mehrere Objekte mit dem selben Titel (manche Clients verwerfen solche)
	for rec in formitaeten:							# Datensätze gesamt
		# Log(rec)		# bei Bedarf
		typ = stringextract('\"type\": \"', '\"', rec)
		facets = stringextract('\"facets\": ', ',', rec)	# Bsp.: "facets": ["progressive"]
		facets = facets.replace('\"', '').replace('\n', '').replace(' ', '') 
		Log(typ); Log(facets)
		if typ == "h264_aac_f4f_http_f4m_http":				# manifest.f4m auslassen
			continue
		if typ == "h264_aac_ts_http_m3u8_http":				# bereits in GetZDFVideoSources ausgewertet
			continue
			
		audio = blockextract('\"audio\":', rec)		# Datensätze je Typ
		# Log(audio)	# bei Bedarf
		for audiorec in audio:		
			url = stringextract('\"uri\": \"',  '\"', audiorec)			# URL
			url = url.replace('https', 'http')
			quality = stringextract('\"quality\": \"',  '\"', audiorec)
			Log(url); Log(quality);
			i = i +1
			if url:			
				summary = 'Qualität: ' + quality + ' | Typ: ' + typ + ' ' + facets 
				summary = summary.decode(encoding="utf-8", errors="ignore")
				oc.add(CreateVideoClipObject(url=url, title=str(i) + '. ' + title + ' | ' + quality,
					summary=summary, meta= Plugin.Identifier + str(i), tagline=tagline, thumb=thumb, 
					duration='duration', resolution='unbekannt'))	
	return oc
#-------------------------
def ZDF_Bildgalerie(oc, page, mode, title):	# keine Bildgalerie, aber ähnlicher Inhalt
	Log('ZDF_Bildgalerie'); Log(mode); Log(title)
	
	if mode == 'is_gallery':							# "echte" Bildgalerie
		content =  stringextract('class=\"content-box gallery-slider-box', 'title=\"Bilderserie schließen\"', page)
		content =  blockextract('class=\"img-container', content)   					# Bild-Datensätze
	if mode == 'pics_in_accordion-panels':				# Bilder in Klappboxen	
		content =  stringextract('class=\"b-group-contentbox\"', '</section>', page)
		content =  blockextract('class=\"accordion-panel\"', content)
	if mode == '<article class="b-group-persons">':		# ZDF-Korrespondenten, -Mitarbeiter,...	
		content = page	
		content =  blockextract('guest-info m-clickarea', content)
			
	Log(len(content))
	# neuer Container mit neuem Titel
	oc = ObjectContainer(title2=title, view_group="InfoList")
	
	image = 1
	for rec in content:
		# Log(rec)  # bei Bedarf
		summ = ''; 
		if mode == 'is_gallery':				# "echte" Bildgalerie
			img_src =  stringextract('data-srcset=\"', ' ', rec)			
			item_title = stringextract('class=\"item-title', 'class=\"item-description\">', rec)  
			teaser_cat =  stringextract('class=\"teaser-cat\">', '</span>', item_title)  
			teaser_cat = teaser_cat.strip()			# teaser_cat hier ohne itemprop
			if teaser_cat.find('|') > 0:  			# über 3 Zeilen verteilt
				tclist = teaser_cat.split('|')
				teaser_cat = str.strip(tclist[0]) + ' | ' + str.strip(tclist[1])			# zusammenführen
			#Log(teaser_cat)					
			descript = stringextract('class=\"item-description\">', '</p', rec)
			pos = descript.find('<span')			# mögliche Begrenzer: '</p', '<span'
			if pos >= 0:
				descript = descript[0:pos]
			descript = descript.strip()
			#Log(descript)					

			title_add = stringextract('data-plusbar-title=\"', ('\"'), rec)	# aus Plusbar - im Teaser schwierig
			title = teaser_cat
			if title_add:
				title = title + ' |' + title_add
			if descript:		
				summ = descript
				
		if mode == 'pics_in_accordion-panels':				# Bilder in Klappboxen
			img_src =  stringextract('data-srcset=\"', ' ', rec)
			title =  stringextract('class=\"shorter\">', '<br/>', rec) 
			summ = stringextract('p class=\"text\">', '</p>', rec) 		
			summ = cleanhtml(summ)
		
		if mode == '<article class=\"b-group-persons\">':
			img_src = stringextract('data-src=\"', '\"', rec)
			
			guest_name =  stringextract('trackView\": true}\'>', '</button>', rec)
			guest_name = guest_name.strip()
			guest_title =  stringextract('guest-title\"><p>', '</p>', rec)
			guest_title = unescape(guest_title)
			title = guest_name + ': ' + guest_title						
			summ = stringextract('desc-text\">', '</p>', rec)
			summ = summ.strip()
			summ = cleanhtml(summ)
			
		if img_src == '':									# Sicherung			
			msgH = 'Error'; msg = 'Problem in Bildgalerie: Bild nicht gefunden'
			Log(msg)
			msg =  msg.decode(encoding="utf-8", errors="ignore")
			return ObjectContainer(header=msgH, message=msg)
					
		title = unescape(title)
		title = title.decode(encoding="utf-8", errors="ignore")
		summ = unescape(summ)
		summ = summ .decode(encoding="utf-8", errors="ignore")
		Log('neu');Log(title);Log(img_src);Log(summ[0:40]);
		oc.add(PhotoObject(
			key=img_src,
			rating_key='%s.%s' % (Plugin.Identifier, 'Bild ' + str(image)),	# rating_key = eindeutige ID
			summary=summ,
			title=title,
			thumb = img_src
			))
		image += 1
	return oc	
	
#-------------------------
####################################################################################################
#									Hilfsfunktionen
def Parseplaylist(container, url_m3u8, thumb):		# master.m3u8 auswerten, Url muss komplett sein
#													# container muss nicht leer ein (siehe SingleSendung)
#  1. Besonderheit: in manchen *.m3u8-Dateien sind die Pfade nicht vollständig,
#	sondern nur als Ergänzung zum Pfadrumpf (ohne Namen + Extension) angegeben, Bsp. (Arte):
#	delive/delive_925.m3u8, url_m3u8 = http://delive.artestras.cshls.lldns.net/artestras/contrib/delive.m3u8
#	Ein Zusammensetzen verbietet sich aber, da auch in der ts-Datei (z.B. delive_64.m3u8) nur relative 
#	Pfade angegeben werden. Beim Redirect des Videoplays zeigt dann der Pfad auf das Plugin und Plex
#	versucht die ts-Stücke in Dauerschleife zu laden.
#	Wir prüfen daher besser auf Pfadbeginne mit http:// und verwerfen Nichtpassendes - auch wenn dabei ein
#	Sender komplett ausfällt.
#	Lösung ab April 2016:  Sonderbehandlung Arte in Arteplaylists
#  2. Besonderheit: fast identische URL's zu einer Auflösung (...av-p.m3u8, ...av-b.m3u8) Unterschied n.b.
#  3. Besonderheit: für manche Sendungen nur 1 Qual.-Stufe verfügbar (Bsp. Abendschau RBB)
#  4. Besonderheit: manche Playlists enthalten zusätzlich abgeschaltete Links, gekennzeichnet mit #. Fehler Webplayer:
#		 crossdomain access denied. Keine Probleme mit OpenPHT und VLC

  Log ('Parseplaylist: ' + url_m3u8)
  playlist = ''
  # seit ZDF-Relaunch 28.10.2016 dort nur noch https
  if url_m3u8.find('http://') == 0 or url_m3u8.find('https://') == 0:		# URL oder lokale Datei?	
	try:
		playlist = HTTP.Request(url_m3u8).content  # als Text, nicht als HTML-Element
	except:
		if playlist == '':
			msg = 'Playlist kann nicht geladen werden. URL:\r'
			msg = msg + url_m3u8
			return ObjectContainer(message=msg)	  # header=... ohne Wirkung	(?)			
  else:													
	playlist = Resource.Load(url_m3u8) 
  # Log(playlist)   # bei Bedarf
	 
  lines = playlist.splitlines()
  #Log(lines)
  lines.pop(0)		# 1. Zeile entfernen (#EXTM3U)
  BandwithOld = ''	# für Zwilling -Test (manchmal 2 URL für 1 Bandbreite + Auflösung) 
  i = 0
  #for line in lines[1::2]:	# Start 1. Element, step 2
  for line in lines:	
 	line = lines[i].strip()
 	# Log(line)				bei Bedarf
	if line.startswith('#EXT-X-STREAM-INF'):# tatsächlich m3u8-Datei?
		url = lines[i + 1].strip()	# URL in nächster Zeile
		Log(url)

		Bandwith = GetAttribute(line, 'BANDWIDTH')
		Resolution = GetAttribute(line, 'RESOLUTION')
		if Resolution:	# fehlt manchmal (bei kleinsten Bandbreiten)
			Resolution = 'Auflösung ' + Resolution
		else:
			Resolution = 'Auflösung unbekannt'	# verm. nur Ton? CODECS="mp4a.40.2"
		Codecs = GetAttribute(line, 'CODECS')
		# als Titel wird die  < angezeigt (Sender ist als thumb erkennbar)
		if int(Bandwith) >  64000: 	# < 64000 vermutl. nur Audio, als Video keine Wiedergabe 
			title='Bandbreite ' + Bandwith
			if url.find('#') >= 0:	# Bsp. SR = Saarl. Rundf.: Kennzeichnung für abgeschalteten Link
				Resolution = 'zur Zeit nicht verfügbar!'
			if Bandwith == BandwithOld:	# Zwilling -Test
				title = 'Bandbreite ' + Bandwith + ' (2. Alternative)'
			if url.startswith('http://') == False:   	# relativer Pfad? 
				pos = url_m3u8.rfind('/')				# m3u8-Dateinamen abschneiden
				url = url_m3u8[0:pos+1] + url 			# Basispfad + relativer Pfad
				
			Log(url); Log(title); Log(thumb); Log('Resolution')
			container.add(CreateVideoStreamObject(url=url, title=title, # Einbettung in DirectoryObject zeigt bei
				summary= Resolution, tagline='', meta=Codecs, thumb=thumb, 			# AllConnect trotzdem nur letzten Eintrag
				rtmp_live='nein', resolution=''))
			BandwithOld = Bandwith
			
		if url_m3u8.find('http://') < 0:		# lokale Datei
			if Prefs['pref_tvlive_allbandwith'] == False:	# nur 1. Eintrag
				return container

				
  	i = i + 1	# Index für URL
  #Log (len(container))	# Anzahl Elemente
  if len(container) == 0:	# Fehler, zurück zum Hauptmenü
  		container.add(DirectoryObject(key=Callback(Main),  title='inkompatible m3u8-Datei', 
			tagline='Kennung #EXT-X-STREAM-INF fehlt oder den Pfaden fehlt http:// ', thumb=thumb)) 
	
  return container

#----------------------------------------------------------------  
def GetAttribute(text, attribute, delimiter1 = '=', delimiter2 = ','):
# Bsp.: #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=61000,CODECS="mp4a.40.2"

    if attribute == 'CODECS':	# Trenner = Komma, nur bei CODEC ist Inhalt 'umrahmt' 
    	delimiter1 = '="'
    	delimiter2 = '"'
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return ''

#----------------------------------------------------------------  
def NotFound(msg):
    return ObjectContainer(
        header=u'%s' % L('Error'),
        message=u'%s' % (msg)
    )

#----------------------------------------------------------------  
def CalculateDuration(timecode):
	milliseconds = 0
	hours        = 0
	minutes      = 0
	seconds      = 0
	d = re.search('([0-9]{1,2}) min', timecode)
	if(None != d):
		minutes = int( d.group(1) )
	else:
		d = re.search('([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}).([0-9]{1,3})', timecode)
		if(None != d):
			hours = int ( d.group(1) )
			minutes = int ( d.group(2) )
			seconds = int ( d.group(3) )
			milliseconds = int ( d.group(4) )
	milliseconds += hours * 60 * 60 * 1000
	milliseconds += minutes * 60 * 1000
	milliseconds += seconds * 1000
	return milliseconds
#----------------------------------------------------------------  
def stringextract(mFirstChar, mSecondChar, mString):  	# extrahiert Zeichenkette zwischen 1. + 2. Zeichenkette
	pos1 = mString.find(mFirstChar)						# return '' bei Fehlschlag
	ind = len(mFirstChar)
	#pos2 = mString.find(mSecondChar, pos1 + ind+1)		
	pos2 = mString.find(mSecondChar, pos1 + ind)		# ind+1 beginnt bei Leerstring um 1 Pos. zu weit
	rString = ''

	if pos1 >= 0 and pos2 >= 0:
		rString = mString[pos1+ind:pos2]	# extrahieren 
		
	#Log(mString); Log(mFirstChar); Log(mSecondChar); 	# bei Bedarf
	#Log(pos1); Log(ind); Log(pos2);  Log(rString); 
	return rString
#----------------------------------------------------------------  
def teilstring(zeile, startmarker, endmarker):  		# rfind: endmarker=letzte Fundstelle, return '' bei Fehlschlag
  # die übergebenen Marker bleiben Bestandteile der Rückgabe (werden nicht abgeschnitten)
  pos2 = zeile.find(endmarker, 0)
  pos1 = zeile.rfind(startmarker, 0, pos2)
  if pos1 & pos2:
    teils = zeile[pos1:pos2+len(endmarker)]	# 
  else:
    teils = ''
  #Log(pos1) Log(pos2) 
  return teils 
#----------------------------------------------------------------  
def blockextract(blockmark, mString):  	# extrahiert Blöcke begrenzt durch blockmark aus mString
	#	blockmark bleibt Bestandteil der Rückgabe
	#	Rückgabe in Liste. Letzter Block reicht bis Ende mString (undefinierte Länge)
	#	Verwendung, wenn xpath nicht funktioniert (Bsp. Tabelle EPG-Daten www.dw.com/de/media-center/live-tv/s-100817)
	rlist = []				
	if 	blockmark == '' or 	mString == '':
		Log('blockextract: blockmark or mString leer')
		return rlist
	
	pos = mString.find(blockmark)
	if 	mString.find(blockmark) == -1:
		Log('blockextract: blockmark nicht in mString enthalten')
		# Log(pos); Log(blockmark);Log(len(mString));Log(len(blockmark));
		return rlist
	pos2 = 1
	while pos2 > 0:
		pos1 = mString.find(blockmark)						
		ind = len(blockmark)
		pos2 = mString.find(blockmark, pos1 + ind)		
	
		block = mString[pos1:pos2]	# extrahieren einschl.  1. blockmark
		rlist.append(block)
		# reststring bilden:
		mString = mString[pos2:]	# Rest von mString, Block entfernt	
	return rlist  
#----------------------------------------------------------------  
def repl_dop(liste):	# Doppler entfernen, im Python-Script OK, Problem in Plex - s. PageControl
	mylist=liste
	myset=set(mylist)
	mylist=list(myset)
	mylist.sort()
	return mylist
#----------------------------------------------------------------  
def transl_umlaute(line):	# Umlaute übersetzen, wenn decode nicht funktioniert
	line_ret = line
	line_ret = line_ret.replace("Ä", "Ae", len(line_ret))
	line_ret = line_ret.replace("ä", "ae", len(line_ret))
	line_ret = line_ret.replace("Ü", "Ue", len(line_ret))
	line_ret = line_ret.replace('ü', 'ue', len(line_ret))
	line_ret = line_ret.replace("Ö", "Oe", len(line_ret))
	line_ret = line_ret.replace("ö", "oe", len(line_ret))
	line_ret = line_ret.replace("ß", "ss", len(line_ret))	
	return line_ret
#----------------------------------------------------------------  
def repl_char(cut_char, line):	# problematische Zeichen in Text entfernen, wenn replace nicht funktioniert
	line_ret = line				# return line bei Fehlschlag
	pos = line_ret.find(cut_char)
	while pos >= 0:
		line_l = line_ret[0:pos]
		line_r = line_ret[pos+len(cut_char):]
		line_ret = line_l + line_r
		pos = line_ret.find(cut_char)
		#Log(cut_char); Log(pos); Log(line_l); Log(line_r); Log(line_ret)	# bei Bedarf	
	return line_ret
#----------------------------------------------------------------  	
def unescape(line):	# HTML-Escapezeichen in Text entfernen, bei Bedarf erweitern. ARD auch &#039; statt richtig &#39;
	line_ret = (line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
		.replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", '"').replace("&#x27;", "'")
		.replace("&ouml;", "ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&szlig;", "ß")
		.replace("&Ouml;", "Ö").replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&apos;", "'"))
		
	# Log(line_ret)		# bei Bedarf
	return line_ret	
#----------------------------------------------------------------  	
def cleanhtml(line): # ersetzt alle HTML-Tags zwischen < und >  mit 1 Leerzeichen
	cleantext = line
	cleanre = re.compile('<.*?>')
	cleantext = re.sub(cleanre, ' ', line)
	return cleantext
#----------------------------------------------------------------  	
def mystrip(line):	# Ersatz für unzuverlässige strip-Funktion
	line_ret = line	
	line_ret = line.replace('\t', '').replace('\n', '').replace('\r', '')
	line_ret = line_ret.strip()	
	# Log(line_ret)		# bei Bedarf
	return line_ret






