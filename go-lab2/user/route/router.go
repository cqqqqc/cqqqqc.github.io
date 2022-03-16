package route

import (
	"github.com/gin-gonic/gin"
	"user/controller"
)

func SetRouter() *gin.Engine {
	r := gin.Default()

	/**
	  用户User路由组
	*/
	userGroup := r.Group("user")
	{
		//增加用户User
		userGroup.POST("/register", controller.CreateUser)
		userGroup.POST("/login", controller.Login)
		//查看所有的User
		userGroup.GET("", controller.GetUserList)
		userGroup.GET("/:stuffNo", controller.GetUserByStuffNo)
		//修改某个User
		userGroup.PUT("/:stuffNo", controller.UpdateUser)
		//删除某个User
		userGroup.DELETE("/:stuffNo", controller.DeleteUserByStuffNo)
	}

	return r
}
