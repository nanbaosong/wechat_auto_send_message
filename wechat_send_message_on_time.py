from json.tool import main
import threading
import pyautogui
import pyperclip
import time
import json

input_box = "tools/inputbox.png"
send_pic = "tools/sendpic.png"
message_file = 'message.json'

def get_center_of_position(position):
    return [position[0] + position[2] / 2, position[1] + position[3] / 2]

def click_picture(picture):
    picture_pos = pyautogui.locateOnScreen(picture)
    picture_mid_position = get_center_of_position(picture_pos)
    pyautogui.click(picture_mid_position[0], picture_mid_position[1]) 

def click_contact_icon(contact_name):
    contact_icon = "contact/" + contact_name + ".png"
    click_picture(contact_icon)

def input_text(message):
    inputbox_position = pyautogui.locateOnScreen(input_box)
    real_inputbox_pos = [inputbox_position[0] + inputbox_position[2] / 2, inputbox_position[1] + inputbox_position[3] * 0.95]
    pyautogui.click(real_inputbox_pos[0], real_inputbox_pos[1])
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    
def input_picture(message):
    click_picture(send_pic)
    time.sleep(1)
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
    
