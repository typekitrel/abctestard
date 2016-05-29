# -*- coding: utf-8 -*-
#import lxml.html  	# hier für Konvertierungen - Funktionen von Plex nicht akzeptiert
#import requests	# u.a. Einlesen HTML-Seite, Methode außerhalb Plex-Framework 
import string
import os 			# u.a. Behandlung von Pfadnamen
import re			# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import datetime
import locale

import updater

# locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')	# crasht (Debug-Auszug von Otto Kerner)
# 	locale-Setting erfolgt im Enviroment des Plex-Servers: Bsp. Environment=LANG=en_US.UTF-8 in
# 	plexmediaserver.service (OpenSuse 42.1)

# +++++ ARD Mediathek 2016 Plugin for Plex +++++

VERSION =  '2.1.2'		
VDATE = '29.05.2016'


# (c) 2016 by Roland Scholz, rols1@gmx.de Version
#     Testing Enviroment: 
#		PC: Fujitsu Esprimo E900 8 GB RAM, 3,4 GHz
#		Linux openSUSE 42.1 und Plex-Server 0.9.16.4
#		Tablet Nexus 7, Android 5.1.1,
#		Web-Player: Google-Chrome (alles OK), Firefox (alles OK, Flash-Plugin erforderlich)
#		Videoplayer-Apps: VLC-Player, MXPlayer
#		Streaming-Apps: BubbleUPnP (alle Funktionen OK), AllConnect (keine m3u8-Videos)
# 		Media Player at TV: WD TV Live HD, WDAAP0000NBK, 2012 (nicht alle Auflösungsstufen unterstützt,
#																Vor- und Rückspulen nicht nutzbar)
#
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
# TV-Logos : upload.wikimedia.org

####################################################################################################

# NAME = L('Title')								# s. Strings/en.json
NAME = 'ARD Mediathek 2016'
PREFIX = "/video/ardmediathek2016"

PLAYLIST = 'livesender.xml'					# basiert auf der Channeldatei von gammel, Download:
# http://dl.gmlblog.de/deutschesender.xml. Veröffentlicht: https://gmlblog.de/2013/08/xbmc-tv-livestreams/
ART = 'art.png'								# ARD 
ICON = 'icon.png'							# ARD
ICON_SEARCH = 'icon-search.png'				# gtk themes / Adwaita system-search-symbolic.symbolic.png

ICON_AZ = 'icon-AZ.png'
ICON_CAL = 'icon-calendar.png'				# gnome / Tango x-office-calendar.png
ICON_EINSLIKE = 'icon-Einslike.png'
ICON_SENDER = 'icon-Sender.png' 
ICON_RUBRIKEN = 'icon-Rubriken.png'
ICON_Themen = 'icon-Themen.png'
ICON_MEIST = 'icon-meist.png'

ICON_UPDATER = "icon-updater.png"
ICON_UPDATE_NEW = "icon-update-new.png"
ICON_OK = "icon-ok.png"
ICON_WARNING = "icon-warning.png"
ICON_NEXT = "icon-next.png"
ICON_CANCEL = "icon-error.png"

THUMBNAIL = [									# Vorgaben für THUMBNAILS in ZDF_BEITRAG_DETAILS 
  '946x532',
  '644x363',
  '672x378',
]
ICON_RUBRIKEN
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

ZDF					 = 'http://www.zdf.de/ZDFmediathek/hauptnavigation/startseite?flash=off'	# Mediathek ohne Flash
ZDF_RUBRIKEN         = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/rubriken'
ZDF_THEMEN           = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/themen'
ZDF_MEISTGESEHEN     = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?id=_GLOBAL&maxLength=10&offset=%s'
ZDF_SENDUNGEN_AZ     = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeStart=%s&characterRangeEnd=%s&detailLevel=2'
ZDF_SENDUNG_VERPASST = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?enddate=%s&maxLength=50&startdate=%s&offset=%s'
# Bsp.: http://www.zdf.de/ZDFmediathek/xmlservice/web/sendungVerpasst?enddate=140516&maxLength=50&startdate=140516&offset=0
ZDF_SENDUNG          = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?id=%s&maxLength=25&offset=%s'
ZDF_BEITRAG          = 'http://www.zdf.de/ZDFmediathek/beitrag/%s/%s'
ZDF_BEITRAG_DETAILS = 'http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id=%s'



REPO_NAME = 'Plex-Plugin-ARDMediathek2016'
GITHUB_REPOSITORY = 'rols1/' + REPO_NAME


''' 
####################################################################################################
Live-Sender der Mediathek: | ARD-Alpha | BR |Das Erste | HR | MDR | NDR | RBB | SR | SWR | 
	WDR | tagesschau24 |  | KIKA | PHOENIX | Deutsche Welle
	zusätzlich: Tagesschau | NDR Fernsehen Hamburg, Mecklenburg-Vorpommern, Niedersachsen, Schleswig-Holstein |
	RBB Berlin, Brandenburg | MDR Sachsen-Anhalt, Sachsen, Thüringen

Live-Sender des ZDF: ZDF | ZDFneo | ZDFkultur | ZDFinfo | 3Sat | ARTE

Live-Sender Sonsstige: NRW.TV | Joiz | DAF | N24 | n-tv

Sonderbehandlung im Code für ARTE wegen relativer Links in den m3u8-Dateien

####################################################################################################

Programmpfade:
1. VerpasstWoche -> Wochenliste -> PageControl -> SinglePage
2. SendungenAZ -> AZ-Liste -> SinglePage (Steuerung via next_cbKey) -> PageControl
3. SenderLiveListePre  -> SenderLiveListe -> SenderLiveResolution -> Parseplaylist 
		-> CreateVideoStreamObject
4. Search -> PageControl (Direktsprung mit Suchbegriff) -> SinglePage
5. Einslike -> Rubrik-Liste ("mehr"-Seiten) -> PageControl -> SinglePage

Einzelsendungen:  SinglePage -> get_sendungen -> Parseplaylist: 
		a) für angebotene m3u8-Datei, Auflistung der angebotenen Auflösungen
		b) Auflistung der angebotenen Quali.-Stufen |  a) und b) in gemeinsamer Liste
		-> createVideoClipObject
####################################################################################################
'''

