# Windows 應用程式阻擋工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md)

這是一個 Windows 應用程式，提供圖形化介面來管理被阻擋的應用程式。透過 Windows 註冊表來防止特定應用程式執行。

## 📋 功能特色

- 阻擋指定的 Windows 應用程式執行
- 直覺的圖形使用者介面
- 支援手動輸入和檔案選擇
- 多語言支援（繁體中文/英文）
- 支援多重選擇批次刪除
- 即時更新阻擋清單
- 自動偵測系統語言

## 📸 軟體畫面

![主視窗介面](https://github.com/user-attachments/assets/3e1446d8-4547-4fc3-aa6e-9451a8918c16)
![禁止執行展示](https://github.com/user-attachments/assets/2aa3a050-1b50-454f-8e2c-f18c850c7fe1)

## 💻 安裝方式

1. 從發布頁面[下載最新版本](https://github.com/jmsch23280866/Windows-Blocklist-Manager/releases/latest)
2. 以系統管理員身分執行程式
3. 程式會自動設定必要的註冊表項目

## 📖 使用方法

### 新增阻擋應用程式
- 直接輸入應用程式名稱（例如：notepad.exe）
- 或使用「瀏覽」按鈕選擇執行檔
- 按下 Enter 鍵或點擊「新增」按鈕來加入阻擋清單

### 移除阻擋應用程式
- 在清單中選擇一個或多個項目
- 按下 Delete 鍵或點擊「刪除選定項目」按鈕
- 在彈出的確認對話框中確認刪除

## ⚙️ 技術細節

- 使用 Python 和 Tkinter 開發
- 透過 Windows 註冊表實現阻擋功能
### 運作原理

本工具透過修改 Windows 註冊表中的以下機碼來實現應用程式阻擋功能：
```
HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun
```
- 需要系統管理員權限修改系統設定
- 支援 Windows 10/11


## 📋 系統需求

- Windows 10 或更新版本
- 系統管理員權限
- Python 3.x（如果從原始碼執行）

## 📜 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🤝 貢獻指南

歡迎提交 Issue 或 Pull Request 來協助改善這個專案！

## 👨‍💻 作者

特務E04 ([@jmsch23280866](https://github.com/jmsch23280866))

## 🤖 AI 協助聲明

本專案在開發過程中獲得 Claude AI 及 ChatGPT 的協助，包括程式碼優化建議和文件撰寫。

## 📝 更新日誌

### v2 (2025-01-13)
- 新增多語言系統（支援繁體中文/英文）
- 支援多重選擇批次刪除功能
- 新增刪除確認機制
- 改善使用者介面與排版
- 新增鍵盤快捷鍵支援
- 新增滾動軸功能
- 程式碼重構，提升穩定性

### v1.2 (2025-01-10)
- 改善系統政策設置機制
- 新增重複項目檢查
- 強化錯誤處理功能

### v1.1 (2025-01-10)
- 新增檔案瀏覽功能
- 新增輸入框提示文字
- 改善介面排版

### v1 (2025-01-10)
- 首次發布
- 基本阻擋功能
- 簡易圖形介面
- 基本新增/刪除功能

## 🙏 致謝

特別感謝 [CyberCPU Tech](https://youtu.be/z-4YYzWb-GQ) 的影片提供開發靈感。
