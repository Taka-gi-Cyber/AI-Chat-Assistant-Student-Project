# -*- coding: utf-8 -*-
# 百度AI大模型聊天助手（单页版）
# 运行前：请安装依赖 -> pip install requests
import requests
import tkinter as tk
from tkinter import scrolledtext, ttk

# ===================== 填写你的信息 =====================
STUDENT_ID = "梁灿麟"
STUDENT_NAME = "423830109"
BAIDU_API_KEY = "你的百度AI API Key"
BAIDU_SECRET_KEY = "你的百度AI Secret Key"


# ========================================================

# 获取百度AI Access Token
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY
    }
    try:
        response = requests.post(url, data=params)
        return response.json().get("access_token")
    except:
        return None


# 调用百度大模型
def call_baiduaibot(message):
    token = get_access_token()
    if not token:
        return "❌ 获取Access Token失败，请检查API Key。"

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={token}"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json().get("result", {}).get("answer", "AI回复失败。")
        return result
    except Exception as e:
        return f"❌ 调用失败：{str(e)}"


# 主窗口
root = tk.Tk()
root.title(f"AI聊天助手 | {STUDENT_NAME}({STUDENT_ID})")
root.geometry("900x700")
root.resizable(True, True)

# 侧边栏
sidebar = ttk.Frame(root, padding=15)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
ttk.Label(sidebar, text="📌 项目信息", font=("微软雅黑", 14, "bold")).pack(pady=10)
ttk.Label(sidebar, text=f"学号：{STUDENT_ID}", font=("微软雅黑", 11)).pack(pady=5, anchor=tk.W)
ttk.Label(sidebar, text=f"姓名：{STUDENT_NAME}", font=("微软雅黑", 11)).pack(pady=5, anchor=tk.W)
ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
ttk.Label(sidebar, text="⚙️ 项目特性", font=("微软雅黑", 14, "bold")).pack(pady=10)
ttk.Label(sidebar, text="✅ 百度AI大模型", font=("微软雅黑", 11)).pack(pady=3, anchor=tk.W)
ttk.Label(sidebar, text="✅ 单页代码运行", font=("微软雅黑", 11)).pack(pady=3, anchor=tk.W)
ttk.Label(sidebar, text="✅ 可参数调优", font=("微软雅黑", 11)).pack(pady=3, anchor=tk.W)

# 聊天区域
chat_frame = ttk.Frame(root, padding=15)
chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# 聊天记录
chat_history = scrolledtext.ScrolledText(
    chat_frame, wrap=tk.WORD, font=("微软雅黑", 11),
    state=tk.DISABLED, bg="#f8f9fa", padx=10, pady=10
)
chat_history.pack(fill=tk.BOTH, expand=True, pady=5)

# 输入框
input_frame = ttk.Frame(chat_frame)
input_frame.pack(fill=tk.X, pady=10)
input_box = ttk.Entry(input_frame, font=("微软雅黑", 11))
input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=5)


# 发送
def send_message():
    user_input = input_box.get().strip()
    if not user_input:
        return
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"你：{user_input}\n\n", "user")
    chat_history.tag_config("user", foreground="#007bff", font=("微软雅黑", 11, "bold"))
    chat_history.config(state=tk.DISABLED)
    input_box.delete(0, tk.END)

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "AI：思考中...\n\n", "thinking")
    chat_history.tag_config("thinking", foreground="#6c757d", font=("微软雅黑", 11, "italic"))
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)

    root.after(100, lambda: show_ai_response(user_input))


def show_ai_response(user_input):
    ai_reply = call_baiduaibot(user_input)
    chat_history.config(state=tk.NORMAL)
    chat_history.delete("end-2l", tk.END)
    chat_history.insert(tk.END, f"AI：{ai_reply}\n\n", "ai")
    chat_history.tag_config("ai", foreground="#28a745", font=("微软雅黑", 11))
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)


# 按钮
send_btn = ttk.Button(input_frame, text="发送", command=send_message)
send_btn.pack(side=tk.RIGHT, padx=5, ipady=5)
input_box.bind("<Return>", lambda e: send_message())

# 启动
if __name__ == "__main__":
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"AI：你好！我是{STUDENT_NAME}({STUDENT_ID})的百度AI聊天助手。\n\n", "ai")
    chat_history.config(state=tk.DISABLED)
    root.mainloop()