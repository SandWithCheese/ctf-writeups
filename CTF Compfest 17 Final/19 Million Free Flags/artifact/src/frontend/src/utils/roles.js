export const ROLE_NAMES = {
  0: 'User',
  1: 'Administrator'
}

export const ROLE_COLORS = {
  0: 'bg-blue-100 text-blue-800',
  1: 'bg-red-100 text-red-800'
}

export const ROLE_DESCRIPTIONS = {
  0: 'Regular user with basic access',
  1: 'Administrator with full system access'
}

export function getRoleName(role) {
  return ROLE_NAMES[role] || 'Unknown'
}

export function getRoleColor(role) {
  return ROLE_COLORS[role] || 'bg-gray-100 text-gray-800'
}

export function getRoleDescription(role) {
  return ROLE_DESCRIPTIONS[role] || 'Unknown role'
}

export function isAdmin(user) {
  return user && user.role === 1
}

export function canAccessInternal(user) {
  return isAdmin(user)
}
