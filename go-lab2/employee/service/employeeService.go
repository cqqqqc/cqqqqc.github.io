package service

import (
	"employee/dao"
	"employee/entity"
	"math/rand"
)

var letters = []rune("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func RandSeq(n int) string {
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}
func CreateEmployee(employee *entity.Employee) (err error) {
	if err = dao.Db.Create(employee).Error; err != nil {
		return err
	}
	return
}
func GetAllEmployee() (employeeList []*entity.Employee, err error) {
	if err := dao.Db.Find(&employeeList).Error; err != nil {
		return nil, err
	}
	return
}
func DeleteEmployeeByStuffNo(stuffNo string) (err error) {
	if err = dao.Db.Where("stuff_no=?", stuffNo).Delete(&entity.Employee{}).Error; err != nil {
		return err
	}
	return
}
func GetEmployeeByStuffNo(stuffNo string) (employee *entity.Employee, err error) {
	if err = dao.Db.Where("stuff_no=?", stuffNo).First(&employee).Error; err != nil {
		return nil, err
	}
	return
}
func UpdateEmployee(employee *entity.Employee) (err error) {
	tx := dao.Db.Model(&employee).Updates(&entity.Employee{
		StuffNo:    employee.StuffNo,
		Name:       employee.Name,
		Department: employee.Department,
	}).Error
	if tx != nil {
		return tx
	}
	return
}
