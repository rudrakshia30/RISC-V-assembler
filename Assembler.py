import sys,re

input_file = sys.argv[1]
output_file = sys.argv[2]

d= {
        "x0": "00000", "x1": "00001", "x2": "00010", "x3": "00011", "x4": "00100",
        "x5": "00101", "x6": "00110", "x7": "00111", "x8": "01000", "x9": "01001", 
        "x10": "01010", "x11": "01011", "x12": "01100", "x13": "01101", "x14": "01110", 
        "x15": "01111", "x16": "10000", "x17": "10001", "x18": "10010", "x19": "10011",
        "x20": "10100", "x21": "10101", "x22": "10110", "x23": "10111", "x24": "11000", 
        "x25": "11001", "x26": "11010", "x27": "11011", "x28": "11100", "x29": "11101", 
        "x30": "11110", "x31": "11111",
        "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100", 
        "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "s1": "01001", 
        "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110",
        "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011", 
        "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000", 
        "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101",
        "t5": "11110", "t6": "11111"
    }

def chk_reg(r, lnum, f2,labelno1):

    if r not in d:
        print(f"Invalid register '{r}' at line {lnum+labelno1}")
        fltrun(f2)

def fltrun(f2):

    f2.truncate(0)
    exit()

B_list = ["beq","bne","blt","bge","bltu","bgeu"]
I_list = ["lw","addi","sltiu","jalr"]
J_list = ["jal"]
R_list = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]

list_instruction = R_list+B_list+I_list+J_list
list_instruction.append("auipc")
list_instruction.append("lui")
list_instruction.append("sw")

labels={}
lnumcopy = 1
labelno = 0
indexl = []

emptycopy = 0
empty = []

def clip(s):

    parts = []
    for p in s.split(","):
        parts.extend(p.strip().split())
    return parts

with open(input_file,"r") as f:

    ll = f.readlines()
    lnew = []

    for i in ll:
        if (i.strip() == ""):
            continue
        if(":" in i.strip()and i.strip().endswith(":")):
            continue
        else:
            lnew.append(i)

    if len(lnew) > 64:
        print("instruction out of memory range")
        with open(output_file,"w"):
            pass
        exit() 

    while(len(ll) > 0 and ll[-1] == "\n"):
        del ll[-1]

    if(len(ll) == 0):
        print("no instruction in the file")
        exit()

    for ind,i in enumerate(ll):

        if i == "\n" or i == "":
            emptycopy+=1
            empty.append(ind+1)
            continue

        last = i.strip()[-1]

        if not last.isalnum() and last != ")" and last != ":":

            print(f"syntax error in line {lnumcopy+labelno+emptycopy}")
            with open(output_file,"w"):
                pass
            exit()

        if re.search(r'\s+:', i):

            print(f"syntax error in line {lnumcopy+labelno+emptycopy}")
            with open(output_file,"w"):
                pass
            exit()

        if ":" in i and  i.strip().endswith(":"):

            if ind+1 < len(ll):

                indexl.append(ind+1)
                labelno += 1
                st = ll[ind+1].strip()
                i = i.strip()+" "+st
                ll[ind] = i
                del ll[ind+1]

            else:
                print("error in last line")
                exit()

        if re.search(r'[,)(;]\s*[,)(;]', i):

            print(f"syntax error in line {lnumcopy+labelno+emptycopy}")
            with open(output_file,"w") as x:
                        pass
            exit()

        if ":" in i and not i.strip().endswith(":"):

            label, rest = i.split(":",1)
            parts = re.split(r'[ ,;()]+', rest.strip())
            s1 = [label+":"] + [x for x in parts if x!=""]

        else:
            parts = [x for x in re.split(r'[ ,;()]+', i) if x != ""]
            s1 = parts

        if len(s1) == 0:
            continue

        if(s1[0] not in list_instruction):

            if s1[0] != "" and s1[0][-1] == ":":

                if s1[0][0:-1] in labels:
                    print(f"invalid instruction as same label is defined again in line {lnumcopy+labelno+emptycopy}")
                    with open(output_file,"w") as x:
                        pass
                    exit()

                labels.update({s1[0][0:-1]:(lnumcopy-1)*4})

                if str(s1[0][0]).isalpha() != True:
                    print(f"error in label in line number {lnumcopy+labelno+emptycopy}")
                    p= open(output_file,"w")
                    p.close()
                    exit()

            else:
                print(f"error in instruction in line number {lnumcopy+labelno+emptycopy}")
                p= open(output_file,"w")
                p.close()
                exit()

        lnumcopy += 1

