# Gorm+Gin Demo

### 技术文档：

* gin:https://www.topgoer.com/gin%E6%A1%86%E6%9E%B6/%E7%AE%80%E4%BB%8B.html

* gorm: https://gorm.io/zh_CN/docs/conventions.html

* go:https://books.studygolang.com/gopl-zh/ch6/ch6-04.html

### 项目结构：

* conf：存放数据库配置以及之后的微服务注册发现配置
* documents：存放改动小的文件
* repository：
  * initDB：初始化数据库
  * others：项目所需要用到的类，并在类中写访问数据库的方法。类似于DAO

* utils：一些公用的方法
* app.go：作为主类运行项目

