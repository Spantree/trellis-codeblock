interface User {
  id: string
  name: string
  roles: Role[]
}

type Role = 'admin' | 'editor' | 'viewer'

class UserStore {
  private users = new Map<string, User>()

  add(user: User): void {
    this.users.set(user.id, user)
  }

  admins(): User[] {
    return [...this.users.values()].filter((u) =>
      u.roles.includes('admin'),
    )
  }
}
