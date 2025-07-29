"use client";
import { useState } from "react";

export default function ZipUploader() {

  const FASTAPI_BACKEND = process.env.NEXT_PUBLIC_FASTAPI_BACKEND;

  const [file, setFile] = useState(null);
  const [uploadStatus, setStatus] = useState("Idle");

  const handleFileChange = async (e: any) => {
    const selected = e.target.files?.[0];
    if (!selected || !selected.name.endsWith(".zip")) return;
    setFile(selected);

    const res = await fetch(
      ` ${FASTAPI_BACKEND}/generate-presigned-url?filename=${selected.name}&content_type=${selected.type}`
    );
    const { url, key } = await res.json();

    const payload = {
    s3_key: key,
    name: selected.name,
    content_type: selected.type,
    size: selected.size,

    };

    await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": selected.type },
      body: selected,
    });

    const res2 = await fetch(`${FASTAPI_BACKEND}/zip-processing`, {
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
