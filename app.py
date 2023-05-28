import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv('./.env')
from chatgpt.app import *
from speech_to_text.app import *
from account.app import *
from lib_app.utils import *
from summary_long_text.app import *
from docs.app import *

OPEN_API_KEY = os.environ['OPEN_API_KEY']
first_key_lock = encode("encode", OPEN_API_KEY, SECRET_KEY)
SECRET_KEY = os.environ['SECRET_KEY']
# IMG_BANNER = os.environ['IMG_BANNER']
#all function process app
# func check type account
def filter_type_account(type_account):
  if type_account == "OpenAI Token":
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
  elif type_account == "Tài khoản NPSSolutions":
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
#func check options cut video
def filter_full_time(fulltime, link_youtube):
  if fulltime == True:
    return gr.update(visible=False), gr.update(visible=False)
  elif fulltime == False:
    print("This link: ",link_youtube)
    length = length_link(link_youtube)
    return gr.update(visible=True, maximum=length), gr.update(visible=True, maximum=length)
# func check ready result speech to text
def check_result_speech_to_text(whisper_result):
   if whisper_result:
      return gr.update(interactive=True)
   else:
      return gr.update(interactive=False)

# func check exits link youtube
def check_link_youtube(link_youtube):
   try:
      populate_metadata(link_youtube)
      return gr.update(interactive=True), gr.update(value="""<i style="color:#3ADF00"><center>Link youtube hợp lệ. Mời tiếp tục</center></i>""", visible=True)
   except:
      return gr.update(interactive=False), gr.update(value="""<i style="color:red"><center>Link youtube không hợp lệ. Xin thử lại</center></i>""", visible=True)

# func check type speech_to_text
def check_type_transcripts(type_transcripts):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      return gr.update(visible=False), gr.update(visible=True)
   else:
      return gr.update(visible=True), gr.update(visible=False)

# process before speech_to_text
def process_speech_to_text(type_transcripts, language_transcripts,link_youtube, cut_fulltime, msecond_start, msecond_end, main_key):
   if type_transcripts == "Sử dụng subtitles của Youtube":
      if language_transcripts == "Tiếng Việt":
        transcripts = youtube_transcripts_with_subtitles(link_youtube, "vi")
      else:
        transcripts = youtube_transcripts_with_subtitles(link_youtube, "en")
      return transcripts
   else:
      transcripts = speech_to_text(link_youtube, cut_fulltime, msecond_start, msecond_end, main_key)
      return transcripts
   
# function process speech to text
def process_transcribe_with_cut_file(audio_upload, main_key):
   result = transcribe_with_cut_file(audio_upload, main_key)
   if result:
      return result, gr.update(value="""<i style="color:#3ADF00"><center>Bóc băng thành công. Mời tiếp tục</center></i>""", visible=True), gr.update(interactive=True), gr.update(interactive=True)
   else:
      return result, gr.update(value="""<i style="color:red"><center>Đã có lỗi xảy ra. Xin thử lại</center></i>""", visible=True), gr.update(interactive=False), gr.update(interactive=False)

# function update main key (openai api key) for all app
def update_main_key(api_key_textbox):
   key_lock = encode("encode", api_key_textbox, SECRET_KEY)
   return gr.update(value=key_lock)


block = gr.Blocks(css=".gradio-container {padding-top:0px !important; padding-bottom:0px !important;} footer {display:none !important;} #chatbot_custom > .wrap > .message-wrap > .bot {font-size:16px !important; background-color: rgb(129, 140, 248) !important; color: #FFF} #chatbot_custom > .wrap > .message-wrap > .user {font-size:16px !important; background-color: rgb(100, 116, 139) !important; color: #FFF} #custom_row {flex-direction: row-reverse;} #chatbot_custom > .wrap > .message-wrap {min-height: 150px;} #custom_title_h1 > h1 {margin-bottom:0px;} #chatbot_custom > .wrap {max-height: 1500px;}")

# function check event change value of flag textbox
def check_flag_textbox(flag_textbox):
   return gr.update(value=flag_textbox)

