export const ROLES =["admin", "staff", "direction"] as const;

export type Role = (typeof ROLES)[number];

export interface AuthUser {
    username: string;
    role: Role;
    restaurant_id: number | null;
}

export function isRole(value: unknown): value is Role {
    return typeof value === "string" && (ROLES as readonly string[]).includes(value);
}