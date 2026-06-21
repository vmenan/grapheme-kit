import type { Metadata } from "next";
import "./globals.css";
import { TopNav } from "@/components/TopNav";

export const metadata: Metadata = {
  title: "graphemes++ · Tamil & Sinhala grapheme tools",
  description:
    "Grapheme-level segmentation, decomposition and evaluation metrics (chrF, chrF++, CER, Levenshtein) for Tamil and Sinhala.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <TopNav />
        <main className="mx-auto w-full max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
