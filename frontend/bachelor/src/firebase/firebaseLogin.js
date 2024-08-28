import { signInWithEmailAndPassword } from "firebase/auth"; 
import { auth } from "./firebaseCredentials";

export const firebaseLogin = async (email, password) => {
  try {
    await signInWithEmailAndPassword(auth, email, password);
    return "success"
  } catch (error) {
    console.error("Error logging in: ", error.message);
    return "failure"
  }
};