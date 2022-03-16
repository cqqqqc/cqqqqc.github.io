package main

import (
	"fmt"
	"github.com/go-ini/ini"
	"os"
	"task/consumer"
	"task/dao"
	"task/entity"
	"task/route"
)

func main() {
	//连接数据库
	dao.InitDB()
	//程序退出关闭数据库连接
	//defer dao.Close()
	//绑定模型
	dao.Db.AutoMigrate(&entity.Task{})
	httpPort, err := ini.Load("conf/app.init")
	if err != nil {
		fmt.Printf("Fail to read file: %v", err)
		os.Exit(1)
	}
	runPort := httpPort.Section("server").Key("HttpPort").String()
	//注册路由
	r := route.SetRouter()

	rabbimq1 := consumer.NewRabbitMQRouting("exchange", "task")
	rabbimq1.TaskReceiveRouting()

	rabbimq2 := consumer.NewRabbitMQRouting("change", "task")
	rabbimq2.TaskReceiveRouting2()

	//启动端口为8085的项目
	r.Run(":" + runPort) //读取端口号
}
