from motordecalidad.constants import *
from pyspark.sql import DataFrame


def send_email(registerAmount,rulesNumber,outputPath,data: DataFrame,receiver_email = "operacionestelefonicabi.hispam@outlook.com"):
    import smtplib
    from email.message import EmailMessage
    dataDict = str(data.collect())
    sslPort = 587  # For SSL
    smtp_server = "smtp-mail.outlook.com"
    sender_email = "enzo.ip.98@outlook.com.pe"
    password = "lpbrvukonxcucdvh"    
    message = EmailMessage()
    message["Subject"] = "Ejecucion de Motor de Calidad"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f"""\
    Hola,
    Su ejecucion del motor de calidad ha dado los siguientes resultados:
    Cantidad de Registros Evaluados: {registerAmount}
    Cantidad de Reglas Evaluadas: {rulesNumber}
    Error promedio por regla: {dataDict}
    Se pueden consultar los resultados en {outputPath} """
    message.set_content(text)
    smtp = smtplib.SMTP(smtp_server,port=sslPort)
    smtp.starttls()
    smtp.login(sender_email,password)
    smtp.sendmail(sender_email,receiver_email,message.as_string())
    smtp.quit()
#Function to define the dbutils library from Azure Databricks
def get_dbutils(spark):
        try:
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        except ImportError:
            import IPython
            dbutils = IPython.get_ipython().user_ns["dbutils"]
        return dbutils
def applyFilter(object:DataFrame, filtered) :
    try:
        filteredColumn = filtered.get(JsonParts.Fields)
        filterValue = filtered.get(JsonParts.Values)
        print("Extracción de parametros de filtrado finalizada")
        return object.filter(col(filteredColumn)==filterValue)
    except:
        print("Se omite filtro")
        return object