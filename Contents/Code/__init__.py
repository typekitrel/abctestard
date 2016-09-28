# -*- coding: utf-8 -*-
#import lxml.html  	# hier für Konvertierungen - Funktionen von Plex nicht akzeptiert
#import requests	# u.a. Einlesen HTML-Seite, Methode außerhalb Plex-Framework 
import string
import urllib		# urllib.quote()
import os 			# u.a. Behandlung von Pfadnamen
import re			# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import time
import datetime

import locale

import updater


# +++++ ARD Mediathek 2016 Plugin for Plex +++++

VERSION =  '2.4.2'		
VDATE = '28.09.2016'


# (c) 2016 by Roland Scholz, rols1@gmx.de
#	GUI by Arauco (Plex-Forum)
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
ICON_ARD_EINSLIKE = 'ard-einslike.png' 			
ICON_ARD_RUBRIKEN = 'ard-rubriken.png' 			
ICON_ARD_Themen = 'ard-themen.png'	 			
ICON_ARD_Filme = 'ard-ausgewaehlte-filme.png' 	
ICON_ARD_FilmeAll = 'ard-alle-filme.png' 		
ICON_ARD_Dokus = 'ard-ausgewaehlte-dokus.png'			
ICON_ARD_DokusAll = 'ard-alle-dokus.png'		
ICON_ARD_Serien = 'ard-serien.png'				

ICON_ZDF_AZ = 'zdf-sendungen-az.png' 		
ICON_ZDF_VERP = 'zdf-sendung-verpasst.png'	
ICON_ZDF_RUBRIKEN = 'zdf-rubriken.png' 		
ICON_ZDF_Themen = 'zdf-themen.png'			
ICON_ZDF_MEIST = 'zdf-meist-gesehen.png' 	


ICON_OK = "icon-ok.png"
ICON_WARNING = "icon-warning.png"
ICON_NEXT = "icon-next.png"
ICON_CANCEL = "icon-error.png"
ICON_MEHR = "icon-mehr.png"


THUMBNAIL = [									# Vorgaben für THUMBNAILS in ZDF_BEITRAG_DETAILS, Suchergebnissen
  '946x532',									# 946x532 teilw. als Fallback gekennzeichnet
  '644x363',
  '672x378',
  '644x363',
  '485x273',
  '476x268',
  '404x227', 
  '404x227',
]

SENDUNGENAZ = [									# ZDF A-Z
  ['ABC', 'A', 'C'],
  ['DEF', 'D', 'F'],
  ['GHI', 'G', 'I'],
  ['JKL', 'J', 'L'],
  ['MNO', 'M', 'O'],
  ['PQRS', 'P', 'S'],
  ['TUV', 'T', 'V'],
  ['WXYZ', 'W', 'Z'],
  ['0-9', '0-9', '0-9']
]

BASE_URL = 'http://www.ardmediathek.de'
ARD_VERPASST = '/tv/sendungVerpasst?tag='		# ergänzt mit 0, 1, 2 usw.
ARD_AZ = '/tv/sendungen-a-z?buchstabe='			# ergänzt mit 0-9, A, B, usw.
ARD_Suche = '/tv/suche?searchText='				# ergänzt mit Suchbegriff
ARD_Live = '/tv/live'
ARD_Einslike = '/einslike'

ARD_Rubriken = 'http://www.ardmediathek.de/tv/Rubriken/mehr?documentId=21282550'
ARD_Themen = 'http://www.ardmediathek.de/tv/Themen/mehr?documentId=21301810'
ARD_Serien = 'http://www.ardmediathek.de/tv/Serien/mehr?documentId=26402940'
ARD_Dokus = 'http://www.ardmediathek.de/tv/Ausgew%C3%A4hlte-Dokus/mehr?documentId=33649086'
ARD_DokusAll = 'http://www.ardmediathek.de/tv/Alle-Dokus-Reportagen/mehr?documentId=29897596'
ARD_Filme = 'http://www.ardmediathek.de/tv/Ausgew%C3%A4hlte-Filme/mehr?documentId=33649088'
ARD_FilmeAll = 'http://www.ardmediathek.de/tv/Alle-Filme/mehr?documentId=33594630'
ARD_RadioAll = 'http://www.ardmediathek.de/radio/live?genre=Alle+Genres&kanal=Alle'

ZDF					= 'http://www.zdf.de/ZDFmediathek/hauptnavigation/startseite?flash=off'	# Mediathek ohne Flash
ZDF_RUBRIKEN      	= 'http://www.zdf.de/ZDFmediathek/xmlservice/web/rubriken'
ZDF_THEMEN        	= 'http://www.zdf.de/ZDFmediathek/xmlservice/web/themen'
ZDF_MEISTGESEHEN	= 'http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?id=_GLOBAL&maxLength=10&offset=%s'
ZDF_SENDUNGEN_AZ	= 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeStart=%s&characterRangeEnd=%s&detailLevel=2'
ZDF_SENDUNG_VERPASST = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?enddate=%s&maxLength=50&startdate=%s&offset=%s'
ZDF_SENDUNG         = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?id=%s&maxLength=25&offset=%s'
ZDF_BEITRAG        	= 'http://www.zdf.de/ZDFmediathek/beitrag/%s/%s'
ZDF_BEITRAG_DETAILS = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id=%s'
ZDF_Search_PATH		= 'https://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?searchString=%s&maxLength=%s&offset=%s'


REPO_NAME = 'Plex-Plugin-ARDMediathek2016'
GITHUB_REPOSITORY = 'rols1/' + REPO_NAME
myhost = 'http://127.0.0.1:32400'


