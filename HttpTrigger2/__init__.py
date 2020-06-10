import logging
import azure.functions as func
import pyodbc as pyodbc

def main(req: func.HttpRequest) -> func.HttpResponse:
    logger = logging.getLogger(__name__)
    logging.info('Python HTTP trigger function processed a request.')

    logger.info('Hello, World! Now connecting to an Azure SQL DB')

    server = 'v-eltheusqldb.database.windows.net' 
    database = 'v-eltheusqldb'
    username = 'v-eltheu'
    password = 'ABcd1234'
    driver= '{ODBC Driver 17 for SQL Server}'

    logger.info('Connected to Azure SQL DB')

    try:
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
    except Exception as e:
        logger.info("Exception occured: " + e)
    else:
        cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
        row = cursor.fetchone()
        while row:
            logger.info(str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()

    return func.HttpResponse("ok")
