import psutil
import time
import tkinter as tk
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from threading import Thread
import queue
import pythoncom

def get_network_speed():
    net1 = psutil.net_io_counters()
    time.sleep(0.02)
    net2 = psutil.net_io_counters()
    
    download_speed = (net2.bytes_recv - net1.bytes_recv) * 8 / 1_000_000  # in Mbps
    upload_speed = (net2.bytes_sent - net1.bytes_sent) * 8 / 1_000_000    # in Mbps
    return download_speed, upload_speed

def get_volume_level():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar() * 100  
    return current_volume

def collect_data(data_queue):
    pythoncom.CoInitialize()
    try:
        while True:
            cpu_usage = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            download_speed, upload_speed = get_network_speed()
            volume_level = get_volume_level()
            current_time = datetime.now().strftime("%H:%M:%S")
            
            data_queue.put((cpu_usage, memory_info.percent, volume_level, download_speed, upload_speed, current_time))
            time.sleep(0.2) 
    finally:
        pythoncom.CoUninitialize()

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("500x400")
        self.root.configure(bg="#2E2E2E")  

        title_label = tk.Label(root, text="System Monitor", font=("Helvetica", 18, "bold"), bg="#2E2E2E", fg="#FFFFFF")
        title_label.pack(pady=20)

        stats_frame = tk.Frame(root, bg="#2E2E2E")
        stats_frame.pack(pady=10)

        self.cpu_label = tk.Label(stats_frame, text="CPU Usage: 0%", font=("Arial", 14), bg="#2E2E2E", fg="#FFFFFF")
        self.cpu_label.grid(row=0, column=0, padx=20)

        self.memory_label = tk.Label(stats_frame, text="Memory Usage: 0%", font=("Arial", 14), bg="#2E2E2E", fg="#FFFFFF")
        self.memory_label.grid(row=1, column=0, padx=20)

        self.volume_label = tk.Label(stats_frame, text="Volume Level: 0%", font=("Arial", 14), bg="#2E2E2E", fg="#FFFFFF")
        self.volume_label.grid(row=2, column=0, padx=20)

        self.network_label = tk.Label(stats_frame, text="Download: 0 Mbps | Upload: 0 Mbps", font=("Arial", 14), bg="#2E2E2E", fg="#FFFFFF")
        self.network_label.grid(row=3, column=0, padx=20)

        self.time_label = tk.Label(root, text="Time: 00:00:00", font=("Arial", 12), bg="#2E2E2E", fg="#FFFFFF")
        self.time_label.pack(pady=10)

        self.status_bar = tk.Label(root, text="", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.data_queue = queue.Queue()

        self.data_thread = Thread(target=collect_data, args=(self.data_queue,), daemon=True)
        self.data_thread.start()

        self.update_stats()

        close_button = tk.Button(root, text="Exit", command=root.quit, bg="#FF4D4D", fg="#FFFFFF", font=("Arial", 12, "bold"))
        close_button.pack(pady=20)

    def update_stats(self):
        while not self.data_queue.empty():
            cpu_usage, memory_usage, volume_level, download_speed, upload_speed, current_time = self.data_queue.get()

            self.cpu_label.config(text=f"CPU Usage: {cpu_usage:.1f}%")
            self.memory_label.config(text=f"Memory Usage: {memory_usage:.1f}%")
            self.volume_label.config(text=f"Volume Level: {volume_level:.1f}%")
            self.network_label.config(text=f"Download: {download_speed:.2f} Mbps | Upload: {upload_speed:.2f} Mbps")
            self.time_label.config(text=f"Time: {current_time}")

            self.status_bar.config(text="Monitoring system performance...")

        self.root.after(10, self.update_stats)  # Update every 100ms

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
