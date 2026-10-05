export interface Restaurant {
    id: number;
    name: string;
    city: string;
    address: string | null;
    is_open: boolean;
    opening_hours: string | null;
    contact: string | null;
}