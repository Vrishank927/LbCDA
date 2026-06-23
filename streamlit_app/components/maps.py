from __future__ import annotations

import streamlit as st


def render_location_map(lat: float, lon: float, quality: float) -> None:
    """Placeholder for professional mapping.

    In this redesign, we keep it lightweight; if Mapbox keys are available,
    we can switch to pydeck/mapbox layers.
    """

    # Keep Folium optional at runtime; if unavailable, show a minimal marker.
    try:
        import folium
        from streamlit_folium import st_folium

        m = folium.Map(location=[lat, lon], zoom_start=12, tiles="CartoDB dark_matter")
        tone = "rgba(34,230,255,0.95)" if quality >= 0.75 else "rgba(255,200,87,0.95)" if quality >= 0.45 else "rgba(255,77,109,0.95)"
        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            color=tone,
            fill=True,
            fill_color=tone,
            fill_opacity=0.8,
            popup="Predicted location risk/health",
        ).add_to(m)
        st_folium(m, width=None, height=320)
    except Exception:
        st.markdown(
            f"""
            <div class="premium-card" style="padding:14px;">
              <div style="font-weight:900; margin-bottom:6px;">Map unavailable</div>
              <div style="color: rgba(255,255,255,0.7); font-size:13px;">
                Coordinates: ({lat:.4f}, {lon:.4f}) • Quality score: {quality:.2f}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

