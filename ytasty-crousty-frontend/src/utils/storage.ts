export const STORAGE_KEYS = {
    token: "ytasty.token",
    selectedRestaurantId: "ytasty.selectedRestaurantId",
} as const;

export function safeGet(key: string): string | null {
    try {
        return localStorage.getItem(key);
    } catch {
        return null;
    }
}

export function safeSet(key: string, value:string): void {
    try {
        localStorage.setItem(key, value);
    } catch{
    }
}

export function safeRemove(key: string): void {
    try {
        localStorage.removeItem(key);
    } catch {
    }
}