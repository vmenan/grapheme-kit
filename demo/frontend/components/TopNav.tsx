"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "@/components/ThemeToggle";

const links = [
  { href: "/graphemizer", label: "Graphemizer" },
  { href: "/metrics", label: "Metrics" },
  { href: "/canonicalization", label: "Canonicalization" },
];

export function TopNav() {
  const pathname = usePathname();
  return (
    <header className="border-b border-slate-200 dark:border-slate-800">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-baseline gap-2">
          <span className="font-mono text-xl font-bold tracking-tight text-ink">
            grapheme
            <span className="text-slate-400">Kit</span>
          </span>
        </Link>
        <div className="flex items-center gap-2">
          <nav className="flex items-center gap-1">
            {links.map((l) => {
              const active = pathname?.startsWith(l.href);
              return (
                <Link
                  key={l.href}
                  href={l.href}
                  className={
                    "rounded-md px-3 py-1.5 text-sm font-medium transition " +
                    (active
                      ? "bg-ink text-white dark:text-slate-900"
                      : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800")
                  }
                >
                  {l.label}
                </Link>
              );
            })}
          </nav>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
