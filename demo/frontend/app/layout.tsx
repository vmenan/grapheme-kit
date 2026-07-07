import type { Metadata } from "next";
import "./globals.css";
import { TopNav } from "@/components/TopNav";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "graphemeKit",
  description:
    "Grapheme-aware segmentation, evaluation metrics (chrF, chrF++, CER, CharBLEU), distance measures, and Tamil/Sinhala decomposition and composition.",
};

// Sets the `dark` class before hydration so there's no flash of the wrong theme.
const THEME_INIT = `
(function() {
  try {
    var stored = localStorage.getItem('theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var isDark = stored ? stored === 'dark' : prefersDark;
    if (isDark) document.documentElement.classList.add('dark');
  } catch (e) {}
})();
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_INIT }} />
      </head>
      <body className="flex min-h-screen flex-col">
        <TopNav />
        <main className="mx-auto w-full max-w-6xl flex-1 px-6 py-8">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
