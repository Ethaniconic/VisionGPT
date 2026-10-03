import ImageUploader from "../components/ImageUploader"

const Workspace = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white shadow-sm p-4">
        <h1 className="text-xl font-bold text-gray-800">VisionGPT Workspace</h1>
      </header>

      <main className="flex-grow flex items-start justify-center pt-10 px-4">
        <ImageUploader />
      </main>
    </div>
  );
}

export default Workspace