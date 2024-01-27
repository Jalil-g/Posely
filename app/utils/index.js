import axios from 'axios';

export const sendImage = async (base64) => {
   try {
    console.log(base64.slice(0, 50))
    const response = await axios.post("https://de8b-142-157-196-117.ngrok-free.app/api/photo", 
    {image: base64},
    {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }
    });
    console.log(response.data)
    return response.data;
   } catch (error) {
         console.error(error);
    }
}