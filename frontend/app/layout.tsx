"use client";
import { Inter } from "next/font/google";
import "./globals.css";
import NotificationProvider from "@/components/ui/NotificationProvider";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`}>
        <NotificationProvider>{children}</NotificationProvider>
      </body>
    </html>
  );
}
