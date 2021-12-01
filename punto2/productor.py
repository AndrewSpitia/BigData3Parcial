
from kafka import KafkaProducer
import pandas as pd
import time

acciones = pd.read_csv('SPY_TICK_TRADE.csv')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

filas = acciones['PRICE'].count()
for i in range(filas):
    precio = str(acciones['PRICE'][i])
    producer.send('quickstart-events', bytes(precio,encoding='utf-8'))
    print(precio)
    time.sleep(1)

producer.flush()