# -*- coding: utf-8 -*-
#import lxml.html  	# hier für Konvertierungen - Funktionen von Plex nicht akzeptiert
#import requests	# u.a. Einlesen HTML-Seite, Methode außerhalb Plex-Framework 
import string
import os 			# u.a. Behandlung von Pfadnamen
import re			# u.a. Reguläre Ausdrücke in CalculateDuration
import datetime
import locale

# locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')	# crasht (Debug-Auszug von Otto Kerner)
# 	locale-Setting erfolgt im Enviroment des Plex-Servers: Bsp. Environment=LANG=en_US.UTF-8 in
# 	plexmediaserver.service (OpenSuse 42.1)

# +++++ ARD Mediathek 2016 Plugin for Plex +++++
# 
# Version 1,2	Stand 27.04.2016
#
# (c) 2016 by Roland Scholz, rols1@gmx.de 
#     Testing Enviroment: 
#		PC: Fujitsu Esprimo E900 8 GB RAM, 3,4 GHz
#		Linux openSUSE 42.1 und Plex-Server 0.9.16.4
#		Tablet Nexus 7, Android 5.1.1,
#		Web-Player: Google-Chrome (alles OK), Firefox (alles OK, Flash-Plugin erforderlich)
#		Videoplayer-Apps: VLC-Player, MXPlayer
#		Streaming-Apps: BubbleUPnP (alle Funktionen OK), AllConnect (keine m3u8-Videos)
# 		Media Player at TV: WD TV Live HD, WDAAP0000NBK, 2012 (nicht alle Auflösungsstufen unterstützt)
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

####################################################################################################

#NAME = 'ARD Mediathek 2016'	# s. Strings/en.json

NAME = L('Title')

PLAYLIST = 'livesender.xml'					# basiert auf der Channeldatei von gammel, Download:
# http://dl.gmlblog.de/deutschesender.xml. Veröffentlicht: https://gmlblog.de/2013/08/xbmc-tv-livestreams/
ART = 'art.png'
ICON = 'icon.png'
SICON = 'search.png'
BASE_URL = 'http://www.ardmediathek.de'

ARD_VERPASST = '/tv/sendungVerpasst?tag='		# ergänzt mit 0, 1, 2 usw.
ARD_AZ = '/tv/sendungen-a-z?buchstabe='			# ergänzt mit 0-9, A, B, usw.
ARD_Suche = '/tv/suche?searchText='				# ergänzt mit Suchbegriff
ARD_Live = '/tv/live'

''' 
# Hartkodierte Links für Arte (Parseplaylist)- die relativen Links der *.m3u8-Datei verursachen Rekursion
# z.Z. nicht verwendet, da auch diese relative Links enthalten
Arte_delive = 'http://delive.artestras.cshls.lldns.net/artestras/contrib/delive.m3u8'  # entspr. master.m3u8
Arte_150 = 'http://delive.artestras.cshls.lldns.net/artestras/contrib/delive/delive_150.m3u8'
Arte_315 = 'http://delive.artestras.cshls.lldns.net/artestras/contrib/delive/delive_315.m3u8'
Arte_540 = 'http://delive.artestras.cshls.lldns.net/artestras/contrib/delive/delive_540.m3u8'
Arte_925 = 'http://delive.artestras.cshls.lldns.net/artestras/contrib/delive/delive_925.m3u8'

Live-Sender der Mediathek: | ARD-Alpha | BR |Das Erste | HR | MDR | NDR | RBB | SR | SWR | 
	WDR | tagesschau24 | 3Sat | KIKA | PHOENIX

zusätzlich: Tagesschau | NDR Fernsehen Hamburg, Mecklenburg-Vorpommern, Niedersachsen, Schleswig-Holstein | 
	RBB Berlin, Brandenburg | MDR Sachsen-Anhalt, Sachsen, Thüringen |
	ZDF ZDFneo ZDFkultur ZDFinfo

Nicht kompatibel: ARTE	
''' 
####################################################################################################
''' 
Programmpfade:
1. VerpasstWoche -> SinglePage -> get_sendungen -> PageControl -> SingleSendung:
		a) Parseplaylist - für angebotene m3u8-Datei, Auflistung der angebotenen Auflösungen
		b) Auflistung der angebotenen Quali.-Stufen |  a) und b) in gemeinsamer Liste
		-> createVideoClipObject 
2. SendungenAZ -> SinglePage (zeigt die Sendereihen, dann PageControl weiteren Seiten)
3. SenderLiveListe -> SenderLiveResolution -> Parseplaylist -> CreateVideoStreamObject
4. Search -> PageControl -> ... wie VerpasstWoche
'''
####################################################################################################

