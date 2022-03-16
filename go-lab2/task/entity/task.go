package entity

import (
	"gorm.io/gorm"
	"time"
)

type Task struct {
	//gorm.Model
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	StuffNo   string         `gorm:"primaryKey" json:"stuff_no" binding:"required"`
	TaskInfo  string         `json:"task_info"`
	TaskNo    string         `gorm:"primaryKey" json:"task_no" binding:"required"`
	Status    bool           `gorm:"not null" json:"status"`
}
