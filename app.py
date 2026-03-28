import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ── Données simulées ──────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
revenue = np.cumsum(np.random.randint(500, 2000, 30)) + 10000
visitors = np.random.randint(800, 3000, 30)
conversions = (visitors * np.random.uniform(0.03, 0.08, 30)).astype(int)

df_time = pd.DataFrame({
    'date': dates,
    'revenue': revenue,
    'visitors': visitors,
    'conversions': conversions,
})

products = ['Analytics Pro', 'DataSync', 'CloudBoard', 'InsightAI', 'FlowKit']
product_revenue = [45200, 38700, 29400, 52100, 18900]
product_growth = [12.4, -3.2, 8.7, 23.1, 5.6]

regions = ['Afrique', 'Europe', 'Amériques', 'Asie-Pacifique', 'Moyen-Orient']
region_sales = [23000, 41000, 35000, 28000, 12000]

# ── App ───────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = "Business Intelligence Dashboard"
server = app.server  # pour le déploiement

# ── Palette ───────────────────────────────────────────────────────────────────
COLORS = {
    'bg': '#0F1117',
    'surface': '#1A1D27',
    'card': '#1E2132',
    'accent': '#6C63FF',
    'accent2': '#00D4AA',
    'accent3': '#FF6B6B',
    'accent4': '#FFD166',
    'text': '#E8E9F3',
    'muted': '#8B8FA8',
    'border': '#2A2D3E',
}

FONT = "Inter, -apple-system, BlinkMacSystemFont, sans-serif"

# ── Layout helpers ────────────────────────────────────────────────────────────
def kpi_card(title, value, delta, color, icon):
    is_positive = delta.startswith('+')
    delta_color = '#00D4AA' if is_positive else '#FF6B6B'
    return html.Div([
        html.Div([
            html.Span(icon, style={'fontSize': '22px'}),
            html.Span(title, style={'color': COLORS['muted'], 'fontSize': '12px',
                                     'textTransform': 'uppercase', 'letterSpacing': '1px'}),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px', 'marginBottom': '12px'}),
        html.Div(value, style={'fontSize': '28px', 'fontWeight': '700', 'color': COLORS['text'],
                                'marginBottom': '6px'}),
        html.Div(delta + ' vs mois préc.', style={'fontSize': '12px', 'color': delta_color,
                                                    'fontWeight': '500'}),
        html.Div(style={
            'position': 'absolute', 'top': 0, 'left': 0, 'width': '4px',
            'height': '100%', 'background': color,
            'borderRadius': '8px 0 0 8px'
        }),
    ], style={
        'background': COLORS['card'],
        'borderRadius': '12px',
        'padding': '20px 20px 20px 24px',
        'border': f"1px solid {COLORS['border']}",
        'position': 'relative',
        'overflow': 'hidden',
        'flex': '1',
        'minWidth': '160px',
    })


# ── Figures ───────────────────────────────────────────────────────────────────
def make_revenue_chart():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_time['date'], y=df_time['revenue'],
        name='Revenus', fill='tozeroy',
        line=dict(color=COLORS['accent'], width=2.5),
        fillcolor='rgba(108,99,255,0.12)',
        hovertemplate='%{x|%d %b}<br><b>%{y:,.0f} FCFA</b><extra></extra>',
    ))
    fig.add_trace(go.Scatter(
        x=df_time['date'], y=df_time['visitors'],
        name='Visiteurs', yaxis='y2',
        line=dict(color=COLORS['accent2'], width=1.5, dash='dot'),
        hovertemplate='%{x|%d %b}<br><b>%{y:,} visiteurs</b><extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT, color=COLORS['muted'], size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation='h', x=0, y=1.1, font=dict(size=11)),
        hovermode='x unified',
        xaxis=dict(showgrid=False, showline=False, tickformat='%d %b'),
        yaxis=dict(showgrid=True, gridcolor=COLORS['border'], showline=False, tickformat=',.0f'),
        yaxis2=dict(overlaying='y', side='right', showgrid=False, showline=False),
    )
    return fig


def make_product_bar():
    colors = [COLORS['accent'], COLORS['accent2'], COLORS['accent4'],
              COLORS['accent3'], '#A78BFA']
    fig = go.Figure(go.Bar(
        x=products, y=product_revenue,
        marker_color=colors,
        text=[f'{r/1000:.0f}k' for r in product_revenue],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=11),
        hovertemplate='<b>%{x}</b><br>%{y:,.0f} FCFA<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT, color=COLORS['muted'], size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor=COLORS['border'], tickformat=',.0f'),
        showlegend=False,
    )
    return fig


def make_region_donut():
    fig = go.Figure(go.Pie(
        labels=regions, values=region_sales,
        hole=0.62,
        marker=dict(colors=[COLORS['accent'], COLORS['accent2'], COLORS['accent4'],
                             COLORS['accent3'], '#A78BFA'],
                    line=dict(color=COLORS['bg'], width=2)),
        textinfo='label+percent',
        textfont=dict(size=11, color=COLORS['text']),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} FCFA<br>%{percent}<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT, color=COLORS['muted'], size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        annotations=[dict(text='Ventes', x=0.5, y=0.5, font_size=14,
                          font_color=COLORS['muted'], showarrow=False)],
    )
    return fig


def make_conv_gauge():
    val = round(float(df_time['conversions'].sum() / df_time['visitors'].sum() * 100), 1)
    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=val,
        delta={'reference': 5.2, 'valueformat': '.1f'},
        number={'suffix': '%', 'font': {'size': 32, 'color': COLORS['text']}},
        gauge={
            'axis': {'range': [0, 10], 'tickfont': {'color': COLORS['muted'], 'size': 10}},
            'bar': {'color': COLORS['accent2']},
            'bgcolor': COLORS['border'],
            'steps': [
                {'range': [0, 3], 'color': COLORS['surface']},
                {'range': [3, 6], 'color': '#1A2A3A'},
                {'range': [6, 10], 'color': '#0A2A1A'},
            ],
            'threshold': {'line': {'color': COLORS['accent'], 'width': 2}, 'value': 7},
        },
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT, color=COLORS['muted']),
        margin=dict(l=20, r=20, t=30, b=10),
        height=200,
    )
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────
card_style = {
    'background': COLORS['card'],
    'borderRadius': '12px',
    'padding': '20px',
    'border': f"1px solid {COLORS['border']}",
}

