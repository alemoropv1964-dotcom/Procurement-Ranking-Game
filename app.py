import streamlit as st
import random

# ---------------------------------------------------------
# TITOLO E INTRODUZIONE
# ---------------------------------------------------------
st.title("🔄 Simulatore di Procurement – Ciclo Mod 4")
st.write("""
Questo simulatore permette di esplorare dinamiche di procurement multi-fornitore
con fallback ciclico **mod 4**, considerando:
- costo unitario
- lead time
- probabilità di ritardo
- capacità massima
- quantità ordinate
- lead time massimo accettabile

Modifica i parametri e premi **Simula** per vedere i risultati.
""")


# ---------------------------------------------------------
# VISUALIZZAZIONE GRAFICA DEL CICLO
# ---------------------------------------------------------
st.header("🔁 Visualizzazione del ciclo Mod 4")

st.code("""
F1 → F2 → F3 → F4 → F1
""", language="text")

st.write("Il ciclo rappresenta l'ordine dei fallback: se un fornitore fallisce, si passa al successivo nel ciclo.")


# ---------------------------------------------------------
# PARAMETRI FORNITORI
# ---------------------------------------------------------
st.header("📦 Parametri dei 4 Fornitori")

fornitori = []
for i in range(4):
    st.subheader(f"Fornitore F{i+1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        costo = st.number_input(f"Costo F{i+1}", 1, 100, 10)

    with col2:
        lt = st.number_input(f"Lead Time F{i+1}", 1, 60, 5)

    with col3:
        prob = st.slider(f"Prob. Ritardo F{i+1}", 0.0, 1.0, 0.10)

    with col4:
        cap = st.number_input(f"Capacità F{i+1}", 1, 500, 100)

    fornitori.append({
        "costo": costo,
        "lead_time": lt,
        "prob_ritardo": prob,
        "capacita": cap
    })


# ---------------------------------------------------------
# PARAMETRI PROCUREMENT
# ---------------------------------------------------------
st.header("📝 Parametri Procurement")

ordini = []
colA, colB, colC, colD = st.columns(4)

with colA:
    q1 = st.number_input("Ordine 1", 0, 500, 50)
with colB:
    q2 = st.number_input("Ordine 2", 0, 500, 40)
with colC:
    q3 = st.number_input("Ordine 3", 0, 500, 70)
with colD:
    q4 = st.number_input("Ordine 4", 0, 500, 30)

ordini = [q1, q2, q3, q4]

lead_time_max = st.number_input("Lead Time massimo accettabile", 1, 60, 10)


# ---------------------------------------------------------
# FUNZIONE CICLO MOD 4
# ---------------------------------------------------------
def ciclo_mod4(i):
    return (i + 1) % 4


# ---------------------------------------------------------
# SEZIONE FALLBACK PER OGNI ORDINE
# ---------------------------------------------------------
st.header("📌 Logica dei fallback per ogni ordine")

for i in range(4):
    primario = i
    fb1 = ciclo_mod4(primario)
    fb2 = ciclo_mod4(fb1)
    fb3 = ciclo_mod4(fb2)

    st.write(f"""
### Ordine {i+1}
- **Fornitore primario:** F{primario+1}
- **Fallback 1:** F{fb1+1}
- **Fallback 2:** F{fb2+1}
- **Fallback 3:** F{fb3+1}
""")


# ---------------------------------------------------------
# SIMULAZIONE
# ---------------------------------------------------------
st.header("🚀 Esegui Simulazione")

if st.button("Simula"):
    st.subheader("📊 Risultati")

    for i, quantita in enumerate(ordini):
        st.write(f"### 🔹 Ordine {i+1}: {quantita} unità")

        tentativi = 0
        corrente = i  # fornitore primario

        while tentativi < 4:
            f = fornitori[corrente]

            st.write(f"- Tentativo con **F{corrente+1}**")

            # Controllo capacità
            if quantita > f["capacita"]:
                st.warning(f"Capacità insufficiente (max {f['capacita']})")
                corrente = ciclo_mod4(corrente)
                tentativi += 1
                continue

            # Controllo ritardo
            if random.random() < f["prob_ritardo"]:
                st.warning(f"Ritardo! Probabilità {f['prob_ritardo']:.2f}")
                corrente = ciclo_mod4(corrente)
                tentativi += 1
                continue

            # Controllo lead time
            if f["lead_time"] > lead_time_max:
                st.warning(f"Lead time troppo alto: {f['lead_time']} > {lead_time_max}")
                corrente = ciclo_mod4(corrente)
                tentativi += 1
                continue

            # Se tutto OK → assegnazione
            costo_totale = quantita * f["costo"]
            st.success(
                f"Ordine assegnato a **F{corrente+1}** "
                f"(Costo totale: {costo_totale}, LT: {f['lead_time']})"
            )
            break

        if tentativi == 4:
            st.error("❌ Nessun fornitore disponibile per questo ordine.")
