import pkuseg
from collections import Counter

words=[]
seg = pkuseg.pkuseg()
for line in open('D:\\JennyYang\\testfiles\\20221118_2.txt',encoding="utf-8"):
    words.extend(seg.cut(line))

results=Counter(words).most_common()
f=open('D:\\JennyYang\\testfiles\\20221118_2_output.txt','w',encoding="utf-8")
for word in results:
    f.writelines(str(word[0])+":"+str(word[1])+"\n")
f.close

