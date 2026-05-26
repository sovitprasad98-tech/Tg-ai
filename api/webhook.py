
from http.server import BaseHTTPRequestHandler
import sys, os, json, telebot

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import bot, setup_webhook


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
        # Pehli baar URL visit karo — webhook set ho jayega automatically
        setup_webhook()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Raju Bot is alive! Webhook set ho gaya!')
