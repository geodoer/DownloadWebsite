> 爬取开源技术文档，并翻译

【步骤一】sipder.py
1. 从start_url开始，获得所有指定域名DOMAIN下的网页资源列表
2. 包括HTML、静态资源（js、css、txt等）、图片（png、gif）
3. HTML为原始网页渲染之后的结果

【步骤二】download.py
1. 根据第一步所爬取的网址表单下载

【步骤三】翻译网页的所有内容