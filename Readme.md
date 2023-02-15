## Web Printer
#### Make printers without Ethernet or Wifi connection available on LAN.

If a printer does not have any Ethernet or Wifi connection it's not possible to print directly from other machine in the local network. This flask app creates a webeserver that can accepts and prints documents. The webserver is accessible from any machine on the LAN, thus document can be printed on the isolated printer directly from any machine on the LAN.

### Usage:
1. Clone this repo.
2. Install flask and run the server where the printer is locally connected via USB.
4. Go to the IP address of the host machine. The webserver should be available there to submit print jobs.