import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const editReport = async (form) => {
    try {
        // form.append('createdTimestamp', new Date())
        const response = await axios.post(`${BASE_URL}/update-report`, form, { headers: {'Content-Type': 'multipart/form-data'}});
        if (response.status === 200) {
            console.log("Updated document successfully");
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error saving report: ", error.message);
        return "failure";
    }
};