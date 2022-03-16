package producer

import (
	"fmt"
	"github.com/streadway/amqp"
	"log"
)

// url格式 amqp://账号:密码@rabbitmq服务器地址:端口号/vhost
const MQURL = "amqp://admin:admin@47.100.60.194:5672"

var UserQueue *RabbitMQ
var TaskQueue *RabbitMQ

type RabbitMQ struct {
	conn      *amqp.Connection
	channel   *amqp.Channel
	QueueName string //队列名称
	Exchange  string //交换机
	Key       string //Key
	Mqurl     string //连接信息
}

// 断开channel和connection
func (r *RabbitMQ) Destory() {
	r.channel.Close()
	r.conn.Close()
}

//错误处理函数
func (r *RabbitMQ) failOnErr(err error, message string) {
	if err != nil {
		log.Fatalf("%s:%s\n", message, err)
		panic(fmt.Sprintf("%s:%s", message, err))
	}
}

// 创建RabbitMQ结构体实例
func NewRabbitMQ(queueName string, exchange string, key string) *RabbitMQ {
	rabbitMQ := &RabbitMQ{
		QueueName: queueName,
		Exchange:  exchange,
		Key:       key,
		Mqurl:     MQURL,
	}
	var err error
	//创建rabbitmq连接
	rabbitMQ.conn, err = amqp.Dial(rabbitMQ.Mqurl)
	rabbitMQ.failOnErr(err, "创建连接错误")
	rabbitMQ.channel, err = rabbitMQ.conn.Channel()
	rabbitMQ.failOnErr(err, "获取Channel失败")
	return rabbitMQ
}

//路由模式Step：1、创建路由模式下RabbitMQ实例
func NewRabbitMQRouting(exchangeName string, routingKey string) *RabbitMQ {
	//创建RabbitMq实例
	return NewRabbitMQ("", exchangeName, routingKey)
}
