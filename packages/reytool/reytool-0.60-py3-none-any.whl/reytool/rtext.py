# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 13:18:24
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's print methods
"""


from typing import Any, List, Literal, Optional
import pprint
from urwid import old_str_util

from .rbasic import error, get_name


def monkey_patch_format() -> None:
    """
    Based on module pprint.pformat, modify the chinese width judgment.
    """

    def _format(_self, object, stream, indent, allowance, context, level):
        objid = id(object)
        if objid in context:
            stream.write(pprint._recursion(object))
            _self._recursive = True
            _self._readable = False
            return
        rep = _self._repr(object, context, level)
        max_width = _self._width - indent - allowance
        width = get_width(rep)
        if width > max_width:
            p = _self._dispatch.get(type(object).__repr__, None)
            if p is not None:
                context[objid] = 1
                p(_self, object, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
            elif isinstance(object, dict):
                context[objid] = 1
                _self._pprint_dict(object, stream, indent, allowance,
                                context, level + 1)
                del context[objid]
                return
        stream.write(rep)

    # Modify the chinese width judgment.
    pprint.PrettyPrinter._format = _format

monkey_patch_format()

def split_text(text: str, length: int, by_width: bool = False) -> List:
    """
    Split text by length or not greater than display width.
    """

    texts = []
    if by_width:
        str_group = []
        str_width = 0
        for char in text:
            char_width = get_width(char)
            str_width += char_width
            if str_width > length:
                string = "".join(str_group)
                texts.append(string)
                str_group = [char]
                str_width = char_width
            else:
                str_group.append(char)
        string = "".join(str_group)
        texts.append(string)
    else:
        test_len = len(text)
        split_n = test_len // length
        if test_len % length:
            split_n += 1
        for n in range(split_n):
            start_indxe = length * n
            end_index = length * (n + 1)
            text_group = text[start_indxe:end_index]
            texts.append(text_group)
    return texts

def get_width(text: str) -> int:
    """
    Get text display width.
    """
    
    total_width = 0
    for char in text:
        char_unicode = ord(char)
        char_width = old_str_util.get_width(char_unicode)
        total_width += char_width
    return total_width

def fill_width(text: str, char: str, width: int, align: Literal["left", "right", "center"] = "right") -> str:
    """
    Text fill character by display width.

    Parameters
    ----------
    text : Fill text.
    char : Fill character.
    width : Fill width.
    align : Align orientation.
        - Literal['left'] : Fill right, align left.
        - Literal['right'] : Fill left, align right.
        - Literal['center'] : Fill both sides, align center.
    
    Returns
    -------
    Text after fill.
    """

    if get_width(char) != 1:
        error("parameter char value error", ValueError)
    text_width = get_width(text)
    fill_width = width - text_width
    if fill_width > 0:
        if align == "left":
            new_text = "%s%s" % (char * fill_width, text)
        elif align == "right":
            new_text = "%s%s" % (text, char * fill_width)
        elif align == "center":
            fill_width_left = int(fill_width / 2)
            fill_width_right = fill_width - fill_width_left
            new_text = "%s%s%s" % (char * fill_width_left, text, char * fill_width_right)
        else:
            error("parameter align value error", ValueError)
    else:
        new_text = text
    return new_text

def print_frame(*contents: Any, title: Optional[str] = None, width: int = 100, frame: Literal["full", "half", "plain"] = "full") -> None:
    """
    Print contents and frame.

    Parameters
    ----------
    contents : Print contents.
    title : Print frame title.
        - None : No title.
        - str : Use this value as the title.

    width : Print frame width.
    frame : Frame type.
        - Literal['full'] : Build with symbol '═╡╞║╠╣╔╗╚╝', and content not can exceed the frame.
            When throw error, then frame is 'half' type.
        - Literal['half'] : Build with symbol '═╡╞', and content can exceed the frame.
        - Literal['plain'] : Build with symbol '=|', and content can exceed the frame.
    """
    
    if title == None or len(title) > width - 6:
        title = ""
    if frame == "full":
        if title != "":
            title = f"╡ {title} ╞"
        width_in = width - 2
        _contents = []
        try:
            for content in contents:
                content_str = str(content)
                pieces_str = content_str.split("\n")
                content_str = [
                    "║%s║" % fill_width(line_str, " ", width_in)
                    for piece_str in pieces_str
                    for line_str in split_text(piece_str, width_in, True)
                ]
                content = "\n".join(content_str)
                _contents.append(content)
        except:
            frame_top = fill_width(title, "═", width, "center")
            frame_split = "═" * width
            frame_bottom = "═" * width
            _contents = contents
        else:
            frame_top = "╔%s╗" % fill_width(title, "═", width_in, "center")
            frame_split = "╠%s╣" % ("═" * width_in)
            frame_bottom = "╚%s╝" % ("═" * width_in)
    elif frame == "half":
        if title != "":
            title = f"╡ {title} ╞"
        frame_top = fill_width(title, "═", width, "center")
        frame_split = "═" * width
        frame_bottom = "═" * width
        _contents = contents
    elif frame == "plain":
        if title != "":
            title = f"| {title} |"
        frame_top = fill_width(title, "=", width, "center")
        frame_split = "=" * width
        frame_bottom = "=" * width
        _contents = contents
    print(frame_top)
    for index, content in enumerate(_contents):
        if index != 0:
            print(frame_split)
        print(content)
    print(frame_bottom)

def rprint(
        *contents: Any,
        title: Optional[str] = None,
        width: int = 100,
        frame: Literal["full", "half", "plain"] = "full",
        format: bool = True
    ) -> None:
    """
    Print formatted contents and contents information.

    Parameters
    ----------
    contents : Print contents.
    title : Print frame title.
        - None : No title.
        - str : Use this value as the title.

    width : Print frame width.
    frame : Frame type.
        - Literal['full'] : Build with symbol '═╡╞║╠╣╔╗╚╝', and content not can exceed the frame.
            When throw error, then frame is 'half' type.
        - Literal['half'] : Build with symbol '═╡╞', and content can exceed the frame.
        - Literal['plain'] : Build with symbol '=|', and content can exceed the frame.
    
    format : Whether format data of type list or tuple or dict or set.
    """

    if title == None:
        titles = get_name(contents)
        if titles != None:
            titles = [title if title[:1] != "'" else "" for title in titles]
            if set(titles) != {""}:
                title = " │ ".join(titles)
    if format:
        contents = [
            pprint.pformat(content, width=width, sort_dicts=False)
            if type(content) in [list, tuple, dict, set]
            else content
            for content in contents
        ]
    print_frame(*contents, title=title, width=width, frame=frame)