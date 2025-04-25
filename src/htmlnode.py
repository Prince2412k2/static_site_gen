from typing import List, Optional, Type


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[list] = children
        self.props: Optional[dict] = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return "".join(f' {key}="{val}"' for key, val in self.props.items())
        return ""

    def __repr__(self) -> str:
        return f"HTMLNode(\n\ttag={self.tag}, \n\tvalue={self.value}, \n\tchildren={self.children}, \n\tprops={self.props}\n\t)"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value in LeafNode")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(\n\ttag={self.tag}, \n\tvalue={self.value}, \n\tprops={self.props}\n\t)"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children=[], props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is a reqired field in ParentNode")
        if not self.children:
            raise ValueError("children is a reqired field in ParentNode")
        return f"<{self.tag}{self.props_to_html()}>{''.join(i.to_html() for i in self.children)}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode(\n\ttag={self.tag}, \n\tchildren={self.children}, \n\tprops={self.props}\n\t)"


def main():
    props = {"href": "https://www.google.com", "target": "_blank", "class": "link"}
    node = HTMLNode(props=props)
    print(node.props_to_html())


if __name__ == "__main__":
    main()
