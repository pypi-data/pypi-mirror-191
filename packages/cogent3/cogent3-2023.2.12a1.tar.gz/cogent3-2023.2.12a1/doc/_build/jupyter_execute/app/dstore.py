#!/usr/bin/env python
# coding: utf-8

# In[1]:


import set_working_directory


# In[2]:


from cogent3 import open_data_store

dstore = open_data_store("data/raw.zip", suffix="fa*", limit=5, mode="r")


# In[3]:


m = dstore[0]
m


# In[4]:


m.read()[:20]  # truncating


# In[5]:


for m in dstore:
    print(m)


# In[6]:


dstore = open_data_store("data/demo-locked.sqlitedb")
dstore.describe


# In[7]:


dstore.unlock(force=True)


# In[8]:


dstore.summary_logs


# In[9]:


dstore.logs


# In[10]:


print(dstore.logs[0].read()[:225])  # truncated for clarity

