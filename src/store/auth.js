export default {
    isAuthenticated() {
      return !!localStorage.getItem('user');
    },
    login(user) {
      localStorage.setItem('user', JSON.stringify(user));
    },
    logout() {
      localStorage.removeItem('user');
    }
  };
  