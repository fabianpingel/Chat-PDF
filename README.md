# 📚 massiverCHAT – IMU Chat PDF

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://imu-chat-pdf.streamlit.app)


---
## 📘 Bedienungsanleitung – massiverCHAT / IMU FDB Chat

### 1. Überblick

**massiverCHAT** ist eine webbasierte Chat-Anwendung auf Basis von **Streamlit**, mit der Nutzer:innen **Fragen zu einem hochgeladenen PDF-Dokument** stellen können.
Die App analysiert den Inhalt des PDFs mithilfe von **OpenAI-Sprachmodellen** und liefert **kontextbasierte Antworten**, die direkt aus dem Dokument abgeleitet sind.

Typische Anwendungsfälle:

- Technische Richtlinien oder Forschungsberichte durchsuchen

- Normen, Handbücher oder Studien befragen

- Schnelles Finden relevanter Textstellen in PDFs

---

### 2. Zugriff auf die App

Die App ist über die Streamlit Community Cloud verfügbar und mit folgendem Badge verlinkt:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://imu-chat-pdf.streamlit.app)

---

### 3. Voraussetzungen

Um die App nutzen zu können, benötigt man:

- einen gültigen OpenAI API-Key

- ein PDF-Dokument, zu dem Fragen gestellt werden sollen

- einen aktuellen Webbrowser (Chrome, Edge, Firefox, ...)

---

### 4. Aufbau der Benutzeroberfläche
#### 4.1 Sidebar (linke Seite)

Die Sidebar dient zur Konfiguration und Vorbereitung der App.

**🔑 OpenAI API-Key**

- persönlichen OpenAI API-Key in das Passwortfeld eintragen

- Format: sk-...

- ohne API-Key ist keine Nutzung möglich

**Statusanzeigen:**

- ⚠️ „Bitte OpenAI API-Key eingeben“ → Key fehlt

- ✔️ „API-Key gesetzt“ → Key erfolgreich erkannt

---

**📄 PDF hochladen**

- Lade ein **PDF-Dokument** über den Upload-Button hoch

- Nach dem Upload wird:

    - das Dokument automatisch analysiert

    - der Text in sinnvolle Abschnitte zerlegt und

    - die Inhalte für eine semantische Suche indexiert.

**Statusmeldungen:**

- ⏳ „PDF wird verarbeitet…“

- ✅ „PDF erfolgreich indexiert!“

- ⚠️ „Bitte PDF hochladen“ → kein Dokument vorhanden

ℹ️ **Hinweis:** Das PDF wird nur einmal pro Session indexiert.

---

#### 4.2 Hauptbereich (Chat)

Der Hauptbereich ist der **interaktive Chat**, über den man Fragen an das PDF stellen kann.

**💬 Chat-Funktion**

- Frage unten ins Eingabefeld eingeben:

    | „Stelle eine Frage zum PDF…“

- Die Antwort wird:

    - live generiert (Streaming)

    - direkt im Chat angezeigt

    - aus Inhalten aus dem hochgeladenen PDF generiert

Beispiele:

- „Worum geht es in Kapitel 3?“

- „Welche Versuchsparameter wurden verwendet?“

- „Fasse die wichtigsten Ergebnisse zusammen.“

---

### 5. Funktionsweise im Hintergrund (vereinfacht erklärt)

1. PDF-Analyse

    - Das Dokument wird in Textabschnitte zerlegt

2. Vektorisierung

    - Inhalte werden in semantische Vektoren umgewandelt

3. Kontextsuche

    - Bei einer Frage werden die relevantesten Textstellen ermittelt

4. KI-Antwort

    - Das Sprachmodell erzeugt eine Antwort auf Basis des gefundenen Kontexts

➡️ Die KI „halluziniert“ nicht, sondern nutzt gezielt den Inhalt des PDFs.

---

### 6. Datenschutz & Hinweise

- Hochgeladene PDFs werden nur temporär verarbeitet

- Inhalte werden nicht dauerhaft gespeichert

- Der OpenAI API-Key wird nicht angezeigt, sondern nur zur Laufzeit verwendet

- Antworten hängen von der Qualität und Struktur des PDFs und der gestellten Frage ab

---

### 7. Fehlerbehebung

| Problem           | Lösung                               |
| ----------------- | ------------------------------------ |
| App startet nicht | OpenAI API-Key prüfen                |
| Keine Antworten   | PDF hochladen & Indexierung abwarten |
| Antwort ungenau   | Frage präziser formulieren           |
| PDF erneut laden  | Seite neu laden                      |

---

### 8. Copyright

© 2025
**Fabian Pingel**

---

