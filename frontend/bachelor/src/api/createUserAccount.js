import axios from "axios";
import { BASE_URL } from "./serverAddress.js"

export const createUserAccount = async (email_param, name_param, surname_param, position_param) => {
    try {
        //console.log('pls be alive')
        //console.log(this_email + '  ' + this_password)
        const response = await axios.post(`${BASE_URL}/add-user`, {
            email: email_param,
            name: name_param,
            surname: surname_param,
            position: position_param
        });
        if (response.status === 200) {
            console.log("Added new user successfully");
        } else {
            return "failure";
        }
    } catch (error) {
        console.error("Error adding user: ", error.message);
        return "failure";
    }
};