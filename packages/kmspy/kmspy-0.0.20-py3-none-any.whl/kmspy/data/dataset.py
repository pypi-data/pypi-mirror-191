from __future__ import annotations


from collections import defaultdict
import copy
from itertools import product
import logging
import random
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Set

from .prefetch_generator import PrefetchGenerator
from ..utils import is_available, width
from ..utils._proxy_class import _proxy_class

import numpy as np


logger = logging.getLogger(__name__)


class Dataset:
    """
    """
    
    def __init__(self, data: List[Dict[str, Any]] = None, *args, **kwargs) -> None:
        self._has_changed = False
        self.data = _proxy_class(list, self)()
        if data is None:
            pass
        else:
            if isinstance(data, list):
                if data:
                    if isinstance(data[0], dict):
                        pass
                    else:
                        raise(ValueError("각각의 요소는 dict 타입이어야 합니다."))
            else:
                raise(ValueError("data는 list 타입이어야 합니다."))

        self.data.extend(data) if data is not None else None
        self._num_data = None
        self._counts = None
    
    def update_states(func):
        def wrapper(self, *args, **kwargs):
            if self._num_data is None or self._counts is None or self._has_changed:
                self._get_counts()
                self._num_data = len(self.data)
                self._has_changed = False
            return func(self, *args, **kwargs)
        return wrapper            

    def shuffle(self):
        random.shuffle(self.data)

    def append(self, data: Dict[str, Any]) -> None:
        self.data.append(data)

    def drop(self, condition: function) -> Dataset:
        return self.filter(lambda x: not condition(x))

    def filter(self, condition: function) -> Dataset:
        return Dataset(list(filter(condition, self.data)))

    def merge(self, key: str, values: Union[List[str], Tuple[str]], sort: bool = True, remain: bool = False, prefix: str = "old") -> Dataset:
        if isinstance(values, (list, tuple)):
            if sort:
                values = sorted([str(v) for v in values])
            new_values = "+".join(values)
            new_data = [{k: (new_values if (key == k and d[k] in values) else d[k]) for k in d.keys()} for d in self.data]
            if remain:
                for td, d in zip(new_data, self.data):
                    td[f"{prefix}_{key}"] = d[key]
            return Dataset(new_data)
        else:
            raise TypeError("unsupported operand type(values) for merge")

    def _get_counts(self):
        _counts = defaultdict(lambda: defaultdict(int))
        for d in self.data:
            for k, v in d.items():
                _counts[k][v] += 1
        self._counts = {k1: dict(v1) for k1, v1 in _counts.items()}

    @update_states
    def counts(self, keys: Optional[Union[List[str], Tuple[str], Set[str], str]] = None):
        if keys is not None and isinstance(keys, str):
            keys = set([keys])
        if keys is not None:
            tmp = {}
            for k in keys:
                tmp[k] = self._counts[k]
            return tmp
        else:
            return self._counts

    def combination_counts(self, keys: Union[List[str], Tuple[str], Set[str]], views: Optional[Union[List[str], Tuple[str], Set[str], str]] = None) -> List[Dict[str, Any]]:
        def _cond(keys, values):
            def _wrapper(data):
                for k, v in zip(keys, values):
                    if data[k] == v:
                        pass
                    else:
                        b = False
                        break
                else:
                    b = True
                return b
            return _wrapper

        if not isinstance(keys, list):
            keys = list(keys)
        
        if views is not None:
            if isinstance(views, str):
                views = [views]
                
        _kvs = {k: list(v.keys()) for k, v in self.counts(keys).items() if k in keys}

        combinations = _kvs[keys[0]]
        for i in range(len(keys)-1):
            combinations = ["\x1b".join(p) for p in product(combinations, _kvs[keys[i+1]])]
        combinations = [c.split("\x1b") for c in combinations]

        _counts = []
        for c in combinations:
            ds = self.filter(_cond(keys, c))
            if ds.num_data > 0:
                _tmp = {k: v for k, v in zip(keys, c)}
                if views:
                    _ds_counts = ds.counts()
                    for v in views:
                        _tmp[v] = list(set(_ds_counts[v]))
                _counts.append(_tmp)
                _tmp["count"] = ds.num_data
        return _counts
        
    def print_counts(self, max_display: int = 10, keys: Optional[Union[List[str], Tuple[str], Set[str], str]] = None, print_all: bool = False):
        if print_all:
            max_display = int(1e10)
        _warn = True
        _counts = self.counts(keys)
        _repr = []
        for k, v in _counts.items():
            _tmp = []
            for _i, (_k, _v) in enumerate(v.items()):
                if _i+1 == max_display+1:
                    if not print_all and _warn:
                        logger.warning(f"표시할 요소의 개수가 {max_display:d}개를 초과합니다. 모든 요소를 표시하려면 'print_all=True' 옵션을 사용하세요.")
                        _warn = False
                    _tmp.append("...")
                    break
                _tmp.append(f"{_k if _v == 1 else f'{_k}({_v})'}")
            _repr.append(f"{k}: {', '.join(_tmp)}")
        _repr = "\n".join(_repr)
        _repr = re.sub(r"^", " " * 4, _repr, 0, re.M)
        print(f"Dataset: {self.num_data}\n{_repr}")

    def __add__(self, other: Dataset) -> Dataset:
        cls = Dataset()
        cls.data.extend(copy.deepcopy(self.data))
        cls.data.extend(copy.deepcopy(other.data))
        return cls

    def __radd__(self, other: Dataset) -> Dataset:
        if not isinstance(other, Dataset):
            other = Dataset()
        return self + other

    def __getitem__(self, index: Union[int, slice]) -> Dataset:
        cls = Dataset()
        data = self.data[index]
        if isinstance(data, dict):
            cls.data.append(data)
        else:
            cls.data.extend(data)
        return cls

    def __len__(self) -> int:
        return self.num_data

    @property
    @update_states
    def num_data(self):
        return self._num_data

    def __repr__(self):
        return f"Dataset: {self.num_data}\n"

    def __iter__(self):
        return iter(self.data)