def Start():
    #Log.Debug()  	# definiert in Info.plist
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

#   ObjectContainer.art        = R(ART)
    ObjectContainer.art        = R(ICON)  # gefällt mir als Hintergrund besser
    ObjectContainer.title1     = NAME
    ObjectContainer.view_group = "InfoList"

#   HTTP.CacheTime = CACHE_1HOUR	
    HTTP.CacheTime = 0			# Debug
 
# handler bindet an das bundle
@handler('/video/ardmediathek2016', NAME, art = ART, thumb = ICON)
def Main():
    oc = ObjectContainer(view_group="List", art=ObjectContainer.art)	
    # folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
    oc.add(DirectoryObject(key=Callback(Main),title='Suche: im Suchfeld eingeben', summary='', tagline='TV'))
    oc.add(InputDirectoryObject(key=Callback(Search, s_type='video', title=u'%s' % L('Search Video')),
     	title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=SICON))
    oc.add(DirectoryObject(key=Callback(VerpasstWoche, name="Sendung Verpasst"), title="Sendung Verpasst (1 Woche)",
    	summary='', tagline='TV'))
    oc.add(DirectoryObject(key=Callback(SendungenAZ, name='Sendungen 0-9 | A-Z'), title='Sendungen A-Z',
    	summary='', tagline='TV'))   
    path = BASE_URL + ARD_Live	
    oc.add(DirectoryObject(key=Callback(SenderLiveListe, title='Live-Sender'), title='Live-Sender',
    	summary='', tagline='TV'))   
      
#   Log('Funktion Main')
    return oc

#----------------------------------------------------------------  

####################################################################################################
@route('/video/ardmediathek2016/SendungenAZ')
def SendungenAZ(name):		# Auflistung 0-9 (1 Eintrag), A-Z (einzeln) 
	Log('SendungenAZ')
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	azlist = list(string.ascii_uppercase)
	azlist.append('0-9')
	#next_cbKey = 'SinglePage'	# 
	next_cbKey = 'PageControl'	# SinglePage zeigt die Sendereihen, PageControl dann die weiteren Seiten

	for element in azlist:
		Log(element)
		azPath = BASE_URL + ARD_AZ + element
		button = element
		title = "Sendungen mit " + button
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=azPath, next_cbKey=next_cbKey), 
				title=title, thumb=ICON))
	return oc
   
