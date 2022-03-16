package entity

import (
	"gorm.io/gorm"
	"time"
)

type Employee struct {
	//gorm.Model
	CreatedAt  time.Time
	UpdatedAt  time.Time
	DeletedAt  gorm.DeletedAt `gorm:"index"`
	Name       string         `gorm:"not null" json:"name" binding:"required"`
	StuffNo    string         `gorm:"primaryKey" json:"stuff_no" binding:"required"`
	Department string         `json:"department"`
}
