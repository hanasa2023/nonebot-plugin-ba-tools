import platform
import subprocess
from datetime import datetime
from typing import Any

import nonebot
import psutil


def bytes_to_gb(bytes: int) -> float:
    """将字节转换为GB并保留两位小数"""
    return round(bytes / (1024**3), 2)


def get_cpu_info() -> dict[str, str]:
    """获取CPU信息"""
    cpu_info: dict[str, Any] = {
        "cpu_count": psutil.cpu_count(),
        "cpu_freq": psutil.cpu_freq(),
        "cpu_percent": f"{psutil.cpu_percent(interval=1)}%",
    }

    if platform.system() == "Windows":
        cpu_info["processor_name"] = platform.processor()
    elif platform.system() == "Linux":
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.strip().startswith("model name"):
                    cpu_info["processor_name"] = line.split(":")[1].strip()
                    break
    elif platform.system() == "Darwin":
        cpu_info["processor_name"] = (
            subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        )

    return cpu_info


def get_memory_info() -> dict[str, dict[str, Any]]:
    """获取内存和SWAP信息"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    memory_info: dict[str, dict[str, Any]] = {
        "mem": {
            "total": bytes_to_gb(mem.total),
            "used": bytes_to_gb(mem.used),
            "percent": f"{mem.percent}%",
        },
        "swap": {
            "total": bytes_to_gb(swap.total),
            "used": bytes_to_gb(swap.used),
            "percent": f"{swap.percent}%",
        },
    }

    return memory_info


def get_disk_info() -> list[Any]:
    """获取磁盘分区信息"""
    disks_info: list[Any] = []
    for part in psutil.disk_partitions():
        if part.fstype:
            usage = psutil.disk_usage(part.mountpoint)
            disks_info.append(
                {
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "total": bytes_to_gb(usage.total),
                    "used": bytes_to_gb(usage.used),
                    "free": bytes_to_gb(usage.free),
                    "percent": f"{usage.percent}%",
                }
            )

    return disks_info


def get_system_info() -> dict[str, str]:
    """获取系统版本信息"""
    system_info: dict[str, str] = {
        "type": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "arch": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
    }

    return system_info


def get_nonebot_info() -> dict[str, Any]:
    """获取NoneBot信息"""
    plugin_count = len(nonebot.get_loaded_plugins())
    nonebot_version = f"nonebot {nonebot.__version__} x ba-tools 0.5.5"
    nickname = nonebot.get_driver().config.nickname

    return {
        "version": nonebot_version,
        "plugin_count": plugin_count,
        "nickname": nickname,
    }


def get_all_info() -> dict[str, Any]:
    """获取所有信息"""
    return {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "system": get_system_info(),
        "nonebot": get_nonebot_info(),
    }
