import hashlib
#https://www.blockchain.com/btc/tx/e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d blocknumber 100000 .
#doublesha256hash_method
class Node:

    def __init__(self,data):
        self.left     = None
        self.right    = None
        self.parent   = None
        self.sibling  = None
        self.position = None
        self.data     = data
        self.hash     = self.doublesha256(data)

        #Bitcoin's specification
    def doublesha256(self,Txhashdata):
        first  = hashlib.sha256(Txhashdata.encode()).hexdigest()
        result = hashlib.sha256(first.encode()).hexdigest()
        return result

class Tree:
    def __init__(self,leaves):
        self.leaves = [Node(leaf) for leaf in leaves]
        self.layer = self.leaves[::]
        self.root = None
        self.build_tree()
    
    def build_layer(self):
        new_layer = []
        #要素数が奇数なら最後の要素をコピして追加
        if len(self.layer) % 2 == 1:
            self.layer.append(self.layer[-1])
        
        for i in range(0,len(self.layer),2):
            left = self.layer[i]
            right = self.layer[i+1]
            print(left.hash)
            print(right.hash)
            parent = Node(left.hash + right.hash)

            left.parent = parent
            left.sibling = right
            left.position = "left"

            right.parent = parent
            right.sibling = left
            right.position = "right"

            parent.left = left
            parent.right = right

            new_layer.append(parent)
        
        self.layer = new_layer
    
    def build_tree(self):
        while len(self.layer)>1:
            print("Now_Layer's List")
            self.build_layer()
            print("\n")
        print("Now_Layer's List")
        print(self.layer[0].hash+"\n")
        self.root = self.layer[0].hash

    def search(self,data):
        target = None
        confirm = Node(data)
        for node in self.leaves:
            if node.hash == confirm.hash:
                target = node
        return target
    
    def get_pass(self, data):
        targethash = self.search(data)
        marklepass = []
        if not(targethash):
            return
        marklepass.append(targethash.hash)
        while targethash.parent:
            sibling = targethash.sibling
            marklepass.append((sibling.hash,sibling.position))
            targethash = targethash.parent
        return marklepass

    def calclate(self,marklepass):
        value = marklepass[0]
        for node in marklepass[1:]:
            sib = node[0]
            position= node[1]
            if position == "right":
                result = Node(value + sib)
                value  = result.hash
            else:
                result = Node(sib + value)
                value  = result.hash
        return value



#Main-source
Tx_Hash = ["8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87","fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4","6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4","e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d"]

tree = Tree(Tx_Hash)
marlkeroot = tree.root
print("merkleroot is :\t" + marlkeroot+"\n")
marklepass = tree.get_pass("fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4")
print(marklepass)
result = None
if marklepass :
    result = tree.calclate(marklepass)
    print(result + "\n")
if result == marlkeroot:
    print("Confirm result: true")
else:
    print("Confirm result: false")


