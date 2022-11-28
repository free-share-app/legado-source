# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/10/22
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import asyncio

from common import config


async def wait(tasks):
    arr = []

    semaphore = config.asyncio['semaphore']
    if semaphore is not None:
        semaphore = asyncio.Semaphore(min(semaphore, len(tasks)))

    for task in tasks:

        if semaphore is not None:
            arr.append(asyncio.create_task(with_semaphore(semaphore, with_sleep(task))))
            continue
        arr.append(asyncio.create_task(with_sleep(task)))

    return await asyncio.wait(arr)



async def gather(tasks):
    arr = []

    semaphore = config.asyncio['semaphore']
    if semaphore is not None:
        semaphore = asyncio.Semaphore(min(semaphore, len(tasks)))

    for task in tasks:

        if semaphore is not None:
            arr.append(asyncio.create_task(with_semaphore(semaphore, with_sleep(task))))
            continue
        arr.append(asyncio.create_task(with_sleep(task)))

    return await asyncio.gather(*arr)


def run(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(func)

async def with_semaphore(semaphore, func):
    async with semaphore:
        return await func


async def with_sleep(func):
    await asyncio.sleep(config.asyncio['sleep'])
    return await func
