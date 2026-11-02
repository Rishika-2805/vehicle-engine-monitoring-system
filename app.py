import streamlit as st
import random
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Vehicle Engine Health Monitoring System",
    page_icon="🚗",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #aaaaaa;
    font-size: 18px;
    margin-bottom: 30px;
}

.sensor-card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1b1f2a;
    border: 1px solid #303642;
    text-align: center;
    margin-bottom: 10px;
}

.sensor-value {
    font-size: 32px;
    font-weight: bold;
}

.sensor-label {
    color: #aaaaaa;
    font-size: 16px;
}

.normal {
    color: #00d084;
}

.warning {
    color: #ffb020;
}

.danger {
    color: #ff4b4b;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=2000,
    key="vehicle_refresh"
)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "counter" not in st.session_state:
    st.session_state.counter = 0


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🚗 Vehicle Controls")

scenario = st.sidebar.selectbox(
    "Select Vehicle Condition",
    [
        "Normal",
        "Overheating",
        "Low Engine Temperature",
        "Low Oil Pressure",
        "High Oil Pressure",
        "Low Battery",
        "High Battery Voltage",
        "Low Tire Pressure",
        "High Tire Pressure",
        "Multiple Faults"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write("### Safety Thresholds")

st.sidebar.write("🌡️ Engine Temperature")
st.sidebar.write("Low: <70 °C")
st.sidebar.write("Normal: 70–100 °C")
st.sidebar.write("High: >100 °C")

st.sidebar.write("🛢️ Oil Pressure")
st.sidebar.write("Normal: 30–60 PSI")
st.sidebar.write("Low: <25 PSI")
st.sidebar.write("High: >65 PSI")

st.sidebar.write("🔋 Battery Voltage")
st.sidebar.write("Normal: 12–14.5 V")
st.sidebar.write("Low: <11.5 V")
st.sidebar.write("High: >15 V")

st.sidebar.write("🛞 Tire Pressure")
st.sidebar.write("Normal: 30–35 PSI")
st.sidebar.write("Low: <28 PSI")
st.sidebar.write("High: >40 PSI")


# =========================================================
# SENSOR SIMULATION
# =========================================================

def generate_sensor_data(condition):

    # Normal values
    temperature = random.uniform(75, 95)
    oil_pressure = random.uniform(35, 55)
    battery_voltage = random.uniform(12.5, 14.2)
    tire_pressure = random.uniform(30, 35)

    # Fault scenarios

    if condition == "Overheating":

        temperature = random.uniform(105, 125)

    elif condition == "Low Engine Temperature":

        temperature = random.uniform(30, 65)

    elif condition == "Low Oil Pressure":

        oil_pressure = random.uniform(10, 22)

    elif condition == "High Oil Pressure":

        oil_pressure = random.uniform(66, 80)

    elif condition == "Low Battery":

        battery_voltage = random.uniform(9.5, 11.4)

    elif condition == "High Battery Voltage":

        battery_voltage = random.uniform(15.1, 17)

    elif condition == "Low Tire Pressure":

        tire_pressure = random.uniform(20, 27)

    elif condition == "High Tire Pressure":

        tire_pressure = random.uniform(41, 50)

    elif condition == "Multiple Faults":

        temperature = random.uniform(108, 125)
        oil_pressure = random.uniform(10, 22)
        battery_voltage = random.uniform(9.5, 11.4)
        tire_pressure = random.uniform(41, 50)

    return (
        temperature,
        oil_pressure,
        battery_voltage,
        tire_pressure
    )


# =========================================================
# GET SENSOR VALUES
# =========================================================

temperature, oil_pressure, battery_voltage, tire_pressure = \
    generate_sensor_data(scenario)


# =========================================================
# FAULT DETECTION
# =========================================================

alerts = []


# ---------------- ENGINE TEMPERATURE ----------------

if temperature < 70:

    alerts.append(
        ("warning",
         "⚠️ WARNING: Low engine temperature detected!")
    )

elif temperature > 100:

    alerts.append(
        ("danger",
         "🔥 CRITICAL: Engine overheating detected!")
    )


# ---------------- OIL PRESSURE ----------------

if oil_pressure < 25:

    alerts.append(
        ("danger",
         "🛢️ CRITICAL: Low oil pressure detected!")
    )

elif oil_pressure > 65:

    alerts.append(
        ("danger",
         "🛢️ CRITICAL: High oil pressure detected!")
    )


# ---------------- BATTERY ----------------

if battery_voltage < 11.5:

    alerts.append(
        ("danger",
         "🔋 CRITICAL: Low battery voltage detected!")
    )

elif battery_voltage > 15:

    alerts.append(
        ("danger",
         "🔋 CRITICAL: High battery voltage detected!")
    )


# ---------------- TIRE PRESSURE ----------------

if tire_pressure < 28:

    alerts.append(
        ("danger",
         "🛞 CRITICAL: Low tire pressure detected!")
    )

elif tire_pressure > 40:

    alerts.append(
        ("danger",
         "🛞 CRITICAL: High tire pressure detected!")
    )


# =========================================================
# OVERALL VEHICLE STATUS
# =========================================================

if len(alerts) == 0:

    vehicle_status = "HEALTHY"
    status_class = "normal"

else:

    vehicle_status = "CRITICAL"
    status_class = "danger"


# =========================================================
# STORE HISTORY
# =========================================================

st.session_state.counter += 1

new_data = {
    "Time": datetime.now().strftime("%H:%M:%S"),
    "Engine Temperature": temperature,
    "Oil Pressure": oil_pressure,
    "Battery Voltage": battery_voltage,
    "Tire Pressure": tire_pressure
}

st.session_state.history.append(new_data)


# Keep latest 30 readings

if len(st.session_state.history) > 30:

    st.session_state.history.pop(0)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🚗 Vehicle Engine Health Monitoring System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Real-Time Digital Vehicle Sensor Monitoring & Fault Detection'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# OVERALL VEHICLE STATUS
# =========================================================

st.markdown(
    f"""
    <div style="
        text-align:center;
        padding:18px;
        border-radius:15px;
        background-color:#1b1f2a;
        margin-bottom:25px;
    ">

    <div style="font-size:20px;">
    Overall Vehicle Health
    </div>

    <div class="{status_class}"
         style="font-size:35px;font-weight:bold;">
    ● {vehicle_status}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SENSOR CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


# ---------------- ENGINE ----------------

with col1:

    if temperature < 70:
        temp_status = "warning"
        temp_message = "🟡 Low Temperature"
    elif temperature > 100:
        temp_status = "danger"
        temp_message = "🔴 Overheating"
    else:
        temp_status = "normal"
        temp_message = "🟢 Normal"

    st.markdown(
        f"""
        <div class="sensor-card">

        <div class="sensor-label">
        🌡️ ENGINE TEMPERATURE
        </div>

        <div class="sensor-value {temp_status}">
        {temperature:.1f} °C
        </div>

        <div>
        {temp_message}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- OIL ----------------

with col2:

    if oil_pressure < 25:

        oil_status = "danger"
        oil_message = "🔴 Low Pressure"

    elif oil_pressure > 65:

        oil_status = "danger"
        oil_message = "🔴 High Pressure"

    else:

        oil_status = "normal"
        oil_message = "🟢 Normal"

    st.markdown(
        f"""
        <div class="sensor-card">

        <div class="sensor-label">
        🛢️ OIL PRESSURE
        </div>

        <div class="sensor-value {oil_status}">
        {oil_pressure:.1f} PSI
        </div>

        <div>
        {oil_message}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- BATTERY ----------------

with col3:

    if battery_voltage < 11.5:

        battery_status = "danger"
        battery_message = "🔴 Low Voltage"

    elif battery_voltage > 15:

        battery_status = "danger"
        battery_message = "🔴 High Voltage"

    else:

        battery_status = "normal"
        battery_message = "🟢 Normal"

    st.markdown(
        f"""
        <div class="sensor-card">

        <div class="sensor-label">
        🔋 BATTERY VOLTAGE
        </div>

        <div class="sensor-value {battery_status}">
        {battery_voltage:.2f} V
        </div>

        <div>
        {battery_message}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- TIRE ----------------

with col4:

    if tire_pressure < 28:

        tire_status = "danger"
        tire_message = "🔴 Low Pressure"

    elif tire_pressure > 40:

        tire_status = "danger"
        tire_message = "🔴 High Pressure"

    else:

        tire_status = "normal"
        tire_message = "🟢 Normal"

    st.markdown(
        f"""
        <div class="sensor-card">

        <div class="sensor-label">
        🛞 TIRE PRESSURE
        </div>

        <div class="sensor-value {tire_status}">
        {tire_pressure:.1f} PSI
        </div>

        <div>
        {tire_message}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ALERT SECTION
# =========================================================

st.markdown("## 🚨 Vehicle Alerts")


if len(alerts) == 0:

    st.success(
        "✅ No active faults. All vehicle parameters are within safe limits."
    )

else:

    for alert_type, message in alerts:

        st.error(message)


# =========================================================
# LIVE SENSOR GRAPH
# =========================================================

st.markdown("## 📊 Live Sensor Monitoring")


history_df = pd.DataFrame(
    st.session_state.history
)


if not history_df.empty:

    chart_df = history_df.set_index("Time")

    st.line_chart(
        chart_df[
            [
                "Engine Temperature",
                "Oil Pressure"
            ]
        ]
    )


# =========================================================
# BATTERY & TIRE GRAPH
# =========================================================

if not history_df.empty:

    st.markdown("### 🔋 Battery & 🛞 Tire Pressure")

    chart_df2 = history_df.set_index("Time")

    st.line_chart(
        chart_df2[
            [
                "Battery Voltage",
                "Tire Pressure"
            ]
        ]
    )


# =========================================================
# CURRENT SIMULATION
# =========================================================

st.markdown("---")

st.markdown(
    f"""
    ### Current Simulation

    **Scenario:** `{scenario}`

    **Sensor readings generated:** `{st.session_state.counter}`

    **System:** 🟢 ONLINE

    **Data source:** Digital Sensor Simulation
    """
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#888;">
    Vehicle Health Monitoring System | Digital Prototype
    </div>
    """,
    unsafe_allow_html=True
)