####################################################################################################
# Hinweis zur Suche in der Mediathek: miserabler unscharfer Algorithmus - findet alles mögliche
@route('/video/ardmediathek2016/Search')	# Suche - Verarbeitung der Eingabe
#def Search(query, url=None):
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
	
	oc = PageControl(title=title, path=path, cbKey=next_cbKey) 	# wir springen direkt
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
@route('/video/ardmediathek2016/VerpasstWoche')	# Liste der Wochentage
# Ablauf: 	
#		2. PageControl: Liste der Rubriken des gewählten Tages
#		3. SinglePage: Sendungen der ausgewählten Rubrik mit Bildern (mehrere Sendungen pro Rubrik möglich)
#		4. Parseplaylist: Auswertung m3u8-Datei (verschiedene Auflösungen)
#		5. CreateVideoClipObject: einzelnes Video-Objekt erzeugen mit Bild + Laufzeit + Beschreibung
def VerpasstWoche(name):	# Wochenliste zeigen
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	#page = HTML.ElementFromURL(BASE_URL + ARD_VERPASST) # in neuer Mediathek nicht mehr auslesbar
	#Log(page)
	wlist = range(0,6)
	now = datetime.datetime.now()
	# Test auf Folgeseiten hier nicht nötig, immer nur 1 pro Tag

	for nr in wlist:
		#Log(element)
		iPath = BASE_URL + ARD_VERPASST + str(nr)
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")		# Formate s. man strftime (3)
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
		oc.add(DirectoryObject(key=Callback(PageControl, title=title, path=iPath, cbKey='SinglePage'), 
				title=title, thumb=ICON))
					
	return oc

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
@route('/video/ardmediathek2016/PageControl')	# kontrolliert auf Folgeseiten. Mehrfache Verwendung.
# Wir laden beim 1. Zugriff alle Seitenverweise in eine Liste. Bei den Folgezugriffen können die Seiten
# verweise entfallen - der Rückschritt zur Liste ist dem Anwender nach jedem Listenelement  möglich.
# Dagegen wird in der Mediathek geblättert.

def PageControl(cbKey, title, path, offset=0):  # 
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2='Folgeseiten: ' + title, art = ObjectContainer.art)
	page = HTML.ElementFromURL(path)
	path_page1 = path							# Pfad der ersten Seite sichern, sonst gehts mit Seite 2 weiter
	
	Log('PageControl'); Log(cbKey); Log(path)
	# doc_txt = lxml.html.tostring(page)			# akzeptiert Plex nicht
	doc_txt = HTML.StringFromElement(page)
	#Log(doc_txt)

	pagenr_suche = re.findall("mresults=page", doc_txt)   
	pagenr_andere = re.findall("mcontents=page", doc_txt)  
	Log(pagenr_suche); Log(pagenr_andere)
	if (pagenr_suche) or (pagenr_andere):
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


	first_site = False								# falls 1. Aufruf ohne Seitennr. im Pfad ergänzen für Liste		
	if (pagenr_suche) or (pagenr_andere):			# .findall("mresults=page", doc_txt)  		
		if path_page1.find('mcontents=page') == -1: 
			first_site = True
			path_page1 = path_page1 + 'mcontents=page.1'
		if path_page1.find('mresults=page') == -1:
			first_site = True
			path_page1 = path_page1 + '&mresults=page.1'
		if path_page1.find('searchText=') >= 0:			#  kommt direkt von Suche
			first_site = True
			path_page1 = path + '&source=tv&mresults=page.1'

	if  first_site == True:										
		path_page1 
		title = 'Weiter zu Seite 1'
		next_cbKey = 'SingleSendung'
		Log(first_site)
		Log(path_page1)
		oc.add(DirectoryObject(key=Callback(SinglePage, title=title, path=path_page1, next_cbKey=next_cbKey), 
				title=title, thumb=ICON))
	else:	# Folgeseite - keine Liste mehr notwendig
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
@route('/video/ardmediathek2016/SinglePage')	# Liste der Sendungen eines Tages / einer Suche 
#						# durchgehend angezeigt (im Original collapsed)
def SinglePage(title, path, next_cbKey, offset=0):	# path komplett

	oc = ObjectContainer(view_group="InfoList", title1=title, art=ICON)
	Log('Funktion SinglePage'); # Log(path)
					
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
@route('/video/ardmediathek2016/SingleSendung')	# einzelne Sendung, path in neuer Mediathekführt zur 
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
		oc.add(CreateVideoStreamObject(url=link_m3u8, title=title, 
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
	
	Log(href_quality_S); Log(href_quality_M); Log(href_quality_L);  Log(href_quality_XL)
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
# Plex-Warnung: Media part has no streams - attempting to synthesize | keine Auswirkung
# **kwargs erforderlich bei Fehler: CreateVideoClipObject() got an unexpected keyword argument 'checkFiles'
#	beobachtet bei Firefox (Suse Leap) + Chrome (Windows7)
#	s.a. https://github.com/sander1/channelpear.bundle/tree/8605fc778a2d46243bb0378b0ab40a205c408da4
@route('/video/ardmediathek2016/CreateVideoClipObject')	# <- SingleSendung Qualitätsstufen
def CreateVideoClipObject(url, title, summary, meta, thumb, duration,include_container=False, **kwargs):
  #title = title.encode("utf-8")		# ev. für alle ausgelesenen Details erforderlich
  Log('CreateVideoClipObject')
  Log(url)
 
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
			],
			container = Container.MP4,  	# weitere Video-Details für Chrome nicht erf., aber Firefox 
			video_codec = VideoCodec.H264,	# benötigt VideoCodec + AudioCodec zur Audiowiedergabe
			audio_codec = AudioCodec.AAC,	# 
		)
	])

  if include_container:
	return ObjectContainer(objects=[videoclip_obj])
  else:
	return videoclip_obj
	
