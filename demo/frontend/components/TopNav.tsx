"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/graphemizer", label: "Graphemizer" },
  { href: "/metrics", label: "Metrics" },
  { href: "/decompose", label: "Decomposition" },
];

export function TopNav() {
  const pathname = usePathname();
  return (
    <header className="border-b border-slate-200">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-baseline gap-2">
          <span className="font-mono text-xl font-bold tracking-tight text-ink">
            graphemes
            <span className="text-slate-400">++</span>
          </span>
        </Link>
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
                    ? "bg-ink text-white"
                    : "text-slate-600 hover:bg-slate-100")
                }
              >
                {l.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
