import { createServerClient } from "@supabase/ssr";
import createIntlMiddleware from "next-intl/middleware";
import { type NextRequest, NextResponse } from "next/server";
import { routing } from "./i18n/routing";

const intlMiddleware = createIntlMiddleware(routing);

const protectedPattern = /^\/(en|id)\/(dashboard|onboarding)/;

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (protectedPattern.test(pathname)) {
    const locale = pathname.split("/")[1] ?? routing.defaultLocale;
    let response = NextResponse.next({ request });

    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() {
            return request.cookies.getAll();
          },
          setAll(cookiesToSet) {
            cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
            response = NextResponse.next({ request });
            cookiesToSet.forEach(({ name, value, options }) =>
              response.cookies.set(name, value, options),
            );
          },
        },
      },
    );

    const { data } = await supabase.auth.getUser();
    if (!data.user) {
      return NextResponse.redirect(new URL(`/${locale}/login`, request.url));
    }
  }

  return intlMiddleware(request);
}

export const config = {
  matcher: ["/", "/(en|id)/:path*"],
};
