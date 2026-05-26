from http.server import BaseHTTPRequestHandler
import sys, os, telebot

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import bot, setup_webhook, startup_log

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body   = self.rfile.read(length).decode('utf-8')
        update = telebot.types.Update.de_json(body)
        bot.process_new_updates([update])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

    def do_GET(self):
        setup_webhook()
        startup_log()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Raju Bot is alive!')

    def log_message(self, format, *args):
        pass
