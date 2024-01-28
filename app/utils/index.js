import axios from 'axios';

export const sendImage = async (uri) => {
   try {
    const formData = new FormData();
    formData.append("image", {
      uri: uri,
      name: uri.split('/').pop(),
      type: 'image/jpg'
  });
    console.log(formData)
    const response = await axios.post("https://e40c-192-197-121-94.ngrok-free.app/api/photo", 
    formData,
    {
        headers: { "Content-Type": "multipart/form-data" }
    });
    console.log(response.data)
    return response.data;
   } catch (error) {
         console.error(error);
    }
}