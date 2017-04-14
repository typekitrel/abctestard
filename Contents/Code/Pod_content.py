# -*- coding: utf-8 -*-
# Pod_content.py	- Aufruf durch __init__.py/PodFavoritenListe 
#
# Die Funktionen dienen zur Auswertung von Podcasts außerhalb www.ardmediathek.de/radio
# Basis ist die Liste podcast-favorits.txt (Default/Muster im Ressourcenverzeichnis), die
# 	Liste enthält weitere  Infos zum Format und zu bereits unterstützten Podcast-Seiten
# 	- siehe nachfolgende Liste Podcast_Scheme_List

Podcast_Scheme_List = [		# Liste vorhandener Auswertungs-Schemata
	'www.br-online.de', 'www.swr3.de/mehr/podcasts',  
	'www.deutschlandfunk.de']	


####################################################################################################
@route(PREFIX + '/PodFavoriten')
def PodFavoriten(title, path, offset=1):
	Log('PodFavoriten'); Log(offset)
	
	rec_per_page = 20		# Anzahl pro Seite - berücksichtigt in Pod_content.get_pod_content	
	title_org = title

	Scheme = ''
	for s in Podcast_Scheme_List:				# Prüfung: Schema für path vorhanden?
		Log(s); Log(path)
		if path.find(s) >= 0:
			Scheme = s
			break			
	if Scheme == '':			
		msg='Auswertungs-Schema fehlt für Url:\n' +  path
		msg = msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header='Error', message=msg)
		
	# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
	#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild	
	POD_rec = get_pod_content(url=path, rec_per_page=rec_per_page, mode=Scheme, offset=offset)
	
	rec_cnt = len(POD_rec)							# Anzahl gelesener Sätze
	start_cnt = int(offset) + 1						# Startzahl diese Seite
	end_cnt = int(start_cnt) + int(rec_per_page)-1	# Endzahl diese Seite
	
	title2 = 'Pocasts %s - %s (%s)' % (start_cnt,  min(end_cnt,POD_rec[0][0]), POD_rec[0][0])
	oc = ObjectContainer(view_group="InfoList", title1='Favoriten', title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc, ID='PODCAST')					# Home-Button
	
	if rec_cnt == 0:			
		msg='Keine Podcast-Daten gefunden. Url:\n' +  path
		msg = msg.decode(encoding="utf-8", errors="ignore")
		return ObjectContainer(header='Error', message=msg)
			
	for rec in POD_rec:
		max_len=rec[0]
		url=rec[1]; summ=rec[3]; title=rec[7];
		img = R(ICON_NOTE)	
		if rec[8]:
			img = rec[8]
		Log(title); Log(summ); Log(url); 
		oc.add(CreateTrackObject(url=url, title=title, summary=summ, fmt='mp3', thumb=img))
		
	# Mehr Seiten anzeigen:
	Log(rec_cnt);Log(offset);Log(max_len)
	if rec_cnt + int(offset) < max_len: 
		new_offset = rec_cnt + int(offset)
		Log(new_offset)
		summ = 'Mehr (insgesamt ' + str(max_len) + ' Podcasts)'
		summ = summ.decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(PodFavoriten, title=title_org, path=path, offset=new_offset), 
			title=title_org, tagline='Favoriten', summary=summ,  thumb=R(ICON_MEHR)))	
			 
	return oc

#------------------------	
def get_pod_content(url, rec_per_page, mode, offset):
	Log('get_pod_content'); Log(rec_per_page); Log(mode); Log(offset);
	
	page, err = get_page(path=url)				# Absicherung gegen Connect-Probleme
	if err:
		return err	
	Log(len(page))

	if mode == 'www.br-online.de':
		return Scheme_br_online(page, rec_per_page, offset)
	if mode == 'www.swr3.de/mehr/podcasts':
		return Scheme_swr3(page, rec_per_page, offset)
	if mode == 'www.deutschlandfunk.de':
		return Scheme_deutschlandfunk(page, rec_per_page, offset)
		
		
