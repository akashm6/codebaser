import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "codebaser",
  description: "Navigate unfamiliar codebases!",
  openGraph: {
    title: "Codebaser – Understand Any Codebase",
    description: "Navigate unfamiliar codebases by asking questions on what you're confused about!",
    images: ["https://i.ibb.co/ymdJqVgz/ographimage.png"], 
    url: "https://codebaser.vercel.app/",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Toaster position="top-center"></Toaster>
        {children}
      </body>
    </html>
  );
}
