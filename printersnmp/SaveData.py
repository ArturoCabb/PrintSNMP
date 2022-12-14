from datetime import datetime

def saveFile(value):
    date = datetime.today().strftime('%Y-%m-%d')
    file = open(date + ".txt" ,"a+")
    file.write(value)
    file.close
    