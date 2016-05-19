Plex-Plugin-ARDMediathek2016
===================
Plex Plugin für die ARD Mediathek - mit Live-TV der ARD + weiteren Sendern

Download aktuelle Version: https://github.com/rols1/Plex-Plugin-ARDMediathek2016/releases

Das Plugin löst den Vorgänger Plex-Plugin-ARDMediathek2015 ab. Das alte Plugin ist inkompatibel mit der neuen Struktur der Webseiten.

#### TODO:  
Vorschläge und Fehlerhinweise an rols1@gmx.de 
  
Funktionen: 
===================  
- Suche nach Sendungen
- Sendung Verpasst (Sendungen der letzten 7 Tage)
- Sendungen A-Z
- Sender Live (z.Z. 30 Sender, siehe Hinweise zu Sender Live)


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


Hinweise zu Sender Live:
===================  
Das Plugin verwendet die mitgelieferte Playlist im Unterverzeichnis Contents/Resources/livesender.xml. Diese muss ev. erneuert werden, falls die Sender den Zugriff ändern. Aktuell enthält sie neben den Regional-Sendern der ARD auch ZDF, ZDF-neo, ZDFkultur und ZDFinfo, sowie N24, n-tv, NRW.TV, Joiz und DAF

ARTE ist inzwischen lauffähig, getrennte Behandlung im Programmcode: 4 Streams, deutsch/französisch, RTMP/HTTP
 
RTMP-Streaming wird vom Plugin unterstützt, klappt aber nicht mit beliebigen neuen Sendern.

Beliebige Sender können manuell der Playlist hinzugefügt werden. Nicht alle werden funktionieren, da die Zugänge zu den Streaming-Quellen sich technisch stark unterscheiden können. Für manche ist eine Sonderbehandlung im Programmcode de Plugins erforderlich (Beispiel ARTE).

Credits:
===================  
- Credits to [Gammel] (https://gmlblog.de/2013/08/xbmc-tv-livestreams/): Playlist http://dl.gmlblog.de/deutschesender.xml 
- Credits to [coder-alpha] https://forums.plex.tv/discussion/166602/rel-ccloudtv-channel-iptv/p1): (Channel updater, based on Channel updater by sharkone/BitTorrent.bundle)
- Credits to [Arauco] (https://forums.plex.tv/profile/Arauco): processing of Senderlogos

