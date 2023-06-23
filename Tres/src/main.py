from fastapi import FastAPI,File,Form, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
app = FastAPI()

# Load the CSV data into a DataFrame
data = pd.read_csv('vacaciones 2023-03-01 18 05 03.790332.csv', encoding="UTF8")

# Endpoint for downloading the CSV file
@app.get('/ejercicio/descarga/')
async def download_csv(format: str = Query(..., description='Response format (csv or json)')):
    if format == 'csv':
        # Save the DataFrame as a CSV file
        filename = 'downloaded_file.csv'
        data.to_csv(filename, index=False)
        return FileResponse(filename, media_type='text/csv', filename='downloaded_file.csv')

    elif format == 'json':
        # Convert the DataFrame to a JSON object
        json_data = data.to_json(orient='records')
        return json_data

    # Invalid format
    raise HTTPException(status_code=400, detail='Invalid format specified.')

@app.post("/ejercicio/descarga/")
async def download_data(format: str = Form(...)):
    # Read the CSV file and store it as a DataFrame
    try:
        data = pd.read_csv('vacaciones 2023-03-01 18 05 03.790332.csv', encoding="UTF8")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to read CSV file")

    if format.lower() == "csv":
        # Save the DataFrame as a CSV file
        csv_file_path = "downloaded_file.csv"
        data.to_csv(csv_file_path, index=False)

        # Return the CSV file for download
        return FileResponse(csv_file_path, filename="data.csv")
    elif format.lower() == "json":
        # Convert the DataFrame to JSON format
        json_data = data.to_json(orient="records")

        # Return the JSON data as a response
        return JSONResponse(content=json_data, media_type="application/json")
    else:
        raise HTTPException(status_code=400, detail="Invalid format specified")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)