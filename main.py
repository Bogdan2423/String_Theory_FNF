f = open("data2.txt", "r")
lines = f.readlines()

symbols = lines[0][5:-2].split(", ")
word = lines[1][4:-1]

alphabet = dict()

for line in lines[2:]:
    alphabet[line[0]] = line[3:].split(" = ")

f.close()

D = set()
I = set()

for sym in alphabet:
    D.add((sym, sym))
    for other in alphabet:
        if other != sym:
            if alphabet[sym][0] in alphabet[other][1] or alphabet[other][0] in alphabet[sym][1]:
                D.add((sym, other))
                D.add((other, sym))
            else:
                I.add((sym, other))
                I.add((other, sym))

print("D =", D)
print("I =", I)


class Vertex:

    def __init__(self, label, index):
        self.label = label
        self.index = index
        self.children = []

    def check_dependency(self, x, D):
        if self == x:
            return True
        added = False
        if len(self.children) > 0:
            for child in self.children:
                added = child.check_dependency(x, D) or added
        if not added and (self.label, x.label) in D:
            self.children.append(x)
            return True
        return added


heads = [Vertex(word[0], 1)]
for index, sym in enumerate(word[1:]):
    curr = Vertex(sym, index+2)
    not_independent = False
    for head in heads:
        dep = head.check_dependency(curr, D)
        not_independent = dep or not_independent
    if not not_independent:
        heads.append(curr)


def calc_steps(head, steps, steps_list):
    steps_list[head.index] = max(steps_list[head.index], steps)
    for child in head.children:
        calc_steps(child, steps + 1, steps_list)

steps_list = [0 for _ in range(len(word)+1)]
for head in heads:
    calc_steps(head, 0, steps_list)

def calc_FNF(head, FNF, steps_list, already_added):
    if head not in already_added:
        FNF[steps_list[head.index]].append(head.label)
        already_added.add(head)
    for child in head.children:
        calc_FNF(child, FNF, steps_list, already_added)


FNF = [[] for _ in range(max(steps_list)+1)]
already_added = set()
for head in heads:
    calc_FNF(head, FNF, steps_list,already_added)

print("FNF =", FNF)

def write_graph_to_file(head, file):
    file.write(str(head.index)+"[label="+head.label+"]\n")
    for child in head.children:
        file.write(str(head.index)+" -> " + str(child.index)+"\n")
        write_graph_to_file(child, file)


output = open("output.dot", "w")
output.write("digraph g{\n")
for head in heads:
    write_graph_to_file(head, output)
output.write("}")
output.close()