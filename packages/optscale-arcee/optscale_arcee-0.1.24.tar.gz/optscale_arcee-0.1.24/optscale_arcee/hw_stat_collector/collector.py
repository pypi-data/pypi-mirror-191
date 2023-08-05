import asyncio
import concurrent.futures
from functools import partial, reduce

import GPUtil
import psutil


class Collector:

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    @classmethod
    async def run_async(cls, func, *args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        if executor is None:
            executor = cls.executor
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    @staticmethod
    def _gpu_stats():
        gpus = GPUtil.getGPUs()
        len_gpus = len(gpus)
        if len_gpus < 1:
            return {}
        avg_gpu_load = reduce(lambda x, y: x + y, map(lambda z: z.load, gpus)) / len(
            gpus
        )
        avg_gpu_memory_free = reduce(
            lambda x, y: x + y, map(lambda z: z.memoryFree, gpus)
        ) / len(gpus)
        avg_gpu_memory_total = reduce(
            lambda x, y: x + y, map(lambda z: z.memoryTotal, gpus)
        ) / len(gpus)
        avg_gpu_memory_used = reduce(
            lambda x, y: x + y, map(lambda z: z.memoryUsed, gpus)
        ) / len(gpus)
        return {
            "avg_gpu_load": avg_gpu_load,
            "avg_gpu_memory_free": avg_gpu_memory_free,
            "avg_gpu_memory_total": avg_gpu_memory_total,
            "avg_gpu_memory_used": avg_gpu_memory_used,
        }

    @staticmethod
    def _ps_stats():
        load1, load5, load15 = psutil.getloadavg()
        return {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "load_average": [load1, load5, load15],
            "cpu_usage": (load15 / psutil.cpu_count()) * 100,
            "used_ram_percent": psutil.virtual_memory()[2],
            "used_ram_mb": psutil.virtual_memory()[3] / 1000000,
        }

    @classmethod
    def _collect_stats(cls):
        gpu_stats = cls._gpu_stats()
        ps_stats = cls._ps_stats()
        return {
            "ps_stats": ps_stats,
            "gpu_stats": gpu_stats,
        }

    @classmethod
    async def collect_stats(cls):
        return await cls.run_async(cls._collect_stats)
