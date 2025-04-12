import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO

st.set_page_config(page_title='Turnera Kinesiología', layout='wide')
st.title('Turnera Kinesiología 🩷')
st.caption('Turnos de lunes a sábado (semana actual + siguiente). Intervalos de 30 minutos.')

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
st.subheader("📅 Agenda de turnos (una sola tabla)")

def generar_dias():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    return [lunes + timedelta(days=i) for i in range(12)]

def generar_horarios():
    horarios = []
    for h in range(7, 21):
        horarios.append(f"{h:02d}:00")
        horarios.append(f"{h:02d}:30")
    return horarios

dias = generar_dias()
horarios = generar_horarios()
columnas = [d.strftime('%a %d/%m') for d in dias]
tabla = pd.DataFrame("", index=horarios, columns=columnas)

for t in st.session_state.turnos:
    fecha = datetime.strptime(t["fecha"], "%Y-%m-%d")
    col = fecha.strftime('%a %d/%m')
    if col in tabla.columns and t["hora"] in tabla.index:
        tabla.at[t["hora"], col] = t["nombre"]

def estilo_columnas(df):
    colores = ['#ffe6f0', '#fce4ec']
    style = pd.DataFrame("", index=df.index, columns=df.columns)
    for i, col in enumerate(df.columns):
        style[col] = [f'background-color: {colores[i % 2]}; text-align: center; font-weight: bold;' for _ in df.index]
    return style

st.dataframe(tabla.style.apply(estilo_columnas, axis=None), use_container_width=True)

# 🔧 Edición y eliminación
st.markdown("---")
st.subheader("✏️ Modificar o eliminar turno")

if st.session_state.turnos:
    opciones = [f"{t['fecha']} {t['hora']} - {t['nombre']}" for t in st.session_state.turnos]
    seleccion = st.selectbox("Seleccioná un turno", opciones)
    index = opciones.index(seleccion)
    turno = st.session_state.turnos[index]

    with st.form("editar_turno"):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_nombre = st.text_input("Nombre del paciente", turno["nombre"])
            nuevo_telefono = st.text_input("Teléfono", turno["telefono"])
            nuevo_email = st.text_input("Correo electrónico", turno["email"])
        with col2:
            nuevo_tratamiento = st.text_input("Tratamiento", turno["tratamiento"])
            nueva_fecha = st.date_input("Fecha del turno", datetime.strptime(turno["fecha"], "%Y-%m-%d"))
            nueva_hora = st.time_input("Hora del turno", datetime.strptime(turno["hora"], "%H:%M").time())
        nueva_obs = st.text_area("Observaciones / seguimiento", turno["observaciones"])

        col_editar, col_borrar = st.columns(2)
        actualizar = col_editar.form_submit_button("💾 Guardar cambios")
        eliminar = col_borrar.form_submit_button("🗑️ Eliminar turno")

        if actualizar:
            st.session_state.turnos[index] = {
                "nombre": nuevo_nombre,
                "telefono": nuevo_telefono,
                "email": nuevo_email,
                "tratamiento": nuevo_tratamiento,
                "fecha": nueva_fecha.strftime("%Y-%m-%d"),
                "hora": nueva_hora.strftime("%H:%M"),
                "observaciones": nueva_obs
            }
            st.success("✅ Turno actualizado")

        if eliminar:
            st.session_state.turnos.pop(index)
            st.success("🗑️ Turno eliminado")

# 📤 Exportar a Excel
st.markdown("---")
st.subheader("📁 Exportar turnos a Excel")

if st.session_state.turnos:
    df_export = pd.DataFrame(st.session_state.turnos)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False, sheet_name="Turnos")
    st.download_button("⬇️ Descargar Excel", data=buffer.getvalue(), file_name="turnos_kinesiologia.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
