# Alfano to RaceRender Converter Desktop App

This windows desktop application converts Alfano data exported from the ADA mobile app (in ZIP format) into a CSV file that can be directly imported into RaceRender for video overlay.

## Description

The Alfano ADA app allows users to record and export data from their karting sessions. This data is typically exported as a ZIP archive containing various files. This application provides a user-friendly graphical interface to extract the relevant data and format it into a CSV file that RaceRender can understand and use for data overlays on your videos.

## Compatibility

Compatible with Alfano 6 and 7

## Features

* **Simple GUI:** Easy-to-use graphical interface for file selection and conversion.
* **File Selection Dialog:** Browse and select your Alfano ZIP files using a standard file dialog.
* **Output File Naming:** Allows user to specify the output CSV file name.
* **Standalone Executable:** No Python installation required. Simply download and run the application.

## Installation

1.  Download the `Alfano2RaceRender.exe` executable from the [Releases](https://github.com/gcuevaf/alfano2racerender/releases) page.
2.  Place the executable in a directory of your choice.
3.  Double-click the executable to launch the application.

## Usage

1.  Launch the `Alfano2RaceRender.exe` application.
2.  Select the Alfano version
3.  Click the "Start" button and choose your Alfano ZIP file using the file dialog.
4.  Enter the desired name and location for the output CSV file.
6.  The converted CSV file will be saved in the specified location.
7.  Import the generated CSV file into RaceRender.

## Notes

* This application assumes the Alfano ZIP file contains the standard data format exported by the ADA app.
* To include partials (sectors), the selected track must have partials.
* The exact column headers in the output CSV may need to be adjusted in RaceRender to match the data fields you want to display.
* Video and data will still have to be manually synced in RaceRender.
* This application is distributed as a standalone executable, so no Python installation is necessary.
* **Mac Version:** I can create a macOS version of this application. Please open an issue or leave a comment on the repository if you would like to see a macOS version.

## Contributing

Feel free to contribute to the underlying Python code, or report issues.

If you find this app useful, also consider contributing to my tire, fuel, and the occasional 'oops, I hit the wall' fund with the following link:

<a href="https://www.buymeacoffee.com/gcuevaf" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## License

This project is licensed under the MIT License.


