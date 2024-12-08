import os
import subprocess
import sys

def create_virtual_env():
    """Tạo môi trường ảo và cài đặt thư viện."""
    print("Đang tạo môi trường ảo...")
    subprocess.run([sys.executable, "-m", "venv", "env"], check=True)
    pip_path = os.path.join("env", "Scripts" if os.name == "nt" else "bin", "pip")
    print("Đang cài đặt các thư viện...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_path, "install", "pyinstaller", "PyQt6", "pandas", "openpyxl"], check=True)
    print("Môi trường ảo và thư viện đã được cài đặt!")

def build_exe():
    """Đóng gói file Python thành exe."""
    pyinstaller_path = os.path.join("env", "Scripts" if os.name == "nt" else "bin", "pyinstaller")
    script_name = os.path.join(os.getcwd(), "Hosts.py")  # Lấy đường dẫn đầy đủ tới file script

    # Kiểm tra file script tồn tại
    if not os.path.isfile(script_name):
        raise FileNotFoundError(f"File script '{script_name}' không tồn tại. Hãy kiểm tra lại tên file hoặc đường dẫn!")

    print("Đang đóng gói file exe...")
    try:
        # Đường dẫn UPX
        upx_path = "D:/Users/HT-IT/Desktop/Ai Automation/Code Python/upx-4.2.4-win64/upx.exe"
        subprocess.run([upx_path, "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        upx_option = f"--upx-dir={os.path.dirname(upx_path)}"
    except FileNotFoundError:
        print("UPX không được tìm thấy. Đóng gói mà không nén bằng UPX.")
        upx_option = ""

    # Lệnh PyInstaller
    output_folder = os.path.join(os.getcwd(), "output_exe")  # Thư mục xuất file .exe
    os.makedirs(output_folder, exist_ok=True)

    pyinstaller_command = [
        pyinstaller_path,
        "--onefile",              # Đóng gói thành 1 file
        "--windowed",             # Ẩn terminal (cho ứng dụng GUI)
        "--noconfirm",            # Bỏ qua xác nhận
        "--clean",                # Dọn dẹp file tạm
        "--distpath", output_folder,  # Thư mục xuất file
        script_name
    ]
    if upx_option:
        pyinstaller_command.insert(-1, upx_option)  # Thêm trước script_name

    subprocess.run(pyinstaller_command, check=True)
    print("File exe đã được tạo thành công!")

def main():
    """Hàm chính."""
    try:
        create_virtual_env()
        build_exe()
        print("Hoàn tất quá trình đóng gói!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    main()
