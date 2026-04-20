
import math

# =============================================
# VTOL UAV MTOW & Performance Sizing Tool
# =============================================

def get_user_inputs():
    print("\n=== VTOL UAV Sizing Tool ===")
    print("Enter the following parameters:\n")

    payload = float(input("Payload weight (kg): "))
    battery_weight = float(input("Battery weight (kg): "))
    propulsion_weight = float(input("Propulsion system weight (kg): "))
    avionics_weight = float(input("Avionics weight (kg): "))
    structure_fraction = float(input("Structure weight fraction (e.g. 0.25 for 25%): "))

    num_motors = int(input("Number of motors: "))
    thrust_factor = float(input("Thrust-to-Weight ratio (e.g. 2.0 for hover + margin): "))

    battery_capacity = float(input("Battery capacity (Ah): "))
    usable_fraction = float(input("Usable battery fraction (e.g. 0.8): "))

    hover_current = float(input("Hover current draw (A): "))
    cruise_current = float(input("Cruise current draw (A): "))
    launch_current = float(input("Launch/Transition current draw (A): "))
    launch_time = float(input("Launch/Transition time (seconds): "))

    return {
        "payload": payload,
        "battery_weight": battery_weight,
        "propulsion_weight": propulsion_weight,
        "avionics_weight": avionics_weight,
        "structure_fraction": structure_fraction,
        "num_motors": num_motors,
        "thrust_factor": thrust_factor,
        "battery_capacity": battery_capacity,
        "usable_fraction": usable_fraction,
        "hover_current": hover_current,
        "cruise_current": cruise_current,
        "launch_current": launch_current,
        "launch_time": launch_time
    }


def compute_mtow(data):
    '''Calculate Maximum Take-Off Weight (MTOW)'''
    known_weight = (
        data["payload"]
        + data["battery_weight"]
        + data["propulsion_weight"]
        + data["avionics_weight"]
    )
    mtow = known_weight / (1 - data["structure_fraction"])
    return mtow, known_weight


def compute_thrust(mtow, num_motors, thrust_factor):
    '''Calculate required thrust'''
    g = 9.81
    weight_newton = mtow * g
    total_thrust = thrust_factor * weight_newton
    thrust_per_motor = total_thrust / num_motors
    return weight_newton, total_thrust, thrust_per_motor


def compute_flight_time(data, mtow):
    '''Estimate cruise flight time after launch/transition'''
    usable_capacity = data["battery_capacity"] * data["usable_fraction"]  # Ah
    launch_consumption = (data["launch_current"] * data["launch_time"]) / 3600  # Ah

    remaining_capacity = usable_capacity - launch_consumption

    # Simple estimation: using cruise current
    if data["cruise_current"] > 0:
        cruise_time_hours = remaining_capacity / data["cruise_current"]
        cruise_time_minutes = cruise_time_hours * 60
    else:
        cruise_time_minutes = 0

    return cruise_time_minutes


def main():
    print("VTOL UAV MTOW & Flight Time Calculator")
    print("=====================================\n")

    data = get_user_inputs()

    # Calculations
    mtow, known_weight = compute_mtow(data)
    weight_n, total_thrust, thrust_per_motor = compute_thrust(
        mtow, data["num_motors"], data["thrust_factor"]
    )
    flight_time = compute_flight_time(data, mtow)

    # Results
    print("\n" + "="*50)
    print("                  CALCULATION RESULTS")
    print("="*50)
    print(f"Known Fixed Weight      : {known_weight:.3f} kg")
    print(f"Structure Fraction      : {data['structure_fraction']*100:.1f}%")
    print(f"Maximum Take-Off Weight : {mtow:.3f} kg")
    print(f"Total Weight (Force)    : {weight_n:.2f} N")
    print(f"Required Thrust-to-Weight : {data['thrust_factor']:.2f}")
    print(f"Total Thrust Required   : {total_thrust:.2f} N")
    print(f"Thrust per Motor        : {thrust_per_motor:.2f} N")
    print(f"Estimated Cruise Time   : {flight_time:.1f} minutes")
    print("="*50)

    # Optional: Show breakdown
    print("\nBreakdown of MTOW:")
    print(f"  Payload          : {data['payload']:.2f} kg")
    print(f"  Battery          : {data['battery_weight']:.2f} kg")
    print(f"  Propulsion       : {data['propulsion_weight']:.2f} kg")
    print(f"  Avionics         : {data['avionics_weight']:.2f} kg")
    print(f"  Structure        : {(mtow - known_weight):.2f} kg")
    print(f"  -------------------------------")
    print(f"  Total MTOW       : {mtow:.2f} kg")


if __name__ == "__main__":
    main()
