# toomics_comic_spider
首先不得不说toomics玩漫漫画网上的漫画，很难爬取，1.网站有添加了图片反爬机制，请求的时候必须加上referer的请求头，2.网站需要登录才可以进行爬取（因为这个网站的漫画都是要钱的，）所以呢必须的登录才可以进行下一步的爬取工作，我之前用fiddler抓包到了toomics的登录的url，之后用urllib的解析以及requests的请求试了很多遍，一直没有成功，所以就手动的将网页保存下来，然后再进行解析，下载漫画，这样的话就显得有些笨拙了，对于我这个python开发者来说，这个是deny的！

  其实这样也是很好的，先使用一些基础的爬取模块，进行一些基础的练习，这样可以对知识更好的理解，知道之后自己接触了一个强大的scrapy框架，这个简直是爬虫的利器，一个是解析很快，里面有很多的开放的api模块，比如说form表单提交的功能，这样很是方便登录， 二是，scrapy采用的异步下载和解析引擎，下载和解析几乎是同步的，超级的快！废话不多说，快来show me coding！
