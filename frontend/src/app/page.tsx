"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { motion } from "framer-motion";
import { Github } from "lucide-react";
import { toast } from "sonner";
import { Progress } from "@/components/ui/progress";

export default function Home() {
  const router = useRouter();
  const [zipFile, setZipFile] = useState<File | null>(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const FASTAPI_BACKEND = process.env.NEXT_PUBLIC_FASTAPI_BACKEND;

  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    setIsAuthenticated(!!token);
  }, []);

  async function handleZipUpload() {
    if (!zipFile) {
      toast.error("Please select a file");
      return;
    }

    if (!isAuthenticated) {
      return toast.error("Please login with GitHub first!", {
        description: "This keeps your uploads private to your account.",
        action: {
          label: "Got it",
          onClick: () => {},
        },
      });
    }
    setIsUploading(true);

    const token = localStorage.getItem("auth_token");
    const res = await fetch(
      `${FASTAPI_BACKEND}/generate-presigned-url?filename=${zipFile.name}&content_type=${zipFile.type}`
    );
    const { url, key } = await res.json();

    await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": zipFile.type },
      body: zipFile,
    });

    const payload = {
      s3_key: key,
      name: zipFile.name,
      content_type: zipFile.type,
      size: zipFile.size,
    };

    const res2 = await fetch(`${FASTAPI_BACKEND}/zip-processing`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (res2.ok) {
      toast.success("Upload complete!");
      router.push("/workspace");
    } 
    else if (res2.status === 401) {
      return toast.error("Please login with GitHub first!", {
        description: "This keeps your uploads private to your account.",
        action: {
          label: "Got it",
          onClick: () => {},
        },
      });
    }
    else {
      toast.error("Processing failed");
    }
    
    setIsUploading(false);
  }

  async function handleGithubZip() {
    if (!isAuthenticated) {
      return toast.error("Please login with GitHub first!", {
        description: "This keeps your uploads private to your account.",
        action: {
          label: "Got it",
          onClick: () => {},
        },
      });
    }

    if (!githubUrl) return toast.error("Enter a GitHub repo URL");
    setIsUploading(true);

    const token = localStorage.getItem("auth_token");
    const res = await fetch(`${FASTAPI_BACKEND}/github-process`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ url: githubUrl }),
    });
    if (res.ok) {
      toast.success("GitHub repo processed!");
      router.push("/workspace");
    } else if (res.status === 401) {
      return toast.error("Please login with GitHub first!", {
        description: "This keeps your uploads private to your account.",
        action: { label: "Got it", onClick: () => {} },
      });
    } else {
      toast.error("GitHub repo processing failed");
    }
    setIsUploading(false);
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-16 bg-background text-white">
      <div className="absolute top-6 w-full px-6 flex items-center justify-between">
        <div className="text-xl text-black font-semibold tracking-tight">
          codebaser
        </div>
        <Button
          variant="secondary"
          onClick={() =>
            window.open("https://github.com/akashm6/codebaser", "_blank")
          }
          className="gap-2 hover:scale-105 transition-transform"
        >
          <Github className="w-4 h-4" />
          GitHub
        </Button>
      </div>

      <div className="text-center mb-8">
        <h1 className="text-5xl md:text-5xl text-black font-bold mb-4 tracking-tight">
          Understand Any Codebase Instantly
        </h1>
        <p className="text-muted-foreground text-lg max-w-2xl mx-auto mb-6">
          Upload a zip file or GitHub repo and start asking questions about your
          code with AI-powered context awareness.
        </p>
      </div>

      {!isAuthenticated && (
        <p className="text-sm text-muted-foreground mb-6">
          You must log in to upload or process a repository.
        </p>
      )}

      <Card className="w-full max-w-md border border-border bg-card/50 backdrop-blur rounded-2xl shadow-md">
        <CardHeader>
          <CardTitle className="text-xl">Upload or Link a Repo</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="zip" className="w-full">
            <TabsList className="w-full grid grid-cols-2">
              <TabsTrigger value="zip">ZIP Upload</TabsTrigger>
              <TabsTrigger value="github">GitHub Repo</TabsTrigger>
            </TabsList>

            <TabsContent value="zip" className="mt-4 space-y-4">
              <Input
                type="file"
                accept=".zip"
                onChange={(e) => {
                  if (!isAuthenticated) {
                    e.target.value = "";
                    return toast.error("Please login with GitHub first!", {
                      description:
                        "This keeps your uploads private to your account.",
                      action: { label: "Got it", onClick: () => {} },
                    });
                  }
                  setZipFile(e.target.files?.[0] || null);
                }}
              />
              <Button
                onClick={handleZipUpload}
                disabled={isUploading}
                className="w-full"
              >
                {isUploading ? "Uploading..." : "Upload & Analyze"}
              </Button>
              {isUploading && (
                <div className="mt-4 space-y-2 text-center">
                  <Progress value={100} className="animate-pulse h-2 w-full" />
                  <p className="text-sm text-muted-foreground">
                    Processing… This may take up to a minute or two for larger
                    repos.
                  </p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="github" className="mt-4 space-y-4">
              <Input
                placeholder="https://github.com/user/repo"
                value={githubUrl}
                onChange={(e) => {
                  if (!isAuthenticated) {
                    return toast.error("Please login with GitHub first!", {
                      description:
                        "This keeps your uploads private to your account.",
                      action: { label: "Got it", onClick: () => {} },
                    });
                  }
                  setGithubUrl(e.target.value);
                }}
              />
              <Button
                onClick={handleGithubZip}
                disabled={isUploading}
                className="w-full"
              >
                {isUploading ? "Processing..." : "Process GitHub Repo"}
              </Button>
              {isUploading && (
                <div className="mt-4 space-y-2 text-center">
                  <Progress value={100} className="animate-pulse h-2 w-full" />
                  <p className="text-sm text-muted-foreground">
                    Processing… This may take up to a minute or two for larger
                    repos.
                  </p>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
      <Button
        onClick={() =>
          (window.location.href = `${FASTAPI_BACKEND}/auth/github/login`)
        }
        className="mt-6 gap-2 hover:scale-105 transition-transform"
      >
        <Github className="w-4 h-4" />
        Login with GitHub
      </Button>
      <motion.a
        href="#demo"
        animate={{ y: [0, -8, 0] }}
        transition={{ repeat: Infinity, duration: 1.5 }}
        className="mt-20 text-muted-foreground text-sm cursor-pointer"
      >
        ↓ Scroll to see how it works ↓
      </motion.a>
      <div className="mt-40">
        <h2 className="text-2xl md:text-3xl text-black font-semibold mb-4 text-center">
          See Codebaser in Action
        </h2>
        <video
          src="/demo.mp4"
          autoPlay
          loop
          muted
          playsInline
          className="size-auto rounded-xl shadow-lg border border-border"
        />
        <p className="text-muted-foreground text-sm mt-4 text-center">
          Watch how Codebaser chunks, summarizes, and answers questions about
          your codebase.
        </p>
      </div>
    </main>
  );
}
