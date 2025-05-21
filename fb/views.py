from django.shortcuts import render, HttpResponse, redirect
import multiprocessing, io
import pandas as pd
from .auto import main_handler
import os
import datetime
import zipfile
from django.http import HttpResponse, FileResponse
from django.conf import settings
from io import BytesIO

# Create your views here.
def facebook(request):
    if not request.user.is_authenticated:
        print('User not logged In........')
        return redirect('/')

    if request.method == 'POST':
        uploaded_file = request.FILES.get('csv_file')
        print(uploaded_file)
        file_data = uploaded_file.read().decode('utf-8')
        csv_reader = pd.read_csv(io.StringIO(file_data))

        univeri = request.FILES.get('uni')  
        print(univeri)
        file_data1 = univeri.read().decode('windows-1252')  
        univer = pd.read_csv(io.StringIO(file_data1))
        print(univer)

        row = csv_reader.shape[0]
        print(row)

        processes = []
        max_workers = 1
        username = request.user.username
        print(username)

        # Start processes that run the task in parallel
        for i, row in csv_reader.iterrows():
            uname = row['username']
            pas = row['password']
            print(uname, pas)

            while len(processes) >= max_workers:
                # Iterate over the processes to check if any have finished
                for p in processes:
                    if not p.is_alive():  # If the process is not running
                        p.join()  # Clean up the process
                        processes.remove(p)  # Remove it from the list
                        break 

            process = multiprocessing.Process(target=main_handler, args=(uname, pas, univer, i, username))
            processes.append(process)
            process.start()

        # Wait for all processes to complete
        for process in processes:
            process.join()

    return render(request, 'fb/upload.html')


def display_excel(request):
    file_path = "visited_profiles.xlsx"

    if not os.path.exists(file_path):
        print("❌ File not found!")  # Debugging line
        return HttpResponse("Error: Excel file not found!", status=404)

    try:
        df = pd.read_excel(file_path)
        print("✅ File loaded successfully!")  # Debugging line
        # Convert datetime safely to string or empty string
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].apply(
                    lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if pd.notnull(x) else ""
                )
        data = df.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Error reading file: {e}")  # Debugging line
        return HttpResponse(f"Error reading file: {e}", status=500)

    return render(request, "excel_template.html", {"data": data})


# def summary_table(request):
#     file_path = "execution_log.csv"

#     if not os.path.exists(file_path):
#         print("❌ File not found!")  # Debugging line
#         return HttpResponse("Error: Excel file not found!", status=404)

#     try:
#         df = pd.read_csv(file_path)
#         print("✅ File loaded successfully!")  # Debugging line
#         data = df.to_dict(orient="records")
#     except Exception as e:
#         print(f"❌ Error reading file: {e}")  # Debugging line
#         return HttpResponse(f"Error reading file: {e}", status=500)

#     return render(request, "summary.html", {"data": data})
# def fb_user_searched(request):
#     file_path = "profile_data.csv"
#     if not os.path.exists(file_path):
#         print("❌ File not found!")
#         return HttpResponse("Error: CSV file not found!", status=404)
#     try:
#         df = pd.read_csv(file_path)
#         print("✅ File loaded successfully!")  # Debugging line
#         data = df.to_dict(orient="records")
#     except Exception as e:
#         print(f"❌ Error reading file: {e}")
#         return HttpResponse(f"Error reading file: {e}", status=500)
#     return render(request, "fb/fb_users_searched.html", {"data": data})


import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

def fb_user_searched(request):
    import os
    import pandas as pd
    from django.http import HttpResponse
    from django.shortcuts import render

    file_path = "profile_data.csv"
    
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return HttpResponse("Error: CSV file not found!", status=404)
    
    try:
        # Try reading with UTF-8 first
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except UnicodeDecodeError as e:
            print(f"⚠️ UTF-8 decode error: {e}, trying fallback encoding...")
            df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Fallback to Latin-1
        print("✅ File loaded successfully!")  # Debugging line
        
        data = df.to_dict(orient="records")

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return HttpResponse(f"Error reading file: {e}", status=500)
    
    return render(request, "fb/fb_users_searched.html", {"data": data})



def log_session_visits(request):
    import os
    import pandas as pd
    from django.http import HttpResponse
    from django.shortcuts import render

    file_path = "log_session_visits.xlsx"
    
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return HttpResponse("Error: XLSX file not found!", status=404)
    
    try:
        df = pd.read_excel(file_path)
        print("✅ File loaded successfully!")

        df["Delivered_Time"] = pd.to_datetime(df["Delivered_Time"], errors="coerce")
        df["Find_Time"] = pd.to_datetime(df["Find_Time"], errors="coerce")

        # Conditional datetime formatting
        df["Delivered_Time"] = df.apply(
            lambda row: "null" if row["Delivered_Status"] == "pending" else (
                row["Delivered_Time"].strftime("%Y-%m-%d %H:%M:%S") if pd.notnull(row["Delivered_Time"]) else ""
            ),
            axis=1
        )

        df["Find_Time"] = df["Find_Time"].apply(
            lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if pd.notnull(x) else ""
        )

        data = df.to_dict(orient="records")

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return HttpResponse(f"Error reading file: {e}", status=500)
    
    return render(request, "fb/messages.html", {"data": data})



