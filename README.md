# Emergency_Room_Triage_Optimizatio

## Project Overview

This project implements a **Dynamic Programming (DP)** solution to optimize **Emergency Room (ER) Patient Triage** under resource constraints, formulated as a **0/1 Knapsack Problem**.

### The Problem

Emergency Departments (EDs) often experience overcrowding due to limited bed availability and varying patient urgency, severity, and treatment duration, leading to increased waiting times and delayed care. This project formulates the ER bed allocation challenge as an optimization problem and applies a Dynamic Programming approach to allocate beds efficiently based on patient priority and resource constraints, aiming to improve patient outcomes and operational efficiency.

### Formal Problem Definition

**The ER bed allocation problem is formally defined as follows:**

**Input:**

- A set of N patients arriving at the ER
- A fixed number of available beds B
- For each patient i:
  - Severity score sᵢ, representing the medical urgency
  - Required treatment time tᵢ

**Output:**
- The maximum total severity score achievable
- The subset of patients selected for bed assignment

**Constraints:**
- Each patient can either be assigned a bed or not
- The number of selected patients must not exceed the available beds
- The total treatment time must not exceed the available time

**Objective:**

To maximize the sum of severity scores of the selected patients while respecting ER resource constraints.
This formulation closely resembles the classical 0/1 Knapsack optimization problem, where patients are items, beds are capacity, and severity represents value.

### Why Dynamic Programming?

Dynamic Programming provides a robust alternative by exploiting the problem’s optimal substructure and overlapping subproblems. Formulating ER bed allocation as a 0/1 Knapsack problem allows optimal patient selection, ensuring maximal total severity benefit.

## Key Features

### Algorithm Capabilities

- **Provably Optimal Solutions**: Guaranteed maximum severity within constraints
- **Dual-Constraint Modeling**: Simultaneously considers time and bed limitations
- **Backtracking**: Exact reconstruction of which patients to treat

### Interactive Application

- **Streamlit-Based GUI**: Web-based interface for real-time interaction
- **Dual Visualization**: Side-by-side comparison of time vs bed optimization
- **DP Table Heatmaps**: Color-coded visualization showing optimization progression
- **Patient Management**: Manual entry or random generation with realistic medical conditions

## Algorithm Details

### Dynamic Programming Formulation

**Time-Based Knapsack:**

State: Let $DP[i][t]$ denote the maximum total severity achievable by considering the first i patients within t available time units

•	For each patient, the algorithm decides whether to skip treatment or to treat the patient if sufficient time is available. The DP recurrence is defined as:

$$
DP[i][t] = \max \begin{cases}
DP[i-1][t] & \text{(skip patient } i\text{)} \\
s_i + DP[i-1][t - t_i] & \text{(treat patient } i\text{)}
\end{cases}
$$

•	The table is initialized with DP[0][t]=0 and DP[i][0]=0. The optimal solution is obtained from DP[n][T], and the selected patients are identified through backtracking.

<img width="925" height="81" alt="image" src="https://github.com/user-attachments/assets/e5a447cb-e24e-4c2f-8e73-ceab6cb191d0" />

------------------------------------------------------------------------

**Bed-Based Knapsack:**

State: Let $DP[i][b]$ denote the maximum total severity achievable by considering the first i patients using at most b available beds.

•	For each patient, two decisions are possible: either the patient is skipped or assigned a bed, provided that at least one bed is available. The DP recurrence is defined as:

$$
DP_{bed}[b][i] = \max \begin{cases}
DP_{bed}[b][i-1] & \text{(skip patient } i\text{)} \\
s_i + DP_{bed}[b-1][i-1] & \text{(treat patient } i\text{)}
\end{cases}
$$

•	The table is initialized with DP[0][b]=0 and DP[i][0]=0. The optimal solution is obtained from DP[n][B]. The selected patients are identified through backtracking, where a change in DP value indicates that a patient was assigned a bed.

<img width="868" height="79" alt="image" src="https://github.com/user-attachments/assets/db53584a-360a-4912-9def-5d8190c501b4" />


### Complexity Analysis

| Metric               | Time-Based              | Bed-Based       |
| -------------------- | ----------------------- | --------------- |
| **Time Complexity**  | $O(n \times T)$         | $O(B \times n)$ |
| **Space Complexity** | $O(n \times T)$         | $O(B \times n)$ |
| **Preprocessing**    | $O(n \log n)$ (sorting) |$O(n \log n)$ (sorting)            |

### Overall Complexity
**Time**: $O(nT + nB)$  
**Space**: $O(nT + nB)$  

## Usage Guide

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

   ```bash
   pip install streamlit pandas numpy
   ```
## Running the Application

   ```bash
   streamlit run app.py
   ```

  The application will automatically open in your browser at `http://localhost:8501`

### Step-by-Step Instructions

1. **Set Constraints** (left Sidebar):

   - Available Time: physician shift duration (default: 60 min)
   - Available Beds: ER capacity (default: 6 beds)

2. **Add Patients**:

   - **Quick**: Click "Generate Random Patients" for sample data
   - **Manual**: Enter name, condition, severity (1-100), and treatment time

3. **Run Optimization**:

   - Click "Run Triage Algorithm"
   - View two solutions:
     - **Time-Based**: Optimal within time constraint
     - **Bed-Based**: Optimal within bed constraint
       
4. **Interpret Results**:
   - Selected patients list
   - Total severity score (higher = better)
   - Resource utilization metrics
   - DP table visualization
     
5. **Download Results**:
   - You can download the DP tables and the selected patients table as csv files from the download icon above each table


### Team Members

| Name               | 
| -------------------- |
| Caroline Ehab  | 
| Khadija Ali | 
| Mohamed Mostafa    |
| Khalid Mohamed   |

