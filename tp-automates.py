#!/usr/bin/env python3
"""
Developpez votre projet de TP automates finis dans ce fichier.
"""
import sys
import os.path
from automaton import *

if __name__ == "__main__": # If the module is run from command line, test it
     
###initialisation des automates de test'

 a7=Automaton("aut6")
 a7.from_txtfile("./tests/astar_bstar.af")
 print(a7)
 
 a8=Automaton("aut7")
 a8.from_txtfile("./tests/aa_factor.af")
 print(a8)
 
 a9=Automaton("aut8")
 a9.from_txtfile("./tests/det_aa_factor.af")
 print(a9)
 
 a10=Automaton("aut10")
 a10.from_txtfile("./tests/abstar.af")
 

############################La partie 01###############################

########################################################################
def is_determinisitc(a:Automaton)->bool:
     
   state_with_epsilon=[]
   for (source,letter,target) in a.get_transitions():
      if letter == EPSILON:
         return False
      else:
       src_ltr=[source,letter]
       if (src_ltr) not in state_with_epsilon: 
         state_with_epsilon.append(src_ltr)
       else : 
           return False

   return True
########################################################################## 
##################################test de is determinsitic################

print("expected false car astar_bstar est non deterministe")
print(is_determinisitc(a7))
print("expected false  car aa_factor est non  deterministe")
print(is_determinisitc(a8))
print("expected True  car abstar est  deterministe")
print(is_determinisitc(a10))
###################################################################
def execute(a:Automaton,s:str()):
     
  if  (is_determinisitc(a)):
   
     finales=a.get_final()
     if s=="%" and len(s)==1 and finales[0]=="0" : 
         return False
     else: 
        if s=="%" and finales[0]!="0": 
            return False
   
        else:
             transition=dict()
             
             for (source,letter,target) in a.get_transitions():
                
                transition[(source,letter)]=target
                current_state=a.initial
                l=0
             for char in s:
                 if((current_state,char) not in transition.keys()): 
                     return False
                 current_state=transition[(current_state,char)]
                 l+=1
                 
             if  l!=len(s): 
                 return False   
             if current_state in finales :
                 return True
             else: 
                 return False
  else :   
        return "error"

########################## test execute #####################################
print("expected true car aaabbaab est accepte par lauromate det_aa_factor")
print(execute(a9,"aaabbaab"))

print(execute(a10, "abababab"))
print("expected erreur car a7 est non deterministe ")
print(execute(a7, "abababab"))

#############################Parite 02#####################################

def get_accessible(a:Automaton):
    acc=[]
    c=[a.initial]
    for ( source, letter, target) in a.get_transitions():
        if source in c:
            c.append(target)
    for state in c :
        if state not in acc:
            acc.append(state)
    return acc

############################################################################


def get_coaccessible(a:Automaton):
    coacc=[]
   
    for i in a.finalList:
        coacc.append(i)
        for ( source,letter,target) in a.get_transitions():
            if target ==i:
               if source not in coacc : 
                coacc.append(source)
                i==source
    return coacc    
########################################################################
def trim (a:Automaton):
    acc= get_accessible(a)
    accco= get_coaccessible(a)
   
    new=Automaton("new")
    for (source,letter,target) in a.get_transitions():
        for a in acc:
            for b in accco:
                if source==a or target ==b:
                    new.add_transition(source,letter,target)
    return new  
###############################################################

##########################test de  get_accessible#############
print(" la liste des etas accessible de aa_factor")
print(get_accessible(a8))
print(" la liste des etas accessible de astar_bstar")
print(get_accessible(a7))
###################test de get_coaccessible####################

print(" la liste des etas co_accessible de aa_factor")
print(get_coaccessible(a8))
print(" la liste des etas co_accessible de astar_bstar")
print(get_coaccessible(a7))


######################test de trim#####################
print("trim de aa_facteur")
print(trim(a8))


#######################################################################################
def complete(a:Automaton):
    
    transition=dict()
    sources=a.get_states()
    for i in sources:
      transition[i] = []

    for (source,letter,target) in a.get_transitions():

       if letter not in transition[source]:
          transition[source].append(letter)
     
    
    non_complete_states=[]
    for i in sources:
     if transition[i]!=a.get_alphabet():
        non_complete_states.append(i)
        
    if len(non_complete_states)==0:  
         print("Automate Complet")
         return
      
    else:
         non_complete_states.append("p")
         transition["p"]=[]
         for state in non_complete_states:
             for al in a.get_alphabet():
                 if(al  not in transition[state]):
                     
                     a.add_transition(state, al, "p")
                     
    return a
