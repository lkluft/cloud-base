# Möglichkeiten einfacher Messinstrumente

Das Repository dient zur Unterstützung der wissenschaftlichen Arbeit während
der Lehrexkursion des Meteorologischen Instituts der Universität Hamburg.
Es umfasst sowohl die Dokumentation des aktuellen Projektstatus als auch die
zur Auswertung verwendeten Skripte.

Die Grundidee der Auswertung ist zu untersuchen, welche atmosphärischen
Zustandsgrößen aus einfachen Messgrößen abgeleitet werden können. Zu Grunde
liegen hierbei die langwellige Einstrahlung sowie die bodennahe Temeratur, die
mit einem Pyrgeometer beziehungsweise einem Thermometer ermittelt werden.

# Bestimmung der Wölkenhöhe

Im ersten Teil der Untersuchungen wird versucht, die Wolkenbasishöhe tiefer
Bewölkung zu ermitteln.

Die Menge der Strahlung, die ein Körper emittiert, hängt von seiner Temperatur
ab. Aus diesem Grund liefern tiefe Wolken ein stärkeres (wärmeres) Signal in
der langwelligen Einstrahlung. Diese Information kann unter Annahme
eines Temperaturegradienten in eine Höhe umgerechnet werden.

![Ceilometer profile time series](/doc/presentation/figures/ceilometer.png)

# Bestimmung des integrierten Wasserdampfgehaltes

Eine weitere interessante Größe ist die wasserdampfsäule (*Integrated Water
Vapor*, IWV).

Wasserdampf ist ein Treibhausgas und als solches ein seh guter Emittent
elektromagnetischer Strahlung. Eine Erhöhung des Wasserdampfgehaltes hat somit
eine stärkere langwellige Einstrahlung zur Folge. Ziel ist es, diese
Abhängigkeit mit Hilfe von Modellatmosphären und dem Strahlungstransfermodell
ARTS [0] zu genauer zu quantifizieren. Die gewonnen Daten werden verwendet, um
eine Funktion anzunähern, die zu Bestimmung des IWV aus einfachen Messdaten
verwendet werden kann.

![IWV fit correlation](/doc/abstract/figures/iwv_fit_correlation.png)

# Dokumentation
* [Extended Abstract (Draft)](doc/abstract/LEX2016_Pyrgeometer_Abstract.pdf)
* [Poster](doc/poster/LEX2016_Pyrgeometer_Poster.pdf)
* [Präsentation des Projektes](doc/presentation/LEX2016_Pyrgeometer_Praesentation.pdf)

# Weiterführende Links

[0] http://www.radiativetransfer.org/
