import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # 為了使用提示文字功能
import winreg
import ctypes
import sys
import os  # 用於處理檔案路徑

# 註冊表路徑
EXPLORER_POLICIES_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
DISALLOW_RUN_KEY = EXPLORER_POLICIES_KEY + r"\DisallowRun"

# 檢查是否以系統管理員身份運行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 確保 DisallowRun 政策已啟用
def ensure_disallow_run_policy():
    try:
        # 開啟或建立 Explorer Policies 機碼
        explorer_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, EXPLORER_POLICIES_KEY)
        # 設置 DisallowRun 為 1 (啟用)
        winreg.SetValueEx(explorer_key, "DisallowRun", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(explorer_key)
        
        # 確保 DisallowRun 子機碼存在
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY)
    except Exception as e:
        messagebox.showerror("錯誤", f"無法設置 DisallowRun 政策：{str(e)}")
        sys.exit(1)

# 在主程式開始前檢查管理員權限後，加入這行
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

# 確保政策已啟用
ensure_disallow_run_policy()

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

# 檢查程式是否已在阻擋清單中
def is_app_in_blocklist(app_name):
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, winreg.KEY_READ)
        i = 0
        while True:
            try:
                _, value_data, _ = winreg.EnumValue(reg_key, i)
                if value_data.lower() == app_name.lower():  # 不區分大小寫比較
                    winreg.CloseKey(reg_key)
                    return True
                i += 1
            except OSError:
                break
        winreg.CloseKey(reg_key)
    except FileNotFoundError:
        pass
    return False

# 新增阻擋項目
def add_to_block_list():
    app_name = entry.get().strip()
    if not app_name:
        # 開啟檔案選擇對話框
        file_path = filedialog.askopenfilename(
            title="選擇要阻擋的應用程式",
            filetypes=[
                ("執行檔", "*.exe"),
                ("所有檔案", "*.*")
            ]
        )
        if file_path:
            # 只取得檔案名稱，不要完整路徑
            app_name = os.path.basename(file_path)
            entry.delete(0, tk.END)
            entry.insert(0, app_name)
        else:
            return

    # 檢查是否已存在於清單中
    if is_app_in_blocklist(app_name):
        messagebox.showwarning("警告", f"{app_name} 已經在阻擋清單中！")
        entry.delete(0, tk.END)
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
        # 清空輸入欄位
        entry.delete(0, tk.END)
        messagebox.showinfo("成功", f"已將 {app_name} 新增到阻擋清單！")
    except PermissionError:
        messagebox.showerror("錯誤", "無法新增項目，請以管理員身分運行程式！")

# 選擇檔案按鈕的回調函數
def browse_file():
    file_path = filedialog.askopenfilename(
        title="選擇要阻擋的應用程式",
        filetypes=[
            ("執行檔", "*.exe"),
            ("所有檔案", "*.*")
        ]
    )
    if file_path:
        app_name = os.path.basename(file_path)
        entry.delete(0, tk.END)
        entry.insert(0, app_name)

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

# 建立一個框架來容納輸入框和範例提示
entry_frame = tk.Frame(frame_top)
entry_frame.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(entry_frame, width=30)
entry.pack(side=tk.TOP)

example_label = tk.Label(entry_frame, text="範例: Steam.exe, obs64.exe", 
                        font=("新細明體", 8), fg="gray")
example_label.pack(side=tk.TOP)

browse_button = tk.Button(frame_top, text="瀏覽...", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=2)

add_button = tk.Button(frame_top, text="新增", command=add_to_block_list)
add_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(root, text="刪除選定項目", command=remove_from_block_list)
remove_button.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

update_listbox()

# 啟動主程式
root.mainloop()
