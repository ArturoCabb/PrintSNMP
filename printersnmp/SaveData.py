from datetime import datetime

def saveFile(value):
    date = datetime.today().strftime('%Y-%m-%d')
    dateComplete = datetime.today().strftime('%Y-%m-%d %H:%M:%S %f %p')
    file = open(date + ".txt" ,"a+")
    file.write(dateComplete + ' > ' + value)
    file.close
    