import functools
import json
import random
import math
from collections import defaultdict
from hashlib import md5
from typing import Any, Dict, List, Match, Set, Tuple, Union


class Monad(str):
    def __init__(self, data):
        self.data = data
        str.__init__(self)

    def __getitem__(self, attr):
        try:
            return Monad(self.data[attr])
        except Exception:
            return Monad("")

    def __repr__(self):
        if not self.data:
            return ""
        else:
            return self.data >> to_json


def monad(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        rst = await func(*args, **kwargs)
        return Monad(rst)

    return inner


class pipe(object):
    def __init__(self, function):
        self.function = function
        self.rst = None
        functools.update_wrapper(self, function)

    def __rrshift__(self, other):
        return self.function(other)

    def __le__(self, other):
        if isinstance(other, pipe):
            self.rst = list(map(self.function, other.rst))
        else:
            self.rst = list(map(self.function, other))
        return self.rst

    def __call__(self, *args, **kwargs):
        return pipe(lambda x: self.function(x, *args, **kwargs))


@pipe
def to_list(data: Union[List, str, Tuple, Set]):
    return list(data)


@pipe
def to_int(data: Union[int, str, float]):
    return int(data)


@pipe
def to_dict(data: Union[List[Tuple], Dict]):
    return dict(data)


@pipe
def to_float(data: Union[int, float, str]):
    return float(data)


@pipe
def to_bool(data: Any):
    return bool(data)


@pipe
def to_str(obj):
    return str(obj)


@pipe
def join(lst: list, sep="\t") -> str:
    return sep.join(list(map(str, lst)))


@pipe
def mkey(obj, default=None, *args):
    rst = []
    for key in args:
        rst.append(obj.get(key, default))
    return rst


@pipe
def get_key_or_key(obj, keys: List[str] = [], default=None):
    rst = default
    for key in keys:
        rst = obj.get(key, None) or rst
        if rst != default:
            break
    return rst


@pipe
def mindex(lst, *args):
    return [lst[i] for i in args]


@pipe
def trim(data):
    return data.replace('"', "").replace("'", "").strip(" ")


@pipe
def group_by_range(lst, s=3, e=None):
    '''
    '''
    rtn = []
    if not e:
        # 均分
        return lst >> group_by_n(s)
    else:
        # 在一定范围内均分
        i = 0
        while i < len(lst):
            step = random.randrange(s, e)
            rtn.append(lst[i:i + step])
            i += step
    return rtn


@pipe
def group_by_key(lst: List[Dict], key: str = "") -> Dict[str, List]:
    group = defaultdict(list)
    for ele in lst:
        if isinstance(ele, dict):
            val = ele.get(key)
        else:
            val = getattr(ele, key)
        group[val].append(ele)
    return group


@pipe
def group_by_n(lst, count=4):
    '''
        [1,2,3,4,5,6,7,8]
            >>group_by_n(2)
        =>[[1,2],[3,4],[5,6],[7,8]]
    '''
    rtn = []
    for i in range(0, len(lst), count):
        rtn.append(lst[i:i + count])
    return rtn


@pipe
def group_into_n(lst, count):
    '''
    [1,2,3,4,5,6,7,8]
            >>group_into_n(2)
        =>[[1,2,3,4],[5,6,7,8]]
    '''
    rtn = []
    elen = math.ceil(len(lst) / count)
    s = i = 0
    while i < count:
        rtn.append(lst[s:s + elen])
        i += 1
        s = s + elen
    return rtn


@pipe
def group_by_sep(lst, sep=None):
    '''
        [a,b,c,sep,c,d,sep,s,e,sep,sep,u]
            >>split_by(sep)
        =>[[a,b,c],[c,d],[s,e],[u]]
    '''
    rst, tmp = [], []
    for ele in lst:
        if ele != sep:
            tmp.append(ele)
        else:
            rst.append(tmp)
            tmp = []
    if tmp:
        rst.append(tmp)
    return rst


@pipe
def head(lst: list, default=""):
    try:
        return lst[0]
    except Exception:
        return default


@pipe
def json_to_str(data: dict):
    return json.dumps(data, ensure_ascii=False)


@pipe
def mreplace(src: str, lstb: list, b="") -> str:
    for ele in lstb:
        src = src.replace(ele, b)
    return src


@pipe
def to_json(data: Union[str, bytes], encoding="utf8") -> dict:
    # 替换字符中含有的双引号
    if isinstance(data, bytes):
        data = data.decode(encoding)
        try:
            return json.loads(data)
        except Exception:
            data = data.replace('\\"', "")
            return json.loads(data)
    else:
        try:
            return json.loads(data)
        except:
            # 单引号
            return eval(data)


@pipe
def strip_group(data, trim):
    while data.startswith(trim):
        data = data[len(trim):]
    while data.endswith(trim):
        data = data[:-len(trim)]
    return data


@pipe
def to_md5(data) -> int:
    if isinstance(data, list):
        data = "".join(data)
    md = md5()
    md.update(data.encode("utf8"))
    return str(md.hexdigest())


def main():
    lst = ["ac", "ac"] >= pipe(str.replace)("a", "c")
    print(lst)
    lst = ['1', '2', '3', '4', '5'] >> mindex(1, 2, 3) >= to_int
    print(lst)


if __name__ == "__main__":
    main()
