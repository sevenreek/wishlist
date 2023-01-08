import {fetchWishlist} from '$lib/api/wishlist'

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
  const items = await fetchWishlist(params.wishlist_slug)
  return items
}

