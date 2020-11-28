#!/usr/bin/env python
# coding: utf-8

# # Helper - fields Enum

# In[1]:


from enum import IntEnum, auto

class fields(IntEnum):
    traceId = 0
    startTime = auto()
    spanId = auto()
    parentSpanId = auto()
    duration = auto()
    serviceName = auto()
    spanName = auto()
    host = auto()
    tags = auto()

def print_head(obj, rows_num=10):
    for i, row in enumerate(obj):
        if i >= rows_num:
            break
        print(row)
        
# end


# # Start

# In[2]:


split1_raw = open('trace1.data').read()
split2_raw = open('trace2.data').read()

split_raws = [split1_raw, split2_raw]


# # Brutal
# 1. 找到异常的traceId，遍历发送到后端

# In[3]:


def parse(split_raw):
    return map(lambda x: x.split('|'), split_raw.split('\n'))


# In[4]:


# 1 split contains multiple spans
splits = map(lambda split_raw: parse(split_raw), split_raws)


# In[5]:


def _isValid(tags_raw: str):
    if 'http.status_code=200' in tags_raw:
        return True
    elif 'http.status_code=' in tags_raw:
        return False
    elif 'error=1' in tags_raw:
        return False
    else:
        return True


# In[6]:


def get_error_traceIds(spans):
    error_traceIds = set()
    for span in spans:
        if span[fields.traceId] in error_traceIds:
            continue
        if not _isValid(span[fields.tags]):
            error_traceIds.add(span[fields.traceId])
    
    return error_traceIds


# In[7]:


error_traceIds_list = map(lambda split: get_error_traceIds(split), splits)


# In[8]:


print_head(error_traceIds_list)


# In[ ]:




