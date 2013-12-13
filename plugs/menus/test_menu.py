from __init__ import load_menu, print_menu, default_menu, default_navigation

menus = {
    'home':{'title':'Test'},
    'event':{'order':100, 'title':'Event', 'subs':[
        {'name':'e1', 'order':300, 'title':'e1'},
        {'name':'e2', 'order':100, 'title':'e2'},
        {'name':'e3', 'title':'e3'},
    ]},
    'tasks':{'parent':'event', 'title':'t1'},
    'develop_tasks':{'parent':'event/tasks', 'title':'develop_tasks'},
}

def test_load_menu():
    """
    >>> x = load_menu(menus.items())
    >>> print_menu()
    event
        e2
        e1
        e3
        tasks
            develop_tasks
    home
    >>> print_menu('event')
    event
        e2
        e1
        e3
        tasks
            develop_tasks
    >>> print_menu('event/tasks')
    tasks
        develop_tasks
    >>> print_menu('event/tasks/develop_tasks')
    develop_tasks
    """

def test_menu():
    """
    >>> x = load_menu(menus.items())
    >>> print default_menu('event')
    <ul class="menu">
      <li><a href="#">e2</a></li>
      <li><a href="#">e1</a></li>
      <li><a href="#">e3</a></li>
      <li><a href="#">t1</a>
      <ul>
        <li><a href="#">develop_tasks</a></li>
      </ul>
      </li>
    </ul>
    <BLANKLINE>
    """

def test_menu_active():
    """
    >>> x = load_menu(menus.items())
    >>> print default_menu('event', 'tasks/develop_tasks')
    <ul class="menu">
      <li><a href="#">e2</a></li>
      <li><a href="#">e1</a></li>
      <li><a href="#">e3</a></li>
      <li><a href="#">t1</a>
      <ul>
        <li class="active"><a href="#">develop_tasks</a></li>
      </ul>
      </li>
    </ul>
    <BLANKLINE>
    >>> print default_menu('event', 'tasks/develop_tasks', id='menus', _class='test')
    <ul class="menu test" id="menus">
      <li><a href="#">e2</a></li>
      <li><a href="#">e1</a></li>
      <li><a href="#">e3</a></li>
      <li><a href="#">t1</a>
      <ul>
        <li class="active"><a href="#">develop_tasks</a></li>
      </ul>
      </li>
    </ul>
    <BLANKLINE>
    """

def test_navigation():
    """
    >>> menus = {
    ... 'main':{'subs':[
    ...     {'name':'home', 'title':'Home'},
    ...     {'name':'about', 'title':'About'},
    ... ]}
    ... }
    >>> x = load_menu(menus.items())
    >>> print default_navigation('main', 'home')
    <ul class="nav">
      <li><a href="#">About</a></li>
      <li class="active"><a href="#">Home</a></li>
    </ul>
    <BLANKLINE>
    """
