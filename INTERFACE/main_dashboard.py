"""
[GVIC Standard Operating Procedure]
File Name: main_dashboard.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

# -*- coding: utf-8 -*-
"""
================================================================================
LOCATION: C:/GVIC/app/scripts/
FILE NAME: main_dashboard.py
DATE: 2026-03-13
VERSION: v0.1 [GENESIS]
DESCRIPTION: Rebuilt from scratch. 3-Layer Architecture. Zero-Encoding Error.
================================================================================
"""

import dash
from dash import html, dcc, Input, Output, State, callback_context, ALL
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime
import json
import random

# Initializing App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
app.title = "GVIC COMMAND HUB v0.1"

# [CSS: HARMONIOUS DESIGN]
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}<title>{%title%}</title>{%favicon%}{%css%}
        <style>
            body { background-color: #05070a; font-family: 'Segoe UI', sans-serif; overflow-x: hidden; }
            .navbar { border-bottom: 2px solid #00d2ff; }
            .nav-link, .dropdown-toggle { font-size: 1.0rem !important; font-weight: 800 !important; color: #00d2ff !important; }
            
            /* LAYER 1: MONITORING CARDS */
            .monitor-card { background: rgba(10, 15, 20, 0.95); border: 1px solid #333; height: 530px; border-radius: 12px; }
            .metric-box { border-bottom: 1px solid #222; padding: 12px 0; }
            .metric-label { font-size: 0.8rem; color: #888; margin-bottom: 4px; }
            .metric-value { font-size: 1.5rem; font-weight: 900; }
            
            /* LAYER 3: OVERLAY DESIGN */
            #overlay-layer {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                z-index: 999999 !important; background: radial-gradient(circle, #0a111a 0%, #05070a 100%);
                display: none; padding: 40px; overflow-y: auto; border: 4px solid #00d2ff;
            }
            .folder-card { background: rgba(0, 210, 255, 0.05); border-left: 5px solid #00d2ff; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
            .item-3rd { color: #00ff88; font-size: 1.1rem; font-weight: bold; margin-top: 10px; cursor: pointer; padding: 8px; transition: 0.2s; }
            .item-3rd:hover { background: rgba(0, 255, 136, 0.15); color: #fff; padding-left: 15px; border-radius: 4px; }
            
            .status-card { padding: 15px; border-radius: 10px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
            .bg-red { border: 1px solid #ff4136; background: rgba(255, 65, 54, 0.15); color: #ff4136; }
            .bg-yellow { border: 1px solid #ffb700; background: rgba(255, 183, 0, 0.15); color: #ffb700; }
            .bg-green { border: 1px solid #2ecc40; background: rgba(46, 204, 64, 0.15); color: #2ecc40; }
            .cumulative-box { background: #080a0d; border-top: 1px solid #333; padding: 10px; font-size: 0.9rem; color: #00d2ff; margin-bottom: 25px; border-radius: 0 0 8px 8px; }
        </style>
    </head>
    <body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>
'''

# [DATABASE: 13 PATHS HIERARCHY]
IMPERIAL_DB = {
    "nav-1-1": {"title": "GATEKEEPER 1.1", "subtitle": "IDENTITY & MARKET FILTER", "folders": [{"name": "Auth", "items": ["ID Verification", "Staff List Sync"]}, {"name": "Market", "items": ["API Token", "Logistics Map"]}]},
    "nav-1-2": {"title": "GATEKEEPER 1.2", "subtitle": "BILLING SETUP", "folders": [{"name": "Finance", "items": ["Deposit Status", "Fee Config"]}]},
    "nav-2-1": {"title": "HEART 2.1", "subtitle": "8-EVILS MONITORING", "folders": [{"name": "Inventory", "items": ["Stock Out", "Negative Margin"]}]},
    "nav-2-2": {"title": "HEART 2.2", "subtitle": "ANALYTICS HUB", "folders": [{"name": "Sales", "items": ["GMV Trend", "Conversion"]}]},
    "nav-2-3": {"title": "HEART 2.3", "subtitle": "SUB ENGINE", "folders": [{"name": "Retention", "items": ["Renewal Status", "Churn Analysis"]}]},
    "nav-3-1": {"title": "IMMUNITY 3.1", "subtitle": "THREAT DETECTION", "folders": [{"name": "Security", "items": ["API Abuse", "Fraud Detect"]}]},
    "nav-3-2": {"title": "IMMUNITY 3.2", "subtitle": "PURGE EXECUTION", "folders": [{"name": "Action", "items": ["Account Suspend", "IP Block"]}]},
    "nav-3-3": {"title": "IMMUNITY 3.3", "subtitle": "POST-CLEANUP", "folders": [{"name": "Audit", "items": ["Exit Log", "Refund"]}]},
    "nav-4-1": {"title": "BRAIN 4.1", "subtitle": "PREDICTIVE RESOURCE", "folders": [{"name": "AI", "items": ["Server Forecast", "Load Balance"]}]},
    "nav-4-2": {"title": "BRAIN 4.2", "subtitle": "RESOURCE ROI", "folders": [{"name": "Efficiency", "items": ["Cost Analysis", "Model ROI"]}]},
    "nav-5-1": {"title": "SPINE 5.1", "subtitle": "COMPLIANCE VAULT", "folders": [{"name": "Legal", "items": ["Policy Version", "Privacy Sync"]}]},
    "nav-5-2": {"title": "SPINE 5.2", "subtitle": "SECURE CONNECTION", "folders": [{"name": "Network", "items": ["VPN Tunnel", "Encryption"]}]},
    "nav-5-3": {"title": "SPINE 5.3", "subtitle": "SYSTEM GOVERNANCE", "folders": [{"name": "Master", "items": ["Emergency Kill-Switch", "Audit Log"]}]}
}

# [NAVBAR CONSTRUCTION]
def make_nav():
    return dbc.Navbar(dbc.Container([
        dbc.NavbarBrand("🛡️ GVIC COMMAND HUB v0.1", href="/", className="me-4 fw-bold"),
        dbc.Nav([
            dbc.DropdownMenu([dbc.DropdownMenuItem("1.1 Filter", id="nav-1-1"), dbc.DropdownMenuItem("1.2 Billing", id="nav-1-2")], nav=True, label="GATEKEEPER"),
            dbc.DropdownMenu([dbc.DropdownMenuItem("2.1 8-Evils", id="nav-2-1"), dbc.DropdownMenuItem("2.2 Analytics", id="nav-2-2"), dbc.DropdownMenuItem("2.3 Sub", id="nav-2-3")], nav=True, label="HEART"),
            dbc.DropdownMenu([dbc.DropdownMenuItem("3.1 Threat", id="nav-3-1"), dbc.DropdownMenuItem("3.2 Purge", id="nav-3-2"), dbc.DropdownMenuItem("3.3 Cleanup", id="nav-3-3")], nav=True, label="IMMUNITY"),
            dbc.DropdownMenu([dbc.DropdownMenuItem("4.1 Predictive", id="nav-4-1"), dbc.DropdownMenuItem("4.2 ROI", id="nav-4-2")], nav=True, label="BRAIN"),
            dbc.DropdownMenu([dbc.DropdownMenuItem("5.1 Compliance", id="nav-5-1"), dbc.DropdownMenuItem("5.2 Secure", id="nav-5-2"), dbc.DropdownMenuItem("5.3 Governance", id="nav-5-3")], nav=True, label="SPINE"),
        ], className="mx-auto", navbar=True),
    ], fluid=True), color="dark", dark=True, className="sticky-top shadow-lg")

# [MAIN LAYOUT]
app.layout = dbc.Container([
    dcc.Interval(id='pulse-5s', interval=5000, n_intervals=0),
    make_nav(),
    
    # LAYER 1: 3 MAIN SURVEILLANCE AREAS
    html.Div([
        dbc.Row([
            # 1. Strategic Risk Radar
            dbc.Col(dbc.Card([
                dbc.CardHeader("1. STRATEGIC RISK RADAR", className="fw-bold text-info"),
                dbc.CardBody(dcc.Graph(id='main-risk-radar', config={'displayModeBar': False}))
            ], className="monitor-card"), width=4),
            
            # 2. Seller Metrics (3-Stages)
            dbc.Col(dbc.Card([
                dbc.CardHeader("2. SELLER METRICS (STAGES)", className="fw-bold text-success"),
                dbc.CardBody([
                    html.Div(id='main-seller-stats'),
                    dcc.Graph(id='main-seller-trend', config={'displayModeBar': False})
                ])
            ], className="monitor-card"), width=4),
            
            # 3. Infra Status Gauge
            dbc.Col(dbc.Card([
                dbc.CardHeader("3. INFRASTRUCTURE STATUS", className="fw-bold text-warning"),
                dbc.CardBody([
                    html.H5(id='main-infra-status', className="text-center mb-4"),
                    dcc.Graph(id='main-infra-gauge', config={'displayModeBar': False})
                ])
            ], className="monitor-card"), width=4),
        ], className="mt-4 g-3"),
        
        # LAYER 3: ACTION OVERLAY (HIDDEN)
        html.Div(id="overlay-layer", children=[
            dbc.Button("CLOSE COMMAND [X]", id="close-btn", color="danger", className="float-end fw-bold", n_clicks=0),
            html.Div(id="overlay-content", className="mt-5")
        ])
    ], className="px-2"),
    
    html.Footer(id='main-footer', className="text-center text-muted mt-5 small")
], fluid=True)

# [CALLBACK: LAYER 1 - CORE MONITORING ENGINE]
@app.callback(
    [Output('main-risk-radar', 'figure'), Output('main-seller-stats', 'children'), 
     Output('main-seller-trend', 'figure'), Output('main-infra-status', 'children'), 
     Output('main-infra-gauge', 'figure'), Output('main-footer', 'children')],
    [Input('pulse-5s', 'n_intervals')]
)
def update_surveillance(n):
    # Radar Data
    risk = go.Figure(data=go.Scatterpolar(r=[random.randint(30, 80) for _ in range(8)], theta=['Stock','Margin','Pay','Cash','Ad','Data','Return','Ship'], fill='toself')).update_layout(template="plotly_dark", height=430, margin=dict(l=40,r=40,t=20,b=20), paper_bgcolor='rgba(0,0,0,0)')
    
    # Seller Data
    new_d, total_c, active_n = 45 + random.randint(-5,5), 25118 + n, 24519 + random.randint(-10,10)
    stats_ui = html.Div([
        html.Div([html.P("Daily New Count:", className="metric-label"), html.Div(f"+{new_d}", className="metric-value text-info")], className="metric-box"),
        html.Div([html.P("Total Cumulative Sellers:", className="metric-label"), html.Div(f"{total_c:,}", className="metric-value text-success")], className="metric-box"),
        html.Div([html.P("Currently Active Sellers:", className="metric-label"), html.Div(f"{active_n:,}", className="metric-value text-warning")], className="metric-box"),
    ])
    trend = go.Figure(data=go.Scatter(y=[random.randint(180,220) for _ in range(12)], line=dict(color='#00ff88', width=2), fill='tozeroy')).update_layout(template="plotly_dark", height=150, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', xaxis={'visible': False}, yaxis={'visible': False})
    
    # Infra Data
    gauge = go.Figure(go.Indicator(mode="gauge+number", value=random.randint(20,28))).update_layout(template="plotly_dark", height=320, paper_bgcolor='rgba(0,0,0,0)')
    
    return risk, stats_ui, trend, "SYSTEM STATUS: OPTIMAL", gauge, f"GVIC COMMAND ENGINE v0.1 ACTIVE | {datetime.now().strftime('%H:%M:%S')}"

# [CALLBACK: LAYER 2 & 3 - NAVIGATION & ACTION HUB]
@app.callback(
    [Output("overlay-layer", "style"), Output("overlay-content", "children")],
    [Input(f"nav-{i}-{j}", "n_clicks") for i in range(1, 6) for j in range(1, 4) if f"nav-{i}-{j}" in IMPERIAL_DB] + [Input("close-btn", "n_clicks")],
    prevent_initial_call=True
)
def handle_navigation(*args):
    ctx = callback_context
    if not ctx.triggered: return {"display": "none"}, ""
    tid = ctx.triggered[0]['prop_id'].split('.')[0]
    if tid == "close-btn": return {"display": "none"}, ""
    
    info = IMPERIAL_DB.get(tid)
    if info:
        content = html.Div([
            html.H1(info["title"], className="text-info fw-bold"),
            html.P(info["subtitle"], className="text-muted small mb-4"),
            dbc.Row([
                dbc.Col([ # Folder List
                    html.Div([html.Div([
                        html.H5(f["name"], className="text-info mb-3"),
                        html.Div([html.Div(item, className="item-3rd", id={'type': 'level-3', 'id': item}) for item in f["items"]])
                    ], className="folder-card") for f in info["folders"]])
                ], width=4),
                dbc.Col([ # Action Monitor
                    html.Div(id="overlay-monitor", className="monitor-panel", style={"background":"rgba(0,0,0,0.6)", "borderRadius":"12px", "padding":"25px", "minHeight":"550px"}, children=[
                        html.Div(style={"textAlign":"center", "paddingTop":"200px"}, children=[html.H3("📡 WAITING FOR PARAMETER SCAN", className="text-muted")])
                    ])
                ], width=8)
            ])
        ])
        return {"display": "block"}, content
    return {"display": "none"}, ""

@app.callback(
    Output("overlay-monitor", "children"),
    [Input({'type': 'level-3', 'id': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def run_action_stats(n_clicks):
    ctx = callback_context
    if not any(n_clicks): return dash.no_update
    clicked_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['id']
    n_r, n_y, n_g = random.randint(10, 80), random.randint(100, 400), 18000
    return html.Div([
        html.H3(f"TARGET: {clicked_id}", className="text-warning fw-bold mb-4"),
        html.Div([html.H5("🚨 DANGER (CURRENT)"), html.H2(f"{n_r}")], className="status-card bg-red"),
        html.Div(f"Σ Daily Total Actions: {random.randint(800, 1200)} Sellers Processed", className="cumulative-box"),
        html.Div([html.H5("⚠️ WARNING (CURRENT)"), html.H2(f"{n_y}")], className="status-card bg-yellow"),
        html.Div(f"Σ Daily Total Actions: {random.randint(2000, 4000)} Commands Dispatched", className="cumulative-box"),
        html.Div([html.H5("✅ NORMAL (OPTIMAL)"), html.H2(f"{n_g}")], className="status-card bg-green")
    ])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=False)