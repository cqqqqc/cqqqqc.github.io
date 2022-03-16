package service

import (
	"math/rand"
	"task/dao"
	"task/entity"
)

var letters = []rune("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func RandSeq(n int) string {
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}
func CreateTask(task *entity.Task) (err error) {
	if err = dao.Db.Create(task).Error; err != nil {
		return err
	}
	return
}
func GetAllTask() (taskList []*entity.Task, err error) {
	if err := dao.Db.Find(&taskList).Error; err != nil {
		return nil, err
	}
	return
}
func DeleteTasksByStuffNo(stuffNo string) (err error) {
	if err = dao.Db.Where("stuff_no=?", stuffNo).Delete(&entity.Task{}).Error; err != nil {
		return err
	}
	return
}
func DeleteTasksByTaskNo(taskNo string) (err error) {
	if err = dao.Db.Where("task_no=?", taskNo).Delete(&entity.Task{}).Error; err != nil {
		return err
	}
	return
}
func GetTasksByStuffNo(stuffNo string) (taskList []*entity.Task, err error) {
	if err = dao.Db.Where("stuff_no=?", stuffNo).Find(&taskList).Error; err != nil {
		return nil, err
	}
	return
}
func GetTaskByTaskNo(taskNo string) (task *entity.Task, err error) {
	if err = dao.Db.Where("task_no=?", taskNo).First(&task).Error; err != nil {
		return nil, err
	}
	return
}
func UpdateTask(task *entity.Task) (err error) {
	tx := dao.Db.Model(&task).Updates(&entity.Task{
		StuffNo:  task.StuffNo,
		TaskInfo: task.TaskInfo,
		TaskNo:   task.TaskNo,
		Status:   true,
	}).Error
	if tx != nil {
		return tx
	}
	return
}
