# -*- coding: utf8 -*-
from collections import defaultdict
from os import path
from jinja2 import Environment, PackageLoader


class CommandDoc(object):
    def __init__(self, name, output, mapper, module='doom',
                 template_module='template',
                 template_item_name='item.rst',
                 template_index_name='index.rst',
                 module_path_prefix=''):
        self.name = name
        self.output = output
        self.module_path_prefix = module_path_prefix

        self.tree = self.build_tree(mapper)
        self.env = Environment(loader=PackageLoader(module, template_module))
        self.template_item = self.env.get_template(template_item_name)
        self.template_index = self.env.get_template(template_index_name)

    @staticmethod
    def build_tree(mapper):
        store = defaultdict(defaultdict)
        for name, command in mapper.iteritems():
            module_name, action = name.split('.')
            store[module_name][action] = '.{module}.{name}'.format(
                module=command.__module__,
                name=command.__name__
            )
        return store

    @staticmethod
    def under_line(name, line):
        return line * (len(name) + 4)

    def render_item(self, module, name_cls):
        return self.template_item.render(
            module=module,
            name_cls=name_cls,
            module_path_prefix=self.module_path_prefix,
            under_line=self.under_line
        )

    def render_index(self, name, modules):
        return self.template_index.render(
            name=name,
            modules=modules,
            under_line=self.under_line
        )

    def make_file(self, module):
        return file(path.join(self.output, module + '.rst'), 'w+')

    def make_index(self, name, modules):
        self.make_file('index').write(self.render_index(name, modules))

    def make_files(self):
        for module, name_cls in self.tree.iteritems():
            f = self.make_file(module)
            f.write(self.render_item(module, name_cls))
        self.make_index(self.name, self.tree.keys())
