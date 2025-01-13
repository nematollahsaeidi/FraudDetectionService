# App Fraud Detection

This project implements a web-based system for detecting potential fraudulent activities based on user transaction data. It combines multiple modules for data processing, user behavior analysis, and fuzzy inference simulation to determine anomalies or fraud risks.

---

## Features

### 1. Dynamic Fraud Analysis
- Simulates transaction-based scenarios using **fuzzy inference** to detect suspicious patterns.
- Leverages user-provided data, including transaction frequency, amount, and types, to compute metrics.

### 2. User Behavior Modeling
- Categorizes users into different profiles (e.g., retailer, business person, organization).
- Generates reports and behavioral thresholds for daily, weekly, and monthly activity.

### 3. Web-Based Interface
- Built using **Flask** to provide a seamless interface for data input and result visualization.
- Allows for multiple user states and interactions with customizable transaction parameters.

### 4. Data Simulation
- Generates synthetic transaction data to simulate user activities over specific time frames.
- Includes advanced metrics such as **input/output frequency**, amounts, and thresholds.

### 5. Integration with External Services
- Incorporates tools like **google drive** for file uploads/downloads.
- Supports configuration-based modularity for easier updates and extensions.

---

Note: Files of `fuzzy_inference_simulator` and `simulation` were implemented by others. These are not included in the repository.

---