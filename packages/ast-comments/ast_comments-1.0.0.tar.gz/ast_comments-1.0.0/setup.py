# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ast_comments']
setup_kwargs = {
    'name': 'ast-comments',
    'version': '1.0.0',
    'description': '',
    'long_description': '# ast-comments\n\nAn extension to the built-in `ast` module. \nFinds comments in source code and adds them to the parsed tree.\n\n## Installation\n```\npip install ast-comments\n```\n\n## Usage\n\nThere is no difference in usage between `ast` and `ast-comments`\n```\n>>> from ast_comments import *\n>>> tree = parse("hello = \'hello\' # comment to hello")\n```\nParsed tree is instance of the original ast.Module object.\nThe only difference is there is a new type of tree node: Comment\n```\n>>> tree\n<_ast.Module object at 0x7ffba52322e0>\n>>> tree.body\n[<ast_comments.Comment object at 0x10c1b6160>, <_ast.Assign object at 0x10bd217c0>]\n>>> tree.body[0].value\n\'# comment to hello\'\n>>> dump(tree)\n"Module(body=[Comment(value=\'# comment to hello\'), Assign(targets=[Name(id=\'hello\', ctx=Store())], value=Constant(value=\'hello\', kind=None), type_comment=None)], type_ignores=[])"\n```\nIf you have python3.9 or above it\'s also possible to unparse the tree object with its comments preserved.\n```\n>>> print(unparse(tree))\n# comment to hello\nhello = \'hello\'\n```\nMore examples can be found in test_parse.py and test_unparse.py.\n\n## Notes\n1. Right now it is assumed that there is no difference between inlined comments and regular. \nAll inlined comments become regular after the tree object is unparsed.\n\n2. Inlined comments for class- (def-, if-, ...) block shift "inside" body of the corresponding block:\n    ```\n    >>> source = """class Foo: # c1\n    ...     pass\n    ... """\n    >>> unparse(parse(source))\n    >>> print(unparse(parse(source)))\n    class Foo:\n        # c1\n        pass\n    ```\n\n## Contributing\nYou are welcome to open an issue or create a pull request',
    'author': 'Dmitry Makarov',
    'author_email': 'dmtern0vnik@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/t3rn0/ast-comments',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
