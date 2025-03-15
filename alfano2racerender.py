import pandas as pd
import tkinter as tk
from tkinter import ttk
from io import StringIO
from tkinter import filedialog, messagebox
import os
import zipfile

def extract_sort_key(filename):
    parts = filename.split('_')
    if len(parts) > 2 and parts[1].isdigit():
        return int(parts[1])  # Use the second number in the filename as the sorting key
    return float('inf')  # Default to a high number if unexpected format

def extract_lap_from_filename_section(filename):
    parts = filename.split('_')
    if len(parts) > 2:
        return parts[1]  # Extract content between the second pair of '_'
    return filename  # Fallback to original filename if format is unexpected

def transform(selected_alfano,include_partials,zip_path,master_file,input_files, output_csv):
    try:
        # Create a dictionary to map (Lap, Partiel) to Time Partiel values
        time_partiel_mapping = {}
        best_partiel_mapping = {}  
        if master_file is not None:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                with zip_ref.open(master_file[0], 'r') as file:
                        # Decode file content and split into lines
                        csv_data_cleaned = file.read().decode('utf-8').splitlines()[1:]        

                        # Join the remaining lines back into a string
                        csv_data_string = "\n".join(csv_data_cleaned)

                        # Convert the string into a file-like object
                        csv_data_io = StringIO(csv_data_string)

                        # Read the cleaned data into a pandas DataFrame
                        df2 = pd.read_csv(csv_data_io)
                        best_lap_time = (df2["time lap"].min())/1000
                        print(f"Best Lap Time: {best_lap_time}")
                        partial_columns = [col for col in df2.columns if "time partiel" in col]
                        total_partials = len(partial_columns)
                        total_laps = len(df2["lap"])
                        print(f"Total track partials: {total_partials}")
                        print(f"Full laps completed:{total_laps}")
                        for column in partial_columns:
                            best_partial_time = (df2[column].min())/1000
                            #print(f"Best {column}: {best_partial_time}")
                        for _, row in df2.iterrows():
                            lap = row["lap"]
                            for i in range(1, total_partials + 1): 
                                key = (lap, i)
                                time_partiel_mapping[key] = row[f"time partiel {i}"]/1000
                        for i in range(1, total_partials + 1):
                            column_name = f"time partiel {i}"
                            if column_name in df2.columns:
                                best_partiel_mapping[i] = df2[column_name].min()/1000
                    

        # Sort files by the lap number in their filename
        input_files = sorted(input_files, key=lambda x: extract_sort_key(x.split('/')[-1]))

        dataframes = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:      
            for lap_file in input_files:
                with zip_ref.open(lap_file) as f:
                    df = pd.read_csv(f)
                    if(selected_alfano == 'Alfano 6'):
                        df['Time'] = [round(i * 0.1, 1) for i in range(len(df))]
                    elif(selected_alfano == 'Alfano 7'):
                        df['Time'] = [round(i * 0.04, 2) for i in range(len(df))]
                    else:
                        raise Exception("Device not supported")
                    col = df.pop('Time')
                    df.insert(0,'Time',col)
                    
                    if 'Lat.' in df.columns:
                        df['Lat.'] = (df['Lat.'] / 1000000).round(8)
                        df.rename(columns={'Lat.': 'Latitude'}, inplace=True)
                    if 'Lon.' in df.columns:
                        df['Lon.'] = (df['Lon.'] / 1000000).round(8)
                        df.rename(columns={'Lon.': 'Longitude'}, inplace=True)
                    if 'T1' in df.columns:
                        df['T1'] = (df['T1'] / 10).round(2)
                        df['T1(f)'] = ((df['T1']*9/5) + 32).round(2)
                    if 'T2' in df.columns:
                        df['T2'] = (df['T2'] / 10).round(2)
                        df['T2(f)'] = ((df['T2']*9/5) + 32).round(2)
                    if 'Orientation' in df.columns:
                        df['Orientation'] = (df['Orientation'] / 100).round(2)
                    if 'Altitute' in df.columns:
                        df['Altitute'] = (df['Altitute'] / 10).round(2)
                    if 'Speed GPS' in df.columns:
                        df['Speed GPS'] = (df['Speed GPS'] / 10).round(2)
                        df['MPH'] = (df['Speed GPS'] * 0.621371).round(2)
                    if 'Speed rear' in df.columns:
                        df['Speed rear'] = (df['Speed rear'] / 10).round(2)
                    if 'Gf. X' in df.columns:
                        df['Gf. X'] = ((df['Gf. X']/100)-9.8).round(2)* -1
                        df.rename(columns={'Gf. X': 'Y'}, inplace=True)
                    if 'Gf. Y' in df.columns:
                        df['Gf. Y'] = ((df['Gf. Y']/100)-9.8).round(2)
                        df.rename(columns={'Gf. Y': 'X'}, inplace=True)

                    # Add source file name as a new column
                    lap_number = extract_lap_from_filename_section(lap_file.split('/')[-1])  # Extracts lap from path
                    df['Lap'] = lap_number

                    #we try to find the exact laptime in the master file
                    if master_file is not None:
                        timelap = df2.loc[df2['lap'] == int(lap_number), 'time lap']
                        if not timelap.empty:
                            #if we find it we modify the last record of the lap with it
                            value =(timelap.iloc[0]/ 1000).round(3)
                            last_index = df.index[-1]
                            df.at[last_index, 'Time'] = value
                        if include_partials:
                            df["Lap"] = df["Lap"].astype(int)
                            df["Partiel"] = df["Partiel"].astype(int)
                            df["Partiel Time"] = df.apply(lambda row: time_partiel_mapping.get((row["Lap"], row["Partiel"]), '999'), axis=1) 
                            df["Partiel Time"] = df["Partiel Time"].astype(int)
                            df["Best Partiel Time"] = df["Partiel"].map(best_partiel_mapping)
                            df["Partiel Differece With Best"] = (df["Partiel Time"]-df["Best Partiel Time"]).round(2)
                            
                            df["Previous Partiel Time"] = df.apply(lambda row: time_partiel_mapping.get((int(row["Lap"]), int(row["Partiel"]) - 1), None) 
                                                                    if row["Partiel"] > 1 else time_partiel_mapping.get((int(row["Lap"]) - 1, total_partials), None), axis=1)
                            df["Best Previous Partiel Time"]= df.apply(lambda row: best_partiel_mapping.get(( int(row["Partiel"]) - 1), None)
            if row["Partiel"] > 1 else best_partiel_mapping.get((6), None), axis=1)
                            df["Previous Partiel Difference With Best"] = (df["Previous Partiel Time"]-df["Best Previous Partiel Time"]).round(2)
            
                    dataframes.append(df)
            
        
        # Concatenate all dataframes into one
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_csv(output_csv, index=False)
        messagebox.showinfo("Success", f"Consolidated CSV saved as: {output_csv}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_files():
    selected_alfano = selected_option.get()
    include_partials = partials_checkbox.get()
    print(f"Selected Dropdown: {selected_alfano}")
    print(f"Partials Checked: {include_partials}")

    zip_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
    if not zip_path:
        return
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            lap_file_paths = [f for f in zip_ref.namelist() if f.endswith('.csv') and f.startswith('LAP_')]
            master_file_path = [f for f in zip_ref.namelist() if f.endswith('.csv') and f.startswith('SN')]
            
            if not (lap_file_paths):
                messagebox.showinfo("No CSVs", "No CSV files starting with 'LAP_' found in the ZIP")
                return
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            transform(selected_alfano,include_partials,zip_path,master_file_path,lap_file_paths, save_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read ZIP file: {e}")

# Create UI
root = tk.Tk()
if os.path.exists('icon.ico'):
    root.iconbitmap('icon.ico')
root.title("Alfano to RaceRender converter by Full Send Racing")
root.geometry("500x250")

# Dropdown options
supported_alfanos = ["Alfano 6", "Alfano 7"]

# Create a StringVar to hold the selected value
selected_option = tk.StringVar()

dropdown = ttk.Combobox(root, textvariable=selected_option, values=supported_alfanos, state="readonly")
dropdown.pack(pady=5)

# Set default value
dropdown.current(0)

# Checkbox variable
partials_checkbox = tk.BooleanVar()
partials_checkbox.set = True

# Create a Checkbox
checkbox = tk.Checkbutton(root, text="Add Partial Sector Times", variable=partials_checkbox)
checkbox.pack(pady=5)

tk.Label(root, text="1. Select zip file generated from the Alfano ADA app.").pack(pady=10)
tk.Label(root, text="2. Select where to create output file.").pack(pady=10)

tk.Button(root, text="Start", command=select_files).pack(pady=10)

tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()