def Start():
	#Log.Debug()  	# definiert in Info.plist
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	#ObjectContainer.art        = R(ART)
	ObjectContainer.art        = R(ICON)  # gefällt mir als Hintergrund besser
	ObjectContainer.title1     = NAME
	ObjectContainer.view_group = "InfoList"

	HTTP.CacheTime = CACHE_1HOUR # Debugging: falls Logdaten ausbleiben, Browserdaten löschen

# handler bindet an das bundle
@route(PREFIX)
@handler(PREFIX, NAME, art = ART, thumb = ICON)
def Main():
	Log('Funktion Main'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	

	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main_ARD, name="ARD Mediathek"), title="ARD Mediathek",
		summary='', tagline='TV', thumb=R('ard.png')))
	oc.add(DirectoryObject(key=Callback(Main_ZDF, name="ZDF Mediathek"), title="ZDF Mediathek", 
		summary='', tagline='TV', thumb=R('zdf.png')))
	oc.add(DirectoryObject(key=Callback(SenderLiveListePre, title='Live-Sender-Vorauswahl'), title='Live-Sender-Vorauswahl',
		summary='', tagline='TV', thumb=R(ICON_SENDER)))

	repo_url = 'https://github.com/{0}/releases/'.format(GITHUB_REPOSITORY)
	oc.add(DirectoryObject(key=Callback(SearchUpdate, title='Plugin-Update'), 
		title='Plugin-Update | akt. Version: ' + VERSION + ', vom ' + VDATE,
		summary='Suche nach neuen Updates starten', tagline='Bezugsquelle: ' + repo_url, thumb=R(ICON_UPDATER)))
		
	return oc	
#---------------------------------------------------------------- 
@route(PREFIX + '/Main_ARD')
def Main_ARD(name):
	Log('Funktion Main_ARD'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	
	
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main),title='Suche: im Suchfeld eingeben', summary='', tagline='TV'))
	oc.add(InputDirectoryObject(key=Callback(Search, s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name), title=" Sendung Verpasst (1 Woche)",
		summary='', tagline='TV', thumb=R(ICON_CAL)))
	oc.add(DirectoryObject(key=Callback(SendungenAZ, name='Sendungen 0-9 | A-Z'), title='Sendungen A-Z',
		summary='', tagline='TV', thumb=R(ICON_AZ)))
	oc.add(DirectoryObject(key=Callback(Einslike, title='Einslike'), title='Einslike',
		summary='', tagline='TV', thumb=R(ICON_EINSLIKE)))
		
	title=name + ' Rubriken' # Übersichtsseite leider nicht kompatibel mit SinglePage -> get_sendungen
	oc.add(DirectoryObject(key=Callback(ARDRubriken, title='Rubriken'), title='Rubriken',
		summary='', tagline='TV', thumb=R(ICON_RUBRIKEN)))
		
	return oc	
#---------------------------------------------------------------- 
@route(PREFIX + '/Main_ZDF')
def Main_ZDF(name):
	Log('Funktion Main_ZDF'); Log(PREFIX); Log(VERSION); Log(VDATE)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art, title1=name)	
	oc.add(DirectoryObject(key=Callback(VerpasstWoche, name=name), title="Sendung Verpasst (1 Woche)",
		thumb=R(ICON_CAL)))
	oc.add(DirectoryObject(key=Callback(ZDFSendungenAZ, name="Sendungen A-Z"), title="Sendungen A-Z",
		thumb=R(ICON_AZ)))
	oc.add(DirectoryObject(key=Callback(RubrikenThemen, auswahl="Rubriken"), title="Rubriken", 
		thumb=R(ICON_RUBRIKEN)))
	oc.add(DirectoryObject(key=Callback(RubrikenThemen, auswahl="Themen"), title="Themen", thumb=R(ICON_Themen)))
	oc.add(DirectoryObject(key=Callback(Sendung, title="Meist Gesehen", assetId="MEISTGESEHEN"), title="Meist Gesehen",
		thumb=R(ICON_MEIST)))
 
	return oc	
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
			thumb = R(ICON_UPDATE_NEW)))
			
		oc.add(DirectoryObject(
			key = Callback(Main), 
			title = 'Update abbrechen',
			summary = 'weiter im aktuellen Plugin',
			thumb = R(ICON_UPDATE_NEW)))
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
					title=title, thumb=ICON))
		else:
			oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=azPath, next_cbKey=next_cbKey), 
					title=title,  thumb=R('ard.png')))
	return oc
   
####################################################################################################
@route(PREFIX + '/Search')	# Suche - Verarbeitung der Eingabe
	# Hinweis zur Suche in der Mediathek: miserabler unscharfer Algorithmus - findet alles mögliche
def Search(query=None, title=L('Search'), s_type='video', offset=0, **kwargs):
	Log('Search'); Log(query)
	
	#if not query:				# leere Eingabe ohne Auswirkung
	#     return NotFound()

	name = 'Suchergebnis zu: ' + query
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
	path =  BASE_URL +  ARD_Suche + query  
	page = HTML.ElementFromURL(path)
	s = XML.StringFromElement(page)
	Log(page)
	
	i = s.find('<h3 class="headline">')
	Log(i)
	if i >= 0:
		return NotFound()
	
	oc = PageControl(title=name, path=path, cbKey=next_cbKey) 	# wir springen direkt
	return oc
	
	err_txt = page.xpath("//h3[@class='headline']/text()")
	Log(err_txt)
   
	try:				# Test auf keine Treffer
		test = page.xpath("//div[@class='box']/h3/text()")
		return NotFound()
	except:					# Treffer
		oc.add(DirectoryObject(key=Callback(PageControl, title=title, path=path, cbKey=next_cbKey), 
				title=title, thumb=ICON))
 
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
				title=title, thumb=ICON))
		else:
			oc.add(DirectoryObject(key=Callback(Sendung, title=title, assetId="VERPASST_"+zdfDate),	  
				title=title, thumb=R('zdf.png')))
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
def Einslike(title):	# Wochenliste zeigen
	title2='Einslike - Videos fuer Musik und Lifestyle in der ARD Mediathek'
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	page = HTML.ElementFromURL(BASE_URL + ARD_Einslike)
	list = page.xpath("//*[@class='more']")
	Log(page); Log(list)
	#next_cbKey = 'PageControl'	# SinglePage zeigt die Sendereihen, PageControl dann die weiteren Seiten
	
	for element in list:	# class='more']
		s = HTML.StringFromElement(element)
		Log(s)
		path = element.xpath("./@href")[0]
		path = BASE_URL + path
		rubrik = element.xpath("./span/text()")[0]	
		rubrik = title + '| ' + rubrik
		Log(path); Log(rubrik)
		oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=rubrik, cbKey=""), title=rubrik, 
			tagline=title2, summary='', thumb='', art=ICON))
		#oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=rubrik, next_cbKey=next_cbKey), title=rubrik, 
		#	tagline=title2, summary='', thumb='', art=ICON))
		
	return oc
	
