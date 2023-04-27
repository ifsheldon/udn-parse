import re
from abc import ABC, abstractmethod


class UDNBlock(ABC):

    @staticmethod
    @abstractmethod
    def parse(content: str):
        pass


class ExcerptBlock(UDNBlock):

    def __init__(self, name: str, content: str):
        self.name = name
        self._original_content = content
        self.content = content

    def __str__(self):
        return f"""[EXCERPT:{self.name}]\n{self.content}\n[/EXCERPT:{self.name}]"""

    def __repr__(self):
        return f"""ExcerptBlock(name = {self.name}, content = {self.content})\n"""

    @staticmethod
    def parse(content: str):
        excerpt_block_name_pattern = r"\[EXCERPT:(.*?)\]"
        excerpt_block_content_pattern = r"\[EXCERPT:.*?\]\s*(.*?)\s*\[/EXCERPT:.*?\]"
        block_names = re.findall(excerpt_block_name_pattern, content)
        block_contents = re.findall(excerpt_block_content_pattern, content, re.DOTALL)
        assert len(block_names) == len(block_contents)
        return [ExcerptBlock(n, c) for n, c in zip(block_names, block_contents)]


class ImgBlock(UDNBlock):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"![]({self.name})"

    def __repr__(self):
        return f"ImageBlock(name = {self.name})\n"

    @staticmethod
    def parse(content: str):
        img_block_pattern = r"!\[\]\((.*?)\)"
        img_names = re.findall(img_block_pattern, content)
        return [ImgBlock(x) for x in img_names]


class VarBlock(UDNBlock):

    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

    def __str__(self):
        return f"""[VAR:{self.name}]\n{self.content}\n[/VAR]"""

    def __repr__(self):
        return f"""VarBlock(name = {self.name}, content = {self.content})"""

    @staticmethod
    def parse(content: str):
        var_block_name_pattern = r"\[VAR:(.*?)\]"
        var_block_content_pattern = r"\[VAR:.*?\]\s*(.*?)\s*\[/VAR\]"
        block_names = re.findall(var_block_name_pattern, content)
        block_contents = re.findall(var_block_content_pattern, content, re.DOTALL)
        assert len(block_names) == len(block_contents)
        return list(map(lambda x, y: VarBlock(x, y), block_names, block_contents))
