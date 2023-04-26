import os

# Get current working directory
cwd = os.getcwd()
print("Current working directory:", cwd)

# Check if Attendance.xlsx exists in current directory
attendance_file = 'Attendance.xlsx'
if os.path.isfile(attendance_file):
    print("Attendance file exists!")
else:
    print("Attendance file does not exist!")
