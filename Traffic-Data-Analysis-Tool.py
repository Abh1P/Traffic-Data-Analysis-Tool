

from graphics import *
import csv
import os

# --- Task A: Input Validation ---

def get_validated_input(prompt, error_msg, min_val, max_val):
    """
    Prompts the user for an integer input within a specified range,
    handling both incorrect data types and out-of-range values.

    Args:
        prompt (str): The message to display to the user.
        error_msg (str): The message to display for a range error.
        min_val (int): The minimum acceptable integer value.
        max_val (int): The maximum acceptable integer value.

    Returns:
        int: A validated integer from the user.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Out of range - {error_msg}")
        except ValueError:
            print("Integer required")

def get_user_date():
    """
    Prompts the user to enter a day, month, and year, validates the input,
    and returns it in a formatted string tuple.

    Returns:
        tuple: A tuple containing the formatted day, month, and year as strings.
               Returns (None, None, None) if the user wishes to exit.
    """
    print("Please enter the date of the survey.")
    day = get_validated_input(
        "Enter the day in the format dd: ",
        "values must be in the range 1 and 31.", 1, 31
    )
    month = get_validated_input(
        "Enter the month in the format MM: ",
        "values must be in the range 1 to 12.", 1, 12
    )
    year = get_validated_input(
        "Enter the year in the format YYYY: ",
        "values must range from 2000 and 2024.", 2000, 2024
    )
    
    # Format with leading zeros
    day_str = f"{day:02d}"
    month_str = f"{month:02d}"
    year_str = str(year)
    
    return day_str, month_str, year_str

def load_data(filename):
    """
    Loads data from a specified CSV file.

    Args:
        filename (str): The name of the CSV file to load.

    Returns:
        list: A list of lists containing the CSV data, or an empty list if
              the file is not found.
    """
    data_list = []
    if not os.path.exists(filename):
        print(f"\nError: Data file not found: {filename}")
        print("Please ensure the file is in the same directory as the program.")
        return None

    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # Skip header
        for row in csvreader:
            data_list.append(row)
    return data_list


# --- Task B: Outcomes ---

def calculate_outcomes(data_list, filename):
    """
    Processes the loaded traffic data to calculate and print all required outcomes.

    Args:
        data_list (list): The list of traffic data records.
        filename (str): The name of the data file being processed.

    Returns:
        list: A list of strings, where each string is a formatted result.
    """
    # Initialize counters and collectors
    total_vehicles = len(data_list)
    total_trucks = 0
    total_electric = 0
    two_wheeled_vehicles = 0
    buses_north_elm = 0
    no_turn_vehicles = 0
    speeding_vehicles = 0
    elm_junction_vehicles = 0
    hanley_junction_vehicles = 0
    elm_scooters = 0
    total_bicycles = 0
    
    hanley_hourly_counts = {i: 0 for i in range(24)}
    rainy_hours = set()

    # Process each record
    for record in data_list:
        junction = record[0]
        weather = record[5]
        speed_limit = int(record[6])
        vehicle_speed = int(record[7])
        vehicle_type = record[8]
        is_electric = record[9]
        direction_in = record[3]
        direction_out = record[4]
        time_of_day = record[2]
        hour = int(time_of_day.split(':')[0])

        # Increment junction-specific counters
        if junction == "Elm Avenue/Rabbit Road":
            elm_junction_vehicles += 1
            if vehicle_type == "Scooter":
                elm_scooters += 1
            if vehicle_type == "Buss" and direction_out == 'N':
                buses_north_elm += 1
        elif junction == "Hanley Highway/Westway":
            hanley_junction_vehicles += 1
            hanley_hourly_counts[hour] += 1
            
        # Increment general counters
        if vehicle_type == "Truck":
            total_trucks += 1
        if is_electric == 'True':
            total_electric += 1
        if vehicle_type in ["Bicycle", "Motorcycle", "Scooter"]:
            two_wheeled_vehicles += 1
        if direction_in == direction_out:
            no_turn_vehicles += 1
        if vehicle_speed > speed_limit:
            speeding_vehicles += 1
        if vehicle_type == "Bicycle":
            total_bicycles += 1
        if "Rain" in weather:
            rainy_hours.add(hour)

    # Final calculations
    truck_percentage = round((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0
    avg_bicycles_per_hour = round(total_bicycles / 24)
    elm_scooter_percentage = round((elm_scooters / elm_junction_vehicles) * 100) if elm_junction_vehicles > 0 else 0
    total_rain_hours = len(rainy_hours)

    # Find busiest hour(s) for Hanley Highway
    busiest_hour_count = 0
    if hanley_junction_vehicles > 0:
        busiest_hour_count = max(hanley_hourly_counts.values())
        
    busiest_hours = [h for h, count in hanley_hourly_counts.items() if count == busiest_hour_count]
    
    busiest_hour_times = []
    for h in busiest_hours:
        busiest_hour_times.append(f"Between {h:02d}:00 and {h+1:02d}:00")
    busiest_hours_str = ", ".join(busiest_hour_times)
    
    # Collate results for printing and saving
    results = [
        "*******************************************",
        f"data file selected is {filename}",
        "*******************************************",
        f"The total number of vehicles recorded for this date is {total_vehicles}",
        f"The total number of trucks recorded for this date is {total_trucks}",
        f"The total number of electric vehicles for this date is {total_electric}",
        f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicles}",
        f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {buses_north_elm}",
        f"The total number of Vehicles through both junctions not turning left or right is {no_turn_vehicles}",
        f"The percentage of total vehicles recorded that are trucks for this date is {truck_percentage}%",
        f"the average number of Bikes per hour for this date is {avg_bicycles_per_hour}",
        f"The total number of Vehicles recorded as over the speed limit for this date is {speeding_vehicles}",
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {elm_junction_vehicles}",
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {hanley_junction_vehicles}",
        f"{elm_scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {busiest_hour_count}",
        f"The most vehicles through Hanley Highway/Westway were recorded {busiest_hours_str}",
        f"The number of hours of rain for this date is {total_rain_hours}"
    ]

    print("\n--- Analysis Results ---")
    for line in results:
        print(line)
    print("------------------------\n")
    
    return results

# --- Task C: Save Results to Text File ---

def save_results_to_file(results_list):
    """
    Appends the list of formatted result strings to 'results.txt'.

    Args:
        results_list (list): A list of strings containing the results to save.
    """
    try:
        with open("results.txt", "a") as f:
            for line in results_list:
                f.write(line + "\n")
            f.write("\n") # Add a blank line for separation
        print('Results have been successfully appended to results.txt')
    except IOError as e:
        print(f"Error: Could not write to file results.txt. {e}")

# --- Task D: Histogram ---

def draw_histogram(data_list, date_str):
    """
    Draws a histogram of vehicle frequency per hour for two junctions using graphics.py.

    Args:
        data_list (list): The list of traffic data records.
        date_str (str): The formatted date string for the histogram title.
    """
    # Prepare data for histogram
    elm_hourly = {i: 0 for i in range(24)}
    hanley_hourly = {i: 0 for i in range(24)}
    
    for record in data_list:
        hour = int(record[2].split(':')[0])
        if record[0] == "Elm Avenue/Rabbit Road":
            elm_hourly[hour] += 1
        else:
            hanley_hourly[hour] += 1

    max_vehicles = 0
    for hour in range(24):
        if elm_hourly[hour] > max_vehicles:
            max_vehicles = elm_hourly[hour]
        if hanley_hourly[hour] > max_vehicles:
            max_vehicles = hanley_hourly[hour]
    
    # Set up window and coordinates
    win_width = 800
    win_height = 600
    win = GraphWin(f"Histogram - {date_str}", win_width, win_height)
    # Set coordinates: x_left, y_bottom, x_right, y_top
    win.setCoords(-3.5, -max_vehicles * 0.2, 24.5, max_vehicles * 1.2)

    # Draw Title
    title = Text(Point(11, max_vehicles * 1.1), f"Histogram of Vehicle Frequency per Hour ({date_str})")
    title.setSize(16)
    title.setStyle("bold")
    title.draw(win)

    # Draw Axes
    Line(Point(-0.5, 0), Point(24, 0)).draw(win) # X-axis
    Line(Point(-0.5, 0), Point(-0.5, max_vehicles * 1.05)).draw(win) # Y-axis
    
    # Draw axis labels and ticks
    Text(Point(11.5, -max_vehicles * 0.15), "Hours 00:00 to 24:00").draw(win)
    for i in range(0, max_vehicles + 1, 10):
        Text(Point(-1.5, i), str(i)).draw(win)
        Line(Point(-0.6, i), Point(-0.4, i)).draw(win)

    # Draw Bars and hour labels
    bar_width = 0.4
    for hour in range(24):
        # Elm Avenue bar
        elm_count = elm_hourly[hour]
        elm_bar = Rectangle(Point(hour - bar_width, 0), Point(hour, elm_count))
        elm_bar.setFill("lightgreen")
        elm_bar.draw(win)
        if elm_count > 0:
            Text(Point(hour - bar_width/2, elm_count + max_vehicles*0.04), elm_count).draw(win)
            
        # Hanley Highway bar
        hanley_count = hanley_hourly[hour]
        hanley_bar = Rectangle(Point(hour, 0), Point(hour + bar_width, hanley_count))
        hanley_bar.setFill("lightblue")
        hanley_bar.draw(win)
        if hanley_count > 0:
            Text(Point(hour + bar_width/2, hanley_count + max_vehicles*0.04), hanley_count).draw(win)

        # Hour label on X-axis
        Text(Point(hour, -max_vehicles*0.05), f"{hour:02d}").draw(win)
        
    # Draw Legend
    legend_y = max_vehicles * 0.95
    Rectangle(Point(-3, legend_y), Point(-2.5, legend_y - max_vehicles*0.05)).setFill("lightgreen").draw(win)
    Text(Point(-1, legend_y - max_vehicles*0.025), "Elm Avenue/Rabbit Road").setAnchor("w").draw(win)
    
    legend_y2 = max_vehicles * 0.85
    Rectangle(Point(-3, legend_y2), Point(-2.5, legend_y2 - max_vehicles*0.05)).setFill("lightblue").draw(win)
    Text(Point(-1, legend_y2 - max_vehicles*0.025), "Hanley Highway/Westway").setAnchor("w").draw(win)

    print("Histogram window generated. Click on the window to close it.")
    win.getMouse()
    win.close()


# --- Task E: Code Loops ---

def ask_to_continue():
    """
    Asks the user if they want to process another file and validates their input.

    Returns:
        bool: True if the user wants to continue, False otherwise.
    """
    while True:
        choice = input("Do you want to select another data file for a different date? Y/N > ").lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        else:
            print('Please enter "Y" or "N"')


# --- Main Program Execution ---

def main():
    """
    The main function to run the traffic analysis program.
    """
    while True:
        day, month, year = get_user_date()
        
        filename = f"traffic_data{day}{month}{year}.csv"
        
        data = load_data(filename)
        
        if data:
            results_to_save = calculate_outcomes(data, filename)
            save_results_to_file(results_to_save)
            
            # Use a different date format for the title as per example
            display_date = f"{day}/{month}/{year}"
            draw_histogram(data, display_date)
        
        if not ask_to_continue():
            break

    print("\nEnd of run")

# Run the main program
if __name__ == "__main__":
    main()
