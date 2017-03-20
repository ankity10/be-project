# Constants
ol_start = '<ol>'
ol_end = '</ol>'
li_start = '<li>'
li_end = '</li>'
div_start = '<div>'
div_end = '</div>'
style_start = '<style>'
style_end = '</style>'

checklist_start = '<ul class="firepad-todo">'
checklist_end = '</ul>'
checked_item = '<li class="firepad-checked">'
unchecked_item = '<li class="firepad-unchecked">'
item_end = '</li>'

new_line = '<div><br/></div>'
conflict = [-1, -1]
breaker = '<div>---------------------------------</div>'

'''
style - 0
div - 1
ol - 2
checklist(ul) - 3
'''

from html.parser import HTMLParser
from collections import defaultdict


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.obj = []
        self.style = 0
        self.div = 0
        self.ol = 0
        self.checklist = 0
        self.li = 0
        self.temp_list = []
        self.checked = 0
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag != "b" and tag != "i":
            self.text = ""
        if tag == "style":
            self.style = 1
        elif tag == "div":
            self.div = 1
        elif tag == "ol":  # Ordered list 1,2,3
            self.ol = 1
            self.temp_list = [2, []]
        elif tag == "ul":  # Checklist [x] []
            self.checklist = 1
            self.temp_list = [3, []]
        elif tag == "li":
            self.li = 1
            if self.checklist == 1 and len(attrs) and attrs[0][1] == "firepad-unchecked":
                self.checked = 0
            elif self.checklist == 1 and len(attrs) and attrs[0][1] == "firepad-checked":
                self.checked = 1
        elif tag == "b":
            self.text = self.text + "<b>"
        elif tag == "i":
            self.text = self.text + "<i>"

    def handle_endtag(self, tag):
        if tag == "style":
            self.obj.append([0, self.text])
            self.style = 0
        elif tag == "div":
            self.obj.append([1, self.text])
            self.div = 0
        elif tag == "ol":  # Ordered list 1,2,3
            self.obj.append(self.temp_list)
            self.ol = 0
        elif tag == "ul":  # Checklist [x] []
            self.obj.append(self.temp_list)
            self.checklist = 0
        elif tag == "li":
            if self.ol == 1:
                self.temp_list[1].append(self.text)
            elif self.checklist == 1 and self.checked == 1:
                self.temp_list[1].append((1, self.text))
            elif self.checklist == 1 and self.checked == 0:
                self.temp_list[1].append((0, self.text))
            self.li = 0
        elif tag == "b":
            self.text = self.text + "</b>"
        elif tag == "i":
            self.i = self.text + "</i>"

    def handle_data(self, data):
        self.text = self.text + data


def generate_string(l):
    s = ""
    for item in l:
        if item[0] == 0:  # style
            s += style_start + item[1] + style_end
        elif item[0] == 1:  # div
            s += div_start + item[1] + div_end
        elif item[0] == 2:  # OL
            s += ol_start
            for li in item[1]:
                s += li_start + li + li_end
            s += ol_end
        elif item[0] == 3:  # Checklist
            s += checklist_start
            for li in item[1]:
                if li[0] == 0:  # Unchecked
                    s += unchecked_item + li[1] + item_end
                else:  # Checked
                    s += checked_item + li[1] + item_end
            s += checklist_end
        elif item == conflict:
            s += breaker
    return s


def merge(s1, s2):
    print("string s1 is : ", s1)
    print("string s2 is : ", s2)
    parser = MyHTMLParser()
    parser.feed(s1)
    l1 = parser.obj
    parser = MyHTMLParser()
    parser.feed(s2)
    l2 = parser.obj
    final_l = []
    in1 = 0
    in2 = 0
    len1 = len(l1)
    len2 = len(l2)
    if l1[0][0] == 0:
        final_l.append([0, l1[0][1]])
        in1 += 1
    elif l2[0][0] == 0:
        final_l.append([0, l2[0][1]])
    if l2[0][0] == 0:
        in2 += 1

    while in1 < len1 and in2 < len2:
        if l1[in1][0] != l2[in2][0]:  # Different rich texts
            final_l.append(l1[in1])
            final_l.append(conflict)
            final_l.append(l2[in2])
        else:  # Same rich texts
            if l1[in1][0] == 1:  # div
                if l1[in1][1] == l2[in2][1]:  # Same
                    final_l.append(l1[in1])
                else:  # Different
                    final_l.append(l1[in1])
                    final_l.append(conflict)
                    final_l.append(l2[in2])
            else:  # OL or Checklist
                d = defaultdict(lambda: False)
                final_l.append(l1[in1])
                for li in l1[in1][1]:
                    d[li] = True
                temp_list = []
                for li in l2[in2][1]:
                    if d[li] == False:  # Not present
                        temp_list.append(li)
                if len(temp_list):
                    final_l.append(conflict)
                    final_l.append([l1[in1][0], temp_list])
        in1 += 1
        in2 += 1
    if in1 < len1 or in2 < len2:
        final_l.append(conflict)

    final_l += l1[in1:] + l2[in2:]
    result = generate_string(final_l)
    print("Merged String is : ", result)
    return result
