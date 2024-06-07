import socket
import threading
import pyautogui
import pickle
import zlib

# Server details
HOST = '127.0.0.1'  # Listen on all interfaces
PORT = 6000

def capture_screen():
    # Capture the screen
    screenshot = pyautogui.screenshot()
    return screenshot

def handle_client(client_socket):
    try:
        while True:
            # Capture the screen
            screenshot = capture_screen()
            
            # Convert screenshot to bytes
            screenshot_bytes = screenshot.tobytes()
            width, height = screenshot.size

            # Compress the screenshot
            compressed_data = zlib.compress(screenshot_bytes, 9)

            # Send width, height, and compressed screenshot size
            client_socket.sendall(pickle.dumps((width, height, len(compressed_data))))
            
            # Send the compressed screenshot
            client_socket.sendall(compressed_data)
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
