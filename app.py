import streamlit as st
import pandas as pd
import random

# Patient Class (it will contatin the patient data)
class Patient:
    """
    - severity is the value
    - treatment_time is the weight
    """
    def __init__(self, id, name, condition, severity, treatment_time):
        self.id = id
        self.name = name
        self.condition = condition
        self.severity = severity  # Importance/Value (1-10 or 1-100)
        self.treatment_time = treatment_time  # Cost/Weight (minutes)

    def __repr__(self):
        return f"Patient({self.name}, Sev={self.severity}, Time={self.treatment_time})"

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Condition": self.condition,
            "Severity": self.severity,
            "Treatment Time (steps)": self.treatment_time
        }

# Function to generate random patients
def generate_random_patients(num_patients, max_time):
    
    #(medical condition, min severity, max severity, min treatment time, max treatment time)
    conditions = [
        ("Cardiac Arrest", 90, 100, 30, 60), 
        ("Severe Bleeding", 70, 90, 20, 45),
        ("Broken Bone", 40, 60, 30, 90),
        ("Mild Fever", 10, 30, 5, 15),
        ("Allergic Reaction", 50, 80, 15, 30),
        ("Stroke Criteria", 85, 95, 40, 70),
        ("Abdominal Pain", 30, 60, 20, 45)
    ]
    names = ["Ahmed", "Mostafa", "Yasmine", "Abd Elhamed", "soly", "Caroline", "Mazen", "jennie", "Khadija", "Mohamed", "Khalid"]
    
    patients = []
    for i in range(num_patients):
        cond_name, min_sev, max_sev, min_time, max_time_cond = random.choice(conditions)
        
        # Ensure treatment time doesn't exceed max_time constraint
        if max_time is not None:
            max_time_cond = min(max_time_cond, max_time)
            min_time = min(min_time, max_time)
        
        #generates a random name, choice of condition, severity and treatment time
        p = Patient(
            id=i+1,
            name=random.choice(names),
            condition=cond_name,
            severity=random.randint(min_sev, max_sev),
            treatment_time=random.randint(min_time, max_time_cond)
        )
        patients.append(p)
    return patients

def solve_triage_dp(patients, max_time, max_beds=None):
    patients = sorted(patients, key=lambda p: p.treatment_time)
    n = len(patients)
    
    # Time-Based DP: Rows = Patients, Columns = Time Steps
    dp = [[0] * (max_time + 1) for _ in range(n + 1)] #
    
    for i in range(1, n + 1):  # For each patient
        score = patients[i-1].severity # Value of patient i
        time_steps = patients[i-1].treatment_time # Weight of patient i
        
        for t in range(0, max_time + 1):  # For each time step
            dp[i][t] = dp[i-1][t] #take the previous data as default (not including patient i)
            
            # Makes sures that the patient time is within the time limit
            if t >= time_steps: 
                # Recurrence: Max(the previous patient, updated patient + optimal score of remaining time)
                dp[i][t] = max(dp[i][t], score + dp[i-1][t - time_steps])
    
    # Backtrack time-based solution
    selected_time, remain = [], max_time
    for i in range(n, 0, -1):
        if dp[i][remain] != dp[i-1][remain]:        #it checks if the value is different from the previous row
            selected_time.append(patients[i-1])     #if different, it means the patient was included
            remain -= patients[i-1].treatment_time  #reduce the remaining time
    selected_time.reverse()                         #reverses the selected patients list to maintain original order
    
    # Bed limit in time-based solution
    if max_beds and len(selected_time) > max_beds:
        selected_time.sort(key=lambda p: p.severity, reverse=True)
        selected_time = selected_time[:max_beds]
    
    # Bed-based DP: Similar structure for beds
    dp_beds, selected_beds, bed_headers = None, [], None
    if max_beds:
        dp_beds = [[0] * (n + 1) for _ in range(max_beds + 1)] # Rows = Beds, Columns = Patients
        
        for b in range(1, max_beds + 1):  # loops For each bed capacity
            for i in range(1, n + 1):  # loops For each patient
                vi = patients[i-1].severity      # value of patient i
                
                dp_beds[b][i] = dp_beds[b][i-1]  # take the previous data as default (not including patient i)
                
                if b >= 1:  # Can we include patient i (need 1 bed)?
                    val = dp_beds[b-1][i-1] + vi # Include patient i (we take the maximum between the patients in the upper row or the diagonal + current patient value)
                    if val > dp_beds[b][i]:      # If the value is greater than the existing one, update it 
                        dp_beds[b][i] = val      # Update DP table
        
        # Backtrack bed-based solution
        remaining_beds = max_beds
        for i in range(n, 0, -1):
            if dp_beds[remaining_beds][i] != dp_beds[remaining_beds][i-1]:  #it checks if the value is different from the previous row
                selected_beds.append(patients[i-1])         #if different, it means the patient was included
                remaining_beds -= 1                                 #reduce the remaining beds
        selected_beds.reverse()                             #reverses the selected patients list to maintain original order
        bed_headers = [f"B={b}" for b in range(max_beds + 1)] #shows the beds titles in the table
    
    # Transpose bed-based DP for display (rows=patients, cols=beds)
    dp_beds_transposed = None
    if dp_beds:
        dp_beds_transposed = [[dp_beds[b][i] for b in range(max_beds + 1)] for i in range(n + 1)]
    
    return {
        "max_severity_time": dp[n][max_time], #return max severity for time-based
        "selected_patients_time": selected_time, #returns the patients selected for time-based
        "max_severity_beds": dp_beds[max_beds][n] if dp_beds else None, #return max severity for bed-based
        "selected_patients_beds": selected_beds, #returns the patients selected for bed-based
        "dp_table_raw": dp, 
        "dp_table_headers": [f"T={t}" for t in range(max_time + 1)], 
        "dp_table_rows": ["Initial (0)"] + [f"{p.name} ({p.treatment_time}m, {p.severity}s)" for p in patients], 
        "dp_beds_raw": dp_beds_transposed,
        "dp_beds_headers": bed_headers
    }

