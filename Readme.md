## Web Printer
#### Make printers without Ethernet or Wifi connection available on LAN.

If a printer does not have any Ethernet or Wifi connection it's not possible to print directly from other machine in the local network. This flask app creates a webeserver that can accepts and prints documents. The webserver is accessible from any machine on the LAN, thus document can be printed on the isolated printer directly from any machine on the LAN.

### 🛠️ Setting up:
1. Clone this repo in a computer where the printer is locally connected via USB.
2. Check the full name of the printer with `lpstat -p -d` and modify `web_printer.py` file with the name. 
3. Install flask and run the server with `python web_printer.py` or using gunicorn with `gunicorn -w 4 'web_printer:app' -b '0.0.0.0:8080'`
4. Go to the IP address of the host machine with port `8080` (or whatever you provided), the webserver should be available there. For example, if the machine IP is `192.168.31.111`, then the webserver is accessible at `http://192.168.31.111:8080/`. You can submit print jobs using this web-page.
