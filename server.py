from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import requests
import datetime

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        s = requests.Session()
        date = datetime.datetime.today().strftime('%d.%m.%Y')

        payload = {'query': '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"'+date+'","viewTypeEntityId":"193","channels":[624,642,628,646,644,649,645,622,630,626,629,623,650,643]}'}
        r = s.post('http://80.53.180.198/dane-pomiarowe/pobierz', data=payload)
        air = r.json()

        nazwa = air['data']['title']
		#select keys needed
        for serie in air['data']['series']:
			
            if(serie['label'] == 'Benzen'):
                for data in serie['data']:
                    benzen = data[1]+serie['unit']

            if(serie['label'] == 'Ci\u015bnienie atmosferyczne'):
                for data in serie['data']:
                    cisnienie = data[1]+serie['unit']
					
            if(serie['label'] == 'Dwutlenek azotu'):
                for data in serie['data']:
                    no2 = data[1]+serie['unit']
					
            if(serie['label'] == 'Etylobenzen'):
                for data in serie['data']:
                    etylobenzen = data[1]+serie['unit']
					
            if(serie['label'] == 'Kierunek wiatru'):
                for data in serie['data']:
                    kierwiatr = data[1]+serie['unit']
					
            if(serie['label'] == 'M-P-Ksylen'):
                for data in serie['data']:
                    mpksylen = data[1]+serie['unit']
					
            if(serie['label'] == 'Pr\u0119dko\u015b\u0107 wiatru'):
                for data in serie['data']:
                    predkoscwiatru = data[1]+serie['unit']
					
            if(serie['label'] == 'Py\u0142 zawieszony PM10'):
                for data in serie['data']:
                    pm10 = data[1]+serie['unit']
					
            if(serie['label'] == 'Py\u0142 zawieszony PM2.5'):
                for data in serie['data']:
                    pm25 = data[1]+serie['unit']
					
            if(serie['label'] == 'Temperatura'):
                for data in serie['data']:
                    temperatura = data[1]+serie['unit']
					
            if(serie['label'] == 'Tlenek azotu'):
                for data in serie['data']:
                    no = data[1]+serie['unit']
					
            if(serie['label'] == 'Tlenki azotu'):
                for data in serie['data']:
                    tlenkiazotu = data[1]+serie['unit']
					
            if(serie['label'] == 'Toluen'):
                for data in serie['data']:
                    toluen = data[1]+serie['unit']
					
            if(serie['label'] == 'Wilgotno\u015b\u0107 wzgl\u0119dna'):
                for data in serie['data']:
                    wilgotnoscwzgledna = data[1]+serie['unit']
				
        self._set_headers()
        self.wfile.write(json.dumps({'data':{'nazwa': nazwa, 'benzen': benzen, 'cisnienie': cisnienie, 'no2': no2, 'etylobenzen': etylobenzen, 'kierwiatr': kierwiatr,
        'mpksylen': mpksylen, 'predkoscwiatru': predkoscwiatru, 'pm10': pm10, 'pm25': pm25, 'temperatura': temperatura, 'no': no, 'tlenkiazotu': tlenkiazotu, 'wilgotnoscwzgledna': wilgotnoscwzgledna}}).encode('utf8'))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8009):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print('Starting httpd on port %d...', port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        
