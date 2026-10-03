const BASE_URL = "http://localhost:8000";

export const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch(`${BASE_URL}/vision/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok){
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (err) {
        console.error("Upload failed:", err);
        throw err;
    }
}