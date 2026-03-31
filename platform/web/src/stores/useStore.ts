import { create } from 'zustand';

interface AppState {
  currentPage: string;
  setCurrentPage: (page: string) => void;
  notification: { type: 'success' | 'error' | 'info'; message: string } | null;
  setNotification: (n: AppState['notification']) => void;
  clearNotification: () => void;
}

export const useStore = create<AppState>((set) => ({
  currentPage: 'knowledge',
  setCurrentPage: (page) => set({ currentPage: page }),
  notification: null,
  setNotification: (n) => set({ notification: n }),
  clearNotification: () => set({ notification: null }),
}));
