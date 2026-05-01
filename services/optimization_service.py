from services.demand_service import get_all_zone_demands

TOTAL_DRIVERS = 42

def optimize_driver_allocation(weather='clear', temperature=28):
    demands = get_all_zone_demands(weather=weather, temperature=temperature)
    total_demand = sum(d['demand'] for d in demands) or 1
    allocations = []
    for zone_data in demands:
        share = zone_data['demand'] / total_demand
        drivers = max(1, round(share * TOTAL_DRIVERS))
        allocations.append({
            'zone': zone_data['zone'],
            'demand': zone_data['demand'],
            'recommended_drivers': drivers,
            'priority': 'high' if zone_data['demand'] > 70 else 'medium' if zone_data['demand'] > 40 else 'low'
        })
    return allocations
