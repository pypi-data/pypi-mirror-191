#!/usr/bin/env python
# coding: utf-8

# In[1]:


import set_working_directory


# In[2]:


from cogent3 import get_app

reader = get_app("load_aligned", format="fasta")
select_seqs = get_app("take_named_seqs", "Mouse", "Human")
aln = reader("data/primate_brca1.fasta")
result = select_seqs(aln)
result


# In[3]:


result == False
result.type
result.message


# In[4]:


result = reader("primate_brca1.fasta")
result


# In[5]:


process = reader + select_seqs
result = process("data/primate_brca1.fasta")
result


# In[6]:


result = process("primate_brca1.fasta")
result

