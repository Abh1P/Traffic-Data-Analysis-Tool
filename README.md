# Traffic-Data-Analysis-Tool and Visualization Tool

## Overview

This project is a Python-based application developed for the 4COSC001W Software Development I module at the University of Westminster. The tool is designed to analyze traffic flow data from CSV files and provide statistical insights and a visual summary.

The goal of the project was to build a tool that allows a user to select a traffic survey dataset by date and then:
1.  Calculate a series of specified statistical outcomes.
2.  Display these results to the user in the console.
3.  Append the results to a cumulative `results.txt` file.
4.  Generate a graphical histogram comparing hourly traffic volume for two key junctions using a provided `graphics.py` library.

The application was required to handle user input errors gracefully and allow for the analysis of multiple files in a single session.

## Key Features

-   **User Input and Validation**:
    -   Prompts the user to enter a date (day, month, year) to select the correct CSV data file.
    -   Validates that all inputs are integers and fall within logical ranges (e.g., day 1-31, month 1-12).
    -   Provides clear error messages for invalid input.

-   **Comprehensive Data Analysis**:
    -   Processes the selected CSV file to calculate 16 required statistical outcomes, such as total vehicle counts, number of trucks, electric vehicles, vehicles exceeding the speed limit, and busiest hours of traffic.

-   **Automated Reporting**:
    -   Prints a formatted summary of the analysis to the console.
    -   Appends the summary to a `results.txt` file, preserving a log of all analyses performed.

-   **Graphical Visualization**:
    -   Uses the `graphics.py` module exclusively to render a bar chart.
    -   The histogram visually compares the volume of traffic per hour for the "Elm Avenue/Rabbit Road" and "Hanley Highway/Westway" junctions.
    -   Includes a dynamic title with the selected date, a labeled x-axis, and a color-coded legend for clarity.

-   **Interactive Session Loop**:
    -   After each analysis, the user is asked if they wish to process another file.
    -   The program loops or terminates based on user input (`Y/N`), gracefully handling both uppercase and lowercase letters.
 
## Technologies Used

-   **Language**: Python 3
-   **Libraries**:
    -   `csv` for parsing data files.
    -   `os` for file system interactions.
    -   `graphics.py` (a custom Tkinter-based graphics library) for all visualizations.

## Setup and Usage

### Prerequisites

-   Python 3.x must be installed on your system.
-   The `Tkinter` library, which is included with most Python installations, is required for the `graphics.py` module to function.

### File Structure

Ensure the following files are in the same directory:

```
.
├── Traffic-Data-Analysis-Tool.py   # Main application script
├── graphics.py                     # Required graphics library
├── traffic_data15062024.csv        # Sample dataset 1
├── traffic_data21062024.csv        # Sample dataset 2
└── ...                             # Other potential data files
```

### Running the Application

1.  Navigate to the project directory in your terminal or command prompt.
2.  Run the main script using the following command:

    ```bash
    python Traffic-Data-Analysis-Tool.py
    ```

3.  Follow the on-screen prompts to enter the date (day, month, year) for the dataset you wish to analyze.
4.  The analysis results will be printed to the console and saved to `results.txt`.
5.  A new window will pop up displaying the histogram. **Click anywhere on the histogram window to close it** and continue the program.
6.  You will then be prompted to analyze another dataset or exit the program.