####################################################################################################
@route(PREFIX + '/ARDRubriken')	# Übersicht Rubriken (16) alle filme, krimi
def ARDRubriken(title):	#
	Log('ARDRubriken');
	title2='Rubriken in der ARD Mediathek'
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	page = HTML.ElementFromURL(ARD_Rubriken)
	next_cbKey = 'SingleSendung'	#
	list = page.xpath("//*[@class='media mediaA']")		
	list = list[1:]										# Rubriken erst ab 2. Element
	Log(page); Log(list)
	
	for element in list:	# [@class='media mediaA'] 
		s = XML.StringFromElement(element)
		Log('element :' + s)
		url = element.xpath("./a/@href")[0]
		headl = url.split('/')[2]			# Rubrikname aus url ermitteln | class="headline" nicht im element
		url = BASE_URL + url
		img_src = img_urlScheme(s, 320) 	# Bsp.: 'urlScheme':'/image/00/34/52/92/68/555337067/16x9/##width##'
		img_alt = element.xpath("./a/noscript/img/@alt")[0]
		Log('url: ' + url); Log('img_src: ' + img_src); Log('img_alt :' + img_alt);  Log('headl :' + headl); 
		oc.add(DirectoryObject(key=Callback(SinglePage, path=url, title=title, next_cbKey=next_cbKey), title=headl, 
			tagline='', summary='', thumb=img_src, art=ICON))		
		
	return oc

####################################################################################################
@route(PREFIX + '/PageControl')	# kontrolliert auf Folgeseiten. Mehrfache Verwendung.
	# Wir laden beim 1. Zugriff alle Seitenverweise in eine Liste. Bei den Folgezugriffen können die Seiten
	# verweise entfallen - der Rückschritt zur Liste ist dem Anwender nach jedem Listenelement  möglich.
	# Dagegen wird in der Mediathek geblättert.
