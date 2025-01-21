import streamlit as st
import matplotlib.pyplot as plt
import math

# Hilfsfunktion zum Runden auf die nächsten 1000€
def runde_auf_1000(betrag):
    return math.ceil(betrag / 1000) * 1000

# Titel und Einleitung
st.title("🏠 Baufinanzierungsrechner - Teil 1")
st.markdown(
    """
    **Ermittlung des Finanzierungsbedarfs:**
    Geben Sie die relevanten Informationen zu Ihrer Immobilie, den Nebenkosten und weiteren Ausgaben ein.
    Danach wird Ihr gesamter Finanzierungsbedarf berechnet.
    """
)

# Schritt 1: Immobilientyp wählen
st.markdown("### Schritt 1: Immobilientyp auswählen")
immobilientyp = st.radio(
    "Welche Art von Immobilie möchten Sie finanzieren?",
    ("Reines Grundstück", "Neubau", "Bestandsimmobilie")
)
st.caption("Wählen Sie den Immobilientyp, um die Nebenkosten korrekt zu berechnen.")

# Eingabe des Kaufpreises
if immobilientyp == "Neubau":
    neubau_typ = st.radio(
        "Handelt es sich um einen Neubau vom Bauträger oder um Neubau und Grundstückskauf separat?",
        ("Neubau vom Bauträger", "Neubau und Grundstückskauf separat")
    )
    if neubau_typ == "Neubau und Grundstückskauf separat":
        grundstueckspreis = st.number_input("Kaufpreis des Grundstücks (€):", min_value=0.0, step=1000.0)
        bebauungskosten = st.number_input("Kosten für die Bebauung (€):", min_value=0.0, step=1000.0)
    else:
        kaufpreis = st.number_input("Gesamtkaufpreis (€):", min_value=0.0, step=1000.0)
else:
    kaufpreis = st.number_input("Kaufpreis (€):", min_value=0.0, step=1000.0)

# Nebenkosten
st.markdown("### Schritt 2: Nebenkosten eingeben")
st.caption("Nebenkosten wie Notarkosten und Grunderwerbssteuer werden standardmäßig mit 2% bzw. 6% berechnet.")

notarkosten_prozent = 2.0
grunderwerbssteuer_prozent = 6.0
maklercourtage = st.number_input("Maklercourtage (in %):", min_value=0.0, max_value=10.0, step=0.1)

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
st.markdown("### Schritt 3: Zusätzliche Kosten eingeben")
erschliessungskosten = st.number_input("Erschließungskosten (€):", min_value=0.0, step=1000.0)
hausanschlusskosten = st.number_input("Hausanschlusskosten (€):", min_value=0.0, step=1000.0)
renovierungskosten = st.number_input("Renovierungs-/Modernisierungskosten (€):", min_value=0.0, step=1000.0)
kueche_kosten = st.number_input("Kosten für Küche (€):", min_value=0.0, step=1000.0)
aussenanlagen_kosten = st.number_input("Kosten für Außenanlagen (€):", min_value=0.0, step=1000.0)
weitere_kosten_summe = erschliessungskosten + hausanschlusskosten + renovierungskosten + kueche_kosten + aussenanlagen_kosten

# Gesamtkosten berechnen
if immobilientyp == "Neubau" and neubau_typ == "Neubau und Grundstückskauf separat":
    finanzierungsbedarf_vor_abzuegen = grundstueckspreis + bebauungskosten + nebenkosten_summe + weitere_kosten_summe
else:
    finanzierungsbedarf_vor_abzuegen = kaufpreis + nebenkosten_summe + weitere_kosten_summe

# Eigenkapital
st.markdown("### Schritt 4: Eigenkapital")
eigenkapital = st.number_input("Eigenkapital (€):", min_value=0.0, step=1000.0)

# Bausparvertrag
st.markdown("### Schritt 5: Bausparvertrag")
bausparer_option = st.radio("Möchten Sie einen Bausparvertrag einbringen?", ("Ja", "Nein"))
if bausparer_option == "Ja":
    bausparsumme = st.number_input("Bausparsumme (€):", min_value=0.0, step=1000.0)
    finanzierungsbedarf_vor_abzuegen -= bausparsumme

# Eigenkapitalanteil berechnen
urspruenglicher_finanzierungsbedarf = finanzierungsbedarf_vor_abzuegen
eigenkapitalanteil = (eigenkapital / urspruenglicher_finanzierungsbedarf) * 100

# Endgültiger Finanzierungsbedarf
finanzierungsbedarf = finanzierungsbedarf_vor_abzuegen - eigenkapital

# Ergebnisse anzeigen
if st.button("Ergebnis anzeigen"):
    st.markdown("## 📝 Ergebnis")
    st.markdown(f"**Finanzierungsbedarf (inkl. Nebenkosten & Co.):** {urspruenglicher_finanzierungsbedarf:,.2f} €")
    st.markdown(f"**Eigenkapital:** {eigenkapital:,.2f} €")
    st.markdown(f"**Eigenkapitalanteil am ursprünglichen Finanzierungsbedarf:** {eigenkapitalanteil:.2f}%")
    st.markdown(f"**Endgültiger Finanzierungsbedarf:** {finanzierungsbedarf:,.2f} €")
    st.markdown(f"**Aufgerundeter Finanzierungsbedarf:** {runde_auf_1000(finanzierungsbedarf):,.2f} €")

    # Visualisierung
    labels = ["Nebenkosten", "Weitere Kosten", "Eigenkapital", "Darlehen"]
    sizes = [
        nebenkosten_summe,
        weitere_kosten_summe,
        eigenkapital,
        finanzierungsbedarf
    ]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    plt.title("Aufteilung der Finanzierungskosten")
    st.pyplot(fig)



