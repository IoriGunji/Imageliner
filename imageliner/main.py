import image_liner
import sys
import re
import configparser
import tkinter as tk
import tkinter.messagebox as mb
from tkinterdnd2 import DND_FILES, TkinterDnD


def main():
    config = read_config()
    gui(config)


# GUI ウィンドウ
def gui(config):
    # ウィンドウ設定
    root = TkinterDnD.Tk()
    root.title('ImageLiner')
    root.geometry('330x100')
    default_color = root.cget("bg")

    # 変数宣言
    color = tk.StringVar()
    color.set(config['color'])
    size = tk.StringVar()
    size.set(config['size'])

    # ボーダー設定
    border_frame = tk.Frame(root, height=80, width=150, pady=10, padx=10, relief=tk.SOLID, bg=default_color, bd=1)
    border_frame.place(x=10, y=10)

    border_color_label = tk.Label(border_frame, text='Color：')
    border_color_label.place(x=0, y=10)
    border_color_input = tk.Entry(border_frame, textvariable=color, readonlybackground='white', justify=tk.CENTER)
    border_color_input.configure(validate='key', vcmd=(border_color_input.register(pre_validation_color), '%s', '%P'))
    border_color_input.place(x=50, y=10, width=60, height=21)

    border_size_label = tk.Label(border_frame, text='Size  ：')
    border_size_label.place(x=0, y=35)
    border_size_input = tk.Entry(border_frame, textvariable=size, readonlybackground='white', justify=tk.CENTER)
    border_size_input.configure(validate='key', vcmd=(border_size_input.register(pre_validation_size), '%s', '%P'))
    border_size_input.place(x=50, y=35, width=60, height=21)
    border_size_unit = tk.Label(border_frame, text='px')
    border_size_unit.place(x=110, y=35)

    # ドロップエリア
    drop_frame = tk.Frame(root, height=80, width=150, pady=10, padx=10, relief=tk.SOLID, bg=default_color, bd=1)
    drop_frame.drop_target_register(DND_FILES)
    drop_frame.dnd_bind('<<Drop>>', lambda e: drop(e.data, color.get(), size.get()))
    drop_frame.place(x=170, y=10)

    drop_label = tk.Label(drop_frame, text='* Drop image file here')
    drop_label.place(x=65, y=30, anchor=tk.CENTER)

    # 各種タイトル
    border_label = tk.Label(root, text='Border settings')
    border_label.place(x=20, y=0)
    dorp_label = tk.Label(root, text='Drop files')
    dorp_label.place(x=180, y=0)

    # 閉じるボタンの制御
    root.protocol("WM_DELETE_WINDOW", lambda: exit(color.get(), size.get()))

    # GUI描画
    root.mainloop()


# 画像処理
def drop(files, color, size):
    try:
        validation_color(color)
        validation_size(size)
    except Exception as e:
        mb.showerror('Error', e)
        return

    files = dnd2_parse_files(files)
    color = '#' + color
    size = int(size)

    for file in files:
        for ext in image_liner.IMAGE_EXTS:
            if re.search(f'\.{ext}$', file):
                image_liner.image_edit(file, size, color)


# DnD2 ファイルパスの解析
def dnd2_parse_files(files_str):
    start = 0
    length = len(files_str)
    files = []
    while start < length:
        if files_str[start] == '{':
            end = files_str.find('}', start+1)
            file = files_str[start+1 : end]
            start = end + 2
        else:
            end = files_str.find(' ', start)
            if end < 0:
                file = files_str[start:]
                start = length
            else:
                file = files_str[start : end]
                start = end + 1
        files.append(file)
    return files


# 終了処理
def exit(color, size):
    try:
        validation_color(color)
        validation_size(size)
    except Exception as e:
        print(e)
        sys.exit()
    save_config(color, size)
    sys.exit()


# バリデーションチェック
def pre_validation_color(before_word, after_word):
    return (len(after_word) <= 6 or len(after_word) == 0)

def pre_validation_size(before_word, after_word):
    return ((after_word.isdecimal() or after_word == '') and (len(after_word) <= 4 or len(after_word) == 0))

def validation_color(color):
    if len(color) != 6:
        raise ValueError("Color code is not 6 digits!")
    if not re.match(r'^[0-9a-fA-F]{6}$', color):
        raise ValueError("Color code is invalid!")

def validation_size(size):
    if not size.isdecimal():
        raise ValueError("Size is not a number!")
    if int(size) <= 0:
        raise ValueError("Size is invalid!")


# 設定の読み込み
def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    default = config['DEFAULT']
    configs = {
        'color': default.get('color') if default.get('color') != None else ''
        , 'size': default.get('size') if default.get('size') != None else ''
    }
    return configs


# 設定の保存
def save_config(color, size):
    config = configparser.ConfigParser()
    config.set('DEFAULT', 'color', color)
    config.set('DEFAULT', 'size', size)
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    main()


# https://magicode.io/taraku3/articles/20c53c1f06cf4131b452271f214a73de
# https://teratail.com/questions/226925