def main(inline,f2):

    if len(inline) == 0:
        return -1
    
    if (inline[0] not in list_instruction):

        p = open(output_file,"w")
        p.close()
        print(f"error in instruction in line number {lnum+labelno1+el}")
        exit()

    if(inline[0] in R_list ):
        w = R_type_to_Binary(inline,f2)

    elif(inline[0] in B_list):
        w = btype(inline,f2)

    elif(inline[0] in I_list):
        w = Iinstruction(inline,f2)

    elif(inline[0] in J_list):
        w = J(inline,f2)

    elif(inline[0] == "sw"):
        w = sw(inline,f2)

    elif(inline[0] == "auipc"):
        w = auipc(inline,f2)

    elif(inline[0] == "lui"):
        w = lui(inline,f2)

    else:
        print(f"error in instruction in line number {lnum+labelno1+el}")
        fltrun(f2)

    return w
def immcheck(imm,n,f2):

    if imm.lstrip('-').isdigit() != True:     
        print(f"invalid immediate in line number {lnum+labelno1+el}")
        fltrun(f2) 

    if int(imm)>=-(2**(n-1)) and int(imm)<=(2**(n-1))-1:
        return
    
    else:
        print(f"immediate out of range in line number {lnum+labelno1+el}")
        fltrun(f2)

def bin_nbits(x,n):

    s=""
    s1=""

    if(x==0):
        return "0"*n
    
    while(x!=0):
        r=x%2
        x=x//2
        s+=str(r)

    s=s[::-1]
    s1+="0"*(n-len(s))
    s1+=s
    return s1

def compl(x,n):

    if(x>=0):
        return bin_nbits(x,n)
    
    else:
        return bin_nbits(x+(1<<n),n) 
    
class R_Type:

    def __init__(self):

        self.opcode = "0110011"
        self.instruction_map = {
            "add":  {"f3": "000", "f7": "0000000"},
            "sub":  {"f3": "000", "f7": "0100000"},
            "sll":  {"f3": "001", "f7": "0000000"},
            "slt":  {"f3": "010", "f7": "0000000"},
            "sltu": {"f3": "011", "f7": "0000000"},
            "xor":  {"f3": "100", "f7": "0000000"},
            "srl":  {"f3": "101", "f7": "0000000"},
            "or":   {"f3": "110", "f7": "0000000"},
            "and":  {"f3": "111", "f7": "0000000"},
        }

def R_type_to_Binary(lst,f2):

    if len(lst) != 4:
            print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
            fltrun(f2)

    r = R_Type()

    instr = lst[0]   
    rd = lst[1]         
    rs1 = lst[2]       
    rs2 = lst[3] 

    chk_reg(rd, lnum, f2,labelno1+el)   
    chk_reg(rs1, lnum, f2,labelno1+el)
    chk_reg(rs2, lnum, f2,labelno1+el)

    funct3 = r.instruction_map[instr]["f3"]
    funct7 = r.instruction_map[instr]["f7"]

    opcode = r.opcode

    rd_bin = d[rd]
    rs1_bin = d[rs1]
    rs2_bin = d[rs2]

    R_type_Binary = funct7 + rs2_bin + rs1_bin + funct3 + rd_bin + opcode

    return (R_type_Binary)

class B_type:

    def __init__(self,name,func3,opcode="1100011"):

        self.opcode="1100011"
        self.name1=name
        self.func3=func3

beq=B_type("beq","000")
bne=B_type("bne","001")
blt=B_type("blt","100")
bge=B_type("bge","101")
bltu=B_type("bltu","110")
bgeu=B_type("bgeu","111")

