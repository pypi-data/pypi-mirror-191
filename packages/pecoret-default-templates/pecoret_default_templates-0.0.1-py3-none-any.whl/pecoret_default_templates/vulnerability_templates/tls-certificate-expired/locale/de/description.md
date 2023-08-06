Das von der Anwendung gesendete TLS-Zertifikat ist abgelaufen. Webbrowser betrachten es als ungültig und zeigen den Benutzern Ihrer Anwendung einen Fehler an.
In den meisten Fällen erlauben Browser und TLS-Bibliotheken dem Benutzer nicht, den Fehler zu ignorieren, so dass der Zugriff auf Ihre Anwendung effektiv blockiert wird.

Die Verwendung eines ungültigen Zertifikats erhöht die Wahrscheinlichkeit, dass der Benutzer Opfer eines Man-in-the-Middle-Angriffs wird, da ein böswilliger Dritter den Angriff mit einem ungültigen Zertifikat durchführen kann.
Dies geschieht, weil es für einen Benutzer schwierig sein kann, zu unterscheiden zwischen:

- Einem abgelaufenen, aber legitimen Zertifikat, das vom Server gesendet wurde (OK)
- Einem ungültigen Zertifikat, das vom Angreifer gesendet wurde (nicht OK)

Dies erhöht die Wahrscheinlichkeit eines erfolgreichen MITM-Angriffs erheblich.
