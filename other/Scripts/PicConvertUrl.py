import os
import re
    
# URL工厂，转换URL
def UrlFactory(url):

    url = formatUrl(url)
 
    # cdn转github
    if "cdn.jsdelivr.net" in url:
        if url[-1]=="/":
            url = url[:-1]
        author = url.split("/")[4]
        repo = url.split("/")[5].split("@")[0]
        branch = url.split("/")[5].split("@")[1]
        others = '/'.join(url.split('/')[6:])
        if branch=='main':
            return f"https://github.com/{author}/{repo}/blob/main/{others}"
        return f"https://github.com/{author}/{repo}/tree/{branch}/{others}"
    
    # github转cdn
    file_d = url.split("/")[-1]
    author = url.split("/")[3]
    repo = url.split("/")[4]
    branch = url.split("/")[6]
    others = '/'.join(url.split('/')[7:-1])
    if others!='':
        others = others+"/"
    fast_url = f"https://cdn.jsdelivr.net/gh/{author}/{repo}@{branch}/{others}{file_d}"
    return fast_url

# 格式化URL
def formatUrl(url):
    if url[-1]=="/":
        return url[:-1]
    else:
        return url
#查找后缀文件
def findAllSuffix(target_dir, target_suffix="md"):
    find_res = []
    target_suffix_dot = "." + target_suffix
    walk_generator = os.walk(target_dir)
    for root_path, dirs, files in walk_generator:
        if len(files) < 1:
            continue
        for file in files:
            file_name, suffix_name = os.path.splitext(file)
            if suffix_name == target_suffix_dot:
                find_res.append(os.path.join(root_path, file))
    return find_res
def SingleConvert(filePath,repo,index):
    f = open(filePath,"r",encoding='utf-8')
    r = f.read()
    f.close()
    
    if index==1:  #     github => cdn       
        #    repo = "https://github.com/nmydt/LearningNote/tree/main/Concurrent"
        match = list(filter(lambda x:"https://cdn.jsdelivr.net/" not in x, re.findall(r"!\[.*?\]\((.*?)\)",r)))
        tuple_ = list(zip(match,list(map(lambda y:UrlFactory(y),map(lambda x:f"{repo}/"+x,match)))))
        for i in tuple_:
            r = r.replace(i[0],i[1])

    if index==2:  #     cdn => github
        global path_glo
        match = list(filter(lambda x:"https://cdn.jsdelivr.net/"  in x, re.findall(r"!\[.*?\]\((.*?)\)",r)))
        for i in match:
            r = r.replace(i,'/'.join(i.split("/")[-2:]))

    f = open(filePath,"w",encoding='utf-8')
    f.write(r)
    f.close()

if __name__ == '__main__':
    find_res = findAllSuffix("E:\\jupyter_test\\数据分析\\test\\LearningNote")[1:]
    path_glo = "https://github.com/nmydt/LearningNote/tree/main/"
    for path in find_res:
        print(path)
        path_ = path_glo +'/'.join(path.split("\\")[5:-1])
        if path_[-1]=="/":
            path_ = path_[:-1]
        print("path_"+path_)
        SingleConvert(path,path_,1)
    
