# Codecodix AI Lab

## Overview
The Codecodix AI Lab is a workspace designed for developing and managing various dashboards and functionalities for the BCS platform. It includes multiple Python scripts and resources to support different user roles and functionalities.

## Project Structure

```
Codecodix_AI_Lab/
├── admin_dashboard.py         # Admin dashboard functionalities
├── app.py                     # Main application entry point
├── background.jpg             # Background image resource
├── background1.jpg            # Alternative background image resource
├── BCSplatform.py             # Core platform functionalities
├── clients_dashboard.py       # Dashboard for clients
├── company_dashboard.py       # Dashboard for companies
├── guest_dashboard.py         # Dashboard for guests
├── landing.py                 # Landing page functionalities
├── platform.db                # Database file
├── promoter_dashboard.py      # Dashboard for promoters
├── starter_dashboard.py       # Dashboard for starters
├── __pycache__/               # Compiled Python files
└── ¿Qué es BCS AI.pdf         # Documentation in PDF format
```

## Key Files

- **`app.py`**: The main entry point of the application.
- **`BCSplatform.py`**: Contains core functionalities for the BCS platform.
- **Dashboards**: Separate Python scripts for different user roles:
  - `admin_dashboard.py`
  - `clients_dashboard.py`
  - `company_dashboard.py`
  - `guest_dashboard.py`
  - `promoter_dashboard.py`
  - `starter_dashboard.py`
- **Resources**:
  - `background.jpg` and `background1.jpg`: Background images used in the application.
  - `platform.db`: SQLite database file.
  - `¿Qué es BCS AI.pdf`: Documentation about the BCS AI platform.

## How to Run

1. Ensure you have Python installed on your system.
2. Navigate to the project directory.
3. Run the application using the following command:

   ```bash
   python app.py
   ```

## Dependencies

Make sure to install the required dependencies before running the application. You can use `pip` to install them:

```bash
pip install -r requirements.txt
```

*(Note: Add a `requirements.txt` file if not already present.)*

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. Ensure your code follows best practices and is well-documented.

## License

This project is licensed under the MIT License. See the LICENSE file for details.