#####################################################################################################
@route('/video/ardmediathek2016/SenderLiveListe')	# LiveListe - verwendet lokale Playlist
def SenderLiveListe(title, offset=0):	# 
	# SenderLiveListe -> SenderLiveResolution (reicht nur durch) -> Parseplaylist (Ausw. m3u8)
	#	-> CreateVideoStreamObject 
	Log.Debug('SenderLiveListe')

	oc = ObjectContainer(view_group="InfoList", title1='Live-Sender', title2=title, art = ICON)
	playlist = Resource.Load(PLAYLIST)	# lokale XML-Datei (Pluginverz./Resources)
	#Log(playlist)	#

	#doc = XML.ElementFromString(playlist)		# schlägt bei Zeichen & in Url's fehl
	doc = HTML.ElementFromString(playlist)		# unterschlägt </link>
	
	liste = doc.xpath('//channels/channel/items/item')
	#Log(liste)

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
		Log(link); Log(title); Log(img);

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
@route('/video/ardmediathek2016/SenderLiveResolution')	# Auswahl der Auflösungstufen des Livesenders
#	Die URL der gewählten Auflösung führt zu weiterer m3u8-Datei (*.m3u8), die Links zu den 
#	Videosegmenten (.ts-Files enthält). Diese  verarbeitet der Plexserver im Videoobject. 
def SenderLiveResolution(path, title, thumb, include_container=False):
	#oc = ObjectContainer(view_group="InfoList", title1=title + ' Live', art=ICON)
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
			summary='', meta=Codecs, thumb=thumb))
		return oc
		
	# alle übrigen (i.d.R. http-Links)
	oc.add(CreateVideoStreamObject(url=url_m3u8, title=title + ' | Bandbreite und Auflösung automatisch', 
		summary='funktioniert nicht mit allen Playern', meta=Codecs, thumb=thumb))
	# Auslösungsstufen (bei relativen Pfaden nutzlos):
	oc = Parseplaylist(oc, url_m3u8, thumb)	# Auswertung *.m3u8-Datei, Auffüllung Container mit Auflösungen
	return oc								# (-> CreateVideoStreamObject pro Auflösungstufe)

