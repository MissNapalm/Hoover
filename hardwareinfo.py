import platform
import json
import psutil
import GPUtil
import win32com.client
import keyboard
import os  # Import the 'os' module

def gather_gpu_info():
    gpu_info = GPUtil.getGPUs()
    gpu_data = []
    
    for idx, gpu in enumerate(gpu_info):
        gpu_data.append(f"GPU {idx + 1}:")
        gpu_data.append(f"  Name: {gpu.name}")
        gpu_data.append(f"  Driver: {gpu.driver}")
        gpu_data.append(f"  VRAM: {gpu.memoryTotal} MB")
    
    return gpu_data

def gather_motherboard_info():
    motherboard_info = {}
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
    for board in wmi.ExecQuery("SELECT * FROM Win32_BaseBoard"):
        motherboard_info["Manufacturer"] = board.Manufacturer
        motherboard_info["Model"] = board.Product

    return motherboard_info

def gather_usb_device_info():
    usb_device_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
    for usb in wmi.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE ConfigManagerErrorCode = 0"):
        usb_device_info.append(usb.Name)

    return usb_device_info

def gather_update_status():
    update_status = os.popen("schtasks /query /fo LIST /v /s Microsoft\\Windows\\WindowsUpdate").read()
    return update_status

def gather_running_processes():
    running_processes = psutil.process_iter(attrs=['pid', 'name'])
    process_info = []
    for process in running_processes:
        process_info.append(f"PID: {process.info['pid']}, Name: {process.info['name']}")

    return process_info

def gather_system_info():
    system_info = {}

    # Get hardware information
    system_info["CPU"] = platform.processor()
    system_info["RAM"] = f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"  # RAM in GB

    # Get GPU information
    system_info["GPUs"] = gather_gpu_info()

    # Get motherboard information
    system_info["Motherboard"] = gather_motherboard_info()

    # Get USB device information
    system_info["USB Devices"] = gather_usb_device_info()

    # Get computer update status
    system_info["Update Status"] = gather_update_status()

    # Get running processes
    system_info["Running Processes"] = gather_running_processes()

    return system_info

def display_system_info(system_info):
    print("╔════════════════════════════════════╗")
    print("║       System Information          ║")
    print("╚════════════════════════════════════╝")

    for category, info in system_info.items():
        print(f"  {category}:")
        
        if isinstance(info, list):
            for item in info:
                print(item)
        elif isinstance(info, dict):
            for key, value in info.items():
                print(f"    {key}: {value}")
        else:
            print(f"    {info}")

def save_to_json(data):
    with open("system_info.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    input("Press Enter to continue...")

    system_info = gather_system_info()
    display_system_info(system_info)

    save_to_json(system_info)
    print("System information saved to system_info.json")

    input("Press Enter to exit...")
