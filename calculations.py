"""
Solar System Calculation Modules
"""
import numpy as np
from typing import List, Tuple
from models import Device, SystemConfiguration, SimulationResult, FinancialAnalysis

class SolarCalculator:
    """Core calculation engine for solar system sizing and simulation"""
    
    def __init__(self, config: SystemConfiguration):
        self.config = config
    
    def calculate_pv_size_needed(self, daily_load_kwh: float, sunlight_hours: float, 
                                 system_efficiency: float = 0.85) -> float:
        """
        Calculate required PV array size in kW
        Accounts for system losses (inverter, wiring, temperature, etc.)
        """
        if sunlight_hours <= 0:
            return 0.0
        
        # PV size = Daily Load / (Sunlight Hours * System Efficiency)
        pv_size_kw = daily_load_kwh / (sunlight_hours * system_efficiency)
        return pv_size_kw
    
    def calculate_battery_size_needed(self, night_load_kwh: float, 
                                      autonomy_days: float = 1.0,
                                      dod: float = 0.8) -> float:
        """
        Calculate required battery capacity in kWh
        
        Args:
            night_load_kwh: Energy needed during night hours
            autonomy_days: Days of backup desired
            dod: Depth of discharge (0.8 = 80%)
        """
        # Battery size = (Night Load * Autonomy Days) / DoD
        battery_size_kwh = (night_load_kwh * autonomy_days) / dod
        return battery_size_kwh
    
    def split_day_night_load(self, devices: List[Device]) -> Tuple[float, float]:
        """
        Split load into day (6am-6pm) and night (6pm-6am) consumption
        """
        day_load = 0.0
        night_load = 0.0
        
        for device in devices:
            if device.preferred_hours:
                # Calculate based on preferred hours
                day_hours = sum(1 for h in device.preferred_hours if 6 <= h < 18)
                night_hours = len(device.preferred_hours) - day_hours
                
                energy_per_hour = device.power_watts / 1000  # kW
                day_load += energy_per_hour * day_hours
                night_load += energy_per_hour * night_hours
            else:
                # Assume even distribution, or typical household pattern
                # 60% day, 40% night for general devices
                day_load += device.daily_energy_kwh * 0.6
                night_load += device.daily_energy_kwh * 0.4
        
        return day_load, night_load
    
    def calculate_hourly_pv_generation(self, pv_capacity_kw: float, 
                                       hour: int, month: int = 6) -> float:
        """
        Calculate PV generation for a specific hour using sine curve
        
        Args:
            pv_capacity_kw: Total PV array capacity
            hour: Hour of day (0-23)
            month: Month (1-12) for seasonal adjustment
        """
        # No generation at night (before 6am and after 6pm)
        if hour < 6 or hour >= 18:
            return 0.0
        
        # Peak at solar noon (12pm)
        # Use sine curve from 6am to 6pm
        hours_from_sunrise = hour - 6
        total_daylight_hours = 12
        
        # Sine curve: generation peaks at midday
        angle = (hours_from_sunrise / total_daylight_hours) * np.pi
        generation_factor = np.sin(angle)
        
        # Seasonal adjustment (June has more sun than December)
        seasonal_factor = 1.0 + 0.2 * np.sin((month - 6) * np.pi / 6)
        
        # Actual generation
        pv_generation = pv_capacity_kw * generation_factor * seasonal_factor
        
        return max(0, pv_generation)
    
    def simulate_24_hours(self, pv_capacity_kw: float, battery_capacity_kwh: float,
                          devices: List[Device], initial_soc: float = 50.0) -> List[SimulationResult]:
        """
        Simulate 24 hours of energy flow
        
        Returns list of SimulationResult for each hour
        """
        results = []
        battery_soc = initial_soc  # Start at 50% SoC
        battery_kwh = battery_capacity_kwh * (battery_soc / 100)
        
        battery_efficiency = 0.95
        max_charge_rate = battery_capacity_kwh * 0.5  # C-rate of 0.5
        max_discharge_rate = battery_capacity_kwh * 0.5
        
        for hour in range(24):
            # Calculate PV generation
            pv_gen = self.calculate_hourly_pv_generation(pv_capacity_kw, hour)
            
            # Calculate load for this hour
            load = self.calculate_hourly_load(devices, hour)
            
            # Energy flow logic
            battery_charge = 0.0
            battery_discharge = 0.0
            grid_import = 0.0
            grid_export = 0.0
            surplus = 0.0
            
            # Net energy: PV - Load
            net_energy = pv_gen - load
            
            if net_energy > 0:
                # Surplus: charge battery or export to grid
                available_to_charge = min(net_energy, max_charge_rate)
                space_in_battery = battery_capacity_kwh - battery_kwh
                
                if space_in_battery > 0:
                    # Charge battery
                    battery_charge = min(available_to_charge, space_in_battery / battery_efficiency)
                    battery_kwh += battery_charge * battery_efficiency
                    remaining_surplus = net_energy - battery_charge
                else:
                    remaining_surplus = net_energy
                
                if remaining_surplus > 0:
                    # Export to grid or waste
                    if self.config.grid_available:
                        grid_export = remaining_surplus
                    else:
                        surplus = remaining_surplus
            
            else:
                # Deficit: discharge battery or import from grid
                deficit = abs(net_energy)
                available_from_battery = battery_kwh * battery_efficiency
                
                can_discharge = min(deficit, max_discharge_rate, available_from_battery)
                
                if can_discharge > 0:
                    # Discharge battery
                    battery_discharge = can_discharge
                    battery_kwh -= battery_discharge / battery_efficiency
                    remaining_deficit = deficit - battery_discharge
                else:
                    remaining_deficit = deficit
                
                if remaining_deficit > 0:
                    # Import from grid
                    if self.config.grid_available:
                        grid_import = remaining_deficit
                    # else: load shedding situation
            
            # Update SoC
            battery_soc = (battery_kwh / battery_capacity_kwh) * 100 if battery_capacity_kwh > 0 else 0
            battery_soc = max(0, min(100, battery_soc))
            
            # Store result
            result = SimulationResult(
                hour=hour,
                pv_generation_kw=pv_gen,
                load_kw=load,
                battery_charge_kw=battery_charge,
                battery_discharge_kw=battery_discharge,
                battery_soc=battery_soc,
                grid_import_kw=grid_import,
                grid_export_kw=grid_export,
                energy_surplus_kw=surplus
            )
            results.append(result)
        
        return results
    
    def calculate_hourly_load(self, devices: List[Device], hour: int) -> float:
        """
        Calculate total load for a specific hour based on device schedules
        """
        total_load = 0.0
        
        for device in devices:
            if device.preferred_hours:
                # Use preferred hours
                if hour in device.preferred_hours:
                    total_load += device.power_watts / 1000  # Convert to kW
            else:
                # Distribute evenly across daily hours
                if device.daily_hours > 0:
                    hours_per_day = device.daily_hours
                    probability = hours_per_day / 24
                    
                    # Simple distribution: assume device runs during typical hours
                    # Morning/evening peak for homes
                    if 6 <= hour <= 9 or 17 <= hour <= 22:
                        # Peak hours - higher probability
                        if np.random.random() < probability * 2:
                            total_load += device.power_watts / 1000
                    elif 10 <= hour <= 16:
                        # Midday - moderate
                        if np.random.random() < probability:
                            total_load += device.power_watts / 1000
                    else:
                        # Night - lower probability
                        if np.random.random() < probability * 0.5:
                            total_load += device.power_watts / 1000
        
        return total_load
    
    def calculate_financial_analysis(self, system_cost: float, 
                                     annual_energy_kwh: float,
                                     electricity_rate: float = 0.20,
                                     system_lifetime_years: int = 25) -> FinancialAnalysis:
        """
        Calculate ROI, payback period, and savings
        """
        # Annual savings from solar
        annual_savings = annual_energy_kwh * electricity_rate
        
        # Payback period
        if annual_savings > 0:
            payback_years = system_cost / annual_savings
        else:
            payback_years = float('inf')
        
        # ROI
        lifetime_savings = annual_savings * system_lifetime_years
        roi_percent = ((lifetime_savings - system_cost) / system_cost) * 100 if system_cost > 0 else 0
        
        # Monthly savings
        monthly_savings = annual_savings / 12
        
        # CO2 reduction (approx 0.5 kg CO2 per kWh from grid)
        co2_reduction = annual_energy_kwh * 0.5
        
        return FinancialAnalysis(
            total_system_cost=system_cost,
            annual_savings=annual_savings,
            payback_period_years=payback_years,
            roi_percent=roi_percent,
            lifetime_savings=lifetime_savings,
            monthly_savings=monthly_savings,
            co2_reduction_kg_per_year=co2_reduction
        )
    
    def get_device_recommendations(self, devices: List[Device], 
                                   pv_capacity_kw: float,
                                   battery_capacity_kwh: float) -> List[str]:
        """
        Generate AI-based recommendations for device scheduling
        """
        recommendations = []
        
        # Calculate total load
        total_daily_load = sum(d.daily_energy_kwh for d in devices)
        avg_pv_daily = pv_capacity_kw * self.config.sunlight_hours
        
        # Check if system is undersized
        if total_daily_load > avg_pv_daily * 0.85:
            recommendations.append(
                f"⚠️ System undersized: Daily load ({total_daily_load:.2f} kWh) exceeds PV generation "
                f"({avg_pv_daily:.2f} kWh). Consider adding {(total_daily_load - avg_pv_daily) / self.config.sunlight_hours:.1f} kW more panels."
            )
        
        # Identify high-power devices
        high_power_devices = [d for d in devices if d.power_watts > 1000]
        if high_power_devices:
            recommendations.append(
                f"💡 Run high-power devices ({', '.join(d.name for d in high_power_devices)}) during peak sun hours (10 AM - 2 PM) for maximum solar utilization."
            )
        
        # Battery recommendations
        day_load, night_load = self.split_day_night_load(devices)
        if night_load > battery_capacity_kwh * 0.8:
            recommendations.append(
                f"🔋 Night load ({night_load:.2f} kWh) exceeds battery capacity. Consider shifting some loads to daytime or adding {(night_load - battery_capacity_kwh * 0.8):.1f} kWh battery capacity."
            )
        
        # Priority device check
        priority_devices = [d for d in devices if d.is_priority]
        if priority_devices:
            total_priority_load = sum(d.daily_energy_kwh for d in priority_devices)
            if total_priority_load > battery_capacity_kwh * 0.5:
                recommendations.append(
                    f"⚡ Priority devices require {total_priority_load:.2f} kWh. Ensure battery capacity is sufficient for backup."
                )
        
        # Energy efficiency tips
        recommendations.append(
            "🌟 Energy Tip: Replace incandescent bulbs with LED lights to reduce consumption by up to 75%."
        )
        
        return recommendations
