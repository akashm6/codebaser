"use client";
import { useState } from "react";

export default function ZipUploader() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setStatus] = useState("Idle");

  const handleFileChange = async (e: any) => {
    const selected = e.target.files?.[0];
    if (!selected || !selected.name.endsWith(".zip")) return;
    setFile(selected);

    const payload = {
        name: selected.name,
        content_type: selected.type,
        size: selected.size
    }

    const res = await fetch(`http://localhost:8000/generate-presigned-url?filename=${selected.name}&content_type=${selected.type}`);
    const { url, key } = await res.json();

    await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": selected.type },
      body: selected,
    });

    const res2 = await fetch("http://localhost:8000/zip-processing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    setStatus("Uploaded and processing started");
  };

  return (
    <div className="p-4 border rounded">
      <input type="file" accept=".zip" onChange={handleFileChange} />
      <p>Status: {uploadStatus}</p>
    </div>
  );
}
