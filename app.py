import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title='Turnera Kinesiología', layout='wide')
st.title('Turnera Kinesiología 🩷')
st.caption('Turnos de lunes a sábado (semana actual + siguiente). Intervalos de 30 minutos.')

# Inicializar turnos en memoria
if 'turnos' not in st.session_state:
    st.session_state.turnos = []

# Formulario de carga
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
    obs = st.text_area("Observaciones / seguimiento")
    enviar = st.form_submit_button("Guardar turno")

    if enviar and nombre and tratamiento:
        st.session_state.turnos.append({
            "nombre": nombre,
            "telefono": telefono,
            "email": email,
            "tratamiento": tratamiento,
            "fecha": fecha.strftime("%Y-%m-%d"),
            "hora": hora.strftime("%H:%M"),
            "observaciones": obs
        })
        st.success("✅ Turno guardado")

st.markdown("---")
st.subheader("📅 Agenda de turnos (una sola tabla con días y horarios)")

# Generar días lunes a sábado para semana actual + siguiente
def generar_dias():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    return [lunes + timedelta(days=i) for i in range(12)]  # lunes a sábado * 2 semanas

# Generar horarios desde 07:00 a 21:00 en intervalos de 30 minutos
def generar_horarios():
    horarios = []
    for h in range(7, 21):
        horarios.append(f"{h:02d}:00")
        horarios.append(f"{h:02d}:30")
    return horarios

dias = generar_dias()
horarios = generar_horarios()

# Crear tabla vacía
columnas = [d.strftime('%a %d/%m') for d in dias]
tabla = pd.DataFrame("", index=horarios, columns=columnas)

# Completar con turnos
for t in st.session_state.turnos:
    fecha = datetime.strptime(t["fecha"], "%Y-%m-%d")
    col = fecha.strftime('%a %d/%m')
    if col in tabla.columns and t["hora"] in tabla.index:
        tabla.at[t["hora"], col] = t["nombre"]

# Estilo pastel alternado por columnas
def estilo_columnas(df):
    colores = ['#ffe6f0', '#fce4ec']
    style = pd.DataFrame("", index=df.index, columns=df.columns)
    for i, col in enumerate(df.columns):
        style[col] = [f'background-color: {colores[i % 2]}; text-align: center; font-weight: bold;' for _ in df.index]
    return style

st.dataframe(tabla.style.apply(estilo_columnas, axis=None), use_container_width=True)
