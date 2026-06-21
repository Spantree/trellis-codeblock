import { reactive, computed } from 'vue'

interface Todo {
  id: number
  text: string
  done: boolean
}

const state = reactive({
  todos: [] as Todo[],
  filter: 'all' as 'all' | 'active' | 'done',
})

let nextId = 1

export function addTodo(text: string): void {
  state.todos.push({ id: nextId++, text, done: false })
}

export function toggle(id: number): void {
  const todo = state.todos.find((t) => t.id === id)
  if (todo) todo.done = !todo.done
}

export const visible = computed(() => {
  switch (state.filter) {
    case 'active':
      return state.todos.filter((t) => !t.done)
    case 'done':
      return state.todos.filter((t) => t.done)
    default:
      return state.todos
  }
})

export const remaining = computed(
  () => state.todos.filter((t) => !t.done).length,
)