def PageControl(cbKey, title, path, offset=0):  # 
	title1='Folgeseiten: ' + title
	oc = ObjectContainer(view_group="InfoList", title1=title1, title2=title1, art = ObjectContainer.art)
	page = HTML.ElementFromURL(path)
	path_page1 = path							# Pfad der ersten Seite sichern, sonst gehts mit Seite 2 weiter
	
	Log('PageControl'); Log(cbKey); Log(path)
	# doc_txt = lxml.html.tostring(page)			# akzeptiert Plex nicht
	doc_txt = HTML.StringFromElement(page)
	#Log(doc_txt)

	pagenr_suche = re.findall("mresults=page", doc_txt)   
	pagenr_andere = re.findall("mcontents=page", doc_txt)  
	pagenr_einslike = re.findall("mcontent=page", doc_txt)  
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
	if (pagenr_suche) or (pagenr_andere) or (pagenr_einslike) :		# .findall("mresults=page", doc_txt)  		
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

	if  first_site == True:										
		path_page1 = path
		title = 'Weiter zu Seite 1'
		next_cbKey = 'SingleSendung'
		Log(first_site)
		Log(path_page1)
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
			
		Log(s)
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

	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	Log('Funktion SinglePage'); Log(path)
					
	page = HTML.ElementFromURL(path) 	
	
	sendungen = page.xpath("//*[@class='teaser']") # 1 oder mehrere Sendungen
	if not sendungen: 								# für A-Z-Ergebnisse + in Verpasst, 1. Element
		sendungen = page.xpath("//div/div/*[@class='entry']") 
		
	#Log(sendungen)
	send_arr = get_sendungen(oc, sendungen)	# send_arr enthält pro Satz 8 Listen 
	# Rückgabe end_arr = (send_path, send_headline, send_img_src, send_millsec_duration)
	#Log(send_arr); Log('Länge send_arr: ' + str(len(send_arr)))
	send_path = send_arr[0]; send_headline = send_arr[1]; send_subtitel = send_arr[2];
	send_img_src = send_arr[3]; send_img_alt = send_arr[4]; send_millsec_duration = send_arr[5]
	send_dachzeile = send_arr[6]; send_sid = send_arr[7]
	#Log(send_path)
	#Log(send_arr)
	for i in range(len(send_path)):	
		path = send_path[i]
		headline = send_headline[i]
		subtitel = send_subtitel[i]
		img_src = send_img_src[i]
		img_alt = send_img_alt[i]
		millsec_duration = send_millsec_duration[i]
		if not millsec_duration:
			millsec_duration = "leer"
		dachzeile = send_dachzeile[i]
		sid = send_sid[i]
		summary = img_alt
		if dachzeile != "":
			summary = dachzeile + ' | ' + subtitel
		
		Log('path: ' + path); Log(title); Log(headline); Log(img_src); Log(millsec_duration);
		Log('next_cbKey: ' + next_cbKey)
		if next_cbKey == 'SingleSendung':		# Callback verweigert den Funktionsnamen als Variable
			path = BASE_URL + '/play/media/' + sid			# -> *.mp4 (Quali.-Stufen) + master.m3u8-Datei
			oc.add(DirectoryObject(key=Callback(SingleSendung, path=path, title=headline, thumb=img_src, 
				duration=millsec_duration), title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
		if next_cbKey == 'SinglePage':		# Callback verweigert den Funktionsnamen als Variable
			path = BASE_URL + path
			oc.add(DirectoryObject(key=Callback(SinglePage, path=path, title=headline, next_cbKey='SingleSendung'), 
				title=headline, tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
		if next_cbKey == 'PageControl':		# Callback verweigert den Funktionsnamen als Variable
			path = BASE_URL + path
			oc.add(DirectoryObject(key=Callback(PageControl, path=path, title=headline, cbKey=""), title=headline, 
				tagline=subtitel, summary=summary, thumb=img_src, art=ICON))
					
	Log(len(oc))	# Anzahl Einträge					
	return oc

					 		
####################################################################################################
@route(PREFIX + '/SingleSendung')		# einzelne Sendung, path in neuer Mediathekführt zur 
										# Quellenseite (Ausgabe im Textformat)
	# für weitere Infos zur Sendung müsste der Sendungspfad aus SinglePage (hier m3u8-Pfad) zusätzlich
	# mitgeführt und hier übergeben werden. Weitere Infos sind z.B. in <meta name="description" die
	# ausführliche Beschreibung der Sendung. Da Plex nicht über Möglichkeit der ganzeitigen Darstellung
	# verfügt, verzichten wir hier zunächst darauf.
def SingleSendung(path, title, thumb, duration, offset=0):	# -> CreateVideoClipObject
	title = title.decode("utf-8")	 	# ohne: Exception All strings must be XML compatible 

	Log('SingleSendung path: ' + path)
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	# Log(path)
	page = HTTP.Request(path).content  # als Text, nicht als HTML-Element

	link_m3u8 = teilstring(page, 'http', '.m3u8')
	link_img = teilstring(page, 'http://www.ardmediathek.de/image', '\",\"_subtitleUrl')
	link_img = link_img.split('\",\"_subtitleUrl')[0]

	s = page.split('\"_quality\":')
	del s[0]	# 1. Teil entfernen, nicht benötigt
	link_path = []	# List nimmt Pfade und Quali.-Markierung auf
	for i in range(len(s)):
		s1 =  s[i]
		#print s1
		pos = s1.find(',')	# entweder Ziffern 0,1,2,3 oder "auto"
		mark = s1[:pos]
		mark = str(mark)
		
		s2 = teilstring(s1, 'http','.mp4' )
		s2 = mark + '|' + s2			# Markierung + Pfad verbinden (wird später wieder entfernt)
		link_path.append(s2)
		
	del link_path[0]		# 1. Eintrag (auto) entfernen - entspricht link_m3u8
	link_path = list(set(link_path))	# Doppel entfernen (gesehen: 0, 1, 2 doppelt)
	link_path.sort()					# Original: 0,1,2,0,1,2,3


	Log(link_m3u8); Log(link_img); Log(link_path)	
	# *.m3u8-Datei vorhanden -> auswerten, falls ladefähig. die Alternative 'Client wählt selbst' stellen wir voran
	# (WDTV-Live OK, VLC-Player auf Nexus7 'schwerwiegenden Fehler'), MXPlayer läuft dagegen
	if link_m3u8 != '':	  		  								# 
		title = 'Bandbreite und Auflösung automatisch'
		#oc.add(CreateVideoClipObject(url=link_m3u8, title=title, 
		#			summary='funktioniert nicht mit allen Playern', meta=path, thumb=thumb, duration=''))
		Codecs = ''
		oc.add(CreateVideoStreamObject(url=link_m3u8, title=title, rtmp_live='nein',
			summary='funktioniert nicht mit allen Playern', meta=Codecs, thumb=thumb))

		cont = Parseplaylist(oc, link_m3u8, thumb)	# Einträge für die einzelnen Auflösungen dort zusätzlich zum
		Log(cont)  									# Eintrag '..automatisch'

	# im alten Mediathekformat gab es zu einer Sendung unterschiedliche Qualitätsstufen und häufig zusätzlich
	# eine *.m3u8-Datei.
	# Im neuen Format ist eine weitere Datei (Textformat) einzulesen, die im Listenformat sowohl den Link
	# zu einer  *.m3u8-Datei als auch die direkten Links zu .mp4-Videos verschiedener Quali.-Stufen enthält.
	# Bei letzteren erfolgt die Transcodierung durch Plex-Server (falls direkte Wiedergabe abgeschaltet)
	 
	#description = ...  # bisher nicht verwendet, kein passender key im Videoobjekt

	href_quality_S 	= ''; href_quality_M 	= ''; href_quality_L 	= ''; href_quality_XL 	= ''
	for i in range(len(link_path)):
		s = link_path[i]	# Format: 0|http://mvideos.daserste.de/videoportal/Film/c_610000/611560/format706220.mp4
		if s[0:1] == "0":			
			href_quality_S = s[2:]
		if s[0:1] == "1":			
			href_quality_M = s[2:]
		if s[0:1] == "2":			
			href_quality_L = s[2:]
		if s[0:1] == "3":			
			href_quality_XL = s[2:]
	
	Log(duration); Log(href_quality_S); Log(href_quality_M); Log(href_quality_L);  Log(href_quality_XL)
	if href_quality_XL:
		title = 'Qualität EXTRALARGE'
		oc.add(CreateVideoClipObject(url=href_quality_XL, title=title, 
		summary="", meta=path, thumb=thumb, duration=duration))		# summary leer (Übersichtlichkeit)
	if href_quality_L:
		title = 'Qualität LARGE'
		oc.add(CreateVideoClipObject(url=href_quality_L, title=title, 
		summary="", meta=path, thumb=thumb, duration=duration))
	if href_quality_M:
		title = 'Qualität MEDIUM'
		oc.add(CreateVideoClipObject(url=href_quality_M, title=title, 
		summary="", meta=path, thumb=thumb, duration=duration))
	if href_quality_S:
		title = 'Qualität SMALL'
		oc.add(CreateVideoClipObject(url=href_quality_S, title=title, 
		summary="", meta=path, thumb=thumb, duration=duration))		
	return oc
	
####################################################################################################
def get_sendungen(container, sendungen): # Sendungen ausgeschnitten mit class='teaser', aus Verpasst + A-Z,
	# 										Suche, Einslike
	# Headline + Subtitel sind nicht via xpath erreichbar, daher Stringsuche:
	# ohne linklist + Subtitel weiter (teaser Seitenfang od. Verweis auf Serie, bei A-Z teaser-Satz fast identisch,
	#	nur linklist fehlt )
	# Die Rückgabe-Liste send_arr nimmt die Datensätze auf (path, headline usw.)
	
	Log('get_sendungen')
	# send_arr nimmt die folgenden Listen auf (je 1 Datensatz pro Sendung)
	send_path = []; send_headline = []; send_subtitel = []; send_img_src = [];
	send_img_alt = []; send_millsec_duration = []; send_dachzeile = []; send_sid = []; 
	arr_ind = 0
	img_alt = ""	# fehlt manchmal
	for sendung in sendungen:					 
		#s = lxml.html.tostring(sendung)
		s = XML.StringFromElement(sendung)	# XML.StringFromElement Plex-Framework
		# Log(s)							# umfangreiche Ausgabe (nur bei Bedarf)						
		if s.find('<div class="linklist">') == -1 and s.find('subtitle') >= 0: 
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
			subtitel = re.search("<p class=\"subtitle\">(.*?)</p>\s+?", s)	# Bsp. <p class="subtitle">25 Min.</p>
			subtitel = subtitel.group(1)
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
				Log('xpath-Fehler in Liste class=teaserbox, sendung: ' + s )
		
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
def CreateVideoClipObject(url, title, summary, meta, thumb, duration,include_container=False, **kwargs):
	#title = title.encode("utf-8")		# ev. für alle ausgelesenen Details erforderlich
	Log('CreateVideoClipObject')
	Log(url); Log(duration); 

 
	videoclip_obj = VideoClipObject(
	key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary,
		meta=meta, thumb=thumb, duration=duration, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		thumb = thumb,
		items = [
			MediaObject(
				parts = [
					PartObject(key=url)
					# PartObject(key=Callback(PlayVideo, url=url, resolution=resolution)) # s.u., verzichtbar
				],
				container = Container.MP4,  	# weitere Video-Details für Chrome nicht erf., aber Firefox 
				video_codec = VideoCodec.H264,	# benötigt VideoCodec + AudioCodec zur Audiowiedergabe
				audio_codec = AudioCodec.AAC,	# 
				
			)  									# <- for resolution in [720, 540, 480] (in PlayVideo übergeben)
	])

	if include_container:						# Abfrage anscheinend verzichtbar, schadet aber auch nicht 
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj
	
#####################################################################################################
@route(PREFIX + '/SenderLiveListePre')	# LiveListe Vorauswahl - verwendet lokale Playlist
def SenderLiveListePre(title, offset=0):	# Vorauswahl: ARD, ZDF, Sonstige
	Log.Debug('SenderLiveListePre')
	playlist = Resource.Load(PLAYLIST)	# lokale XML-Datei (Pluginverz./Resources)
	#Log(playlist)	#

	oc = ObjectContainer(view_group="InfoList", title1='Live-Sender-Vorauswahl', title2=title, art = ICON)
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>	
	liste = doc.xpath('//channels/channel')
	Log(liste)
	
	for element in liste:
		element_str = HTML.StringFromElement(element)
		name = stringextract('<name>', '</name>', element_str)
		img = stringextract('<thumbnail>', '</thumbnail>', element_str) # channel-thumbnail in playlist
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
		Log(element_str); Log(name); Log(img);
		oc.add(DirectoryObject(key=Callback(SenderLiveListe, title=name, listname=name),
			title='Live-Sender: ' + name, thumb=img, tagline=''))
			
	return oc
#-----------------------------------------------------------------------------------------------------
@route(PREFIX + '/SenderLiveListe')	# LiveListe - verwendet lokale Playlist
def SenderLiveListe(title, listname, offset=0):	# 
	# SenderLiveListe -> SenderLiveResolution (reicht nur durch) -> Parseplaylist (Ausw. m3u8)
	#	-> CreateVideoStreamObject 
	Log.Debug('SenderLiveListe')

	oc = ObjectContainer(view_group="InfoList", title1='Live-Sender', title2='Live-Sender ' + title, art = ICON)
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
	Log(liste); Log(element_str)

	# Besonderheit: die Senderliste wird lokal geladen (s.o.). Über den link wird die URL zur  
	#	*.m3u8 geholt. Nach Anwahl eines Live-Senders erfolgt in SenderLiveResolution die Listung
	#	der Auflösungsstufen.
	#
	i = 0		# Debug-Zähler
	for element in liste:
		Log(HTML.StringFromElement(element))		# Ergebnis wie XMML.StringFromElement
		#title = element.xpath("./title/text()")	# xpath arbeitet fehlerhaft bei Sonderzeichen (z.B. in URL)
		#link =  element.xpath("./link/text()")		
		element_str = HTML.StringFromElement(element)
		link = stringextract('<link>', '<thumbnail>', element_str) 	# HTML.StringFromElement unterschlägt </link>
		link = link.strip()							# \r + Leerz. am Ende entfernen
		#link = link.replace('amp;', len(link))		# replace verweigert solche Strings, daher -> 	repl_char
		link = repl_char('amp;',link)				# amp; entfernen! Herkunft: HTML.ElementFromString bei &-Zeichen
		Log(link)
									
		title = stringextract('<title>', '</title>', element_str)
		title = transl_umlaute(title)	# DirectoryObject verträgt keine Umlaute
				
		img = stringextract('<thumbnail>', '</thumbnail>', element_str) 
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
		
		Log(title); Log(link); Log(img); Log(i)
		#img = ""		# Senderlogos lassen wir wg. fehlender Skalierungsmöglichkeit weg
		Resolution = ""; Codecs = ""; duration = ""
		i = i +1	
		#if link.find('rtmp') == 0:				# rtmp-Streaming s. CreateVideoStreamObject

        # Link zu master.m3u8 erst auf Folgeseite? - SenderLiveResolution reicht an  Parseplaylist durch  
		oc.add(DirectoryObject(key=Callback(SenderLiveResolution, path=link, title=title, thumb=img),
			title=title, thumb=img, tagline=''))

	Log(len(oc))
	return oc
	
###################################################################################################
@route(PREFIX + '/SenderLiveResolution')	# Auswahl der Auflösungstufen des Livesenders
	#	Die URL der gewählten Auflösung führt zu weiterer m3u8-Datei (*.m3u8), die Links zu den 
	#	Videosegmenten (.ts-Files enthält). Diese  verarbeitet der Plexserver im Videoobject. 
def SenderLiveResolution(path, title, thumb, include_container=False):
	#page = HTML.ElementFromURL(path)
	url_m3u8 = path
	Log(title); Log(url_m3u8);

	oc = ObjectContainer(view_group="InfoList", title1=title + ' Live', art=ICON)
	Codecs = ''										
	if title.find('Arte') >= 0:
		Log('Arte-Stream gefunden')			
		oc = Arteplaylist(oc, url_m3u8, title, thumb)	# Auswertung Arte-Parameter rtmp- + hls-streaming
		Log(len(oc))
		return oc
		
	if url_m3u8.find('rtmp') == 0:		# hier noch flash-Infos auswerten
		oc.add(CreateVideoStreamObject(url=url_m3u8, title=title, 
			summary='', meta=Codecs, thumb=thumb, rtmp_live='ja'))
		return oc
		
	# alle übrigen (i.d.R. http-Links)
	oc.add(CreateVideoStreamObject(url=url_m3u8, title=title + ' | Bandbreite und Auflösung automatisch', 
		summary='funktioniert nicht mit allen Playern', meta=Codecs, thumb=thumb, rtmp_live='nein'))
	# Auslösungsstufen (bei relativen Pfaden nutzlos):
	oc = Parseplaylist(oc, url_m3u8, thumb)	# Auswertung *.m3u8-Datei, Auffüllung Container mit Auflösungen
	return oc								# (-> CreateVideoStreamObject pro Auflösungstufe)

####################################################################################################
@route(PREFIX + '/Arteplaylist')	# Auswertung Arte-Parameter rtmp- + hls-streaming
	# Die unter  https://api.arte.tv/api/player/v1/livestream/de?autostart=1 ausgelieferte Textdatei
	# 	enthält je 2 rtmp-Url und 2 hls-Url
def Arteplaylist(oc, url, title, thumb):
	Log('Arteplaylist')
	playlist = HTTP.Request(url).content  # als Text, nicht als HTML-Element
	#rtmp1_list = playlist.split("RTMP_EQ_1")
	rtmp1_list = stringextract('\"RTMP_EQ_1\":', '\"RTMP_EQ_2\":', playlist) # orig.: "HLS_EQ_1":
	rtmp2_list = stringextract('\"RTMP_EQ_2\":', '\"HLS_EQ_1\":', playlist)
	hls1_list = stringextract('\"HLS_EQ_1\":', '\"HLS_EQ_2\":', playlist)
	hls2_list = stringextract('\"HLS_EQ_2\":', '\"tracking\":', playlist) 
	Log(rtmp1_list)
	
	r1 = stringextract('\"streamer\": \"', '\",',  rtmp1_list)  # rtmp-Url verteilt auf 2 Zeilen
	r2 = stringextract('\"url\": \"', '\",',  rtmp1_list)
	rtmp1_url = r1 + r2 
	rtmp1_url = repl_char('\\', rtmp1_url)	# Quotierung für Slashes entfernen
	
	r1 = stringextract('\"streamer\": \"', '\",',  rtmp2_list)  # 2. rtmp-Url
	r2 = stringextract('\"url\": \"', '\",',  rtmp2_list)
	rtmp2_url = r1 + r2 
	rtmp2_url = repl_char('\\', rtmp2_url)	# Quotierung für Slashes entfernen
	
	r1 = stringextract('\"url\": \"', '\",',  hls1_list)  # hls-Url nur in 1 Zeile (m3u8-Url)
	r2 = stringextract('\"url\": \"', '\",',  hls2_list)  # hls-Url nur in 1 Zeile (m3u8-Url)
	hls1_url = repl_char('\\', r1)	# Quotierung für Slashes entfernen
	hls2_url = repl_char('\\', r2)		
	
	oc.add(CreateVideoStreamObject(url=rtmp1_url, title=title + ' (de) | rtmp', 	# weniger stabil als HLS
		summary='RTMP-Streaming deutsch', meta='', thumb=thumb, rtmp_live='ja'))
	oc.add(CreateVideoStreamObject(url=rtmp2_url, title=title + ' (fr) | rtmp', 	# weniger stabil als HLS
		summary='RTMP-Streaming französisch', meta='', thumb=thumb, rtmp_live='ja'))
	oc.add(CreateVideoStreamObject(url=hls1_url, title=title + ' (de) | http', 
		summary='HLS-Streaming deutsch', meta='', thumb=thumb, rtmp_live='nein'))
	oc.add(CreateVideoStreamObject(url=hls2_url, title=title + ' (fr) | http', 
		summary='HLS-Streaming französisch', meta='', thumb=thumb, rtmp_live='nein'))
	
	Log(rtmp1_url); Log(rtmp2_url); Log(hls1_url); Log(hls2_url); Log(len(oc))
	return oc

####################################################################################################
@route(PREFIX + '/CreateVideoStreamObject')	# <- LiveListe, SingleSendung (nur m3u8-Dateien)
											# **kwargs - s. CreateVideoClipObject
def CreateVideoStreamObject(url, title, summary, meta, thumb, rtmp_live, include_container=False, **kwargs):
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
  
  #	resolution = [720, 540, 480] # Parameter bei Livestream nicht akzeptiert +  auch nicht nötig
  # rtmp_live: Steuerung via False/True nicht möglich. Bei zweiten Durchlauf gehen Bool-Parameter verloren
	
	Log('CreateVideoStreamObject: ' + url); Log('rtmp_live: ' + rtmp_live) 
	if url.find('rtmp:') >= 0:	# rtmp = Protokoll für flash, rtmpdump ermittelt Quellen
		#mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url,live=True))]) # live=True nur Streaming
		if rtmp_live == 'ja':
			Log('rtmp_live: ' + rtmp_live) 
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url,live=True))])
			rating_key = title
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, 
				meta=meta, thumb=thumb, rtmp_live='ja', include_container=True), 
				rating_key=title,
				title=title,
				summary=summary,
				thumb=thumb,)  
		else:
			mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url))])
			rating_key = title
			videoclip_obj = VideoClipObject(
				key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, 
				meta=meta, thumb=thumb, rtmp_live='nein', include_container=True), 
				rating_key=title,
				title=title,
				summary=summary,
				thumb=thumb,) 			 

	else:
		# Auslösungsstufen weglassen? (bei relativen Pfaden nutzlos) 
		# Auflösungsstufen - s. SenderLiveResolution -> Parseplaylist
		mo = MediaObject(parts=[PartObject(key=HTTPLiveStreamURL(url=url))]) 
		rating_key = title
		videoclip_obj = VideoClipObject(
			key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,
			meta=meta, thumb=thumb, rtmp_live=rtmp_live, include_container=True), 
			rating_key=title,
			title=title,
			summary=summary,
			thumb=thumb,)
			
	videoclip_obj.add(mo)

	Log(url); Log(title); Log(summary); Log(meta); Log(thumb); 
	Log(rating_key);  
	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

	return oc