##################################################################################    
def complement(a:Automaton):
   if(is_determinisitc(a)):
    a=complete(a)
    for state in a.get_states():
        if(state in a.get_final()):
            a.unmake_final(state)
        else :
            a.make_final(state)
    return a     
   else :
        print("un Automate non deterministe ne peut pas etre Complementer")
#############################test complete et complement#################################   
print("complete a10 ")
print(complete(a10))
print("complete a9 ")
print(complete(a9))
print("complete a10 ")
print(complement(a10))
print("complete a9 ")
print(complement(a9))
##########################################################################
def new_sup_state(a:Automaton)->str:   
    """Trouve un nouveau nom d'état supérieur a letat max de a`"""
    max_state = -1
    for state in a.get_states() :
        try : max_state = max(int(state),max_state)
        except ValueError: pass # ce n'est pas un entier, on ignore
    return str(max_state+10)

######################################################################

def union(a:Automaton,b:Automaton)->Automaton:
    ##automate c est lautomate a ou b'
    c=Automaton("Autc")
    c.make_copy(a)
    bCopy=Automaton("autbcopy")

    """ creation d'un automate copy de b q'on va luis modifier le nom des etat grace a new_up_state"""
  
    
    new_state=new_sup_state(c)
    finals_b=[]
    """ copier les transition de b a bcopy"""
    for t in b.get_transitions():
        if(t[0]=="p" and t[2]!="p"):  bCopy.add_transition("p",t[1], str(int(t[2])+int(new_state)))
        if(t[2]=="p" and t[0]!="p"):  bCopy.add_transition(str(int(t[0])+int(new_state)), t[1], "p") 
        if(t[2]=="p" and t[0]=="p"):  bCopy.add_transition("p", t[1], "p") 

        else:
          bCopy.add_transition(str(int(t[0])+int(new_state)), t[1], str(int(t[2])+int(new_state)))
        if(t[0] in b.get_final()):
            if(t[0] not in finals_b):
                if(t[0]=="p"):finals_b.append("p")
                else :finals_b.append(str(int(t[0])+int(new_state)))
            
        if(t[2] in b.get_final()):
              if(t[2] not in finals_b):
                  if(t[2]=="p"):finals_b.append("p")
                  else :finals_b.append(str(int(t[2])+int(new_state)))
                 
    """recupere kes etat finaux de b """
    
    """ Copier les transitions de lautomate bcopy dans c"""
    for t in bCopy.get_transitions():
        c.add_transition(t[0], t[1], t[2])
   
    for t in b.get_final():
        if(t[0]=="p"):c.make_final("p")
        else:
           c.make_final(str(int(t[0])+int(new_state)))
    """creation des etat finaux de c"""
    sa=[]
    sb=[]
    sa=a.get_states()
    sb=bCopy.get_states()
    """ cree l'etat initiale -1 qui vas vers les deux automates a travers epsilon """
    c.add_transition("-1", EPSILON, sa[0])
    c.add_transition("-1", EPSILON, str(int(sb[0])+int(new_state)))
    
    return c
###################test union########################################
print("le resultat de l'union de des automates det_aa_factor et abstar")
c=Automaton("AUTC#")
c=union(a10,a9)    
print(c)
#################################################################################
def intersection(a:Automaton,b:Automaton)->Automaton:
    
    '''
    nous savons que on peut obtenir l'intersection grace a l'union'''
    #AetB=non(non(A)ou non(B))-->AetB=
    
    #la negation est le complement de l'automate

    
    c=Automaton("AUTC#")
    
    aCopy=Automaton("AUTA")
    bCopy=Automaton("AUTB")
    
    aCopy=complement(a)
    bCopy=complement(b)
    
    cCopy=Automaton("AUTC")
    cCopy=union(aCopy,bCopy)
    
    
    c=complement(cCopy)
    return c
 #######################test intersection#########################   
c=Automaton("AUTC#")
c=intersection(a10,a9)  
print("l'union des automates complementaire qui font partie de la non disjonction est un automate non deterministe")
print("donc le resultat et rien car on peut pas complementer un automate non deterministe")
print(c)
##l'union de aCopy et b Copy et un automate non deterministe 
##donc le resultat de l'automate est impossible

############################ Partie 03########################

def remove_epsilon(a):
      for s in a.get_states():
        for t1 in a.get_transitions():
          if t1[1] == "%":
              a.remove_transition(t1[0], t1[1], t1[2])
              for t2 in a.get_transitions():
                  if t1[2] == t2[0]:
                      a.add_transition(t1[0], t2[1], t2[2])
                  if t2[0] not in a.get_final():
                      a.make_final(t1[0])
                      
        return a     
####################### test remove epsilon#############################
print("l'automate aa_factor apres l'enlevemebt du epsilon")         
print(remove_epsilon(a8))





