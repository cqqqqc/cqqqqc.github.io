package controller

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"task/entity"
	"task/service"
)

func CreateTask(c *gin.Context) {
	//定义一个User变量
	var task entity.Task
	//将调用后端的request请求中的body数据根据json格式解析到User结构变量中
	c.BindJSON(&task)
	//将被转换的user变量传给service层的CreateUser方法，进行User的新建
	err := service.CreateTask(&task)
	//判断是否异常，无异常则返回包含200和更新数据的信息
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": task,
		})
	}
}
func GetAllTask(c *gin.Context) {
	userList, err := service.GetAllTask()
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
func UpdateTask(c *gin.Context) {
	//定义一个User变量
	var task entity.Task
	//将调用后端的request请求中的body数据根据json格式解析到User结构变量中
	c.BindJSON(&task)
	//将被转换的user变量传给service层的CreateUser方法，进行User的新建
	err := service.UpdateTask(&task)
	//判断是否异常，无异常则返回包含200和更新数据的信息
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": task,
		})
	}
}
func DeleteTasksByStuffNo(c *gin.Context) {
	err := service.DeleteTasksByStuffNo(c.Param("stuffNo"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
		})
	}
}
func DeleteTasksByTaskNo(c *gin.Context) {
	err := service.DeleteTasksByStuffNo(c.Param("taskNo"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
		})
	}
}
func GetTasksByStuffNo(c *gin.Context) {
	user, err := service.GetTasksByStuffNo(c.Param("stuffNo"))
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
func GetTaskByTaskNo(c *gin.Context) {
	user, err := service.GetTaskByTaskNo(c.Param("taskNo"))
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