# PlayVideo: .m3u8 wurde in Route als fehlend bemängelt, wird aber als Attribut der Funktion nicht 
#	akzeptiert - Ursache nicht gefunden. 
#	Routine ab 03.04.2016 entbehrlich - s.o.
@route(PREFIX + '/PlayVideo')  
def PlayVideo(url):		# resolution übergeben, falls im  videoclip_obj verwendet
	Log('PlayVideo')  		
	HTTP.Request(url).content
	return Redirect(url)

####################################################################################################
#									ZDF-Funktionen
#
@route(PREFIX + '/ZDFSendungenAZ')
def ZDFSendungenAZ(name):
	Log('ZDFSendungenAZ')
	oc = ObjectContainer(title2=name, view_group="List")

	# A to Z
	for page in SENDUNGENAZ:
		oc.add(DirectoryObject(key=Callback(SendungenAZList, char=page[0]), title=page[0], thumb=R('zdf.png')))
	return oc

####################################################################################################
@route(PREFIX + '/RubrikenThemen')
def RubrikenThemen(auswahl):
	#auswahl = 'Rubriken'
	Log.Debug('RubrikenThemen: ' + auswahl)
	oc = ObjectContainer(title2='ZDF: ' + auswahl, view_group="List")
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
  
	if len(oc) == 0:
		return MessageContainer("Empty", "There aren't any speakers whose name starts with " + char)

	return oc
  