#------------------------
def Scheme_br_online(page, rec_per_page, offset):		# Schema www.br-online.de
	Log('Scheme_br_online')
	sendungen = blockextract('<table class="ci"', page)
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze
	Log(max_len)
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('<td class="ci01" colspan="3">', '</td', s) 
		title = title_org.strip()
		summ = stringextract('<td class="ci02" colspan="3">', '</td', s) 
		summ = summ.strip()
		url = stringextract('href="', '\"', s) 
		img =  ''						# Bild nicht vorhanden
		
		datum = stringextract('Datum:</strong>', '<br/>', s) 				# im Titel bereits vorhanden
		dauer = stringextract('L&auml;nge:</strong>', '<br/>', s) 
		groesse = stringextract('Gr&ouml;&szlig;e:</strong>', '</span>', s)
		groesse = groesse.strip()
		title = title_org + ' | %s | %s' % (dauer, groesse)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
	
# ------------------------
def Scheme_swr3(page, rec_per_page, offset):					# Schema www.br-online.de
	Log('Scheme_swr3')
	sendungen = blockextract('<li id=\"audio-', page)
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze
	Log(max_len)
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('data-title="', '\"', s) 
		title = title_org.strip()
		summ = stringextract('"duration" content="T', '\"', s) 			# Dauer statt Beschreibung (fehlt)
		summ = summ.strip()
		url = stringextract('data-mp3="', '\"', s) 
		img =  stringextract('<img src="', '\"', s) 
		img_alt =  stringextract('alt="', '\"', s) 						# Bildbeschr. - nicht verwendet
		
		datum = stringextract('datePublished">', '</time>', s) 			# im Titel ev. bereits vorhanden
		dauer = stringextract('content="T', '">', s) 
		groesse = stringextract('data-ati-size="', '"', s)
		groesse = float(int(groesse)) / 1000000						# Konvert. nach MB, auf 2 Stellen gerundet
		groesse = '%.2f MB' % groesse
		
		title = ' %s | %s' % (title, datum)
		summ = ' Dauer %s | Größe %s' % (dauer, groesse)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
		
# ------------------------
def Scheme_deutschlandfunk(page, rec_per_page, offset):					# Schema www.deutschlandfunk.de, XML-Format
	Log('Scheme_Scheme_swr3')
	sendungen = blockextract('<item>', page)
	max_len = len(sendungen)					# Gesamtzahl gefundener Sätze
	Log(max_len)
	
	POD_rec = []			# Datensaetze gesamt (1. Dim.)
	for i in range(len(sendungen)):
		cnt = int(i) + int(offset)
		# Log(cnt); Log(i)
		if int(cnt) >= max_len:			# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:			# Anzahl pro Seite überschritten?
			break
		s = sendungen[cnt]
		
		single_rec = []		# Datensatz einzeln (2. Dim.)
		title_org = stringextract('<title>', '</title>', s) 
		title = title_org.strip()
		summ = stringextract('vspace="4"/>', '<br', s) 			# direkt nach Bildbeschreibung
		summ = summ.strip()
		url = stringextract('<enclosure url="', '"', s) 
		img =  stringextract('<img src="', '\"', s) 
		img_alt =  stringextract('alt="', '\"', s) 						# 
		
		author = stringextract('itunes:author>', '</itunes:author>', s) 
		datum = stringextract('<pubDate>', '</pubDate>', s)
		datum = datum.replace('+0200', '')	
		dauer = stringextract('duration>', '</itunes', s) 
		groesse = stringextract('length="', '"', s) 
		groesse = float(int(groesse)) / 1000000						# Konvert. nach MB, auf 2 Stellen gerundet
		groesse = '%.2f MB' % groesse
		
		title = ' %s | %s' % (title, datum)
		summ = ' Autor %s | Datum %s | Größe %s' % (author, datum, groesse)
		
		Log(title); Log(summ); Log(url); 
		title=title.decode(encoding="utf-8", errors="ignore")
		summ=summ.decode(encoding="utf-8", errors="ignore")
		
		# Indices: 	0. Gesamtzahl, 1. Url, 2. Originaltitel, 3. Summary, 4. Datum,
		#			5. Dauer, 6. Größe, 7. Titel (zusammengesetzt), 8. Bild
		single_rec.append(max_len); single_rec.append(url); single_rec.append(title_org); 
		single_rec.append(summ); single_rec.append(datum); single_rec.append(dauer); 
		single_rec.append(groesse); single_rec.append(title); single_rec.append(img);
		POD_rec.append(single_rec)
		
	Log(len(POD_rec))	
	return POD_rec
		
####################################################################################################
#									Hilfsfunktionen
####################################################################################################
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
def blockextract(blockmark, mString=''):  	# extrahiert Blöcke aus mString, begrenzt durch blockmark 
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

