import api from "../lib/axios";
import { BackendIncident } from "../types/incident";

export async function fetchIncidents(): Promise<BackendIncident[]> {

    const response = await api.get<BackendIncident[]>("/logs/analyse");
    console.log(response.data)
    return response.data
    
}