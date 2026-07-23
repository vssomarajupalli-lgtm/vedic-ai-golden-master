import type { StateStorage } from 'zustand/middleware';

const DB_NAME = 'VedicAI_DB';
const STORE_NAME = 'zustand_store';
const DB_VERSION = 1;

let dbPromise: Promise<IDBDatabase> | null = null;

const getDb = (): Promise<IDBDatabase> => {
  if (!dbPromise) {
    dbPromise = new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME);
        }
      };
    });
  }
  return dbPromise;
};

export const idbStorage: StateStorage = {
  getItem: async (name: string): Promise<string | null> => {
    const db = await getDb();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(STORE_NAME, 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(name);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        let result = request.result;
        
        // Migration: If not found in IndexedDB, fallback to localStorage
        if (result === undefined) {
          const localData = localStorage.getItem(name);
          if (localData !== null) {
            result = localData;
          }
        }
        
        resolve(result || null);
      };
    });
  },
  
  setItem: async (name: string, value: string): Promise<void> => {
    const db = await getDb();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(STORE_NAME, 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(value, name);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  },
  
  removeItem: async (name: string): Promise<void> => {
    const db = await getDb();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(STORE_NAME, 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.delete(name);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  },
};
