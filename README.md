Plex-Plugin-ARDMediathek2016
===================
Plex Plugin für die ARD Mediathek - mit Live-TV der ARD + weiteren Sendern
ab Version 2.0.0 mit ZDF Mediathek (Integration ZDF Mediathek.bundle V2.0)

Download aktuelle Version: https://github.com/rols1/Plex-Plugin-ARDMediathek2016/releases

Das Plugin löst den Vorgänger Plex-Plugin-ARDMediathek2015 ab. Das alte Plugin ist inkompatibel mit der neuen Struktur der Webseiten. Die ZDF Mediathek ist ab Version 2.1.1 integriert.

#### Rückmeldungen willkommen:
Im Forum: https://forums.plex.tv/discussion/213947/plex-plugin-ardmediathek2016
direkt: rols1@gmx.de 
  
Funktionen ab Version 2.2.0: 
===================
- TV-Sender Live (z.Z. 30 Sender)

#### ARD Mediathek:  
- Suche nach Sendungen
- Sendung Verpasst (Sendungen der letzten 7 Tage)
- Sendungen A-Z

#### ZDF Mediathek: 
- Sendung Verpasst (Sendungen der letzten 7 Tage)
- Sendungen A-Z
- Rubriken
- Themen
- MeistGesehen

#### Radio-Live-Streams der ARD:
- alle Radiosender von Bayern, HR, mdr, NDR, Radio Bremen, RBB, SR, SWR, WDR, Deutschlandfunk. Insgesamt 10 Stationen, 63 Sender
 
#### Videobehandlung ARD Mediathek und ZDF Mediathek:
- Videostreams: Auflistung der verfügbaren Angebote an Bandbreiten + Auflösungen (Ausnahme Audio ohne Video)
- Videoclips: Auflistung der verfügbaren Angebote an Qualitätstufen sowie zusätzlich verfügbarer Videoformate (Ausnahme HDS + SMIL) 


INSTALLATION:
===================  
Installationshilfe von Otto Kerner (Plex-Forum Mai 2015):
Anleitung zum manuellen Installieren von Plex Software-Bundles (Channels, Agenten, Scanner):
- zip-Datei von Github herunterladen
- zip auspacken, heraus kommt ein Ordner namens "Plex-Plugin-ARDMediathek2016-master"
- Diesen Ordner umbenennen in "ARDMediathek2016.bundle"
- den kompletten Ordner kopieren ins Plex Datenverzeichnis, in den Unterordner /Plug-ins

ein Neustart von Plex oder ein vorheriges Beenden von Plex ist i.d.R. nicht erforderlich
Beim Aktualisieren einfach den .bundle Ordner löschen und die neue Version an seine Stelle kopieren.
 
   
Meine Test- und Gebrauchsumgebung:
===================  
- PC: Fujitsu Esprimo E900 8 GB RAM, 3,4 GHz
- Linux openSUSE 42.1 und Plex-Server 0.9.16.4
- Tablet Nexus 7, Android 5.1.1,
- Web-Player: Google-Chrome (alles OK), Firefox (alles OK, Flash-Plugin erforderlich)
- Videoplayer-Apps: VLC-Player, MXPlayer
- Streaming-Apps: BubbleUPnP (alles OK), AllConnect (keine m3u8-Videos)
- Media Player at TV: WD TV Live HD, WDAAP0000NBK, 2012 (nicht alle Auflösungsstufen unterstützt)


Credits:
===================  
- Credits to [Gammel] (https://gmlblog.de/2013/08/xbmc-tv-livestreams/): Playlist http://dl.gmlblog.de/deutschesender.xml 
- Credits to [coder-alpha] https://forums.plex.tv/discussion/166602/rel-ccloudtv-channel-iptv/p1): (Channel updater, based on Channel updater by sharkone/BitTorrent.bundle)
- Credits to [Arauco] (https://forums.plex.tv/profile/Arauco): processing of Senderlogos
- Credits to [Sender1] (https://github.com/plexinc-plugins/ZDFMediathek.bundle): Plex-Plugin ZDFMediathek
