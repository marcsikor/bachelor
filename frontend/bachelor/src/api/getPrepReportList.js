import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const getPrepReportList = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/get-prep-list`)
        if (response.status === 200) {
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error getting report list: ", error.message);
        return "failure";
    }
};

export const getPrepHistory = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/get-prep-history`)
        if (response.status === 200) {
            return response.data
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error getting report list: ", error.message);
        return "failure";
    }
};