name = {
    "beq":beq,
    "bne": bne,
    "blt": blt,
    "bge": bge,
    "bltu": bltu,
    "bgeu": bgeu
}

def btype(l,f2):

    if (len(l)!=4):
        print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
        fltrun(f2)

    chk_reg(l[1], lnum, f2,labelno1+el)
    chk_reg(l[2], lnum, f2,labelno1+el)

    s=''

    if(l==["beq","zero","zero","0x00000000"]):
        l[3]="0"

    if(l[3].lstrip('-').isdigit()==True):

        immcheck(l[3],12,f2)
        if int(l[3]) % 2 != 0:
            print(f"Branch immediate is not a multiple of 2 at line {lnum+labelno1+el}")
            fltrun(f2)

        imm=compl(int(l[3])//2,12)

    else:

        if l[3] not in labels:
            print(f"label used in line {lnum+labelno1+el} but not defined")
            fltrun(f2)

        offset=(labels[l[3]]-((lnum-1)*4))

        imm=offset>>1
        imm=compl(imm,12)

    s+=imm[0]
    s+=imm[2:8]
    s+=d[l[2]]
    s+=d[l[1]]
    s+=(name[l[0]]).func3
    s+=imm[8:12]
    s+=imm[1]
    s+=(name[l[0]]).opcode

    return s  

class I:

    def __init__(self,func3,opcode):
        self.func3=func3
        self.opcode=opcode

def Iinstruction(l,f2): 

    s=""

    if l[0]=="lw" :

        if (len(l)!=4):
            print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
            fltrun(f2)

        chk_reg(l[1], lnum, f2,labelno1+el) 
        chk_reg(l[3], lnum, f2,labelno1+el) 

        immcheck((l[2]),12,f2)

        s+=compl(int(l[2]),12)+d[l[3]]+lw.func3+d[l[1]]+lw.opcode

    elif l[0]=="addi" or l[0]=="sltiu":

        if (len(l)!=4):
            print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
            fltrun(f2)

        chk_reg(l[1], lnum, f2,labelno1+el) 
        chk_reg(l[2], lnum, f2,labelno1+el)
        immcheck((l[3]),12,f2)

        s+=compl(int(l[3]),12)+d[(l[2])]+dictI[l[0]].func3+d[(l[1])]+dictI[l[0]].opcode

    else:#jalr
        
        if (len(l)!=4):
            print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
            fltrun(f2)

        chk_reg(l[1], lnum, f2,labelno1+el)
        chk_reg(l[2], lnum, f2,labelno1+el)
        immcheck((l[3]),12,f2)

        s+=compl(int(l[3]),12) +d[l[2]]+"000"+d[l[1]]+"1100111"
    return s

def J(l,f2):#jal

    if (len(l)!=3):
            print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
            fltrun(f2)

    chk_reg(l[1],lnum,f2,labelno1+el)

    s=""

    if(l[2].lstrip('-').isdigit()==True):

        immcheck(l[2],20,f2)
        if int(l[2]) % 2 != 0:
            print(f"Branch immediate is not a multiple of 2 at line {lnum+labelno1+el}")
            fltrun(f2)

        imm = compl(int(l[2])//2,20)
    else:
        if l[2] not in labels:
            print(f"label used in line {lnum+labelno1+el} but not defined")
            fltrun(f2)

        offset=(labels[l[2]]-((lnum-1)*4))
        imm=offset>>1
        imm=compl(imm,20)

    s1=imm
    s+=s1[0]+s1[10:20]+s1[9]+s1[1:9]+d[l[1]]+"1101111" 
    return s

lw=I("010","0000011")
addi=I("000","0010011")
sltiu=I("011","0010011")
jalr=I("000","1100111")

dictI = {
    "lw": lw,
    "addi": addi,
    "sltiu": sltiu,
    "jalr": jalr
}

def sw(l,f2):

    chk_reg(l[1], lnum, f2,labelno1+el)  
    chk_reg(l[3], lnum, f2,labelno1+el)

    rs2 = l[1]

    if (len(l)!=4):
        print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
        fltrun(f2)

    if l[2].lstrip('-').isdigit():
        imm = int(l[2])

    else:
        print(f"Invalid immediate in line number: {lnum+labelno1+el}")
        fltrun(f2)

    if imm<=2**11-1 and imm>=-2**11:
        pass

    else:
        print(f"Immediate out of range in line number: {lnum+labelno1+el}")
        fltrun(f2)

    rs1 = l[3]

    imm_bin=compl(imm,12)

    return (
        imm_bin[:7] +          
        d[rs2] +               
        d[rs1] +               
        "010" +                
        imm_bin[7:] +          
        "0100011"              
    )

def auipc(l,f2):

    chk_reg(l[1], lnum, f2,labelno1+el)

    rd=d[l[1]]
    op="0010111"

    if (len(l)!=3):

        print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
        fltrun(f2)

    if l[2].lstrip('-').isdigit():
        imm = int(l[2])

    else:
        print(f"Invalid immediate in line number: {lnum+labelno1+el}")
        fltrun(f2)

    if imm<=2**19-1 and imm>=-2**19:
        pass

    else:

        print(f"Immediate out of range in line number: {lnum+labelno1+el}")
        fltrun(f2)

    imm_b=compl(imm,20)
    final=imm_b+rd+op
    return final

def lui(l,f2):

    chk_reg(l[1], lnum, f2,labelno1+el)
    rd=d[l[1]]
    op="0110111"

    if (len(l)!=3):
        print(f"Error in line {lnum+labelno1+el}, invalid number of arguments")
        fltrun(f2)

    if l[2].lstrip('-').isdigit():
        imm = int(l[2])

    else:
        print(f"Invalid immediate in line number: {lnum+labelno1+el}")
        fltrun(f2)

    if imm<=2**19-1 and imm>=-2**19:          
        pass

    else:
        print(f"Immediate out of range in line number: {lnum+labelno1+el}")
        fltrun(f2)

    imm_b=compl(imm,20)
    final=imm_b+rd+op
    return final

lnum=1
f2=open(output_file,"w")

for im,i in enumerate(ll):

    el=0
    for y in empty:

        if y <= im+1:
            el += 1
    if i == "\n":
        continue

    else:
        i=i.strip()
        if re.search(r'[,:;]\s*[,:;]', i):
            print(f"syntax error in line {lnum+labelno1+el}")
            fltrun(f2)

        if ":" in i and not i.strip().endswith(":"):
            label, rest = i.split(":",1)
            parts = re.split(r'[ ,;()]+', rest.strip())
            s1 = [label+":"] + [x for x in parts if x!=""]

        else:
            parts = [x for x in re.split(r'[ ,;()]+', i) if x != ""]
            s1 = parts

        if len(s1)==0:
            continue

        labelno1 = 0

        for k in indexl:
            if k <= im+1:
                labelno1 += 1

        if(s1[0] not in list_instruction):
            if str(s1[0])[-1]==":":
                del s1[0]

        if(im==len(ll)-1):

            if(s1!=["beq","zero","zero","0"] and s1!=["beq","zero","zero","0x00000000"]):
                for i in range(0,len(ll)-1):
                    if(clip(ll[i].strip())==["beq","zero","zero","0"] or clip(ll[i].strip())==["beq","zero","zero","0x00000000"]):
                        print("Virtual Halt not used as last instruction")
                        exit()
                    if(":" in ll[i]):
                        p=ll[i]
                        p=p.split(":",1)
                        del p[0]
                        if(clip(p[0].strip())==["beq","zero","zero","0"] or clip(p[0].strip())==["beq","zero","zero","0x00000000"]):
                            print("Virtual Halt not used as last instruction")
                            exit()

                print("Missing Virtual Halt instruction")
                exit()

        x=main(s1,f2)
        
        if(x==-1):
            continue

        else:
            f2.write(x+"\n")
            lnum+=1

f2.close()
