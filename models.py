"""
Data Models for Solar Planning Software
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class Device:
    """Represents an electrical device"""
    name: str
    power_watts: float
    daily_hours: float
    is_priority: bool = False
    preferred_hours: List[int] = field(default_factory=list)  # Hours when device should run (0-23)
    device_type: str = "general"  # general, heating, cooling, lighting, etc.
    has_inverter: bool = False  # Smart inverter technology for power saving
    
    @property
    def inverter_savings_percent(self) -> float:
        """Power savings percentage for inverter devices"""
        # Typical savings by device type
        inverter_savings = {
            "cooling": 40,  # AC and refrigerators save 35-45%
            "heating": 35,  # Water heaters save 30-40%
            "general": 30,  # Washing machines, etc save 25-35%
        }
        if self.has_inverter:
            return inverter_savings.get(self.device_type, 30)
        return 0
    
    @property
    def effective_power_watts(self) -> float:
        """Actual power consumption considering inverter savings"""
        if self.has_inverter:
            savings_factor = 1 - (self.inverter_savings_percent / 100)
            return self.power_watts * savings_factor
        return self.power_watts
    
    @property
    def daily_energy_kwh(self) -> float:
        """Calculate daily energy consumption in kWh (with inverter savings)"""
        return (self.effective_power_watts * self.daily_hours) / 1000
    
    @property
    def power_saved_kwh(self) -> float:
        """Daily power saved by inverter technology"""
        if self.has_inverter:
            non_inverter_consumption = (self.power_watts * self.daily_hours) / 1000
            return non_inverter_consumption - self.daily_energy_kwh
        return 0.0

@dataclass
class Product:
    """Represents a solar system product"""
    product_id: str
    name: str
    category: str  # pv_panel, inverter, battery, controller, etc.
    specifications: Dict
    cost: float
    currency: str = "USD"
    warranty_years: int = 0
    supplier: str = ""
    notes: str = ""

@dataclass
class SolarPanel:
    """PV Panel specifications"""
    name: str
    power_watts: float
    efficiency: float = 0.18
    cost_per_panel: float = 0.0
    quantity: int = 1
    
    @property
    def total_power_kw(self) -> float:
        return (self.power_watts * self.quantity) / 1000

@dataclass
class Battery:
    """Battery specifications"""
    name: str
    capacity_kwh: float
    voltage: float
    depth_of_discharge: float = 0.8  # 80% DoD
    efficiency: float = 0.95
    cost: float = 0.0
    quantity: int = 1
    
    @property
    def usable_capacity_kwh(self) -> float:
        return self.capacity_kwh * self.depth_of_discharge * self.quantity
    
    @property
    def total_capacity_kwh(self) -> float:
        return self.capacity_kwh * self.quantity
    
    @property
    def total_cost(self) -> float:
        return self.cost * self.quantity

@dataclass
class Inverter:
    """Inverter specifications"""
    name: str
    power_kw: float
    efficiency: float = 0.95
    cost: float = 0.0
    input_voltage: float = 48.0

@dataclass
class SystemConfiguration:
    """Complete solar system configuration"""
    location: str = "Phnom Penh, Cambodia"
    sunlight_hours: float = 5.5  # Average peak sun hours
    solar_panels: Optional[SolarPanel] = None
    battery: Optional[Battery] = None
    inverter: Optional[Inverter] = None
    devices: List[Device] = field(default_factory=list)
    monthly_usage_kwh: float = 0.0
    grid_available: bool = True
    electricity_rate: float = 0.20  # USD per kWh
    
    @property
    def total_daily_load_kwh(self) -> float:
        """Calculate total daily load from devices"""
        if self.devices:
            return sum(d.daily_energy_kwh for d in self.devices)
        elif self.monthly_usage_kwh > 0:
            return self.monthly_usage_kwh / 30
        return 0.0
    
    @property
    def labor_cost(self) -> float:
        """Calculate labor cost based on inverter size"""
        if self.inverter:
            if self.inverter.power_kw <= 5.0:
                return 250.0  # $250 for systems ≤5kW
            else:
                return 500.0  # $500 for systems >5kW
        return 0.0
    
    @property
    def support_material_cost(self) -> float:
        """Calculate support material cost based on system size"""
        if self.inverter:
            inverter_kw = self.inverter.power_kw
            # Linear interpolation between 5kW ($450) and 10kW ($600)
            if inverter_kw <= 5.0:
                return 450.0
            elif inverter_kw >= 10.0:
                return 600.0
            else:
                # Linear scaling between 5kW and 10kW
                return 450.0 + ((inverter_kw - 5.0) / 5.0) * (600.0 - 450.0)
        return 0.0
    
    @property
    def total_system_cost(self) -> float:
        """Calculate total system cost including equipment, labor, and support materials"""
        cost = 0.0
        if self.solar_panels:
            cost += self.solar_panels.cost_per_panel * self.solar_panels.quantity
        if self.battery:
            cost += self.battery.total_cost  # Use total_cost to handle multiple batteries
        if self.inverter:
            cost += self.inverter.cost
        # Add labor and support material costs
        cost += self.labor_cost
        cost += self.support_material_cost
        return cost

@dataclass
class SimulationResult:
    """Results from hourly simulation"""
    hour: int
    pv_generation_kw: float
    load_kw: float
    battery_charge_kw: float
    battery_discharge_kw: float
    battery_soc: float  # State of charge (0-100%)
    grid_import_kw: float
    grid_export_kw: float
    energy_surplus_kw: float

@dataclass
class FinancialAnalysis:
    """Financial calculations for solar system"""
    total_system_cost: float
    annual_savings: float
    payback_period_years: float
    roi_percent: float
    lifetime_savings: float  # 25 years
    monthly_savings: float
    co2_reduction_kg_per_year: float = 0.0
    currency: str = "USD"