class DataLoader:
    def __init__(self, dataset: Dataset, shuffle: bool = False, batch_size: int = 1, collate_fn: Optional[Callable] = None, prefetch_factor: int = 1, num_workers: int = 1, format: Optional[str] = None, padding_value: int = 0, **kwargs) -> None:
        self.dataset = dataset
        self._shuffle = shuffle
        self._batch_size = batch_size
        self._collate_fn = collate_fn
        self._prefetch_factor = prefetch_factor
        self._num_workers = num_workers
        self.set_format(format)
        self._padding_value = padding_value

    def make_gen(self):
        if hasattr(self, "_gen"):
            if isinstance(self._gen, PrefetchGenerator) and self._gen._is_running:
                # 실행 중
                pass
            else:
                # stop된 상태
                self._gen = PrefetchGenerator(self.dataset.data, num_prefetch=self._prefetch_factor*self._batch_size, num_workers=self._num_workers, shuffle=self._shuffle, processing_func=self._collate_fn, name="DataLoader", start=True)
        else:
            # 최초 생성
            self._gen = PrefetchGenerator(self.dataset.data, num_prefetch=self._prefetch_factor*self._batch_size, num_workers=self._num_workers, shuffle=self._shuffle, processing_func=self._collate_fn, name="DataLoader", start=True)

    def set_format(self, format):
        self._format = format if format in {"tf", "tensorflow", "torch", "pytorch"} else "numpy"
        if self._format in {"tf", "tensorflow"}:
            if is_available("tensorflow"):
                import tensorflow as tf
            else:
                import tensorflow as tf  # raise
        elif self._format in {"torch", "pytorch"}:
            if is_available("torch"):
                import torch
            else:
                import torch  # raise

    def as_format(self, batch):
        if is_available("numpy"):
            ranks = [len(b) for b in batch]
            keys = [list(b.keys()) for b in batch]
            types = [[type(_b) for _b in b.values()] for b in batch]
            rank = np.unique(ranks)
            if len(rank) == 1:
                rank = rank[0]
                keys = keys[0]
                types = types[0]
                datas = [[] for _ in range(rank)]
                for b in batch:
                    for i in range(rank):
                        datas[i].append(b[keys[i]])
                for i, data in enumerate(datas):
                    if types[i] in {np.ndarray, list, tuple, int, float}:
                        max_shape = np.amax(np.array([np.shape(d) if hasattr(d, "__len__") else 1 for d in data]), axis=0)
                        min_shape = np.amin(np.array([np.shape(d) if hasattr(d, "__len__") else 1 for d in data]), axis=0)
                        if np.all(max_shape == min_shape):
                            datas[i] = np.array(data)
                        else:
                            padded_begin = np.zeros(max_shape.shape).astype(np.int32)
                            datas[i] = np.array([np.pad(d, np.stack((padded_begin, max_shape - np.shape(d))).T, constant_values=self._padding_value) for d in data])
                    elif types[i] is dict:
                        tmp_dict = {k: [] for k in data[0].keys()}
                        for d in data:
                            for k, v in d.items():
                                tmp_dict[k].append(v)
                        datas[i] = tmp_dict
                datas = {k: v for k, v in zip(keys, datas)}
            else:
                raise ValueError("collate_fn에서 출력하는 데이터의 개수가 동일하지 않습니다.")
        else:
            raise ModuleNotFoundError("numpy")
        if self._format == "tf":
            if is_available("tensorflow"):
                import tensorflow as tf
                for k, v in datas.items():
                    if isinstance(v, np.ndarray):
                        datas[k] = tf.convert_to_tensor(v)
            else:
                raise ModuleNotFoundError("tensorflow")
        elif self._format == "torch":
            if is_available("torch"):
                import torch
                for k, v in datas.items():
                    if isinstance(v, np.ndarray):
                        datas[k] = torch.tensor(v)
            else:
                raise ModuleNotFoundError("torch")
        return datas

    def __next__(self):
        data = []
        for _ in range(self._batch_size):
            try:
                data.append(next(self._gen))
            except StopIteration:
                self._gen.stop()
                if data:
                    return self.as_format(data)
                else:
                    raise StopIteration
        return self.as_format(data)

    def __iter__(self):
        self.make_gen()
        return self

    def __len__(self):
        return self.dataset.num_data//self._batch_size + (0 if self.dataset.num_data%self._batch_size == 0 else 1)