# Page Config
st.set_page_config(page_title="ER Triage Optimization", layout="wide")

# Creating a list to add the patients in it
if 'patients' not in st.session_state:
    st.session_state.patients = []

st.title("Emergency Room Optimization")

# Sidebar
st.sidebar.header("Constraint Settings")
#slider to select the maximum time available
max_time = st.sidebar.number_input(
    "Available Time (Step)", 
    min_value=10, 
    # max_value=300, 
    value=60, 
    step=10,
    help="Total time available for the doctor in this shift."
)
#slider to select the number of beds available
max_beds = st.sidebar.number_input(
    "Available Beds",
    min_value=1,
    max_value=20,
    value=6,
    step=1,
    help="Maximum number of patients that can be treated (bed capacity)."
)

# Patient Management Section
add_patient, waiting_room = st.columns([1, 2])

# Add Patient Section
with add_patient:
    st.subheader("Add Patient")
    with st.form("add_patient_form"):
        #Allow user to input patient details
        p_name = st.text_input("Name", value="")
        p_cond = st.text_input("Condition", value="")
        p_sev = st.slider("Severity (Value)", 1, 100, 50, help="Medical Urgency Score")
        p_time = st.number_input("Time of treatment (Weight)", 1, 120, 20, help="Time required for treatment")
        
        #checks if the add patient button is clicked
        if st.form_submit_button("Add Patient"):
            new_id = len(st.session_state.patients) + 1  #It will increment the id
            new_p = Patient(new_id, p_name, p_cond, p_sev, p_time) #creates a new patient object
            st.session_state.patients.append(new_p) #adds the new patient to the session state list
            st.success(f"Added {p_name}")

    st.divider() 
    if st.button("Generate Random Patients"):
        st.session_state.patients = generate_random_patients(7, max_time) #calls the function to generate 7 random patients
        st.success("Generated 7 random patients.")
    
    if st.button("Clear All Patients"):
        st.session_state.patients = []  #clears the patient list
        st.rerun()

with waiting_room:
    st.subheader("Waiting Room (Current Patients)")
    if st.session_state.patients:
        patient_data = [p.to_dict() for p in st.session_state.patients] #converts patient objects to dictionaries for display
        df_patients = pd.DataFrame(patient_data)                        #creates a table from the list of dictionaries
        st.dataframe(df_patients, use_container_width=True)
    else:
        st.info("No patients in the waiting room. Add some or generate random ones.")

# Optimization Section
st.divider()
st.header("Triage Decision Support")

