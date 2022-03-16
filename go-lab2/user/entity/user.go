package entity

import (
	"gorm.io/gorm"
	"time"
)

type User struct {
	//gorm.Model
	CreatedAt  time.Time
	UpdatedAt  time.Time
	DeletedAt  gorm.DeletedAt `gorm:"index"`
	Name       string         `gorm:"not null" json:"name" binding:"required"`
	Password   string         `gorm:"not null" json:"password" binding:"required"`
	Info       string         `json:"info"`
	StuffNo    string         `gorm:"primaryKey" json:"stuff_no" binding:"required"`
	Department string         `json:"department"`
	Active     bool           `gorm:"not null" json:"active"`
}