section_title = lambda t: html.H3(t, style={
    'color': COLORS['text'], 'fontSize': '14px', 'fontWeight': '600',
    'marginBottom': '14px', 'textTransform': 'uppercase', 'letterSpacing': '1px',
})

app.layout = html.Div([
    # ─ Header ─
    html.Div([
        html.Div([
            html.Div('●', style={'color': COLORS['accent'], 'fontSize': '20px'}),
            html.H1('BI Dashboard', style={
                'color': COLORS['text'], 'fontSize': '20px',
                'fontWeight': '700', 'margin': 0,
            }),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),
        html.Div([
            html.Span('●', style={'color': COLORS['accent2'], 'marginRight': '6px', 'fontSize': '10px'}),
            html.Span('Live · Douala, CM', style={'color': COLORS['muted'], 'fontSize': '12px'}),
        ], style={'display': 'flex', 'alignItems': 'center'}),
    ], style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'padding': '16px 24px', 'borderBottom': f"1px solid {COLORS['border']}",
        'background': COLORS['surface'],
    }),

    # ─ Body ─
    html.Div([
        # ─ KPI row ─
        html.Div([
            kpi_card('Revenus', '184 300 FCFA', '+18.4%', COLORS['accent'], '💰'),
            kpi_card('Visiteurs', '52 840', '+12.1%', COLORS['accent2'], '👥'),
            kpi_card('Conversions', '3 217', '+6.3%', COLORS['accent4'], '🎯'),
            kpi_card('Ticket moyen', '57 320 FCFA', '-2.8%', COLORS['accent3'], '🛒'),
        ], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap'}),

        # ─ Charts row 1 ─
        html.Div([
            html.Div([
                section_title('Revenus & Trafic — 30 jours'),
                dcc.Graph(figure=make_revenue_chart(), config={'displayModeBar': False},
                          style={'height': '220px'}),
            ], style={**card_style, 'flex': '2', 'minWidth': '280px'}),

            html.Div([
                section_title('Taux de conversion'),
                dcc.Graph(figure=make_conv_gauge(), config={'displayModeBar': False},
                          style={'height': '200px'}),
                html.P('Objectif : 7%', style={'color': COLORS['muted'], 'fontSize': '11px',
                                                'textAlign': 'center', 'marginTop': '-10px'}),
            ], style={**card_style, 'flex': '1', 'minWidth': '200px'}),
        ], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap', 'marginTop': '16px'}),

        # ─ Charts row 2 ─
        html.Div([
            html.Div([
                section_title('Revenus par produit'),
                dcc.Graph(figure=make_product_bar(), config={'displayModeBar': False},
                          style={'height': '220px'}),
            ], style={**card_style, 'flex': '2', 'minWidth': '280px'}),

            html.Div([
                section_title('Ventes par région'),
                dcc.Graph(figure=make_region_donut(), config={'displayModeBar': False},
                          style={'height': '220px'}),
            ], style={**card_style, 'flex': '1', 'minWidth': '200px'}),
        ], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap', 'marginTop': '16px'}),

        # ─ Table ─
        html.Div([
            section_title('Top produits — performances'),
            html.Table([
                html.Thead(html.Tr([
                    html.Th(c, style={'color': COLORS['muted'], 'fontSize': '11px',
                                      'textAlign': 'left', 'padding': '8px 12px',
                                      'borderBottom': f"1px solid {COLORS['border']}"})
                    for c in ['Produit', 'Revenus', 'Croissance', 'Statut']
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(products[i], style={'padding': '10px 12px', 'color': COLORS['text'],
                                                     'fontSize': '13px'}),
                        html.Td(f"{product_revenue[i]:,} FCFA", style={'padding': '10px 12px',
                                                                          'color': COLORS['text'], 'fontSize': '13px'}),
                        html.Td([
                            html.Span('▲ ' if product_growth[i] > 0 else '▼ ',
                                      style={'color': COLORS['accent2'] if product_growth[i] > 0 else COLORS['accent3']}),
                            f"{abs(product_growth[i])}%",
                        ], style={'padding': '10px 12px', 'fontSize': '13px',
                                  'color': COLORS['accent2'] if product_growth[i] > 0 else COLORS['accent3']}),
                        html.Td(
                            html.Span('Actif' if product_growth[i] > 0 else 'Surveillance',
                                      style={
                                          'background': 'rgba(0,212,170,0.15)' if product_growth[i] > 0 else 'rgba(255,107,107,0.15)',
                                          'color': COLORS['accent2'] if product_growth[i] > 0 else COLORS['accent3'],
                                          'padding': '3px 10px', 'borderRadius': '20px', 'fontSize': '11px',
                                      }),
                            style={'padding': '10px 12px'}),
                    ], style={'borderBottom': f"1px solid {COLORS['border']}"})
                    for i in range(len(products))
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse'}),
        ], style={**card_style, 'marginTop': '16px'}),

    ], style={'padding': '20px 24px', 'maxWidth': '1100px', 'margin': '0 auto'}),

], style={
    'background': COLORS['bg'],
    'minHeight': '100vh',
    'fontFamily': FONT,
})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
