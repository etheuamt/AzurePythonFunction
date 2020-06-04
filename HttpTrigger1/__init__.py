import logging
import azure.functions as func
import pyodbc as pyodbc

def main(req: func.HttpRequest) -> func.HttpResponse:
    logger = logging.getLogger(__name__)
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    logger.info('Hello, World! Now connecting to an Azure SQL DB')

    server = 'xxxxx' 
    database = 'xxxxx'
    username = 'xxxxx'
    password = 'xxxxx'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    logger.info('Connected to Azure SQL DB')

    cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
    row = cursor.fetchone()
    while row:
        print (str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
