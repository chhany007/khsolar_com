# Water Pump Sets Tab Content
# This will be inserted into app.py

water_pump_tab_code = """
    # ========== TAB 3: WATER PUMP SETS ==========
    with main_tab3:
        st.markdown("### 💧 Solar Water Pump System Sets")
        st.markdown("Complete solar-powered water pumping systems with panels, controller, and installation")
        
        # Water pump system configurations
        pump_sets = [
            {
                "name": "1 HP Solar Water Pump System",
                "hp": 1,
                "pump_model": "3DPC5.2-50-48-600W",
                "pump_power": 600,
                "pump_specs": {
                    "power": "600W (1 HP)",
                    "voltage": "48V DC",
                    "max_flow": "5.2 m³/h",
                    "max_head": "50m",
                    "outlet": "1.5 inch"
                },
                "solar_panels": {"name": "Lvtopsun 340W", "quantity": 2, "total_kw": 0.68},
                "controller": "MPPT Solar Pump Controller 48V",
                "description": "Perfect for small farms and home gardens",
                "applications": "Irrigation, livestock watering, domestic use",
                "daily_water": "20-30 m³/day",
                "icon": "🏡"
            },
            {
                "name": "2 HP Solar Water Pump System",
                "hp": 2,
                "pump_model": "4DPC9-85-110-1500W",
                "pump_power": 1500,
                "pump_specs": {
                    "power": "1500W (2 HP)",
                    "voltage": "110V DC",
                    "max_flow": "9 m³/h",
                    "max_head": "85m",
                    "outlet": "2 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 3, "total_kw": 1.65},
                "controller": "MPPT Solar Pump Controller 110V",
                "description": "Ideal for medium farms and irrigation",
                "applications": "Farm irrigation, fish ponds, water supply",
                "daily_water": "40-60 m³/day",
                "icon": "🌾"
            },
            {
                "name": "3 HP Solar Water Pump System",
                "hp": 3,
                "pump_model": "4DSC19-60-300-2200W",
                "pump_power": 2200,
                "pump_specs": {
                    "power": "2200W (3 HP)",
                    "voltage": "300V DC",
                    "max_flow": "19 m³/h",
                    "max_head": "60m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 5, "total_kw": 2.75},
                "controller": "MPPT Solar Pump Controller 300V",
                "description": "Great for large farms and commercial use",
                "applications": "Large-scale irrigation, water distribution",
                "daily_water": "80-100 m³/day",
                "icon": "🚜"
            },
            {
                "name": "4 HP Solar Water Pump System",
                "hp": 4,
                "pump_model": "4DSC19-98-380/550-3000W",
                "pump_power": 3000,
                "pump_specs": {
                    "power": "3000W (4 HP)",
                    "voltage": "380V AC / 550V DC",
                    "max_flow": "19 m³/h",
                    "max_head": "98m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 6, "total_kw": 3.3},
                "controller": "MPPT Solar Pump Controller 380V",
                "description": "Heavy-duty for deep wells and high head",
                "applications": "Deep well pumping, high-pressure irrigation",
                "daily_water": "100-120 m³/day",
                "icon": "🏭"
            },
            {
                "name": "5 HP Solar Water Pump System",
                "hp": 5,
                "pump_model": "4DSC19-135-380/550-4000W",
                "pump_power": 4000,
                "pump_specs": {
                    "power": "4000W (5 HP)",
                    "voltage": "380V AC / 550V DC",
                    "max_flow": "19 m³/h",
                    "max_head": "135m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 8, "total_kw": 4.4},
                "controller": "MPPT Solar Pump Controller 380V",
                "description": "Industrial-grade for maximum performance",
                "applications": "Industrial water supply, large irrigation systems",
                "daily_water": "120-150 m³/day",
                "icon": "🏗️"
            }
        ]
        
        # Display each pump set
        for pump_set in pump_sets:
            with st.expander(f"{pump_set['icon']} {pump_set['name']} - {pump_set['hp']} HP"):
                # Display pump image using HTML
                img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
                with img_col2:
                    pump_img = product_images.get(pump_set['pump_model'], "https://via.placeholder.com/400x300.png?text=Water+Pump")
                    st.markdown(f'''
                    <div style='text-align: center;'>
                        <img src='{pump_img}' style='max-width: 400px; width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);' onerror="this.src='https://via.placeholder.com/400x300.png?text=Water+Pump'">
                        <p style='margin-top: 0.5rem; color: #666; font-size: 0.9rem;'>{pump_set['pump_model']}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown(f"**{pump_set['description']}**")
                st.markdown(f"**Applications:** {pump_set['applications']}")
                st.markdown("---")
                
                # Performance Summary
                st.markdown(f'''
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            padding: 1.2rem; border-radius: 10px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;'>
                    <h3 style='margin: 0 0 0.8rem 0; color: #1e40af;'>💧 System Performance</h3>
                    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
                        <div style='text-align: center;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #1e40af;'><b>Pump Power</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #1e3a8a; font-weight: 700;'>{pump_set['pump_power']}W ({pump_set['hp']} HP)</p>
                        </div>
                        <div style='text-align: center; border-left: 2px solid #3b82f6; border-right: 2px solid #3b82f6;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #1e40af;'><b>Daily Water Output</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #1e3a8a; font-weight: 700;'>{pump_set['daily_water']}</p>
                        </div>
                        <div style='text-align: center;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #1e40af;'><b>Solar Panels</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #1e3a8a; font-weight: 700;'>{pump_set['solar_panels']['quantity']}x {pump_set['solar_panels']['total_kw']}kW</p>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Component Specifications
                st.markdown("### 🔧 System Components")
                
                spec_col1, spec_col2 = st.columns(2)
                
                with spec_col1:
                    st.markdown(f'''
                    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #92400e;'>☀️ Solar Panels</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {pump_set['solar_panels']['name']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Quantity:</b> {pump_set['solar_panels']['quantity']} panels</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Total Power:</b> {pump_set['solar_panels']['total_kw']} kW</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Area Needed:</b> ~{pump_set['solar_panels']['quantity'] * 2.6:.1f} m²</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #6366f1;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #4338ca;'>⚡ Controller</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Type:</b> {pump_set['controller']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Features:</b> MPPT, Auto start/stop</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Protection:</b> Overload, dry-run, overvoltage</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with spec_col2:
                    st.markdown(f'''
                    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #1e40af;'>💧 Water Pump</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {pump_set['pump_model']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Power:</b> {pump_set['pump_specs']['power']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Voltage:</b> {pump_set['pump_specs']['voltage']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Max Flow:</b> {pump_set['pump_specs']['max_flow']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Max Head:</b> {pump_set['pump_specs']['max_head']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Outlet:</b> {pump_set['pump_specs']['outlet']}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Pricing calculation
                pump_price = pm.products.get(pump_set['pump_model'])
                pump_cost = pump_price.cost if pump_price else 200.00
                
                panel_price = pm.products.get(pump_set['solar_panels']['name'])
                panel_cost = panel_price.cost if panel_price else 66.00
                
                controller_cost = 150.00  # Standard controller cost
                installation_cost = pump_set['pump_power'] * 0.15  # $0.15 per watt
                
                equipment_total = pump_cost + (panel_cost * pump_set['solar_panels']['quantity']) + controller_cost
                wholesale_total = equipment_total + installation_cost
                retail_total = wholesale_total * (1 + st.session_state.price_markup / 100)
                
                # Pricing display
                st.markdown("### 💰 System Pricing")
                
                price_col1, price_col2 = st.columns(2)
                
                with price_col1:
                    st.markdown("#### 📊 Cost Breakdown")
                    st.write(f"💧 Water Pump: ${pump_cost:,.2f}")
                    st.write(f"☀️ Solar Panels ({pump_set['solar_panels']['quantity']}x): ${panel_cost * pump_set['solar_panels']['quantity']:,.2f}")
                    st.write(f"⚡ Controller: ${controller_cost:,.2f}")
                    st.write(f"👷 Installation: ${installation_cost:,.2f}")
                    st.markdown(f"**Total: ${equipment_total + installation_cost:,.2f}**")
                
                with price_col2:
                    if st.session_state.hide_wholesale:
                        st.markdown(f'''
                        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                    padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3b82f6; text-align: center;'>
                            <h4 style='margin: 0 0 0.8rem 0; color: #1e40af;'>💵 System Price</h4>
                            <p style='margin: 0; font-size: 2rem; color: #1e3a8a; font-weight: 700;'>${retail_total:,.2f}</p>
                            <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #1e40af;'>Complete installed system</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                    padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3b82f6;'>
                            <h4 style='margin: 0 0 0.8rem 0; color: #1e40af; text-align: center;'>💵 Final Pricing</h4>
                            <div style='margin: 0.5rem 0;'>
                                <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>💼 Wholesale:</b></p>
                                <p style='margin: 0; font-size: 1.3rem; color: #1e40af; font-weight: 600;'>${wholesale_total:,.2f}</p>
                            </div>
                            <hr style='margin: 0.8rem 0; border: 1px solid #3b82f6;'>
                            <div style='margin: 0.5rem 0;'>
                                <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>🏷️ Retail (+{st.session_state.price_markup:.0f}%):</b></p>
                                <p style='margin: 0; font-size: 1.8rem; color: #1e3a8a; font-weight: 700;'>${retail_total:,.2f}</p>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                
                st.markdown("---")
                st.success("✅ **Includes:** Water pump, solar panels, MPPT controller, mounting structure, cables, and installation")
        
        st.markdown("---")
        st.info("💡 **Note:** All water pump systems are designed for optimal performance with 6-8 hours of peak sunlight. Actual water output may vary based on sunlight conditions and installation location.")
"""
