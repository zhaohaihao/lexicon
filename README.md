# 搜狗细胞词库爬虫器
## 介绍
之前为了给**押韵机器(微信小程序)**扩建词库<br/>
所以临时想出爬取搜狗的词库来进行筛选选用<br/>

## 目录结构
### **python部分**(python/Sougou-Spider)
这一部分主要是针对搜狗细胞词库网站，按照一级分类、二级分类的划分下载对应的scel文件。
采用的是用MongoDB(使用前自行安装，这里不做过多叙述)来存储一级分类、二级分类、三级分类对应的url、分类等相关信息。
```
|——lexicon	
	|——DBTool.py // MongoDB数据库存储工具, 配置在内部修改
	|——ScelFileDownload.py // 下载scel文件工具，对应的下载目标地址只需修改内部的共有变量**DIR**
	|——URLGrapTool.py // 所有分类对应的url、分类等相关信息的存储入库
```

### **Java部分**(java/scel-transform-tool)
这一部分主要是负责针对上述的scel加密文件进行解密成可见的txt文本。
```
|——src	
	|——main                                             
|		|——java					// 存放生成的代码
	|
|		|	|——com
	|
|		|	|	|——bigsea
	|
|		|	|	|	|——scel
	|
|		|	|	|	|	|——transform
	|
|		|	|	|	|	|	|——main
	|
|		|	|	|	|	|	|	|——AppMain.java // 项目启动项
	|
|		|	|	|	|	|	|——tool
	|
|		|	|	|	|	|	|	|——ScelTools.java // 搜狗SCEL文件转换工具
	|
|		|——resource
	|
|		|	|——log4j.properties // 日志配置
	|
|——bin
	|——sougou-tool.jar // 上述代码打成的jar包
	|——sougou-tool-start.bat // jar包执行程序
```

### 使用方法
1. **修改文件保存目录:** 进入 `python` 目录, 找到 `ScelFileDownload.py`, 修改内部的共有变量 `DIR` 作为爬取词库文件的保存目录<br/>
2. **执行python:** 打开 `cmd` 命令窗口, 执行 `python ScelFileDownload.py` 命令。(未安装 `python` 环境的, 自行百度、谷歌安装)<br/>
3. **执行java解密文件:** 将 `bin` 文件夹与步骤1文件的保存目录同目录放置, 进入 `bin` 文件, 双击 `sougou-tool-start.bat` 执行即可。<br/>
