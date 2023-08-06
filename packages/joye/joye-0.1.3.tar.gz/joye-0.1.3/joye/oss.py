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
from typing import BinaryIO, cast

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
                raise NotImplementedError(f"bucket_type `{bucket_type}` not implemented")

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
                raise NotImplementedError(f"open mode should be `rb` or `wb`, got {mode}")

    def list_folder(self, start_after: str = "", end_before: str = "") -> list[str]:
        result: list[str] = []
        continuation_token = ""

        while True:
            resp = self.bucket.list_objects_v2(
                prefix=self.path,
                continuation_token=continuation_token,
                start_after=start_after,
            )

            assert (
                200 <= resp.status < 300
            ), f"list_objects error, prefix: {self.path}, start_after: {start_after}, resp: {resp.resp}"

            for obj in cast(list[oss2.models.SimplifiedObjectInfo], resp.object_list):
                key = cast(str, obj.key)
                if DATA_MODE == "mock" and key.startswith("mock/"):
                    key = key[5:]
                if end_before and key >= end_before:
                    return result
                if key:
                    result.append(key)

            continuation_token = resp.next_continuation_token

            if not resp.is_truncated:
                break

        return result


def open_data(path: str, mode: OpenMode = OpenMode.BINARY_READ) -> BinaryIO:
    """
    打开数据OSS中Path, 返回一个FileObject
    """
    of = OSSFile(path, bucket_type=BucketType.DATA)
    return of.open_file(mode)


def list_folder_data(folder: str, start_after: str = "", end_before: str = "") -> list[str]:
    """
    列表数据OSS中的folder, 返回文件列表
    """
    of = OSSFile(folder, bucket_type=BucketType.DATA)
    return of.list_folder(start_after=start_after, end_before=end_before)


def open_strategy(path: str, mode: OpenMode = OpenMode.BINARY_READ) -> BinaryIO:
    """
    打开策略OSS中的Path, 返回一个FileObject
    """
    of = OSSFile(path, bucket_type=BucketType.STRATEGY)
    return of.open_file(mode)

def list_folder_strategy(folder: str, start_after: str = "", end_before: str = "") -> list[str]:
    """
    列表策略OSS中的folder, 返回文件列表
    """
    of = OSSFile(folder, bucket_type=BucketType.STRATEGY)
    return of.list_folder(start_after=start_after, end_before=end_before)