if st.button("Run Triage Algorithm", type="primary"):
    if not st.session_state.patients:
        st.error("Please add patients first.")
    else:
        # Run Solver
        result = solve_triage_dp(st.session_state.patients, max_time, max_beds)
        selected_time = result["selected_patients_time"]
        selected_beds = result["selected_patients_beds"]
        max_sev_time = result["max_severity_time"]
        max_sev_beds = result["max_severity_beds"]
        
        # Display Solutions in Two Columns
        st.subheader("Optimized Treatment Plans")
        
        Time_based, Bed_based = st.columns(2)
        
        with Time_based:
            with st.container(border=True):
                st.markdown("#### Time-Based Optimization")
                st.caption("Optimized for maximum severity within time constraint")
                
                # Metrics for time-based selected patients
                selected_patients, total_severity = st.columns(2)
                selected_patients.metric("Selected Patients", len(selected_time))
                total_severity.metric("Total Severity", max_sev_time)
                
                total_time_used = sum(p.treatment_time for p in selected_time)
                Time_used, Beds_used = st.columns(2)
                Time_used.metric("Time Used", f"{total_time_used}/{max_time} steps")
                Beds_used.metric("Beds Used", f"{len(selected_time)}")
                
                # Display selected patients table
                if selected_time:
                    sel_data_time = [p.to_dict() for p in selected_time]
                    st.dataframe(pd.DataFrame(sel_data_time), use_container_width=True, height=300)
                else:
                    st.warning("No patients selected.")
        
        with Bed_based:
            with st.container(border=True):
                st.markdown("#### Bed-Based Optimization")
                st.caption("Optimized for maximum severity within bed constraint")
                
                # Metrics for bed-based selected patients
                bm1, bm2 = st.columns(2)
                bm1.metric("Selected Patients", len(selected_beds))
                bm2.metric("Total Severity", max_sev_beds if max_sev_beds else 0)
                
                total_time_beds = sum(p.treatment_time for p in selected_beds)
                TimeUsed, bedsUsed = st.columns(2)
                TimeUsed.metric("Time Used", f"{total_time_beds} mins")
                bedsUsed.metric("Beds Used", f"{len(selected_beds)}/{max_beds}")
                
                # Display selected patients table
                if selected_beds:
                    sel_data_beds = [p.to_dict() for p in selected_beds]
                    st.dataframe(pd.DataFrame(sel_data_beds), use_container_width=True, height=300)
                else:
                    st.warning("No patients selected.")

        # DP Table Visualization
        st.subheader("DP Table Visualizations")
        
        # Create two columns for the two tables
        Time_constraint_DP, Bed_constraint_DP = st.tabs(["Time-Based DP Table", "Bed-Based DP Table"])
        
        with Time_constraint_DP:
            with st.expander("Show Time Constraint DP Table", expanded=True):
                st.write("**Rows**: Patients considered (cumulative). **Columns**: Time capacity (0 to Max Time). **Cell value**: Max Severity.")
                
                # Format DP Table
                dp_raw = result["dp_table_raw"]
                headers = result["dp_table_headers"]
                row_idx = result["dp_table_rows"]
                
                
                if max_time > 30: 
                    
                    step = max(1, max_time // 25)
                    selected_indices = list(range(0, max_time + 1, step))
                    if max_time not in selected_indices:
                        selected_indices.append(max_time)
                    
                    st.caption(f"Showing sampled time slots (every {step} mins) for readability. Full range: 0-{max_time}")
                    sliced_dp = [[row[i] for i in selected_indices] for row in dp_raw]
                    sliced_headers = [headers[i] for i in selected_indices]
                else:
                    sliced_dp = dp_raw
                    sliced_headers = headers
                
                df_dp = pd.DataFrame(sliced_dp, columns=sliced_headers, index=row_idx)
                st.dataframe(df_dp.style.background_gradient(axis=None, cmap="Blues"), use_container_width=True)
        
        with Bed_constraint_DP:
            with st.expander("Show Bed Constraint DP Table", expanded=True):
                st.write("**Rows**: Patients considered (cumulative). **Columns**: Number of beds (0 to Max Beds). **Cell value**: Max Severity.")
                
                dp_beds_raw = result["dp_beds_raw"]
                bed_headers = result["dp_beds_headers"]
                
                if dp_beds_raw is not None:
                    df_dp_beds = pd.DataFrame(dp_beds_raw, columns=bed_headers, index=row_idx)
                    st.dataframe(df_dp_beds.style.background_gradient(axis=None, cmap="Greens"), use_container_width=True)
                else:
                    st.info("Bed constraint DP table not available (no bed limit specified).")
