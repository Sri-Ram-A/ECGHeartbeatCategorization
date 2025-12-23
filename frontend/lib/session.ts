export interface UserSession {
  id: number;
  full_name: string;
}

export const setSession = (user: UserSession) => {
  if (typeof window !== 'undefined') {
    sessionStorage.setItem('user', JSON.stringify(user));
  }
};

export const getSession = (): UserSession | null => {
  if (typeof window !== 'undefined') {
    const userStr = sessionStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
  return null;
};

export const clearSession = () => {
  if (typeof window !== 'undefined') {
    sessionStorage.removeItem('user');
  }
};