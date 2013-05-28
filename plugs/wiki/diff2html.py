#coding=utf8
import re
from uliweb.core.template import template

r_info = re.compile(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')

text = """diff --git a/uliweb/form/widgets.py b/uliweb/form/widgets.py
index d7f193b..59a1c8d 100644
--- a/uliweb/form/widgets.py
+++ b/uliweb/form/widgets.py
@@ -42,13 +42,15 @@ class Password(Text): type = 'password'
 class Number(Text): type = 'number'
 class TextArea(Build):
     def __init__(self, value='', **kwargs):
-        self.value = value
+        self.value = value or ''
         super(TextArea, self).__init__(**kwargs)

     def to_html(self):
-        args = self.kwargs
-        args.setdefault('rows', 5)
-        args.setdefault('cols', 40)
+        args = self.kwargs.copy()
+        if not args.get('rows'):
+            args['rows'] = 5
+        if not args.get('cols'):
+            args['cols'] = 40
         return str(Tag('textarea', self.value, **args))
 class Hidden(Text): type = 'hidden'
 class Button(Build):
"""

default_template = ["""
<div class="diff-view file commentable" id="{{=id}}">
  <div class="meta" data-path="{{=filename}}">
    <div class="info">""",
"""      {{<<fileinfo}}
    </div>
    <div class="actions">
      {{<<actions}}
    </div>
  </div>
  <div class="data highlight">
    <table class="diff-table">
      <colgroup>
        <col width="30px"></col>
        <col width="30px"></col>
        <col width="*"></col>
      </colgroup>
      <tbody>
        {{for ln, rn, cls, line in lines:}}
          <tr>
            <td class="line_numbers">{{=ln}}</td>
            <td class="line_numbers">{{=rn}}</td>
            <td class="{{=cls}} diffline">
                <pre>{{=line}}</pre>
            </td>
          </tr>
        {{pass}}
      </tbody>
    </table>
  </div>
</div>
"""]

info_template = """<span class="diffstat" rel="tooltip" title="%(changes)s">
  %(total_count)s <span class="diffstat-bar">
      %(change_direct)s
      </span>
</span>
"""

def get_changes(ins_count, del_count):
    if ins_count == 0 and del_count == 0:
        return '', ''
    total_count = del_count + ins_count
    if not ins_count:
        if del_count >= 5:
            num = 5
            left = 0
        else:
            num = del_count
            left = 5 - num
        change_direct = '<i class="minus">%s</i>' % ('&#xf053;'*num)
        changes = '%d 删除' % del_count
    elif not del_count:
        if ins_count >= 5:
            num = 5
            left = 0
        else:
            num = ins_count
            left = 5 - num
        change_direct = '<i class="plus">%s</i>' % ('&#xf053;'*num)
        changes = '%d 添加' % ins_count
    else:
        left = 0
        ins_percent = int(ins_count*1.0/total_count*5)
        del_percent = int(del_count*1.0/total_count*5)
        change_direct = '<i class="plus">%s</i><i class="minus">%s</i>' % ('&#xf053;'*ins_percent, '&#xf053;'*del_percent)
        if 5 > (ins_percent+del_percent):
            change_direct = change_direct + '&#xf053;'
        changes = '%d 添加 &amp; %d 删除' % (ins_count, del_count)
    change_direct += '&#xf053;'*left
    return change_direct, changes

def diff2html(filename, id, diff, fileinfo='', actions='', tmpl=None):
    tmpl = tmpl or default_template
    
    if isinstance(diff, (str, unicode)):
        lines = diff.splitlines()
    else:
        lines = diff
        
    def get_lines(diff, counts):
        skip = True
        left = 0
        right = 0
        ins_count = 0
        del_count = 0
        for line in diff:
            if skip:
                if line.startswith('@@'):
                    skip = False
                    info = parse_info_line(line)
                    left = info['L-begin']
                    right = info['R-begin']
                    yield '...', '...', 'gc', line.rstrip()
            else:
                if line.startswith('@@'):
                    info = parse_info_line(line)
                    if info:
                        left = info['L-begin']
                        right = info['R-begin']
                        yield '...', '...', 'gc', line.rstrip()
                        continue
                
                left_line_num = left
                right_line_num = right
                if line.startswith('-'):
                    left += 1
                    del_count += 1
                    right_line_num = ''
                    _cls = 'gd'
                elif line.startswith('+'):
                    right += 1
                    ins_count += 1
                    left_line_num = ''
                    _cls = 'gi'
                else:
                    left += 1
                    right += 1
                    _cls = ''
                yield left_line_num, right_line_num, _cls, line.rstrip()
        counts.append(ins_count)
        counts.append(del_count)
        
    def parse_info_line(line):
        m = r_info.match(line)
        if m:
            return {'L-begin':int(m.group(1)), 'L-count':int(m.group(2) or 1),
                'R-begin':int(m.group(3)), 'R-count':int(m.group(4) or 1)}
                
    counts = []
    text1 = template(tmpl[0], {'filename':filename, 'id':id})
    text2 = template(tmpl[1], {'lines':get_lines(lines, counts), 
        'filename':filename, 'id':id, 'fileinfo':fileinfo, 'actions':actions})

        
    ins_count, del_count = counts
    change_direct, changes = get_changes(ins_count, del_count)
    d = {'total_count':ins_count+del_count,
        'change_direct':change_direct,
        'changes':changes,
        }
    return text1 + (info_template % d) + text2

if __name__ == '__main__':
    print diff2html(text, 'uliweb/form/widgets.py')