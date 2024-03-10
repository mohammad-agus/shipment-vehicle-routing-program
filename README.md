Number of Vehicle   : 2
Vehicle 1
    Capacity        : 100
    Start time      : 2024-06-01 08:30
    End time        : 2024-06-01 10:30
Vehicle 2
    Capacity        : 85
    Start time      : 2024-06-01 09:30
    End time        : 2024-06-01 12:30


# Shipment Vehicle Routing App
## Project Description
This project is a Python application developed as the final project for the CS50 Introduction to Computer Science course at Harvard University. The app is designed to efficiently route shipment vehicles based on input data provided either in CSV format or manually. It utilizes the Vehicle Routing Problem (VRP) solver from the OpenRouteService API to optimize routes. The app also utilizes several third-party Python libraries including dotenv for secure storage of API keys, folium for map visualization, and tabulate for summarizing routing results.

## Technologies Used
Python
dotenv: For storing API keys securely.
folium: For visualizing maps and vehicle routes.
tabulate: For visualizing the summary of routing results.
OpenRouteService API: For solving the Vehicle Routing Problem.
Installation
Clone this repository:
bash
Copy code
git clone https://github.com/yourusername/shipment-vehicle-routing-app.git
Navigate to the project directory:
bash
Copy code
cd shipment-vehicle-routing-app
Install dependencies:
bash
Copy code
pip install -r requirements.txt


## Usage
Obtain an API token from OpenRouteService:

Visit the OpenRouteService website and sign up for a free account if you haven't already.
Once logged in, navigate to your account settings or dashboard to generate an API token.
Copy the generated API token.
Add the API token to the app:

Open the main.py script in a text editor.
Locate the line where the API token is required. It might be indicated with a comment or within a function/method that interacts with the OpenRouteService API.
Replace the existing API token with your own token:
python
Copy code
API_TOKEN = "YOUR_API_TOKEN_HERE"
Provide data in CSV format:

Prepare a CSV file containing the necessary information about route points (start, shipment points, and ending points), including latitude, longitude, delivery amount, and service time.
Run the app:
bash
Copy code
python main.py --csv path/to/your/data.csv
Input data manually:

Run the app:
bash
Copy code
python main.py --manual
Follow the prompts to input the number of vehicles, vehicle capacity, time window (in YYYY-MM-DD HH-SS format), and other relevant information.
Review the summary:

Once the inputted data is correct, the app will return a summary of the routing results.
It will also generate a route map in HTML format for visualization.
Features
Efficiently solves the Vehicle Routing Problem using the OpenRouteService API.
Supports data input from CSV files or manual input.
Visualizes maps and optimized vehicle routes using folium.
Provides a summary of routing results in a tabular format using tabulate.


## Examples
[Include examples or screenshots demonstrating how the app works.]


```
Input csv file: input.csv
Input number of vehicle: 2
Input vehicle 1 capacity: 100
Date and time format: "YYYY-MM-DD HH:mm"
Input shipment schedule (date & time) of vehicle 1 (in  format):
Begin: 2024-06-01 08:30
End: 2024-06-01 10:30
Input vehicle 2 capacity: 85
Date and time format: "YYYY-MM-DD HH:mm"
Input shipment schedule (date & time) of vehicle 2 (in  format):
Begin: 2024-06-01 09:30
End: 2024-06-01 12:30
```


| id               | lat                | long               | delivery_amount | service |
| ---------------- | ------------------ | ------------------ | --------------- | ------- |
| start_point      | 0.5705953948161725 | 123.05911896076756 | 0               | 0       |
| end_point        | 0.5461229144422185 | 123.07928098393106 | 0               | 0       |
| shipment_point01 | 0.5631471392390268 | 123.05288470178134 | 40              | 1200    |
| shipment_point02 | 0.5593274803137437 | 123.06239670199969 |  30             | 900     |
| shipment_pointn  | ...                | ...                | ...             | ...     |

## Credits
dotenv
folium
tabulate
OpenRouteService
License
[Specify the license under which your project is distributed, if applicable.]

This comprehensive README.md file provides users with all the necessary information to understand, install, and use your Shipment Vehicle Routing App. Adjust as necessary to fit your project's specific details and preferences.