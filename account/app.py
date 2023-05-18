import requests
import json
import gradio as gr

def get_token(username, password):
    try:
        url = "https://npssolutions.works/api/v1/auth/login"

        payload = json.dumps({
        "username": username,
        "password": password
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()

        access_token = response['data']['access_token']

        print(response)
        print(access_token)
      

        return access_token, gr.update(value="""<i style="color:#3ADF00"><center>Đăng nhập thành công. Mời sử dụng</center></i>""")
    except:
        return "", gr.update(value="""<i style="color:red"><center>Tài khoản hoặc mật khẩu không đúng. Xin thử lại</center></i>""")
