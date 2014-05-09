import os
from optparse import make_option
from uliweb.core.commands import Command, get_input, get_answer
from uliweb.core.template import template_file

class MenuCommand(Command):
    name = 'menu'
    help = 'Display menu structure. If no menu_name, then display all menus.'
    args = '<menu_name>'

    def handle(self, options, global_options, *args):
        from uliweb import settings
        from . import print_menu
        import sys
        
        self.get_application(global_options)
        if not args:
            args = [None]
        for x in args:
            print_menu(x, title=True, verbose=global_options.verbose)