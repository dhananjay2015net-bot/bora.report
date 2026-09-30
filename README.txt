ENTRY ADMIN SYSTEM

1) Install Python 3 on the main computer.
2) Open Command Prompt in this folder.
3) Run: pip install -r requirements.txt
4) Run: python app.py
5) On the main computer open: http://127.0.0.1:5000
6) Other computers on the SAME Wi-Fi/LAN can open:
   http://MAIN-COMPUTER-IP:5000

To find the main computer IP on Windows:
   ipconfig
Look for IPv4 Address, e.g. 192.168.1.10

Admin login:
   ID: admin
   Password: admin123

IMPORTANT:
- Change app.secret_key in app.py before real use.
- Change the demo admin password before real/public use.
- This simple version is intended for a trusted local network.
- For Internet access from different locations, use a proper hosted server/database and HTTPS.
