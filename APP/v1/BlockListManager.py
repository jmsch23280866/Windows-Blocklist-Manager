import tkinter as tk
from tkinter import messagebox
import winreg
import ctypes
import sys

# 註冊表路徑
DISALLOW_RUN_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"

# 檢查是否以系統管理員身份運行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 重新啟動程式以管理員身份運行
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit()

# 更新顯示阻擋清單
def update_listbox():
    listbox.delete(0, tk.END)
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, winreg.KEY_READ)
        i = 0
        while True:
            try:
                _, value_data, _ = winreg.EnumValue(reg_key, i)
                listbox.insert(tk.END, value_data)
                i += 1
            except OSError:
                break
        winreg.CloseKey(reg_key)
    except FileNotFoundError:
        pass

# 新增阻擋項目
def add_to_block_list():
    app_name = entry.get().strip()
    if not app_name:
        messagebox.showwarning("警告", "請輸入應用程式名稱！")
        return

    try:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY)
        i = 0
        while True:
            try:
                winreg.EnumValue(reg_key, i)
                i += 1
            except OSError:
                break
        winreg.SetValueEx(reg_key, str(i), 0, winreg.REG_SZ, app_name)
        winreg.CloseKey(reg_key)
        update_listbox()
        messagebox.showinfo("成功", f"已將 {app_name} 新增到阻擋清單！")
    except PermissionError:
        messagebox.showerror("錯誤", "無法新增項目，請以管理員身分運行程式！")

# 刪除阻擋項目
def remove_from_block_list():
    selected_item = listbox.curselection()
    if not selected_item:
        messagebox.showwarning("警告", "請先選擇要刪除的項目！")
        return

    app_name = listbox.get(selected_item)
    try:
        # 開啟註冊表項目
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, 
                                winreg.KEY_ALL_ACCESS)
        
        # 獲取所有值
        values = []
        i = 0
        while True:
            try:
                value_name, value_data, _ = winreg.EnumValue(reg_key, i)
                values.append((value_name, value_data))
                i += 1
            except OSError:
                break
        
        # 關閉目前的鍵值
        winreg.CloseKey(reg_key)
        
        # 重新開啟註冊表項目
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, 
                                winreg.KEY_ALL_ACCESS)
        
        # 刪除所有現有值
        for value_name, _ in values:
            try:
                winreg.DeleteValue(reg_key, value_name)
            except WindowsError:
                pass
        
        # 重新寫入未被刪除的值
        new_index = 0
        for value_name, value_data in values:
            if value_data != app_name:
                winreg.SetValueEx(reg_key, str(new_index), 0, winreg.REG_SZ, value_data)
                new_index += 1
        
        winreg.CloseKey(reg_key)
        update_listbox()
        messagebox.showinfo("成功", f"已將 {app_name} 移出阻擋清單！")
        
    except FileNotFoundError:
        messagebox.showwarning("警告", "阻擋清單不存在！")
    except PermissionError:
        messagebox.showerror("錯誤", "無法刪除阻擋項目，請以管理員身分運行程式！")

# 初始化 GUI
root = tk.Tk()
root.title("阻擋清單管理工具")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

entry_label = tk.Label(frame_top, text="應用程式名稱：")
entry_label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(frame_top, width=30)
entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame_top, text="新增", command=add_to_block_list)
add_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(root, text="刪除選定項目", command=remove_from_block_list)
remove_button.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

update_listbox()

# 啟動主程式
root.mainloop()
