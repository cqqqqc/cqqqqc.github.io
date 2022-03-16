package route

import (
	"github.com/gin-gonic/gin"
	"task/controller"
)

func SetRouter() *gin.Engine {
	r := gin.Default()

	/**
	  用户User路由组
	*/
	userGroup := r.Group("task")
	{
		//增加用户User
		userGroup.POST("/create", controller.CreateTask)
		//查看所有的User
		userGroup.GET("", controller.GetAllTask)
		userGroup.GET("/stuff/:stuffNo", controller.GetTasksByStuffNo)
		userGroup.GET("/task/:taskNo", controller.GetTaskByTaskNo)
		//修改某个User
		userGroup.PUT("/:taskNo", controller.UpdateTask)
		//删除某个User
		userGroup.DELETE("/stuff/:stuffNo", controller.DeleteTasksByStuffNo)
		userGroup.DELETE("/task/:taskNo", controller.DeleteTasksByTaskNo)
	}

	return r
}
