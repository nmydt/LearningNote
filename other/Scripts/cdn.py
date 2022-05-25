
import requests
import time
# URL工厂，转换URL
URLS = []

def UrlFactory(url, index=''):
    # cdn转github
    if "cdn.jsdelivr.net" in url:
        if url[-1] == "/":
            url = url[:-1]
        author = url.split("/")[4]
        repo = url.split("/")[5].split("@")[0]
        branch = url.split("/")[5].split("@")[1]
        others = '/'.join(url.split('/')[6:])
        if branch == 'main':
            return f"https://github.com/{author}/{repo}/blob/main/{others}"
        return f"https://github.com/{author}/{repo}/tree/{branch}/{others}"

    # github转cdn
    author = url.split("/")[3]
    repo = url.split("/")[4]
    if len(url.split("/")) == 5:
        return author,repo
        
    branch = url.split("/")[6]
    others = '/'.join(url.split('/')[7:])
    print(others,"others")
    fast_url = f"https://cdn.jsdelivr.net/gh/{author}/{repo}@{branch}/{others}"
    if index == 'directory':
        #         directory_url = f"https://api.github.com/repos/{author}/{repo}/contents/{others}?ref={branch}"
        return author, repo
    else:

        return fast_url
# 创建文件夹
def flush(url):
    global urls
    print("源url: "+url)
    author, repo = UrlFactory(url)
#     other = url.split("/")[-1]
    branch = "main"
    url1 = f"https://api.github.com/repos/{author}/{repo}/contents/?ref={branch}"
    
    r = requests.get(url1)
    r.close()

    print(r.text)
    jss = r.json()
    urls = []
    for js in jss:
        if js['type'] == 'dir':
            others = js['path']
            r2 = requests.get(f"https://api.github.com/repos/{author}/{repo}/git/trees/{js['sha']}?recursive=1")
            print("*"*30)
            print(f"https://api.github.com/repos/{author}/{repo}/git/trees/{js['sha']}?recursive=1")
            print(url1)
            print(others)
            r2.close()
            trees = r2.json()['tree']
            for tree in trees:
                if tree['type'] == 'blob':
                    url = f"https://github.com/{author}/{repo}/blob/{branch}/{others}/" + tree['path']
                    urls.append(url)
        else:
            url = js['_links']['html']
            urls.append(url)
    print(urls)
    
    for url_ in urls:
        url2 = UrlFactory(url_)
        URLS.append(url2)
repos = ["https://github.com/nmydt/LearningNote"]
for repo in repos:
    flush(repo)

    fails = []
    for url in URLS:
        url = url.replace("cdn.jsdelivr.net","purge.jsdelivr.net")
        print(url)
        r =  requests.get(url)
        r.close()
        time.sleep(0.1)
        name = '/'.join(url.split('/')[6:])
        if r.json()['paths']['/'+'/'.join(url.split('/')[3:])]['throttled']==True:
            time_ = str(format(int(r.json()['paths']['/'+'/'.join(url.split('/')[3:])]['throttlingReset'])/60,'.2f'))
            print(name,"刷新缓存失败",f"刷新间隔为：{time_}分钟")
            fails.append(url)
        else:
            print(name,"刷新成功！！！")
    print("失败的URL为")
    print(fails)
