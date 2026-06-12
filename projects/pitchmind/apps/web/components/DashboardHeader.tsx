import { LanguageSwitcher } from "@/components/LanguageSwitcher";
import { Link } from "@/i18n/routing";

type Props = {
  title: string;
  backHref?: string;
  backLabel?: string;
};

export function DashboardHeader({ title, backHref, backLabel }: Props) {
  return (
    <header className="border-b border-slate-800 px-4 sm:px-6 py-4 flex flex-wrap gap-3 justify-between items-center">
      <div className="flex items-center gap-4 min-w-0">
        <Link href="/dashboard" className="font-bold text-indigo-400 shrink-0">
          PitchMind
        </Link>
        {backHref && backLabel && (
          <Link href={backHref} className="text-sm text-slate-400 hover:text-indigo-400 truncate">
            ← {backLabel}
          </Link>
        )}
        <span className="text-sm text-slate-400 truncate hidden sm:inline">{title}</span>
      </div>
      <LanguageSwitcher />
    </header>
  );
}
