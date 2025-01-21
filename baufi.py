import streamlit as st
import math
import time

# Hilfsfunktion zum Runden auf die nächsten 1000€
def runde_auf_1000(betrag):
    return math.ceil(betrag / 1000) * 1000

# Titel und Einleitung
st.title("🏠 Baufinanzierungsrechner - Teil 1")
st.markdown(
    """
    Willkommen! Mit diesem Rechner können Sie Ihren **Finanzierungsbedarf inklusive aller Nebenkosten und Ausgaben** ermitteln. 
    Geben Sie die Details Schritt für Schritt ein, und wir berechnen das Ergebnis für Sie. 🧮
    """
)

# Schritt 1: Immobilientyp wählen
st.markdown("### 1️⃣ Immobilientyp auswählen")
immobilientyp = st.radio(
    "Welche Art von Immobilie möchten Sie finanzieren?",
    ("Reines Grundstück", "Neubau", "Bestandsimmobilie"),
    help="Wählen Sie den Immobilientyp, um die Nebenkosten korrekt zu berechnen."
)

# Eingabe des Kaufpreises
if immobilientyp == "Neubau":
    neubau_typ = st.radio(
        "Handelt es sich um einen Neubau vom Bauträger oder um Neubau und Grundstückskauf separat?",
        ("Neubau vom Bauträger", "Neubau und Grundstückskauf separat"),
        help="Bei 'Neubau und Grundstückskauf separat' werden die Kosten separat für Grundstück und Bau erfasst."
    )
    if neubau_typ == "Neubau und Grundstückskauf separat":
        grundstueckspreis = st.number_input("Kaufpreis des Grundstücks (€):", min_value=0.0, step=1000.0, format="%f")
        bebauungskosten = st.number_input("Kosten für die Bebauung (€):", min_value=0.0, step=1000.0, format="%f")
    else:
        kaufpreis = st.number_input("Gesamtkaufpreis (€):", min_value=0.0, step=1000.0, format="%f")
else:
    kaufpreis = st.number_input("Kaufpreis (€):", min_value=0.0, step=1000.0, format="%f")

# Nebenkosten
st.markdown("### 2️⃣ Nebenkosten eingeben")
st.caption("Die Notarkosten und Grunderwerbssteuer werden standardmäßig mit 2% bzw. 6% berechnet.")
notarkosten_prozent = 2.0
grunderwerbssteuer_prozent = 6.0
maklercourtage = st.number_input("Maklercourtage (in %):", min_value=0.0, max_value=10.0, step=0.1, format="%f")

if immobilientyp == "Neubau" and neubau_typ == "Neubau und Grundstückskauf separat":
    notarkosten = grundstueckspreis * (notarkosten_prozent / 100)
    grunderwerbssteuer = grundstueckspreis * (grunderwerbssteuer_prozent / 100)
    maklerkosten = grundstueckspreis * (maklercourtage / 100)
else:
    notarkosten = kaufpreis * (notarkosten_prozent / 100)
    grunderwerbssteuer = kaufpreis * (grunderwerbssteuer_prozent / 100)
    maklerkosten = kaufpreis * (maklercourtage / 100)

nebenkosten_summe = notarkosten + grunderwerbssteuer + maklerkosten

# Weitere Kosten
st.markdown("### 3️⃣ Zusätzliche Kosten eingeben")
erschliessungskosten = st.number_input("Erschließungskosten (€):", min_value=0.0, step=1000.0, format="%f")
hausanschlusskosten = st.number_input("Hausanschlusskosten (€):", min_value=0.0, step=1000.0, format="%f")
renovierungskosten = st.number_input("Renovierungs-/Modernisierungskosten (€):", min_value=0.0, step=1000.0, format="%f")
kueche_kosten = st.number_input("Kosten für Küche (€):", min_value=0.0, step=1000.0, format="%f")
aussenanlagen_kosten = st.number_input("Kosten für Außenanlagen (€):", min_value=0.0, step=1000.0, format="%f")
weitere_kosten_summe = erschliessungskosten + hausanschlusskosten + renovierungskosten + kueche_kosten + aussenanlagen_kosten

# Gesamtkosten berechnen
if immobilientyp == "Neubau" and neubau_typ == "Neubau und Grundstückskauf separat":
    finanzierungsbedarf_vor_abzuegen = grundstueckspreis + bebauungskosten + nebenkosten_summe + weitere_kosten_summe
else:
    finanzierungsbedarf_vor_abzuegen = kaufpreis + nebenkosten_summe + weitere_kosten_summe

# Eigenkapital
st.markdown("### 4️⃣ Eigenkapital")
eigenkapital = st.number_input("Eigenkapital (€):", min_value=0.0, step=1000.0, format="%f")

# Bausparvertrag
st.markdown("### 5️⃣ Bausparvertrag")
bausparer_option = st.radio("Möchten Sie einen Bausparvertrag einbringen?", ("Ja", "Nein"))
if bausparer_option == "Ja":
    bausparsumme = st.number_input("Bausparsumme (€):", min_value=0.0, step=1000.0, format="%f")
    finanzierungsbedarf_vor_abzuegen -= bausparsumme

# Endgültiger Finanzierungsbedarf
finanzierungsbedarf = finanzierungsbedarf_vor_abzuegen - eigenkapital

# Ergebnisberechnung mit Ladezeit
if st.button("🔄 Ergebnis anzeigen"):
    with st.spinner("Berechnung läuft... Bitte warten Sie einen Moment."):
        time.sleep(2)  # Simulierte Ladezeit

    st.markdown("## 📋 Ergebnis")
    st.success(f"**Endgültiger Finanzierungsbedarf:** {finanzierungsbedarf:,.2f} €")
    st.info(f"**Aufgerundeter Finanzierungsbedarf:** {runde_auf_1000(finanzierungsbedarf):,.2f} €")
