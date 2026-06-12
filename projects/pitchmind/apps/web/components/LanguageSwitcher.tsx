import { Link, usePathname } from "@/i18n/routing";
import { useLocale } from "next-intl";

export function LanguageSwitcher() {
  const locale = useLocale();
  const pathname = usePathname();

  return (
    <div className="flex gap-1 text-sm">
      {(["en", "id"] as const).map((lang) => (
        <Link
          key={lang}
          href={pathname}
          locale={lang}
          className={`px-2 py-1 rounded uppercase ${
            locale === lang
              ? "bg-indigo-600 text-white"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          {lang}
        </Link>
      ))}
    </div>
  );
}
