import axios from "axios";
import { useState } from "react";

export default function Upload() {
  const backend_url = import.meta.env.VITE_API_URL
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (selectedFile) => {
    if (selectedFile) {
      setFile(selectedFile);
      console.log(file)
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const handleUpload = async () =>{
    const formdata = new FormData()
    formdata.append("file",file)
      const response = await axios.post(backend_url + "/uploadfile", formdata)
      console.log(response.data.message)
      alert(response.data.message)
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4 relative overflow-hidden">
      
      {/* Background decoration */}
      <div className="absolute -top-37.5 -left-37.5 w-100 h-100 bg-blue-600/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-37.5 -right-37.5 w-100 h-100 bg-purple-600/20 rounded-full blur-3xl" />

      {/* Main Card */}
      <div className="relative w-full max-w-xl">
        <div className="bg-white/6 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">

          {/* Header */}
          <div className="text-center mb-8">
            <div className="mx-auto mb-4 w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-400/20 flex items-center justify-center">
              <svg
                className="w-7 h-7 text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="1.8"
                  d="M7 16a4 4 0 01-.88-7.903A5.002 5.002 0 0116.9 6H17a5 5 0 011 9.9M12 12v9m0-9l-4 4m4-4l4 4"
                />
              </svg>
            </div>

            <h1 className="text-3xl font-bold text-white">
              Upload your file
            </h1>

            <p className="text-slate-400 mt-2 text-sm">
              Upload a document and let us take care of the rest.
            </p>
          </div>

          {/* Upload Area */}
          {!file ? (
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              className={`relative border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-200 ${
                isDragging
                  ? "border-blue-400 bg-blue-500/10 scale-[1.01]"
                  : "border-slate-700 hover:border-blue-500/60 hover:bg-white/2"
              }`}
            >
              {/* Upload Icon */}
              <div className="mx-auto mb-5 w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center">
                <svg
                  className="w-8 h-8 text-blue-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="1.7"
                    d="M12 16V4m0 0L8 8m4-4l4 4M5 20h14"
                  />
                </svg>
              </div>

              <p className="text-white font-medium">
                Drag & drop your file here
              </p>

              <p className="text-slate-500 text-sm my-2">
                or
              </p>

              <label className="inline-block cursor-pointer">
                <span className="inline-flex items-center px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition">
                  Browse files
                </span>

                <input
                  type="file"
                  className="hidden"
                  onChange={(e) => handleFile(e.target.files[0])}
                />
              </label>

              <p className="text-xs text-slate-500 mt-5">
                PDF, PNG, JPG or DOCX • Max 10MB
              </p>
            </div>
          ) : (
            /* Selected File */
            <div className="border border-white/10 bg-slate-900/70 rounded-2xl p-5">

              <div className="flex items-center gap-4">
                {/* File Icon */}
                <div className="w-12 h-12 shrink-0 rounded-xl bg-blue-500/10 flex items-center justify-center">
                  <svg
                    className="w-6 h-6 text-blue-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.7"
                      d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.7"
                      d="M14 2v6h6M8 13h8M8 17h5"
                    />
                  </svg>
                </div>

                {/* File Info */}
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium truncate">
                    {file.name}
                  </p>

                  <p className="text-sm text-slate-500 mt-1">
                    {formatFileSize(file.size)}
                  </p>
                </div>

                {/* Remove */}
                <button
                  onClick={() => setFile(null)}
                  className="w-9 h-9 rounded-lg hover:bg-red-500/10 text-slate-500 hover:text-red-400 transition flex items-center justify-center"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              {/* Upload Button */}
              <button
                onClick={handleUpload}
                className="w-full mt-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium transition shadow-lg shadow-blue-600/20"
              >
                Upload File
              </button>
            </div>
          )}

          {/* Footer */}
          <div className="flex items-center justify-center gap-2 mt-6 text-xs text-slate-500">
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-5a2 2 0 00-2-2H6a2 2 0 00-2 2v5a2 2 0 002 2zm10-9V7a4 4 0 00-8 0v3h8z"
              />
            </svg>

            Your files are securely processed
          </div>
        </div>
      </div>
    </div>
  );
}