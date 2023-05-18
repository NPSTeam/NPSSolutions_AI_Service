

### Cài đặt trên Windows
1. Cài đặt [Python 3.10.6](https://www.python.org/downloads/windows/), tích chọn vào "Add Python to PATH" trong quá trình cài đặt
2. Cài đặt [git](https://git-scm.com/download/win).
3. Tải về mã nguồn của Chatbot (git clone ../)
4. Tiếp theo bạn kích đúp chuột vào file `run.bat` ở thư mục mã nguồn ChatBot và chờ đợi chương trình khởi chạy.


### Cài đặt trên Linux
Để chạy các lệnh dưới đây bạn cần sử dụng Terminal trên máy của bạn
1. Cài đặt python (phiên bản 3.10.6 trở lên):
```bash
# Debian-based:
sudo apt install wget git python3 python3-venv
# Red Hat-based:
sudo dnf install wget git python3
# Arch-based:
sudo pacman -S wget git python3
```
2. Tiếp theo tải về mã nguồn của ChatBot bằng lệnh sau:
```bash
git clone ...
```
3. Tiếp theo bạn mở thư mục mã nguồn ChatBot đã tải về và copy file `.env.example` thành file `.env` sau đó thay đoạn `your_open_api_key` thành Open API Key của bạn.
4. Tiếp theo chạy file `bash run.sh` để chương trình khởi chạy. (Có thể bạn cần chạy thêm lệnh `chmod +x run.sh` để cấp quyền chạy chương trình cho ChatBot)
5. Sau khi chương trình đã chạy bạn có thể mở đường dẫn `http://127.0.0.1:7860` trên trình duyệt để sử dụng ChatBot.

### ChatBot cài đặt trên Macos
Để chạy các lệnh dưới đây bạn cần sử dụng Terminal trên máy của bạn
1. Cài đặt gói [Brew](https://brew.sh/)
1. Cài đặt python (phiên bản 3.10.6 trở lên) sử dụng lệnh sau:
```bash
brew install python@3.10
```
2. Tiếp theo tải về mã nguồn của ChatBot bằng lệnh sau:
```bash
git clone ...
```
3. Tiếp theo bạn mở thư mục mã nguồn ChatBot đã tải về và copy file `.env.example` thành file `.env` sau đó thay đoạn `your_open_api_key` thành Open API Key của bạn.
4. Tiếp theo chạy file `bash run.sh` để chương trình khởi chạy. (Có thể bạn cần chạy thêm lệnh `chmod +x run.sh` để cấp quyền chạy chương trình cho ChatBot)
5. Sau khi chương trình đã chạy bạn có thể mở đường dẫn `http://127.0.0.1:7860` trên trình duyệt để sử dụng ChatBot.