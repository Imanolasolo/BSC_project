import streamlit as st
import sqlite3
from datetime import datetime

# -------------------------
# Database Setup
# -------------------------

conn = sqlite3.connect("sgs.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    name TEXT,
    email TEXT,
    company TEXT,
    interest TEXT
)
""")
conn.commit()

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Structural Growth System™",
    layout="centered"
)

# -------------------------
# Language Dictionaries
# -------------------------

TEXT = {
    "en": {
        "lang_label": "Language / Idioma",
        "lang_en": "English",
        "lang_es": "Spanish",
        "title": "Structural Growth System™",
        "subtitle": "Scale with stability. Grow without structural breakdown.",
        "hero_body": """Growth does not break companies.  
Weak structure does.

Structural Growth System™ is a partner-led operational infrastructure model designed for CEOs who want to scale without increasing chaos, friction or founder dependency.""",
        "problem_header": "Most companies don't fail because of strategy.",
        "problem_body": """They fail because:

- Decisions stay centralized  
- Roles overlap and create friction  
- Processes don't scale with volume  
- Growth amplifies structural weaknesses  
- The founder becomes the bottleneck""",
        "solution_header": "What is Structural Growth System™?",
        "solution_body": """Structural Growth System™ (SGS) is a proprietary operational infrastructure framework that:

- Measures structural stability  
- Detects friction before it escalates  
- Reduces founder dependency  
- Increases growth capacity  
- Stabilizes decision architecture""",
        "solution_extra": """Unlike traditional consulting, SGS is not a report.

It is a continuous structural monitoring and infrastructure partnership.""",
        "core_header": "Core Products",
        "exp_monitor_title": "SGS Monitor™",
        "exp_monitor_body": """SGS Monitor™ is the core entry point.

A continuous structural stability monitoring system that combines:

• Proprietary structural indices  
• Growth pressure measurement  
• Founder dependency tracking  
• Human strategic interpretation  
• Monthly executive structural review  

We don't take decisions for you.  
We design and monitor the infrastructure that supports them.""",
        "exp_diag_title": "Structural Growth Diagnostic™",
        "exp_diag_body": """A deep-dive structural assessment that maps your current architecture,
friction zones and founder dependencies.

Output:
• Structural risk map  
• Growth capacity baseline  
• Priority intervention zones""",
        "exp_modules_title": "Targeted Structural Modules",
        "exp_modules_body": """Modular interventions that address specific structural weaknesses identified
by SGS Monitor™ and the diagnostic.

Examples:
• Decision architecture redesign  
• Role clarity and accountability maps  
• Operating rhythm and escalation paths""",
        "how_header": "How It Works",
        "how_steps": """1️⃣ Structural Diagnostic  
2️⃣ Activate SGS Monitor™  
3️⃣ Identify structural risk zones  
4️⃣ Deploy targeted structural modules when needed  
5️⃣ Scale with stability""",
        "cta_header": "Activate Structural Clarity",
        "cta_body": """If you're scaling and feel increasing internal friction,  
your structure may be under stress.

Start with a Structural Growth Diagnostic.""",
        "form_name": "Name",
        "form_email": "Email",
        "form_company": "Company",
        "form_interest_label": "What are you most concerned about?",
        "form_interest_options": [
            "Founder Dependency",
            "Operational Friction",
            "Scaling Pressure",
            "Decision Bottlenecks",
            "General Structural Stability",
        ],
        "form_submit": "Request Structural Diagnostic",
        "success_msg": "Request received. We will contact you for the Structural Diagnostic.",
        "warning_msg": "Please complete at least name and email.",
        "footer": "Structural Growth System™ | Operational Infrastructure for Growth-Stage Companies",
    },
    "es": {
        "lang_label": "Idioma / Language",
        "lang_en": "Inglés",
        "lang_es": "Español",
        "title": "Structural Growth System™",
        "subtitle": "Escala con estabilidad. Crece sin que la estructura se rompa.",
        "hero_body": """El crecimiento no rompe las empresas.  
La estructura débil sí.

Structural Growth System™ es un modelo de infraestructura operativa liderado por partners, diseñado para CEOs que quieren escalar sin aumentar el caos, la fricción ni la dependencia del fundador.""",
        "problem_header": "La mayoría de las empresas no fallan por la estrategia.",
        "problem_body": """Fallan porque:

- Las decisiones permanecen centralizadas  
- Los roles se solapan y generan fricción  
- Los procesos no escalan con el volumen  
- El crecimiento amplifica las debilidades estructurales  
- El fundador se convierte en el cuello de botella""",
        "solution_header": "¿Qué es Structural Growth System™?",
        "solution_body": """Structural Growth System™ (SGS) es un marco propietario de infraestructura operativa que:

- Mide la estabilidad estructural  
- Detecta la fricción antes de que escale  
- Reduce la dependencia del fundador  
- Aumenta la capacidad de crecimiento  
- Estabiliza la arquitectura de decisión""",
        "solution_extra": """A diferencia de la consultoría tradicional, SGS no es un informe.

