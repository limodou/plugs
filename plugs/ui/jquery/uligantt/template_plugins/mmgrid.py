def call(pagination=True, treegrid=True):
    a = []
    a.append('uligantt/mmGrid.css')
    a.append('uligantt/mmGrid.js')
    if treegrid:
        a.append('uligantt/uliTreeGrid.css')
        a.append('uligantt/uliTreeGrid.js')
    
    if pagination:
        a.append('uligantt/mmPaginator.css')
        a.append('uligantt/mmPaginator.js')
        a.append('uligantt/scrolling.js')
    return {'toplinks':a, 'depends':['jquery', 'json2']}
