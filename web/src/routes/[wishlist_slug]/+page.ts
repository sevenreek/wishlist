import { fetchWishlist } from '$lib/api/wishlist';
import type { PageLoad, PageLoadEvent } from './$types'

export const load: PageLoad = async ({ params }: PageLoadEvent) => {
  const wishlist = await fetchWishlist(params.wishlist_slug);
  return wishlist;
}

