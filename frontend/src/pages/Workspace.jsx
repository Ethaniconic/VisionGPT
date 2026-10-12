import { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import VisionChat from "../components/VisionChat";

const Workspace = () => {
  const [file, setFile] = useState(null);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white shadow-sm p-4">
        <h1 className="text-xl font-bold text-gray-800">VisionGPT Workspace</h1>
      </header>

      <main className="flex-grow flex flex-col items-center justify-center pt-10 px-4 gap-6">
        <ImageUploader onFileSelect={setFile} />
        <VisionChat selectedFile={file} />
      </main>
    </div>
  );
};

export default Workspace;