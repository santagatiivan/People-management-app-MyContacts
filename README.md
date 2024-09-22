# People Management App

**MyContacts** is a desktop application developed in Python and Tkinter, designed to manage a list of people with information such as name, surname, birthdate, and phone number. This app is distributed as a standalone executable, so there's no need to install Python or additional dependencies to use it.

## Features

- **Add a person**: Enter the name, surname, birthdate, and phone number, with age calculated automatically.
- **Edit a person**: Select a person from the list and modify their details.
- **Remove a person**: Delete a selected person from the list.
- **Save data**: Data is saved in a JSON file (`dist/app/data.json`), allowing it to be reloaded on subsequent launches.
- **Ease of use**: Simple and intuitive graphical interface.
- **Ready-to-use executable**: No Python installation required.

## Usage

1. **Download and run the executable**:

   You can find the executable in the `dist/` folder or downloadable directly from the repository. To run it, simply double-click on `MyContacts`.

2. **Saving and loading data**:

   The data for the people is automatically saved and loaded to/from `dist/app/data.json`, so changes are retained even after closing the app.

## Source Code

If you want to view or modify the source code of the app, you can find it in the `code/main.py` folder. Feel free to explore and modify it as needed.

## Contributing

If you would like to improve the application or report bugs, you can submit a **pull request** or open an **issue**. The source code is well organized in the `app/code` folder.
