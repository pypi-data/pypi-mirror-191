class Registry:
    def __init__(self,  name=None):
        self._name = name
        self._module_dict= dict()

    @property
    def name(self):
        return self._name

    @property
    def module_dict(self):
        return self._module_dict

    def add(self, module_name=None, forece=False, module=None):
        """
        if there is input module, then will return module
        for example: add('Conv1d', module=nn.Conv1d)
        if there is no module, then will return _add
        """

        if module is not None:
            if module_name is None:
                module_name = module.__name__
            self._module_dict[module_name]= module
            return module

        def _add(inputClass):
            module_name = inputClass.__name__
            self._module_dict[module_name] = inputClass
            # print(module_name)
            # print("{} added".format(name))
            return inputClass
        return _add

    def get(self, key):
        return self._module_dict.get(key)

    def __len__(self):
        return len(self._module_dict)

    def __contains__(self, key):
        """
        help to make the class, "Registry" iterable
        """
        return self.get(key) is not None


    def __repr__(self):
        format_str = self.__class__.__name__ + \
                     f'(name={self._name}, ' \
                     f'items={self._module_dict})'
        return format_str