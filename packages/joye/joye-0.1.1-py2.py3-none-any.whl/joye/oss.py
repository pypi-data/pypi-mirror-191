#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把OSS对象封装成文件操作

open_data: 打开数据对象存储文件
open_strategy: 打开策略对象存储文件
"""
import enum
import queue
from concurrent.futures import Future, ThreadPoolExecutor
from typing import BinaryIO

import oss2

from .consts import (
    DATA_ACCESS_KEY_ID,
    DATA_ACCESS_KEY_SECRET,
    DATA_BUCKET,
    DATA_ENDPOINT,
    DATA_MODE,
    STRATEGY_ACCESS_KEY_ID,
    STRATEGY_ACCESS_KEY_SECRET,
    STRATEGY_BUCKET,
    STRATEGY_ENDPOINT,
    STRATEGY_MODE,
)
from .logger import logger


class BucketType(str, enum.Enum):
    DATA = "data"
    STRATEGY = "strategy"


class OpenMode(str, enum.Enum):
    BINARY_READ = "rb"
    BINARY_WRITE = "wb"


class BlockingIO:
    def __init__(self):
        self.queue = queue.Queue()
        self.future: Future

    def set_future(self, future: Future):
        self.future = future

    def read(self, n: int) -> bytes:
        data = self.queue.get()
        return data

    def write(self, data: bytes | str):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.queue.put(data)

    def close(self):
        self.queue.put(b"")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        self.future.result()


class OSSFile:
    def __init__(self, path: str, bucket_type: str):
        self.path = path

        match bucket_type:
            case BucketType.DATA:
                key, secret = DATA_ACCESS_KEY_ID, DATA_ACCESS_KEY_SECRET
                endpoint, bucket = DATA_ENDPOINT, DATA_BUCKET
                if DATA_MODE == "mock":
                    self.path = "mock/" + path
            case BucketType.STRATEGY:
                key, secret = STRATEGY_ACCESS_KEY_ID, STRATEGY_ACCESS_KEY_SECRET
                endpoint, bucket = STRATEGY_ENDPOINT, STRATEGY_BUCKET
                if STRATEGY_MODE == "mock":
                    self.path = "mock/" + path
            case default:
                raise NotImplementedError(
                    f"bucket_type `{bucket_type}` not implemented"
                )

        self.auth = oss2.Auth(key, secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket)
        self.executor = ThreadPoolExecutor(2)

    def open_file(self, mode) -> BinaryIO:
        match mode:
            case OpenMode.BINARY_READ:
                return self.bucket.get_object(self.path)
            case OpenMode.BINARY_WRITE:
                iorw = BlockingIO()
                putter = self.executor.submit(self.bucket.put_object, self.path, iorw)
                iorw.set_future(putter)
                return iorw
            case default:
                raise NotImplementedError(
                    f"open mode should be `rb` or `wb`, got {mode}"
                )


def open_data(path: str, mode: OpenMode = OpenMode.BINARY_READ) -> BinaryIO:
    """
    打开数据OSS中Path, 返回一个FileObject
    """
    of = OSSFile(path, bucket_type=BucketType.DATA)
    return of.open_file(mode)


def open_strategy(path: str, mode: OpenMode = OpenMode.BINARY_READ) -> BinaryIO:
    """
    打开策略OSS中的Path, 返回一个FileObject
    """
    of = OSSFile(path, bucket_type=BucketType.STRATEGY)
    return of.open_file(mode)
