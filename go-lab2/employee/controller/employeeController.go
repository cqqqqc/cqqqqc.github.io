package controller

import (
	"employee/entity"
	"employee/producer"
	"employee/service"
	"github.com/gin-gonic/gin"
	"net/http"
)

func CreateEmployee(c *gin.Context) {
	//定义一个User变量
	var employee entity.Employee
	//将调用后端的request请求中的body数据根据json格式解析到User结构变量中
	c.BindJSON(&employee)

	taskNo := service.RandSeq(4)
	userData := entity.SimpleDemo{
		Name:       employee.Name,
		StuffNo:    employee.StuffNo,
		TaskNo:     taskNo,
		Department: employee.Department,
		Password:   "123456",
		Active:     false,
	}
	taskData := entity.SimpleDemo{
		Name:       employee.Name,
		StuffNo:    employee.StuffNo,
		TaskNo:     taskNo,
		Department: employee.Department,
		Password:   "123456",
		Active:     false,
	}
	rabbitMQOne := producer.NewRabbitMQRouting("exchange", "user")
	rabbitMQTwo := producer.NewRabbitMQRouting("exchange", "task")
	rabbitMQOne.PublishgRouting(userData)
	rabbitMQTwo.PublishgRouting(taskData)

	//将被转换的user变量传给service层的CreateUser方法，进行User的新建
	employeeErr := service.CreateEmployee(&employee)
	//判断是否异常，无异常则返回包含200和更新数据的信息
	if employeeErr != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": employeeErr.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": employee,
		})
	}

}
func GetAllEmployee(c *gin.Context) {
	employeeList, err := service.GetAllEmployee()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": employeeList,
		})
	}
}
func UpdateEmployee(c *gin.Context) {
	//定义一个User变量
	var employee entity.Employee
	//将调用后端的request请求中的body数据根据json格式解析到User结构变量中
	c.BindJSON(&employee)
	//将被转换的user变量传给service层的CreateUser方法，进行User的新建
	err := service.UpdateEmployee(&employee)
	//判断是否异常，无异常则返回包含200和更新数据的信息
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
			"data": employee,
		})
	}
}
func DeleteEmployeeByStuffNo(c *gin.Context) {
	err := service.DeleteEmployeeByStuffNo(c.Param("stuffNo"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"code": 200,
			"msg":  "success",
		})
	}
}
func GetEmployeeByStuffNo(c *gin.Context) {
	user, err := service.GetEmployeeByStuffNo(c.Param("stuffNo"))
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
