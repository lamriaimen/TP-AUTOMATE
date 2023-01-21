#!/usr/bin/env python3
"""
Module to represent, build and manipulate finite state automata
"""

from typing import Dict, List, Union, Tuple, Optional
from collections import OrderedDict, Counter # remember order of insertion
import sys
import os.path

########################################################################
########################################################################

def warn(message, *, warntype="WARNING", pos="", **format_args):
  """Print warning message."""
  msg_list = message.format(**format_args).split("\n")
  beg, end = ('\x1b[33m', '\x1b[m') if sys.stderr.isatty() else ('', '')
  if pos: pos += ": "
  for i, msg in enumerate(msg_list):
    warn = warntype if i==0 else " "*len(warntype)
    print(beg, pos, warn, ": ", msg, end, sep="", file=sys.stderr)

##################

def error(message, **kwargs):
    """Print error message and quit."""
    warn(message, warntype="ERROR", **kwargs)
    sys.exit(1)
    
########################################################################
########################################################################

EPSILON = "%" # Constant to represent empty string

########################################################################
########################################################################

class Automaton(object):
  """
  An automaton is a list of transitions. A transition is a triple (string character,string)
  """  
  name:str
  initial:str
  finalList:list
  transitionList:list

  
##################  
  
  def __init__(self,name:str)->None:
    self.reset(name)     

##################
    
  def reset(self,name:str=None):
    """
    Reinitialize the automaton with empty content
    """
    self.name = name
    self.initial = None 
    self.finalList = []
    self.transitionList = []  

##################
    
  def set_name(self,name:str):
    """
    Change the name of an automaton
    """
    if name == self.name:
        warn("Automaton {aut} already has this name.",aut=self.name)
    else:
        self.name = name

##################
    
  def is_empty(self):
    """
    Checks if an automaton is empty
    """
    return ((self.get_transitions() == []) and (self.initial == None) and (self.get_final() == []))

##################
      
  def add_transition(self, source:str, letter:chr, target:str):
    """
    Add a transition from `source` to `target` on `letter`
    """    
    if ( (source,letter,target) in self.get_transitions() ):
        warn("Transition: {s} -{a}-> {t} is already present. Will not add to automaton {aut}.",s=source,a=letter,t=target,aut=self.name)
    else:
        self.transitionList.append((source,letter,target))
        
##################
        
  def remove_transition(self, source:str, letter:chr, target:str):
    """
    Remove a transition from `source` to `target` on `letter`
    """    
    if ( (source,letter,target) not in self.get_transitions() ):
        warn("Transition: {s} -{a}-> {t} is already absent. Will not modify automaton {aut}.",s=source,a=letter,t=target,aut=self.name)
    else:
        self.transitionList.remove((source,letter,target))
        
##################

  def make_final(self, state:str):
    """
    Transform a state of the automaton into a final state
    """
    if ( state in self.get_final() ):
        warn("State {s} is already final. Will not modify automaton {aut}.",s=state,aut=self.name)
    else:
        self.finalList.append(state) 
                
##################
        
  def unmake_final(self, state:str):
    """
    Transform a final state of the automaton into a not final state
    """
    if ( state not in self.get_final() ):
        warn("State {s} is already not final. Will not modify automaton {aut}.",s=state,aut=self.name)
    else:
        self.finalList.remove(state)  
                
##################

  def set_initial(self, state:str):
    """
    Sets the initial state of the automaton
    """
    if ( state == self.initial ):
        warn("State {s} is already initial. Will not modify automaton {aut}.",s=state,aut=self.name)
    else:
        self.initial=state
        
##################
  def get_intial(self) :
    
    return self.initial()
     

  def get_transitions(self) -> List[Tuple[str,chr,str]]:
    """
    Get the list of transitions of the automaton
    """
    return [x for x in self.transitionList]

##################
    
  def get_final(self) -> str:
    """
    Get a list of the final states of the automaton
    """
    return [x for x in self.finalList] 

##################
    
  def get_states(self) -> List[str]:
    """
    Get a list of states of the automaton
    """
    states=[]
    if (self.initial):
        states.append(self.initial)
    for (source,letter,target) in self.get_transitions():
        if source not in states:
            states.append(source)
        if target not in states:
            states.append(target)
    states+=[ x for x in self.get_final() if x not in states]
    return states
    
##################

  def get_alphabet(self,include_epsilon=False)->List[str]:
    """
    Get the letters used in the automaton, not including EPSILON by default
    """
    letters=[]
    epsilon_found=False
    for (source,letter,target) in self.transitionList:
        if (letter == EPSILON and not epsilon_found):
            epsilon_found=True
        if (letter not in letters and letter != EPSILON):
          letters.append(letter)
    if include_epsilon and epsilon_found:
        letters.append(EPSILON)
    return letters

