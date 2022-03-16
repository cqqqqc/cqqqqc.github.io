package main

import (
	"employee/dao"
	"employee/entity"
	"employee/route"
	"fmt"
	"github.com/go-ini/ini"
	"os"
)

func main() {
	//连接数据库
	dao.InitDB()
	//程序退出关闭数据库连接
	//defer dao.Close()
	//绑定模型
	dao.Db.AutoMigrate(&entity.Employee{})
	httpPort, err := ini.Load("conf/app.init")
	if err != nil {
		fmt.Printf("Fail to read file: %v", err)
		os.Exit(1)
	}
	//producer.UserQueue = producer.NewRabbitMQ("name", "exchange", "user")
	//producer.TaskQueue = producer.NewRabbitMQ("name", "exchange", "task")
	runPort := httpPort.Section("server").Key("HttpPort").String()
	//注册路由
	r := route.SetRouter()
	//启动端口为8085的项目
	r.Run(":" + runPort) //读取端口号
}