def conversation(request):
    file_path = "Unread_profiles.xlsx"
    
    if not os.path.exists(file_path):
        print("❌ File not found!")  # Debugging line
        return HttpResponse("Error: CSV file not found!", status=404)
    
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_excel(file_path, engine="openpyxl")
        print("✅ File loaded successfully!")  # Debugging line
        
        # Convert DataFrame to a list of dictionaries (records)
        data = df.to_dict(orient="records")
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")  # Debugging line
        return HttpResponse(f"Error reading file: {e}", status=500)
    
    # Render the template with the data
    return render(request, "fb/conversation.html", {"data": data})

def summary_table(request):
    file_path = "execution_log.csv"
    # Read the username from the temp file
    try:
        with open("temp_username.txt", "r") as f:
            username = f.read().strip()
    except FileNotFoundError:
        username = "Guest"

    if not os.path.exists(file_path):
        print("❌ File not found!")  # Debugging line
        return HttpResponse("Error: CSV file not found!", status=404)

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        print("✅ File loaded successfully!")  # Debugging line

        # Convert DataFrame to a list of dictionaries
        data = df.to_dict(orient="records")
        
        # Define columns for which we need totals
        columns_to_sum = [
            "profiles_fetched", "profiles_visited", "messages_sent",
            "responses_received", "already_sent", "carry_forward_profiles",
            "carry_forward_messages", "duration (sec)","profiles_matched"

        ]

        # Calculate totals for the specified columns
        totals = {}
        totals["session number"] = "Total"
        for col in columns_to_sum:
            if col in df.columns:
                totals[col] = df[col].sum()
            else:
               totals[col] = "N/A"

        # Handle duration separately (if it's stored as strings)
        total_seconds = df["duration (sec)"].sum()
        time_duration = str(datetime.timedelta(seconds=int(total_seconds)))
        if "duration (hh:mm:ss)" in df.columns:
            totals["duration (hh:mm:ss)"] = time_duration

    except Exception as e:
        print(f"❌ Error reading file: {e}")  # Debugging line
        return HttpResponse(f"Error reading file: {e}", status=500)
    
    return render(request, "fb/summary.html", {"data": data, "totals": totals, "username": username})

# def download_report(request):
#     # Define the original file paths and desired names in the ZIP
#     files_to_include = [
#         (os.path.join(settings.BASE_DIR, "profile_data.csv"), "facebook users.csv"),
#         (os.path.join(settings.BASE_DIR, "log_session_visits.xlsx"), "messages.csv"),  # Will convert below
#         (os.path.join(settings.BASE_DIR, "fb", "Unread_Profiles.xlsx"), "conversation.csv"),  # Will convert below
#         (os.path.join(settings.BASE_DIR, "execution_log.csv"), "summary.csv"),
#     ]

#     # Create a zip in memory
#     zip_buffer = BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as zip_file:
#         for original_path, renamed_filename in files_to_include:
#             if os.path.exists(original_path):
#                 if original_path.endswith(".xlsx"):
#                     # Convert xlsx to csv
#                     import pandas as pd
#                     df = pd.read_excel(original_path)
#                     csv_bytes = df.to_csv(index=False).encode("utf-8")
#                     zip_file.writestr(renamed_filename, csv_bytes)
#                 else:
#                     with open(original_path, "rb") as f:
#                         zip_file.writestr(renamed_filename, f.read())

#     zip_buffer.seek(0)

#     return FileResponse(zip_buffer, as_attachment=True, filename="todays_report.zip")
def download_report(request):
    # Define the original file paths and desired sheet names
    files_to_include = [
        (os.path.join(settings.BASE_DIR, "profile_data.csv"), "Facebook Users"),
        (os.path.join(settings.BASE_DIR, "log_session_visits.xlsx"), "Messages"),
        (os.path.join(settings.BASE_DIR, "Unread_profiles.xlsx"), "Conversation"),
        (os.path.join(settings.BASE_DIR, "execution_log.csv"), "Summary"),
    ]

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for file_path, sheet_name in files_to_include:
            if os.path.exists(file_path):
                if file_path.endswith(".csv"):
                    df = pd.read_csv(file_path, encoding='latin-1')
                elif file_path.endswith(".xlsx"):
                    df = pd.read_excel(file_path)
                else:
                    continue  # Skip unsupported formats

                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Sheet names max 31 chars

    output.seek(0)
    return FileResponse(output, as_attachment=True, filename="todays_report.xlsx")


def download_file(request, filename):
    base_dir = r'C:\Users\Mahnoor-zubair\Desktop\main - Copy\main - Copy'
    file_path = os.path.join(base_dir, filename)

    if os.path.exists(file_path):
        if filename.endswith('.csv') or filename.endswith('.xlsx'):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        else:
            return HttpResponse("Only CSV and XLSX files are allowed.", status=400)
    else:
        return HttpResponse("File not found.", status=404)
