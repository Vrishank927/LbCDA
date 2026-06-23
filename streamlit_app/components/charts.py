from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def plot_metric_line(x, y, title: str):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            line=dict(color="rgba(34,230,255,0.85)", width=3),
            marker=dict(size=7, color="rgba(34,230,255,0.95)"),
            hovertemplate="%{x}<br>%{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.85)"),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=False, tickfont=dict(color="rgba(255,255,255,0.6)")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
    )
    return fig


def plot_hist(data, title: str, xaxis: str):
    fig = px.histogram(
        x=data,
        nbins=30,
        title=title,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.85)"),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=False, tickfont=dict(color="rgba(255,255,255,0.6)"), title=xaxis),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        bargap=0.05,
    )
    fig.update_traces(marker_color="rgba(166,102,255,0.55)")
    return fig

