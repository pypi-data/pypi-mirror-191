import os
import base64
import tkinter

import tkinter.messagebox
import tkinter.scrolledtext


root = tkinter.Tk()

root.title('Pyttyc 1.0')  #设置标题

# try:
#     with open('tempicon.ico', 'wb+') as tmp:
#         tmp.write(base64.b64decode(''))
#
#     root.iconbitmap('tempicon.ico')
# finally:
#     if os.path.exists('tempicon.ico'):
#         os.remove('tempicon.ico')

root.geometry('645x400')  #设置默认大小

root.resizable(False,False)#禁止更改大小

# 建设终端滚动文本框
TerminalText = tkinter.scrolledtext.ScrolledText(
    root,
    state='d',
    fg='white',
    bg='black',
    insertbackground='white',
    font=('consolas',13),
    selectforeground='black',
    selectbackground='white',
    takefocus=False
)

TerminalText.pack(fill=tkinter.BOTH, expand=tkinter.YES)
#设置滚动文框Tag
TerminalText.tag_config('red',foreground='red',selectforeground='#00ffff',selectbackground='#ffffff')
TerminalText.tag_config('green',foreground='green',selectforeground='#ff7eff',selectbackground='#ffffff')
TerminalText.tag_config('blue',foreground='blue',selectforeground='#ffff7e',selectbackground='#ffffff')
TerminalText.tag_config('cyan',foreground='cyan',selectforeground='red',selectbackground='#ffffff')

TerminalText['state'] = 'n' #将文本框状态设为默认"normal"

#插入初始内容
# TerminalText.insert('end',f'EasyTerminal {1.0} By {"zzz"}\n')
# TerminalText.insert('end',f'{os.getcwd()}\n','green')
# TerminalText.insert('end',f'$ ')


def callback(event):
    print(type(event))
    print(event.char, end='')
    # print('test',i)
    TerminalText.mark_set('insert', 'end-1c linestart')  # 移动光标到最后一行

    TerminalText.delete('end-1c linestart', 'end-1c lineend')

TerminalText.bind("<Key>", callback)
# TerminalText.focus_set()
# frame.pack()
# tkinter.messagebox.showinfo(title=None, message=None)


root.mainloop()