import type { LayoutLoad } from './$types'
import { locale, loadTranslations } from '$lib/translations';
export const load: LayoutLoad = async ({ url }) => {
  const { pathname } = url;
  const defaultLocale = 'en'; // get from cookie, user session, ...
  const initLocale = locale.get() || defaultLocale; // set default if no locale already set
  await loadTranslations(initLocale, pathname); // keep this just before the `return`
  return {};
}