##################
    
  def make_copy(self, b):
    """
    Makes a copy of automaton b, but keeps the name
    """
    self.initial=b.initial
    self.finalList=b.get_final()
    self.transitionList=b.get_transitions()

##################
    
  def transition_table(self)->str:
    """
    Return a string representing the transition table of the automaton
    """
    letters=self.get_alphabet(True)
    states=self.get_states()
    rows = [[""]+letters]
    for state in states:
        rows.append([state]+ [[] for i in range(len(letters))])
    for (source,letter,target) in self.transitionList:
        for i in range(len(states)):
            if (rows[i+1][0] == source):
                for j in range(len(letters)):
                    if (rows[0][j+1] == letter):
                        rows[i+1][j+1].append(target)
    
    maxlen=1
    for i in range(len(states)):
        maxlen=max(maxlen,len(rows[i+1][0]))
        for j in range(len(letters)):
            if len(rows[i+1][j+1]) == 0:
                rows[i+1][j+1]=""
            elif len(rows[i+1][j+1]) == 1:
                rows[i+1][j+1]=rows[i+1][j+1][0]
            else:
                rows[i+1][j+1]="{"+",".join(rows[i+1][j+1])+"}"
                
            if i==0 :
                maxlen=max(maxlen,len(rows[0][j+1]))
            maxlen=max(maxlen,len(rows[i+1][j+1]))
    res=""
    for row in rows:
        res += "|"+"|".join([("{:"+str(maxlen)+"}").format(c) for c in row])+"|\n"
        res += "-"*((maxlen+1)*len(row)+1) + "\n"
    
    return res
                	  
##################
    
  def __str__(self)->str:
    """
    Standard function to obtain a string representation of an automaton
    """
    alphabet_no_eps = [ x for x in self.get_alphabet() if x is not EPSILON ]
    tpl = "{A} = <Q={{{Q}}}, S={{{S}}}, D, q0={q0}, F={{{F}}}>\nD =\n{D}"    
    return tpl.format(A=self.name, Q=str(",".join(self.get_states())), S=",".join(alphabet_no_eps), q0=self.initial, F=",".join(self.get_final()), D=self.transition_table())
    
##################
    
  def to_txtfile(self, outfilename:str=None) -> str:
    """
    Save automaton into txt file.
    """
    res = ""
    if self.initial:
        res += "I "+self.initial+"\n"
    else:
        res += "I"+"\n"
    res += "F "
    res += " ".join([s for s in self.get_final()])
    for (source,letter,target) in self.get_transitions():
      res += "\n{} {} {}".format(source,letter,target)   
     
    if outfilename:
      if os.path.isfile(outfilename):
        warn("File {f} already exists, will be overwritten",f=outfilename)
      with open(outfilename,"w") as outfile:
        print(res,file=outfile)
    return res
    
##################

  def from_txt(self, text:str, name:str=None):
    """
    Reads from a txt source string and initializes automaton.
    """
    if not self.is_empty() :
      warn("Automaton {a} not empty: content will be lost",a=self.name)
    self.reset(name)
    rows = text.strip().split("\n")
    if len(rows) < 2:
      error("File must contain at least two lines")
    line1=rows[0].split(" ")
    if not line1[0] == "I":
      error("File must begin with \"I\" ")
    line2=rows[1].split(" ")
    if not line2[0] == "F":
      error("Second line must begin with \"F\" ")
    
    if len(line1) > 2:
        error("Only one line can be initial")
    if len(line1) == 2:
        self.initial=line1[1]
    line2=line2[1:]
    for state in line2:
        self.finalList.append(state)
    for (i,row) in enumerate(rows[2:]):
      try:
        (source,letter,target) = row.strip().split(" ")
        self.add_transition(source,letter,target)
      except ValueError:
        error("Malformed triple {t}",pos=name+":"+str(i+1),t=row.strip())
    

##################
    
  def from_txtfile(self, infilename:str):
    """
    Reads from txt file and initializes automaton.
    """    
    try:
      with open(infilename) as infile:
        rows = infile.readlines()
    except FileNotFoundError:
      error("File not found: {f}",f=infilename)
    name = os.path.splitext(os.path.basename(infilename))[0]
    return self.from_txt("".join(rows), name)

########################################################################
########################################################################

if __name__ == "__main__": # If the module is run from command line, test it
    a=Automaton("aut1")
    print(a)

    
    

    
