package service

import (
	"user/dao"
	"user/entity"
)

func CreateUser(user *entity.User) (err error) {
	if err = dao.Db.Create(user).Error; err != nil {
		return err
	}
	return
}
func GetAllUser() (userList []*entity.User, err error) {
	if err := dao.Db.Find(&userList).Error; err != nil {
		return nil, err
	}
	return
}
func DeleteUserByStuffNo(stuffNo string) (err error) {
	if err = dao.Db.Where("stuff_no=?", stuffNo).Delete(&entity.User{}).Error; err != nil {
		return err
	}
	return
}
func GetUserByStuffNo(stuffNo string) (user *entity.User, err error) {
	if err = dao.Db.Where("stuff_no=?", stuffNo).First(&user).Error; err != nil {
		return nil, err
	}
	return
}
func GetUserByName(name string) (user *entity.User, err error) {
	if err = dao.Db.Where("name=?", name).First(&user).Error; err != nil {
		return nil, err
	}
	return
}
func UpdateUser(user *entity.User) (err error) {
	tx := dao.Db.Model(&user).Updates(&entity.User{
		StuffNo:    user.StuffNo,
		Name:       user.Name,
		Password:   user.Password,
		Info:       user.Info,
		Department: user.Department,
		Active:     true,
	}).Error
	if tx != nil {
		return tx
	}
	return
}
func login() {

}
