import os

def load_patient_data(username):
    # This function loads the user's patient data and daily readings from the data file
    # Create the file path based on the username and the PatientData folder
    data_folder = "PatientData"
    data_file_path = os.path.join(data_folder, f"{username.replace(' ', '')}Data.txt")
    print(f"{username.replace(' ', '')}Data.txt")
    patient_info = None
    daily_readings = []
    
    try:
        with open(data_file_path, 'r') as file:
            # Read the first line as patient data
            patient_data = file.readline().strip()
            # Parse the first line for patient information
            name, patient_id, doctor_name, doctor_phone, low_glucose, high_glucose = patient_data.split(',')
            
            # Store patient information
            patient_info = {
                "name": name.strip(),
                "patient_id": patient_id.strip(),
                "doctor_name": doctor_name.strip(),
                "doctor_phone": doctor_phone.strip(),
                "low_glucose": low_glucose.strip(),
                "high_glucose": high_glucose.strip()
            }

            # Read the remaining lines as daily readings
            for line in file:
                reading_date, glucose_level, reason_level = line.strip().split(',')
                # Store daily reading data as a tuple of date and glucose level
                daily_readings.append((reading_date.strip(), glucose_level.strip(), reason_level.strip()))

    except FileNotFoundError:
        # If the data file is not found, return None for patient_info and daily_readings
        return None, []

    # Return the parsed patient info and daily readings
    return patient_info, daily_readings

def save_patient_data(username, date, glucose_level, reason_level):
    # This function saves a new daily glucose reading data to the patient's data file
    # Create the file path based on the username and the PatientData folder
    data_folder = "PatientData"
    data_file_path = os.path.join(data_folder, f"{username.replace(' ', '')}Data.txt")
    
    # Format the data as a comma-separated string
    new_reading = f"{date}, {glucose_level}, {reason_level}"
    
    try:
        # Open the data file in append mode
        with open(data_file_path, 'a') as file:
            # Write the new reading data to the file
            file.write('\n' + new_reading)
        print(f"Saved new reading for {username}: {new_reading}")
    except Exception as e:
        print(f"Error saving data for {username}: {e}")