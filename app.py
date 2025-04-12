import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title='Turnera Kinesiología', layout='wide')

st.title('Turnera Kinesiología')
st.caption('Semana actual + siguiente. Turnos cada 30 min.')

# Configuración de horarios
def generar_turnos():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    dias = [lunes + timedelta(days=i) for i in range(6 * 2)]  # lunes a sábado, 2 semanas
    horarios = []

    for dia in dias:
        if dia.weekday() < 5:  # Lun a Vie
            hs_inicio, hs_fin = 14, 21
        else:  # Sábados
            hs_inicio, hs_fin = 7, 21

        franja = []
        hora = hs_inicio
        while hora < hs_fin:
            franja.append(f"{hora:02d}:00")
            franja.append(f"{hora:02d}:30")
            hora += 1
        horarios.append((dia.strftime('%Y-%m-%d'), franja))

    return horarios

# Mostrar tabla semanal
turnos = generar_turnos()
for i, (fecha, horas) in enumerate(turnos):
    st.subheader(f"{fecha} ({['Lun','Mar','Mié','Jue','Vie','Sáb'][i % 6]})")
    df = pd.DataFrame({"Horario": horas, "Paciente": [""] * len(horas)})
    st.dataframe(df, width=1000)

st.markdown("---")
st.write("🔧 Aquí irá el formulario de edición de turnos, pacientes, tratamientos y exportación.")
