Hinweise zum Modupdater


Funktionsweise:
Es wird geprüft ob die Dateien "update_info.json" und "update_config.json" aktuell sind.
Wenn das der Fall ist, gibt es kein Update.
Wenn auf dem Server neuere Daten sind, werden diese heruntergeladen und ausgeführt.
Zum Testen kann man ein Update erzwingen, indem man im Mod "update_info.json" und "update_config.json" löscht.

Nachdem der Updater auf dem Server vorberitet wurde, müssen noch im Mod noch abgeglichen werden, ob
- in beiden Dateien ."..\Phyton\Extras\ModUpdater.py +.py3" die Angaben "PB93" durch "PB_PAE_6.17" ersetzt wurden.
- die Dateien "update_info.json" und "update_config.json" gelöscht sind.






