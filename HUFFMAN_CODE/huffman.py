class TreeNode:
    def __init__(self,letter,sum):
        self.letter=letter
        self.sum=sum
        self.left=None
        self.right=None


class Huffmancode:
    def __init__(self):      
        self.frequency={}
        self.heap=[]
        self.codes={}
        self.reversecode={}


    def build_frequency(self,text):
        for i in text:
            if i in self.frequency:
                self.frequency[i]+=1
            else:
                self.frequency[i]=1


    def insert_heap(self,node):
        heap=self.heap
        heap.append(node)
        current=len(heap)-1
        parent=(current-1)//2
        while current!=0 and heap[current].sum<heap[parent].sum:
            heap[current],heap[parent]=heap[parent],heap[current]
            current=parent
            parent=(current-1)//2

   
    def heapify_heap(self):
        heap=self.heap
        current=0
        left=1
        right=2
        while left<len(heap):
            if right<len(heap):
                left=left if heap[left].sum<=heap[right].sum else right
            if heap[current].sum<=heap[left].sum:
                return
            heap[current],heap[left]=heap[left],heap[current]
            current=left
            left=(current*2)+1
            right=(current*2)+2
    
    
    def extract_heap(self):
        heap=self.heap
        if len(heap)==1:
            return heap.pop()
        temp=heap[0]
        heap[0]=heap.pop()
        self.heapify_heap()
        return temp

    

    def build_heap(self):
        for i in self.frequency:
            letter=i
            freq=self.frequency[i]
            node= TreeNode(letter,freq)
            self.insert_heap(node)



    def build_binary_tree(self):
        heap=self.heap
        while len(heap)>1:
            node1=self.extract_heap()
            node2=self.extract_heap()

            total= node1.sum + node2.sum
            node3= TreeNode(None,total)
            node3.left= node1
            node3.right= node2
            self.insert_heap(node3)



    def getcodes(self,root,s=''):
        if root.letter!=None:
            self.codes[root.letter]=s
            self.reversecode[s]=root.letter
            return

        self.getcodes(root.left,s+'0')
        self.getcodes(root.right,s+'1')



    def build_encoded_text(self,text):
        s=''
        for i in text:
            s+=self.codes[i]
        return s



    def build_int_array(self,text):
        arr=[]
        count=0
        s=''
        for i in range(len(text)):
            s+=text[i]
            if count==7:
                arr.append(int(s,2))
                s=''
                count=0
            else:
                count+=1
        return arr
            
    
    
    
    def compress(self,path):
        file=open(path,'r')
        text=''
        for i in file:
            text+=i

        self.build_frequency(text)
        self.build_heap()
        self.build_binary_tree()
        root=self.heap.pop()
        self.getcodes(root)
        encoded_string= self.build_encoded_text(text)
        num='00000000'
        if len(encoded_string)%8!=0:
            leftout= len(encoded_string)%8
            padding=(8-leftout)
            for i in range(padding):
                encoded_string+='0'
            num=''
            for i in range(7,-1,-1):
                if i==padding:
                    num+='1'
                else:
                    num+='0'
        encoded_string=num+encoded_string
        int_array= self.build_int_array(encoded_string)

        byte=bytes(int_array)
        encoded_file=open("encoded_text.bin", "wb")
        encoded_file.write(byte)


    def getencoded(self,ints):
        encoded=''
        for nums in ints:
            for i in range(7,-1,-1):
                bit=(nums>>i) & 1
                encoded+= str(bit)
        return encoded


    def getpad(self,encoded):
        for i in range(7,0,-1):
            if encoded[i]=='1':
                return i
        return 0


    def get_decoded_string(self,encoded,padd):
        s=''
        decoded_string=''
        for i in range(8,len(encoded)-padd):
            s+=encoded[i]
            if s in self.reversecode:
                decoded_string+= self.reversecode[s]
                s=''
        return decoded_string



    def decompress(self,path):
        file=open(path,'rb')
        temp=[]
        for i in file:
            temp.append(i)
        ints=[]
        for i in temp:
            for j in i:
                ints.append(j)
        
        encoded= self.getencoded(ints)
        padd= self.getpad(encoded)
        decoded_string= self.get_decoded_string(encoded,padd)

        file=open('decoded_text.txt','w')
        file.write(decoded_string)
        
        
        
        
        





        


        



            

guy= Huffmancode()
guy.compress('sample.txt')
guy.decompress('encoded_text.bin')



