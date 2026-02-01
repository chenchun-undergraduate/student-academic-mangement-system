# student-academic-mangement-system
A data-driven academic management system with automated record tracking and AI-ready design.
## Project Overview

This project presents a data-driven academic management system designed
to support student course planning and academic progress tracking.

The system integrates course structures, prerequisite logic, and
academic performance records into a unified backend architecture,
emphasizing data consistency and historical traceability.
## Motivation & Context

In many academic environments, course scheduling, grade management,
and prerequisite evaluation are handled by separate systems.
This fragmentation limits integrated analysis and data-driven decision-making.

This project addresses this limitation by centralizing academic records
and automatically tracking grade changes over time, providing a reliable
foundation for future analytics and applied AI systems.
## System Architecture

The system is organized into three clearly separated layers
to improve maintainability and support future AI integration.

- Frontend Layer  
  Implemented in `class_gpa_management_app.py`, this layer handles
  user interaction through a Tkinter-based GUI.
  It collects user input, triggers backend services, and updates
  the interface based on returned results.

- Backend Service Layer  
  Implemented in `backend_code.py`, this layer encapsulates all
  academic logic, including grade updates, GPA calculation,
  and prerequisite evaluation.
  It acts as a service layer between the frontend and the database.

- Database Access Layer  
  Implemented in `db_connection.py`, this layer manages database
  connections and isolates SQL access from application logic,
  ensuring clean separation of concerns.

## Data Design & Management

The database schema distinguishes between current academic state
and historical academic transitions.

Key design features include:

- Structured storage of course and grade records
- Automated logging of grade changes using database triggers
- Explicit modeling of prerequisite relationships

This design enables reliable historical analysis and supports
future data-driven or AI-assisted academic decision systems.
## Applied AI Readiness

Although this project does not yet integrate machine learning models,
it was intentionally designed with AI readiness in mind.

The system provides structured, time-stamped academic data and a clear
separation between data storage and application logic, making it suitable
for future extensions such as predictive analytics, recommendation systems,
or academic risk detection.
## Implementation Highlights

- Relational schema design with enforced data integrity
- Automated change tracking using database triggers
- Backend logic implemented in Python and SQL
- GUI designed for real-time data interaction

```text
student-academic-management-system/
├── README.md
├── database/
│   └── ClassGPAManagementSYSdb.sql
├── backend/
│   ├── db_connection.py
│   └── backend_code.py
└── frontend/
    └── class_gpa_management_app.py
```


## Future AI Integration Path

The backend service layer was intentionally designed to support
future AI-driven extensions without modifying the frontend logic.

Potential AI integrations include:

- Predictive GPA Modeling  
  Using historical grade records to predict academic performance
  and identify students at potential academic risk.

- Course Recommendation  
  Recommending optimal course selections based on prerequisite
  structures, grade history, and performance trends.

- Academic Risk Detection  
  Applying anomaly detection or classification models to identify
  unusual academic trajectories and provide early warnings.

These AI components can be integrated as additional backend services,
allowing the frontend to remain unchanged while enhancing
decision-support capabilities.

