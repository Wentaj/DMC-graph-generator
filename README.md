# Automatic DMC Graph Creator

Python app that allows users to create graphs from csv,xls/xlsx files.
## Features
-Upload datafile
-Pandas will automatically parses through data 
-Plotly Express will create graphs

## How it works

1. The user uploads a file with the upload box.
2. A callback decodes the uploaded file contents and loads the data into a pandas DataFrame, which follows the normal `dcc.Upload` callback in Dash.
3. The app stores the parsed rows and filename in `dcc.Store` components so later callbacks can rebuild the figure without re-uploading the file.
4. The app generates one button for each column name found in `df.columns`, so buttons appear only after a file exists.
5. Clicking a button selects that column for visualization, and the radio control chooses between ascending or descending order.

## Supported files

- CSV
- XLS / XLSX

## Run the app

```bash
pip install dash dash-mantine-components plotly pandas openpyxl
python app.py
```
