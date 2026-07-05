import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# =====================================================================
# 1. COMPLETE UNIFIED PHYSICS, ASTROPHYSICS & RELATIVITY ENGINE
# =====================================================================
G = 6.67430e-11       # Gravitational Constant (m^3 kg^-1 s^-2)
M_EARTH = 5.972e24     # Mass of Earth (kg)
R_EARTH = 6.371e6      # Mean Radius of Earth (meters)
M_SUN = 1.989e30       # Mass of Sun (kg)
SIGMA = 5.670374e-8   # Stefan-Boltzmann constant (W m^-2 K^-4)
AU = 1.496e11         # 1 Astronomical Unit in meters
L_SUN = 3.828e26      # Luminosity of the Sun (Watts)
C = 299792458         # Speed of Light (m/s)

def calculate_escape_velocity(mass, radius):
    if mass <= 0 or radius <= 0: raise ValueError("Inputs must be positive.")
    return math.sqrt((2 * G * mass) / radius)

def calculate_orbital_period(mass, semi_major_axis):
    if mass <= 0 or semi_major_axis <= 0: raise ValueError("Inputs must be positive.")
    numerator = 4 * (math.pi ** 2) * (semi_major_axis ** 3)
    denominator = G * mass
    return math.sqrt(numerator / denominator)

def calculate_vis_viva_velocity(mass, current_radius, semi_major_axis):
    if mass <= 0 or current_radius <= 0 or semi_major_axis <= 0: raise ValueError("Inputs must be positive.")
    inside_brackets = (2 / current_radius) - (1 / semi_major_axis)
    if inside_brackets <= 0: raise ValueError("Invalid orbital geometry mapping.")
    return math.sqrt(G * mass * inside_brackets)

def calculate_stellar_luminosity(radius, temperature):
    if radius <= 0 or temperature <= 0: raise ValueError("Inputs must be positive.")
    return 4 * math.pi * (radius ** 2) * SIGMA * (temperature ** 4)

def calculate_habitable_zone(luminosity):
    l_relative = luminosity / L_SUN
    r_inner = math.sqrt(l_relative / 1.1)
    r_outer = math.sqrt(l_relative / 0.53)
    return r_inner, r_outer

def calculate_time_dilation(mass, radius):
    """Calculates the time dilation factor based on Schwarzschild metric."""
    schwarzschild_r = (2 * G * mass) / (C ** 2)
    if radius <= schwarzschild_r:
        return float('inf') # Horizon Crossed
    return math.sqrt(1 - (schwarzschild_r / radius))

# =====================================================================
# 2. STREAMLIT FRAMEWORK LAYOUT
# =====================================================================
st.set_page_config(page_title="ASTRID Astrophysics Lab", layout="wide")