''' 
####################################################################################################
TV-Live-Sender der Mediathek: | ARD-Alpha | BR |Das Erste | HR | MDR | NDR | RBB | SR | SWR | 
	WDR | tagesschau24 |  | KIKA | PHOENIX | Deutsche Welle
	zusätzlich: Tagesschau | NDR Fernsehen Hamburg, Mecklenburg-Vorpommern, Niedersachsen, Schleswig-Holstein |
	RBB Berlin, Brandenburg | MDR Sachsen-Anhalt, Sachsen, Thüringen

TV-Live-Sender des ZDF: ZDF | ZDFneo | ZDFkultur | ZDFinfo | 3Sat | ARTE (Sonderbehandlung im Code für ARTE 
	wegen relativer Links in den m3u8-Dateien)

TV-Live-Sender Sonstige: NRW.TV | Joiz | DAF | N24 | n-tv

Radio-Live-Streams der ARD: alle Radiosender von Bayern, HR, mdr, NDR, Radio Bremen, RBB, SR, SWR, WDR, 
	Deutschlandfunk. Insgesamt 10 Stationen, 63 Sender

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
	oc = home(cont=oc)							# Home-Button	
	
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ARD, name=name),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(Search,  channel='ARD', s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))
		
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name), title=" Sendung Verpasst (1 Woche)",
		summary='', tagline='TV', thumb=R(ICON_ARD_VERP)))
	oc.add(DirectoryObject(key=Callback(SendungenAZ, name='Sendungen 0-9 | A-Z'), title='Sendungen A-Z',
		summary='', tagline='TV', thumb=R(ICON_ARD_AZ)))
	oc.add(DirectoryObject(key=Callback(Einslike, title='Einslike'), title='Einslike',
		summary='', tagline='TV', thumb=R(ICON_ARD_EINSLIKE)))

	title = 'Ausgewählte Filme'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title), title=title,
		summary='', tagline='TV', thumb=R(ICON_ARD_Filme)))
	oc.add(DirectoryObject(key=Callback(ARDMore, title='Alle Filme'), title='Alle Filme',
		summary='', tagline='TV', thumb=R(ICON_ARD_FilmeAll)))
	title = 'Ausgewählte Dokus'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(ARDMore, title=title), title=title,
		summary='', tagline='TV', thumb=R(ICON_ARD_Dokus)))
	oc.add(DirectoryObject(key=Callback(ARDMore, title='Alle Dokus'), title='Alle Dokus',
		summary='', tagline='TV', thumb=R(ICON_ARD_DokusAll)))
	oc.add(DirectoryObject(key=Callback(ARDThemenRubrikenSerien, title='Serien'), title='Serien',
		summary='', tagline='TV', thumb=R(ICON_ARD_Serien)))
	oc.add(DirectoryObject(key=Callback(ARDThemenRubrikenSerien, title='Themen'), title='Themen',
		summary='', tagline='TV', thumb=R(ICON_ARD_Themen)))
	oc.add(DirectoryObject(key=Callback(ARDThemenRubrikenSerien, title='Rubriken'), title='Rubriken',
		summary='', tagline='TV', thumb=R(ICON_ARD_RUBRIKEN)))
	return oc	
	
#---------------------------------------------------------------- 
@route(PREFIX + '/Main_ZDF')
def Main_ZDF(name):
	Log('Funktion Main_ZDF'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art, title1=name)	
	oc = home(cont=oc)							# Home-Button	
	
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ZDF, name=name),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_ZDF_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(ZDF_Search,  channel='ZDF', s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_ZDF_SEARCH)))
		
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name), title="Sendung Verpasst (1 Woche)",
		thumb=R(ICON_ZDF_VERP)))
	oc.add(DirectoryObject(key=Callback(ZDFSendungenAZ, name="Sendungen A-Z"), title="Sendungen A-Z",
		thumb=R(ICON_ZDF_AZ)))
	oc.add(DirectoryObject(key=Callback(RubrikenThemen, auswahl="Rubriken"), title="Rubriken", 
		thumb=R(ICON_ZDF_RUBRIKEN)))
	oc.add(DirectoryObject(key=Callback(RubrikenThemen, auswahl="Themen"), title="Themen", thumb=R(ICON_ZDF_Themen)))
	oc.add(DirectoryObject(key=Callback(Sendung, title="Meist Gesehen", assetId="MEISTGESEHEN"), title="Meist Gesehen",
		thumb=R(ICON_ZDF_MEIST)))
 
	return oc	
#----------------------------------------------------------------
def home(cont):															# Home-Button, Aufruf: oc = home(cont=oc)			
	title = 'Zurück zum Hauptmenü'.decode(encoding="utf-8", errors="ignore")
	summary = 'Zurück zum Hauptmenü'.decode(encoding="utf-8", errors="ignore")
	cont.add(DirectoryObject(key=Callback(Main),title=title, summary=summary, tagline=NAME, thumb=R('home.png')))

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
	oc = home(cont=oc)				# Home-Button - in den Untermenüs Rücksprung hierher zu Einstellungen 
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
			oc = home(cont=oc)							# Home-Button	
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
	oc = home(cont=oc)								# Home-Button
	azlist = list(string.ascii_uppercase)
	azlist.append('0-9')
	#next_cbKey = 'SinglePage'	# 
	next_cbKey = 'PageControl'	# SinglePage zeigt die Sendereihen, PageControl dann die weiteren Seiten
	
	path = azPath = BASE_URL + ARD_AZ + 'A'		# A-Seite laden für Prüfung auf inaktive Buchstaben
	page = HTML.ElementFromURL(path)
	#s = XML.StringFromElement(page)
	Log(page)
	try:										# inaktive Buchstaben?
		#liste = page.xpath("//li[@class='inactive']/h3/text()")
		inactive_list  = page.xpath("//li[@class='inactive']")
		Log(inactive_list)		
	except:
		inactive_list = ""

	inactive_char = ""
	if inactive_list:							# inaktive Buchstaben ermitteln (werden 2 x angegeben)
		for element in inactive_list:
			char = element.xpath("./a/text()")[0]
			char = char.strip()
			#inactive_char.append(char)
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
			oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=azPath, next_cbKey=next_cbKey), 
					title=title,  thumb=R(ICON_ARD_AZ)))
	return oc
   
####################################################################################################
@route(PREFIX + '/Search')	# Suche - Verarbeitung der Eingabe
	# Hinweis zur Suche in der Mediathek: miserabler unscharfer Algorithmus - findet alles mögliche
def Search(channel, query=None, title=L('Search'), s_type='video', offset=0, **kwargs):
	Log('Search'); Log(query)
	
	name = 'Suchergebnis zu: ' + query
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
	path =  BASE_URL +  ARD_Suche + query  
	page = HTML.ElementFromURL(path)
	s = XML.StringFromElement(page)
	Log(page)
	
	i = s.find('<strong>keine Treffer</strong')
	Log(i)
	if i > 0:
		msg_notfound = 'Leider kein Treffer.'
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		summary = 'zurück zu ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ARD, name=NAME), title=msg_notfound, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ARD)))
		return oc
	else:
		oc = PageControl(title=name, path=path, cbKey=next_cbKey) 	# wir springen direkt
	 
	return oc
 
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
	oc = home(cont=oc)							# Home-Button	
		
	wlist = range(0,6)
	now = datetime.datetime.now()

	for nr in wlist:
		iPath = BASE_URL + ARD_VERPASST + str(nr)
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")		# Formate s. man strftime (3)
		zdfDate = rdate.strftime("%d%m%y")		
		iWeekday =  rdate.strftime("%A")
		punkte = '.'
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		iWeekday = transl_wtag(iWeekday)
		Log(iPath); Log(iDate); Log(iWeekday);
		#title = ("%10s ..... %10s"% (iWeekday, iDate))	 # Formatierung in Plex ohne Wirkung
		title = iWeekday + ' | ' + iDate	 # Bsp.: Heute........15.05.2015
		cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
		if name.find('ARD') == 0 :
			oc.add(DirectoryObject(key=Callback(PageControl, title=title, path=iPath, cbKey='SinglePage'), 
				title=title, thumb=R(ICON_ARD_VERP)))				
		else:
			oc.add(DirectoryObject(key=Callback(Sendung, title=title, assetId="VERPASST_"+zdfDate),	  
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
@route(PREFIX + '/Einslike')	# Menü Einslike (Rubrik-Liste)
	# Erweiterung Einslike: http://www.ardmediathek.de/einslike
	# 	Liste Rubriken (6): Leben, Musik, Netz & Tech, Spaß & Fiktion, Info, Neueste Videos
	# 	<a class="more" href="/einslike/Spa%C3%9F-Fiktion/mehr?documentId=21301902"
	#	Folgeseiten: mcontent=page (anders ARD-Mediathek: mcontents=page, stimmt Rest überein?)
	#
	# Info zu einslike: http://www.ard.de/home/ard/Gestatten__Einslike_/492028/index.html
	# Ablauf: 	
	#			hier: Rubrik-Liste zusammenstellen mit Links zu den "mehr"-Seiten, 
	#			weiter wie Verpasst Woche (->PageControl -> SinglePage -> Parseplaylist -> CreateVideoClipObject
def Einslike(title):	
	title2='Einslike - Videos fuer Musik und Lifestyle in der ARD Mediathek'
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc)								# Home-Button
	page = HTML.ElementFromURL(BASE_URL + ARD_Einslike)
	list = page.xpath("//*[@class='more']")
	Log(page); Log(list)
	#next_cbKey = 'PageControl'	# SinglePage zeigt die Sendereihen, PageControl dann die weiteren Seiten
	
	for element in list:	# class='more']
		s = HTML.StringFromElement(element)
		Log(element); 	# Log(s)   	# class="more" - nur bei Bedarf
		path = element.xpath("./@href")[0]
		path = BASE_URL + path
		rubrik = element.xpath("./span/text()")[0]	
		rubrik = title + ' | ' + rubrik
		Log(path); Log(rubrik)
		oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=rubrik, cbKey='SingleSendung'), title=rubrik, 
			tagline=title2, summary='', thumb=R(ICON_ARD_EINSLIKE), art=R(ICON_ARD_EINSLIKE)))
		#oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=rubrik, next_cbKey=next_cbKey), title=rubrik, 
		#	tagline=title2, summary='', thumb='', art=ICON))
		
	return oc
	
####################################################################################################
@route(PREFIX + '/ARDThemenRubrikenSerien')	# Seiten die mehrere Beiträge pro Eintrag enhalten
def ARDThemenRubrikenSerien(title):			# leider nicht kompatibel mit PageControl
	Log('ARDThemenRubrikenSerien');
	if title.find('Themen') >= 0:
		title2='Themen in der ARD Mediathek'
		morepath = ARD_Themen
	if title.find('Rubriken') >= 0:
		title2='Rubriken in der ARD Mediathek'
		morepath = ARD_Rubriken
	if title.find('Serien') >= 0:
		title2='Serien in der ARD Mediathek'
		morepath = ARD_Serien
	
	next_cbKey = 'SinglePage'			# mehrere Beiträge  pro Satz
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc)								# Home-Button
	page = HTML.ElementFromURL(morepath)
	doc_txt = HTML.StringFromElement(page)
			
	# Folgeseiten?:
	pagenr_path =  re.findall("=page.(\d+)", doc_txt) # Mehrfachseiten?
	Log(pagenr_path)
	if pagenr_path:
		del pagenr_path[-1]						# letzten Eintrag entfernen (Doppel) - OK
	Log(pagenr_path)	
	
	if pagenr_path:	 							# bei Mehrfachseiten Liste weiter bauen, beginnend mit 1. Seite
		title = 'Weiter zu Seite 1'
		path = morepath + '&' + 'mcontent=page.1'  # 1. Seite, morepath würde auch reichen
		Log(path)
		oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey), title=title, 
			tagline='', summary='', thumb='', art=ICON))			
		
		for page_nr in pagenr_path:				# Folgeseiten
			path = morepath + '&' + 'mcontent=page.' + page_nr
			title = 'Weiter zu Seite ' + page_nr
			Log(path)
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey), title=title, 
				tagline='', summary='', thumb='', art=ICON))			
	else:										# bei nur 1 Seite springen wir direkt, z.Z. bei Rubriken
		Log(morepath)
		oc = SinglePage(path=morepath, title=title, next_cbKey=next_cbKey)
		
	return oc
####################################################################################################
@route(PREFIX + '/ARDMore')	# Seiten die nur 1 Beitrag pro Eintrag enhalten
def ARDMore(title):	#
	Log('ARDMore');
	title2=title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc)								# Home-Button
	next_cbKey = 'SingleSendung'	#
	
	if title.find('Ausgewählte Filme') >= 0:
		morepath = ARD_Filme
	if title.find('Alle Filme') >= 0:
		morepath = ARD_FilmeAll
	if title.find('Ausgewählte Dokus') >= 0:
		morepath = ARD_Dokus
	if title.find('Alle Dokus') >= 0:
		morepath = ARD_DokusAll
				 
	page = HTML.ElementFromURL(morepath)
	doc_txt = HTML.StringFromElement(page)
				
	pagenr_path =  re.findall("=page.(\d+)", doc_txt) # Mehrfachseiten?
	Log(pagenr_path)
	if pagenr_path:
		del pagenr_path[-1]						# letzten Eintrag entfernen (Doppel) - OK
	Log(pagenr_path)	

	
	if pagenr_path:	 							# bei Mehrfachseiten Liste Weiter bauen, beginnend mit 1. Seite
		title = 'Weiter zu Seite 1'
		path = morepath + '&' + 'mcontent=page.1'  # 1. Seite, morepath würde auch reichen
		Log(path)
		oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey), title=title, 
			tagline='', summary='', thumb='', art=ICON))			
		
		for page_nr in pagenr_path:
			path = morepath + '&' + 'mcontent=page.' + page_nr
			title = 'Weiter zu Seite ' + page_nr
			Log(path)
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=title, next_cbKey=next_cbKey), title=title, 
				tagline='', summary='', thumb='', art=ICON))			
	else:										# bei nur 1 Seite springen wir direkt, z.Z. bei Rubriken
		oc = getOnePage(path=morepath, title=title) 
		
	return oc

####################################################################################################
@route(PREFIX + '/PageControl')	# kontrolliert auf Folgeseiten. Mehrfache Verwendung.
	# Wir laden beim 1. Zugriff alle Seitenverweise in eine Liste. Bei den Folgezugriffen können die Seiten-
	# verweise entfallen - der Rückschritt zur Liste ist dem Anwender nach jedem Listenelement  möglich.
	# Dagegen wird in der Mediathek geblättert.
def PageControl(cbKey, title, path, offset=0):  # 
	title1='Folgeseiten: ' + title.decode(encoding="utf-8", errors="ignore")

	oc = ObjectContainer(view_group="InfoList", title1=title1, title2=title1, art = ObjectContainer.art)
	oc = home(cont=oc)								# Home-Button
	
	page = HTML.ElementFromURL(path)
	path_page1 = path							# Pfad der ersten Seite sichern, sonst gehts mit Seite 2 weiter
	
	Log('PageControl'); Log(cbKey); Log(path)
	# doc_txt = lxml.html.tostring(page)			# akzeptiert Plex nicht
	doc_txt = HTML.StringFromElement(page)
	#Log(doc_txt)

	pagenr_suche = re.findall("mresults=page", doc_txt)   
	pagenr_andere = re.findall("mcontents=page", doc_txt)  
	pagenr_einslike = re.findall("mcontent=page", doc_txt)  	# auch in ARDThemen
	Log(pagenr_suche); Log(pagenr_andere); Log(pagenr_einslike)
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike):
		Log('PageControl: Mehrfach-Seite mit Folgeseiten')
	else:												# keine Folgeseiten -> SinglePage
		Log('PageControl: Einzelseite, keine Folgeseiten'); Log(cbKey); Log(path); Log(title)
		oc = SinglePage(title=title, path=path, next_cbKey='SingleSendung') # wir springen direkt, 
		return oc															# erspart dem Anwender 1 Klick

	# pagenr_path =  re.findall("&mresults{0,1}=page.(\d+)", doc_txt) # lange Form funktioniert nicht
	pagenr_path =  re.findall("=page.(\d+)", doc_txt) # 
	Log(pagenr_path)
	if pagenr_path:
		# pagenr_path = repl_dop(pagenr_path) 	# Doppel entfernen (z.B. Zif. 2) - Plex verweigert, warum?
		del pagenr_path[-1]						# letzten Eintrag entfernen - OK
	Log(pagenr_path)
	pagenr_path = pagenr_path[0]	# 1. Seitennummer in der Seite - brauchen wir nicht , wir beginnen bei 1 s.u.
	Log(pagenr_path)		
	
	# ab hier Auflistung der Folgeseiten. letzten Eintrag entfernen (Mediathek: Rückverweis auf vorige Seite)
	list = page.xpath("//div/div/*[@class='entry']")  # sowohl in A-Z, als auch in Verpasst, 1. Element
	del list[-1]				# ebenfalls letzten Eintrag entfernen wie in pagenr_path
	Log(list)


	first_site = True								# falls 1. Aufruf ohne Seitennr.: im Pfad ergänzen für Liste		
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike) :		# re.findall s.o.  		
		if path_page1.find('mcontents=page') == -1: 
			path_page1 = path_page1 + 'mcontents=page.1'
		if path_page1.find('mresults=page') == -1:
			path_page1 = path_page1 + '&mresults=page.1'
		if path_page1.find('searchText=') >= 0:			#  kommt direkt von Suche
			path_page1 = path + '&source=tv&mresults=page.1'
		if path_page1.find('mcontent=page') >= 0:			#  einslike
			path_page1 = path_page1 + 'mcontent=page.1'
	else:
		first_site = False
		
	Log(first_site)
	if  first_site == True:										
		path_page1 = path
		title = 'Weiter zu Seite 1'
		next_cbKey = 'SingleSendung'
			
		Log(first_site); Log(path_page1); Log(next_cbKey)
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=path_page1, next_cbKey=next_cbKey), 
				title=title, thumb=ICON))
	else:	# Folgeseite einer Mehrfachseite - keine Liste mehr notwendig
		Log(first_site)
		oc = SinglePage(title=title, path=path, next_cbKey='SingleSendung') # wir springen wieder direkt
	
	for element in list:	# [@class='entry'] 
		pagenr_suche = ''; pagenr_andere = ''; title = ''; href = ''
		# s = lxml.html.tostring(element)    # nicht in Plex
		s = HTML.StringFromElement(element)
		try:
			href = element.xpath("./a/@href")[0]
		except:
			continue							# Satz verwerfen
			
		Log(element); 	# Log(s)  # class="entry" - nur bei Bedarf
		pagenr =  re.findall("=page.(\d+)", s) 	# einzelne Nummer aus dem Pfad s ziehen	

		Log(pagenr); Log(href); #Log(pagenr_andere)
					
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
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=href, next_cbKey=next_cbKey), 
				title=title, thumb=ICON))
	    
	Log(len(oc))
	return oc
  
####################################################################################################
@route(PREFIX + '/SinglePage')	# Liste der Sendungen eines Tages / einer Suche 
								# durchgehend angezeigt (im Original collapsed)
def SinglePage(title, path, next_cbKey, offset=0):	# path komplett
	Log('Funktion SinglePage: ' + path)
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc)								# Home-Button
	
	func_path = path								# für Vergleich sichern
					
	page = HTML.ElementFromURL(path) 	
	
	sendungen = page.xpath("//*[@class='teaser']") 	# 1 oder mehrere Sendungen
	if not sendungen: 								# für A-Z-Ergebnisse + in Verpasst, 1. Element
		sendungen = page.xpath("//div/div/*[@class='entry']") 
		
	#Log(sendungen)
	send_arr = get_sendungen(oc, sendungen)	# send_arr enthält pro Satz 8 Listen 
	# Rückgabe end_arr = (send_path, send_headline, send_img_src, send_millsec_duration)
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
		millsec_duration = send_millsec_duration[i]
		if not millsec_duration:
			millsec_duration = "leer"
		dachzeile = send_dachzeile[i]
		Log(dachzeile)
		sid = send_sid[i]
		summary = img_alt
		if dachzeile != "":
			summary = dachzeile 
		if  subtitel != "":
			subtitel = subtitel.decode(encoding="utf-8", errors="ignore")
			summary = subtitel
			if  dachzeile != "":
				summary = dachzeile + ' | ' + subtitel
		summary = unescape(summary)
		summary = summary.decode(encoding="utf-8", errors="ignore")
		
		Log('path: ' + path); Log(title); Log(headline); Log(img_src); Log(millsec_duration);
		Log('next_cbKey: ' + next_cbKey); Log('summary: ' + summary);
		if next_cbKey == 'SingleSendung':		# Callback verweigert den Funktionsnamen als Variable
			Log('path: ' + path); Log('func_path: ' + func_path); Log('subtitel: ' + subtitel); Log(sid)
			if func_path == BASE_URL + path: 	# überspringen - in ThemenARD erscheint der Dachdatensatz nochmal
				Log('BASE_URL + path == func_path | Satz überspringen');
				continue
			if subtitel == '':	# ohne subtitel verm. keine EinzelSendung, sondern Verweis auf Serie o.ä.
				continue
			
			path = BASE_URL + '/play/media/' + sid			# -> *.mp4 (Quali.-Stufen) + master.m3u8-Datei (Textform)
			oc.add(DirectoryObject(key=Callback(SingleSendung, path=path, title=headline, thumb=img_src, 
				duration=millsec_duration), title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
		if next_cbKey == 'SinglePage':		# Callback verweigert den Funktionsnamen als Variable
			path = BASE_URL + path
			Log('path: ' + path);
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=headline, next_cbKey='SingleSendung'), 
				title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
		if next_cbKey == 'PageControl':		# Callback verweigert den Funktionsnamen als Variable
			path = BASE_URL + path
			Log('path: ' + path);
			oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=headline, cbKey='SingleSendung'), title=headline, 
				tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
					
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

	Log('SingleSendung path: ' + path)					# z.B. http://www.ardmediathek.de/play/media/11177770
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc)								# Home-Button
	# Log(path)
	page = HTTP.Request(path).content  # als Text, nicht als HTML-Element

	link_path,link_img, m3u8_master = parseLinks_Mp4_Rtmp(page)	# link_img kommt bereits mit thumb,  hier auf Vorrat						
	Log(link_path); Log(link_img); Log(m3u8_master);  

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
			summary='automatische Auflösung | Auswahl durch den Player', meta=Codecs, thumb=thumb, 
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
					summary=summary, meta=path, thumb=thumb, duration=duration, rtmp_live='nein', resolution=''))					
			else:
				summary='Video-Format: MP4'	# 3. mp4-Links:	
				oc.add(CreateVideoClipObject(url=url, title=title, 
					summary=summary, meta=path, thumb=thumb, duration=duration, resolution=''))
						
	return oc
#--------------------------			 		
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
				Log(mark); Log(s2); Log(link); Log(link_path)
			
	Log(link_path)				
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
	
	Log('get_sendungen'); Log(sendungen)
	# send_arr nimmt die folgenden Listen auf (je 1 Datensatz pro Sendung)
	send_path = []; send_headline = []; send_subtitel = []; send_img_src = [];
	send_img_alt = []; send_millsec_duration = []; send_dachzeile = []; send_sid = []; 
	arr_ind = 0
	img_alt = ""	# fehlt manchmal
	for sendung in sendungen:				 
		#s = lxml.html.tostring(sendung)
		s = XML.StringFromElement(sendung)	# XML.StringFromElement Plex-Framework
		#Log(s)							#  class="teaser" - umfangreiche Ausgabe (nur bei Bedarf)						
		found_sendung = False
		if s.find('<div class="linklist">') == -1:
			if  s.find('subtitle') >= 0: 
				found_sendung = True
			if  s.find('dachzeile') >= 0: # subtitle in ARDThemen nicht vorhanden
				found_sendung = True
			if  s.find('headline') >= 0:  # in Rubriken weder subtitle noch dachzeile vorhanden
				found_sendung = True
				
		Log(found_sendung)
		if found_sendung:
			dachzeile = re.search("<p class=\"dachzeile\">(.*?)</p>\s+?", s)  # Bsp. <p class="dachzeile">Weltspiegel</p>
			if dachzeile:									# fehlt komplett bei ARD_SENDUNG_VERPASST
				dachzeile = dachzeile.group(1)
			else:
				dachzeile = ''
				
			headline = re.search("<h4 class=\"headline\">(.*?)</h4>\s+?", s) # Bsp. <h4 class="headline">Mit Armin ...</h4>
			headline = headline.group(1)					# group(1) liefert bereits den Ausschnitt
			#headline = stringextract('>', '<', s)
			headline = headline .decode('utf-8')			# tagline-Attribute verlangt Unicode
			if headline.find('- Hörfassung') >= 0:			# Hörfassung unterdrücken
				continue
			if headline.find('Diese Seite benötigt') >= 0:	# bei Rubriken im Error-Teaser
				continue
			hupper = headline.upper()
			if hupper.find(str.upper('Livestream')) >= 0:			# Livestream hier unterdrücken (mehrfach in Rubriken)
				continue
			if s.find('subtitle') >= 0:	# nicht in ARDThemen
				subtitel = re.search("<p class=\"subtitle\">(.*?)</p>\s+?", s)	# Bsp. <p class="subtitle">25 Min.</p>
				subtitel = subtitel.group(1)
			else:
				subtitel =""
				
			send_duration = subtitel
			send_date = ''
				
				
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
				
			img_src = ""
			if s.find('urlScheme') >= 0:					# Bildaddresse versteckt im img-Knoten
				img_src = img_urlScheme(s,320)				# ausgelagert - s.u.

			try:
				extr_path = sendung.xpath("./div/div/a/@href")[0]   	# ohne Pfad weiter (mehrere teaser am Seitenanfang)				
				Log(extr_path)
				sid = ""
				if extr_path.find('documentId=') >= 0:
					sid = extr_path.split('documentId=')[1]
				Log(sid)
				path = extr_path	# korrigiert in SinglePage für Einzelsendungen in  '/play/media/' + sid
				Log(path)
				#path = BASE_URL + '/play/media/' + sid			# -> *.mp4 (Quali.-Stufen) + master.m3u8-Datei
				#path = BASE_URL + path.split('documentId=')[0] + sid + '&documentId=' + sid			
				img_alt = sendung.xpath("./div/div/a/img/@alt")[0] 
				Log(img_alt)
							
			except:
				Log('xpath-Fehler in Liste class=teaserbox, sendung: ' + s )	# Satz überspringen
				continue
		
			Log('neuer Satz')
			Log(sid); Log(extr_path); Log(path); Log(img_src); Log(img_alt); Log(headline);  
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
	Log('img_urlScheme')
	#text = text.split('urlScheme&#039;:&#039;')[0]	#	zwischen beiden split-strings
	text = text.split('urlScheme')[1]					#	klappt wg. Sonderz. nur so	
	img_src = text.split('##width##')[0]
	img_src  = img_src [3:]						# 	vorne ':' abschneiden
	img_src = BASE_URL + img_src + str(dim)			# Größe nicht in Quelle, getestet: 160,265,320,640
	Log('img_urlScheme: ' + img_src)
		
	return img_src
####################################################################################################
@route(PREFIX + '/CreateVideoClipObject')	# <- SingleSendung Qualitätsstufen
	# Plex-Warnung: Media part has no streams - attempting to synthesize | keine Auswirkung
	# **kwargs erforderlich bei Fehler: CreateVideoClipObject() got an unexpected keyword argument 'checkFiles'
	#	beobachtet bei Firefox (Suse Leap) + Chrome (Windows7)
	#	s.a. https://github.com/sander1/channelpear.bundle/tree/8605fc778a2d46243bb0378b0ab40a205c408da4
def CreateVideoClipObject(url, title, summary, meta, thumb, duration, resolution, include_container=False, **kwargs):
	#title = title.encode("utf-8")		# ev. für alle ausgelesenen Details erforderlich
	Log('CreateVideoClipObject')
	Log(url); Log(duration); 
	# resolution = ''					# leer - Clients skalieren besser selbst
	resolution=[720, 540, 480]			# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich

 
	videoclip_obj = VideoClipObject(
	key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary,
		meta=meta, thumb=thumb, duration=duration, resolution=resolution, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
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
	oc = home(cont=oc)							# Home-Button	
		
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
	oc = home(cont=oc)								# Home-Button
			
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
			
			if epg_schema == 'ARD':						# EPG-Daten ARD holen 
				epg_date, epg_title, epg_text = get_epg_ARD(epg_url, listname)			
					
			if epg_schema == 'ZDF':						# EPG-Daten  ZDF holen	
				epgname = stringextract('<epgname>', '</epgname>', element_str)		
				epg_date, epg_title, epg_text = get_epg_ZDF(epg_url, epgname)	
									
			if epg_schema == 'KiKA':					# EPG-Daten  KiKA holen	
				epgname = stringextract('<epgname>', '</epgname>', element_str)		
				epg_date, epg_title, epg_text = get_epg_KiKA(epg_url, epgname)	
									
			if epg_schema == 'Phoenix':					# EPG-Daten  Phoenix holen	
				epgname = stringextract('<epgname>', '</epgname>', element_str)		
				epg_date, epg_title, epg_text = get_epg_Phoenix(epg_url, epgname)	
									
			if epg_schema == 'DW':					# EPG-Daten  Deutsche Welle holen	
				epgname = stringextract('<epgname>', '</epgname>', element_str)		
				epg_date, epg_title, epg_text = get_epg_DW(epg_url, epgname)	
								
		Log(epg_schema); Log(epg_url); 
		Log(epg_title); Log(epg_date); Log(epg_text[0:40]);		
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

	page = HTTP.Request(epg_url, cacheTime=1, timeout=float(1)).content # ohne xpath, Cache max. 1 sec
	# Log(page)		# nur bei Bedarf		
	
	s = stringextract('mod modA modProgramm', '<div class=\"modSocialbar\">', page)		
	#Log(s)			# nur bei Bedarf				
	if s.find('<span class=\"date\">'):
		epg_date = stringextract('<span class=\"date\">', '</span>', s)
		#epg_date = epg_date.replace('\t', '').replace('\n', '').replace('\r', '')
		epg_date = mystrip(epg_date)
	if s.find('<span class=\"titel\">'):
		epg_title = stringextract('<span class=\"titel\">', '</span', s)
		#epg_title = epg_title.strip(' \t\n\r')
		epg_title = mystrip(epg_title)
		epg_title = unescape(epg_title)				# HTML-Escapezeichen  im Titel	
			
	if s.find('<p class=\"teasertext\">'):			# kann fehlen
		epg_text = stringextract('<p class=\"teasertext\">', '</p', s)
		epg_text = epg_text.replace('\t', '').replace('\n', '').replace('\r', '')
		epg_text = unescape(epg_text)				# HTML-Escapezeichen  im Teasertext	
			
	epg_text = epg_text.decode(encoding="utf-8", errors="ignore") # möglich: UnicodeDecodeError: 'utf8' codec can't decode byte 0xc3 ...
	Log(epg_date); Log(epg_title); Log(epg_text[0:80]); 	
	return epg_date, epg_title, epg_text
#----------------------
def get_epg_ZDF(epg_url, epgname):					# EPG-Daten ermitteln für SenderLiveListe, ZDF
	Log('get_epg_ZDF: ' + epgname)		
	#Log(epgname)

	page = HTML.ElementFromURL(epg_url, cacheTime=1, timeout=float(1))	# EPG-Daten laden, Cache max. 1 sec
	#page = HTTP.Request(epg_url, cacheTime=1, timeout=float(1)).content # ohne xpath, Cache max. 1 sec
	x = ('{0} broadcasts'.format(epgname))			# xpath Bsp.: <td class="zdf_kultur broadcasts">
	xdef = (('//*[@class="{0}"]').format(x))
	Log(xdef)
	xpath_liste = page.xpath(xdef)					# EPG-Daten für ganzen Tag
	Log(epgname); # Log(liste)						# bei Bedarf
	
	now = datetime.datetime.now()
	nowtime = now.strftime("%H:%M")		# ZDF: <p class="time">23:10</p>
	epg_date = ''; epg_title = ''; epg_text = '';
	
	liste = []
	for i in range (len(xpath_liste)):		# bereinigen - häufig sowas: <td class="zdf broadcasts"></td>
		element = xpath_liste[i]		  
		element_str = HTML.StringFromElement(element)
		element_str = mystrip(element_str)
		if len(element_str) > 50:
			liste.append(element_str)	

	for i in range (len(liste)):
		element_str = liste[i]		  
		starttime = stringextract('<p class=\"time\">', '</p>', element_str)	# aktuelle Sendezeit
		
		try:
			element_next_str = liste[i+1]	# nächste Sendezeit			  
			endtime = stringextract('<p class=\"time\">', '</p>', element_next_str)	# nächste Sendezeit	
		except:
			endtime = '23:59'			# Listenende
					
		#Log(element_str); 				# bei Bedarf
		#Log(element_next_str)			# bei Bedarf
		Log('starttime ' + starttime); Log('endtime ' + endtime); Log('nowtime ' + nowtime);	# bei Bedarf
		
		if nowtime >= starttime and nowtime < endtime:
			#  	Beschreib.: h3, (h5), (p, p). h3= titel, h5= Untertitel, p=Herkunft/Jahr 
			epg_date = starttime
			pos = element_str.find(starttime)			# auf Seite wiederfinden + ausschneiden, enthält col_r
			pos2 = element_str.find('broadcasts\">', pos +1) 
			try:
				col_r =  element_str[pos:pos2]
			except:
				col_r =  element_str[pos:]			
			
			epg_title = stringextract('<h3>', '</h3>', col_r)	# h5, h3 immmer vorhanden, h3 manchmal leer			
			etext = stringextract('<h5>', '</h5>', col_r)
			Log(epg_date); Log(epg_title); Log(etext); 
			if col_r.find('<p>'):
				etext2 = stringextract('<p>', '</p>', col_r)			# Text?
				lpos = col_r.find('/p')
				#Log(lpos)					# bei Bedarf
				etext3 = ''
				if col_r.find('<p>', lpos + 2) >0 :						# noch weiterer Text?
					col_r = col_r[lpos +  2:]
					#Log(col_r)						
					etext3 = stringextract('<p>', '</p>', col_r)	
			if etext:
				if etext2: 
					etext = etext + ' | ' + etext2
					if etext3: 
						etext = etext2 + ' | ' + etext3
			epg_text = etext
			epg_text = unescape(epg_text)		
			
			break												# fertig mit 'Jetzt'
						
	epg_text = epg_text.decode(encoding="utf-8", errors="ignore")	
	Log(epg_date); Log(epg_title); Log(epg_text[0:40]);  
	return epg_date, epg_title, epg_text
#----------------------
def get_epg_KiKA(epg_url, epgname):					# EPG-Daten ermitteln für SenderLiveListe, KiKA
	Log('get_epg_KiKA: ' + epgname)		

	#page = HTML.ElementFromURL(epg_url, cacheTime=1, timeout=float(1))	# EPG-Daten laden, Cache max. 1 sec
	page = HTTP.Request(epg_url, cacheTime=1, timeout=float(1)).content # für KIKA ohne xpath - hier nur Stringsuche
	
	now = datetime.datetime.now()
	nowtime = now.strftime("%Y-%m-%dT%H:%M:%S")		# im kika-format

	epg_date = ''; 	epg_title = ''; epg_text = ''
	# Suchzeile: data-ctrl-livestreamprogress= ... ,'start':'2016-06-19T07:50:00+02:00','end':'2016-06-19T08:20:00+02:00'}"
	while len(page) >= 0:
		data_line = stringextract('data-ctrl-livestreamprogress=', '}\"', page)
		pos = page.find('data-ctrl-livestreamprogress=')
		next_pos = pos + len(data_line)	
		page_segment =  page[next_pos:] 						# Teilstück auschneiden
		pos2 = page_segment.find('data-ctrl-livestreamprogress=')
		page_segment =  page_segment[:pos2]  							

		# Log(data_line); Log(next_pos);  Log(pos2); Log(page_segment) # bei Bedarf
		if data_line == '':
			break

		if data_line.find('start'):
			starttime = stringextract('\'start\':\'', '\',', data_line)
			endtime = stringextract('\'end\':\'', '\'', data_line)
			Log(data_line); Log(starttime); Log(endtime)
			
			starttime.split('+')[0]; endtime.split('+')[0];		# +02:00 abschneiden
			if nowtime >= starttime and nowtime < endtime:
				epg_date = starttime[11:16] + ' - ' + endtime[11:16]
				epg_title = stringextract('<h4 class=\"headline\">', '</h4>', page_segment) # Titel fehlt manchmal
				epg_text = epg_title 														# epg_text fehlt hier
				epg_title = unescape(epg_title)				# HTML-Escapezeichen  im Titel	
				epg_text = unescape(epg_text)				# HTML-Escapezeichen  im Titel	
				break											# fertig
		page = page[next_pos:]		# ab hier weitersuchen		
				
	if epg_date == '' and epg_title == "":			# ab ca. 21 Uhr Sendeschluss
		epg_date = nowtime = now.strftime("jetzt: %H:%M")	
		epg_title= 'keine Sendung gefunden'; epg_text = 'vermutlich Sendeschluss'
	epg_text = epg_text.decode(encoding="utf-8", errors="ignore")	
	Log(epg_date); Log(epg_title); Log(epg_text[0:40]);  
	return epg_date, epg_title, epg_text
#----------------------
def get_epg_Phoenix(epg_url, epgname):					# EPG-Daten ermitteln für SenderLiveListe, Phoenix
	Log('get_epg_Phoenix: ' + epgname)		
	#Log(epgname)

	#page = HTML.ElementFromURL(epg_url, cacheTime=1, timeout=float(0.5))	# EPG-Daten laden, Cache max. 1 sec
	page = HTML.ElementFromURL(epg_url, cacheTime=1)
	#page = HTTP.Request(epg_url, cacheTime=1, timeout=float(1)).content # ohne xpath, Cache max. 1 sec
	
	liste = page.xpath("//div[@class='sendung aktiv']")	# Phoenix zeigt  EPG-Daten eindeutig für die aktuelle Sendung
		
	Log(liste);
	epg_date = ''; epg_title = ''; epg_text = '';
	try:			# manchmal ohne Kennung 'sendung aktiv'
		element = liste[0]	# Phoenix zeigt  EPG-Daten eindeutig für die aktuelle Sendung
	except:
		Log('get_epg_Phoenix: Kennung >sendung aktiv< fehlt');
		now = datetime.datetime.now()
		epg_date = now.strftime("%H:%M")			# akt. Zeit als Fehlerhinweis
		epg_title = 'Programmhinweis >sendung aktiv< fehlt auf ' + epg_url
		return epg_date, epg_title, epg_text
	
	
	s = HTML.StringFromElement(element)
	Log(s[0:40])					# bei Bedarf
	
	epg_date =  stringextract('\"uz\">', '<', s)	# Formate: class="uz">21.45<br/>, class="uz">22.30</span>
	epg_date =  epg_date[0:5]						# vorsichtshalber begrenzen				
	epg_title_h1 = stringextract('<h1>', '</h1>', s)
	epg_title_h1 = epg_title_h1.split('title=')[1]
	epg_title = stringextract('>', '<', epg_title_h1)
	
	epg_text = stringextract('<em>', '</em>', s)
	epg_text = unescape(epg_text)				# HTML-Escapezeichen  im Teasertext	
	
	epg_text = epg_text.decode(encoding="utf-8", errors="ignore")	
 	Log(epg_date); Log(epg_title); Log(epg_text[0:40]);  
	return epg_date, epg_title, epg_text
 
#----------------------
def get_epg_DW(epg_url, epgname):					# EPG-Daten ermitteln für SenderLiveListe, Deutsche Welle
	Log('get_epg_DW: ' + epgname)	
	#page = HTML.ElementFromURL(epg_url, cacheTime=1)
	page = HTTP.Request(epg_url, cacheTime=1, timeout=float(1)).content #  nur Stringsuche
	
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

	oc = ObjectContainer(view_group="InfoList", title1=title + ' Live', art=ICON)
	oc = home(cont=oc)								# Home-Button
	
	Codecs = 'H.264'	# dummy-Vorgabe für PHT (darf nicht leer sein)										
	if title.find('Arte') >= 0:
		Log('Arte-Stream gefunden')			
		oc = Arteplaylist(oc, url_m3u8, title, thumb)	# Auswertung Arte-Parameter rtmp- + hls-streaming
		Log(len(oc))
		return oc
		
	if url_m3u8.find('rtmp') == 0:		# rtmp, summary darf für PHT nicht leer sein
		oc.add(CreateVideoStreamObject(url=url_m3u8, title=title, 
			summary='rtmp-Stream', meta=Codecs, thumb=thumb, rtmp_live='ja', resolution=''))
		return oc
		
	# alle übrigen (i.d.R. http-Links)
	if url_m3u8.find('.m3u8') >= 0:					# häufigstes Format
		if url_m3u8.find('http://') == 0:			# URL oder lokale Datei? (lokal entfällt Eintrag "autom.")			
			oc.add(CreateVideoStreamObject(url=url_m3u8, title=title + ' | Bandbreite und Auflösung automatisch', 
				summary='automatische Auflösung | Auswahl durch den Player', meta=Codecs, thumb=thumb, 
				rtmp_live='nein', resolution=''))
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
		summary='HLS-Streaming deutsch', meta='', thumb=thumb, rtmp_live='nein', resolution=''))
	oc.add(CreateVideoStreamObject(url=hls2_url, title=title2 + ' (fr) | http', 
		summary='HLS-Streaming französisch', meta='', thumb=thumb, rtmp_live='nein', resolution=''))
	
	Log(len(oc))
	return oc

####################################################################################################
@route(PREFIX + '/CreateVideoStreamObject')	# <- LiveListe, SingleSendung (nur m3u8-Dateien)
											# **kwargs - s. CreateVideoClipObject
def CreateVideoStreamObject(url, title, summary, meta, thumb, rtmp_live, resolution, include_container=False, **kwargs):
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
  
	Log('CreateVideoStreamObject: '); Log(url); Log(rtmp_live) 
	Log('include_container: '); Log(include_container)

	if url.find('rtmp:') >= 0:	# rtmp = Protokoll für flash, Quellen: rtmpdump, shark, Chrome/Entw.-Tools
		if rtmp_live == 'ja':
			Log('rtmp_live: '); Log(rtmp_live) 
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url,live=True))]) # live=True nur Streaming
			rating_key = title
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, 
				meta=meta, thumb=thumb, rtmp_live='ja', resolution=[720, 540, 480], include_container=True), 
				rating_key=title,
				title=title,
				summary=summary,
				thumb=thumb,)  
		else:
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url))])
			rating_key = title
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, 
				meta=meta, thumb=thumb, rtmp_live='nein', resolution='', include_container=True), 
				rating_key=title,
				title=title,
				summary=summary,
				thumb=thumb,) 			 

	else:
		# Auslösungsstufen weglassen? (bei relativen Pfaden nutzlos) 
		# Auflösungsstufen - s. SenderLiveResolution -> Parseplaylist
		resolution=[720, 540, 480]		# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich
		meta=url						# leer (None) im Webplayer OK, mit PHT:  Server: Had trouble breaking meta
		mo = MediaObject(parts=[PartObject(key=HTTPLiveStreamURL(url=url))]) 
		rating_key = title
		videoclip_obj = VideoClipObject(					# Parameter wie MovieObject
			key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,
			meta=meta, thumb=thumb, rtmp_live='nein', resolution=resolution, include_container=True), 
			rating_key=title,
			title=title,
			summary=summary,
			thumb=thumb,)
			
	videoclip_obj.add(mo)

	Log(url); Log(title); Log(summary); 
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
	Log('PlayVideo: ' + url); # Log('PlayVideo: ' + resolution)	 		
	HTTP.Request(url).content
	return Redirect(url)

####################################################################################################
@route(PREFIX + '/RadioLiveListe')  
def RadioLiveListe(path, title):
	Log('RadioLiveListe');
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	oc = home(cont=oc)								# Home-Button
	
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
			title=title, summary='weitere Sender', tagline='Radio', thumb=img))
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
		oc = home(cont=oc)							# Home-Button macht bei PHT die Trackliste unbrauchbar 
			
	page = HTML.ElementFromURL(path) 
	entries = page.xpath("//*[@class='teaser']")
	
	del entries[0:2]								# "Javascript-Fehler" überspringen (2 Elemente)
	Log(entries)

	for element in entries:
		s = XML.StringFromElement(element)	# XML.StringFromElement Plex-Framework
		Log(s[0:80])						#  nur bei Bedarf)						
		
		img_src = ""
		if s.find('urlScheme') >= 0:					# Bildaddresse versteckt im img-Knoten
			img_src = img_urlScheme(s,320)				# ausgelagert - s.u.
			
		headline = ''; subtitel = ''		# nicht immer beide enthalten
		if s.find('headline') >= 0:			# h4 class="headline" enthält den Sendernamen
			headline = stringextract('\"headline\">', '</h4>', s)
			headline = headline .decode('utf-8')		# tagline-Attribute verlangt Unicode
		if s.find('subtitle') >= 0:	
			subtitel = stringextract('\"subtitle\">', '</p>', s)
		Log(headline); Log(subtitel);					
			
		href = element.xpath("./div/div/a/@href")[0]
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
		msgH = 'keine Radiostreams bei ' + title + ' gefunden/verfuegbar' 
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
@route(PREFIX + '/ZDF_Search')	# Suche - Verarbeitung der Eingabe
	# Hinweis zur Suche in der Mediathek: miserabler unscharfer Algorithmus - findet alles mögliche
def ZDF_Search(channel, query=None, title=L('Search'), s_type='video', offset=0, **kwargs):
	query = urllib.quote(query)
	Log('ZDF_Search'); Log(query)
	
	maxLength = 50
	Log(maxLength); Log(offset); 
	
	path = ZDF_Search_PATH % (query, maxLength, offset)
	Log(maxLength);Log(path)	
	content = XML.ElementFromURL(path)
	
	searchResult = content.xpath('//teaserlist/searchResult/batch/text()')[0]
	Log(content);Log(searchResult)	
	
	NAME = 'ZDF Mediathek'
	name = 'Suchergebnis zu: %s (Gesamt: %s, ab %s)'  		% (urllib.unquote(query), searchResult, max(1, offset))
	name = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	oc = home(cont=oc)								# Home-Button

	if searchResult == '0':
		msg_notfound = 'Leider kein Treffer.'
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		summary = 'zurück zu ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main_ZDF, name=NAME), title=msg_notfound, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN_ZDF)))
		return oc
	
	teasers = content.xpath('//teaserlist/teasers/teaser')
	# Log(teasers);
	for teaser in teasers:
		teaserimages = teaser.xpath('./teaserimages/teaserimage')
		thumbfind = False
		for image in teaserimages:
			if thumbfind:
				continue
			s = XML.StringFromElement(image)
			s = mystrip(s)
			thumb = stringextract('http:', '</teaserimage>', s)
			thumb = 'http:' + thumb
			# Log(s); Log(thumb)
			for res in THUMBNAIL:			# entweder Größe passend zur Liste oder letztes Image	
				if thumb.find(res) > 0:
					thumbfind = True
					# Log(res); Log(thumb);
					break

		title = teaser.xpath('./information/title')[0].text
		summary = teaser.xpath('./information/detail')[0].text
		assetId = teaser.xpath('./details/assetId')[0].text
		assetId = 'SEARCH_' + assetId
		
		typ = teaser.xpath('./type')[0].text
		# hier ev. weitere geeignete Formate verwenden (Bilderserien, Themen usw.)
		# 	getestet + nicht geeignet: einzelsendung, thema, sendung
		if(typ !=  'video'):	
			Log('ZDF_Search: Unsupported type ' + typ)
			continue

		airtime = teaser.xpath('./details/airtime')[0].text
		date = Datetime.ParseDate(airtime)
		# lengthSec = teaser.xpath('./details/lengthSec')[0].text   # nicht immer vorh. (z.B. Suche)
		length = teaser.xpath('./details/length')[0].text
		dauer = length		# ev. noch formatieren, Bsp.: 11 min, 00:02:27.000, oder zusätzl. <lengthSec>147</lengthSec>
		if dauer.find('.000'):
			dauer = dauer.split('.000')[0]
		tagline = airtime + ' | ' + dauer

		Log(assetId);Log(typ);Log(title);Log(thumb);Log(summary[0:40]);
		summary = summary.decode(encoding="utf-8", errors="ignore")
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		# in Sendung wird die Suchanfrage wiederholt und der Treffer über die assetId ausgefiltert:
		oc.add(DirectoryObject(key=Callback(Sendung, title=title, assetId=assetId, search_url=path), title=title, 
			thumb=thumb, summary=summary, tagline=tagline))
			
	# auf mehr prüfen:
	if int(offset) + int(maxLength) < int(searchResult):
		offset = int(offset) + int(maxLength) + 1 
		oc.add(DirectoryObject(key=Callback(ZDF_Search, channel=channel, query=query, offset=offset ), 
			title=str("Weitere Beiträge").decode('utf-8', 'strict'), thumb=R(ICON_MEHR), summary=None))	
 
	return oc
 
####################################################################################################
@route(PREFIX + '/ZDFSendungenAZ')
def ZDFSendungenAZ(name):
	Log('ZDFSendungenAZ')
	oc = ObjectContainer(title2=name, view_group="List")
	oc = home(cont=oc)								# Home-Button

	# A to Z
	for page in SENDUNGENAZ:
		oc.add(DirectoryObject(key=Callback(SendungenAZList, char=page[0]), title=page[0], thumb=R(ICON_ZDF_AZ)))
	return oc

####################################################################################################
@route(PREFIX + '/RubrikenThemen')
def RubrikenThemen(auswahl):
	#auswahl = 'Rubriken'
	Log.Debug('RubrikenThemen: ' + auswahl)
	oc = ObjectContainer(title2='ZDF: ' + auswahl, view_group="List")
	oc = home(cont=oc)								# Home-Button

	if(auswahl == 'Rubriken'):
		content = XML.ElementFromURL(ZDF_RUBRIKEN, cacheTime=CACHE_1HOUR)
		#content = XML.ElementFromURL(ZDF_RUBRIKEN, cacheTime=0)	# Debug
	elif(auswahl == 'Themen'):
		content = XML.ElementFromURL(ZDF_THEMEN, cacheTime=CACHE_1HOUR)
		#content = XML.ElementFromURL(ZDF_THEMEN, cacheTime=0)	# Debug
	else:
		raise Ex.MediaNotAvailable
		
	Log(content)
	teasers = content.xpath('//teaserlist/teasers/teaser')
	for teaser in teasers:
		typ = teaser.xpath('./type')[0].text
		if(typ != 'rubrik' and typ != 'topthema' and typ != 'thema'):
			Log('RubrikenThemen: Unsupported type ' + typ)
			continue
      
		for res in THUMBNAIL:
			thumb = teaser.xpath('./teaserimages/teaserimage[@key="%s"]' % (res))[0].text
			if thumb.find('fallback') == -1:
				break
      
		title = teaser.xpath('./information/title')[0].text
		summary = teaser.xpath('./information/detail')[0].text
		assetId = teaser.xpath('./details/assetId')[0].text

		tagline = None
		if(typ == 'topthema'):
			title = 'Topthema - %s' % (title)
			tagline = 'Topthema'
		oc.add(DirectoryObject(key=Callback(Sendung, title=title, assetId=assetId), title=title, 
			thumb=thumb, summary=summary, tagline=tagline))
			
	Log(auswahl); Log(title); Log(assetId);
	return oc
	
####################################################################################################
@route(PREFIX + '/SendungenAZList/{char}')
def SendungenAZList(char):
	Log('SendungenAZList')
	oc = ObjectContainer(title2=char, view_group="List")
	oc = home(cont=oc)								# Home-Button

	for page in SENDUNGENAZ:
		if page[0] != char:
			continue
		content = XML.ElementFromURL(ZDF_SENDUNGEN_AZ % (page[1], page[2]), cacheTime=CACHE_1HOUR)
		#content = XML.ElementFromURL(ZDF_SENDUNGEN_AZ % (page[1], page[2]), cacheTime=0)	# Debug
		teasers = content.xpath('//teaserlist/teasers/teaser')
		for teaser in teasers:
			for res in THUMBNAIL:
				thumb = teaser.xpath('./teaserimages/teaserimage[@key="%s"]' % (res))[0].text
				if thumb.find('fallback') == -1:
					break
      
			title = teaser.xpath('./information/title')[0].text
			summary = teaser.xpath('./information/detail')[0].text
			assetId = teaser.xpath('./details/assetId')[0].text
			oc.add(DirectoryObject(key=Callback(Sendung, title=title, assetId=assetId), title=title, 
				thumb=thumb, summary=summary))
  
	if len(oc) == 1:	# home berücksichtigen
		return NotFound('Leer - keine Sendung(en), die mit  >' + char + '< starten')

	return oc
  
####################################################################################################
@route(PREFIX + '/Sendung/{assetId}', allow_sync = True)
def Sendung(title, assetId, offset=0, search_url = None, search_mode=False):
	Log('Sendung: ' + title); Log(assetId); Log(offset);Log(search_url);
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	oc = home(cont=oc)								# Home-Button

	if(assetId == 'MEISTGESEHEN'):
		maxLength = 25	# vormals 10
		content = XML.ElementFromURL(ZDF_MEISTGESEHEN % (offset), cacheTime=CACHE_1HOUR)
	elif(assetId.find('VERPASST_') != -1):
		maxLength = 50
		Log(maxLength); 
		d = re.search('VERPASST_([0-9]{1,6})', assetId)
		day = d.group(1)
		content = XML.ElementFromURL(ZDF_SENDUNG_VERPASST % (day, day, offset), cacheTime=CACHE_1HOUR)
	elif(assetId.find('SEARCH_') != -1):	# Diese assetId werden über die URL ZDF_SENDUNG nicht gefunden
		search_mode = True					# Ablauf: Wiederholung Suchanfrage (search_url), Ausfiltern assetId
		maxLength = 50		# hier nur Platzhalter
		assetId = assetId.split('SEARCH_')[1]
		content = XML.ElementFromURL(search_url)
	else:
		maxLength = 25
		content = XML.ElementFromURL(ZDF_SENDUNG % (str(assetId), offset), cacheTime=CACHE_1HOUR)

	Log(assetId);  Log(content); 
	try:	# Attribut additionalTeaser in Suchergebnissen n.v. 
		more = content.xpath('//teaserlist/additionalTeaser')[0].text == 'true'
	except:
		more  = False
		
	teasers = content.xpath('//teaserlist/teasers/teaser')
	Log(more); Log(teasers)
	for teaser in teasers:
		s = XML.StringFromElement(teaser)
		# Log(s)	# bei Bedarf
		typ = teaser.xpath('./type')[0].text
		Log('teaser: '); Log(teaser);Log(typ);
		teaserimages = teaser.xpath('./teaserimages/teaserimage')
		thumbfind = False
		for image in teaserimages:
			if thumbfind:
				continue
			s = XML.StringFromElement(image)
			s = mystrip(s)
			thumb = stringextract('http:', '</teaserimage>', s)
			thumb = 'http:' + thumb
			# Log(s); Log(thumb)
			for res in THUMBNAIL:			# entweder Größe passend zur Liste oder letztes Image	
				if thumb.find(res) > 0:
					thumbfind = True
					# Log(res); Log(thumb);
					break
		
		ttitle = teaser.xpath('./information/title')[0].text	
		tsummary = teaser.xpath('./information/detail')[0].text
		tassetId = teaser.xpath('./details/assetId')[0].text
		Log('2154');Log(thumb);Log(typ); Log(ttitle); Log(tsummary); Log(assetId); Log(tassetId);
		if search_mode and (assetId != tassetId):	# übergebenene assetId Suchergebnis herausfiltern
				continue
		
		'''			
		Problemfeld Video-URL:
			Videoquellen werden im Webservice der ZDF-Mediathek über folgende URL ermittelt (Bsp.:)
				details-Bsp.: http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id=2739308
			Die Auswahl ist umfangreich - häufig ca. 30 Quellen in verschiedenen Auflösungen, darunter 
			h264-mpeg4-Videos, rtsp-Streams, vod-Streams (Video-on-Demand, Dateiendung manifest.f4m), 
			http-Streams (Dateiendung manifest.mp4), rtmp/rtmpt-Streams (Dateiendungen .smil, .meta), 
			MOV-Videos (QuickTime Movie, Dateiendung .mov), WebM-Videos (HTML5-Videos, Dateiendung .webm),
			m3u8-Streaming (Playlist-Datei, Dateiendung .m3u8).
			Zusätzliche gibt es noch eine Version für HBBTV (mit spez. Receiver) im Feld <tvUrl>.
			
			In ZDFMediathek V2.0 wurde die Video-URL für h264-mpeg4-Videos (basetype="h264_aac_mp4_http_na_na")
			ermittelt. Die Server sind unterschiedlich (z.B. vdl.zdf.de, nrodl.zdf.de); einige blocken die 
			Auslieferung (beobachtet bei  vdl.zdf.de), ev. um Downloads zu verhindern.
			
			Wir verwenden hier vorerst nur die m3u8-Streaming-Angebote, da solche sich im Plugin ARDMediathek2016
			bewährt haben und die offenichtlich bei jeder Sendung angeboten werden (hier: 
			basetype="h264_aac_ts_http_m3u8_http". Bei Bedarf können später andere nachgerüstet werden.		
		'''
		if(typ == 'video'):
			show = teaser.xpath('./details/originChannelTitle')[0].text
			if(show != title):
				ttitle = '%s - %s' % (show, ttitle)

			#airtime = teaser.xpath('./details/onlineairtime')[0].text  # Archivierungszeitpunkt?
			airtime = teaser.xpath('./details/airtime')[0].text
			date = Datetime.ParseDate(airtime)
			# lengthSec = teaser.xpath('./details/lengthSec')[0].text   # nicht immer vorh. (z.B. Suche)
			length = teaser.xpath('./details/length')[0].text
			dauer = length		# ev. noch formatieren, Bsp.: 11 min, 00:02:27.000, oder zusätzl. <lengthSec>147</lengthSec>
			if dauer.find('.000'):
				dauer = dauer.split('.000')[0]
			tagline = airtime + ' | ' + dauer
			duration = CalculateDuration(length)
			details = XML.ElementFromURL(ZDF_BEITRAG_DETAILS % tassetId, cacheTime=CACHE_1HOUR)
			#details = XML.ElementFromURL(ZDF_BEITRAG_DETAILS % tassetId, cacheTime=0)	# Debug
			vtype = details.xpath('//video/type')[0].text
			Log('vtype: ' + vtype); Log(tagline); Log(dauer); Log(duration); Log(details); 
				
			if(vtype == 'video' or vtype == 'livevideo'):  # wir verwenden nur m3u8-Dateien, falls vorhanden
				try:	# manchmal nur im Angebot: vcmsUrl (Verweis auf Beitrag in der Mediathek)  oder tvUrl (HBBTV) 
					#videoURL = details.xpath('//formitaet[@basetype="h264_aac_mp4_http_na_na" and quality="veryhigh" and ratio="16:9"]/url')[0].text # V 2.0
					videoURL = details.xpath('//formitaet[@basetype="h264_aac_ts_http_m3u8_http" and quality="high"]/url')[0].text
				except:
					Log('vtype: ' + 'kein Video zum m3u8-Streaming gefunden')
					break	# ohne Hinweis überspringen
			else:
				Log('Sendung: unkown Type ' + vtype)	
				Log(" -> PICKED %s", videoURL)
			
			Log('videoURL ' +videoURL)		# OK: nrodl.zdf.de, rodl.zdf.de, geblockt: tvdl.zdf.de
			if videoURL:		# erst master.m3u8 komplett, Auswertung einzelner Auflösungen in VideoParameterAuswahl
				oc.add(DirectoryObject(key=Callback(VideoParameterAuswahl, tassetId=tassetId, videoURL=videoURL, 
					title=ttitle, duration=duration,thumb=thumb, summary=tsummary), title=ttitle, thumb=thumb, 
					summary=tsummary, tagline=tagline))

		elif(typ == 'thema' or typ == 'sendung'):
				oc.add(DirectoryObject(key=Callback(Sendung, title=ttitle, assetId=tassetId), title=ttitle, 
					thumb=thumb, summary=tsummary))
		elif(typ == 'imageseries_informativ'):
				oc.add(PhotoAlbumObject(url=ZDF_BEITRAG % ('bilderserie', tassetId), title=ttitle, 
					summary=tsummary, thumb=thumb))
					
	
	Log(len(oc)); Log(more); Log(offset); Log(maxLength); 
	#Somehow the webservice does not support an offset over 100	
	if more and int(offset) + maxLength <= 100:
		oc.add(NextPageObject(key=Callback(Sendung, title=title, assetId=assetId, offset=str(int(offset)+maxLength)), 
			title=str("Weitere Beiträge").decode('utf-8', 'strict'), summary=None, thumb=R(ICON_MEHR)))
	return oc

#--------------------------------------------------------------------------------------------
@route(PREFIX + '/VideoParameterAuswahl', allow_sync = True)
	# duration für CreateVideoStreamObject nicht benötigt, ev. bei Bedarf für andere Videoformate
def VideoParameterAuswahl(videoURL, title, tassetId, duration, thumb, summary):
	Log('VideoParameterAuswahl:' + videoURL); 
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	oc = home(cont=oc)								# Home-Button

	oc.add(CreateVideoStreamObject(videoURL, title=title, 	# master.m3u8 high
		#summary='automatische Auflösung | funktioniert nicht mit allen Playern', meta='', 
		summary='automatische Auflösung | Auswahl durch den Player', meta='', 
		thumb=thumb, rtmp_live='nein', resolution=''))
	oc = Parseplaylist(oc, videoURL, thumb)	# Einträge für die einzelnen Auflösungen dort zusätzlich zum
											# Eintrag '..automatisch'
	
	stext = 'Rueckmeldung im Plex-Forum willkommen (was läuft womit?)'
	stext = stext.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(OtherSources, tassetId=tassetId, videoURL=videoURL, title=title, 
		duration=duration, thumb=thumb,  summary=summary), title='weitere Videos - nicht alle getestet', 
			summary=stext, thumb=thumb))
	
	Log(len(oc))
	return oc

#--------------------------------------------------------------------------------------------
@route(PREFIX + '/OtherSources', allow_sync = True)	# weitere Videoquellen, neuer XML-Request erforderlich,
													# da das Objekt details in Sendung nicht übergeben werden kann 
def OtherSources(videoURL, tassetId, title, duration, thumb, summary):
	Log('OtherSources:' + videoURL); 
	#oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	#oc = ObjectContainer(title2='weitere Videos - teilweise in Plex nicht lauffaehig', view_group="InfoList")
	oc = ObjectContainer(title2='weitere Videos - nicht alle getestet', view_group="InfoList")
	oc = home(cont=oc)								# Home-Button

	#details = XML.ElementFromURL(ZDF_BEITRAG_DETAILS % tassetId, cacheTime=0)	# Debug 
	details = XML.ElementFromURL(ZDF_BEITRAG_DETAILS % tassetId, cacheTime=CACHE_1HOUR)
	
	try:	#  3GPP-Multimedia								- OK 24.05.2016
		url = details.xpath('//formitaet[@basetype="h264_aac_3gp_http_na_na" and quality="high"]/url')[0].text
		oc.add(CreateVideoClipObject(url=url, title=title, 
			summary='3GPP-Multimedia-Video', meta=url, thumb=thumb, duration=duration, resolution=''))				
	except:
		Log('OtherSources: ' + 'Typ >h264_aac_3gp_http_na_na< nicht vorhanden')
		
	try:	#  RTSP (Real-Time Streaming Protocol)			- 24.05.2016 neg.: VLC, Chrome + Firefox OK (nur direkt)
		url = details.xpath('//formitaet[@basetype="h264_aac_3gp_rtsp_na_na" and quality="high"]/url')[0].text
		oc.add(CreateVideoClipObject(url=url, title=title, 
			summary='RTSP (Real-Time Streaming Protocol)', meta=url, thumb=thumb, duration=duration, resolution=''))			
	except:
		Log('OtherSources: ' + 'Typ >h264_aac_3gp_rtsp_na_na< nicht vorhanden')
		
	# nicht umsetzbar (zur Zeit):
	#	1. HDS: Link führt zu Textdatei *.f4m Video-Url nicht ableitbar
	#		details.xpath('//formitaet[@basetype="h264_aac_f4f_http_f4m_http" and quality="high"]/url')[0].text
		
	#	2. SMIL (Synchronized Multimedia Integration Language) Link führt zu Textdatei *.smil Video-Url nicht ableitbar
	#		details.xpath('//formitaet[@basetype="h264_aac_mp4_rtmp_smil_http" and quality="high"]/url')[0].text
	
	
	try:	#  Metafile-Video mit RTMP-Stream				- OK 24.05.2016
		meta_url = details.xpath('//formitaet[@basetype="h264_aac_mp4_rtmp_zdfmeta_http" and quality="high"]/url')[0].text
		doc =  HTTP.Request(meta_url).content	# Textdatei *.meta laden
		url =  stringextract('<default-stream-url>', '</default-stream-url>', doc)
		oc.add(CreateVideoStreamObject(url=url, title=title, 
			summary='Metafile-Video mit RTMP-Stream', meta=url, thumb=thumb, duration=duration, 
			rtmp_live='nein', resolution=''))			
	except:
		Log('OtherSources: ' + 'Typ >h264_aac_mp4_rtmp_zdfmeta_http< nicht vorhanden')
	
	try:	#  Schleife: Auswertung für hbbtv, progressive, restriction_useragent 
		list = details.xpath('//formitaet[@basetype="h264_aac_mp4_http_na_na" and quality="high"]')
		Log(list)
	except:
		list = None	
	if list:
		for spez in list:
			#Log(HTML.StringFromElement(spez))
			Log(spez.xpath('./facets/facet/text()')[0])
			if spez.xpath('./facets/facet/text()')[0] == "hbbtv":		# neg.: VLC, Chrome + Firefox OK (nur direkt)
				url = spez.xpath('./url')[0].text								
				oc.add(CreateVideoClipObject(url=url, title=title, 
				summary='HbbTV (Hybrid broadcast broadband TV)', meta=url, thumb=thumb, duration=duration, resolution=''))							
			if spez.xpath('./facets/facet/text()')[0] == "progressive":				# OK 24.05.2016 Web + VLC
				url = spez.xpath('./url')[0].text
				oc.add(CreateVideoClipObject(url=url, title=title, 
				summary='H.264 Video - progressive ', meta=url, thumb=thumb, duration=duration, resolution=''))			
			if spez.xpath('./facets/facet/text()')[0] == "restriction_useragent":	# OK 24.05.2016 Web + VLC
				url = spez.xpath('./url')[0].text
				oc.add(CreateVideoClipObject(url=url, title=title, 
				summary='H.264 Video - restriction_useragent', meta=url, thumb=thumb, duration=duration, resolution=''))			
			Log(url)

	try:	#  mov-Videos (Apples QuickTime)					- 25.05.2016 neg.: VLC, Chrome + Firefox OK (nur direkt)
		meta_url = details.xpath('//formitaet[@basetype="h264_aac_mp4_rtsp_mov_http" and quality="high"]/url')[0].text
		doc =  HTTP.Request(meta_url).content	# Textdatei *.mov laden
		pos = doc.find('rtsp://')				# 1. Zeile: RTSPtext, 2. Zeile rtsp-Url 
		url = doc[pos:]
		oc.add(CreateVideoClipObject(url=url, title=title, 
		summary='mov-Videos (Apples QuickTime)', meta=url, thumb=thumb, duration=duration, resolution=''))			
	except:
		Log('OtherSources: ' + 'Typ >h264_aac_mp4_rtsp_mov_http< nicht vorhanden')
 
	try:	#  webm-Videos (Container für Audio + Video im HTML5-Standard)	- 25.05.2016 OK, BubbleUPnP neg.
		url = details.xpath('//formitaet[@basetype="vp8_vorbis_webm_http_na_na" and quality="high"]/url')[0].text
		oc.add(CreateVideoClipObject(url=url, title=title, 
		summary='webm-Videos (Container im HTML5-Standard)', meta=url, thumb=thumb, duration=duration, resolution=''))			
	except:
		Log('OtherSources: ' + 'Typ >vp8_vorbis_webm_http_na_na< nicht vorhanden')
	
	Log('Anzahl Formate: ' + str(len(oc)))							
	if len(oc) == 0:
		summary='zurueck zur Video-Parameter-Auswahl'
		oc.add(DirectoryObject(key=Callback(VideoParameterAuswahl, videoURL=videoURL, details=details, title=title, 
			 duration=duration,thumb=thumb, summary=summary), title=title, thumb=thumb, 
			 summary=summary, tagline='keine weiteren geeignete Videoquellen gefunden'))
			
	return oc

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
#	aktuelle Lösung (ab April 2016):  Sonderbehandlung Arte in Arteplaylists
#  2. Besonderheit: fast identische URL's zu einer Auflösung (...av-p.m3u8, ...av-b.m3u8) Unterschied n.b.
#  3. Besonderheit: für manche Sendungen nur 1 Qual.-Stufe verfügbar (Bsp. Abendschau RBB)

  Log ('Parseplaylist: ' + url_m3u8)
  if url_m3u8.find('http://') == 0:			# URL oder lokale Datei?
	playlist = HTTP.Request(url_m3u8).content  # als Text, nicht als HTML-Element
  else:
	playlist = Resource.Load(url_m3u8) 
	 
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
			if url.find('#') >= 0:	# Bsp. saarl. Rundf.: Kennzeichnung für abgeschalteten Link
				Resolution = 'zur Zeit nicht verfügbar!'
			if Bandwith == BandwithOld:	# Zwilling -Test
				title = 'Bandbreite ' + Bandwith + ' (2. Alternative)'
			if url.startswith('http://') == False:   	# relativer Pfad? 
				pos = url_m3u8.rfind('/')				# m3u8-Dateinamen abschneiden
				url = url_m3u8[0:pos+1] + url 			# Basispfad + relativer Pfad
				
			Log(url); Log(title); Log(thumb); 
			container.add(CreateVideoStreamObject(url=url, title=title, # Einbettung in DirectoryObject zeigt bei
				summary= Resolution, meta=Codecs, thumb=thumb, 			# AllConnect trotzdem nur letzten Eintrag
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
	#	Rückgabe in Liste. Letzter Block reicht bis Ende mString (undefinierte Länge)
	#	Verwendung, wenn xpath nicht funktioniert (Bsp. Tabelle EPG-Daten www.dw.com/de/media-center/live-tv/s-100817)
	rlist = []				
	if 	blockmark == '' or 	mString == '':
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
		.replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", '"'))
	# Log(line_ret)		# bei Bedarf
	return line_ret	
#----------------------------------------------------------------  	
def mystrip(line):	# Ersatz für unzuverlässige strip-Funktion
	line_ret = line	
	line_ret = line.replace('\t', '').replace('\n', '').replace('\r', '')
	line_ret = line_ret.strip()	
	# Log(line_ret)		# bei Bedarf
	return line_ret






