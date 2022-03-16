package consumer

type SimpleDemo struct {
	Name       string `json:"name"`
	StuffNo    string `json:"stuff_no"`
	TaskNo     string `json:"task_no"`
	Department string `json:"department"`
	Password   string `json:"password"`
	Active     bool   `json:"active"`
}
