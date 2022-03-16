package producer

import (
	"employee/entity"
	"employee/service"
	"encoding/json"
	"github.com/streadway/amqp"
)

//路由模式Step：2、路由模式下生产代码
func (r *RabbitMQ) PublishgRouting(data entity.SimpleDemo) {
	//1、尝试创建交换机
	err := r.channel.ExchangeDeclare(
		r.Exchange,
		"direct", //路由类型
		true,
		false,
		//true表示这个exchange不可以被client用来推送消息，仅用来进行exchange和exchange之间的绑定
		false,
		false,
		nil,
	)
	r.failOnErr(err, "Failed t declare an exchange")

	//2、发送消息
	dataBytes, err := json.Marshal(data)
	if err != nil {
		service.FailOnError(err, "struct to json failed")
	}
	err = r.channel.Publish(
		r.Exchange,
		r.Key,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        dataBytes,
		})
}
