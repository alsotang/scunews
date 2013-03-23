# coding=utf-8

config = {
	"news": {
        "site_name": "川大新闻网",
		"url": "http://news.scu.edu.cn/news2012/cdzx/I0201index_1.htm",
		"url_pattern": r"^/news2012/cdzx/webinfo",
		"prefix_url": "http://news.scu.edu.cn",
		"encoding": "gbk"
	},
    # "sw": {
    #     "site_name": "软件学院",
    #     "url": "http://sw.scu.edu.cn/",
    #     "url_pattern": r"^/sw/\w+/\w+/webinfo/\d+/\d+/\d+.htm$",
    #     "prefix_url": "http://sw.scu.edu.cn/",
    #     "encoding": "gbk"
    # },
    "sculj": {
        "site_name": "文新学院",
        "url": "http://www.sculj.cn/Special_News.asp?SpecialID=41&SpecialName=%B1%BE%D5%BE%B5%BC%B6%C1",
        "url_pattern": r'^ReadNews.asp',
        "prefix_url": "http://www.sculj.cn/",
        "encoding": "gb2312"
    },

}