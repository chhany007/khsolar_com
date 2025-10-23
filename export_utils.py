"""
Export and Reporting Utilities
"""
import pandas as pd
from typing import List
from models import SimulationResult, Device, FinancialAnalysis
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime
from export_utils_word import generate_word_report
from report_translations import REPORT_LABELS as RL

class ReportExporter:
    """Export simulation results and reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def export_to_excel(self, simulation_results: List[SimulationResult], 
                       devices: List[Device], 
                       financial: FinancialAnalysis,
                       filename: str):
        """Export all data to Excel with multiple sheets"""
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Hourly Simulation
            sim_data = {
                'Hour': [r.hour for r in simulation_results],
                'PV Generation (kW)': [r.pv_generation_kw for r in simulation_results],
                'Load (kW)': [r.load_kw for r in simulation_results],
                'Battery Charge (kW)': [r.battery_charge_kw for r in simulation_results],
                'Battery Discharge (kW)': [r.battery_discharge_kw for r in simulation_results],
                'Battery SoC (%)': [r.battery_soc for r in simulation_results],
                'Grid Import (kW)': [r.grid_import_kw for r in simulation_results],
                'Grid Export (kW)': [r.grid_export_kw for r in simulation_results],
            }
            df_sim = pd.DataFrame(sim_data)
            df_sim.to_excel(writer, sheet_name='Hourly Simulation', index=False)
            
            # Sheet 2: Device List
            device_data = {
                'Device Name': [d.name for d in devices],
                'Power (W)': [d.power_watts for d in devices],
                'Daily Hours': [d.daily_hours for d in devices],
                'Daily Energy (kWh)': [d.daily_energy_kwh for d in devices],
                'Priority': [d.is_priority for d in devices],
                'Type': [d.device_type for d in devices]
            }
            df_devices = pd.DataFrame(device_data)
            df_devices.to_excel(writer, sheet_name='Devices', index=False)
            
            # Sheet 3: Financial Analysis
            financial_data = {
                'Metric': [
                    'Total System Cost',
                    'Annual Savings',
                    'Monthly Savings',
                    'Payback Period (Years)',
                    'ROI (%)',
                    'Lifetime Savings (25 years)',
                    'CO2 Reduction (kg/year)'
                ],
                'Value': [
                    f"${financial.total_system_cost:,.2f}",
                    f"${financial.annual_savings:,.2f}",
                    f"${financial.monthly_savings:,.2f}",
                    f"{financial.payback_period_years:.1f}",
                    f"{financial.roi_percent:.1f}%",
                    f"${financial.lifetime_savings:,.2f}",
                    f"{financial.co2_reduction_kg_per_year:,.0f}"
                ]
            }
            df_financial = pd.DataFrame(financial_data)
            df_financial.to_excel(writer, sheet_name='Financial Analysis', index=False)
            
            # Sheet 4: Daily Summary
            total_pv = sum(r.pv_generation_kw for r in simulation_results)
            total_load = sum(r.load_kw for r in simulation_results)
            total_grid_import = sum(r.grid_import_kw for r in simulation_results)
            self_sufficiency = ((total_load - total_grid_import) / total_load * 100) if total_load > 0 else 0
            
            summary_data = {
                'Metric': [
                    'Total PV Generation',
                    'Total Load',
                    'Grid Import',
                    'Self-Sufficiency Rate',
                    'Total Device Count'
                ],
                'Daily': [
                    f"{total_pv:.2f} kWh",
                    f"{total_load:.2f} kWh",
                    f"{total_grid_import:.2f} kWh",
                    f"{self_sufficiency:.1f}%",
                    len(devices)
                ],
                'Monthly (Est.)': [
                    f"{total_pv * 30:.2f} kWh",
                    f"{total_load * 30:.2f} kWh",
                    f"{total_grid_import * 30:.2f} kWh",
                    f"{self_sufficiency:.1f}%",
                    len(devices)
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
    
    def export_to_csv(self, simulation_results: List[SimulationResult], filename: str):
        """Export hourly simulation to CSV"""
        sim_data = {
            'Hour': [r.hour for r in simulation_results],
            'PV_Generation_kW': [r.pv_generation_kw for r in simulation_results],
            'Load_kW': [r.load_kw for r in simulation_results],
            'Battery_Charge_kW': [r.battery_charge_kw for r in simulation_results],
            'Battery_Discharge_kW': [r.battery_discharge_kw for r in simulation_results],
            'Battery_SoC_percent': [r.battery_soc for r in simulation_results],
            'Grid_Import_kW': [r.grid_import_kw for r in simulation_results],
            'Grid_Export_kW': [r.grid_export_kw for r in simulation_results],
        }
        df = pd.DataFrame(sim_data)
        df.to_csv(filename, index=False)
    
    def generate_pdf_report(self, simulation_results: List[SimulationResult],
                           devices: List[Device],
                           financial: FinancialAnalysis,
                           system_config: dict,
                           filename: str):
        """Generate comprehensive professional PDF report"""
        
        doc = SimpleDocTemplate(filename, pagesize=letter,
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.75*inch, rightMargin=0.75*inch)
        story = []
        
        # Company Header
        header_style = ParagraphStyle(
            'CompanyHeader',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#FF6B35'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        story.append(Paragraph(RL['company_name'], header_style))
        story.append(Paragraph(RL['company_subtitle'], subtitle_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Report Title
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph(RL['report_title'], title_style))
        
        # Date and Report Info
        import datetime
        date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        date_text = f"{RL['report_generated']}: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        story.append(Paragraph(date_text, date_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Customer Information Section
        if system_config.get('customer_name'):
            story.append(Paragraph(RL['customer_info'], self.styles['Heading2']))
            customer_data = [
                [RL['customer_name'] + ':', system_config.get('customer_name', 'N/A')],
                [RL['company'] + ':', system_config.get('customer_company', 'N/A') or RL['individual']],
                [RL['phone'] + ':', system_config.get('customer_phone', 'N/A')],
                [RL['email'] + ':', system_config.get('customer_email', 'N/A') or 'N/A'],
                [RL['address'] + ':', system_config.get('customer_address', 'N/A') or 'N/A'],
            ]
            
            customer_table = Table(customer_data, colWidths=[2*inch, 4.5*inch])
            customer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(customer_table)
            story.append(Spacer(1, 0.3*inch))
        
        # System Configuration
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=15,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            borderPadding=5
        )
        
        story.append(Paragraph(RL['system_config'], section_header))
        config_data = [
            [RL['parameter'], RL['value'], RL['unit']],
            [RL['location'], system_config.get('location', 'Cambodia'), ''],
            [RL['pv_capacity'], f"{system_config.get('pv_capacity', 0):.2f}", 'kW'],
            [RL['battery_capacity'], f"{system_config.get('battery_capacity', 0):.2f}", 'kWh'],
            [RL['inverter_power'], f"{system_config.get('inverter_power', 0):.2f}", 'kW'],
            [RL['num_devices'], str(len(devices)), 'units'],
            [RL['system_type'], RL['grid_tied_battery'], ''],
            [RL['labor_cost'], f"${system_config.get('labor_cost', 0):.2f}", ''],
            [RL['support_materials'], f"${system_config.get('support_material_cost', 0):.2f}", ''],
        ]
        
        config_table = Table(config_data, colWidths=[2.5*inch, 2.5*inch, 1.5*inch])
        config_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#EBF5FB')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#EBF5FB'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#AED6F1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(config_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Cost Breakdown Section
        story.append(Paragraph(RL['cost_breakdown'], section_header))
        
        equipment_cost = system_config.get('equipment_cost', 0)
        labor_cost = system_config.get('labor_cost', 0)
        support_cost = system_config.get('support_material_cost', 0)
        
        cost_breakdown_data = [
            [RL['cost_component'], RL['amount'], RL['percentage']],
        ]
        
        total = financial.total_system_cost
        if equipment_cost > 0:
            cost_breakdown_data.append([RL['equipment'], f"${equipment_cost:,.2f}", f"{(equipment_cost/total*100):.1f}%" if total > 0 else '0%'])
        if labor_cost > 0:
            inverter_kw = system_config.get('inverter_power', 0)
            labor_note = RL['system_5kw'] if inverter_kw <= 5 else RL['system_above_5kw']
            cost_breakdown_data.append([f"{RL['labor_system']} ({labor_note})", f"${labor_cost:,.2f}", f"{(labor_cost/total*100):.1f}%" if total > 0 else '0%'])
        if support_cost > 0:
            cost_breakdown_data.append([RL['support_installation'], f"${support_cost:,.2f}", f"{(support_cost/total*100):.1f}%" if total > 0 else '0%'])
        
        cost_breakdown_data.append([RL['total_system_cost'], f"${total:,.2f}", '100%'])
        
        cost_breakdown_table = Table(cost_breakdown_data, colWidths=[3*inch, 2*inch, 1.5*inch])
        cost_breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#ECF0F1')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#BDC3C7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.HexColor('#ECF0F1'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95A5A6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#34495E')),
        ]))
        story.append(cost_breakdown_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Financial Summary
        story.append(Paragraph(RL['financial_analysis'], section_header))
        financial_data = [
            [RL['metric'], RL['value'], RL['details']],
            [RL['total_investment'], f"${financial.total_system_cost:,.2f}", RL['complete_installation']],
            [RL['monthly_savings'], f"${financial.monthly_savings:,.2f}", RL['electricity_reduction']],
            [RL['annual_savings'], f"${financial.annual_savings:,.2f}", RL['year1_savings']],
            [RL['payback_period'], f"{financial.payback_period_years:.1f} years", RL['breakeven_point']],
            [RL['roi'], f"{financial.roi_percent:.1f}%", RL['over_25years']],
            [RL['lifetime_savings'], f"${financial.lifetime_savings:,.2f}", RL['total_25years']],
            [RL['co2_reduction'], f"{financial.co2_reduction_kg_per_year:,.0f} kg/year", RL['environmental_impact']],
        ]
        
        financial_table = Table(financial_data, colWidths=[2.2*inch, 2.2*inch, 2.1*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#D5F4E6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#D5F4E6'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#82E0AA')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(financial_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Energy Summary
        story.append(Paragraph(RL['energy_analysis'], section_header))
        total_pv = sum(r.pv_generation_kw for r in simulation_results)
        total_load = sum(r.load_kw for r in simulation_results)
        total_grid_import = sum(r.grid_import_kw for r in simulation_results)
        total_grid_export = sum(r.grid_export_kw for r in simulation_results)
        self_sufficiency = ((total_load - total_grid_import) / total_load * 100) if total_load > 0 else 0
        
        energy_data = [
            [RL['metric'], RL['daily'], RL['monthly'], RL['annual_est']],
            [RL['solar_generation'], f"{total_pv:.2f} kWh", f"{total_pv * 30:.1f} kWh", f"{total_pv * 365:.0f} kWh"],
            [RL['total_consumption'], f"{total_load:.2f} kWh", f"{total_load * 30:.1f} kWh", f"{total_load * 365:.0f} kWh"],
            [RL['grid_import'], f"{total_grid_import:.2f} kWh", f"{total_grid_import * 30:.1f} kWh", f"{total_grid_import * 365:.0f} kWh"],
            [RL['grid_export'], f"{total_grid_export:.2f} kWh", f"{total_grid_export * 30:.1f} kWh", f"{total_grid_export * 365:.0f} kWh"],
            [RL['self_sufficiency'], f"{self_sufficiency:.1f}%", f"{self_sufficiency:.1f}%", f"{self_sufficiency:.1f}%"],
        ]
        
        energy_table = Table(energy_data, colWidths=[2.3*inch, 1.4*inch, 1.4*inch, 1.4*inch])
        energy_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E67E22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FADBD8')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FADBD8'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#F5B7B1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(energy_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Device List
        story.append(PageBreak())
        story.append(Paragraph(RL['device_inventory'], section_header))
        
        # Add device summary
        total_device_power = sum(d.power_watts for d in devices)
        total_daily_energy = sum(d.daily_energy_kwh for d in devices)
        priority_count = sum(1 for d in devices if d.is_priority)
        
        summary_text = f"{RL['total_devices']}: {len(devices)} | {RL['total_power']}: {total_device_power:.0f}W | {RL['daily_consumption']}: {total_daily_energy:.2f} kWh | {RL['priority_devices']}: {priority_count}"
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
        
        device_data = [['#', RL['device_name'], RL['power_w'], RL['hours_day'], RL['daily_energy'], RL['type'], RL['priority']]]
        for idx, device in enumerate(devices, 1):
            device_data.append([
                str(idx),
                device.name,
                f"{device.power_watts:.0f}",
                f"{device.daily_hours:.1f}",
                f"{device.daily_energy_kwh:.2f} kWh",
                device.device_type.title(),
                "⭐ Yes" if device.is_priority else "○ No"
            ])
        
        device_table = Table(device_data, colWidths=[0.4*inch, 2*inch, 0.8*inch, 0.8*inch, 1*inch, 0.9*inch, 0.9*inch])
        device_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8E44AD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F4ECF7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F4ECF7'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D7BDE2')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(device_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add footer with professional notes
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=10,
            alignment=TA_CENTER
        )
        
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("—" * 60, footer_style))
        story.append(Paragraph(RL['footer_text'], footer_style))
        story.append(Paragraph(RL['contact_support'], footer_style))
        story.append(Paragraph(f"{RL['report_id']}: KHS-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}", footer_style))
        
        # Build PDF
        doc.build(story)
    
    def export_device_schedule(self, devices: List[Device], filename: str):
        """Export device schedule as printable CSV"""
        schedule_data = {
            'Device': [d.name for d in devices],
            'Power (W)': [d.power_watts for d in devices],
            'Daily Hours': [d.daily_hours for d in devices],
            'Preferred Hours': [', '.join(map(str, d.preferred_hours)) if d.preferred_hours else 'Flexible' for d in devices],
            'Priority': ['High' if d.is_priority else 'Normal' for d in devices],
            'Recommendation': ['Run during peak sun (10AM-2PM)' if d.power_watts > 1000 else 'Flexible timing' for d in devices]
        }
        df = pd.DataFrame(schedule_data)
        df.to_csv(filename, index=False)
    
    def generate_word_report(self, simulation_results: List[SimulationResult],
                            devices: List[Device],
                            financial: FinancialAnalysis,
                            system_config: dict,
                            filename: str):
        """Generate professional Word document report with same style as PDF"""
        generate_word_report(simulation_results, devices, financial, system_config, filename)
