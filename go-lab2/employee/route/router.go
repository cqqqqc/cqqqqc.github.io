package route

import (
	"employee/controller"
	"github.com/gin-gonic/gin"
)

func SetRouter() *gin.Engine {
	r := gin.Default()

	/**
	  用户User路由组
	*/
	userGroup := r.Group("employee")
	{
		//增加用户User
		userGroup.POST("/create", controller.CreateEmployee)
		//查看所有的User
		userGroup.GET("", controller.GetAllEmployee)
		userGroup.GET("/:stuffNo", controller.GetEmployeeByStuffNo)
		//修改某个User
		userGroup.PUT("/:stuffNo", controller.UpdateEmployee)
		//删除某个User
		userGroup.DELETE("/:stuffNo", controller.DeleteEmployeeByStuffNo)
	}

	return r
}
