import pandas as pd

### Instalo e importo las librerias que necesito poniendo: !pip install python-binance mplfinance
### (mplfinance requiere de Pandas y Matplotlib)
from binance import Client

### Necesito 2 keys para usar la API de Binance, para esto hago lo siguiente:
### Inicio sesion en Binance
### Creo una API en 'Gestion de API' sobre el logo de perfil en el inicio de Binance.
### Al momento de crear la API es IMPORTANTE ir a 'Editar restricciones' y habilitar solo para lectura
### asi como tambien restringir el acceso solo para direcciones de IP confiables. Ahi pongo mi IP.
### Inserto las keys que genera Binance en variables.
api_key = 'Aca se inserta la api key, dejar comillas'
secret_key = 'aca la secreta'

### Autenticacion de cliente
client = Client(api_key,secret_key)

### Obtengo todos los tickers en la variable 'tickers'
tickers = client.get_all_tickers()

### Convierto a tickers en un DataFrame
ticker_df = pd.DataFrame(tickers)
#print(ticker_df.head())
#print(ticker_df.tail())

### Creo un indice basado en el ticker
ticker_df.set_index('symbol',inplace=True)
### Si quiero saber el precio actual del BTC o cualquier cripto uso 'loc' para localizar dicha moneda y su respectivo
### valor. Esto me devuelve el precio en formato de texto, entonces uso 'float' 
print("Actualmente el precio del BTC en USD es:",float(ticker_df.loc['BTCUSDT']['price']))

### Datos de oferta y demanda
btc_data = client.get_order_book(symbol='BTCUSDT')
### Si imprimo me devuelve el historial de precios y volumenes de bids y asks en formato dict
#print(btc_data)

### Creo una tabla de muestra con precios y volumenes de los bids
btc_bids = pd.DataFrame(btc_data['bids'])
btc_bids.columns=['Precio de compra','Volumen']
#print(btc_bids.head())

### Y otra para asks
btc_asks = pd.DataFrame(btc_data['asks'])
btc_asks.columns=['Precio de venta','Volumen']
#print(btc_asks.head())

### Concateno ambas para poder compararlas
btc_conc = pd.concat((btc_bids,btc_asks),axis=1)
#print(btc_conc)

### Traigo los datos historicos diarios desde 2017
datos_historicos = client.get_historical_klines('BTCUSDT',Client.KLINE_INTERVAL_1DAY,'1 Jan 2017')
datos_historicos_df = pd.DataFrame(datos_historicos)
#print(datos_historicos_df.head())
### Muestra la tabla pero sin identificatorio
### Entonces reemplazo esos valores por sus correspondientes nombres
datos_historicos_df.columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                    'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
#print(datos_historicos_df.head())
### Chequeo que tipos de datos son las series
#print(datos_historicos_df.dtypes)
### La mayoria son de tipo object o sea texto, por lo tanto tengo que cambiar a formato de fecha a 'Open Time' y a 'Close Time'
### Tambien tengo que cambiar el resto a datos numericos y asi poder hacer analisis.
### De object a datetime
datos_historicos_df['Open Time']=pd.to_datetime(datos_historicos_df['Open Time']/1000, unit='s')
datos_historicos_df['Close Time']=pd.to_datetime(datos_historicos_df['Close Time']/1000, unit='s')
### Ahora de object a float
columnas_numericas = ['Open','High','Low','Close','Volume','Quote Asset Volume','TB Base Volume','TB Quote Volume']
datos_historicos_df[columnas_numericas]=datos_historicos_df[columnas_numericas].apply(pd.to_numeric,axis=1)
#print(datos_historicos_df.dtypes)
#print(datos_historicos_df.info())

### Ahora que los datos estan limpios puedo usar describe para tener un panorama estadistico
print(datos_historicos_df.describe())

### Y hago ploteos con la libreria mplfinance
### Links para personalizar plots con mplfinance: https://medium.com/mlearning-ai/stock-market-data-visualization-using-mplfinance-1d35a8d48e4
### https://github.com/matplotlib/mplfinance

import mplfinance as mpf

mpf.plot(datos_historicos_df.set_index('Close Time').tail(150),type='candle',style='charles',volume=True,
         title='BTC/USDT últimos 150 dias',figratio=(20,12), mav=(10,20,30))

mpf.plot(datos_historicos_df.set_index('Close Time').tail(70),type='line',
         style='mike',title='Tuiteo Elon?',tight_layout=True)

ask = input('Compraste arriba de 50k?\n').lower()
if ask == 'si':
    print('Te comiste el FOMO, dura leccion')
elif ask == 'no':
    print('Bien, espera la oportunidad')
else:
    print('es una pregunta sencilla de si o no')