#coding=utf8

def create_pagination(url, total, page, rows, length=None, 
        total_message=None, first=None, next=None, prev=None, last=None):
    """
    Create bootstrap style pagination html code
    :param total: total records count
    :param page: current page number
    :param rows: records count per page
    :param url: base url for page link
    :param length: the maximum of page links
    """
    import math
    from uliweb import settings
    
    length = length or settings.BOOTSTRAP_PAGINATION.length
    total_message = total_message or settings.BOOTSTRAP_PAGINATION.total_message
    first = first or settings.BOOTSTRAP_PAGINATION.first
    next = next or settings.BOOTSTRAP_PAGINATION.next
    prev = prev or settings.BOOTSTRAP_PAGINATION.prev
    last = last or settings.BOOTSTRAP_PAGINATION.last
    
    def get_url(p):
        from uliweb.utils.common import query_string
        
        return query_string(url, page=p)
    
    pages = int(math.ceil(total*1.0/rows))
    begin = max(1,  page-length/2+1)
    end = min(pages, begin+length-1)
    begin = max(1, end - length + 1)
    buf = []
    buf.append('<ul>')
    total_message = total_message.replace('$pages', str(pages))
    total_message = total_message.replace('$total', str(total))
    buf.append('<li class="disabled total"><a href="#">%s</a></li>' % total_message)
    if begin != 1:
        buf.append('<li class="first"><a href="%s">%s</a></li>' % (get_url(1), first))
    if page != 1:
        buf.append('<li class="prev"><a href="%s">%s</a></li>' % (get_url(page-1), prev))
    for i in range(begin, end+1):
        if page == i:
            cls = ' active'
            href = '#'
        else:
            cls = ''
            href = get_url(i)
        buf.append('<li class="page%s"><a href="%s">%s</a></li>' % (cls, href, i))
    if page != pages:
        buf.append('<li class="next"><a href="%s">%s</a></li>' % (get_url(page+1), next))
    if end != pages:
        buf.append('<li class="last"><a href="%s">%s</a></li>' % (get_url(pages), last))
    buf.append('</ul>')
    return ''.join(buf)
