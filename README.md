# TableView Contact

This project is a desktop application built with PySide6 for managing contact data in a table view (TableView). Contact data is stored in a CSV file and can be viewed and edited through the application.

## Features
- Display the contact list in a table
- Add, delete, and edit contacts
- Save data to a CSV file

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd tableview.contact
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the application:
```bash
python app.py
```

## File Structure
- `app.py`: Main application file (UI and core logic)
- `csvdb.py`: Handles reading/writing data to the CSV file
- `contatcs.csv`: File where contact data is stored
- `requirements.txt`: List of dependencies
- `LICENCE`: License file

## Notes
- The application is developed with PySide6.
- Contact data is stored in the `contatcs.csv` file. If the file does not exist, it will be created on the first run.
- In this project, I learned how to use QModelView and QTableView.

## License
This project is licensed under the [License](./LICENCE). 