with block:
    main_key = gr.Textbox(visible=False, value=first_key_lock)
    flag_textbox = gr.Textbox(visible=False)
    # ChatGPT--turbo3.5
    with gr.Tab("ChatGPT"):
        with gr.Row(elem_id="custom_row"):
            with gr.Column(scale=3, min_width=600):
              # max_tokens = gr.Slider(label="Số từ tối đa trong câu hỏi", minimum=150, maximum=1048, step=1, value=256, visible=False)
              # role=gr.Radio(["user", "system", "assistant"], label="Lựa chọn vai trò sẽ hỏi", visible=False)
              temperature = gr.Slider(label="Creativity level of AI (minimum 0, maximum 1)", minimum=0, maximum=1, step=0.1, value=0.1, interactive=True)
              num_history = gr.Slider(label="Number of AI conversation history that can be remembered", minimum=1, maximum=10, step=1, value=2, interactive=True)
            with gr.Column(scale=5, min_width=600):
              chatbot = gr.Chatbot(elem_id="chatbot_custom")
              alert_response_chatgpt = gr.Markdown(value="""<i style="color:#3ADF00"><center>Câu hỏi càng ngắn gọn số token càng nhỏ</center></i>""", visible=False) 
              message = gr.Textbox(placeholder="Ask the chatbot any question that you want", label="Your question")
              state = gr.State()
              submit = gr.Button("Send")
              #submit gpt
              submit.click(chat, inputs=[message, state, temperature, main_key, num_history], outputs=[chatbot, state, alert_response_chatgpt])
              submit.click(lambda :"", None, message, scroll_to_output=True)
              message.submit(chat, inputs=[message, state, temperature, main_key, num_history], outputs=[chatbot, state, alert_response_chatgpt])
              message.submit(lambda :"", None, message, scroll_to_output=True)
              #clear history chat
              clear = gr.Button("Delete chat history")
              clear.click(lambda: None, None, chatbot, queue=False)
              clear.click(fn=clear_history, inputs=state, outputs=state)
    
    
    # summary text
    
    # Bot hướng dẫn sử dụng
    with gr.Tab("Custom Chatbot"):
        gr.Markdown("""<h1><centerCustom Chatbot</center></h1>""")
        with gr.Box(elem_id="custom_row"):
              chatbot_docs = gr.Chatbot(elem_id="chatbot_custom")
              alert_response_chatgpt_docs = gr.Markdown(value="""<i style="color:#3ADF00"><center>Câu hỏi càng ngắn gọn số token càng nhỏ</center></i>""", visible=False) 
              message_docs = gr.Textbox(placeholder="Ask the chatbot any question about NPSSolutions that you want", label="Your Question")
              state_docs = gr.State()
              with gr.Row().style(equal_height=True):
                submit_docs = gr.Button("Send")
                #submit gpt
                submit_docs.click(chat_docs, inputs=[message_docs, state_docs, main_key], outputs=[chatbot_docs, state_docs, alert_response_chatgpt_docs])
                submit_docs.click(lambda :"", None, message_docs, scroll_to_output=True)
                message_docs.submit(chat_docs, inputs=[message_docs, state_docs, main_key], outputs=[chatbot_docs, state_docs, alert_response_chatgpt_docs])
                message_docs.submit(lambda :"", None, message_docs, scroll_to_output=True)
                #clear history chat
                clear_docs = gr.Button("Delete chat history")
                clear_docs.click(lambda: None, None, chatbot_docs, queue=False)
                clear_docs.click(fn=clear_history_docs, inputs=state_docs, outputs=state_docs)
    # Veri account
    with gr.Tab("Account"):
        gr.Markdown("""<h1><center>Dùng OpenAI Key hoặc tài khoản NPSSolutions để sử dụng</center></h1>""")
        type_account = gr.Radio(label="Loại tài khoản", choices=["OpenAI Token", "Tài khoản NPSSolutions"], value="OpenAI Token")
        api_key_textbox = gr.Textbox(placeholder="Nhập OpenAI Token vào đây" ,show_label=False, lines=1, type='password', interactive=True, visible=True, value=OPEN_API_KEY)
        username = gr.Textbox(label="Tài khoản", visible=False, interactive=True)
        password = gr.Textbox(label="Mật khẩu",type='password', visible=False, interactive=True)
        alert_login = gr.Markdown(value="""<i style="color:#0040FF"><center>Tài khoản này do NPSSolutions cấp</center></i>""", visible=False)
        login_btn = gr.Button("Đăng nhập", visible=False)
        login_btn.click(get_token, [username, password], outputs=[api_key_textbox, alert_login], scroll_to_output=True)
        password.submit(get_token, [username, password], outputs=[api_key_textbox, alert_login], scroll_to_output=True)
        type_account.change(filter_type_account, type_account, outputs=[api_key_textbox, username, password, login_btn, alert_login])
        api_key_textbox.change(update_main_key, api_key_textbox, main_key)
# info auth app
ID = os.environ['ID']
PASSWORD = os.environ['PASSWORD']
AUTH = os.environ['AUTH']
HOST = os.environ['HOST']
if AUTH == "False":
  block.queue(concurrency_count=1)
  block.launch(server_name = HOST,debug = True)
else:
  block.queue(concurrency_count=1)
  block.launch(server_name = HOST, auth = (ID,PASSWORD),debug = True)
 