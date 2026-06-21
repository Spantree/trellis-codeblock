import { retry } from './retry'

const data = await retry(
  () => fetch('/api/status').then((r) => r.json()),
  5,
)

console.log('status:', data.ok)
