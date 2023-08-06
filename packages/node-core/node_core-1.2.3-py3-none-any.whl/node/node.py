


class Node:
    _parent = None

    class PointerError(AttributeError):
        pass

    def __init__(self, name: str, *children: list, **kwargs: dict):
        self.set_name(name)
        self.set_index(kwargs.get('index', 0))
        self.set_kwargs(kwargs)
        self.set_view([node._name for node in children])
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        for node in children:
            node.set_parent(self)
            setattr(self, node.get_name(), node)

    def __call__(self, *args, **kwargs):
        index, arg = Node._parse_first_arg(args)
        if index:
            self.set_name(arg)
        self.update_kwargs(kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        for node in args[index:]:
            self.add_child(node)
        return self

    def __iter__(self):
        for node_name in self.get_view():
            yield self.getattr(node_name)

    def __getitem__(self, pointer: str):
        if pointer is None:
            return

        if pointer[0] == '/':
            attr = self.get_root()
            pointer = pointer[1:]
        else:
            attr = self

        for attr_name in pointer.split('/'):
            if not attr_name or attr_name == '.':
                continue
            elif attr_name == '..':
                attr = attr.get_parent()
            else:
                attr = attr.getattr(attr_name)
        return attr

    def __setitem__(self, pointer: str, value: any):
        if pointer is None:
            return

        if pointer[0] == '/':
            attr = self.get_root()
            pointer = pointer[1:]
        else:
            attr = self

        pointer_split = pointer.split('/')
        final_attr = pointer_split[-1]

        for attr_name in pointer_split[:-1]:
            if not attr_name or attr_name == '.':
                continue
            elif attr_name == '..':
                attr = attr.get_parent()
            else:
                attr = attr.getattr(attr_name)

        attr.setattr(final_attr, value)

    def __delitem__(self, pointer: str):
        self[pointer].destruct()

    def __repr__(self):
        return f'<{self.get_pointer()}>'

    def __truediv__(self, pointer: str):
        return self[pointer]

    def __floordiv__(self, pointer: str):
        return self.get_root()[pointer]

    def __add__(self, nodes: list):
        self(*nodes)
        return self

    def __sub__(self, child_name: str):
        self.remove_child(child_name)
        return self

    def __mod__(self, key: callable):
        yield from self.get_children(key=key)

    def __str__(self) -> str:
        return self.get_pointer()

    def __invert__(self) -> str:
        return self.get_name()

    @staticmethod
    def _parse_first_arg(args):
        arg = next(iter(args), None)
        if isinstance(arg, Node):
            return False, arg
        return True, arg

    def show(self):
        if self.get_parent():
            if self._name not in self.get_parent().get_view():
                self.get_parent()._view.append(self._name)

    def hide(self):
        if self.get_parent():
            if self._name in self.get_parent().get_view():
                self.get_parent()._view.remove(self._name)

    def check_pointer(self, pointer: str) -> bool:
        if pointer is None:
            False

        if pointer[0] == '/':
            attr = self.get_root()
            pointer = pointer[1:]
        else:
            attr = self

        for attr_name in pointer.split('/'):
            if not attr_name or attr_name == '.':
                continue
            elif attr_name == '..':
                attr = attr.get_parent()
            else:
                if not hasattr(attr, attr_name):
                    return False
                else:
                    attr = attr.getattr(attr_name)
        return True

    @property
    def in_view(self) -> bool:
        node = self
        while node.get_parent() is not None:
            if node._name not in node.get_parent().get_view():
                return False
            node = node.get_parent()
        return True

    def initattr(self, attr: str, value: any = None):
        self._kwargs[attr] = value
        if not hasattr(self, attr):
            setattr(self, attr, value)
        elif self[attr] is None:
            setattr(self, attr, value)

    def resetattr(self, attr: str):
        setattr(self, attr, self.get_kwargs().get(attr))

    def setattr(self, attr: str, value: any):
        setattr(self, attr, value)

    def getattr(self, attr: str) -> any:
        try:
            return getattr(self, attr)
        except AttributeError:
            raise self.PointerError(f'{self.__class__.__name__}:{self.get_pointer()} has no child "{attr}"')

    def cascade(self, *signals):
        for signal in signals:
            self.get_root()[signal](self)
        for child in self:
            child.cascade(*signals)

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str):
        self._name = value

    def get_kwargs(self) -> dict:
        return self._kwargs

    def set_kwargs(self, value: dict):
        self._kwargs = value

    def update_kwargs(self, value: dict):
        self._kwargs.update(value)

    def set_parent(self, node):
        self._parent = node

    def sort_view(self):
        self.set_view([node.get_name() for node in sorted(self.get_children(), key=lambda node: node._index)])

    def set_index(self, value: int):
        self._index = value

    def get_index(self) -> int:
        return self._index

    def get_children(self, key=lambda node: True):
        return list(filter(key, self))

    def add_child(self, child, index=None):
        if index is None:
            index = len(self.get_view())
        child.set_parent(self)
        self[child.get_name()] = child
        self._view.insert(index, child.get_name())
        self.sort_view()

    def clear_children(self, key=lambda node: True):
        for node in list(filter(key, self)):
            delattr(self, node.get_name())
            if node.get_name() in self.get_view():
                self.remove_from_view(node.get_name())

    def remove_child(self, child_name):
        if child_name in self.get_view():
            self.remove_from_view(child_name)
        delattr(self, child_name)

    def get_parent(self):
        return self._parent

    def get_root(self):
        if self.get_parent() is None:
            return self

        root = None
        next_node = self.get_parent()
        while root is None:
            if next_node.get_parent() is None:
                root = next_node
            else:
                next_node = next_node.get_parent()

        return root

    def get_pointer(self) -> str:
        next_node = self.get_parent()
        pointer_string = ''
        while next_node:
            if next_node.get_parent():
                pointer_string = f'/{next_node.get_name()}{pointer_string}'
            next_node = next_node.get_parent()
        pointer_string += f'/{self.get_name()}'

        return pointer_string

    def set_view(self, new_view: list):
        self._view = new_view

    def append_in_view(self, node_name: str):
        self._view.append(node_name)

    def insert_in_view(self, index, node_name: str):
        self._view.insert(index, node_name)

    def remove_from_view(self, node_name: str):
        self._view.remove(node_name)

    def get_view(self) -> list:
        return self._view

    def destruct(self):
        if self.get_parent():
            self['../remove_child'](self.get_name())

    def reset(self):
        self.__dict__.update(self.get_kwargs())

    def __fit__(self):
        for node in self:
            node.__fit__()

    async def __loop__(self):
        for node in self:
            await node.__loop__()

    def __run__(self):
        for node in self:
            node.__run__()
