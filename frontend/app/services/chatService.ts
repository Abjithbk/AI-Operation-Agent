import api from "../lib/axios";

export async function sendChatMessage(question:string):Promise<string> {

    const res = await api.post<{answer : string}>("/chat",{question});
    return res.data.answer
    
}