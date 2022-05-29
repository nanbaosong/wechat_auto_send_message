import threading
import pyautogui
import pyperclip
import time
import json

send_pic = "tools/sendpic.png"
message_file = 'message.json'


def click_picture(picture):
    picture_pos = pyautogui.locateOnScreen(picture, confidence=0.9)
    picture_mid_position = pyautogui.center(picture_pos)
    pyautogui.click(picture_mid_position[0], picture_mid_position[1]) 

def click_contact_icon(contact_name):
    contact_icon = "contact/" + contact_name + ".png"
    click_picture(contact_icon)

def input_text(message):
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    
def input_picture(message):
    click_picture(send_pic)
    time.sleep(2)
    click_picture("picture_icon/" + message + "_icon.png")
    pyautogui.press('enter')

def wechat_send_message(contact, message, isTest):
    click_contact_icon(contact)
    if isTest:
        input_text(message)
    else:
        input_picture(message)
    pyautogui.press('enter')

def wechat_send_message_on_time(contact, message, sendTime, isText):
    while True:
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if cur_time == sendTime:
            wechat_send_message(contact, message, isText)
            break
        
if __name__ == '__main__':
    with open(message_file, 'r+', encoding='utf-8') as mf:
        all_messages = json.load(mf)["allmessages"]
    work_thread = []
    for message in all_messages:
        if "text" in message:
            t = threading.Thread(target=wechat_send_message_on_time, args=(message["contact"], message["text"], message["sendtime"], True))
        elif "picture" in message:
            t = threading.Thread(target=wechat_send_message_on_time, args=(message["contact"], message["picture"], message["sendtime"], False))
        work_thread.append(t)
        t.start()
    for t in work_thread:
        t.join()