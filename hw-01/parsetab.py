
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftIFFIFTHENleftORleftANDrightNOTAND FALSE IFF IFTHEN LBRAC NOT OR RBRAC TRUE VARexpression : VARexpression : TRUEexpression : FALSEexpression : LBRAC expression RBRACexpression : NOT expressionexpression : expression AND expressionexpression : expression OR expressionexpression : expression IFTHEN expressionexpression : expression IFF expression'
    
_lr_action_items = {'VAR':([0,5,6,7,8,9,10,],[2,2,2,2,2,2,2,]),'TRUE':([0,5,6,7,8,9,10,],[3,3,3,3,3,3,3,]),'FALSE':([0,5,6,7,8,9,10,],[4,4,4,4,4,4,4,]),'LBRAC':([0,5,6,7,8,9,10,],[5,5,5,5,5,5,5,]),'NOT':([0,5,6,7,8,9,10,],[6,6,6,6,6,6,6,]),'$end':([1,2,3,4,12,13,14,15,16,17,],[0,-1,-2,-3,-5,-6,-7,-8,-9,-4,]),'AND':([1,2,3,4,11,12,13,14,15,16,17,],[7,-1,-2,-3,7,-5,-6,7,7,7,-4,]),'OR':([1,2,3,4,11,12,13,14,15,16,17,],[8,-1,-2,-3,8,-5,-6,-7,8,8,-4,]),'IFTHEN':([1,2,3,4,11,12,13,14,15,16,17,],[9,-1,-2,-3,9,-5,-6,-7,-8,-9,-4,]),'IFF':([1,2,3,4,11,12,13,14,15,16,17,],[10,-1,-2,-3,10,-5,-6,-7,-8,-9,-4,]),'RBRAC':([2,3,4,11,12,13,14,15,16,17,],[-1,-2,-3,17,-5,-6,-7,-8,-9,-4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,5,6,7,8,9,10,],[1,11,12,13,14,15,16,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> VAR','expression',1,'p_expression_var','tst.py',55),
  ('expression -> TRUE','expression',1,'p_expression_true','tst.py',59),
  ('expression -> FALSE','expression',1,'p_expression_false','tst.py',63),
  ('expression -> LBRAC expression RBRAC','expression',3,'p_expression_brackets','tst.py',67),
  ('expression -> NOT expression','expression',2,'p_expression_not','tst.py',71),
  ('expression -> expression AND expression','expression',3,'p_expression_and','tst.py',76),
  ('expression -> expression OR expression','expression',3,'p_expression_or','tst.py',81),
  ('expression -> expression IFTHEN expression','expression',3,'p_expression_ifthen','tst.py',86),
  ('expression -> expression IFF expression','expression',3,'p_expression_iff','tst.py',91),
]
