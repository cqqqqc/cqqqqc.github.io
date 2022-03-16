package controller

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"user/entity"
	"user/producer"
	"user/service"
)

type login struct {
	UserName string `json:"name" form:"name" binding:"required"`
	Password string `json:"password" form:"password" binding:"required"`
}

func Login(c *gin.Context) {
	var loginInfo login
	c.BindJSON(&loginInfo)
	name := loginInfo.UserName
	password := loginInfo.Password
	//先判断用户是否存在，存在再判断密码是否正确
	user, err := service.GetUserByName(name)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		if password != user.Password {
			c.JSON(http.StatusBadRequest, gin.H{
				"code": 400,
				"msg":  "wrong password",
			})
		} else {
			c.JSON(http.StatusOK, gin.H{
				"code": 200,
				"msg":  "success",
			})
		}
	}
}

func CreateUser(c *gin.Context) {
	//定义一个User变量
	var user entity.User
	//将调用后端的request请求中的body数据根据json格式解析到User结构变量中
	c.BindJSON(&user)
	//将被转换的user变量传给service层的CreateUser方法，进行User的新建
	err := service.CreateUser(&user)
	//判断是否异常，无异常则返回包含200和更新数据的信息
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": user,
		})
	}
}

func GetUserList(c *gin.Context) {
	userList, err := service.GetAllUser()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": userList,
		})
	}
}

func UpdateUser(c *gin.Context) {
	//定义一个User变量
	var user entity.User
	//将调用后端的request请求中的body数据根据json格式解析到User结构变量中
	c.BindJSON(&user)

	taskData := entity.SimpleDemo{
		Name:     user.Name,
		StuffNo:  user.StuffNo,
		TaskNo:   "",
		Password: "123456",
		Active:   false,
		Info:     "task",
	}
	rabbitMQ := producer.NewRabbitMQRouting("change", "task")
	rabbitMQ.PublishgRouting(taskData)

	//将被转换的user变量传给service层的CreateUser方法，进行User的新建
	err := service.UpdateUser(&user)
	//判断是否异常，无异常则返回包含200和更新数据的信息
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": user,
		})
	}
}
func DeleteUserByStuffNo(c *gin.Context) {
	err := service.DeleteUserByStuffNo(c.Param("stuffNo"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
		})
	}
}
func GetUserByStuffNo(c *gin.Context) {
	user, err := service.GetUserByStuffNo(c.Param("stuffNo"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": user,
		})
	}
}
