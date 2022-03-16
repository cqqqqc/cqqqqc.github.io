package dao

import (
	"fmt"
	"github.com/go-ini/ini"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"os"
	"strings"
	"user/entity"
)

var Db *gorm.DB

func InitDB() *gorm.DB {
	// 读取conf配置文件的数据库配置信息
	dbConfig, err := ini.Load("conf/app.init")
	if err != nil {
		fmt.Printf("Fail to read file: %v", err)
		os.Exit(1)
	}
	userName := dbConfig.Section("database").Key("User").String()
	pwd := dbConfig.Section("database").Key("Password").String()
	ip := dbConfig.Section("database").Key("Ip").String()
	port := dbConfig.Section("database").Key("Port").String()
	dbName := dbConfig.Section("database").Key("DBName").String()
	path := strings.Join([]string{userName, ":", pwd, "@tcp(", ip, ":", port, ")/", dbName, "?charset=utf8&parseTime=true"}, "")
	// 打开数据库
	mysqlConfig := mysql.New(mysql.Config{
		DSN:                       path,  // DSN data source name
		DefaultStringSize:         256,   // string 类型字段的默认长度
		DisableDatetimePrecision:  true,  // 禁用 datetime 精度，MySQL 5.6 之前的数据库不支持
		DontSupportRenameIndex:    true,  // 重命名索引时采用删除并新建的方式，MySQL 5.7 之前的数据库和 MariaDB 不支持重命名索引
		DontSupportRenameColumn:   true,  // 用 `change` 重命名列，MySQL 8 之前的数据库和 MariaDB 不支持重命名列
		SkipInitializeWithVersion: false, // 根据当前 MySQL 版本自动配置
	})
	Db, err = gorm.Open(mysqlConfig, &gorm.Config{})
	if err != nil {
		//如果打开数据库错误，直接panic
		panic(err)
	}
	fmt.Printf("Database connected!")
	Db.Set("gorm:table_options", "ENGINE=InnoDB").AutoMigrate(&entity.User{})
	return Db
}
