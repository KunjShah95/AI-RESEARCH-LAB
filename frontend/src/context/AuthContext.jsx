import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  
  const login = (email) => {
    setUser({ email, name: email.split('@')[0] })
    return true
  }
  
const signup = (name, email) => {
    setUser({ email, name })
    return true
  }

  const loginWithGoogle = () => {
    const googleUser = {
      email: 'user@gmail.com',
      name: 'Google User',
      avatar: 'https://lh3.googleusercontent.com/a/default',
      provider: 'google'
    }
    setUser(googleUser)
    return true
  }

  const logout = () => setUser(null)
  
  return (
    <AuthContext.Provider value={{ user, login, signup, loginWithGoogle, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}