####################################################################################################
@route(PREFIX + '/Sendung/{assetId}', allow_sync = True)
def Sendung(title, assetId, offset=0):
	Log('Sendung: ' + title); Log(assetId); Log(offset);
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	if(assetId == 'MEISTGESEHEN'):
		maxLength = 25	# vormals 10
		content = XML.ElementFromURL(ZDF_MEISTGESEHEN % (offset), cacheTime=CACHE_1HOUR)
		#content = XML.ElementFromURL(ZDF_MEISTGESEHEN % (offset), cacheTime=0)	# Debug
	elif(assetId.find('VERPASST_') != -1):
		maxLength = 50
		Log(maxLength); 
		d = re.search('VERPASST_([0-9]{1,6})', assetId)
		#if(d == None):
		#  return oc
		day = d.group(1)
		content = XML.ElementFromURL(ZDF_SENDUNG_VERPASST % (day, day, offset), cacheTime=CACHE_1HOUR)
		#content = XML.ElementFromURL(ZDF_SENDUNG_VERPASST % (day, day, offset), cacheTime=0)	# Debug
	else:
		maxLength = 25
		content = XML.ElementFromURL(ZDF_SENDUNG % (str(assetId), offset), cacheTime=CACHE_1HOUR)
		#content = XML.ElementFromURL(ZDF_SENDUNG % (str(assetId), offset), cacheTime=0)	# Debug
	Log(assetId);  Log(content); 

	more = content.xpath('//teaserlist/additionalTeaser')[0].text == 'true'
	teasers = content.xpath('//teaserlist/teasers/teaser')
	Log(more); Log(teasers)
	for teaser in teasers:
		Log('teaser: '); Log(teaser)
		typ = teaser.xpath('./type')[0].text
		for res in THUMBNAIL:
			thumb = teaser.xpath('./teaserimages/teaserimage[@key="%s"]' % (res))[0].text
			if thumb.find('fallback') == -1:
				break

		ttitle = teaser.xpath('./information/title')[0].text	
		tsummary = teaser.xpath('./information/detail')[0].text
		tassetId = teaser.xpath('./details/assetId')[0].text
		Log(typ); Log(ttitle); Log(tsummary); Log(tassetId);	
		
		'''			
		Problematik Video-URL:
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

			#date = Datetime.ParseDate(teaser.xpath('./details/airtime')[0].text).date()
			airtime = teaser.xpath('./details/onlineairtime')[0].text
			date = Datetime.ParseDate(airtime)
			lengthSec = teaser.xpath('./details/lengthSec')[0].text
			minutes = int(lengthSec) / 60
			if minutes >= 1:
				dauer = 'Dauer: ' + str(minutes) + ' min'
			else:
				dauer = 'Dauer: ' + str(lengthSec) + ' sec'
			tagline = airtime + ' | ' + dauer
			duration = CalculateDuration(teaser.xpath('./details/length')[0].text)
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
				Log('PlayVideo: unkown Type ' + vtype)	
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
			title=str("Weitere Beiträge").decode('utf-8', 'strict'), summary=None, thumb="more.png"))
	return oc

#--------------------------------------------------------------------------------------------
@route(PREFIX + '/VideoParameterAuswahl', allow_sync = True)
	# duration für CreateVideoStreamObject nicht benötigt, ev. bei Bedarf für andere Videoformate
def VideoParameterAuswahl(videoURL, title, tassetId, duration, thumb, summary):
	Log('VideoParameterAuswahl:' + videoURL); 
	oc = ObjectContainer(title2=title.decode(encoding="utf-8", errors="ignore"), view_group="InfoList")
	oc.add(CreateVideoStreamObject(videoURL, title=title, 	# master.m3u8 high
		summary='automatische Auflösung | funktioniert nicht mit allen Playern', meta='', thumb=thumb, rtmp_live='nein'))
	oc = Parseplaylist(oc, videoURL, thumb)	# Einträge für die einzelnen Auflösungen dort zusätzlich zum
											# Eintrag '..automatisch'
	oc.add(DirectoryObject(key=Callback(OtherSources, tassetId=tassetId, videoURL=videoURL, title=title, 
		duration=duration, thumb=thumb,  summary=summary), title='weitere Videos - nicht alle getestet', 
			 summary='Rueckmeldung im Plex-Forum willkommen', thumb=thumb))
	
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
	#details = XML.ElementFromURL(ZDF_BEITRAG_DETAILS % tassetId, cacheTime=0)	# Debug 
	details = XML.ElementFromURL(ZDF_BEITRAG_DETAILS % tassetId, cacheTime=CACHE_1HOUR)
	
	try:	#  3GPP-Multimedia								- OK 24.05.2016
		url = details.xpath('//formitaet[@basetype="h264_aac_3gp_http_na_na" and quality="high"]/url')[0].text
		oc.add(CreateVideoClipObject(url=url, title=title, 
		summary='3GPP-Multimedia-Video', meta=url, thumb=thumb, duration=duration))				
	except:
		Log('OtherSources: ' + 'Typ >h264_aac_3gp_http_na_na< nicht vorhanden')
		
	try:	#  RTSP (Real-Time Streaming Protocol)			- 24.05.2016 neg.: VLC, Chrome + Firefox OK (nur direkt)
		url = details.xpath('//formitaet[@basetype="h264_aac_3gp_rtsp_na_na" and quality="high"]/url')[0].text
		oc.add(CreateVideoClipObject(url=url, title=title, 
		summary='RTSP (Real-Time Streaming Protocol)', meta=url, thumb=thumb, duration=duration))			
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
		summary='Metafile-Video mit RTMP-Stream', meta=url, thumb=thumb, duration=duration, rtmp_live='nein'))			
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
				summary='HbbTV (Hybrid broadcast broadband TV)', meta=url, thumb=thumb, duration=duration))							
			if spez.xpath('./facets/facet/text()')[0] == "progressive":				# OK 24.05.2016 Web + VLC
				url = spez.xpath('./url')[0].text
				oc.add(CreateVideoClipObject(url=url, title=title, 
				summary='H.264 Video - progressive ', meta=url, thumb=thumb, duration=duration))			
			if spez.xpath('./facets/facet/text()')[0] == "restriction_useragent":	# OK 24.05.2016 Web + VLC
				url = spez.xpath('./url')[0].text
				oc.add(CreateVideoClipObject(url=url, title=title, 
				summary='H.264 Video - restriction_useragent', meta=url, thumb=thumb, duration=duration))			
			Log(url)

	try:	#  mov-Videos (Apples QuickTime)					- 25.05.2016 neg.: VLC, Chrome + Firefox OK (nur direkt)
		meta_url = details.xpath('//formitaet[@basetype="h264_aac_mp4_rtsp_mov_http" and quality="high"]/url')[0].text
		doc =  HTTP.Request(meta_url).content	# Textdatei *.mov laden
		pos = doc.find('rtsp://')				# 1. Zeile: RTSPtext, 2. Zeile rtsp-Url 
		url = doc[pos:]
		oc.add(CreateVideoClipObject(url=url, title=title, 
		summary='mov-Videos (Apples QuickTime)', meta=url, thumb=thumb, duration=duration))			
	except:
		Log('OtherSources: ' + 'Typ >h264_aac_mp4_rtsp_mov_http< nicht vorhanden')
 
	try:	#  webm-Videos (Container für Audio + Video im HTML5-Standard)	- 25.05.2016 OK, BubbleUPnP neg.
		url = details.xpath('//formitaet[@basetype="vp8_vorbis_webm_http_na_na" and quality="high"]/url')[0].text
		#oc.add(CreateVideoStreamObject(url=url, title=title, 
		#summary='webm-Videos (Container im HTML5-Standard)', meta=url, thumb=thumb, duration=duration, rtmp_live='nein'))			
		oc.add(CreateVideoClipObject(url=url, title=title, 
		summary='webm-Videos (Container im HTML5-Standard)', meta=url, thumb=thumb, duration=duration))			
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

  Log(url_m3u8)
  playlist = HTTP.Request(url_m3u8).content  # als Text, nicht als HTML-Element
  lines = playlist.splitlines()
  #Log(lines)
  lines.pop(0)		# 1. Zeile entfernen (#EXTM3U)
  BandwithOld = ''	# für Zwilling -Test (manchmal 2 URL für 1 Bandbreite + Auflösung) 
  i = 0
  #for line in lines[1::2]:	# Start 1. Element, step 2
  for line in lines:	
 	line = lines[i].strip()
 	Log(line)
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
				summary= Resolution, meta=Codecs, thumb=thumb, rtmp_live='nein'))# AllConnect trotzdem nur letzten Eintrag
			BandwithOld = Bandwith
				
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
def NotFound():
    return ObjectContainer(
        header=u'%s' % L('Error'),
        message=u'%s' % L('No entries found')
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
def stringextract(mFirstChar, mSecondChar, mString):  # extrahiert Zeichenkette zwischen 1. + 2. Zeichenkette
	pos1 = mString.find(mFirstChar)
	ind = len(mFirstChar)
	pos2 = mString.find(mSecondChar, pos1 + ind+1)
	rString = "leer"

	if pos1 and pos2:
		rString = mString[pos1+ind:pos2]	# extrahieren 
		
	#Log(mString); Log(mFirstChar); Log(mSecondChar); 
	#Log(pos1); Log(ind); Log(pos2);  Log(rString); 
	return rString
#----------------------------------------------------------------  
def teilstring(zeile, startmarker, endmarker):  # in init ändern!
  # die übergebenen Marker bleiben Bestandteile der Rückgabe (werden nicht abgeschnitten)
  # content = XML.StringFromElement(page)  - entfällt
  pos2 = zeile.find(endmarker, 0)
  pos1 = zeile.rfind(startmarker, 0, pos2)
  #print pos2; print pos1
  if pos1 & pos2:
    teils = zeile[pos1:pos2+len(endmarker)]	# Versatz +5 schneidet die begrenzenden Suchstellen ab 
  else:
    teils = ''
  #Log(pos1) Log(pos2) Log(len(href)) Log(href)
  return teils
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
	line_ret = line	
	pos = line_ret.find(cut_char)
	while pos > 0:
		line_l = line_ret[0:pos]
		line_r = line_ret[pos+len(cut_char):]
		line_ret = line_l + line_r
		pos = line_ret.find(cut_char)
		#Log(cut_char); Log(pos); Log(line_l); Log(line_r); Log(line_ret)		
	return line_ret










