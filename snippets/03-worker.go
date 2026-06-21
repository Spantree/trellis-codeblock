package main

import (
	"context"
	"fmt"
	"time"
)

func worker(ctx context.Context, id int, jobs <-chan int) {
	for {
		select {
		case <-ctx.Done():
			return
		case j := <-jobs:
			fmt.Printf("worker %d handled job %d\n", id, j)
			time.Sleep(50 * time.Millisecond)
		}
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	jobs := make(chan int, 8)
	for i := 0; i < 3; i++ {
		go worker(ctx, i, jobs)
	}
	<-ctx.Done()
}