####################################################################################################
# Die unter  https://api.arte.tv/api/player/v1/livestream/de?autostart=1 ausgelieferte Textdatei
# 	enthält je 2 rtmp-Url und 2 hls-Url
@route('/video/ardmediathek2016/Arteplaylist')	# Auswertung Arte-Parameter rtmp- + hls-streaming
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
	
	oc.add(CreateVideoStreamObject(url=rtmp1_url, title=title + ' (de) | rtmp', 
		summary='RTMP-Streaming deutsch', meta='', thumb=thumb))
	oc.add(CreateVideoStreamObject(url=rtmp2_url, title=title + ' (fr) | rtmp', 
		summary='RTMP-Streaming französisch', meta='', thumb=thumb))
	oc.add(CreateVideoStreamObject(url=hls1_url, title=title + ' (de) | http', 
		summary='HLS-Streaming deutsch', meta='', thumb=thumb))
	oc.add(CreateVideoStreamObject(url=hls2_url, title=title + ' (fr) | http', 
		summary='HLS-Streaming französisch', meta='', thumb=thumb))
	
	Log(rtmp1_url); Log(rtmp2_url); Log(hls1_url); Log(hls2_url); Log(len(oc))
	return oc

####################################################################################################
# **kwargs - s. CreateVideoClipObject
@route('/video/ardmediathek2016/CreateVideoStreamObject')	# <- LiveListe, SingleSendung (nur m3u8-Dateien)
def CreateVideoStreamObject(url, title, summary, meta, thumb, include_container=False, **kwargs):
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
  
  
	if url.find('rtmp:') >= 0:	# rtmp = Protokoll für flash, rtmpdump ermittelt Quellen
		mo = MediaObject(parts=[PartObject(key=RTMPVideoURL(url=url,live=True))]) # DAF (mit live-Param., NRW.TV OK
		rating_key = title
		videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary, 
			meta=meta, thumb=thumb, include_container=True), 
			rating_key=title,title=title,summary=summary,thumb=thumb,)   # live=True nicht aktzeptiert

	else:
		# Auslösungsstufen weglassen? (bei relativen Pfaden nutzlos) 
		# Auflösungsstufen - s. SenderLiveResolution -> Parseplaylist
		mo = MediaObject(parts=[PartObject(key=HTTPLiveStreamURL(url=url))]) #
		rating_key = title
		videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,
			meta=meta, thumb=thumb, include_container=True), 
			rating_key=title,title=title,summary=summary,thumb=thumb)
			
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
@route('/video/ardmediathek2016/PlayVideo')  
def PlayVideo(url):  		
	HTTP.Request(url).content
	return Redirect(url)

####################################################################################################
#									Hilfsroutinen
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
			container.add(CreateVideoStreamObject(url=url, title=title, 
				summary=Resolution, meta=Codecs, thumb=thumb))
			BandwithOld = Bandwith
				
  	i = i + 1	# Index für URL
  #Log (len(container))	# Anzahl Elemente
  if len(container) == 0:	# Fehler, zurück zum Hauptmenü
  		container.add(DirectoryObject(key=Callback(Main),  title='inkompatible m3u8-Datei', 
			tagline='Kennung #EXT-X-STREAM-INF fehlt oder den Pfaden fehlt http:// ', thumb=thumb)) 
	
  return container

#---------------------------------------------------------------- 
def get_sendungen(container, sendungen): # Sendungen aus Verpasst + A-Z, ausgeschnitten mit class='teaser'
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
				#s = s.split('urlScheme&#039;:&#039;')[0]	#	zwischen beiden split-strings
				s = s.split('urlScheme')[1]					#	klappt wg. Sonderz. nur so	
				img_src = s.split('##width##')[0]
				img_src  = img_src [3:]						# 	vorne ':' abschneiden
				img_src = BASE_URL + img_src + '320'			# Größe nicht in Quelle, getestet: 160,320,640

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
def CalculateDuration(timecode):	# Übergabeform: 05:12, Zeit in Millisekunden wird vom VideoClipObject
  milliseconds = 0					# benötigt, um dem User die Positionierung im Video zu ermöglichen
  minutes      = 0
  seconds      = 0
  timecode = timecode.strip()
  if timecode.find(':') == -1:		# in neuer Mediathek fehlen die Sekundenangaben
		timecode = timecode + ':00'
  minutes = timecode.split(':')[0]	
  seconds = timecode.split(':')[1]
  minutes = int(minutes)
  seconds = int(seconds)
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