Es una alianza continua de monitorización estructural e infraestructura.""",
        "core_header": "Productos Core",
        "exp_monitor_title": "SGS Monitor™",
        "exp_monitor_body": """SGS Monitor™ es el punto de entrada principal.

Un sistema continuo de monitorización de estabilidad estructural que combina:

• Índices estructurales propietarios  
• Medición de la presión de crecimiento  
• Seguimiento de la dependencia del fundador  
• Interpretación estratégica humana  
• Revisión estructural ejecutiva mensual  

No tomamos decisiones por ti.  
Diseñamos y monitorizamos la infraestructura que las soporta.""",
        "exp_diag_title": "Structural Growth Diagnostic™",
        "exp_diag_body": """Una evaluación estructural en profundidad que mapea tu arquitectura actual,
las zonas de fricción y las dependencias del fundador.

Entregables:
• Mapa de riesgo estructural  
• Línea base de capacidad de crecimiento  
• Zonas de intervención prioritarias""",
        "exp_modules_title": "Módulos Estructurales Focalizados",
        "exp_modules_body": """Intervenciones modulares que abordan debilidades estructurales específicas identificadas
por SGS Monitor™ y el diagnóstico.

Ejemplos:
• Rediseño de la arquitectura de decisión  
• Mapas de rol, claridad y accountability  
• Ritmo operativo y rutas de escalado""",
        "how_header": "Cómo Funciona",
        "how_steps": """1️⃣ Diagnóstico estructural  
2️⃣ Activar SGS Monitor™  
3️⃣ Identificar zonas de riesgo estructural  
4️⃣ Desplegar módulos estructurales focalizados cuando sea necesario  
5️⃣ Escalar con estabilidad""",
        "cta_header": "Activa la Claridad Estructural",
        "cta_body": """Si estás escalando y percibes una fricción interna creciente,  
es posible que tu estructura esté bajo estrés.

Empieza con un Structural Growth Diagnostic.""",
        "form_name": "Nombre",
        "form_email": "Email",
        "form_company": "Empresa",
        "form_interest_label": "¿Qué es lo que más te preocupa?",
        "form_interest_options": [
            "Dependencia del fundador",
            "Fricción operativa",
            "Presión de escalado",
            "Cuellos de botella en la decisión",
            "Estabilidad estructural general",
        ],
        "form_submit": "Solicitar Structural Diagnostic",
        "success_msg": "Solicitud recibida. Nos pondremos en contacto para el Structural Diagnostic.",
        "warning_msg": "Por favor completa al menos nombre y email.",
        "footer": "Structural Growth System™ | Infraestructura Operativa para Empresas en Crecimiento",
    },
}

# -------------------------
# Language Selector
# -------------------------

lang_choice = st.radio(
    TEXT["en"]["lang_label"],
    options=["en", "es"],
    index=0,
    format_func=lambda x: TEXT["en"]["lang_en"] if x == "en" else TEXT["en"]["lang_es"],
    horizontal=True,
)

T = TEXT[lang_choice]

# -------------------------
# Hero Section
# -------------------------

st.title(T["title"])
st.subheader(T["subtitle"])

st.markdown(T["hero_body"])

st.markdown("---")

# -------------------------
# Problem Section
# -------------------------

st.header(T["problem_header"])
st.markdown(T["problem_body"])

st.markdown("---")

# -------------------------
# Solution Section
# -------------------------

st.header(T["solution_header"])

st.markdown(T["solution_body"])

st.markdown(T["solution_extra"])

st.markdown("---")

# -------------------------
# Core Product Section
# -------------------------

st.header(T["core_header"])

with st.expander(T["exp_monitor_title"], expanded=True):
    st.markdown(T["exp_monitor_body"])

with st.expander(T["exp_diag_title"]):
    st.markdown(T["exp_diag_body"])

with st.expander(T["exp_modules_title"]):
    st.markdown(T["exp_modules_body"])

st.markdown("---")

# -------------------------
# How It Works
# -------------------------

st.header(T["how_header"])

st.markdown(T["how_steps"])

st.markdown("---")

# -------------------------
# Call to Action
# -------------------------

st.header(T["cta_header"])

st.markdown(T["cta_body"])

with st.form("lead_form"):
    name = st.text_input(T["form_name"])
    email = st.text_input(T["form_email"])
    company = st.text_input(T["form_company"])
    interest = st.selectbox(
        T["form_interest_label"],
        T["form_interest_options"],
    )

    submitted = st.form_submit_button(T["form_submit"])

    if submitted:
        if name and email:
            c.execute(
                """
                INSERT INTO leads (timestamp, name, email, company, interest)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    name,
                    email,
                    company,
                    interest,
                ),
            )
            conn.commit()

            st.success(T["success_msg"])
        else:
            st.warning(T["warning_msg"])

st.markdown("---")

st.caption(T["footer"])