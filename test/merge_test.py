import sys

sys.path.append('../')
from merge import merge

'''
s1 = "<div>hello</div><div>hey</div><div>ssup</div>"
s2 = "<div>hello</div><div>hey</div><div>ssup bro??</div>"
print(merge.merge(s1,s2))
print("===============================")

s1 = '<style>ul.firepad-todo { list-style: none; margin-left: 0; padding-left: 0; } ul.firepad-todo > li { padding-left: 1em; text-indent: -1em; } ul.firepad-todo > li:before { content: "\2610"; padding-right: 5px; } ul.firepad-todo > li.firepad-checked:before { content: "\2611"; padding-right: 5px; }</style><ul class="firepad-todo"><li class="firepad-checked">hello</li><li class="firepad-unchecked">hey</li><li class="firepad-unchecked">ssup bro??</li></ul>'
s2 = '<style>ul.firepad-todo { list-style: none; margin-left: 0; padding-left: 0; } ul.firepad-todo > li { padding-left: 1em; text-indent: -1em; } ul.firepad-todo > li:before { content: "\2610"; padding-right: 5px; } ul.firepad-todo > li.firepad-checked:before { content: "\2611"; padding-right: 5px; }</style><ul class="firepad-todo"><li class="firepad-checked">hello</li><li class="firepad-checked">hey</li><li class="firepad-unchecked">ssup bro??</li><li class="firepad-unchecked">lavda</li></ul>'
print(merge.merge(s1,s2))
print("===============================")

s1 = '<style>ul.firepad-todo { list-style: none; margin-left: 0; padding-left: 0; } ul.firepad-todo > li { padding-left: 1em; text-indent: -1em; } ul.firepad-todo > li:before { content: "\2610"; padding-right: 5px; } ul.firepad-todo > li.firepad-checked:before { content: "\2611"; padding-right: 5px; }</style><ul class="firepad-todo"><li class="firepad-unchecked">a</li><li class="firepad-unchecked">b</li><li class="firepad-unchecked">c</li></ul>'
s2 = '<style>ul.firepad-todo { list-style: none; margin-left: 0; padding-left: 0; } ul.firepad-todo > li { padding-left: 1em; text-indent: -1em; } ul.firepad-todo > li:before { content: "\2610"; padding-right: 5px; } ul.firepad-todo > li.firepad-checked:before { content: "\2611"; padding-right: 5px; }</style><div>a</div><ul class="firepad-todo"><li class="firepad-unchecked">a</li><li class="firepad-unchecked">b</li><li class="firepad-unchecked">c</li></ul>'
print(merge.merge(s1,s2))
print("===============================")

s1 = '<div>a</div><div>b</div><div>c</div>'
s2 = '<div>b</div><div>a</div><div>b</div><div>c</div>'
print(merge.merge(s1,s2))
print("===============================")

s1 = '<ol><li>hello</li><li>abc</li><li>yoco</li></ol>'
s2 = '<ol><li>hello</li><li>What??</li><li>yoco</li></ol>'
print(merge.merge(s1,s2))
print("===============================")

s1 = '<div>asd</div><div>yoco</div><div>haha</div><div>hmmm</div><ol><li>hi</li><li>hello</li></ol>'
s2 = '<div>asd</div><div>yoco</div><div>haha</div><div>hmmm</div><ol><li>hi</li><li>yesss</li><li>yepp</li><li>hello</li></ol>'
print(merge.merge(s1,s2))
print("===============================")

parser = merge.MyHTMLParser()	
s = '<style>ul.firepad-todo { list-style: none; margin-left: 0; padding-left: 0; } ul.firepad-todo > li { padding-left: 1em; text-indent: -1em; } ul.firepad-todo > li:before { content: "\2610"; padding-right: 5px; } ul.firepad-todo > li.firepad-checked:before { content: "\2611"; padding-right: 5px; }</style><div>normal<b>bold</b><i>italic</i><i><b>boldanditalic</b></i></div><ol><li>item1</li><li>item2</li></ol><div><br/></div><div><br/></div><ul class="firepad-todo"><li class="firepad-checked"><b>checked</b>&nbsp;hai be</li><li class="firepad-unchecked"><i>unchecked</i>&nbsp;hai naa</li></ul>'
parser.feed(s)

'''

s1 = "<div>pict</div><div>hi ni</div>"
s2 = "<div>pict</div><div>hi ankit</div>"
print(merge.merge(s1, s2))
