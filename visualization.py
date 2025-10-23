"""
Visualization and Reporting Module
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List
from models import SimulationResult, Device

class SolarVisualizer:
    """Create visualizations for solar system analysis"""
    
    def __init__(self):
        self.color_scheme = {
            'pv': '#FDB462',  # Orange
            'battery_charge': '#80B1D3',  # Light blue
            'battery_discharge': '#FB8072',  # Red
            'load': '#BEBADA',  # Purple
            'grid_import': '#FF6B6B',  # Bright red
            'grid_export': '#4ECDC4',  # Teal
            'battery_soc': '#95E1D3'  # Mint green
        }
    
    def create_24h_energy_flow_chart(self, simulation_results: List[SimulationResult]) -> go.Figure:
        """Create 24-hour energy flow visualization"""
        hours = [r.hour for r in simulation_results]
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Energy Flow (kW)', 'Battery State of Charge (%)'),
            vertical_spacing=0.15,
            row_heights=[0.6, 0.4]
        )
        
        # Top chart: Energy flows
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[r.pv_generation_kw for r in simulation_results],
                name='PV Generation',
                line=dict(color=self.color_scheme['pv'], width=3),
                fill='tozeroy',
                fillcolor='rgba(253, 180, 98, 0.3)'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[r.load_kw for r in simulation_results],
                name='Load',
                line=dict(color=self.color_scheme['load'], width=2, dash='dash')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[r.battery_charge_kw for r in simulation_results],
                name='Battery Charge',
                line=dict(color=self.color_scheme['battery_charge'], width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[r.battery_discharge_kw for r in simulation_results],
                name='Battery Discharge',
                line=dict(color=self.color_scheme['battery_discharge'], width=2)
            ),
            row=1, col=1
        )
        
        # Bottom chart: Battery SoC
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[r.battery_soc for r in simulation_results],
                name='Battery SoC',
                line=dict(color=self.color_scheme['battery_soc'], width=3),
                fill='tozeroy',
                fillcolor='rgba(149, 225, 211, 0.3)'
            ),
            row=2, col=1
        )
        
        # Add horizontal lines for battery zones
        fig.add_hline(y=80, line_dash="dot", line_color="green", 
                     annotation_text="Full", row=2, col=1)
        fig.add_hline(y=20, line_dash="dot", line_color="red", 
                     annotation_text="Low", row=2, col=1)
        
        # Update layout
        fig.update_xaxes(title_text="Hour of Day", row=2, col=1)
        fig.update_yaxes(title_text="Power (kW)", row=1, col=1)
        fig.update_yaxes(title_text="SoC (%)", range=[0, 100], row=2, col=1)
        
        fig.update_layout(
            height=700,
            showlegend=True,
            hovermode='x unified',
            template='plotly_white',
            title_text="24-Hour Solar System Simulation",
            title_x=0.5
        )
        
        return fig
    
    def create_energy_balance_pie(self, simulation_results: List[SimulationResult]) -> go.Figure:
        """Create pie chart showing energy sources"""
        total_pv = sum(r.pv_generation_kw for r in simulation_results)
        total_grid_import = sum(r.grid_import_kw for r in simulation_results)
        total_battery = sum(r.battery_discharge_kw for r in simulation_results)
        
        labels = ['Solar (PV)', 'Grid Import', 'Battery Discharge']
        values = [total_pv, total_grid_import, total_battery]
        colors = [self.color_scheme['pv'], self.color_scheme['grid_import'], 
                 self.color_scheme['battery_discharge']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='%{label}<br>%{value:.2f} kWh<br>%{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title_text="Daily Energy Sources",
            title_x=0.5,
            template='plotly_white'
        )
        
        return fig
    
    def create_device_consumption_chart(self, devices: List[Device]) -> go.Figure:
        """Create bar chart of device energy consumption"""
        device_names = [d.name for d in devices]
        energy_values = [d.daily_energy_kwh for d in devices]
        
        # Color code by priority
        colors = ['#FF6B6B' if d.is_priority else '#4ECDC4' for d in devices]
        
        fig = go.Figure(data=[
            go.Bar(
                x=device_names,
                y=energy_values,
                marker_color=colors,
                text=[f"{e:.2f} kWh" for e in energy_values],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Device Daily Energy Consumption",
            xaxis_title="Device",
            yaxis_title="Energy (kWh/day)",
            template='plotly_white',
            showlegend=False
        )
        
        return fig
    
    def create_financial_chart(self, years: int, annual_savings: float, 
                              system_cost: float) -> go.Figure:
        """Create financial analysis chart showing cumulative savings"""
        year_range = list(range(years + 1))
        cumulative_savings = [annual_savings * y - system_cost for y in year_range]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=year_range,
            y=cumulative_savings,
            mode='lines+markers',
            name='Net Savings',
            line=dict(color='#4ECDC4', width=3),
            fill='tozeroy',
            fillcolor='rgba(78, 205, 196, 0.3)'
        ))
        
        # Add break-even line
        fig.add_hline(y=0, line_dash="dash", line_color="red", 
                     annotation_text="Break-even")
        
        # Find and mark payback year
        for i, val in enumerate(cumulative_savings):
            if val >= 0:
                fig.add_vline(x=i, line_dash="dot", line_color="green",
                            annotation_text=f"Payback: Year {i}")
                break
        
        fig.update_layout(
            title="Cumulative Savings Over Time",
            xaxis_title="Years",
            yaxis_title="Net Savings (USD)",
            template='plotly_white',
            hovermode='x'
        )
        
        return fig
    
    def create_roi_gauge(self, roi_percent: float) -> go.Figure:
        """Create gauge chart for ROI"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=roi_percent,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Return on Investment (ROI)", 'font': {'size': 24}},
            delta={'reference': 100},
            gauge={
                'axis': {'range': [None, 500]},
                'bar': {'color': "#4ECDC4"},
                'steps': [
                    {'range': [0, 100], 'color': "#FFE5E5"},
                    {'range': [100, 300], 'color': "#E5F7F6"},
                    {'range': [300, 500], 'color': "#C5F2ED"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_monthly_summary_table(self, simulation_results: List[SimulationResult]) -> pd.DataFrame:
        """Create summary statistics table"""
        total_pv = sum(r.pv_generation_kw for r in simulation_results)
        total_load = sum(r.load_kw for r in simulation_results)
        total_battery_charge = sum(r.battery_charge_kw for r in simulation_results)
        total_battery_discharge = sum(r.battery_discharge_kw for r in simulation_results)
        total_grid_import = sum(r.grid_import_kw for r in simulation_results)
        total_grid_export = sum(r.grid_export_kw for r in simulation_results)
        
        avg_battery_soc = sum(r.battery_soc for r in simulation_results) / len(simulation_results)
        
        self_sufficiency = ((total_load - total_grid_import) / total_load * 100) if total_load > 0 else 0
        
        data = {
            'Metric': [
                'Total PV Generation',
                'Total Load Consumption',
                'Battery Charged',
                'Battery Discharged',
                'Grid Import',
                'Grid Export',
                'Average Battery SoC',
                'Self-Sufficiency Rate'
            ],
            'Daily Value': [
                f"{total_pv:.2f} kWh",
                f"{total_load:.2f} kWh",
                f"{total_battery_charge:.2f} kWh",
                f"{total_battery_discharge:.2f} kWh",
                f"{total_grid_import:.2f} kWh",
                f"{total_grid_export:.2f} kWh",
                f"{avg_battery_soc:.1f}%",
                f"{self_sufficiency:.1f}%"
            ],
            'Monthly Estimate': [
                f"{total_pv * 30:.2f} kWh",
                f"{total_load * 30:.2f} kWh",
                f"{total_battery_charge * 30:.2f} kWh",
                f"{total_battery_discharge * 30:.2f} kWh",
                f"{total_grid_import * 30:.2f} kWh",
                f"{total_grid_export * 30:.2f} kWh",
                f"{avg_battery_soc:.1f}%",
                f"{self_sufficiency:.1f}%"
            ]
        }
        
        return pd.DataFrame(data)
