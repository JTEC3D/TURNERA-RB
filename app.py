import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title='Turnera Kinesiología', layout='wide')

st.title('Turnera Kinesiología 🩷')
st.caption('Turnos de lunes a viernes (14-21 hs) y sábados (7-21 hs), cada 30 minutos.')

# Inicializar session state
if 'turnos' not in st.session_state:
    st.session_state.turnos = []

# ---- FORMULARIO ----
st.subheader("➕ Cargar nuevo turno")

with st.form("form_turno"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del paciente")
        telefono = st.text_input("Teléfono")
        email = st.text_input("Correo electrónico")
    with col2:
        tratamiento = st.text_input("Tratamiento")
        fecha = st.date_input("Fecha del turno", value=datetime.today())
        hora = st.time_input("Hora del turno", value=datetime.strptime("14:00", "%H:%M").time())

    observaciones = st.text_area("Observaciones / seguimiento")

    enviado = st.form_submit_button("Guardar turno")

    if enviado and nombre and tratamiento:
        st.session_state.turnos.append({
            "nombre": nombre,
            "telefono": telefono,
            "email": email,
            "tratamiento": tratamiento,
            "fecha": fecha.strftime("%Y-%m-%d"),
            "hora": hora.strftime("%H:%M"),
            "observaciones": observaciones
        })
        st.success("✅ Turno guardado correctamente")

st.markdown("---")

# ---- AGENDA SEMANAL ----
st.subheader("📅 Turnos agendados (semana actual + siguiente)")

def generar_agenda():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    dias = [lunes + timedelta(days=i) for i in range(6 * 2)]  # lunes a sábado, 2 semanas
    agenda = []

    for dia in dias:
        if dia.weekday() < 5:  # Lun a Vie
            hs_inicio, hs_fin = 14, 21
        else:  # Sáb
            hs_inicio, hs_fin = 7, 21

        hora_actual = hs_inicio
        while hora_actual < hs_fin:
            for m in [0, 30]:
                hora_str = f"{hora_actual:02d}:{m:02d}"
                agenda.append({
                    "Fecha": dia.strftime("%Y-%m-%d"),
                    "Hora": hora_str,
                    "Paciente": ""
                })
            hora_actual += 1
    return agenda

# Generar agenda base
agenda = generar_agenda()

# Cargar turnos en agenda
for turno in st.session_state.turnos:
    for slot in agenda:
        if slot["Fecha"] == turno["fecha"] and slot["Hora"] == turno["hora"]:
            slot["Paciente"] = turno["nombre"]

df_agenda = pd.DataFrame(agenda)

# Colorear con estilo pastel rosa
def formato_html(row):
    color_fondo = "#ffe6f0" if row.name % 2 == 0 else "#fce4ec"
    texto = f"<div style='background-color:{color_fondo}; text-align:center; padding:5px; font-weight:{'bold' if row['Paciente'] else 'normal'}'>{row['Paciente'] or ''}</div>"
    return texto

df_agenda["Mostrar"] = df_agenda.apply(formato_html, axis=1)

# Mostrar por días
dias = df_agenda["Fecha"].unique()
for fecha in dias:
    st.markdown(f"#### {fecha}")
    df_dia = df_agenda[df_agenda["Fecha"] == fecha][["Hora", "Mostrar"]]
    df_dia.columns = ["Hora", "Paciente"]
    st.write(df_dia.to_html(escape=False, index=False), unsafe_allow_html=True)
