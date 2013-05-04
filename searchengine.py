#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dan
#
# Created:     19/09/2012
# Copyright:   (c) Dan 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
#Finish crawl web

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index={}
    graph={}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content=get_page(page)
            add_page_to_index(index,page,content)
            outlinks=get_all_links(content)
            graph[page]=outlinks
            union(tocrawl,outlinks)
            crawled.append(page)
    return index,graph

def record_user_click(index,keyword,url):
    urls=lookup(index,keyword)
    if urls:
        for entry in urls:
            if entry[0]==url:
                entry[1]=entry[1]+1

def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword]=[url]


def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index,url,content):
    words=content.split()
    for word in words:
        add_to_index(index,word,url)

def split_string(source,splitlist):
    output=[]
    atsplit=True
    for char in source:
        if char in splitlist:
            atsplit=True
        else:
            if atsplit:
                output.append(char)
                atsplit=False
            else:
                output[-1]=output[-1]+ char
    return output

def hash_string(keywords,buckets):
    h=0
    for c in keywords:
        h=(h+ord(c))%buckets
    return h

def make_hashtable(nbuckets):
    i=0
    table=[]
    for unused in range(0,nbuckets):
        table.append([])

    return table
def hashtable_get_bucket(htable, key):
    return htable[hash_string(key, len(htable))]


def hashtable_add(htable,key,value):
    hashtable_get_bucket(htable,key).append([key,value])


def hashtable_lookup(htable,key):
    bucket=hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0]==key:
            return entry[1]
    return None

def hashtable_update(htable,key,value):
    bucket=hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0]==key:
            entry[1]==value
            return
    bucket.append([key,value])


def compute_ranks(graph):
    d=0.8 #damping factor
    numloops=10
    ranks={}
    npages=len(graph)
    for page in graph:
        ranks[page]=1.0 / npages
    for i in range(0,numloops):
        newranks={}
        for page in graph:
            newrank=(1-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank=newrank + d* (ranks[node]/ len(graph[node]))
            newranks[page]=newrank
        ranks=newranks
    return ranks

def lucky_search(index,ranks,keyword):
    pages=lookup(index,keyword)
    if not  pages:
        return None
    best_page=pages[0]
    for candidate in pages:
        if ranks[candidate]>ranks[best_page]:
            best_page=candidate
    return best_page


def quicksort_pages(pages,ranks):
    if not pages or len(pages)<=1:
        return pages
    else:
        pivot=ranks[pages[0]]
        worse=[]
        better=[]
        for page in pages[1:]:
            if ranks[page]<=pivot:
                worse.append(page)
            else:
                better.append(page)
        return quicksort_pages(better,ranks) + [pages[0]] + quicksort_pages(worse,ranks)





def ordered_search(index,ranks,keyword):
    pages=lookup(index,keyword)
    return quicksort_pages(pages,ranks)






