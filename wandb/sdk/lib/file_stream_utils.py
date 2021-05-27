import wandb


if wandb.TYPE_CHECKING:
    from typing import Dict, Iterable


def split_files(files: Dict[str, Dict], max_mb: int = 10) -> Iterable[Dict[str, Dict]]:
    """
    Splits a files dict (see `files` arg) into smaller dicts of at most `MAX_MB` size.
    This method is used in `FileStreamAPI._send()` to limit the size of post requests sent
    to wandb server.

    Arguments:
    files (dict): `dict` of form {file_name: {'content': ".....", 'offset': 0}}
    `max_mb`: max size for chunk in MBs
    """
    current_volume = {}
    current_size = 0
    max_size = max_mb * 1024 * 1024

    def _str_size(x):
        return len(x) if isinstance(x, bytes) else len(x.encode("utf-8"))

    def _file_size(file):
        size = file.get("_size")
        if size is None:
            size = 0
            content = file["content"]
            for i in range(file["start"], file["end"]):
                size += _str_size(content[i])
            file["_size"] = size
        return size

    def _split_file(file, num_lines):
        f1 = file.copy()
        f1["end"] = f1["start"] + num_lines
        f2 = file.copy()
        f2["start"] += num_lines
        f2["_size"] = file["_size"] - _file_size(f1)
        return f1, f2

    def _num_lines_from_num_bytes(file, num_bytes):
        size = 0
        num_lines = 0
        content = file["content"]
        start = file["start"]
        end = file["end"]
        while start + num_lines < end:
            size += _str_size(content[start + num_lines])
            if size > num_bytes:
                break
            num_lines += 1
        return num_lines

    def _get_content(file):
        c = file["content"]
        s = file["start"]
        e = file["end"]
        if s == 0 and e == len(c):
            return c
        return c[s:e]

    files_stack = [
        {
            "name": k,
            "offset": v["offset"],
            "content": v["content"],
            "start": 0,
            "end": len(v["content"]),
        }
        for k, v in files.items()
    ]

    while files_stack:
        f = files_stack.pop()
        # For each file, we have to do 1 of 4 things:
        # - Add the file as such to the current volume if possible.
        # - Split the file and add the first part to the current volume and push the second part back onto the stack.
        # - If that's not possible, check if current volume is empty:
        # - If empty, add first line of file to current volume and push rest onto stack (This volume will exceed MAX_MB).
        # - If not, push file back to stack and yield current volume.
        fsize = _file_size(f)
        rem = max_size - current_size
        if fsize <= rem:
            current_volume[f["name"]] = {
                "offset": f["offset"],
                "content": _get_content(f),
            }
            current_size += fsize
        else:
            num_lines = _num_lines_from_num_bytes(f, rem)
            if not num_lines and not current_volume:
                num_lines = 1
            if num_lines:
                f1, f2 = _split_file(f, num_lines)
                current_volume[f1["name"]] = {
                    "offset": f1["offset"],
                    "content": _get_content(f),
                }
                files_stack.append(f2)
                yield current_volume
                current_volume = {}
                current_size = 0
                continue
            else:
                files_stack.append(f)
                yield current_volume
                current_volume = {}
                current_size = 0
                continue
        if current_size >= max_size:
            yield current_volume
            current_volume = {}
            current_size = 0
            continue

    if current_volume:
        yield current_volume
