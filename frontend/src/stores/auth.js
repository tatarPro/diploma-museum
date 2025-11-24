import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
  }),
  actions: {
    async login(username, password) {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      try {
        const res = await axios.post('http://localhost:8000/auth/login', formData);
        this.token = res.data.access_token;
        this.role = res.data.role;
        localStorage.setItem('token', this.token);
        localStorage.setItem('role', this.role);
        return true;
      } catch (e) {
        console.error(e);
        return false;
      }
    },
    logout() {
      this.token = null;
      this.role = null;
      localStorage.removeItem('token');
      localStorage.removeItem('role');
    }
  }
});