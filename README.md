Project Name: py_supabase_rest
Description:
This project is a FastAPI-based RESTful API service designed to handle PLC
(Programmable Logic Controller) data storage, retrieval, and visualization.
It integrates with Supabase for backend data storage and provides both static
and interactive chart rendering.

---
Key Features:
1. PLC data retrieval from Supabase.
2. Generate static and interactive 2D/3D charts for Voltage and Current data.
3. Multi-device support with time-based querying.
4. Modular structure for maintainability and scalability.

---
Installation:

1. Clone the repository:
   git clone https://github.com/charleswhitesun/py_supabase_rest.git

2. Navigate to project folder:
   cd py_supabase_rest

3. Create virtual environment and activate:
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows

4. Install dependencies:
   pip install -r requirements.txt

---
Usage:

1. Run the API server:
   uvicorn py_supabase_rest.main:app --reload

2. Access Swagger UI:
   Open browser and go to http://127.0.0.1:8000/docs

3. Use the PLC chart endpoints:
   GET /plc-chart/device-line_drawing
   GET /plc-chart/device-line_drawing_3d

---
API Endpoints:

/plc-chart/device-line_drawing
   - Generate 2D line charts for PLC voltage or current data.
   - Supports static PNG or interactive HTML mode.

/plc-chart/device-line_drawing_3d
   - Generate 3D line charts for multiple PLC devices.
   - Interactive mode opens chart in default browser.

---
License:

This project is licensed under the Apache License 2.0.
