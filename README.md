# QALAT · App2 IRT · Sistema de Monitoreo de Resultados de Tratamiento

## Países
- Colombia (IRT)
- Panamá (IRT)
- Honduras (IRT)
- Costa Rica (IRT)
- República Dominicana (IRT)

## Arquitectura
- **Formularios HTML** (GitHub Pages): Captura de datos por país
- **Supabase**: Base de datos PostgreSQL en la nube (tabla `irt_registros`)
- **Streamlit**: App de gestión, reportes y panel de control

## Estructura
```
App-IRT-Paises/
├── app.py                    # Interfaz Streamlit
├── requirements.txt
├── packages.txt
├── pipeline/
│   ├── __init__.py
│   ├── wide_irt.py           # Motor de procesamiento IRT
│   └── panel/                # Módulos del panel de gestión
│       └── __init__.py
├── irt_colombia.html          # Formulario captura
├── irt_panama.html
├── irt_honduras.html
├── irt_costarica.html
├── irt_repdominicana.html
├── correccion_irt_colombia.html  # Formulario corrección
└── ...
```

## Desarrollado para
Proyecto QALAT · UNODC · 2026