st.markdown("""
    <style>
    .brand-title { font-size: 28px !important; font-weight: 300 !important; letter-spacing: 2px; }
    h3 { font-size: 14px !important; text-transform: uppercase; letter-spacing: 1px; margin-top: 20px !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="brand-title">ASTRID ASTROPHYSICS LAB</div>', unsafe_allow_html=True)
st.caption("Advanced Orbital Kinematics, Stellar Flux & Relativistic Time Matrix Engine")
st.markdown("---")

mode = st.sidebar.radio("Select Research Domain", ["Orbital Kinematics & Vectors", "Stellar Flux & Habitable Zones", "Relativistic Time Dilation"])

# ---------- DOMAIN 1: ORBITAL KINEMATICS WITH DYNAMIC VECTORS ----------
if mode == "Orbital Kinematics & Vectors":
    st.sidebar.markdown("### Celestial Body Engine")
    body_choice = st.sidebar.selectbox("Select Central Mass Reference", ["Earth", "Sun", "Custom Configuration"])

    if body_choice == "Earth":
        M, R = M_EARTH, R_EARTH
    elif body_choice == "Sun":
        M, R = M_SUN, 6.9634e8
    else:
        M = st.sidebar.number_input("Custom Mass (kg)", value=5.0e24, format="%.3e")
        R = st.sidebar.number_input("Custom Radius (m)", value=6.0e6, format="%.3e")

    st.sidebar.info(f"Mass: {M:.3e} kg\n\nRadius: {R/1000:,.1f} km")

    tab1, tab2 = st.columns([1.2, 1.8])

    with tab1:
        st.markdown("### Telemetry Solvers")
        with st.expander("🌌 Escape Velocity Matrix", expanded=True):
            v_esc = calculate_escape_velocity(M, R)
            st.metric(label="Escape Velocity ($v_{esc}$)", value=f"{v_esc / 1000:.3f} km/s")

        with st.expander("⏳ Keplerian Orbit Period Resolver", expanded=True):
            alt = st.number_input("Orbit Altitude Above Surface (km)", value=400.0, step=50.0)
            semi_major_axis = R + (alt * 1000)
            try:
                period_seconds = calculate_orbital_period(M, semi_major_axis)
                st.metric("Orbital Period", f"{period_seconds / 3600:.2f} Hours")
            except Exception as e:
                st.error(f"Invalid parameters: {e}")

        with st.expander("⚡ Instantaneous Speed & Velocity Vector", expanded=True):
            eccentricity = st.slider("Orbital Eccentricity ($e$)", min_value=0.0, max_value=0.6, value=0.3, step=0.05)
            r_perigee = semi_major_axis * (1 - eccentricity)
            r_apogee = semi_major_axis * (1 + eccentricity)
            
            orbit_position = st.select_slider("Position Selector", options=["Perigee", "Mid-Orbit", "Apogee"])
            current_r = r_perigee if orbit_position == "Perigee" else (r_apogee if orbit_position == "Apogee" else semi_major_axis)
                
            try:
                v_inst = calculate_vis_viva_velocity(M, current_r, semi_major_axis)
                st.metric("Instantaneous Speed ($v$)", f"{v_inst / 1000:.3f} km/s")
            except Exception as e:
                st.error(f"Geometry error: {e}")

    with tab2:
        st.markdown("### Dynamic Trajectory Engine Map with Velocity Vectors")
        theta = np.linspace(0, 2 * np.pi, 200)
        a_plot = semi_major_axis / 1000
        b_plot = a_plot * np.sqrt(1 - eccentricity**2)
        c_shift = a_plot * eccentricity
        
        # Spacecraft specific dynamic configurations
        if orbit_position == "Perigee":
            sc_x, sc_y = a_plot - c_shift, 0
            vy = (v_inst / 1000) * 15  # Scale vector size for visualization
            vx = 0
        elif orbit_position == "Apogee":
            sc_x, sc_y = -a_plot - c_shift, 0
            vy = -(v_inst / 1000) * 15
            vx = 0
        else:
            sc_x, sc_y = 0 - c_shift, b_plot
            vx = -(v_inst / 1000) * 15
            vy = 0

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=25, color='#1f77b4'), name=body_choice))
        fig.add_trace(go.Scatter(x=a_plot*np.cos(theta)-c_shift, y=b_plot*np.sin(theta), mode='lines', line=dict(color='#00ffcc', width=2, dash='dash'), name="Orbit Path"))
        fig.add_trace(go.Scatter(x=[sc_x], y=[sc_y], mode='markers', marker=dict(size=12, color='#ffffff'), name="Asset Vector"))
        
        # Adding Velocity Vector Arrow
        fig.add_annotation(
            x=sc_x + vx, y=sc_y + vy, ax=sc_x, ay=sc_y,
            xref="x", yref="y", axref="x", ayref="y",
            text="", showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor="#ff3366"
        )
        
        fig.update_layout(template="plotly_dark", xaxis=dict(title="X (km)", scaleanchor="y"), yaxis=dict(title="Y (km)"), height=500)
        st.plotly_chart(fig, use_container_width=True)

# ---------- DOMAIN 2: STELLAR FLUX & HABITABLE ZONES ----------
elif mode == "Stellar Flux & Habitable Zones":
    st.sidebar.markdown("### Star Classification Specs")
    star_type = st.sidebar.selectbox("Preset Star Type", ["Sol (Our Sun)", "Sirius (Bright A-type)", "Proxima Centauri (Red Dwarf)", "Custom Star"])
    
    if star_type == "Sol (Our Sun)":
        t_star, r_star = 5778, 6.9634e8
    elif star_type == "Sirius (Bright A-type)":
        t_star, r_star = 9940, 6.9634e8 * 1.711
    elif star_type == "Proxima Centauri (Red Dwarf)":
        t_star, r_star = 3042, 6.9634e8 * 0.154
    else:
        t_star = st.sidebar.slider("Surface Temperature (K)", min_value=2000, max_value=30000, value=5778, step=500)
        r_star = st.sidebar.number_input("Star Radius (meters)", value=6.9634e8, format="%.3e")

    left, right = st.columns([1.2, 1.8])
    with left:
        st.markdown("### Stellar Thermodynamics")
        L = calculate_stellar_luminosity(r_star, t_star)
        r_inner, r_outer = calculate_habitable_zone(L)
        st.metric("Total Luminosity ($L$)", value=f"{L / L_SUN:.3f} L☉", delta=f"{L:.2e} Watts")
        st.markdown("---")
        st.markdown("#### Habitable Zone Boundaries")
        st.info(f"🟢 **Inner Edge (Boiling Limit):** {r_inner:.3f} AU\n\n❄️ **Outer Edge (Freezing Limit):** {r_outer:.3f} AU")
        
    with right:
        st.markdown("### Radial Goldilocks Zone Visualization")
        angles = np.linspace(0, 2*np.pi, 200)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=30, color='#ffaa00'), name="Star Center"))
        fig.add_trace(go.Scatter(x=r_inner*np.cos(angles), y=r_inner*np.sin(angles), mode='lines', line=dict(color='#ff4b4b', width=1.5), name="Inner Boundary"))
        fig.add_trace(go.Scatter(x=r_outer*np.cos(angles), y=r_outer*np.sin(angles), mode='lines', line=dict(color='#4b4bff', width=1.5), name="Outer Boundary"))
        
        fig.add_shape(type="circle", x0=-r_outer, y0=-r_outer, x1=r_outer, y1=r_outer, line_color="rgba(0,0,0,0)", fillcolor="rgba(0, 255, 100, 0.15)", layer="below")
        fig.add_shape(type="circle", x0=-r_inner, y0=-r_inner, x1=r_inner, y1=r_inner, line_color="rgba(0,0,0,0)", fillcolor="rgba(11, 15, 26, 1)", layer="below")
        
        fig.update_layout(template="plotly_dark", xaxis=dict(title="Distance (AU)", scaleanchor="y"), yaxis=dict(title="Distance (AU)"), height=500)
        st.plotly_chart(fig, use_container_width=True)

# ---------- DOMAIN 3: RELATIVISTIC TIME DILATION MATRIX ----------
else:
    st.sidebar.markdown("### Deep Space Massive Body")
    compact_object = st.sidebar.selectbox("Select Singularity Reference", ["Custom Black Hole", "Intermediate Mass Black Hole", "Supermassive Black Hole"])
    
    if compact_object == "Custom Black Hole":
        m_obj = st.sidebar.number_input("Mass (Solar Masses - M☉)", value=10.0, step=5.0) * M_SUN
    elif compact_object == "Intermediate Mass Black Hole":
        m_obj = 1000 * M_SUN
    else:
        m_obj = 4.15e6 * M_SUN # Sagittarius A* Mass Specs
        
    schwarzschild_radius = (2 * G * m_obj) / (C ** 2)
    st.sidebar.warning(f"Event Horizon ($R_s$): {schwarzschild_radius/1000:,.2f} km")
    
    col_rel_l, col_rel_r = st.columns([1.2, 1.8])
    
    with col_rel_l:
        st.markdown("### Schwarzschild Spacetime Engine")
        orbit_multiplier = st.slider("Distance from Singularity (Multiples of $R_s$)", min_value=1.01, max_value=15.0, value=2.0, step=0.1)
        target_r = orbit_multiplier * schwarzschild_radius
        
        time_factor = calculate_time_dilation(m_obj, target_r)
        
        st.metric("Gravitational Shift Factor ($\gamma_{g}$)", value=f"{time_factor:.5f}")
        st.markdown("---")
        
        if time_factor > 0:
            earth_years = 1.0 / time_factor
            st.info(f"⏳ **Spacetime Variance Profile:**\n\nFor every **1.0 Hour** elapsed inside your spacecraft on this vector, exactly **{earth_years:.2f} Hours** pass back on planet Earth.")
        else:
            st.error("🚨 CRITICAL ALERT: Event Horizon crossed. Gravitational singularity escape vector non-existent.")

    with col_rel_r:
        st.markdown("### General Relativity Dilations Sweep")
        # Generate data curve mapping distance vs time dilation factor
        r_sweep = np.linspace(1.02 * schwarzschild_radius, 10 * schwarzschild_radius, 300)
        t_sweep = [calculate_time_dilation(m_obj, ri) for ri in r_sweep]
        earth_hours_sweep = [1.0 / ti if ti > 0 else None for ti in t_sweep]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=r_sweep / schwarzschild_radius, y=earth_hours_sweep, mode='lines', line=dict(color='#ff00ff', width=3), name="Time Dilated Matrix"))
        
        # Current Position Node Marker
        fig.add_trace(go.Scatter(x=[orbit_multiplier], y=[1.0 / time_factor if time_factor > 0 else 0], mode='markers', marker=dict(size=12, color='#ffffff'), name="Current Position Vector"))
        
        fig.update_layout(
            template="plotly_dark",
            xaxis=dict(title="Distance from Singularity (Radial Multiples of Rs)", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Hours Passed on Earth per Hour on Craft", gridcolor='rgba(255,255,255,0.05)'),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)