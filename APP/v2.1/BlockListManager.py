import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # 用於進階的 GUI 元件
import winreg  # 用於操作 Windows 註冊表
import ctypes  # 用於檢查管理員權限
import sys
import os
import locale  # 用於檢測系統語言

# 語言設定字典：包含中文和英文的所有介面文字
LANGUAGES = {
    'zh_TW': {
        # 中文介面文字設定
        'title': "阻擋清單管理工具",
        'app_name_label': "應用程式名稱：",
        'example_text': "範例: Steam.exe, obs64.exe",
        'browse_button': "🔍 瀏覽...",
        'add_button': "➕ 新增",
        'remove_button': "❌ 刪除選定項目",
        'change_language': "🌐 Change Language",
        'success_add': "已將 {} 新增到阻擋清單！",
        'success_remove': "已將 {} 移出阻擋清單！",
        'warning_exists': "{} 已經在阻擋清單中！",
        'warning_select': "請先選擇要刪除的項目！",
        'warning_blocklist': "阻擋清單不存在！",
        'error_admin': "無法新增項目，請以管理員身分運行程式！",
        'error_policy': "無法設置 DisallowRun 政策：{}",
        'file_dialog_title': "選擇要阻擋的應用程式",
        'file_types': [("執行檔", "*.exe"), ("所有檔案", "*.*")],
        'export_button': "💾 匯出設定",
        'export_success': "設定已匯出至：\n{}",
        'export_error': "匯出設定時發生錯誤：{}",
        'export_dialog_title': "選擇匯出位置",
        'export_file_types': [("登錄檔", "*.reg")],
        'export_default_name': "阻擋清單設定.reg"
    },
    'en_US': {
        # 英文介面文字設定
        'title': "Block List Manager",
        'app_name_label': "Application Name:",
        'example_text': "Example: Steam.exe, obs64.exe",
        'browse_button': "🔍 Browse...",
        'add_button': "➕ Add",
        'remove_button': "❌ Remove Selected",
        'change_language': "🌐 中文介面",
        'success_add': "{} has been added to block list!",
        'success_remove': "{} has been removed from block list!",
        'warning_exists': "{} is already in the block list!",
        'warning_select': "Please select an item to remove!",
        'warning_blocklist': "Block list does not exist!",
        'error_admin': "Cannot add item, please run as administrator!",
        'error_policy': "Cannot set DisallowRun policy: {}",
        'file_dialog_title': "Select Application to Block",
        'file_types': [("Executable", "*.exe"), ("All Files", "*.*")],
        'export_button': "💾 Export Settings",
        'export_success': "Settings exported to:\n{}",
        'export_error': "Error exporting settings: {}",
        'export_dialog_title': "Choose Export Location",
        'export_file_types': [("Registry File", "*.reg")],
        'export_default_name': "BlockListSettings.reg"
    }
}

# 註冊表路徑常數
EXPLORER_POLICIES_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
DISALLOW_RUN_KEY = EXPLORER_POLICIES_KEY + r"\DisallowRun"

# 檢測系統預設語言
def get_system_language():
    """
    檢測系統預設語言並返回對應的語言代碼
    返回值：'zh_TW' 或 'en_US'
    """
    try:
        # 使用 Windows API 獲取系統語言代碼
        import ctypes
        windll = ctypes.windll.kernel32
        LOCALE_SYSTEM_DEFAULT = 0x0800
        LOCALE_SISO639LANGNAME = 0x0059
        LOCALE_SISO3166CTRYNAME = 0x005A

        # 獲取語言代碼
        lang_buf = ctypes.create_unicode_buffer(9)
        country_buf = ctypes.create_unicode_buffer(9)
        
        windll.GetLocaleInfoW(LOCALE_SYSTEM_DEFAULT, LOCALE_SISO639LANGNAME, lang_buf, len(lang_buf))
        windll.GetLocaleInfoW(LOCALE_SYSTEM_DEFAULT, LOCALE_SISO3166CTRYNAME, country_buf, len(country_buf))
        
        # 組合語言和地區代碼
        system_locale = f"{lang_buf.value}_{country_buf.value}"
        
        # 檢查是否為繁體中文（台灣）
        if system_locale.lower() in ['zh_tw', 'zh_hk', 'zh_mo']:
            return 'zh_TW'
        return 'en_US'
    except:
        return 'en_US'  # 如果無法檢測則預設使用英文

