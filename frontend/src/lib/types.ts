export type Event = {
    id?: number;
    name: string;
    start_date: Date;
    end_date: Date;
    description?: string;
    location?: string;
    recurrence?: string;
};
