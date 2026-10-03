import { useState } from "react";
import { uploadImage } from "../services/api";

const ImageUploader = () => {
  const [status, setStatus] = useState("Idle");
  const [result, setResult] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setStatus("Error: Not an image file.");
      return;
    }

    setStatus("Uploading...");
    setResult(null);

    try {
      const data = await uploadImage(file);
      setStatus("Success!");
      setResult(`Processed: ${data.width}x${data.height}`);
    } catch (err) {
      setStatus("Error");
      setResult(err.message);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg bg-white shadow-sm max-w-md mx-auto mt-10">
      <label className="cursor-pointer group">
        <span className="block text-lg font-medium text-gray-700 group-hover:text-blue-600 transition">
          Click to upload an image
        </span>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="hidden"
        />
      </label>

      <div className="mt-4 text-sm flex flex-col items-center">
        <div className="flex items-center gap-2">
          {status === "Uploading..." && <span className="loading loading-spinner loading-md text-primary"></span>}
          <p className={`font-bold ${status === 'Success!' ? 'text-green-600' : status === 'Error' ? 'text-red-600' : 'text-gray-500'}`}>
            {status}
          </p>
        </div>
        {result && <p className={`text-xs mt-1 ${status === 'Error' ? 'text-red-600 font-semibold' : 'text-gray-500'}`}>{result}</p>}
      </div>
    </div>
  );
}

export default ImageUploader