# 檢查是否以系統管理員身份運行
def is_admin():
    """
    檢查當前程式是否以管理員權限運行
    返回值：True 表示是管理員權限，False 表示不是
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 確保 DisallowRun 政策已啟用
def ensure_disallow_run_policy():
    """
    確保 Windows 的 DisallowRun 政策已正確設置
    - 建立必要的註冊表項目
    - 設置 DisallowRun 為啟用狀態
    如果設置失敗會顯示錯誤訊息並結束程式
    """
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

class BlockListManager:
    """
    阻擋清單管理工具的主要類別
    處理 GUI 介面和阻擋清單的管理功能
    """
    def __init__(self):
        """
        初始化阻擋清單管理器
        - 設置初始語言
        - 初始化 GUI 介面
        """
        self.current_language = get_system_language()
        self.init_gui()

    def change_language(self):
        """
        切換介面語言（中英文互換）
        並更新所有介面文字
        """
        self.current_language = 'en_US' if self.current_language == 'zh_TW' else 'zh_TW'
        self.update_gui_text()

    def update_gui_text(self):
        """
        更新所有 GUI 元件的文字為當前選擇的語言
        """
        lang = LANGUAGES[self.current_language]
        self.root.title(lang['title'])
        self.entry_label.config(text=lang['app_name_label'])
        self.example_label.config(text=lang['example_text'])
        self.browse_button.config(text=lang['browse_button'])
        self.add_button.config(text=lang['add_button'])
        self.remove_button.config(text=lang['remove_button'])
        self.language_button.config(text=lang['change_language'])
        self.export_button.config(text=lang['export_button'])

    def update_listbox(self):
        """
        更新顯示阻擋清單
        - 清空現有清單
        - 從註冊表讀取並顯示所有阻擋項目
        """
        self.listbox.delete(0, tk.END)
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    _, value_data, _ = winreg.EnumValue(reg_key, i)
                    self.listbox.insert(tk.END, value_data)
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(reg_key)
        except FileNotFoundError:
            pass

    def is_app_in_blocklist(self, app_name):
        """
        檢查應用程式是否已在阻擋清單中
        參數：
            app_name: 要檢查的應用程式名稱
        返回值：
            True: 已在清單中
            False: 不在清單中
        """
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    _, value_data, _ = winreg.EnumValue(reg_key, i)
                    if value_data.lower() == app_name.lower():
                        winreg.CloseKey(reg_key)
                        return True
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(reg_key)
        except FileNotFoundError:
            pass
        return False

    def add_to_block_list(self):
        """
        新增應用程式到阻擋清單
        - 可以手動輸入或通過檔案選擇器選擇
        - 檢查是否重複
        - 新增到註冊表
        - 更新顯示清單
        """
        app_name = self.entry.get().strip()
        if not app_name:
            file_path = filedialog.askopenfilename(
                title=LANGUAGES[self.current_language]['file_dialog_title'],
                filetypes=LANGUAGES[self.current_language]['file_types']
            )
            if file_path:
                app_name = os.path.basename(file_path)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, app_name)
            else:
                return

        if self.is_app_in_blocklist(app_name):
            if self.current_language == 'zh_TW':
                messagebox.showwarning("錯誤", f"{app_name} 已經在阻擋清單中！")
            else:
                messagebox.showwarning("Error", f"{app_name} is already in the block list!")
            self.entry.delete(0, tk.END)
            return

        try:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY)
            i = 1
            while True:
                try:
                    winreg.EnumValue(reg_key, i-1)
                    i += 1
                except OSError:
                    break
            winreg.SetValueEx(reg_key, str(i), 0, winreg.REG_SZ, app_name)
            winreg.CloseKey(reg_key)
            self.update_listbox()
            self.entry.delete(0, tk.END)
            if self.current_language == 'zh_TW':
                messagebox.showinfo("成功", LANGUAGES[self.current_language]['success_add'].format(app_name))
            else:
                messagebox.showinfo("Success", LANGUAGES[self.current_language]['success_add'].format(app_name))
        except PermissionError:
            if self.current_language == 'zh_TW':
                messagebox.showerror("錯誤", LANGUAGES[self.current_language]['error_admin'])
            else:
                messagebox.showerror("Error", LANGUAGES[self.current_language]['error_admin'])

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title=LANGUAGES[self.current_language]['file_dialog_title'],
            filetypes=LANGUAGES[self.current_language]['file_types']
        )
        if file_path:
            app_name = os.path.basename(file_path)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, app_name)

    def show_delete_confirmation(self, selected_apps):
        """
        顯示刪除確認對話框
        參數：
            selected_apps: 要刪除的應用程式名稱列表
        返回值：
            True: 使用者確認刪除
            False: 使用者取消刪除
        """
        if len(selected_apps) == 1:
            if self.current_language == 'zh_TW':
                message = f"確定要刪除 {selected_apps[0]} 嗎？"
                title = "確認刪除"
            else:
                message = f"Are you sure you want to delete {selected_apps[0]}?"
                title = "Confirm Deletion"
        else:
            if self.current_language == 'zh_TW':
                message = "確定要刪除以下項目嗎？\n\n" + "\n".join(selected_apps)
                title = "確認刪除"
            else:
                message = "Are you sure you want to delete the following items?\n\n" + "\n".join(selected_apps)
                title = "Confirm Deletion"
        
        return messagebox.askyesno(title, message)

    def handle_delete_key(self, event):
        """
        處理 Delete 鍵事件
        """
        selected_items = self.listbox.curselection()
        if selected_items:
            selected_apps = [self.listbox.get(index) for index in selected_items]
            if self.show_delete_confirmation(selected_apps):
                self.remove_from_block_list()

    def remove_from_block_list(self):
        """
        從阻擋清單中移除選定的項目
        - 支援多重選擇
        - 從註冊表中刪除
        - 重新編號剩餘項目
        - 更新顯示清單
        """
        selected_items = self.listbox.curselection()
        if not selected_items:
            messagebox.showwarning("警告", LANGUAGES[self.current_language]['warning_select'])
            return

        # 獲取所有選中的項目名稱
        selected_apps = [self.listbox.get(index) for index in selected_items]
        
        try:
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
            
            # 重新寫入未被刪除的值，從1開始編號
            new_index = 1
            for value_name, value_data in values:
                if value_data not in selected_apps:  # 檢查是否在要刪除的清單中
                    winreg.SetValueEx(reg_key, str(new_index), 0, winreg.REG_SZ, value_data)
                    new_index += 1
            
            winreg.CloseKey(reg_key)
            self.update_listbox()
            
            # 根據刪除的數量顯示不同的訊息
            if len(selected_apps) == 1:
                if self.current_language == 'zh_TW':
                    messagebox.showinfo("成功", LANGUAGES[self.current_language]['success_remove'].format(selected_apps[0]))
                else:
                    messagebox.showinfo("Success", LANGUAGES[self.current_language]['success_remove'].format(selected_apps[0]))
            else:
                if self.current_language == 'zh_TW':
                    messagebox.showinfo("成功", f"已將 {len(selected_apps)} 個項目移出阻擋清單！")
                else:
                    messagebox.showinfo("Success", f"{len(selected_apps)} items have been removed from block list!")
            
        except FileNotFoundError:
            messagebox.showwarning("警告", LANGUAGES[self.current_language]['warning_blocklist'])
        except PermissionError:
            messagebox.showerror("錯誤", LANGUAGES[self.current_language]['error_admin'])

    def export_settings(self):
        """
        將當前的阻擋設定匯出為 .reg 檔案
        讓使用者選擇儲存位置和檔案名稱
        """
        try:
            # 取得所有阻擋清單項目
            blocked_apps = []
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DISALLOW_RUN_KEY, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    _, value_data, _ = winreg.EnumValue(reg_key, i)
                    blocked_apps.append(value_data)
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(reg_key)

            # 讓使用者選擇儲存位置
            file_path = filedialog.asksaveasfilename(
                title=LANGUAGES[self.current_language]['export_dialog_title'],
                filetypes=LANGUAGES[self.current_language]['export_file_types'],
                defaultextension=".reg",
                initialfile=LANGUAGES[self.current_language]['export_default_name']
            )
            
            if not file_path:  # 使用者取消選擇
                return

            # 建立 .reg 檔案內容
            reg_content = 'Windows Registry Editor Version 5.00\n\n'
            reg_content += '[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies]\n\n'
            reg_content += '[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer]\n'
            reg_content += '"DisallowRun"=dword:00000001\n\n'
            reg_content += '[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\DisallowRun]\n'
            
            # 加入阻擋清單項目
            for i, app in enumerate(blocked_apps, 1):
                reg_content += f'"{i}"="{app}"\n'

            # 儲存檔案
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(reg_content)

            # 顯示成功訊息
            messagebox.showinfo(
                "成功" if self.current_language == 'zh_TW' else "Success",
                LANGUAGES[self.current_language]['export_success'].format(file_path)
            )

        except Exception as e:
            # 顯示錯誤訊息
            messagebox.showerror(
                "錯誤" if self.current_language == 'zh_TW' else "Error",
                LANGUAGES[self.current_language]['export_error'].format(str(e))
            )

    def init_gui(self):
        """
        初始化圖形使用者介面
        - 建立主視窗
        - 建立所有 GUI 元件
        - 設置事件綁定
        """
        self.root = tk.Tk()
        lang = LANGUAGES[self.current_language]
        self.root.title(lang['title'])
        
        # 設置最小視窗大小
        self.root.minsize(500, 400)  # 加大最小視窗大小
        
        # 設定所有文字的字體
        button_font = ('Arial', 12)  # 按鈕字體
        label_font = ('Arial', 12)   # 標籤字體
        entry_font = ('Arial', 12)   # 輸入框字體
        list_font = ('Arial', 12)    # 清單框字體
        hint_font = ('Arial', 10)    # 提示文字字體
        
        # 配置根視窗的行列權重
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 語言切換按鈕
        self.language_button = tk.Button(
            self.root, 
            text=lang['change_language'],
            font=button_font,
            command=self.change_language
        )
        self.language_button.grid(row=0, pady=10)  # 增加間距

        # 頂部框架
        frame_top = tk.Frame(self.root)
        frame_top.grid(row=1, pady=10, sticky='ew')
        frame_top.grid_columnconfigure(1, weight=1)

        # 應用程式名稱標籤
        self.entry_label = tk.Label(
            frame_top,
            text=lang['app_name_label'],
            font=label_font
        )
        self.entry_label.grid(row=0, column=0, padx=5)

        # 輸入框架
        entry_frame = tk.Frame(frame_top)
        entry_frame.grid(row=0, column=1, padx=5, sticky='ew')
        entry_frame.grid_columnconfigure(0, weight=1)

        # 輸入框
        self.entry = tk.Entry(
            entry_frame,
            font=entry_font
        )
        self.entry.grid(row=0, column=0, sticky='ew')
        self.entry.bind('<Return>', lambda event: self.add_to_block_list())

        # 範例提示文字
        self.example_label = tk.Label(
            entry_frame,
            text=lang['example_text'],
            font=hint_font,
            fg="gray"
        )
        self.example_label.grid(row=1, column=0)

        # 瀏覽按鈕
        self.browse_button = tk.Button(
            frame_top, 
            text=lang['browse_button'],
            font=button_font,
            command=self.browse_file
        )
        self.browse_button.grid(row=0, column=2, padx=5)

        # 新增按鈕
        self.add_button = tk.Button(
            frame_top, 
            text=lang['add_button'],
            font=button_font,
            command=self.add_to_block_list
        )
        self.add_button.grid(row=0, column=3, padx=5)

        # 建立按鈕框架來容納刪除和匯出按鈕
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, pady=10)  # 增加間距

        # 刪除按鈕
        self.remove_button = tk.Button(
            button_frame,
            text=LANGUAGES[self.current_language]['remove_button'],
            font=button_font,
            command=self.remove_from_block_list
        )
        self.remove_button.grid(row=0, column=0, padx=(0, 15))  # 增加按鈕間距

        # 匯出按鈕
        self.export_button = tk.Button(
            button_frame,
            text=LANGUAGES[self.current_language]['export_button'],
            font=button_font,
            command=self.export_settings
        )
        self.export_button.grid(row=0, column=1)

        # 建立框架來容納清單和滾動軸
        list_frame = tk.Frame(self.root)
        list_frame.grid(row=3, sticky='nsew', padx=10, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # 建立滾動軸
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # 建立清單框並連接滾動軸
        self.listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set,
            font=list_font
        )
        self.listbox.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.listbox.yview)
        
        # 綁定 Delete 鍵事件
        self.listbox.bind('<Delete>', self.handle_delete_key)

    def run(self):
        """
        啟動應用程式
        - 更新初始清單
        - 開始主迴圈
        """
        self.update_listbox()
        self.root.mainloop()

# 主程式入口
if __name__ == "__main__":
    # 檢查管理員權限
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    # 確保政策已啟用
    ensure_disallow_run_policy()
    
    # 建立並運行應用程式
    app = BlockListManager()
    app.run()
